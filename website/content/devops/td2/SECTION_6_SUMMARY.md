SECTION 6: OpenTofu Modules - COMPLETED

Overview:
Refactored OpenTofu configuration to use modules for better code reuse and organization.

Directory Structure Created:

/home/sable/devops_base/td2/scripts/
├── modules/
│ └── ec2-instance/
│ ├── main.tf (Resources: SG, SG rule, instance)
│ ├── variables.tf (ami_id, name, instance_type, port)
│ ├── outputs.tf (instance_id, security_group_id, public_ip, public_dns)
│ └── user-data.sh (Node.js startup script)
│
├── live/
│ ├── sample-app/ (Static: 2 modules)
│ │ ├── main.tf
│ │ ├── variables.tf
│ │ └── outputs.tf
│ │
│ └── sample-app-scalable/ (Scalable: 3 modules with for_each)
│ └── main.tf
│
└── tofu/
 ├── ec2-instance/ (Original single instance)
 └── ec2-multi/ (Original multi with for_each)

---

DEPLOYMENT 1: Static Module Usage (live/sample-app/)
=====================================================

Configuration:
- 2 module instances: sample_app_1, sample_app_2
- Both use same module: ../../modules/ec2-instance
- Parameters: ami_id, name, instance_type, port

Command:
tofu apply -var="ami_id=ami-07eb809c44dd0fcab"

Results:
 sample-app-1: 13.58.147.3:8080
 Instance ID: i-0abb5af9369f82038
 Security Group: sg-09f99659b3093ac4d
 Response: "Hello from ip-172-31-41-140.us-east-2.compute.internal!"

 sample-app-2: 18.191.207.76:8080
 Instance ID: i-01503049f6b462109
 Security Group: sg-0706e8286805b7060
 Response: "Hello from ip-172-31-32-120.us-east-2.compute.internal!"

---

DEPLOYMENT 2: Scalable with for_each (live/sample-app-scalable/)
================================================================

Configuration:
- 3 instances defined via map variable
- Module called with for_each loop
- Each iteration creates separate instance + SG + rule

Variable:
instances = {
 "prod-1" = { name = "prod-app-1", instance_type = "t3.micro", port = 8080 }
 "prod-2" = { name = "prod-app-2", instance_type = "t3.micro", port = 8080 }
 "prod-3" = { name = "prod-app-3", instance_type = "t3.micro", port = 8080 }
}

Command:
tofu apply -var="ami_id=ami-07eb809c44dd0fcab"

Results:
 prod-1: 18.222.76.46:8080
 Instance ID: i-001685ec314537d40
 Security Group: sg-0d1257d2171f51c3c
 Response: "Hello from ip-172-31-32-201.us-east-2.compute.internal!"

 prod-2: 3.137.158.194:8080
 Instance ID: i-03408248e002397b6
 Security Group: sg-0f08c578efff8bc1c
 Response: "Hello from ip-172-31-46-104.us-east-2.compute.internal!"

 prod-3: 18.116.203.64:8080
 Instance ID: i-09547c9ac05b4f93c
 Security Group: sg-0dc65e32a37920ca7
 Response: "Hello from ip-172-31-45-108.us-east-2.compute.internal!"

---

KEY BENEFITS OF MODULE APPROACH:

1. DRY Principle
 - No code duplication
 - Single source of truth for instance configuration
 - Changes to module apply everywhere

2. Reusability
 - Same module used for different deployments
 - Parameterized (instance_type, port, name)
 - Can be shared across teams/projects

3. Maintainability
 - Module owner maintains stability
 - Users don't need to understand implementation
 - Easier to test and debug

4. Scalability
 - Scale from 1 to N instances with for_each
 - No Terraform code changes needed
 - Just modify variable

5. Separation of Concerns
 - modules/ = Infrastructure templates
 - live/ = Environment-specific configurations
 - Clear separation between what and how

---

EXERCISE 9: Module Parameterization
====================================

Objective: Extend module to accept additional parameters (instance_type, port)

Implementation:
- Added variables: instance_type (default=t3.micro), port (default=8080)
- Updated resources to use these variables
- Root modules pass parameters when calling module

Example:
module "sample_app_1" {
 source = "../../modules/ec2-instance"
 ami_id = var.ami_id
 name = "sample-app-tofu-1"
 instance_type = "t3.small" # Custom type
 port = 9000 # Custom port
}

Benefits:
 Flexibility without code duplication
 Different configs for different environments
 Cost optimization (t3.small vs t3.micro)
 Custom ports for different apps

---

EXERCISE 10: Scalable Deployment with for_each
================================================

Objective: Deploy multiple instances using for_each loop

Implementation:
- Variable "instances" is a map of instance configurations
- Module called with for_each = var.instances
- Each key becomes resource identifier
- All instances created with single module call

Code:
module "sample_apps" {
 for_each = var.instances
 source = "../../modules/ec2-instance"
 ami_id = var.ami_id
 name = each.value.name
 instance_type = each.value.instance_type
 port = each.value.port
}

Advantages over hardcoded modules:
 Add/remove instances by modifying variable
 No code duplication
 Easy to read and understand
 Scales from 1 to 1000+ instances

Example: Scale to 5 instances
variable "instances" {
 default = {
 for i in range(1, 6) : "prod-${i}" => {
 name = "prod-app-${i}"
 instance_type = "t3.micro"
 port = 8080
 }
 }
}

Result: 5 instances created with single apply!

---

COMPARISON: All Approaches

1. Manual Provisioning (Bash)
 Error-prone, not scalable, no state management

2. Configuration Management (Ansible)
 Good for existing resources, limited provisioning

3. Static Modules (Exercise 9)
 Good for predictable, fixed infrastructures
 Hard to scale dynamically

4. Scalable Modules (Exercise 10) 
 Professional, scalable, maintainable
 Used in production
 Cost-effective

---

TOTAL AWS RESOURCES DEPLOYED:

Section 6 Deployments:
- Static (live/sample-app): 2 EC2 instances + 2 SG + 2 SG rules
- Scalable (live/sample-app-scalable): 3 EC2 instances + 3 SG + 3 SG rules

Previous Deployments (still running):
- tofu/ec2-instance: 1 instance (from Section 4)
- tofu/ec2-multi: 2 instances (from Exercise 8)

Total Active:
- 8 EC2 instances
- 8 Security Groups
- All responding on port 8080

Cost Estimate (t3.micro Free Tier eligible):
- Roughly 672 hours/month = ~$0-3/month for non-Free Tier usage
- Once Free Tier expires

---

CLEANUP COMMANDS:

Destroy scalable:
cd live/sample-app-scalable && tofu destroy -auto-approve

Destroy static:
cd live/sample-app && tofu destroy -auto-approve

Destroy all OpenTofu:
cd tofu && for dir in ec2-instance ec2-multi; do cd $dir && tofu destroy -auto-approve && cd ..; done

---

SUMMARY:

Section 6 demonstrates professional IaC patterns:
 Modules for reusability
 Static configurations for predictable use cases
 Scalable patterns for growing infrastructure
 Clean separation of module code and root modules
 Production-ready architecture

This is the foundation for enterprise-grade infrastructure automation.
