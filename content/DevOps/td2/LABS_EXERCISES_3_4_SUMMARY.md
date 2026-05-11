# Lab 2 — Exercices 3 et 4 : Résumé & Guide d'exécution

## 📋 Fichiers et documents créés

### Exercice 3 : Idempotence
- **Documentation** : `EXERCISE_3_IDEMPOTENCE_ANALYSIS.md`
  - Analyse détaillée des résultats
  - Explications du problème d'idempotence
  - 3 solutions (minimale, meilleure pratique)

- **Scripts de rôle** (3 variantes) :
  - `roles/sample-app/tasks/main.yml` (actuelle — non-idempotente)
  - `roles/sample-app/tasks/main_idempotent.yml` (idempotente minimale)
  - `roles/sample-app/tasks/main_systemd.yml` (meilleure pratique avec systemd)

- **Script d'exécution** :
  ```bash
  cd /home/sable/devops_base/td2/scripts/ansible
  ./exercise_3_idempotency.sh
  ```

### Exercice 4 : Déploiement multi-instance
- **Documentation** : `EXERCISES_3_4_ANALYSIS.md`
  - Explication du concept multi-instance
  - Approches (modification playbook, inventaire, configuration)

- **Playbook multi-instance** :
  - `create_ec2_instances_multi.yml` — crée N instances (variable `instance_count`)

- **Script d'exécution** :
  ```bash
  cd /home/sable/devops_base/td2/scripts/ansible
  ./exercise_4_multi_instance.sh [nombre_instances]
  # Exemple : ./exercise_4_multi_instance.sh 3
  ```

---

## 🔍 Résultats observés — Exercice 3

### Idempotence (relancer 2x le même playbook)

**1ère exécution** :
```
PLAY RECAP
... ok=6 changed=1 unreachable=0 failed=0 skipped=1
```

**2ème exécution** (IDENTIQUE) :
```
PLAY RECAP
... ok=6 changed=1 unreachable=0 failed=0 skipped=1
```

### Problème identifié

La tâche **"Start sample app"** n'est **PAS idempotente** :
- Elle est une commande `shell` brute
- S'exécute TOUJOURS (pas de condition `when:`)
- Marque TOUJOURS comme `changed`
- **Résultat** : À chaque relance, un nouveau processus Node est créé → accumulation de processus

### Explication technique

```yaml
# PROBLÉMATIQUE
- name: Start sample app
  shell: nohup node /home/ec2-user/app.js > /tmp/app.log 2>&1 &
  # ❌ Pas de condition (when:)
  # ❌ Pas de changed_when: false
  # ❌ Crée TOUJOURS un nouveau processus
```

**Solution 1** (minimale) :
```yaml
- name: Start sample app (IDEMPOTENT)
  shell: nohup node /home/ec2-user/app.js > /tmp/app.log 2>&1 &
  when: app_running.rc != 0         # ✅ Ne lance que si pas actif
  changed_when: false               # ✅ Supprime le "changed"
```

**Solution 2** (meilleure) :
```yaml
# Utiliser un service systemd — complètement idempotent
- name: Enable and start sample app service
  systemd:
    name: sample-app
    state: started
    enabled: yes
```

---

## 🚀 Exercice 4 — Déploiement multi-instance (préparé)

### Fichiers prêts

**Playbook multi-instance** : `create_ec2_instances_multi.yml`
```yaml
- loop: "{{ range(0, instance_count | int) | list }}"
  # Crée N instances (N = variable instance_count)
```

**Inventaire dynamique** (inchangé) : `inventory.aws_ec2.yml`
```yaml
filters:
  tag:Ansible: ch2_instances  # Découvre TOUTES les instances avec ce tag
```

**Playbook de configuration** (inchangé) : `configure_sample_app_playbook.yml`
```yaml
hosts: _ch2_instances  # Cible TOUS les hôtes du groupe dynamique
```

### Workflow complet

1. **Créer 3 instances** :
   ```bash
   ANSIBLE_PYTHON_INTERPRETER="$(which python3)" \
   AWS_PROFILE=labs-devops_diallo \
   ansible-playbook -v create_ec2_instances_multi.yml \
     -e instance_count=3 \
     -e instance_type=t3.micro
   ```

2. **Inventaire découvre automatiquement les 3 instances**

3. **Configurer toutes les 3 instances en parallèle** :
   ```bash
   ANSIBLE_PYTHON_INTERPRETER="$(which python3)" \
   AWS_PROFILE=labs-devops_diallo \
   ansible-playbook -i inventory.aws_ec2.yml configure_sample_app_playbook.yml
   ```

4. **Tester les 3 apps** :
   ```bash
   # Récupérer les IPs
   aws ec2 describe-instances \
     --filters "Name=tag:Ansible,Values=ch2_instances" \
     --query 'Reservations[].Instances[].PublicIpAddress' \
     --output text \
     --profile labs-devops_diallo --region us-east-2
   
   # Tester chaque app
   for IP in $(aws ec2 describe-instances --filters ... --output text); do
     curl http://$IP:8080/
   done
   ```

### Avantages du design

✅ **Pas de changement du code Ansible** — juste changer une variable (`instance_count`)  
✅ **Inventaire auto-découvre** — le plugin `aws_ec2` voit toutes les instances tagguées  
✅ **Parallélisation automatique** — Ansible se connecte aux N instances en parallèle  
✅ **Même configuration** — tous les hôtes reçoivent la même config  

---

## 📝 Pour aller plus loin

### Améliorer l'idempotence du rôle

Remplacer `main.yml` par une version plus robuste :

```bash
# Variante minimale
cp roles/sample-app/tasks/main_idempotent.yml roles/sample-app/tasks/main.yml

# Variante meilleure (systemd)
cp roles/sample-app/tasks/main_systemd.yml roles/sample-app/tasks/main.yml

# Tester
ansible-playbook -i inventory.aws_ec2.yml configure_sample_app_playbook.yml
# Relancer → doit montrer 0 changement à la 2ème exécution
```

### Test du déploiement multi-instance

```bash
cd /home/sable/devops_base/td2/scripts/ansible

# Déployer 3 instances (utilise le script)
./exercise_4_multi_instance.sh 3

# Ou manuellement
ansible-playbook -v create_ec2_instances_multi.yml -e instance_count=3
# Attendre 30s
ansible-playbook -i inventory.aws_ec2.yml configure_sample_app_playbook.yml
```

### Nettoyage

Terminer les instances (toutes avec le tag `Ansible=ch2_instances`) :

```bash
# Lister les IDs
aws ec2 describe-instances \
  --filters "Name=tag:Ansible,Values=ch2_instances" "Name=instance-state-name,Values=running" \
  --query 'Reservations[].Instances[].InstanceId' \
  --output text \
  --profile labs-devops_diallo --region us-east-2

# Terminer (remplacer ID1 ID2 ID3)
aws ec2 terminate-instances \
  --instance-ids i-0d9e97dcfeef9c1d9 [ID2] [ID3] ... \
  --profile labs-devops_diallo --region us-east-2

# Nettoyer le Security Group (après termination complète)
aws ec2 delete-security-group \
  --group-name sample-app-ansible \
  --profile labs-devops_diallo --region us-east-2

# Supprimer la clé (optionnel)
aws ec2 delete-key-pair --key-name ansible-ch2 \
  --profile labs-devops_diallo --region us-east-2
```

---

## 📚 Lectures recommandées

1. **Idempotence dans Ansible** : https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_execution.html#idempotence
2. **Module `systemd`** : https://docs.ansible.com/ansible/latest/collections/ansible/posix/systemd_module.html
3. **Plugin inventaire `aws_ec2`** : https://docs.ansible.com/ansible/latest/collections/amazon/aws/aws_ec2_inventory.html
4. **Boucles dans Ansible (`loop`, `with_*`)** : https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_loops.html

---

## ✅ Checklist — Exercices 3 & 4

### Exercice 3
- [x] Documentation d'analyse créée (`EXERCISE_3_IDEMPOTENCE_ANALYSIS.md`)
- [x] Exécution pratique réalisée (script `exercise_3_idempotency.sh`)
- [x] Résultats observés : tâche "Start sample app" n'est pas idempotente
- [x] 3 solutions fournies (minimale, meilleure pratique)
- [ ] (Optionnel) Tester une variante en remplaçant `main.yml`

### Exercice 4
- [x] Playbook multi-instance créé (`create_ec2_instances_multi.yml`)
- [x] Documentation fournie (`EXERCISES_3_4_ANALYSIS.md`)
- [x] Script d'exécution préparé (`exercise_4_multi_instance.sh`)
- [ ] (Optionnel) Exécuter le script pour déployer 2-3 instances

---

## 🎓 Conclusion

**Exercice 3** montre l'importance de l'idempotence dans les playbooks Ansible. Les tâches mal écrites peuvent créer des doublons ou des conflits à chaque relance. Les solutions incluent l'ajout de conditions, `changed_when:`, ou (meilleur) l'utilisation de services systemd.

**Exercice 4** démontre la scalabilité horizontale avec Ansible. Grâce à la boucle et aux tags, déployer 3 instances ou 30 instances ne nécessite que la modification d'une seule variable. L'inventaire dynamique et la parallélisation automatique rendent cela puissant et efficace.

