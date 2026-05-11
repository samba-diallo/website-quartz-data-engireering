# 📋 SYNTHÈSE — Exercices 3 & 4

---

## ✅ Exercice 3 : Idempotence — Résultats

### Question
*What happens if you run the configuration playbook a second time? Observe and explain.*

### Exécution pratique

Nous avons relancé le playbook `configure_sample_app_playbook.yml` **deux fois de suite** et capturé les résultats.

### Résultats observés

**1ère exécution** :
```
PLAY RECAP
ec2-3-142-134-207.us-east-2.compute.amazonaws.com : ok=6  changed=1  unreachable=0  failed=0  skipped=1
```

**2ème exécution** :
```
PLAY RECAP
ec2-3-142-134-207.us-east-2.compute.amazonaws.com : ok=6  changed=1  unreachable=0  failed=0  skipped=1
```

### 🔍 Analyse détaillée

| Tâche | 1ère | 2ème | Explication |
|-------|------|------|---|
| Gathering Facts | ok | ok | Collecte des variables — idempotent |
| Install Node.js setup repository | ok | ok | Le fichier de repo existe → skipped ou ok |
| Install Node.js | ok | ok | Package déjà installé → `yum` module est idempotent |
| Copy sample app | ok | ok | Le fichier `app.js` n'a pas changé → no change |
| Check if app running | failed (ignored) | failed (ignored) | Processus inexistant → `pgrep` retourne rc=1 |
| Stop any existing app | skipped | skipped | Condition `when: rc==0` → false → skip |
| **Start sample app** | **changed** | **changed** | ❌ **PROBLÈME** — elle s'exécute TOUJOURS |

### ⚠️ Problème d'idempotence identifié

La tâche **"Start sample app"** est écrite ainsi :

```yaml
- name: Start sample app
  shell: nohup node /home/ec2-user/app.js > /tmp/app.log 2>&1 &
  args:
    chdir: /home/ec2-user/
  become_user: ec2-user
```

**Problèmes** :
1. ❌ Pas de condition `when:` → s'exécute TOUJOURS
2. ❌ Pas de `changed_when: false` → marque TOUJOURS comme `changed`
3. ❌ Pas de vérification d'état → relance l'app même si elle tourne déjà
4. ❌ Résultat : **Chaque exécution crée un nouveau processus Node** → accumulation de processus sur le port 8080 → **conflit potentiel**

### ✅ Solutions proposées

#### Solution 1 : Idempotence minimale (ajouter condition + flag)
```yaml
- name: Start sample app
  shell: nohup node /home/ec2-user/app.js > /tmp/app.log 2>&1 &
  when: app_running.rc != 0        # ✅ Ne lance que si pas déjà actif
  changed_when: false               # ✅ Supprime le "changed"
```
**Résultat** : 2ème exécution → `skipped` (condition fausse)

#### Solution 2 : Meilleure pratique (systemd) — RECOMMANDÉE
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

- name: Enable and start service
  systemd:
    name: sample-app
    state: started
    enabled: yes
```
**Résultat** : Complètement idempotent — `systemd` gère l'idempotence automatiquement

### 📚 Leçons apprises

1. **Idempotence = Propriété clé d'Ansible** — les playbooks DOIVENT pouvoir être relancés sans effets indésirables
2. **Signes de non-idempotence** :
   - `shell:` ou `command:` sans conditions
   - Tâches qui modifient l'état sans vérifier l'état existant
   - Redémarrage/relancement sans détection de state
3. **Bonnes pratiques** :
   - Utiliser les modules de haut niveau (`yum:`, `copy:`, `systemd:`) — idempotents par défaut
   - Ajouter `when:` pour les tâches conditionnelles
   - Ajouter `changed_when:` pour contrôler le signalement de changements
   - Préférer les services systemd pour la gestion d'apps

### 📁 Fichiers fournis

- **Documentation détaillée** : `td2/EXERCISE_3_IDEMPOTENCE_ANALYSIS.md`
- **3 variantes du rôle** :
  - `roles/sample-app/tasks/main.yml` (actuelle — non-idempotente)
  - `roles/sample-app/tasks/main_idempotent.yml` (idempotente minimale)
  - `roles/sample-app/tasks/main_systemd.yml` (meilleure pratique)

---

## 🚀 Exercice 4 : Déploiement multi-instance

### Question
*Modify the playbook to deploy and configure multiple EC2 instances. How would you adjust the playbook and inventory?*

### Architecture proposée

#### Approche 1 : Modifier le playbook de création

**Fichier** : `create_ec2_instances_multi.yml`

```yaml
vars:
  instance_count: 2  # Nombre d'instances à créer

tasks:
  - name: Create multiple EC2 instances
    amazon.aws.ec2_instance:
      name: "sample-app-ansible-{{ item }}"  # Noms uniques
      ...
      tags:
        Ansible: ch2_instances
        Index: "{{ item }}"
    loop: "{{ range(0, instance_count | int) | list }}"  # Crée N instances
```

**Résultat** : Crée `instance_count` instances en boucle

#### Approche 2 : Inventaire découvre automatiquement

**Fichier** : `inventory.aws_ec2.yml` (inchangé)

```yaml
plugin: amazon.aws.aws_ec2
filters:
  tag:Ansible: ch2_instances  # Découvre TOUTES les instances avec ce tag
  instance-state-name: running
```

**Résultat** : Quelle que soit le nombre d'instances créées, l'inventaire les découvre toutes automatiquement dans le groupe `_ch2_instances`

#### Approche 3 : Configuration appliquée à tous les hôtes

**Fichier** : `configure_sample_app_playbook.yml` (inchangé)

```yaml
- name: Configure the EC2 instance to run a sample app
  hosts: _ch2_instances  # Cible TOUS les hôtes du groupe dynamique
```

**Résultat** : Ansible se connecte à TOUS les hôtes du groupe en parallèle et exécute la configuration

### 🎯 Workflow complet

```bash
# 1. Créer 3 instances
ANSIBLE_PYTHON_INTERPRETER="$(which python3)" \
AWS_PROFILE=labs-devops_diallo \
ansible-playbook -v create_ec2_instances_multi.yml \
  -e instance_count=3 \
  -e instance_type=t3.micro

# Attendre ~1-2 minutes que les instances se lancent

# 2. Découvrir les instances via inventaire dynamique
ansible-inventory -i inventory.aws_ec2.yml --list
# Affiche tous les hôtes du groupe _ch2_instances

# 3. Configurer TOUTES les instances en parallèle
ANSIBLE_PYTHON_INTERPRETER="$(which python3)" \
AWS_PROFILE=labs-devops_diallo \
ansible-playbook -i inventory.aws_ec2.yml configure_sample_app_playbook.yml
# Ansible lance 3 connexions SSH en parallèle → configuration rapide

# 4. Tester les 3 apps
aws ec2 describe-instances \
  --filters "Name=tag:Ansible,Values=ch2_instances" \
  --query 'Reservations[].Instances[].[PublicIpAddress,InstanceId]' \
  --output table \
  --profile labs-devops_diallo --region us-east-2

# Puis curl chaque IP:8080
for IP in $(aws ec2 ... --output text); do
  echo "Testing $IP:8080..."
  curl -s "http://$IP:8080/" || echo "Failed"
done
```

### ✨ Avantages du design

✅ **Scalabilité** : Changer `instance_count` de 2 à 10 ne change rien d'autre  
✅ **Inventaire auto-découvert** : Le plugin `aws_ec2` voit toutes les instances tagguées  
✅ **Parallélisation** : Ansible se connecte aux N instances **en parallèle** (pas séquentiellement)  
✅ **Même config** : Tous les hôtes reçoivent exactement la même configuration  
✅ **Pas de duplicate** : Les instances ne se gênent pas (chacune sa clé, son IP)  

### 📊 Comparaison : 1 vs N instances

| Aspect | 1 instance | N instances |
|--------|-----------|------------|
| Playbook création | `loop: 1` ou pas de boucle | `loop: range(0, N)` |
| Inventaire | Découvre 1 hôte | Découvre N hôtes automatiquement |
| Configuration | Cible 1 hôte | Cible N hôtes en parallèle |
| Changement pour passer à 5 instances | Rewrite tout | Juste `-e instance_count=5` |

### 📁 Fichiers fournis

- **Playbook multi-instance** : `scripts/ansible/create_ec2_instances_multi.yml`
- **Script d'exécution** : `scripts/ansible/exercise_4_multi_instance.sh`
  ```bash
  ./exercise_4_multi_instance.sh 3  # Crée 3 instances, configure toutes
  ```
- **Documentation** : `td2/EXERCISES_3_4_ANALYSIS.md`

### 🧹 Nettoyage multi-instance

```bash
# Lister les instances
aws ec2 describe-instances \
  --filters "Name=tag:Ansible,Values=ch2_instances" "Name=instance-state-name,Values=running" \
  --query 'Reservations[].Instances[].[InstanceId,Tags[?Key==`Name`].Value|[0]]' \
  --output table \
  --profile labs-devops_diallo --region us-east-2

# Terminer toutes les instances d'un coup
aws ec2 terminate-instances \
  --instance-ids i-xxx i-yyy i-zzz ... \
  --profile labs-devops_diallo --region us-east-2

# Nettoyer SG et clé
aws ec2 delete-security-group --group-name sample-app-ansible \
  --profile labs-devops_diallo --region us-east-2
aws ec2 delete-key-pair --key-name ansible-ch2 \
  --profile labs-devops_diallo --region us-east-2
```

---

## 📚 Fichiers d'accompagnement

| Fichier | Description |
|---------|-----------|
| `td2/EXERCISE_3_IDEMPOTENCE_ANALYSIS.md` | Analyse détaillée de l'idempotence avec solutions |
| `td2/EXERCISES_3_4_ANALYSIS.md` | Explications concepts et approches pour les deux exercices |
| `td2/LABS_EXERCISES_3_4_SUMMARY.md` | Ce document — récapitulatif complet |
| `scripts/ansible/create_ec2_instances_multi.yml` | Playbook pour créer N instances |
| `scripts/ansible/roles/sample-app/tasks/main_idempotent.yml` | Version idempotente minimale du rôle |
| `scripts/ansible/roles/sample-app/tasks/main_systemd.yml` | Version avec systemd (meilleure pratique) |
| `scripts/ansible/exercise_3_idempotency.sh` | Script pour tester idempotence |
| `scripts/ansible/exercise_4_multi_instance.sh` | Script pour déployer N instances |

---

## 🎓 Conclusions

### Exercice 3 : Idempotence
L'**idempotence est une propriété critique** des playbooks Ansible. Notre test a révélé que la tâche "Start sample app" n'est pas idempotente — elle crée un nouveau processus à chaque relance.

**Takeaway** : Toujours relancer un playbook 2x de suite en développement pour vérifier l'idempotence. Utiliser `changed_when:`, `when:`, ou des modules de haut niveau.

### Exercice 4 : Scalabilité horizontale
Grâce à la **boucle Ansible** et aux **inventaires dynamiques**, déployer N instances est aussi simple que de changer une variable. Pas de code dupliqué, pas de risque d'incohérence.

**Takeaway** : Concevoir les playbooks pour la scalabilité dès le départ. Utiliser les boucles, les tags, et les inventaires dynamiques pour éviter les scripts pour 1, 2, 5, 10 instances.

---

**Tous les fichiers et scripts sont prêts à l'emploi.**  
Pour plus de détails, consultez les fichiers `.md` fournis dans `td2/`.

