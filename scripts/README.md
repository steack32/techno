# Génération des supports

Depuis la racine du dépôt : `python scripts/generer_supports.py`.

Dépendances Python : `reportlab` et `pypdf`.

- `contenus.py` : contenus pédagogiques des séquences.
- `activites.py` : activités HTML et schémas.
- `portail.py` : vue vectorielle du portail et repères communs aux documents élèves et corrigés.
- `generer_supports.py` : sources Markdown et exports PDF.

Chaque séquence est générée dans le dossier de son niveau, sous son nom thématique. Son guide professeur et ses PDF élèves sont rangés dans son dossier `exports/`. Les PDF élèves intermédiaires sont produits dans `output/pdf/`, ignoré par Git.

Le script ne crée ni archive ni dossier temporel. Les titres, pieds de page, champs élèves et réponses exportées restent sans dates. Les métadonnées de création et de modification des PDF sont supprimées. Les adresses des sources officielles sont conservées intactes.

La génération remplace les supports des séquences concernées : modifier les sources Python avant de régénérer. Les index de niveau se maintiennent directement en Markdown.
