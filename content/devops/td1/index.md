---
title: "TD1 - Introduction au Déploiement d'Applications"
publish: true
---

> Students : DIALLO Samba & DIOP Mouhamed
---

# TD1 - Introduction au Déploiement d'Applications

Auteur: Badr TAJINI - DevOps Data for SWE - ESIEE - 2025

## Overview

TD1 introduces fundamental cloud computing concepts and the basics of deploying applications to the cloud. This lab focuses on understanding different deployment models and getting hands-on experience with AWS services.

## Objectives

- Understand what servers are and how they work
- Learn to deploy applications locally
- Explore cloud deployment models (IaaS, PaaS, SaaS)
- Get started with AWS EC2 (Elastic Compute Cloud)
- Deploy a simple Node.js application to the cloud

## Lab Content

### 1. Local Deployment

The lab starts with running a simple "Hello, World" Node.js application locally:

- Creating a minimal web server with Node.js
- Understanding localhost and network interfaces
- Testing applications in a local development environment

### 2. Cloud Computing Models

Introduction to different service models:

- **IaaS (Infrastructure as a Service)**: AWS EC2 - Direct access to compute resources
- **PaaS (Platform as a Service)**: AWS Elastic Beanstalk, Heroku - Managed platform for applications
- **SaaS (Software as a Service)**: Fully managed applications

### 3. AWS EC2 Basics

Hands-on experience with AWS's core compute service:

- Understanding EC2 instances and instance types
- Launching and managing virtual servers
- Connecting to instances via SSH
- Basic security groups and networking

### 4. Deploying to AWS

Practical deployment of the Node.js sample app:

- Preparing an application for cloud deployment
- Configuring EC2 instances
- Running applications on remote servers
- Exposing applications to the internet

## Prerequisites

- AWS Account with appropriate credentials
- Node.js installed locally (v23+ recommended)
- Basic command-line knowledge
- SSH client for remote connections

## Directory Structure

```
td1/
├── README_TD1.md           # This file
├── lab1.pdf                # Original lab instructions
├── aws_support.txt         # AWS configuration notes
└── scripts/                # Deployment scripts and utilities
```

## Key Concepts Learned

1. **Local Development**: Running applications on your own machine before cloud deployment
2. **Server Fundamentals**: Understanding what a server is and how it differs from localhost
3. **Cloud Services**: Differentiating between IaaS, PaaS, and SaaS models
4. **AWS EC2**: Launching and managing virtual servers in the cloud
5. **Remote Deployment**: Moving from local development to production-ready cloud hosting

## Getting Started

1. Review the lab1.pdf document for detailed instructions
2. Set up your AWS credentials
3. Follow the exercises to deploy the sample Node.js application
4. Experiment with different EC2 instance types and configurations

## Documentation Complète

Pour plus de détails sur le TD1, consultez:
- [[devops/td1/readme|Documentation complète du TD1 (Français)]]

## Fichiers Scripts

Les scripts et fichiers de configuration sont disponibles:
- [user-data.sh](/static/devops/td1/scripts/user-data.sh) - Script d'initialisation EC2
- [app.js](/static/devops/td1/scripts/app.js) - Application Node.js exemple

## Ressources

- Documentation AWS EC2: https://docs.aws.amazon.com/ec2/
- Site Officiel Node.js: https://nodejs.org/
- AWS Free Tier: https://aws.amazon.com/free/

## Notes

Ce TD établit les fondations pour les labs suivants qui s'appuient sur ces concepts de déploiement cloud, incluant l'Infrastructure as Code (TD2), les stratégies de déploiement avancées (TD3), et les pipelines CI/CD (TD5).
