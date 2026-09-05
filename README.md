# Technologie au collège

Ressources pédagogiques pour les classes de **5e, 4e et 3e**, dans le contexte de la Nouvelle-Calédonie.

Ce dépôt rassemble les progressions, les séquences, les supports élèves, les corrigés et les évaluations.

## Séances introductives

**[Trois séances de technologie](supports/premieres-seances/README.md)** : une première séance de 55 minutes par niveau, avec uniquement des PC.

- 5e : étudier un objet du quotidien au choix.
- 4e : simuler et corriger la commande d'un éclairage automatique.
- 3e : comprendre les chaînes d'information et d'énergie d'un portail automatique.

[Dossier complet à télécharger](supports/premieres-seances/seances-technologie-college.zip) · [Guide professeur et corrigés](supports/premieres-seances/guide-professeur.pdf) · [Cours illustrés et traces écrites](supports/premieres-seances/cours-illustres.pdf)

Chaque séance commence par une accroche de 5 minutes et un cours explicite de 7 minutes, suivi de 25 minutes d’activité, 10 minutes de correction, 5 minutes de trace écrite et 3 minutes de bilan. Les PDF AVANT et APRÈS sont séparés pour distribuer les documents au bon moment. Les élèves peuvent les consulter sur leur PC ; la projection est facultative. Le guide contient les explications à donner et les réponses attendues aux questions orales.

Les activités HTML s'ouvrent localement dans un navigateur, sans compte ni installation. Les fiches PDF sont imprimables et les fichiers Markdown modifiables.

## Accès par niveau

| Niveau | Progression et séquences |
| --- | --- |
| 5e | [Ouvrir le dossier de 5e](5e/README.md) |
| 4e | [Ouvrir le dossier de 4e](4e/README.md) |
| 3e | [Ouvrir le dossier de 3e](3e/README.md) |

## Modèles communs

- [Fiche de séquence](modeles/sequence.md) : problématique, compétences, articulation des séances et évaluation.
- [Fiche professeur pour une séance](modeles/seance-professeur.md) : préparation, déroulement, aides et bilan.
- [Fiche élève](modeles/fiche-eleve.md) : consignes, documents, production attendue et synthèse.
- [Corrigé](modeles/corrige.md) : réponses attendues, variantes acceptables et erreurs fréquentes.
- [Évaluation](modeles/evaluation.md) : sujet, critères de réussite et barème ou niveaux de maîtrise.
- [Références et ressources](ressources/README.md) : textes officiels et suivi des sources.

## Organisation d'une séquence

Chaque séance est rangée dans le dossier de son niveau, par exemple `5e/S01-objet-du-quotidien/`. Les trois premières séances sont disponibles ; les modèles permettent de construire les séquences suivantes.

| Fichier ou dossier | Contenu |
| --- | --- |
| `sequence.md` | Vue d'ensemble et objectifs |
| `S01-professeur.md`, `S02-professeur.md`… | Déroulement de chaque séance |
| `S01-eleve.md`, `S02-eleve.md`… | Documents distribués aux élèves |
| `S01-corrige.md`, `S02-corrige.md`… | Corrigés et indications pour le professeur |
| `S01-cours.md` | Explications orales, questions et trace écrite |
| `evaluation.md` et `evaluation-corrige.md` | Sujet final et correction |
| `documents/` | Images, documents et fichiers nécessaires à l'activité |
| `exports/` | Versions finales destinées à l'impression ou à la distribution |

Les fichiers Markdown constituent les versions modifiables. Des versions PDF ou Word pourront accompagner les supports finalisés.

## Régénérer les supports

Avec Python et ReportLab : `python scripts/generer_supports.py`. Les contenus d’activité sont dans `scripts/contenus.py` ; les cours, dessins et déroulements révisés dans `scripts/introductions.py`. L’option `--reuse-student-pdfs` conserve les fiches élèves PDF déjà générées lorsque seuls les cours et le guide changent.

## Principes de conception

- Partir d'un problème concret et définir une production observable de l'élève.
- Relier chaque séquence à des compétences du programme applicable au niveau et à l'année scolaire concernés ; conserver le lien vers le texte utilisé.
- Adapter la durée, les consignes et les activités au matériel réellement disponible.
- Prévoir une aide progressive et un approfondissement, ainsi qu'un court bilan individuel.
- Distinguer clairement la fiche élève du corrigé et rendre explicites les critères de réussite.
- Après utilisation en classe, noter les ajustements utiles pour la prochaine séance.

## Contexte de préparation

Matériel confirmé : des PC pour les élèves. Priorité indiquée pour les 3e : chaînes d'information et d'énergie. La durée de 55 minutes est une hypothèse de préparation. Les créneaux exacts et les acquis déjà travaillés pourront guider les séances suivantes.
