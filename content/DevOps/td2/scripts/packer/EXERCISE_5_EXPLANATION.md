Exercise 5: What Happens When Running Packer Build Twice?

When you run `packer build` a second time with the same template, Packer creates a NEW AMI with a DIFFERENT ID, not reuse the existing one.

Key Findings:

1. Different AMI IDs
   - First build: ami-07eb809c44dd0fcab
   - Second build: ami-079a315e32554235f

2. Different Names (Due to Timestamp)
   The ami_name parameter uses formatdate() with timestamp():
   
   ami_name = "sample-app-packer-${formatdate("YYYY-MM-DD-hhmm-ss", timestamp())}"
   
   - First build name: sample-app-packer-2025-11-26-2154-31
   - Second build name: sample-app-packer-2025-11-26-2200-11

3. Different Creation Dates
   - First AMI created: 2025-11-26T21:56:19.000Z
   - Second AMI created: 2025-11-26T22:02:04.000Z

Why This Matters:

- Packer generates a UNIQUE AMI name each time using the timestamp
- AWS allows multiple AMIs with different names, so no conflict occurs
- Each build is independent and creates a fresh AMI
- Both old AMIs remain in your AWS account (you may need to clean them up to save costs)

Idempotency in Packer:

Unlike Terraform or Ansible, Packer is NOT idempotent by default:
- Terraform: Running twice with same config → no changes (idempotent)
- Packer: Running twice with same config → creates 2 different AMIs (not idempotent)

To make Packer idempotent, you would need to:
1. Use a fixed ami_name (without timestamp) → but then second build fails if AMI exists
2. Check if AMI exists before building
3. Use a naming strategy with version numbers and cleanup old versions

Current Template Approach:
The current template uses timestamp() to ensure UNIQUE names, making each build create a new AMI.
This is useful for CI/CD pipelines where you want to track different versions.

Cleanup Recommendation:
After multiple builds, clean up old AMIs:

aws ec2 deregister-image --image-id ami-07eb809c44dd0fcab --region us-east-2 --profile labs-devops_diallo
aws ec2 deregister-image --image-id ami-079a315e32554235f --region us-east-2 --profile labs-devops_diallo

(Note: Also delete associated snapshots to avoid storage costs)
