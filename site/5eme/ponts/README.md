# Les ponts — carnet interactif de 5e

Cinq séances de 55 minutes, adaptées des fiches élèves Word. Les élèves complètent le carnet en ligne et réalisent les simulations séparément dans Bridge Designer 2016.

- Adresse publique : `/5eme/ponts/`, depuis le catalogue 5e.
- Réponses et progression sauvegardées dans une table dédiée du Durable Object existant, sans modifier les évaluations ou leurs données.
- Code privé de reprise aléatoire de 128 bits ; référence indépendante pour retrouver la copie côté professeur. Aucun nom, prénom ni classe demandé.
- Consultation et suppression authentifiées dans `/professeur/ponts/`, accessibles depuis l’espace professeur existant.
- Transmission d’un état du carnet, puis possibilité de le compléter. Une modification remet le statut « en cours » jusqu’à la prochaine transmission.
- Pas de notation automatique ni de mécanisme d’examen sécurisé. Les questions rédigées, le travail dans Bridge Designer et les deux bilans individuels sont corrigés par le professeur. Les exercices de découverte proposent des vérifications formatives.
- Sauvegarde JSON exportable/importable, impression des réponses et cache temporaire par onglet. En cas d’échec réseau, le statut signale clairement que le serveur n’a pas enregistré. Les révisions préviennent l’écrasement depuis deux postes.
- Les coups de pouce affichent des consignes complémentaires ; les réponses restent conservées lors du changement.

Le premier schéma de la séance 1 est l’image de pont à haubans fournie par le professeur. Les sept autres schémas proviennent de la séquence pédagogique. Les cinq photographies sont reproduites sans recadrage, redimensionnées et encodées en WebP ; auteurs, sources Wikimedia Commons et licences sont affichés sous chaque photographie dans `content.js`.

Vérification serveur : `node tests/ponts.test.mjs`. Construction : `node scripts/build-site.mjs`.
