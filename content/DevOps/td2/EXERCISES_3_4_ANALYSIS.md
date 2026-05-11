# Exercises 3 & 4 : Ansible Idempotency & Multi-Instance Deployment

## Exercise 3 : Test d'idempotence

### Objectif
Relancer le playbook `configure_sample_app_playbook.yml` une deuxième fois et observer quel comportement est produit.

### Concept : Idempotence dans Ansible

**Définition** : Un playbook est idempotent s'il peut être relancé plusieurs fois sans changements d'état indésirables du système. Cela signifie :
- Tasks marquées `changed_when: false` ou `state: present` (idempotentes) ne signalent PAS de changement à la deuxième exécution.
- Tasks sans gestion de l'idempotence (comme `shell` brutes) peuvent TOUJOURS signaler un changement.

### Analyse du rôle `sample-app/tasks/main.yml`

#### Task 1 : Install Node.js setup repository
```yaml
- name: Install Node.js setup repository
  shell: curl -fsSL https://rpm.nodesource.com/setup_21.x | bash -
  args:
    creates: /etc/yum.repos.d/nodesource-el8.repo
  changed_when: false
```
**Comportement idempotent ?** OUI
- `creates:` — si le fichier existe, la tâche ne s'exécute pas.
- `changed_when: false` — ne marque jamais comme changé (même si relanc).
- **Deuxième exécution** : `skipped` (car le fichier existe déjà).

#### Task 2 : Install Node.js
```yaml
- name: Install Node.js
  yum:
    name: nodejs
    state: present
```
**Comportement idempotent ?** OUI
- `state: present` — module `yum` est conçu pour être idempotent.
- Si le paquet est déjà installé, il ne fait rien et marque `ok` (pas de changement).
- **Deuxième exécution** : `ok` (car nodejs est déjà installé).

#### Task 3 : Copy sample app
```yaml
- name: Copy sample app
  copy:
    src: app.js
    dest: /home/ec2-user/app.js
    owner: ec2-user
    group: ec2-user
    mode: '0755'
```
**Comportement idempotent ?** OUI
- Module `copy` compare le contenu (checksums). Si le fichier existe et le contenu est identique, marque `ok`.
- **Deuxième exécution** : `ok` (sauf si le fichier `app.js` source a changé).

#### Task 4 : Check if app is already running
```yaml
- name: Check if app is already running
  shell: pgrep -f "node /home/ec2-user/app.js"
  register: app_running
  ignore_errors: yes
  changed_when: false
```
**Comportement idempotent ?** OUI
- Utilise une commande non-destructive (`pgrep`).
- `changed_when: false` — ne marque jamais de changement.
- **Deuxième exécution** : `ok` avec `app_running.rc` = 0 (processus trouvé).

#### Task 5 : Stop any existing app
```yaml
- name: Stop any existing app
  shell: pkill -f "node /home/ec2-user/app.js" || true
  when: app_running.rc == 0
  changed_when: false
```
**Comportement idempotent ?** PARTIEL
- `changed_when: false` — ne marque pas de changement.
- **Deuxième exécution** : `skipped` (car `app_running.rc != 0` après la première exécution qui a arrêté le processus).
- ⚠️ Problème : la première fois elle arrête l'app, mais elle ne remarque pas si l'arrêt a échoué.

#### Task 6 : Start sample app
```yaml
- name: Start sample app
  shell: nohup node /home/ec2-user/app.js > /tmp/app.log 2>&1 &
  args:
    chdir: /home/ec2-user/
  become_user: ec2-user
```
**Comportement idempotent ?** NON (problématique)
- `shell` brute sans condition.
- À chaque exécution, relance le `nohup` → crée un **nouveau processus** (dupliquant potentiellement les instances).
- **Deuxième exécution** : `changed` (car la commande s'exécute toujours).
- ⚠️ Risque : plusieurs instances de `node` en écoute sur le même port → conflit.

### Résultat attendu à la deuxième exécution

```
TASK [sample-app : Install Node.js setup repository] ... skipped
TASK [sample-app : Install Node.js] ..................... ok (no changes)
TASK [sample-app : Copy sample app] ..................... ok (no changes)
TASK [sample-app : Check if app is already running] .... ok (app found)
TASK [sample-app : Stop any existing app] .............. skipped (condition: False)
TASK [sample-app : Start sample app] ................... changed (launched again)
```

### Améliorations pour une meilleure idempotence

**Problème identifié** : La tâche "Start sample app" n'est pas idempotente. Elle redémarre l'app à chaque fois.

**Solution 1 : Conditionner le démarrage**
```yaml
- name: Start sample app (if not running)
  shell: nohup node /home/ec2-user/app.js > /tmp/app.log 2>&1 &
  when: app_running.rc != 0  # Ne lancer que si pas déjà en cours
  changed_when: false
```

**Solution 2 : Utiliser un service systemd** (meilleur)
Créer un fichier service pour gérer l'app comme un vrai service :
```yaml
- name: Create systemd service for app
  copy:
    dest: /etc/systemd/system/sample-app.service
    content: |
      [Unit]
      Description=Sample Node.js App
      After=network.target
      
      [Service]
      Type=simple
      User=ec2-user
      ExecStart=/usr/bin/node /home/ec2-user/app.js
      Restart=on-failure
      
      [Install]
      WantedBy=multi-user.target

- name: Start and enable service
  systemd:
    name: sample-app
    state: started
    enabled: yes
    daemon_reload: yes
```
Avec cette approche, redémarrer le playbook ne crée pas de doublons — `systemd` gère l'idempotence.

---

## Exercise 4 : Déployer sur plusieurs instances

### Objectif
Modifier le playbook de création pour lancer **2 ou 3 instances** en parallèle et mettre à jour l'inventaire pour les découvrir toutes.

### Approche 1 : Modifier le playbook de création

**Fichier : `create_ec2_instance_playbook.yml` (version multi-instance)**

```yaml
- name: Deploy multiple EC2 instances in AWS
  hosts: localhost
  gather_facts: no
  collections:
    - amazon.aws
  vars:
    instance_type: t3.micro
    image_id: ami-0900fe555666598a2
    instance_count: 3  # Nombre d'instances à créer
  environment:
    AWS_REGION: us-east-2
  tasks:
    - name: Create security group
      amazon.aws.ec2_security_group:
        name: sample-app-ansible
        description: Allow HTTP and SSH traffic
        rules:
          - proto: tcp
            ports: [8080]
            cidr_ip: 0.0.0.0/0
          - proto: tcp
            ports: [22]
            cidr_ip: 0.0.0.0/0
      register: aws_security_group

    - name: Create EC2 key pair
      amazon.aws.ec2_key:
        name: ansible-ch2
        file_name: ansible-ch2.key
      no_log: true
      register: aws_ec2_key_pair

    - name: Create multiple EC2 instances
      amazon.aws.ec2_instance:
        name: "sample-app-ansible-{{ item }}"  # Noms uniques : sample-app-ansible-0, -1, -2
        key_name: "{{ aws_ec2_key_pair.key.name }}"
        instance_type: "{{ instance_type }}"
        security_group: "{{ aws_security_group.group_id }}"
        image_id: "{{ image_id }}"
        wait: yes
        wait_timeout: 500
        tags:
          Ansible: ch2_instances
          Index: "{{ item }}"  # Tag pour identifier chaque instance
      register: ec2_instances
      loop: "{{ range(0, instance_count) | list }}"  # Boucle de 0 à instance_count-1

    - name: Display instance information
      debug:
        msg: "Instance {{ item.instances[0].instance_id }} created with IP {{ item.instances[0].public_ip_address }}"
      loop: "{{ ec2_instances.results }}"
```

**Modifications clés** :
- `instance_count: 3` — variable contrôlable.
- `loop: "{{ range(0, instance_count) | list }}"` — crée N instances.
- `name: "sample-app-ansible-{{ item }}"` — noms uniques.
- `tags: { Ansible: ch2_instances, Index: "{{ item }}" }` — identifier chaque instance.

### Approche 2 : Inventaire dynamique (découverte automatique)

**L'inventaire `inventory.aws_ec2.yml` fonctionne déjà !**

Grâce au filtre `tag:Ansible: ch2_instances`, Ansible découvre automatiquement **TOUTES** les instances tagguées, peu importe le nombre.

```yaml
plugin: amazon.aws.aws_ec2
regions:
  - us-east-2
filters:
  instance-state-name: running
  tag:Ansible: ch2_instances  # Découvre tous les instances avec ce tag
keyed_groups:
  - key: tags.Ansible
    leading_separator: ''
compose:
  ansible_host: public_ip_address
```

### Approche 3 : Lancer la configuration sur toutes les instances

**Le playbook `configure_sample_app_playbook.yml` cible déjà `_ch2_instances`.**

Grâce à l'inventaire dynamique, il s'exécute automatiquement sur TOUTES les instances découvertes :

```yaml
- name: Configure the EC2 instance to run a sample app
  hosts: _ch2_instances  # Cible tous les hôtes du groupe dynamique
  gather_facts: true
  become: true
  roles:
    - sample-app
```

### Résumé du workflow multi-instance

1. **Créer les instances** (avec le playbook modifié)
   ```bash
   ANSIBLE_PYTHON_INTERPRETER="$(which python3)" \
   AWS_PROFILE=labs-devops_diallo \
   ansible-playbook -v create_ec2_instance_playbook.yml \
     -e instance_count=3 \
     -e instance_type=t3.micro
   ```

2. **L'inventaire découvre automatiquement les 3 instances** (plugin aws_ec2 + filtre tag).

3. **Configurer toutes les instances en parallèle**
   ```bash
   ANSIBLE_PYTHON_INTERPRETER="$(which python3)" \
   AWS_PROFILE=labs-devops_diallo \
   ansible-playbook -i inventory.aws_ec2.yml -v configure_sample_app_playbook.yml
   ```
   Ansible se connecte à toutes les 3 instances en parallèle et exécute le rôle.

4. **Vérifier les 3 apps**
   ```bash
   for i in {1..3}; do
     # Récupérer l'IP de chaque instance (à adapter selon l'output)
     echo "Instance $i : $(curl -s http://INSTANCE_IP:8080/)"
   done
   ```

### Avantages

✅ Pas de changement de code nécessaire pour 2, 3 ou 10 instances.  
✅ L'inventaire dynamique s'adapte automatiquement.  
✅ Parallélisation automatique par Ansible.  
✅ Même configuration appliquée à toutes les instances.  

### Limitations

⚠️ Les instances partagent le même Security Group et key pair — adapter si isolation nécessaire.  
⚠️ Chaque instance obtient le même `Name=sample-app-ansible-*` — utiliser les tags `Index` ou numéro pour distinguer.  

---

## Conclusion

- **Exercise 3** : L'idempotence révèle les tâches mal écrites (comme "Start sample app" qui relance toujours l'app). Une bonne pratique : utiliser `changed_when: false`, `creates:`, ou `state: present` pour signaler les tâches idempotentes.

- **Exercise 4** : Grâce au plugin `aws_ec2` et aux tags, déployer N instances nécessite juste une modification de variable (`instance_count`) — l'inventaire et la configuration se font automatiquement.

