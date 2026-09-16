# Organisation du site

Navigation publique : accueil → niveau (`5eme`, `4eme`, `3eme`) → séquence → séances et documents élèves.

Le catalogue `site/catalogue.json` définit les séquences et leur ordre dans chaque niveau. Ajouter une entrée au catalogue crée automatiquement la carte du niveau et la navigation. Pour une séquence avec une page spécifique, placer cette page dans `site/<niveau>/<sequence>/index.html`. Les activités historiques gardent leurs sources dans les dossiers `5e`, `4e`, `3e` ; le build les publie sous les adresses longues.

Ne pas éditer `dist` : ce dossier est généré par `node scripts/build-site.mjs`. Les anciennes adresses `/3e/...`, `/4e/...` et `/5e/...` redirigent vers les nouvelles.

Le build utilise une liste explicite de fichiers élèves. Aucun dossier professeur n’est copié dans les fichiers publics. Les corrigés hébergés dans le stockage privé restent disponibles après authentification, et les adresses de l’API d’évaluation ne changent pas.
