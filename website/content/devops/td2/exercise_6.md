---
title: "TD2 - Exercice 6: Support Multi-Provider Packer"
publish: true
---

> Students : DIALLO Samba & DIOP Mouhamed
---

# Exercice 6: Support Multi-Provider dans Packer

Packer supporte la construction d'images pour PLUSIEURS providers à partir d'une seule base de code.
Ceci démontre la flexibilité de l'infrastructure-as-code.

## Modèle Original: AWS (Amazon EBS)

**Fichier**: sample-app.pkr.hcl
- **Provider**: amazon-ebs
- **Sortie**: AMI (Amazon Machine Image)
- **Cas d'usage**: Instances AWS EC2

## Nouveau Modèle: VirtualBox

**Fichier**: sample-app-virtualbox.pkr.hcl
- **Provider**: virtualbox-iso
- **Sortie**: Fichiers de machine virtuelle (.vmdk, .ovf)
- **Cas d'usage**: Développement local, tests, boîtes Vagrant

## Différences Clés Entre les Providers

### 1. Configuration de la Source

**AWS (amazon-ebs)**:
- Utilise une AMI existante comme base (source_ami)
- Configuration minimale nécessaire

**VirtualBox (virtualbox-iso)**:
- Utilise une image ISO comme base
- Nécessite des commandes de boot, configuration du répertoire HTTP
- Configuration plus complexe

### 2. Artefacts de Sortie

**AWS**:
- ID AMI (ami-xxxxx)
- Stocké dans le compte AWS
- Prêt à lancer des instances EC2

**VirtualBox**:
- Fichiers VM (VMDK, OVF)
- Stockés localement dans output-virtualbox-vm/
- Peuvent être importés dans VirtualBox, Vagrant, etc.

### 3. Exigences de Construction

**AWS**:
- Identifiants AWS et permissions
- packer-plugin-amazon installé
- ~3-4 minutes pour la construction

**VirtualBox**:
- Logiciel VirtualBox installé localement
- Fichier ISO ou URL accessible
- ~10-15 minutes pour la construction
- Nécessite plus de ressources locales (disque, RAM)

### 4. Réseau

**AWS**:
- SSH via Internet (IP dynamique)
- Les groupes de sécurité gèrent l'accès

**VirtualBox**:
- SSH via réseau local
- Serveur HTTP pour les fichiers kickstart
- La machine hôte agit comme serveur de construction

## Construction Multi-Provider (Avancé)

Vous pouvez construire à la fois des images AWS et VirtualBox en UNE commande en combinant les sources:

```hcl
# combined-template.pkr.hcl
source "amazon-ebs" "amazon_linux" { ... }
source "virtualbox-iso" "amazon_linux" { ... }

build {
  sources = [
    "source.amazon-ebs.amazon_linux",
    "source.virtualbox-iso.amazon_linux"
  ]
  
  # Provisionneurs communs exécutés pour LES DEUX
  provisioner "file" { ... }
  provisioner "shell" { ... }
}
```

**Commande**:
```bash
packer build combined-template.pkr.hcl
```

**Résultat**:
- AMI AWS créée
- VM VirtualBox créée
- Les deux avec une pile logicielle identique

## Avantages du Multi-Provider

1. Source unique de vérité pour la configuration d'image
2. Environnements cohérents entre cloud et local
3. Facile à tester localement (VirtualBox) avant de déployer sur AWS
4. Réduit la charge de maintenance
5. Permet des déploiements hybrides

## Providers Packer Supportés

- **amazon-ebs** (AWS)
- **google-compute** (Google Cloud)
- **azure-vm** (Microsoft Azure)
- **digitalocean** (DigitalOcean)
- **vmware-iso** (VMware)
- **virtualbox-iso** (VirtualBox/Vagrant)
- **docker** (Images de conteneurs)
- Et bien d'autres...

## Notes d'Implémentation pour sample-app-virtualbox.pkr.hcl

IMPORTANT: Ce modèle est une implémentation de RÉFÉRENCE.
Pour construire réellement avec VirtualBox, vous auriez besoin de:

1. **VirtualBox** installé sur votre machine locale

2. **packer-plugin-virtualbox** installé:
```bash
packer init sample-app-virtualbox.pkr.hcl
```

3. **Une URL ISO valide** ou un fichier ISO local
   - Le modèle actuel utilise Amazon Linux 2 ISO (exemple)
   - Vous devrez peut-être ajuster iso_url et iso_checksum

4. **Ajuster boot_command** pour votre ISO spécifique
   - Différents ISOs nécessitent différentes séquences de boot

5. **Plus de temps de provisionnement** (les constructions VirtualBox prennent plus de temps)

### Exemple pour construire localement:

```bash
packer init sample-app-virtualbox.pkr.hcl
packer build sample-app-virtualbox.pkr.hcl
```

Cela crée une VM dans: `output-virtualbox-vm/`

Vous pouvez ensuite:
- Importer dans VirtualBox
- Convertir en boîte Vagrant
- Utiliser avec des outils d'orchestration de conteneurs

## Conclusion

Le support multi-provider de Packer permet de:
- Maintenir une configuration d'infrastructure unique
- Déployer sur plusieurs environnements
- Tester localement avant la production
- Réduire la duplication de code
- Faciliter les migrations entre providers
