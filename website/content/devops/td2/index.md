---
title: "TD2 - Ansible & Packer"
publish: true
---

# TD2 - Managing Infrastructure as Code (IaC)

Author: Badr TAJINI - DevOps Data for SWE - ESIEE - 2025

## Overview

TD2 focuses on Infrastructure as Code (IaC) principles and tools. You'll learn to automate infrastructure provisioning and configuration management using industry-standard tools: Bash scripts, Ansible, Packer, and OpenTofu (Terraform-compatible).

This lab covers exercises 3 through 12 from the course, progressing from basic scripting to advanced IaC patterns including modules and version control.

## Lab Exercises

### Exercises 3-4: Bash Scripting
- Deploying EC2 instances via AWS CLI
- Understanding idempotency in infrastructure automation
- User data scripts for instance initialization

### Exercises 5-6: Packer
- Building Amazon Machine Images (AMIs) with Packer
- Pre-installing applications in images for faster deployments
- Image versioning and management

### Exercises 7-8: OpenTofu Basics
- Declarative infrastructure configuration
- Managing EC2 instances with OpenTofu
- Understanding state management

### Exercises 9-10: Ansible
- Configuration management with playbooks
- Dynamic inventory with AWS
- Role-based organization for the sample-app

### Exercises 11-12: Advanced OpenTofu
- Refactoring to reusable modules
- Multi-instance deployments with `for_each`
- Using modules from GitHub with version control

## Directory Structure

```
td2/
├── README.md                              # This file
├── scripts/
│   ├── bash/                              # Exercises 3-4: Bash deployment scripts
│   │   ├── deploy-ec2-instance.sh
│   │   └── user-data.sh
│   ├── packer/                            # Exercises 5-6: AMI building
│   │   └── sample-app.pkr.hcl
│   ├── ansible/                           # Exercises 9-10: Configuration management
│   │   ├── create_ec2_instance_playbook.yml
│   │   ├── configure_sample_app_playbook.yml
│   │   ├── inventory.aws_ec2.yml
│   │   └── roles/sample-app/
│   └── tofu/                              # Exercises 7-8, 11-12: IaC
│       ├── ec2-instance/                  # Single instance
│       ├── ec2-multi/                     # Multi-instance with for_each
│       ├── modules/ec2-instance/          # Reusable module
│       └── live/
│           ├── sample-app/                # Static: 2 module instances
│           ├── sample-app-scalable/       # Dynamic: 3 instances with for_each
│           └── github-modules/            # Using versioned GitHub modules
├── SECTION_6_SUMMARY.md                   # Module refactoring details
├── SECTION_7_SUMMARY.md                   # GitHub modules usage guide
└── Others/                                # Additional documentation and references
```


## Prerequisites

- AWS Account with credentials configured
- AWS CLI installed and configured
- Ansible with `amazon.aws` collection
- Packer installed
- OpenTofu/Terraform installed  
- Node.js (for local testing)

## Quick Start Commands

### Bash Scripts (Exercises 3-4)

```bash
chmod +x td2/scripts/bash/deploy-ec2-instance.sh
chmod +x td2/scripts/bash/user-data.sh
./td2/scripts/bash/deploy-ec2-instance.sh
```

### Packer (Exercises 5-6)

```bash
cd td2/scripts/packer
packer init sample-app.pkr.hcl
packer build sample-app.pkr.hcl
```

### Ansible (Exercises 9-10)

```bash
ansible-galaxy collection install amazon.aws
cd td2/scripts/ansible
ansible-playbook -v create_ec2_instance_playbook.yml
ansible-playbook -v -i inventory.aws_ec2.yml configure_sample_app_playbook.yml
```

### OpenTofu (Exercises 7-8, 11-12)

```bash
cd td2/scripts/tofu/ec2-instance
tofu init
tofu apply -var="ami_id=ami-xxxx"
tofu destroy  # Clean up when done
```

## Key Concepts

### Infrastructure as Code (IaC)
- **Declarative Configuration**: Define desired state, let tools handle implementation
- **Version Control**: Infrastructure changes tracked in Git
- **Reproducibility**: Same configuration produces same infrastructure
- **Automation**: Reduce manual processes and human error

### Tool Comparison

- **Bash**: Quick scripts, procedural approach, limited idempotency
- **Packer**: Image building, immutable infrastructure patterns
- **Ansible**: Configuration management, good for mutable infrastructure
- **OpenTofu**: Full IaC lifecycle, strong state management, modular design

### Module Benefits (Exercises 11-12)
- Code reuse across projects
- Standardized infrastructure patterns
- Version control for infrastructure components
- Easier testing and maintenance

## Security Best Practices

- Never commit AWS credentials to Git
- Use `~/.aws/credentials` or environment variables
- Add sensitive files to `.gitignore`
- Regularly rotate access keys
- Use IAM roles when possible

## Resource Cleanup

Always destroy AWS resources after testing to avoid unnecessary costs:

```bash
# EC2 instances
aws ec2 terminate-instances --instance-ids <INSTANCE_ID>

# OpenTofu-managed resources
cd td2/scripts/tofu/ec2-instance
tofu destroy

# Packer AMIs (via AWS Console or CLI)
aws ec2 deregister-image --image-id <AMI_ID>
aws ec2 delete-snapshot --snapshot-id <SNAPSHOT_ID>
```

## Additional Resources

Detailed documentation for specific exercises can be found in:
- `SECTION_6_SUMMARY.md` - OpenTofu modules refactoring
- `SECTION_7_SUMMARY.md` - Using GitHub modules with versioning
- `scripts/*/EXERCISE_*.md` - Exercise-specific implementation notes
- `Others/` - Comprehensive references and summaries

## Notes

This lab builds the foundation for advanced IaC concepts covered in TD3, including Auto Scaling Groups, Lambda functions, and production-grade infrastructure patterns.

---

## Fichiers Configuration Ansible

Les fichiers de configuration Ansible pour ce TD :

- [configure_sample_app_playbook.yml](/static/devops/td2/configure_sample_app_playbook.yml)
- [create_ec2_instance_playbook.yml](/static/devops/td2/create_ec2_instance_playbook.yml)
- [create_ec2_instances_multi.yml](/static/devops/td2/create_ec2_instances_multi.yml)
- [inventory.aws_ec2.yml](/static/devops/td2/inventory.aws_ec2.yml)

## Analyses et Résumés

- [[devops/td2/EXERCISE_3_IDEMPOTENCE_ANALYSIS|Analyse Idempotence]]
- [[devops/td2/SECTION_6_SUMMARY|Résumé Section 6]]
- [[devops/td2/SECTION_7_SUMMARY|Résumé Section 7]]

