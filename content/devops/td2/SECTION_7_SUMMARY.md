# Section 7 Summary: Using OpenTofu Modules from GitHub

## Overview

Section 7 teaches how to use and version OpenTofu modules hosted on GitHub, moving from local development to production-ready, shared infrastructure code.

---

## What You Learn

### 1. GitHub Module Sources
- Syntax: `github.com/username/repo.git//path/to/module`
- Enables code reuse across projects and teams
- Foundation for enterprise infrastructure automation

### 2. Module Versioning
- **Git Tags**: Semantic versioning (v1.2.3)
- **Branches**: Development/production separation
- **Commits**: Precise, but harder to maintain
- **Recommendations**: Use tags in production

### 3. Public Module Ecosystems
- Terraform Registry (registry.terraform.io)
- GitHub open-source communities
- Standardized, tested, production-ready

### 4. Version Constraints
```hcl
# Latest on branch
source = "github.com/user/repo.git//module?ref=main"

# Specific tag (RECOMMENDED for production)
source = "github.com/user/repo.git//module?ref=v1.0.0"

# Development branch
source = "github.com/user/repo.git//module?ref=develop"

# Specific commit
source = "github.com/user/repo.git//module?ref=abc123"
```

---

## Architecture

### Directory Structure

```
/home/sable/devops_base/td2/scripts/live/github-modules/
├── main.tf # Primary config
├── variables.tf # Input variables
├── outputs.tf # Output values
├── example1-local-module.tf # Local module example
├── example2-github-module-terraform-aws.tf # Registry module example
├── example3-custom-github-module.tf # Custom GitHub module
└── example4-multiple-versions.tf # Version constraint examples
```

### Module Patterns

#### Pattern 1: Local Module (Baseline)
```hcl
module "local_app" {
 source = "../../modules/ec2-instance"
 ami_id = var.ami_id
 name = "local-module"
 instance_type = "t3.micro"
 port = 8080
}
```

#### Pattern 2: GitHub Custom Module
```hcl
module "github_app" {
 source = "github.com/YOUR_USERNAME/iac-modules.git//ec2-instance?ref=v1.0.0"
 
 ami_id = var.ami_id
 name = "github-module"
 instance_type = "t3.micro"
 port = 8080
}
```

#### Pattern 3: Terraform Registry Module
```hcl
module "aws_vpc" {
 source = "terraform-aws-modules/vpc/aws"
 version = "5.0.0"
 
 name = "main-vpc"
 cidr = "10.0.0.0/16"
}
```

---

## Exercise 11: Git Versioning

### Objective
Learn to version modules using Git tags, branches, and commits.

### Key Steps

1. **Create GitHub Repository**
 ```
 github.com/YOUR_USERNAME/iac-modules
 ```

2. **Push Local Module**
 ```bash
 cd /home/sable/devops_base/td2/scripts/modules
 git init
 git add -A
 git commit -m "Initial module structure"
 git remote add origin https://github.com/YOUR_USERNAME/iac-modules.git
 git push -u origin main
 ```

3. **Create Release Tags**
 ```bash
 git tag -a v1.0.0 -m "First stable release"
 git tag -a v1.1.0 -m "Add improvements"
 git push origin v1.0.0
 git push origin v1.1.0
 ```

4. **Create Development Branch**
 ```bash
 git checkout -b develop
 git push -u origin develop
 ```

5. **Reference Specific Versions**
 ```hcl
 # Use v1.0.0
 source = "github.com/YOUR_USERNAME/iac-modules.git//ec2-instance?ref=v1.0.0"
 
 # Use v1.1.0
 source = "github.com/YOUR_USERNAME/iac-modules.git//ec2-instance?ref=v1.1.0"
 
 # Use develop branch
 source = "github.com/YOUR_USERNAME/iac-modules.git//ec2-instance?ref=develop"
 ```

### What You Learn

 Semantic versioning (v1.2.3) 
 Git tagging for releases 
 Branch-based versioning 
 Version pinning in OpenTofu 
 Production release strategies 

### Best Practices

- **Production**: Use version tags (?ref=v1.0.0)
- **Development**: Use branches (?ref=develop)
- **Staging**: Test before promoting to production
- **Documentation**: Maintain CHANGELOG.md

---

## Exercise 12: Using Public Modules

### Objective
Find and implement production-ready modules from public repositories.

### Popular Module Sources

#### Terraform Registry (registry.terraform.io)

**terraform-aws-modules/**
- ec2-instance/aws
- vpc/aws
- security-group/aws
- ecs/aws
- rds/aws
- alb/aws
- s3/aws

#### GitHub Communities

- **hashicorp/terraform-aws-modules**
- **gruntwork-io/terraform-aws-modules**
- **cloudposse/terraform-aws-modules**
- **phillipharty/terraform-modules**

### How to Use Public Modules

#### Step 1: Find Module
Visit https://registry.terraform.io/browse/modules
Search by provider, type, or keyword

#### Step 2: Read Documentation
- Module description
- Input variables (required vs optional)
- Output values
- Usage examples

#### Step 3: Copy Module Declaration
```hcl
module "example" {
 source = "terraform-aws-modules/ec2-instance/aws"
 version = "5.0.0"
}
```

#### Step 4: Configure Variables
```hcl
module "web_server" {
 source = "terraform-aws-modules/ec2-instance/aws"
 version = "5.0.0"

 name = "web-server"
 ami = "ami-0c55b159cbfafe1f0"
 instance_type = "t3.micro"
 
 tags = {
 Name = "web-prod"
 }
}
```

#### Step 5: Initialize and Deploy
```bash
tofu init
tofu plan
tofu apply
```

### Common Public Modules

#### 1. EC2 Instance Module
```hcl
source = "terraform-aws-modules/ec2-instance/aws"
version = "5.0.0"
```
- Simple EC2 instance provisioning
- Handles security groups, keypairs, etc.

#### 2. VPC Module
```hcl
source = "terraform-aws-modules/vpc/aws"
version = "5.0.0"
```
- Complete VPC with subnets
- Manages NAT gateways, route tables

#### 3. Security Group Module
```hcl
source = "terraform-aws-modules/security-group/aws"
version = "5.0.0"
```
- Predefined rules (web, ssh, db, etc.)
- Simplifies ingress/egress management

#### 4. RDS Module
```hcl
source = "terraform-aws-modules/rds/aws"
version = "6.0.0"
```
- Database provisioning
- Backup, monitoring setup

#### 5. ALB/NLB Module
```hcl
source = "terraform-aws-modules/alb/aws"
version = "9.0.0"
```
- Load balancer with target groups
- Health checks, SSL/TLS support

### Best Practices

 Always pin version (`version = "5.0.0"`) 
 Read module documentation carefully 
 Test in development first 
 Check module maturity (stars, issues, releases) 
 Review examples in module repository 
 Understand input/output variables 
 Monitor for security updates 

### Red Flags

 No version pin (use `version = "latest"` or no version) 
 No documentation or examples 
 Inactive repository (no recent commits) 
 High number of open issues 
 Minimal test coverage 
 Undocumented breaking changes 

---

## Practical Deployment

### Deploy Section 7 Example

```bash
# Navigate to github-modules
cd /home/sable/devops_base/td2/scripts/live/github-modules

# Initialize OpenTofu (downloads modules and plugins)
tofu init

# Review what will be deployed
tofu plan

# Deploy resources
tofu apply -auto-approve

# View outputs
tofu output

# Test deployed instance
curl http://<PUBLIC_IP>:8080/

# Cleanup
tofu destroy -auto-approve
```

### Expected Output

```
Apply complete! Resources: 2 added, 0 changed, 0 destroyed.

Outputs:

local_module_public_ip = "18.220.100.50"
local_module_instance_id = "i-0abc123def456"
local_module_public_dns = "ec2-18-220-100-50.us-east-2.compute.amazonaws.com"
local_module_security_group = "sg-0abc123"
```

---

## Real-World Scenarios

### Scenario 1: Multi-Team Infrastructure

**Setup:**
- Team A creates module repository
- Versions released as v1.0.0, v1.1.0, v2.0.0
- Each team references specific version

**Benefits:**
- Independent releases
- Controlled adoption
- Clear compatibility matrix

### Scenario 2: Public Module Adoption

**Setup:**
- Organization uses terraform-aws-modules
- Standardized on specific versions
- Regular review of updates

**Benefits:**
- Community-tested code
- Best practices built-in
- Reduced maintenance burden

### Scenario 3: Gradual Migration

**Setup:**
1. Start with local modules
2. Create private GitHub repository
3. Publish to public registry (optional)
4. Teams migrate incrementally

**Timeline:**
- Month 1: Local modules
- Month 2: Internal GitHub repository
- Month 3: Version releases
- Month 4+: Team migrations

---

## Technology Stack

| Component | Purpose | Use Case |
|-----------|---------|----------|
| **GitHub** | Module hosting | Version control, releases |
| **OpenTofu** | Module consumption | Module references, variables |
| **Terraform Registry** | Module discovery | Finding, evaluating modules |
| **Git Tags** | Versioning | Release markers |
| **Semantic Versioning** | Version schema | Breaking change signals |

---

## Key Learnings

1. **Module Reuse**
 - Local modules: Team/project
 - GitHub modules: Shared across projects
 - Registry modules: Community standards

2. **Versioning Strategy**
 - v1.2.3: MAJOR.MINOR.PATCH
 - MAJOR: Breaking changes
 - MINOR: New features
 - PATCH: Bug fixes

3. **Reference Patterns**
 - Production: ?ref=v1.0.0 (tag)
 - Development: ?ref=develop (branch)
 - Debugging: ?ref=abc123 (commit)

4. **Module Sourcing**
 - Local: Fastest, full control
 - GitHub: Shared, version control
 - Registry: Tested, documented

5. **Quality Assurance**
 - Understand module purpose
 - Test before production
 - Pin versions
 - Monitor updates

---

## Comparison Matrix

| Aspect | Local | GitHub | Registry |
|--------|-------|--------|----------|
| **Development Speed** | | | |
| **Reusability** | | | |
| **Documentation** | | | |
| **Community Support** | | | |
| **Maintenance Burden** | | | |
| **Version Control** | | | |

---

## Next Steps

1. **Create GitHub Repository**
 - Push your local modules
 - Create version tags

2. **Test Module References**
 - Use ?ref=v1.0.0 syntax
 - Verify module downloads

3. **Explore Public Modules**
 - Visit registry.terraform.io
 - Review popular modules
 - Study examples

4. **Implement in Projects**
 - Replace local with GitHub modules
 - Adopt public modules where applicable
 - Document decisions

5. **Establish Standards**
 - Define versioning policy
 - Create module template
 - Document best practices

---

## Configuration Files Reference

### main.tf
- Provider configuration
- Module instantiation
- Resource definitions

### variables.tf
- Input variable definitions
- Defaults
- Descriptions

### outputs.tf
- Output declarations
- Value retrieval
- Export to other modules

### examples/
- Reference configurations
- Usage patterns
- Common scenarios

---

## Common Issues & Solutions

### Issue 1: Module Not Found

**Error:** `Error: Failed to download module`

**Solution:**
- Verify GitHub URL format
- Check repository is public
- Verify ?ref parameter

### Issue 2: Version Tag Not Found

**Error:** `Error: Could not find ref: v1.0.0`

**Solution:**
- Verify tag exists: `git tag -l`
- Push tags: `git push origin v1.0.0`
- Check GitHub Releases page

### Issue 3: Module Source Conflicts

**Error:** `Error: Conflicting module instantiations`

**Solution:**
- Ensure unique module names
- Use different source paths
- Check for duplicates

---

## Resources

- **OpenTofu Modules**: https://opentofu.org/docs/language/modules/
- **Terraform Registry**: https://registry.terraform.io
- **GitHub Module Syntax**: https://opentofu.org/docs/language/modules/sources/#github
- **Semantic Versioning**: https://semver.org
- **terraform-aws-modules**: https://github.com/terraform-aws-modules

---

## Conclusion

Section 7 completes the IaC journey:

**Lab 2 Full Progression:**
1. Bash scripting (manual)
2. Ansible (configuration management)
3. Packer (image building)
4. OpenTofu (infrastructure provisioning)
5. Modules (code organization)
6. GitHub Modules (infrastructure sharing)

**Key Achievement:**
From single instance deployment to enterprise-scale module management with version control, reusability, and team collaboration.

**Ready for:**
- Production infrastructure
- Team collaboration
- Infrastructure as Code best practices
- Enterprise automation

---

**Lab 2 Complete! **

All sections (1-7) completed with exercises 3-12 successfully executed.
