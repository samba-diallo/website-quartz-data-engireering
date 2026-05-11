# Exercice 3 : Analyse détaillée de l'idempotence

## Résultats observés

Lorsque le playbook `configure_sample_app_playbook.yml` est relancé une deuxième fois, **exactement les mêmes résultats** sont obtenus :

```
PLAY RECAP
localhost : ok=6 changed=1 unreachable=0 failed=0 skipped=1
```

### Comparaison : 1ère vs 2ème exécution

| Tâche | 1ère exécution | 2ème exécution | Idempotent ? |
|-------|---|---|---|
| Gathering Facts | ok | ok | OUI |
| Install Node.js setup repository | ok | ok | OUI |
| Install Node.js | ok | ok | OUI |
| Copy sample app | ok | ok | OUI |
| Check if app is already running | ignored (failed) | ignored (failed) | OUI |
| Stop any existing app | skipped | skipped | OUI |
| **Start sample app** | **changed** | **changed** | NON |

### Pourquoi "Start sample app" n'est PAS idempotent ?

```yaml
- name: Start sample app
 shell: nohup node /home/ec2-user/app.js > /tmp/app.log 2>&1 &
 args:
 chdir: /home/ec2-user/
 become_user: ec2-user
```

**Problèmes** :
1. **Pas de condition** (`when:`) — s'exécute TOUJOURS
2. **Pas de `changed_when: false`** — marque toujours comme "changed"
3. **Pas de détection d'état** — ne vérifie pas si l'app tourne déjà
4. **Résultat** : À chaque exécution, un nouveau processus Node est créé → **2, 3, 4+ instances en écoute sur le port 8080** → problème grave

---

## Solutions pour rendre le rôle idempotent

### Solution 1 : Ajouter une condition + `changed_when: false` (MINIMAL)

```yaml
- name: Start sample app (IDEMPOTENT - version minimale)
 shell: nohup node /home/ec2-user/app.js > /tmp/app.log 2>&1 &
 args:
 chdir: /home/ec2-user/
 become_user: ec2-user
 when: app_running.rc != 0 # Ne s'exécute que si app NOT running
 changed_when: false # Ne marque jamais comme "changed"
```

**Avantages** :
- Minimal, facile à comprendre
- La tâche s'exécute seulement si l'app n'est pas en cours

**Inconvénients** :
- Toujours un `shell` non-structuré
- Pas de gestion des redémarrages ou crashes
- Logs dans `/tmp/app.log` (non managé)

**Résultat idempotent** : 2ème exécution → `skipped` (condition fausse, app déjà en cours)

### Solution 2 : Service systemd (MEILLEUR)

Créer `/etc/systemd/system/sample-app.service` :

```yaml
- name: Create systemd service file for sample app
 copy:
 dest: /etc/systemd/system/sample-app.service
 mode: '0644'
 content: |
 [Unit]
 Description=Sample Node.js Application
 After=network.target
 
 [Service]
 Type=simple
 User=ec2-user
 WorkingDirectory=/home/ec2-user
 ExecStart=/usr/bin/node /home/ec2-user/app.js
 Restart=on-failure
 RestartSec=10
 StandardOutput=journal
 StandardError=journal
 
 [Install]
 WantedBy=multi-user.target

- name: Enable and start sample app service
 systemd:
 name: sample-app
 state: started
 enabled: yes
 daemon_reload: yes
```

**Avantages** :
- **PLEINEMENT IDEMPOTENT** — systemd gère l'idempotence
- Redémarrage automatique en cas de crash (`Restart=on-failure`)
- Logs centralisés dans `journalctl`
- Contrôle facile : `systemctl start/stop/restart sample-app`
- Démarrage automatique après reboot (`enabled: yes`)

**Inconvénients** :
- Nécessite `become: yes` ou exécution en root

**Résultat idempotent** : 
- 1ère exécution : `changed` (service créé et démarré)
- 2ème exécution : `ok` (service existe et tourne déjà)

---

## Fichiers fournis

### Variante 1 : Idempotence minimale
Fichier : `roles/sample-app/tasks/main_idempotent.yml`
- Ajoute la condition `when: app_running.rc != 0`
- Ajoute `changed_when: false`
- Minimal mais fonctionnel

### Variante 2 : Meilleure pratique (systemd)
Fichier : `roles/sample-app/tasks/main_systemd.yml`
- Crée un service systemd complet
- Gestion professionnelle de l'app
- Idempotence garantie

### Variante 3 : Originale (non-idempotente)
Fichier : `roles/sample-app/tasks/main.yml` (actuellement utilisée)
- Montre le problème de non-idempotence
- À titre pédagogique uniquement

---

## Comment utiliser les variantes

Pour utiliser la **version idempotente minimale** :
```bash
cp roles/sample-app/tasks/main_idempotent.yml roles/sample-app/tasks/main.yml
ansible-playbook -i inventory.aws_ec2.yml configure_sample_app_playbook.yml
```

Pour utiliser la **meilleure pratique (systemd)** :
```bash
cp roles/sample-app/tasks/main_systemd.yml roles/sample-app/tasks/main.yml
ansible-playbook -i inventory.aws_ec2.yml configure_sample_app_playbook.yml
```

Puis relancer le playbook — la 2ème exécution doit montrer `ok` (aucun changement).

---

## Leçons apprises

1. **Idempotence = Talon d'Achille** : Beaucoup de playbooks Ansible naïfs ne sont PAS idempotents.
2. **Signes de non-idempotence** :
 - `shell:` ou `command:` sans `changed_when:` ou `when:`
 - Tâches qui modifient l'état sans vérifier l'état existant
 - Redémarrage/relancement d'apps en boucle
3. **Bonnes pratiques** :
 - Utiliser des modules de haut niveau (`yum:`, `copy:`, `systemd:`, etc.) — ils sont idempotents par défaut
 - Pour les scripts personnalisés (`shell:`), ajouter `when:` ou `changed_when:`
 - Préférer les services systemd ou supervisors pour la gestion d'applications
4. **Vérification** : Relancer le playbook **deux fois de suite** — la 2ème exécution doit produire 0 changement (ou très peu).

