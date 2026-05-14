# Documentation du projet

Documentation interne (workflow de développement). Ces fichiers **ne sont pas
publiés** sur le site — ils restent hors du dossier `content/`.

## Sommaire

- **[MISE_A_JOUR_SITE.md](MISE_A_JOUR_SITE.md)** — Guide complet : en cas de
  modification (notebook, preuves, page markdown), comment mettre à jour le site
  jusqu'au déploiement GitHub → Cloudflare. Contient toutes les commandes
  détaillées, un tableau des chemins par lab, une checklist avant push et une
  section dépannage.

## Mémo express

```bash
cd "/home/sable/Documents/E4FD/S4/Data Engineering"

# Après avoir édité un notebook source (.ipynb) :
# 1) régénérer le HTML rendu        → nbconvert --to html ... quartz/static/nb/...
# 2) recopier le .ipynb             → cp ... content/...
# 3) prévisualiser                  → npx quartz build --serve
# 4) publier                        → git add -A && git commit -m "..." && git push origin main
```

Détails et exemples concrets : voir [MISE_A_JOUR_SITE.md](MISE_A_JOUR_SITE.md).
