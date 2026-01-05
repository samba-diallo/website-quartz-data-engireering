# DevOps Labs - ESIEE 2025

**Authors**: DIALLO Samba, DIOP Mouhamed  
**Course Instructor**: Badr TAJINI - DevOps Data for SWE  
**Institution**: ESIEE PARIS - E4FD Program  
**Academic Year**: 2025-2026

## Project Overview

This repository contains practical lab work (TD - Travaux Dirigés) from the DevOps course at ESIEE. The labs progress from basic cloud deployment concepts to advanced CI/CD pipelines and GitOps practices, using AWS as the primary cloud platform.

## Repository Structure

### [TD1 - Introduction to Deploying Apps](td1/README_TD1.md)
**Focus**: Cloud Computing Fundamentals

Learn the basics of deploying applications to the cloud, understanding different service models (IaaS, PaaS, SaaS), and getting hands-on with AWS EC2. Deploy a simple Node.js application from your local machine to AWS.

**Key Topics**: Localhost vs servers, EC2 instances, SSH connections, basic networking

---

### [TD2 - Managing Infrastructure as Code](td2/README.md)
**Focus**: IaC Tools and Automation

Master Infrastructure as Code principles using Bash, Ansible, Packer, and OpenTofu (Terraform-compatible). Covers exercises 3-12 from the course, progressing from basic scripts to reusable modules and version control.

**Key Topics**: AWS CLI automation, configuration management, AMI building, declarative infrastructure, modules, GitHub integration

---

### [TD3 - Advanced Infrastructure Patterns](td3/README_TD3.md)
**Focus**: Production-Ready Infrastructure

Build scalable and resilient cloud architectures using Auto Scaling Groups, Load Balancers, Lambda functions, and API Gateway. Learn to design infrastructure that handles real-world production requirements.

**Key Topics**: ASG, ALB, serverless computing, multi-tier architectures, high availability

---

### [TD4 - Testing and Version Control](td4/README_TD4.md)
**Focus**: Infrastructure Quality and Reliability

Implement testing strategies for infrastructure code, including unit tests, integration tests, and end-to-end validation. Master Git workflows for infrastructure changes.

**Key Topics**: OpenTofu testing, test-driven infrastructure, Git branching strategies, code review processes

---

### [TD5 - CI/CD Pipelines](td5/README_TD5.md)
**Focus**: Continuous Integration and Deployment

Automate infrastructure and application deployment using GitHub Actions. Configure AWS OIDC for secure authentication, implement automated testing, and create deployment pipelines that run on every code change.

**Key Topics**: GitHub Actions workflows, AWS OIDC, automated testing, tofu plan/apply automation, PR-based deployments

---

### [TD6 - GitOps Practices](td6/README_TD6.md)
**Focus**: GitOps and Advanced Automation  
**Statut**: ❌ ABANDONNÉ (raisons financières)

Explore GitOps methodologies for managing infrastructure and applications through Git. This TD was abandoned due to AWS Organizations costs that exceed the Free Tier limits.

**Key Topics**: Multi-account AWS (not implemented), OpenTofu workspaces, Kubernetes multi-services

**Note**: Alternatives gratuites disponibles avec Kubernetes local (Docker Desktop, Minikube)

---

## Final Project: EcoData Platform (DevOps)

Le projet final du cours DevOps consiste à

**Livrables principaux :**
- Code source (backend, frontend, config)
- Scripts d’infrastructure (Docker, K8s)
- Pipeline CI/CD
- Rapport technique et guide de déploiement

**Objectifs pédagogiques :**
- Maîtriser l’automatisation du déploiement applicatif
- Appliquer les pratiques DevOps modernes
- Documenter et sécuriser une stack cloud complète

## Technology Stack

### Cloud Platform
- **AWS** (Amazon Web Services)
  - EC2, Auto Scaling Groups, Load Balancers
  - Lambda, API Gateway (serverless)
  - S3, DynamoDB (state management)
  - IAM (security and permissions)

### Infrastructure as Code
- **OpenTofu** (Terraform-compatible) - Primary IaC tool
- **Packer** - Machine image building
- **Ansible** - Configuration management

### CI/CD
- **GitHub Actions** - Automation workflows
- **GitHub OIDC** - Secure AWS authentication

### Development
- **Node.js** - Sample application runtime
- **Jest** - Application testing
- **Docker** - Containerization
- **Bash** - Scripting and automation

### Version Control
- **Git** - Source control
- **GitHub** - Repository hosting and collaboration

---

## Prerequisites

To work with these labs, you'll need:

- AWS Account with appropriate credentials
- AWS CLI installed and configured
- OpenTofu or Terraform installed
- Ansible and Packer installed
- Node.js runtime (v23+ recommended)
- Git and GitHub account
- Docker (for containerization exercises)
- Basic command-line proficiency
- SSH client for remote connections

## Getting Started

1. **Clone this repository**
   ```bash
   git clone https://github.com/samba-diallo/Devops.git
   cd devops_base
   ```

2. **Configure AWS credentials**
   ```bash
   aws configure
   # Enter your AWS Access Key ID and Secret Access Key
   ```

3. **Choose a lab and follow its README**
   - Each TD directory contains detailed instructions
   - Start with TD1 if you're new to cloud deployment
   - Labs build on each other progressively

4. **Important**: Always clean up AWS resources after testing to avoid unnecessary costs

## Project Philosophy

This project follows modern DevOps best practices:

- **Infrastructure as Code**: All infrastructure is version-controlled and reproducible
- **Automation First**: Manual processes are minimized through scripting and CI/CD
- **Modular Design**: Reusable components that can be shared across projects
- **Security by Default**: OIDC authentication, no hardcoded credentials
- **Testing Culture**: Infrastructure changes are tested before deployment
- **Documentation**: Clear README files for each lab with examples and explanations

## Resource Management

**Important**: AWS resources incur costs. Always remember to:

1. Destroy resources after testing: `tofu destroy` or `aws ec2 terminate-instances`
2. Check the AWS Console for orphaned resources
3. Delete AMIs and snapshots created during labs
4. Monitor your AWS billing dashboard regularly

## Additional Documentation

- Detailed implementation notes are in each TD's directory
- Exercise-specific guides in `scripts/*/EXERCISE_*.md` files
- Comprehensive references in `Others/` subdirectories
- Original lab PDFs included where available

## Repository Highlights


---

## Final Project: EcoData Platform (DevOps)

Le projet final du cours DevOps consiste à concevoir, documenter et déployer une application web complète (frontend Streamlit, backend FastAPI, base PostgreSQL) sur une infrastructure cloud automatisée. Il met en œuvre Docker, Kubernetes, CI/CD (GitHub Actions), bonnes pratiques DevOps, et une documentation technique détaillée. Le code et la documentation du projet final sont disponibles dans le dossier `projet-final-devops/ecodata-platform/`.

**Livrables principaux :**
- Code source (backend, frontend, config)
- Scripts d’infrastructure (Docker, K8s)
- Pipeline CI/CD
- Rapport technique et guide de déploiement

**Objectifs pédagogiques :**
- Maîtriser l’automatisation du déploiement applicatif
- Appliquer les pratiques DevOps modernes
- Documenter et sécuriser une stack cloud complète

