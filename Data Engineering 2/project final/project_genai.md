# Déclaration d'utilisation de l'IA Générative

Dans le cadre du projet final du cours de **Data Engineering II (Data-Intensive Workloads)**, l'IA générative (notamment Claude/Gemini) a été utilisée comme outil d'assistance pour le développement et la rédaction.

## Usages spécifiques :

1. **Architecture et Cadrage** : L'IA a été utilisée pour structurer le projet en respectant les consignes du professeur, notamment pour vérifier la cohérence de l'architecture Medallion et des flux de streaming.
2. **Rédaction de code boilerplate** : Génération de la structure de base des scripts PySpark, configuration de la journalisation (logs JVM) et configuration du Structured Streaming.
3. **Implémentation de la charge itérative** : Assistance pour l'écriture de l'algorithme PageRank via des jointures itératives (sans dépendre de GraphFrames).
4. **Correction de bugs** : Aide au débogage d'erreurs liées au schéma JSON fortement imbriqué (erreurs liées à `payload` lors du passage à la couche Silver) et aux fuites de mémoire (OOM Java heap space) en affinant les requêtes `.select()`.
5. **Rédaction de la documentation** : Aide à la mise en forme du rapport final, du fichier `data_card.md` et des commentaires de code pour correspondre aux attentes professionnelles.

Les concepts de traitement de graphes, de l'index inversé et des SLO (latence, taille) ont été activement choisis, paramétrés et validés par moi-même (Samba DIALLO) et mon binôme. Le code a été exécuté, testé et ajusté en local sur nos machines pour générer les preuves requises.
