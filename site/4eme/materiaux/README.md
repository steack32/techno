# Matériaux et résistance

Quatre séances de 55 minutes pour les 4e. Travail en binôme, avec deux questions individuelles en séance 4. Pas de note automatique, de nom ni de classe à saisir par les élèves.

- Séance 1 : familles, propriétés, comparaison à volume et géométrie constants.
- Séance 2 : traction, compression, flexion, torsion ; élasticité, déformation permanente, rupture.
- Séance 3 : référence et trois essais ; influence de l'épaisseur et de la portée ; comparaison plein/creux.
- Séance 4 : défi à contraintes multiples, justification et limites du modèle.

Les réponses sont conservées dans les tables `materiaux_*` du Durable Object existant. Le code privé permet la reprise, la référence `M-…` permet au professeur de retrouver le carnet. Les boutons d'enregistrement du simulateur copient les résultats dans les réponses sauvegardées. Les positions des réglages du simulateur sont réinitialisées à la réouverture ; les essais consignés sont conservés.

La page professeur est `/professeur/materiaux/`, avec la même connexion que les contrôles. Les réglages facultatifs de classe et d'ouverture sont similaires à ceux des ponts ; par défaut tout est ouvert.

## Modèle

Poutre simplement appuyée, charge ponctuelle au centre, largeur 0,25 m. Formule de flèche élastique : F L³ / (48 E I). La masse est la masse volumique multipliée par le volume. Constantes pédagogiques arrondies : bois longitudinal E=10 GPa / rho=600 kg/m³, aluminium 69 / 2700, acier 200 / 7850. Section rectangulaire pleine ou caisson métallique à parois de 1,5 mm. La section creuse n'est pas proposée pour le bois.

Le modèle ne calcule pas la rupture, les assemblages, le poids propre, le fluage ou le flambement local. La flèche dessinée est amplifiée ; au-delà de L/100, l'élève voit un avertissement de grande déformation. Les seuils 3 mm et 2 kg sont les contraintes de l'exercice, pas des normes de construction.

Sources scientifiques :
- https://home.eng.iastate.edu/~shermanp/STAT447/STAT%20Articles/Beam_Deflection_Formulae.pdf
- https://www-materials.eng.cam.ac.uk/mpsite/properties/Ie/stiffness.html

Tests : `node tests/materiaux-model.test.mjs` et `node tests/materiaux.test.mjs`.
Synthèse : `scripts/generate-material-pdf.py`, deux pages A4 (ReportLab et DejaVu Sans).
