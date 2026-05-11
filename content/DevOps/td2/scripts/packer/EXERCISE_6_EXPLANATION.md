Exercise 6: Multi-Provider Support in Packer

Packer supports building images for MULTIPLE providers from a single codebase.
This demonstrates infrastructure-as-code flexibility.

Original Template: AWS (Amazon EBS)
File: sample-app.pkr.hcl
- Provider: amazon-ebs
- Output: AMI (Amazon Machine Image)
- Use case: AWS EC2 instances

New Template: VirtualBox
File: sample-app-virtualbox.pkr.hcl
- Provider: virtualbox-iso
- Output: Virtual machine files (.vmdk, .ovf)
- Use case: Local development, testing, Vagrant boxes

Key Differences Between Providers:

1. Source Configuration
   AWS (amazon-ebs):
   - Uses existing AMI as base (source_ami)
   - Minimal configuration needed
   
   VirtualBox (virtualbox-iso):
   - Uses ISO image as base
   - Requires boot commands, HTTP directory setup
   - More complex configuration

2. Output Artifacts
   AWS:
   - AMI ID (ami-xxxxx)
   - Stored in AWS account
   - Ready to launch EC2 instances
   
   VirtualBox:
   - VM files (VMDK, OVF)
   - Stored locally in output-virtualbox-vm/
   - Can be imported into VirtualBox, Vagrant, etc.

3. Build Requirements
   AWS:
   - AWS credentials and permissions
   - packer-plugin-amazon installed
   - ~3-4 minutes for build
   
   VirtualBox:
   - VirtualBox software installed locally
   - ISO file or URL accessible
   - ~10-15 minutes for build
   - Requires more local resources (disk, RAM)

4. Networking
   AWS:
   - SSH over internet (dynamic IP)
   - Security groups handle access
   
   VirtualBox:
   - SSH over local network
   - HTTP server for kickstart files
   - Host machine acts as build server

Multi-Provider Build (Advanced)

You can build BOTH AWS and VirtualBox images in ONE command by combining sources:

combined-template.pkr.hcl:
-----
source "amazon-ebs" "amazon_linux" { ... }
source "virtualbox-iso" "amazon_linux" { ... }

build {
  sources = [
    "source.amazon-ebs.amazon_linux",
    "source.virtualbox-iso.amazon_linux"
  ]
  
  # Common provisioners run for BOTH
  provisioner "file" { ... }
  provisioner "shell" { ... }
}
-----

Command:
packer build combined-template.pkr.hcl

Result:
- AWS AMI created
- VirtualBox VM created
- Both with identical software stack

Benefits of Multi-Provider:

1. Single source of truth for image configuration
2. Consistent environments across cloud and local
3. Easy to test locally (VirtualBox) before deploying to AWS
4. Reduces maintenance burden
5. Enables hybrid deployments

Supported Packer Providers:

- amazon-ebs (AWS)
- google-compute (Google Cloud)
- azure-vm (Microsoft Azure)
- digitalocean (DigitalOcean)
- vmware-iso (VMware)
- virtualbox-iso (VirtualBox/Vagrant)
- docker (Container images)
- And many more...

Implementation Notes for sample-app-virtualbox.pkr.hcl:

⚠ IMPORTANT: This template is a REFERENCE implementation.
To actually build with VirtualBox, you would need:

1. VirtualBox installed on your local machine
2. packer-plugin-virtualbox installed:
   packer init sample-app-virtualbox.pkr.hcl

3. A valid ISO URL or local ISO file
   The current template uses Amazon Linux 2 ISO (example)
   You may need to adjust iso_url and iso_checksum

4. Adjust boot_command for your specific ISO
   Different ISOs require different boot sequences

5. More provisioning time (VirtualBox builds take longer)

Example to build locally:
packer init sample-app-virtualbox.pkr.hcl
packer build sample-app-virtualbox.pkr.hcl

This creates a VM in: output-virtualbox-vm/

You can then:
- Import into VirtualBox
- Convert to Vagrant box
- Use with container orchestration tools
