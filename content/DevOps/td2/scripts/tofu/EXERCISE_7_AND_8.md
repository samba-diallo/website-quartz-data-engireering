Exercise 7: What Happens If You Run tofu apply After Resources Have Been Destroyed?

Answer:
When you run `tofu destroy` followed by `tofu apply`, OpenTofu will recreate all resources that were destroyed.

Sequence of Events:
1. `tofu destroy` removes all resources (instance, security group)
   - State file is updated to reflect destroyed state
   - AWS resources are deleted

2. `tofu apply` after destruction will:
   - Read the current Terraform state (now empty)
   - Read the configuration files (main.tf, variables.tf, etc.)
   - Compare desired state (config) vs actual state (AWS)
   - Find that resources are missing
   - Create new resources from scratch

Key Differences from First Apply:
- New Instance ID will be different
- New Public IP will be assigned
- New Security Group ID will be created
- Same configuration, but fresh resources

Example:
First deployment:
- Instance ID: i-02538a44ef1b9c4d3
- Public IP: 18.220.53.35
- Security Group: sg-0a13eebec9656bbd1

After destroy + apply:
- Instance ID: i-XXXXXXXXXXXXXXXX (different)
- Public IP: X.X.X.X (different - reassigned)
- Security Group: sg-XXXXXXXXXXXXX (different)

Why This Happens:
AWS generates new identifiers for resources. The state file tracks which resources belong to which resource IDs. After destruction, the state is clean, so new apply creates completely new resources.

This is different from Terraform's "replace" operation, which would:
- Keep the same logical resource
- But AWS still generates new IDs
- Useful for immutable infrastructure patterns

---

Exercise 8: How to Deploy Multiple EC2 Instances

Solution 1: Using for_each (Recommended)

main-multi.tf:
```hcl
variable "instance_count" {
  description = "Number of instances to create"
  type        = number
  default     = 3
}

variable "instance_names" {
  description = "Names for each instance"
  type        = list(string)
  default     = ["app-instance-1", "app-instance-2", "app-instance-3"]
}

resource "aws_instance" "sample_app_multi" {
  for_each               = toset(var.instance_names)
  ami                    = var.ami_id
  instance_type          = "t3.micro"
  vpc_security_group_ids = [aws_security_group.sample_app.id]
  user_data              = file("${path.module}/user-data.sh")
  user_data_replace_on_change = true

  tags = {
    Name = each.value
  }
}

output "instance_ips" {
  description = "Public IPs of all instances"
  value       = {
    for name, instance in aws_instance.sample_app_multi :
    name => instance.public_ip
  }
}
```

Usage:
```bash
tofu apply -var="ami_id=ami-07eb809c44dd0fcab" -var='instance_names=["prod-app-1", "prod-app-2"]'
```

---

Solution 2: Using count

main-count.tf:
```hcl
variable "instance_count" {
  description = "Number of instances to create"
  type        = number
  default     = 3
}

resource "aws_instance" "sample_app_count" {
  count                  = var.instance_count
  ami                    = var.ami_id
  instance_type          = "t3.micro"
  vpc_security_group_ids = [aws_security_group.sample_app.id]
  user_data              = file("${path.module}/user-data.sh")
  user_data_replace_on_change = true

  tags = {
    Name = "sample-app-${count.index + 1}"
  }
}

output "instance_ips" {
  description = "Public IPs of all instances"
  value       = aws_instance.sample_app_count[*].public_ip
}
```

Usage:
```bash
tofu apply -var="ami_id=ami-07eb809c44dd0fcab" -var="instance_count=3"
```

---

Comparison: for_each vs count

for_each:
✅ Better naming/identification
✅ Safer when removing items (no index shifting)
✅ More readable for key-based iteration
❌ Only works with maps or sets
❌ More complex syntax

count:
✅ Simpler syntax
✅ Works for numeric iteration
✅ Good for simple cases
❌ Fragile when modifying lists (indices shift)
❌ Less readable for complex scenarios

---

Solution 3: Multiple Resource Blocks (Not Recommended)

```hcl
resource "aws_instance" "sample_app_1" {
  ami                    = var.ami_id
  instance_type          = "t3.micro"
  vpc_security_group_ids = [aws_security_group.sample_app.id]
  user_data              = file("${path.module}/user-data.sh")
  tags = { Name = "sample-app-1" }
}

resource "aws_instance" "sample_app_2" {
  ami                    = var.ami_id
  instance_type          = "t3.micro"
  vpc_security_group_ids = [aws_security_group.sample_app.id]
  user_data              = file("${path.module}/user-data.sh")
  tags = { Name = "sample-app-2" }
}

resource "aws_instance" "sample_app_3" {
  ami                    = var.ami_id
  instance_type          = "t3.micro"
  vpc_security_group_ids = [aws_security_group.sample_app.id]
  user_data              = file("${path.module}/user-data.sh")
  tags = { Name = "sample-app-3" }
}
```

❌ Not DRY (Don't Repeat Yourself)
❌ Hard to maintain
❌ Not scalable

---

Best Practice:
Use for_each for production deployments with meaningful identifiers.
Use count for simple numeric iterations.
Avoid multiple hardcoded resources.

Implementation Steps:
1. Backup current main.tf
2. Create main-multi.tf with for_each or count
3. Update variables.tf with instance count/names
4. Run: tofu plan -var='instance_names=["app1", "app2", "app3"]'
5. Run: tofu apply -var='instance_names=["app1", "app2", "app3"]'
6. Check output with: tofu output instance_ips

---

Testing Multiple Instances:
Once deployed, test all instances:

for instance_ip in $(tofu output -json instance_ips | jq '.[]' -r); do
  echo "Testing $instance_ip..."
  curl http://$instance_ip:8080/
done

This demonstrates OpenTofu's ability to manage infrastructure as code at scale.
