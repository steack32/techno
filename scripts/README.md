# Génération des supports

`generer_supports.py` utilise les contenus de `contenus.py` et les activités de `activites.py`.

Depuis la racine du dépôt : `python scripts/generer_supports.py`.

Dépendance : ReportLab. Les PDF sont produits dans `output/pdf/`, puis copiés dans le dossier `exports/` de chaque séance. Le guide commun est rangé dans `supports/premieres-seances/`. Le script ne crée aucune archive.

Attention : la génération remplace les supports des premières séances. Modifier les sources Python avant de régénérer. Les README de niveau et l'index commun se maintiennent directement en Markdown.
