# SECTION 7: Using OpenTofu Modules from GitHub - DEPLOYMENT GUIDE

## Status: Conceptual Deployment (Due to vCPU Limits)

**Note:** This section demonstrates the **concepts and syntax** for using GitHub modules. Actual deployment is limited by AWS Free Tier vCPU constraints (16 vCPU limit reached from previous deployments).

---

## Quick Start

### Using Your Local Module (Already Working)

```bash
cd /home/sable/devops_base/td2/scripts/live/github-modules
tofu init
tofu plan
tofu apply -auto-approve
```

### Using GitHub Module (Production Ready)

**Step 1: Push Module to GitHub**

```bash
cd /home/sable/devops_base/td2/scripts/modules
git init
git add -A
git commit -m "Initial OpenTofu module"
git remote add origin https://github.com/YOUR_USERNAME/iac-modules.git
git push -u origin main
```

**Step 2: Create Release Tag**

```bash
git tag -a v1.0.0 -m "First stable release"
git push origin v1.0.0
```

**Step 3: Update OpenTofu Configuration**

In `main.tf`, uncomment and update:

```hcl
module "github_module_instance" {
  source = "github.com/YOUR_USERNAME/iac-modules.git//ec2-instance?ref=v1.0.0"
  
  ami_id        = var.ami_id
  name          = "github-module-test"
  instance_type = "t3.micro"
  port          = 8080
}
```

**Step 4: Deploy**

```bash
tofu init
tofu apply -auto-approve
```

---

## Key Concepts Explained

### 1. GitHub Module Source Format

```
github.com/USERNAME/REPO.git//PATH/TO/MODULE?ref=REFERENCE
```

Components:
- **USERNAME**: Your GitHub username
- **REPO**: Repository name (e.g., "iac-modules")
- **PATH**: Path to module inside repo (e.g., "ec2-instance")
- **ref**: Version reference (optional)

### 2. Version References

| Reference | Format | Use Case | Example |
|-----------|--------|----------|---------|
| **Default** | `(no ?ref)` | Development | `github.com/user/repo.git//module` |
| **Tag** | `?ref=v1.0.0` | Production | `github.com/user/repo.git//module?ref=v1.0.0` |
| **Branch** | `?ref=main` | Latest features | `github.com/user/repo.git//module?ref=main` |
| **Commit** | `?ref=abc123` | Debugging | `github.com/user/repo.git//module?ref=abc123` |

### 3. Semantic Versioning

```
v1.2.3
├── 1: MAJOR (breaking changes)
├── 2: MINOR (new features, backwards compatible)
└── 3: PATCH (bug fixes, no new features)
```

**Examples:**
- v1.0.0 → v1.1.0: Safe to update (new features)
- v1.0.0 → v2.0.0: Review carefully (breaking changes)
- v1.0.0 → v1.0.1: Safe to update (bug fix)

---

## Configuration Files in `live/github-modules/`

### 1. example1-local-module.tf
Uses **local module** from `../../modules/ec2-instance`

```hcl
module "example1_local_sample_app" {
  source        = "../../modules/ec2-instance"
  ami_id        = var.ami_id
  name          = "example1-local-module-app"
  instance_type = var.instance_type
  port          = var.port
}
```

**Use case:** Development, testing, internal only

### 2. example2-github-module-terraform-aws.tf
Shows **Terraform Registry module** pattern (terraform-aws-modules)

```hcl
# Commented reference to show syntax
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"
  
  name = "main-vpc"
  cidr = "10.0.0.0/16"
}
```

**Use case:** Production-ready modules from community

### 3. example3-custom-github-module.tf
Shows **custom GitHub module** pattern (your own repository)

```hcl
# Commented reference to show syntax
module "github_sample_app" {
  source = "github.com/YOUR_USERNAME/iac-modules.git//ec2-instance?ref=v1.0.0"
  
  ami_id        = "ami-07eb809c44dd0fcab"
  name          = "github-module-app"
  instance_type = "t3.micro"
  port          = 8080
}
```

**Use case:** Team/organization infrastructure sharing

### 4. example4-multiple-versions.tf
Shows **multiple version patterns** for comparison

```hcl
module "app_v1_0_0" {
  source = "github.com/user/repo.git//module?ref=v1.0.0"
  # ... config
}

module "app_v1_2_0" {
  source = "github.com/user/repo.git//module?ref=v1.2.0"
  # ... config
}

module "app_main" {
  source = "github.com/user/repo.git//module?ref=main"
  # ... config
}
```

**Use case:** Testing version compatibility, gradual upgrades

### 5. main.tf
**Primary configuration** demonstrating local module + GitHub module pattern

- Defines AWS provider
- Instantiates local module (working)
- Shows GitHub module pattern (commented, ready to enable)

### 6. variables.tf
**Input variables** for all modules:
- `ami_id`: AMI to use (default: Packer-built AMI)
- `instance_type`: EC2 type (default: t3.micro)
- `port`: Application port (default: 8080)

### 7. outputs.tf
**Output values** from deployed instances:
- `local_module_public_ip`
- `local_module_instance_id`
- `local_module_public_dns`
- `local_module_security_group`

---

## Practical Workflow

### Scenario: Sharing Module with Team

#### Phase 1: Development (Local)
```bash
# Create module locally
/home/sable/devops_base/td2/scripts/modules/ec2-instance/
├── main.tf
├── variables.tf
├── outputs.tf
└── user-data.sh

# Test locally
cd live/sample-app
tofu apply
```

#### Phase 2: Version (Git)
```bash
cd modules
git init
git add -A
git commit -m "Add ec2-instance module"
git remote add origin https://github.com/user/iac-modules.git
git push -u origin main
```

#### Phase 3: Release (Tag)
```bash
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
```

#### Phase 4: Share (GitHub)
Team members can now use:
```hcl
module "app" {
  source = "github.com/user/iac-modules.git//ec2-instance?ref=v1.0.0"
  
  ami_id = "ami-xxx"
  name   = "my-app"
  # ...
}
```

---

## Comparison: Module Sources

### Local Module
```hcl
source = "../../modules/ec2-instance"
```
- ✅ No network calls
- ✅ Full control
- ✅ Easy debugging
- ❌ No version control
- ❌ Hard to share

### GitHub Custom Module
```hcl
source = "github.com/user/repo.git//module?ref=v1.0.0"
```
- ✅ Version control
- ✅ Easy to share
- ✅ Release management
- ⚠️ Requires GitHub account
- ⚠️ Network dependency

### Terraform Registry Module
```hcl
source  = "terraform-aws-modules/vpc/aws"
version = "5.0.0"
```
- ✅ Community tested
- ✅ Well documented
- ✅ Discovery via web UI
- ⚠️ Limited customization
- ⚠️ Dependency on provider

---

## Real-World Examples

### Example 1: Development Team

**Repository:** github.com/mycompany/terraform-modules

**Structure:**
```
terraform-modules/
├── vpc/
├── ec2-instance/
├── security-group/
├── alb/
└── rds/
```

**Usage:**
```hcl
module "app_vpc" {
  source = "github.com/mycompany/terraform-modules.git//vpc?ref=v2.3.0"
  ...
}

module "app_servers" {
  source = "github.com/mycompany/terraform-modules.git//ec2-instance?ref=v1.5.0"
  ...
}
```

**Benefits:**
- Consistent infrastructure across all projects
- Central versioning
- Controlled updates

### Example 2: SaaS Platform

**Repository:** github.com/acme/platform-infrastructure

**Versions:**
- v1.0.0: MVP, basic EC2, single AZ
- v1.1.0: Multi-AZ support, added RDS
- v1.2.0: ECS containers, auto-scaling
- v2.0.0: Kubernetes, completely redesigned

**Teams using:**
- Dev team: ?ref=main (latest)
- Staging: ?ref=v1.2.0 (production-like)
- Production: ?ref=v1.2.0 (locked, tested)

### Example 3: Public Module Distribution

**Terraform Registry:** https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws

**Published by:** HashiCorp team

**Usage:**
```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"
  
  name = "my-vpc"
  cidr = "10.0.0.0/16"
}
```

**Benefits:**
- Discoverability
- Community validation
- Professional support

---

## Common Workflows

### Workflow 1: Create and Version Module

```bash
# 1. Create module locally
mkdir -p modules/my-resource
# ... create main.tf, variables.tf, outputs.tf

# 2. Test locally
tofu init
tofu apply

# 3. Initialize git
cd modules
git init
git add -A
git commit -m "Initial my-resource module"

# 4. Create remote repository
# Go to GitHub.com → New Repository
# github.com/username/terraform-modules

# 5. Push to remote
git remote add origin https://github.com/username/terraform-modules.git
git branch -M main
git push -u origin main

# 6. Create release
git tag -a v1.0.0 -m "First release"
git push origin v1.0.0

# 7. Use in other projects
# source = "github.com/username/terraform-modules.git//my-resource?ref=v1.0.0"
```

### Workflow 2: Update Module Version

```bash
# 1. Make changes to module
# Edit: modules/my-resource/main.tf

# 2. Commit changes
git add -A
git commit -m "Add new feature to my-resource"

# 3. Create new release
git tag -a v1.1.0 -m "Add parameter X"
git push origin main
git push origin v1.1.0

# 4. Update consuming projects
# Change: ?ref=v1.0.0 → ?ref=v1.1.0
# Run: tofu init && tofu apply
```

### Workflow 3: Version Control in Multi-Project Setup

```
Project A:
  source = "github.com/org/modules.git//vpc?ref=v1.0.0"
  source = "github.com/org/modules.git//ec2?ref=v1.0.0"

Project B:
  source = "github.com/org/modules.git//vpc?ref=v2.0.0"  # Upgraded
  source = "github.com/org/modules.git//ec2?ref=v1.1.0"  # Partial upgrade
  
Project C:
  source = "github.com/org/modules.git//vpc?ref=main"    # Development
  source = "github.com/org/modules.git//ec2?ref=main"
```

---

## Troubleshooting

### Issue 1: Module Not Found

**Error:**
```
Error: Failed to download module from github.com/...
```

**Solutions:**
- Verify GitHub URL format
- Confirm repository is public
- Check ?ref parameter exists as tag/branch
- Verify path inside repository

### Issue 2: VCPULimitExceeded

**Error:**
```
VcpuLimitExceeded: You have requested more vCPU capacity...
```

**Solutions:**
- Destroy unused instances: `tofu destroy`
- Use smaller instance types (t3.nano)
- Request vCPU limit increase on AWS console
- Reduce number of instances

### Issue 3: Module Not Updating

**Issue:** Changed GitHub code but OpenTofu uses cached version

**Solution:**
```bash
# Remove cache and reinitialize
rm -rf .terraform
tofu init
```

### Issue 4: Ambiguous Version Reference

**Error:**
```
Error: Conflicting module instantiations
```

**Solution:**
- Use unique module names
- Check for duplicate module blocks
- Ensure module names don't conflict

---

## Best Practices

✅ **DO:**
- Pin versions in production (?ref=v1.0.0)
- Use semantic versioning
- Document module changes
- Test before upgrading
- Use branches for development (?ref=develop)

❌ **DON'T:**
- Use modules without version pins
- Deploy to production without testing
- Assume module compatibility
- Ignore breaking changes
- Modify modules directly

---

## Summary

**Section 7 teaches:**

1. How to use local modules (foundation)
2. How to publish modules to GitHub
3. How to version with Git tags
4. How to reference specific versions
5. How to discover public modules
6. How to implement enterprise-scale infrastructure sharing

**Key Achievement:**
From individual infrastructure developers → team collaboration on infrastructure code

---

## Next Steps

1. **Create GitHub Account** (if not already done)
2. **Create Repository** for your modules
3. **Push Local Module** to repository
4. **Create Version Tags** (v1.0.0, v1.1.0, etc.)
5. **Reference Module** in other projects
6. **Collaborate** with team on shared infrastructure code

---

## Resources

- **OpenTofu Modules**: https://opentofu.org/docs/language/modules/
- **GitHub Module Source**: https://opentofu.org/docs/language/modules/sources/#github
- **Terraform Registry**: https://registry.terraform.io
- **Semantic Versioning**: https://semver.org
- **Git Basics**: https://git-scm.com/docs

---

**Lab 2 - Section 7 Conceptual Deployment Ready! 🎉**

All configuration files created and documented.
Ready for deployment once vCPU limits are addressed.
