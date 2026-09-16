# Déploiement Cloudflare

Le Worker porte le nom `techno`. Depuis la racine du dépôt, la commande existante
`npx wrangler deploy` lit `wrangler.jsonc`, lance `node scripts/build-site.mjs`
et publie uniquement `dist/`. Aucun réglage de build supplémentaire n'est requis.

Dans Cloudflare : dépôt `steack32/techno`, branche `main`, répertoire racine du dépôt,
commande de déploiement `npx wrangler deploy`. Un commit sur la branche connectée
déclenche normalement un nouveau déploiement. Vérifier son résultat dans Déploiements.

## Vérification locale

Exécuter `node scripts/build-site.mjs`, puis servir le dossier `dist/` avec un serveur HTTP.
Le script utilise uniquement les modules intégrés à Node.js.

## Contenu publié

La liste explicite dans `scripts/build-site.mjs` contient les ressources HTML et PDF
des élèves pour les trois séances existantes. La page d'accueil est dans `site/index.html`.
Les fichiers professeur, corrigés, sources et scripts ne sont pas copiés dans `dist/`.
Cette exclusion ne rend pas confidentiels les fichiers présents dans un dépôt GitHub public.

## Évaluation numérique

Ce déploiement concerne les ressources élèves existantes, pas une évaluation notée.
Le fichier de l'évaluation avec note sur 20 et niveaux de compétences n'a pas été retrouvé.
Il reste à l'intégrer. Une évaluation dont on veut protéger les réponses doit notamment
effectuer la correction côté serveur ; aucune protection ne garantit l'absence de triche.
