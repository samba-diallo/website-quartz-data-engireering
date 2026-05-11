Exercise 9: Module Parameterization - COMPLETED

Objective: Modify the module to accept additional parameters (instance_type, port)

Solution Implemented:

In /home/sable/devops_base/td2/scripts/modules/ec2-instance/variables.tf:

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "port" {
  description = "Port for HTTP traffic"
  type        = number
  default     = 8080
}

In /home/sable/devops_base/td2/scripts/modules/ec2-instance/main.tf:

resource "aws_instance" "sample_app" {
  ami           = var.ami_id
  instance_type = var.instance_type  # Now parameterized
  ...
}

resource "aws_security_group_rule" "allow_http_inbound" {
  from_port = var.port  # Now parameterized
  to_port   = var.port
  ...
}

In /home/sable/devops_base/td2/scripts/live/sample-app/main.tf:

module "sample_app_1" {
  source        = "../../modules/ec2-instance"
  ami_id        = var.ami_id
  name          = "sample-app-tofu-1"
  instance_type = var.instance_type  # Pass parameter
  port          = var.port           # Pass parameter
}

Usage Examples:

# Default values (t3.micro, port 8080)
tofu apply -var="ami_id=ami-07eb809c44dd0fcab"

# Custom instance type and port
tofu apply \
  -var="ami_id=ami-07eb809c44dd0fcab" \
  -var="instance_type=t3.small" \
  -var="port=9000"

# Or use tfvars file
cat > terraform.tfvars << EOF
ami_id        = "ami-07eb809c44dd0fcab"
instance_type = "t3.small"
port          = 3000
EOF
tofu apply

Benefits:
✅ Reusable module across different configurations
✅ Different ports for different environments
✅ Different instance types (cost optimization)
✅ Single module, multiple use cases

---

Exercise 10: Scalable Deployment with for_each - COMPLETED

Objective: Use for_each to deploy multiple instances without code duplication

Implementation:

Create new file: /home/sable/devops_base/td2/scripts/live/sample-app-scalable/main.tf

provider "aws" {
  region  = "us-east-2"
  profile = "labs-devops_diallo"
}

variable "instances" {
  description = "Map of instances to create"
  type = map(object({
    name          = string
    instance_type = string
    port          = number
  }))
  default = {
    "prod-1" = {
      name          = "prod-app-1"
      instance_type = "t3.micro"
      port          = 8080
    }
    "prod-2" = {
      name          = "prod-app-2"
      instance_type = "t3.micro"
      port          = 8080
    }
    "prod-3" = {
      name          = "prod-app-3"
      instance_type = "t3.small"
      port          = 9000
    }
  }
}

variable "ami_id" {
  description = "The ID of the AMI to run."
  type        = string
}

module "sample_apps" {
  for_each      = var.instances
  source        = "../../modules/ec2-instance"
  ami_id        = var.ami_id
  name          = each.value.name
  instance_type = each.value.instance_type
  port          = each.value.port
}

output "instances" {
  description = "Details of all deployed instances"
  value = {
    for key, instance in module.sample_apps :
    key => {
      instance_id = instance.instance_id
      public_ip   = instance.public_ip
    }
  }
}

---

Usage:

# Deployment with default instances (prod-1, prod-2, prod-3)
tofu apply -var="ami_id=ami-07eb809c44dd0fcab"

# Deployment with custom configuration
tofu apply \
  -var="ami_id=ami-07eb809c44dd0fcab" \
  -var='instances={
    "dev-1" = {
      name          = "dev-app-1"
      instance_type = "t3.micro"
      port          = 8080
    }
    "dev-2" = {
      name          = "dev-app-2"
      instance_type = "t3.micro"
      port          = 8080
    }
  }'

---

Comparison: Static vs Scalable

Static (Exercise 9):
module "sample_app_1" { ... }
module "sample_app_2" { ... }
module "sample_app_3" { ... }
❌ Hard to scale
❌ Code duplication
❌ Not maintainable

Scalable (Exercise 10):
module "sample_apps" {
  for_each = var.instances
  ...
}
✅ Easy to add/remove instances
✅ DRY principle
✅ Maintainable
✅ Environment flexibility

---

Benefits of Module Architecture:

1. Reusability
   - Same module used for single instances, pairs, or many
   - No code duplication

2. Maintainability
   - Changes to module apply everywhere
   - Single source of truth

3. Scalability
   - Add/remove instances by changing variable
   - No Terraform code changes needed

4. Testability
   - Test module in isolation
   - Verify with different inputs

5. Team Collaboration
   - Module owners maintain stability
   - Team uses modules without understanding internals

---

Complete Workflow:

1. Module Development (modules/ec2-instance/)
   - Define resources
   - Define variables
   - Define outputs
   - Test with simple case

2. Static Usage (live/sample-app/)
   - 2 hardcoded instances with module

3. Scalable Usage (live/sample-app-scalable/)
   - N instances with for_each

4. CI/CD Pipeline
   - Deploy: tofu init && tofu apply
   - Destroy: tofu destroy
   - Plan: tofu plan

This demonstrates production-ready IaC patterns.
