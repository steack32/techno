// 20 questions, five topics, one point each. Illustrations contain no answer labels.
const q=(prompt,correct,wrong,explanation,media)=>[[prompt,correct,wrong,explanation,media]];
const image=(n,alt,caption='')=>({image:{src:`/evaluations/ponts/figure-${n}.svg`,alt,caption}});
const photos=[{"src": "/evaluations/ponts/photo-1.webp", "alt": "Deux tabliers horizontaux reposent sur des piles successives.", "width": 1000, "height": 667, "caption": "Photo : Glenn (glennaa) · CC BY 2.0", "credit": 1}, {"src": "/evaluations/ponts/photo-2.webp", "alt": "Un pont en pierre avec de grandes formes courbes sous le tablier.", "width": 1000, "height": 750, "caption": "Photo : Gio 2000 · CC BY-SA 3.0", "credit": 2}, {"src": "/evaluations/ponts/photo-3.webp", "alt": "Des câbles inclinés relient le tablier au pylône.", "width": 776, "height": 800, "caption": "Photo : Roger Wollstadt · CC BY-SA 2.0", "credit": 3}, {"src": "/evaluations/ponts/photo-4.webp", "alt": "Des suspentes verticales relient le tablier aux grands câbles qui passent sur les pylônes.", "width": 1000, "height": 625, "caption": "Photo : Frank Schulenburg · CC BY-SA 4.0", "credit": 4}];
const photo=n=>({image:photos[n-1]});
export const ponts5e={
 version:'ponts5e-v2',title:'Les ponts · QCM',level:'5e',minutes:25,mode:'individual',requireClass:true,
 scoring:'points',pointsPerQuestion:1,questionsPerSkill:4,masteryLabels:true,
 // Indicators for this assessment, not claims of full curriculum competency validation.
 competencies:['Identifier les éléments, les familles et les efforts d’un pont','Expliquer la stabilité et interpréter les essais d’un pont'],
 competencyOfQuestion:Array.from({length:20},(_,i)=>i<10?0:1),
 skills:['Vocabulaire','Familles de ponts','Efforts et déformations','Stabiliser les barres','Bridge Designer'],
 bank:[
 q('Quelle partie du pont porte la voie de circulation ?','Le tablier',['Le pylône','La pile','Le hauban'],'Le tablier porte la voie sur laquelle circulent les usagers.'),
 q('Quelle est la différence entre une pile et une culée ?','La pile est un appui intermédiaire ; la culée est un appui à une extrémité.', ['La pile est un appui à une extrémité ; la culée est un appui intermédiaire.','La pile est un câble ; la culée est une barre.','La pile porte la chaussée ; la culée est un garde-corps.'],'Une pile soutient le pont entre ses extrémités. Les culées sont les appuis aux extrémités.'),
 q('À quoi correspond la portée ?','À la distance entre deux appuis consécutifs.',['À la hauteur du tablier au-dessus de l’eau.','À la largeur de la voie de circulation.','À la masse maximale autorisée sur le pont.'],'La portée se mesure entre deux appuis consécutifs. Ce n’est pas forcément la longueur totale du pont.'),
 q('Quel est le rôle des fondations ?','Transmettre les efforts de l’ouvrage au sol.',['Relier les pylônes au tablier.','Protéger les véhicules sur les côtés du tablier.','Constituer la surface de circulation.'],'Les fondations transmettent au sol les efforts reçus par les appuis.'),
 q('À quelle famille appartient le pont sur cette photo ?','Pont à poutres',['Pont en arc','Pont à haubans','Pont suspendu'],'Les poutres portent le tablier et reposent sur les appuis.',photo(1)),
 q('À quelle famille appartient le pont sur cette photo ?','Pont en arc',['Pont à poutres','Pont à haubans','Pont suspendu'],'La structure porteuse courbe sous le tablier est un arc.',photo(2)),
 q('À quelle famille appartient le pont sur cette photo ?','Pont à haubans',['Pont à poutres','Pont en arc','Pont suspendu'],'Les câbles inclinés relient directement le tablier aux pylônes.',photo(3)),
 q('À quelle famille appartient le pont sur cette photo ?','Pont suspendu',['Pont à poutres','Pont en arc','Pont à haubans'],'Le tablier est relié aux grands câbles principaux par des suspentes verticales.',photo(4)),
 q('Les flèches montrent les actions exercées sur la barre. À quel effort est-elle soumise ?','La traction',['La compression','La flexion','La torsion'],'Les actions tirent sur les extrémités de la barre : elle est en traction.',image(5,'Deux flèches tirent sur les extrémités de la barre en s’éloignant l’une de l’autre.')),
 q('Les flèches montrent les actions exercées sur la barre. À quel effort est-elle soumise ?','La compression',['La traction','La flexion','La torsion'],'Les actions poussent sur les extrémités de la barre : elle est en compression.',image(6,'Deux flèches poussent les extrémités de la barre l’une vers l’autre.')),
 q('La poutre se courbe sous la charge. Comment appelle-t-on cette déformation ?','La flexion',['La traction','La torsion','La dilatation'],'La charge fait fléchir la poutre entre ses deux appuis.',image(7,'Une poutre repose sur deux appuis. Une charge au milieu la fait se courber vers le bas.','Pointillés : forme initiale. Déformation exagérée.')),
 q('Quand un camion passe sur un pont, que doit supporter la structure ?', 'Son propre poids et le poids du camion.', ['Seulement son propre poids.','Seulement le poids du camion.','Aucun poids tant que le camion avance.'], 'La structure supporte son propre poids et les charges qui s’y ajoutent, comme les véhicules.'),
 q('Le bas du cadre est maintenu. Les assemblages peuvent pivoter. Que peut-il se passer quand on pousse en haut ?','Le rectangle peut se déformer en parallélogramme.',['Le cadre reste forcément indéformable.','Une barre doit forcément casser pour que la forme change.','Le cadre se transforme en triangle sans déplacer les assemblages.'],'Sans diagonale, les angles du cadre articulé peuvent changer sans que les barres changent de longueur.',image(9,'Cadre rectangulaire articulé sans diagonale, maintenu en bas et poussé horizontalement en haut.','On suppose les barres rigides et les assemblages articulés.')),
 q('Ce cadre possède une diagonale. Pourquoi est-il plus stable ?','La diagonale forme deux triangles qui empêchent le cadre de se déformer.',['La diagonale supprime le poids du cadre.','La diagonale augmente l’épaisseur des autres barres.','La diagonale supprime les forces exercées sur le cadre.'],'La triangulation bloque le changement de forme du cadre articulé. En réalité, les barres doivent aussi résister aux efforts.',image(10,'Cadre rectangulaire maintenu en bas, avec une barre diagonale entre deux coins opposés.','On suppose les barres rigides et les assemblages articulés.')),
 q('Comment appelle-t-on une structure de barres assemblées en triangles ?','Un treillis',['Une fondation','Une culée','Un tablier'],'Un treillis est une structure de barres assemblées, généralement triangulée.'),
 q('Un pont triangulé peut-il supporter n’importe quelle charge ?','Non, les barres peuvent se déformer ou casser si la charge est trop élevée.',['Oui, les triangles suppriment les efforts dans les barres.','Oui, toutes les barres ont alors la même résistance.','Non, une structure triangulée est toujours instable.'],'La triangulation stabilise la forme, mais la résistance dépend aussi du matériau et des dimensions des barres.'),
 q('Pendant l’animation de Bridge Designer, une barre est rouge. Que signifie cette couleur ?','La barre est en compression.',['La barre est forcément cassée.','La barre est en traction.','La barre ne supporte aucun effort.'],'Pendant l’animation, rouge indique la compression et bleu la traction. Une barre rouge n’est pas forcément cassée.'),
 q('Une barre casse pendant le passage du camion. Quelle démarche faut-il suivre ?','Repérer le problème, modifier le pont, puis refaire le test.',['Supprimer la barre sans refaire de test.','Augmenter toutes les dimensions sans refaire de test.','Conserver le pont puisqu’il tenait avant le passage du camion.'],'Il faut observer le problème, modifier la barre ou la structure, puis vérifier l’effet de la modification par un nouveau test.'),
 q('Tu veux tester l’effet de la taille d’une seule barre. Comment comparer les deux essais ?','Modifier uniquement sa taille et conserver les mêmes conditions de test.',['Modifier aussi le matériau et la position de toutes les barres.','Changer les appuis et le chargement à chaque essai.','Comparer seulement l’apparence des deux ponts.'],'Changer un seul paramètre permet d’identifier son effet. Les appuis, le tablier et le chargement restent identiques.'),
 q('Les trois ponts ont été testés dans les mêmes conditions. Lequel réussit le test au coût le plus bas ?','Le pont C',['Le pont A','Le pont B','Les trois ponts'],'C est le moins cher des ponts qui réussissent. B coûte moins cher, mais échoue au test.',{table:{headers:['Pont','Coût','Test'],rows:[['A','225 000 $','Réussi'],['B','170 000 $','Échoué'],['C','195 000 $','Réussi']]}})
 ]
};

// Separate assessment: two questions per topic, two or three choices, two points each.
export const ponts5eAdapte={
 version:'ponts5e-adapte-v1',title:'Les ponts · Parcours adapté',level:'5e',minutes:25,mode:'individual',requireClass:true,
 scoring:'points',pointsPerQuestion:2,questionsPerSkill:2,masteryLabels:true,
 competencies:ponts5e.competencies,
 competencyOfQuestion:Array.from({length:10},(_,i)=>i<5?0:1),
 skills:ponts5e.skills,
 bank:[
 q('À quoi sert un pont ?','À franchir un obstacle.',['À stocker de l’eau.','À produire de l’électricité.'],'Un pont permet de franchir un obstacle, par exemple une rivière ou une route.'),
 q('Sur quelle partie du pont roulent les véhicules ?','Le tablier',['La pile','Le pylône'],'Le tablier porte la voie de circulation.'),
 q('Quelle est la famille du pont sur cette photo ?','Pont en arc',['Pont suspendu'],'Les grandes formes courbes sous le tablier sont des arcs.',photo(2)),
 q('Quelle est la famille du pont sur cette photo ?','Pont suspendu',['Pont à poutres'],'Des suspentes verticales relient le tablier aux grands câbles.',photo(4)),
 q('On tire sur les deux extrémités de la barre. Quel est l’effort ?','La traction',['La compression'],'Tirer sur une barre la met en traction.',image(5,'Deux flèches tirent sur les extrémités de la barre.')),
 q('On pousse sur les deux extrémités de la barre. Quel est l’effort ?','La compression',['La traction'],'Pousser sur une barre la met en compression.',image(6,'Deux flèches poussent sur les extrémités de la barre.')),
 q('Quelle forme utilise-t-on pour stabiliser un assemblage de barres ?','Le triangle',['Le rectangle sans diagonale'],'Le triangle conserve sa forme si les barres restent rigides.'),
 q('Pourquoi ajoute-t-on la barre en diagonale dans ce cadre ?','Pour empêcher le cadre de se déformer.',['Pour supprimer le poids du cadre.','Pour décorer le cadre.'],'La diagonale forme deux triangles et stabilise le cadre.',image(10,'Un cadre rectangulaire avec une barre en diagonale.')),
 q('Dans Bridge Designer, à quoi sert le test avec le camion ?','À vérifier si le pont résiste à son passage.',['À changer la couleur du pont.','À enregistrer le fichier.'],'Le test simule le passage du camion pour vérifier la résistance du pont.'),
 q('Le pont s’effondre pendant le test. Que faut-il faire ?','Modifier le pont, puis refaire le test.',['Garder le pont sans le modifier.'],'Il faut améliorer le pont et vérifier le résultat avec un nouveau test.')
 ]
};
