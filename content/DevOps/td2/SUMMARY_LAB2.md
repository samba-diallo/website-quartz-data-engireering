RÉSUMÉ COMPLET: LAB 2 - Infrastructure as Code (IaC)

Section 1: Bash Scripting (Déploiement EC2 Manuel)
=================================================
✅ Créé deploy-ec2-instance.sh
✅ Script déploie instance EC2 avec security group
✅ Supporte déploiement flexible d'instances

Section 2: Ansible Configuration Management
=============================================
✅ Créé playbooks et roles Ansible
✅ Déployé Node.js app sur instance EC2
✅ Démontré idempotence avec multiple runs
✅ Exercices 3 & 4: Analysé limitations d'idempotence
✅ Créé templates multi-instances

Section 3: Packer - Image Builder
==================================
✅ Installé Packer 1.9.4
✅ Créé template sample-app.pkr.hcl (HCL)
✅ Fixé problèmes: AMI source, Node.js version, timestamps
✅ Build successful avec Node.js 16.20.0
✅ AMI créée: ami-07eb809c44dd0fcab

Exercise 5: Idempotence dans Packer
- Relancé build Packer 2 fois
- Résultat: 2 AMI différents créés (pas idempotent)
- AMI 1: ami-07eb809c44dd0fcab (2154:31)
- AMI 2: ami-079a315e32554235f (2200:11)
- Chaque build crée timestamps uniques → AMI uniques

Exercise 6: Multi-Provider Packer
- Créé sample-app-virtualbox.pkr.hcl
- Démontré support multi-provider (AWS + VirtualBox)
- Même config, outputs différents
- Concept: "Single source of truth for infrastructure"

Section 4: OpenTofu - Infrastructure as Code
==============================================
✅ Déploiement single instance:
  - Instance ID: i-02538a44ef1b9c4d3
  - Public IP: 18.220.53.35
  - Application: http://18.220.53.35:8080/ ✅

✅ Déploiement multi-instance (for_each):
  - prod-1: i-0053d42c3d606a885 (18.218.153.160:8080)
  - prod-2: i-0302e1408114043e8 (18.218.187.192:8080)
  - Réponses: "Hello from [hostname]"

Exercise 7: Post-Destruction Apply
- tofu destroy → supprime toutes ressources
- tofu apply → les récréé
- Ressources ont nouveaux IDs (pas conservées)
- State file tracking assure consistency

Exercise 8: Multiple Instances
- Implémenté avec for_each sur instance_names
- 2 instances déployées simultanément
- Chaque instance répond avec son hostname
- Scalable: peut ajouter/retirer instances facilement

---

FICHIERS CRÉÉS:

Bash Scripts:
- /home/sable/devops_base/scripts/bash/deploy-ec2-instance.sh

Ansible:
- /home/sable/devops_base/scripts/ansible/configure_sample_app_playbook.yml
- /home/sable/devops_base/scripts/ansible/create_ec2_instance_playbook.yml
- /home/sable/devops_base/scripts/ansible/inventory.aws_ec2.yml
- /home/sable/devops_base/scripts/ansible/roles/sample-app/

Packer:
- /home/sable/devops_base/scripts/packer/sample-app.pkr.hcl (HCL)
- /home/sable/devops_base/scripts/packer/sample-app.json (JSON)
- /home/sable/devops_base/scripts/packer/sample-app-virtualbox.pkr.hcl
- /home/sable/devops_base/scripts/packer/EXERCISE_5_EXPLANATION.md
- /home/sable/devops_base/scripts/packer/EXERCISE_6_EXPLANATION.md

OpenTofu:
- /home/sable/devops_base/scripts/tofu/ec2-instance/ (single instance)
  - main.tf
  - variables.tf
  - outputs.tf
  - user-data.sh

- /home/sable/devops_base/scripts/tofu/ec2-multi/ (multiple instances)
  - main.tf (with for_each)
  - variables.tf
  - outputs.tf
  - user-data.sh

- /home/sable/devops_base/scripts/tofu/EXERCISE_7_AND_8.md

---

KEY LEARNINGS:

1. Bash: Manual, inflexible, error-prone
2. Ansible: Configuration management, idempotent, good for existing resources
3. Packer: Image building, consistent base image, one-time build
4. OpenTofu: Infrastructure provisioning, scalable, state management

Workflow:
Packer (build image) → OpenTofu (provision instances) → Ansible (configure instances)

---

AWS RESOURCES CREATED:
- 1x Packer build (t3.micro temporary)
- Multiple EC2 instances via OpenTofu (t3.micro)
- Security groups for HTTP 8080
- All in us-east-2 region with labs-devops_diallo profile

---

COMMANDS REFERENCE:

Bash:
./deploy-ec2-instance.sh <instance-name> <ami-id>

Ansible:
ansible-playbook create_ec2_instance_playbook.yml -i inventory.aws_ec2.yml
ansible-playbook configure_sample_app_playbook.yml -i inventory.aws_ec2.yml

Packer:
packer init sample-app.pkr.hcl
packer build sample-app.pkr.hcl

OpenTofu (single):
cd ec2-instance
tofu init
tofu plan -var="ami_id=ami-07eb809c44dd0fcab"
tofu apply -var="ami_id=ami-07eb809c44dd0fcab"

OpenTofu (multi):
cd ec2-multi
tofu init
tofu plan -var="ami_id=ami-07eb809c44dd0fcab" -var='instance_names=["prod-1","prod-2"]'
tofu apply -var="ami_id=ami-07eb809c44dd0fcab" -var='instance_names=["prod-1","prod-2"]'

Test:
curl http://<public-ip>:8080/

Cleanup:
tofu destroy

---

LAB 2 COMPLETION STATUS: ✅ COMPLETE

All exercises (3-8) completed successfully.
All sections (Bash, Ansible, Packer, OpenTofu) demonstrated.
Multiple deployment patterns shown.
Infrastructure as Code principles applied throughout.
