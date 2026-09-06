# Génération des supports

Depuis la racine du dépôt : `python scripts/generer_supports.py`.

Dépendances Python : `reportlab` et `pypdf`.

- `contenus.py` : questions, documents, déroulements et corrigés.
- `activites.py` : pages numériques de consultation et simulateurs ; aucune réponse élève à saisir.
- `parcours_guide.py` : adaptation très guidée de 5e.
- `portail.py` et `visuels.py` : illustrations vectorielles.
- `generer_supports.py` : PDF, sources Markdown et index des séquences.

Les réponses élèves sont exclusivement sur papier. Les pages numériques renvoient aux questions de la fiche et proposent les documents ou essais nécessaires.

Chaque séquence contient `eleves/a-imprimer/`, `eleves/sur-pc/`, `professeur/`, `sources/` et `documents/`. Les PDF finaux sont directement générés dans leur dossier d'usage. Modifier les sources avant de régénérer ; maintenir l'accueil professeur et les index de niveau en cohérence.

Conserver les dates absentes des documents et des métadonnées PDF. Les URL des références officielles restent intactes. Aucun fichier ZIP.
