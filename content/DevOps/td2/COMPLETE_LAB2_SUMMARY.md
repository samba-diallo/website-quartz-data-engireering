COMPLETE LAB 2 SUMMARY: Infrastructure as Code

Project: devops_base/td2
Date: November 26, 2025
Region: us-east-2
AWS Profile: labs-devops_diallo

========================================
SECTIONS COMPLETED
========================================

✅ Section 1: Bash Scripting
   - Created deploy-ec2-instance.sh
   - Manual EC2 provisioning with security groups

✅ Section 2: Ansible Configuration Management
   - Created playbooks and roles
   - Deployed Node.js application
   - Demonstrated idempotence
   - Exercises 3 & 4: Analyzed limitations

✅ Section 3: Packer Image Building
   - Built custom AMI with Node.js 16.20.0
   - AMI ID: ami-07eb809c44dd0fcab
   - Exercise 5: Demonstrated non-idempotence (2 different AMIs)
   - Exercise 6: Multi-provider support (VirtualBox template)

✅ Section 4: OpenTofu Single Instance
   - Deployed 1 instance: 18.220.53.35:8080
   - Tested application successfully

✅ Section 5: OpenTofu Multi-Instance
   - Deployed 2 instances with for_each pattern
   - Exercise 7: Destroy/Apply behavior
   - Exercise 8: Multiple instances demonstration

✅ Section 6: OpenTofu Modules
   - Created reusable module: modules/ec2-instance
   - Exercise 9: Parameterized module (instance_type, port)
   - Exercise 10: Scalable deployment with for_each
   - Deployed: 2 static + 3 scalable instances

========================================
DIRECTORY STRUCTURE
========================================

/home/sable/devops_base/scripts/
├── bash/
│   └── deploy-ec2-instance.sh
├── ansible/
│   ├── configure_sample_app_playbook.yml
│   ├── create_ec2_instance_playbook.yml
│   ├── inventory.aws_ec2.yml
│   └── roles/
│       └── sample-app/
├── packer/
│   ├── sample-app.pkr.hcl (HCL template)
│   ├── sample-app.json (JSON backup)
│   ├── sample-app-virtualbox.pkr.hcl
│   ├── app.js
│   ├── user-data.sh
│   ├── EXERCISE_5_EXPLANATION.md
│   └── EXERCISE_6_EXPLANATION.md
├── modules/
│   └── ec2-instance/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       └── user-data.sh
├── tofu/
│   ├── ec2-instance/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── user-data.sh
│   ├── ec2-multi/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── user-data.sh
│   └── EXERCISE_7_AND_8.md
├── live/
│   ├── sample-app/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── sample-app-scalable/
│       └── main.tf
└── EXERCISE_9_AND_10.md

========================================
ACTIVE AWS RESOURCES
========================================

Total EC2 Instances: 8

From Section 4:
- Instance: 18.220.53.35:8080 (Single module test)

From Section 5:
- Instance: 18.218.153.160:8080 (prod-1 multi)
- Instance: 18.218.187.192:8080 (prod-2 multi)

From Section 6 - Static (live/sample-app):
- Instance: 13.58.147.3:8080 (sample-app-tofu-1)
- Instance: 18.191.207.76:8080 (sample-app-tofu-2)

From Section 6 - Scalable (live/sample-app-scalable):
- Instance: 18.222.76.46:8080 (prod-app-1)
- Instance: 3.137.158.194:8080 (prod-app-2)
- Instance: 18.116.203.64:8080 (prod-app-3)

Total Security Groups: 8+ (one per instance)

All instances:
✅ Running
✅ Responding to HTTP on port 8080
✅ Returning hostname in response

========================================
KEY LEARNINGS
========================================

1. Bash Scripting
   - Manual but flexible
   - No state management
   - Error-prone at scale

2. Ansible (Configuration Management)
   - Good for existing resources
   - Idempotent operations
   - Limited provisioning capability
   - Exercises 3-4: Showed limitations with dynamic processes

3. Packer (Image Building)
   - One-time image creation
   - Consistent base for instances
   - Not idempotent (each build = new image)
   - Multi-provider support possible
   - Node.js 16.20.0 binary installation strategy worked

4. OpenTofu (Infrastructure as Code)
   - State management critical
   - Idempotent deployments
   - Destroy/Apply predictable
   - Module approach scalable
   - for_each pattern superior to count for flexibility

5. Modular Architecture
   - Separation: modules vs live configurations
   - Reusability across projects
   - Parameterization for flexibility
   - Professional IaC patterns

========================================
TECHNOLOGY STACK
========================================

IaC Tools:
- Bash (0.1: Manual)
- Ansible 2.x (Configuration mgmt)
- Packer 1.9.4 (Image building)
- OpenTofu 1.9.x (Infrastructure provisioning)

Cloud Platform:
- AWS EC2
- AWS Security Groups
- AWS VPC (default)

Application:
- Node.js 16.20.0
- Custom HTTP server (port 8080)
- Response: Hostname of instance

========================================
EXERCISES COMPLETED
========================================

Exercise 3: Ansible Idempotence
✅ Tested: Running configure playbook 2+ times
✅ Finding: Most tasks idempotent, except "Start sample app"

Exercise 4: Multi-instance with Ansible
✅ Created template for 3+ instances
✅ Demonstrated scaling capability

Exercise 5: Packer Build Behavior
✅ Ran packer build twice
✅ Result: Different AMI IDs (non-idempotent)
✅ Reason: Timestamp in ami_name ensures uniqueness

Exercise 6: Multi-provider Packer
✅ Created VirtualBox template
✅ Showed same logic, different provider
✅ Concept: "Single source of truth" across platforms

Exercise 7: OpenTofu Post-Destruction
✅ Demonstrated: destroy → new apply = recreation
✅ Insight: New resource IDs assigned
✅ Benefit: Clean state, reproducible

Exercise 8: Multiple Instances
✅ Used for_each to deploy 2+ instances
✅ Cleaner than hardcoded modules

Exercise 9: Module Parameterization
✅ Added instance_type variable
✅ Added port variable
✅ Root module passes parameters
✅ Result: Reusable, flexible module

Exercise 10: Scalable Modules
✅ Used for_each with var.instances map
✅ Deployed 3 instances from single module
✅ Demonstrated production-ready pattern

========================================
BEST PRACTICES DEMONSTRATED
========================================

Infrastructure as Code:
✅ Version control ready (all .tf files)
✅ State management with OpenTofu
✅ Modular design
✅ DRY principle (Don't Repeat Yourself)
✅ Parameterized configurations
✅ Clear separation of concerns

Security:
✅ Security groups for port access control
✅ AWS profile usage (not hardcoded credentials)
✅ Variable inputs not in code

Automation:
✅ User-data scripts for initialization
✅ Consistent deployment across instances
✅ Repeatable apply/destroy cycles

Documentation:
✅ Exercise explanations in markdown
✅ Module variables documented
✅ Output descriptions clear
✅ Comments in configuration

========================================
SCALING SCENARIOS
========================================

Scenario 1: Dev Environment (1 instance)
tofu apply -var="ami_id=ami-..." -var="instance_count=1"

Scenario 2: Staging (3 instances)
cd live/sample-app-scalable
tofu apply -var="ami_id=ami-..." -var='instances={...3 configs...}'

Scenario 3: Production (10+ instances)
module "prod_apps" {
  for_each = var.prod_instances
  source = "../../modules/ec2-instance"
  ...
}

All achieved with minimal code changes, maximum reuse.

========================================
COST OPTIMIZATION
========================================

Current Setup:
- t3.micro instances (AWS Free Tier eligible for 12 months)
- No persistent storage
- Minimal data transfer
- No additional services

Estimated Monthly Cost (post Free Tier):
- 8 instances × 730 hours × $0.0104/hour = ~$60/month
- Can reduce to 2-3 instances for dev/staging

Optimization Strategies:
✅ Use Free Tier eligible instance types
✅ Destroy when not needed (tofu destroy)
✅ Right-size instances (don't over-provision)
✅ Use spot instances for non-production
✅ Implement auto-shutdown schedules

========================================
CLEANUP & NEXT STEPS
========================================

Current State: 8 instances running

Cleanup Command (all at once):
cd /home/sable/devops_base/scripts/live/sample-app && tofu destroy -auto-approve
cd /home/sable/devops_base/scripts/live/sample-app-scalable && tofu destroy -auto-approve

Next Steps:
1. Implement CI/CD pipeline (GitHub Actions / GitLab CI)
2. Add monitoring (CloudWatch / Prometheus)
3. Implement auto-scaling groups
4. Add database layer
5. Implement infrastructure testing (terratest)
6. Add secrets management (AWS Secrets Manager)
7. Implement blue-green deployments

========================================
CONCLUSION
========================================

Lab 2 demonstrates complete IaC workflow:

Progression:
Bash (manual) → Ansible (config mgmt) → Packer (image building) → OpenTofu (provisioning)

Key Achievement:
✅ Scalable, maintainable, repeatable infrastructure
✅ From 1 to 1000+ instances with minimal code changes
✅ Professional-grade patterns ready for production
✅ All concepts integrated: modules, parameters, scaling

This lab provides foundation for enterprise infrastructure automation.

---

Documentation Files:
- /home/sable/devops_base/SUMMARY_LAB2.md (Sections 1-5)
- /home/sable/devops_base/SECTION_6_SUMMARY.md (Section 6)
- /home/sable/devops_base/scripts/EXERCISE_9_AND_10.md (Exercises 9-10)
- /home/sable/devops_base/scripts/packer/EXERCISE_5_EXPLANATION.md
- /home/sable/devops_base/scripts/packer/EXERCISE_6_EXPLANATION.md
- /home/sable/devops_base/scripts/tofu/EXERCISE_7_AND_8.md

END OF LAB 2
