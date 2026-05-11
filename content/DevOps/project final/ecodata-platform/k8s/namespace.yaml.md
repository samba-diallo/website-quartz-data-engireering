---
date: 2026-05-11
draft: false
tags:
- devops
- ecodata-platform
- kubernetes
title: namespace.yaml
---

# namespace.yaml

Fichier : `namespace.yaml`  (133 octets, langage `yaml`)

[Telecharger le fichier brut](./namespace.yaml)

## Contenu

```yaml
# Namespace pour l'application EcoData Platform
apiVersion: v1
kind: Namespace
metadata:
  name: ecodata
  labels:
    name: ecodata
```
