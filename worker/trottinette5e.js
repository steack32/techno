// Banque du contrôle 5e. Fusionnée dans le stockage privé au premier accès
// après déploiement. Les copies déjà enregistrées ne sont pas modifiées.
const q=(prompt,correct,wrong,explanation)=>[[prompt,correct,wrong,explanation]];
export const trottinette5e={
  title:'Choisir une trottinette électrique',
  level:'5e',
  minutes:25,
  mode:'individual',
  scoring:'competencies',
  competencies:[
    'Associer les solutions techniques aux fonctions',
    'Caractériser et choisir un objet selon des critères'
  ],
  competencyOfSkill:[0,0,1,1],
  skills:[
    'Reconnaître les notions du cours',
    'Associer une fonction à une solution',
    'Lire et comparer les critères',
    'Choisir un modèle selon des contraintes'
  ],
  bank:[
    q('La fonction d’usage indique…','à quoi sert l’objet',['le prix de l’objet','sa masse','la couleur de l’objet'],'La fonction d’usage est le service rendu à l’utilisateur : à quoi sert l’objet.'),
    q('Pour une trottinette, « freiner » est…','une fonction technique',['une solution technique','un critère de prix','la fonction d’usage'],'Freiner est une action que l’objet doit assurer. C’est une fonction technique. Le frein à disque est, lui, une solution technique.'),
    q('Un « frein à disque » est…','une solution technique',['une fonction d’usage','une fonction technique','un critère de masse'],'Le frein à disque est un composant choisi pour assurer la fonction technique « freiner ».'),
    q('« Se déplacer » est, pour une trottinette…','sa fonction d’usage',['une solution technique','un critère de prix','une fonction technique'],'Se déplacer est le service rendu par la trottinette. C’est sa fonction d’usage.'),
    q('« Éclairer la route » est…','une fonction technique',['une solution technique','un critère de choix','la fonction d’usage'],'Éclairer la route est une action à assurer. Le phare est la solution technique qui la réalise.'),
    q('Quelle solution technique fait avancer la trottinette ?','Le moteur électrique',['Le phare avant LED','Le plateau','Le prix affiché'],'Faire avancer est une fonction technique. Le moteur électrique est la solution qui la réalise.'),
    q('Quelle solution technique éclaire la route ?','Le phare avant LED',['Le plateau','Le moteur électrique','L’autonomie annoncée'],'Le phare avant LED est la solution technique de la fonction « éclairer la route ».'),
    q('Quelle solution technique supporte l’utilisateur ?','Le plateau',['Le phare avant LED','Le moteur électrique','La masse de 12 kg'],'Le plateau est la solution technique qui permet de supporter l’utilisateur.'),
    q('Le moteur électrique est…','une solution technique',['la fonction d’usage','une fonction technique','un critère de choix'],'Le moteur est le composant qui fait avancer la trottinette. C’est une solution technique.'),
    q('Quelle fonction technique est assurée par le plateau ?','Supporter l’utilisateur',['Faire avancer la trottinette','Éclairer la route','Indiquer le prix'],'Le plateau supporte l’utilisateur. Le moteur fait avancer la trottinette, le phare éclaire la route.'),
    q('Quel modèle a la plus grande autonomie annoncée ?','MOVECITY PRO',['URBI ONE','Les deux ont la même autonomie','Aucun ne dépasse 10 km'],'MOVECITY PRO annonce 35 km. URBI ONE annonce 15 km.'),
    q('Quel modèle est le plus léger ?','URBI ONE',['MOVECITY PRO','Les deux ont la même masse','On ne peut pas comparer les masses'],'URBI ONE pèse 12 kg. MOVECITY PRO pèse 17 kg.'),
    q('Quel modèle est le moins cher ?','URBI ONE',['MOVECITY PRO','Les deux ont le même prix','MOVECITY PRO coûte 23 900 F CFP'],'URBI ONE coûte 23 900 F CFP. MOVECITY PRO coûte 47 900 F CFP.'),
    q('Quel modèle a la plus petite autonomie annoncée ?','URBI ONE',['MOVECITY PRO','Les deux annoncent 35 km','Aucun ne dépasse 10 km'],'15 km est inférieur à 35 km. URBI ONE a la plus petite autonomie annoncée.'),
    q('Quelle est la différence de prix entre les deux modèles ?','24 000 F CFP',['12 000 F CFP','47 900 F CFP','10 000 F CFP'],'47 900 − 23 900 = 24 000. MOVECITY PRO coûte 24 000 F CFP de plus.'),
    q('Les deux modèles ont-ils la même fonction d’usage ?','Oui, ils permettent de se déplacer',['Non, car leur prix diffère','Non, car leur masse diffère','Non, car leur autonomie diffère'],'Le prix, la masse et l’autonomie sont des critères. La fonction d’usage reste la même : se déplacer.'),
    q('Quel modèle respecte un budget de 30 000 F CFP et une autonomie annoncée d’au moins 10 km ?','URBI ONE',['MOVECITY PRO','Les deux','Aucun des deux'],'URBI ONE coûte 23 900 F CFP et annonce 15 km. MOVECITY PRO annonce 35 km, mais coûte 47 900 F CFP.'),
    q('On dispose de 50 000 F CFP et on veut au moins 30 km d’autonomie annoncée. Quel modèle convient ?','MOVECITY PRO',['URBI ONE','Les deux','Aucun des deux'],'MOVECITY PRO coûte 47 900 F CFP et annonce 35 km. URBI ONE reste dans le budget, mais n’annonce que 15 km.'),
    q('Quel modèle est à la fois le plus léger et a une autonomie annoncée d’au moins 30 km ?','Aucun des deux',['URBI ONE','MOVECITY PRO','Les deux'],'URBI ONE est le plus léger, mais n’annonce que 15 km. MOVECITY PRO annonce 35 km, mais n’est pas le plus léger.'),
    q('Pour aller le plus loin avec une seule charge, selon les notices, on choisit…','MOVECITY PRO',['URBI ONE','Les deux, elles annoncent 15 km','Le modèle le plus léger, quelle que soit l’autonomie'],'L’autonomie annoncée la plus grande est 35 km, celle de MOVECITY PRO.')
  ]
};
