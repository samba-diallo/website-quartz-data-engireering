# Section 7: Using OpenTofu Modules from GitHub
## Exercises 11 & 12

### Overview
This section teaches you how to:
1. Use modules from GitHub repositories
2. Implement version control with Git tags and branches
3. Find and use public modules from Terraform Registry
4. Create reusable infrastructure code

---

## Exercise 11: Git Versioning with Modules

### Objective
Explore versioning strategies for modules using Git tags and branches.

### Concepts

#### 1. Semantic Versioning
```
v1.2.3
├── 1: MAJOR (breaking changes)
├── 2: MINOR (new features, backwards compatible)
└── 3: PATCH (bug fixes)
```

#### 2. Module Source Patterns

**Without Version:**
```hcl
source = "github.com/username/repo.git//modules/ec2"
# Uses: default branch (main/master)
# Risk: Code may change unexpectedly
# Use: Development only
```

**With Git Tag (RECOMMENDED):**
```hcl
source = "github.com/username/repo.git//modules/ec2?ref=v1.2.0"
# Uses: Exact version tag
# Benefit: Reproducible, predictable
# Use: Production environments
```

**With Branch:**
```hcl
source = "github.com/username/repo.git//modules/ec2?ref=develop"
# Uses: Specific branch
# Benefit: Latest features on branch
# Risk: Code may change
# Use: Development, active development
```

**With Commit SHA:**
```hcl
source = "github.com/username/repo.git//modules/ec2?ref=abc123def456"
# Uses: Exact commit
# Benefit: Maximum precision
# Risk: Hard to maintain
# Use: Debugging, rollback scenarios
```

### Hands-On Exercise

#### Step 1: Prepare Your GitHub Repository

If you don't have a GitHub account, create one at github.com.

```bash
# Create new repository on GitHub:
# 1. Go to github.com/new
# 2. Name: "iac-modules"
# 3. Add README
# 4. Create repository
```

#### Step 2: Push Your Local Module to GitHub

```bash
# In your workspace
cd /home/sable/devops_base/td2/scripts/modules

# Initialize git (if not already done)
git init

# Add all files
git add -A
git commit -m "Initial module structure"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/iac-modules.git

# Push to main branch
git branch -M main
git push -u origin main
```

#### Step 3: Create Version Tags

```bash
# Create first release
git tag -a v1.0.0 -m "First stable release"
git push origin v1.0.0

# Create second release (with improvements)
git tag -a v1.1.0 -m "Add port parameterization"
git push origin v1.1.0

# Create development branch
git checkout -b develop
git push -u origin develop
```

#### Step 4: Verify Tags on GitHub

```bash
# View all tags:
git tag -l
# Output:
# v1.0.0
# v1.1.0

# View specific tag info:
git show v1.0.0
```

#### Step 5: Test Different Version References

Create different modules using different versions:

```bash
cd /home/sable/devops_base/td2/scripts/live/github-modules
```

**File: test-v1.0.0.tf**
```hcl
module "app_v1_0_0" {
  source = "github.com/YOUR_USERNAME/iac-modules.git//ec2-instance?ref=v1.0.0"
  
  ami_id        = var.ami_id
  name          = "app-v1-0-0"
  instance_type = "t3.micro"
  port          = 8080
}
```

**File: test-v1.1.0.tf**
```hcl
module "app_v1_1_0" {
  source = "github.com/YOUR_USERNAME/iac-modules.git//ec2-instance?ref=v1.1.0"
  
  ami_id        = var.ami_id
  name          = "app-v1-1-0"
  instance_type = "t3.micro"
  port          = 9000
}
```

**File: test-main.tf**
```hcl
module "app_main" {
  source = "github.com/YOUR_USERNAME/iac-modules.git//ec2-instance?ref=main"
  
  ami_id        = var.ami_id
  name          = "app-main"
  instance_type = "t3.micro"
  port          = 8080
}
```

#### Step 6: Initialize and Deploy (Optional)

```bash
cd /home/sable/devops_base/td2/scripts/live/github-modules

# Initialize
tofu init

# Plan (see what would be created)
tofu plan

# Apply (only if you want to deploy)
# tofu apply -auto-approve

# Test
# curl http://<PUBLIC_IP>:8080/
```

### What You Learn

✅ Semantic versioning for modules  
✅ Git tagging for releases  
✅ Branch-based versioning  
✅ Commit SHA references  
✅ Version constraints in OpenTofu  
✅ Production-ready module management  

### Key Takeaways

1. **Always use version tags in production** (?ref=v1.0.0)
2. **Use branches for development** (?ref=develop)
3. **Document version changes** in CHANGELOG.md
4. **Plan upgrades carefully** - test in staging first
5. **Use semantic versioning** - clear expectations for changes

---

## Exercise 12: Using Public Modules from Terraform Registry

### Objective
Find and implement production-ready modules from public repositories.

### Popular Module Sources

#### 1. Terraform Registry (registry.terraform.io)
Official registry for Terraform and OpenTofu modules.

Common modules:
- **terraform-aws-modules/ec2-instance/aws** - EC2 instances
- **terraform-aws-modules/vpc/aws** - VPC with subnets
- **terraform-aws-modules/security-group/aws** - Security groups
- **terraform-aws-modules/ecs/aws** - ECS clusters

#### 2. GitHub Public Repositories

Well-maintained options:
- hashicorp/terraform-aws-modules
- gruntwork-io/terraform-aws-modules
- cloudposse/terraform-aws-modules

### Hands-On Exercise

#### Option A: Use Terraform Registry Module (EASIEST)

**Step 1: Find Module**

Go to https://registry.terraform.io/modules and search for "security group"

Example: terraform-aws-modules/security-group/aws

**Step 2: Read Documentation**

The registry provides:
- Module description
- Input variables
- Output values
- Example usage

**Step 3: Create Configuration**

```hcl
provider "aws" {
  region  = "us-east-2"
  profile = "labs-devops_diallo"
}

module "web_security_group" {
  source  = "terraform-aws-modules/security-group/aws"
  version = "5.0.0"

  name        = "web-sg"
  description = "Security group for web server"
  vpc_id      = "vpc-xxxxxxxx"  # Your VPC ID

  # Ingress rules
  ingress_rules       = ["http-80-tcp", "https-443-tcp", "ssh-tcp"]
  ingress_cidr_blocks = ["0.0.0.0/0"]

  # Egress rule
  egress_rules       = ["all-all"]
  egress_cidr_blocks = ["0.0.0.0/0"]

  tags = {
    Name = "web-server-sg"
  }
}

output "security_group_id" {
  value = module.web_security_group.security_group_id
}
```

#### Option B: Use GitHub Public Module

**Step 1: Find Repository**

Go to https://github.com/cloudposse/terraform-aws-modules

Example: cloudposse/terraform-aws-modules

**Step 2: Examine Code**

```bash
# Look at:
# - README.md (usage, requirements)
# - variables.tf (input variables)
# - outputs.tf (available outputs)
# - examples/ (sample configurations)
```

**Step 3: Create Configuration**

```hcl
provider "aws" {
  region  = "us-east-2"
  profile = "labs-devops_diallo"
}

module "vpc_module" {
  source = "github.com/cloudposse/terraform-aws-modules.git//vpc?ref=v1.0.0"

  namespace           = "myapp"
  environment         = "dev"
  cidr_block          = "10.0.0.0/16"
  availability_zones  = ["us-east-2a", "us-east-2b"]
  
  tags = {
    Project = "Lab2"
  }
}

output "vpc_id" {
  value = module.vpc_module.vpc_id
}
```

### Recommended Public Modules

#### For EC2:
```hcl
source  = "terraform-aws-modules/ec2-instance/aws"
version = "5.0.0"
```

#### For VPC:
```hcl
source  = "terraform-aws-modules/vpc/aws"
version = "5.0.0"
```

#### For Security Groups:
```hcl
source  = "terraform-aws-modules/security-group/aws"
version = "5.0.0"
```

#### For RDS:
```hcl
source  = "terraform-aws-modules/rds/aws"
version = "6.0.0"
```

#### For Load Balancers:
```hcl
source  = "terraform-aws-modules/alb/aws"
version = "9.0.0"
```

### How to Use Modules from Registry

**Step 1: Identify Module**

Visit https://registry.terraform.io/browse/modules

Search by:
- Provider (AWS, Azure, GCP)
- Resource type (EC2, VPC, RDS)
- Keyword

**Step 2: Copy Module Declaration**

```hcl
module "example" {
  source  = "terraform-aws-modules/ec2-instance/aws"
  version = "5.0.0"
  
  # Configuration
}
```

**Step 3: Fill in Required Variables**

From module documentation, identify:
- `required_variables`: Must be specified
- `optional_variables`: Have defaults

**Step 4: Test with `tofu plan`**

```bash
cd /path/to/module
tofu init
tofu plan  # Preview changes
tofu apply # Deploy (if approved)
```

### Best Practices for Public Modules

✅ **Always pin version** (`version = "5.0.0"`)  
✅ **Read README carefully** (requirements, limitations)  
✅ **Test in non-prod first** (staging, dev)  
✅ **Check module maturity** (verify, examples, usage)  
✅ **Review input/output variables** (compatibility)  
✅ **Document customizations** (why certain values chosen)  
✅ **Monitor module updates** (watch for bug fixes)  

### Avoiding Module Pitfalls

❌ **Don't** use modules without version pins  
❌ **Don't** assume module outputs without reading docs  
❌ **Don't** deploy to production without testing  
❌ **Don't** ignore breaking changes between versions  
❌ **Don't** fork modules unless necessary  

---

## Complete Exercise 11-12 Example

Here's a complete working example combining both exercises:

**Directory:** `/home/sable/devops_base/td2/scripts/live/github-modules/`

**Files:**
- `example1-local-module.tf` - Using local module
- `example2-github-module-terraform-aws.tf` - Using Terraform Registry module
- `example3-custom-github-module.tf` - Using custom GitHub module
- `example4-multiple-versions.tf` - Multiple versions demonstration
- `main.tf` - Primary configuration
- `variables.tf` - Input variables
- `outputs.tf` - Output values

### Deploy Section 7 Example

```bash
# Navigate to github-modules directory
cd /home/sable/devops_base/td2/scripts/live/github-modules

# Initialize OpenTofu
tofu init

# Plan deployment
tofu plan

# Deploy
tofu apply -auto-approve

# View outputs
tofu output

# Test the deployed instance
curl http://<PUBLIC_IP>:8080/

# Cleanup
tofu destroy -auto-approve
```

---

## Comparison: Module Sources

| Aspect | Local Module | GitHub Custom | Terraform Registry |
|--------|--------------|----------------|-------------------|
| **Control** | Full | Full | Limited |
| **Maintenance** | Self | Self | Provider |
| **Discovery** | Manual | Search | Built-in search |
| **Versioning** | Git tags | Git tags | Version pins |
| **Documentation** | Your docs | Your docs | Registry docs |
| **Testing** | Your tests | Your tests | Provider tested |
| **Support** | Self | Self | Provider support |
| **Use Case** | Internal | Shared | Standardized |

---

## Real-World Scenarios

### Scenario 1: Development Team Sharing Modules

1. Team creates internal module repository
2. Each project references with `?ref=v1.0.0`
3. Updates released as new versions
4. Teams adopt at their own pace

### Scenario 2: Using Open Source Modules

1. Find module on Terraform Registry
2. Pin specific version
3. Customize via variables
4. Deploy with confidence

### Scenario 3: Versioning Strategy

- **v1.0.0**: Initial release, all projects
- **v1.1.0**: New feature, backwards compatible
- **v2.0.0**: Breaking change, update projects gradually

---

## Resources

- Terraform Registry: https://registry.terraform.io
- OpenTofu Modules: https://opentofu.org/docs/language/modules/
- GitHub Module Syntax: https://opentofu.org/docs/language/modules/sources/#github
- Semantic Versioning: https://semver.org

---

## Conclusion

Exercises 11-12 teach you:

✅ How to version modules with Git tags  
✅ How to reference specific module versions  
✅ How to find and use public modules  
✅ How to create reusable infrastructure code  
✅ Production-ready module management strategies  

This enables infrastructure reuse across teams and projects, a key practice in enterprise IaC.

---

**Next Steps:**
- Push your module to GitHub
- Create releases with version tags
- Use public modules in your configurations
- Implement modular architecture across projects
