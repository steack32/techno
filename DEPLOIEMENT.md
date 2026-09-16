# Évaluations de technologie sur Cloudflare

Le Worker `techno` publie les ressources élèves et deux évaluations :

- `/evaluations/` : accès élèves par code de séance ;
- `/professeur/` : connexion professeur, séances, copies et export CSV ;
- `/api/evaluations/health` : état technique sans données personnelles.

Le contrôle de 4e reprend le document « Comment choisir ma trottinette électrique ? » fourni par le professeur. Il comporte 20 questions, vaut 20 points et dure 25 minutes par défaut. Mission Savon reprend les 20 questions et variantes de l’évaluation de 3e existante ; elle dure 40 minutes par défaut et se fait en binôme.

## Fonctionnement

Le professeur ouvre une séance et distribue son code. Chaque élève renseigne son prénom, la première lettre de son nom et sa classe. En binôme, les deux identités reçoivent la même note. Une nouvelle copie avec la même identité dans la même séance est refusée ; le professeur peut fournir un nouveau lien de reprise. En cas d’homonymie exacte, utiliser un deuxième prénom ou une précision convenue avec le professeur.

Les réponses sont sauvegardées sur le serveur après chaque choix. Une copie locale temporaire aide à reprendre un envoi interrompu, mais seule la dernière sauvegarde reçue avant l’échéance compte. Les notes sont calculées côté serveur après rendu ou échéance. Les horloges du navigateur ne déterminent pas l’échéance serveur. Le professeur peut ajouter cinq minutes à une copie encore active.

Compétences, chacune sur 5 : 5 = Vert + ; 4 = Vert ; 2–3 = Jaune ; 0–1 = Rouge. Chaque bonne réponse vaut un point ; une erreur ou une absence vaut zéro. Les résultats sont des indicateurs pour ce contrôle, pas une validation globale définitive des compétences du cycle.

L’export CSV UTF-8, séparé par des points-virgules, contient une ligne par élève avec classe, prénom, initiale, note, compétences, statut et référence de copie. Les copies en cours n’ont pas de note finale. Les dates de l’export sont en UTC. Aucun fichier de notes réelles n’existe avant le passage des élèves.

## Déploiement

Conserver le dépôt `steack32/techno`, branche `main`, répertoire racine et commande `npx wrangler deploy`.

`wrangler.jsonc` lance la construction, publie les seuls fichiers publics de `dist/`, et crée la classe Durable Object SQLite `EvaluationStore`. Les copies sont conservées dans son stockage durable et ne sont pas effacées lors d’un redéploiement. Ne pas renommer la classe, sa migration ou l’identifiant logique `college-v1` sans migration des données.

Aucun service Sites ni compte ChatGPT n’est nécessaire pour l’élève ou le professeur.

## Accès et confidentialité

Le mot de passe professeur est remis dans une fiche privée, jamais dans GitHub. Son empreinte et les questions avec réponses sont conservées uniquement dans le stockage privé du serveur. Une initialisation HTTPS unique est effectuée immédiatement après le premier déploiement, avant de distribuer les liens. La route d’installation est ensuite définitivement fermée. Une fenêtre temporelle limite également cette première installation. La première connexion professeur crée les séances prêtes. Le mot de passe et la version déchiffrée ne doivent jamais être ajoutés au dépôt. Les cookies professeur sont HttpOnly et les accès aux copies sont protégés par des jetons aléatoires.

Les fichiers professeur historiques du dépôt ne sont pas copiés sur le site ; leur présence éventuelle dans un dépôt GitHub public n’est pas modifiée.

Les questions et choix sont mélangés. Les variantes existantes de Mission Savon sont conservées. Les bonnes réponses ne sont pas envoyées aux élèves avant la clôture et l’ouverture du corrigé. Un navigateur ordinaire ne peut pas empêcher absolument les échanges entre élèves ou l’utilisation d’un autre appareil. Les sorties d’onglet n’entraînent aucune pénalité automatique.

## Vérifications

`node scripts/build-site.mjs` construit les ressources. `npx wrangler deploy --dry-run` vérifie le déploiement sans publier. Tester dans un environnement local distinct les scores, reprises, export, droits professeur et conservation des réponses. Ne pas publier les identifiants de test ni des notes fictives comme des résultats réels.
