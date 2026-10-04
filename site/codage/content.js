import {choice as c,numeric as n} from '../objective.js';
const yes=(label,answer,explanation)=>c(label,answer?'Vrai':'Faux',[answer?'Faux':'Vrai'],explanation);
const num=(label,value,why)=>n(label,value,why);
export const courses={
'4eme':{title:'Des bits aux images',intro:'Comment une machine représente-t-elle un nombre, un message et une image ?',sessions:[
{title:'Compter avec des interrupteurs',goal:'Composer et lire des nombres binaires simples ; distinguer bit et octet.',timing:'Découverte 5 min · Atelier 20 min · Exercices 20 min · Bilan 10 min',context:'Un afficheur de casier reçoit un numéro sous forme de bits. Ta mission : préparer les bons interrupteurs pour afficher le numéro demandé.',lesson:'Un bit prend la valeur 0 ou 1. Dans un nombre binaire, chaque position a une valeur : de droite à gauche, 1, 2, 4, 8, 16, 32, 64, 128. On additionne uniquement les valeurs des positions à 1. Exemple : 00000101₂ = 4 + 1 = 5. Un octet contient 8 bits.',lab:{type:'bits',targets:[3,10,13],width:4},questions:[
c('Quels symboles utilise le système binaire ?','0 et 1',['1 et 2','Les chiffres de 0 à 9'],'Le binaire utilise deux chiffres : 0 et 1.'),
num('Combien de bits contient un octet ?',8,'Un octet est un groupe de 8 bits.'),
...[6,9,12].map(v=>num(`Quelle est la valeur décimale de ${v.toString(2).padStart(4,'0')}₂ ?`,v,'Additionne les poids des bits à 1 : '+[8,4,2,1].filter(p=>v&p).join(' + ')+` = ${v}.`)),
c('Quel code représente 7 sur 4 bits ?','0111',['1001','1110'],'4 + 2 + 1 = 7.'),
num('Quelle est la plus grande valeur sur 4 bits, pour un entier naturel ?',15,'1111₂ = 8 + 4 + 2 + 1 = 15.'),
yes('Le code 0000 représente le nombre zéro.',true,'Tous les poids sont multipliés par zéro.'),
c('Pour passer de 0011₂ à 0100₂, le nombre…','Augmente de 1',['Double','Diminue de 1'],'0011₂ vaut 3 et 0100₂ vaut 4.'),
num('Bilan : combien de bits faut-il pour 3 octets ?',24,'3 × 8 = 24 bits.')],summary:['Un bit vaut 0 ou 1 ; un octet contient 8 bits.','Pour lire un entier binaire, additionner les poids des positions à 1.','Sur 4 bits, on représente 16 entiers naturels : de 0 à 15.']},
{title:'Envoyer un message en bits',goal:'Utiliser une table de caractères et calculer la taille d’un message dans un codage donné.',timing:'Rappel 5 min · Atelier 20 min · Exercices 20 min · Bilan 10 min',context:'Un panneau lumineux reçoit des codes numériques. Il doit afficher exactement le message envoyé, y compris les espaces.',lesson:'Une table de codage associe un nombre à un caractère. Dans cet atelier, chaque caractère proposé occupe un octet et utilise un code compatible avec ASCII. Exemple : A → 65 → 01000001. L’espace est aussi un caractère. Ce modèle ne signifie pas que tous les textes réels utilisent un octet par caractère : cela dépend du codage.',lab:{type:'text',messages:['BAC','CODE','A B']},questions:[
num('D’après la table, quel est le code décimal de C ?',67,'A vaut 65, B vaut 66 et C vaut 67.'),
c('Associe le code 01000010 au bon caractère.','B',['A','C'],'01000010₂ = 64 + 2 = 66 : B.'),
c('Que donne la suite de codes 67 – 65 – 66 ?','CAB',['BAC','ABC'],'67 → C ; 65 → A ; 66 → B.'),
num('Dans notre modèle, quelle est la taille de CODE en octets ?',4,'Les quatre caractères occupent chacun un octet.'),
num('Quelle est la taille de CODE en bits ?',32,'4 octets × 8 = 32 bits.'),
num('Combien de caractères contient A B, avec son espace ?',3,'A, espace, B : trois caractères.'),
num('Quelle est la taille de A B en bits dans notre modèle ?',24,'3 caractères × 8 bits = 24 bits.'),
yes('On peut supprimer les espaces sans changer le message.',false,'Les espaces font partie du message.'),
c('Pourquoi faut-il connaître la table de codage ?','Pour interpréter les codes reçus',['Pour augmenter la luminosité','Pour alimenter le panneau'],'Un code ne permet de retrouver un caractère que si sa correspondance est connue.'),
yes('Dans tous les fichiers texte, un caractère occupe toujours un octet.',false,'Le nombre d’octets dépend du codage et du caractère.')],summary:['Une table associe les caractères à des codes numériques.','Dans notre atelier : un caractère = un octet ; les espaces comptent.','Le codage réel doit être connu : tous les caractères ne prennent pas toujours un octet.']},
{title:'Dessiner avec des bits',goal:'Coder une image en noir et blanc et calculer la quantité de données de ses pixels.',timing:'Observation 5 min · Atelier 20 min · Exercices 20 min · Bilan 10 min',context:'Tu prépares un pictogramme pour un petit afficheur. Chaque case est un pixel ; le récepteur lit les lignes de gauche à droite, puis de haut en bas.',lesson:'Dans notre modèle, 0 représente un pixel blanc et 1 un pixel noir. Chaque pixel utilise donc 1 bit. La quantité de données des pixels vaut largeur × hauteur × bits par pixel. On ignore ici les en-têtes et la compression : la taille d’un fichier réel peut être différente.',lab:{type:'pixels',patterns:['00111100','01000010','10100101','10000001','10100101','10011001','01000010','00111100']},questions:[
c('Dans notre convention, que représente un 1 ?','Un pixel noir',['Un pixel blanc','Une ligne entière'],'Chaque bit décrit un pixel : 1 noir, 0 blanc.'),
num('Combien de pixels contient une image de 8 × 8 ?',64,'8 lignes × 8 colonnes = 64 pixels.'),
num('À 1 bit par pixel, combien de bits faut-il pour 8 × 8 pixels ?',64,'64 pixels × 1 bit = 64 bits.'),
num('Combien cela représente-t-il d’octets ?',8,'64 ÷ 8 = 8 octets, uniquement pour les pixels.'),
num('Combien de pixels noirs contient la ligne 10110010 ?',4,'Il y a quatre bits à 1.'),
num('À 1 bit par pixel, combien d’octets faut-il pour 16 × 8 pixels ?',16,'16 × 8 = 128 bits ; 128 ÷ 8 = 16 octets.'),
c('Si on double la largeur et la hauteur, le nombre de pixels est…','Multiplié par 4',['Multiplié par 2','Inchangé'],'Deux fois plus de colonnes et deux fois plus de lignes : 2 × 2 = 4.'),
yes('Une image de 64 pixels utilise forcément 64 octets.',false,'Dans ce modèle, un pixel occupe un bit, donc 64 pixels occupent 8 octets.'),
c('Pourquoi préciser l’ordre de lecture des pixels ?','Pour reconstruire la même image',['Pour rendre le fichier secret','Pour économiser automatiquement des bits'],'Émetteur et récepteur doivent utiliser la même convention.'),
num('Défi final : combien d’octets pour une image de 16 × 16 à 1 bit par pixel ?',32,'16 × 16 = 256 bits ; 256 ÷ 8 = 32 octets.')],summary:['Un pixel est un élément de l’image. À 1 bit par pixel, deux valeurs sont possibles.','Données des pixels = largeur × hauteur × bits par pixel.','Pour passer des bits aux octets, diviser par 8 ; ce calcul ignore en-têtes et compression.']}
]},
'3eme':{title:'Coder, transmettre, afficher',intro:'Comment choisir un codage adapté à un objet connecté et à son affichage ?',sessions:[
{title:'Combien d’informations avec des bits ?',goal:'Choisir un nombre de bits adapté ; distinguer un état logique et une mesure.',timing:'Rappel 5 min · Atelier 20 min · Défis 20 min · Bilan 10 min',context:'Une station connectée envoie des états de capteurs et des nombres entiers. Il faut prévoir assez de codes pour toutes les valeurs possibles.',lesson:'Un booléen possède deux valeurs : vrai ou faux. Il peut être représenté par un bit. Pour lire un entier binaire, additionne les poids des bits à 1 : 128, 64, 32, 16, 8, 4, 2, 1. Exemple : 00001010₂ = 8 + 2 = 10. Avec n bits, on dispose de 2ⁿ combinaisons. Pour des entiers naturels codés à partir de zéro, les valeurs vont de 0 à 2ⁿ − 1. Ainsi, 8 bits donnent 256 valeurs de 0 à 255. Ici, nous n’étudions ni nombres négatifs ni nombres à virgule.',lab:{type:'bits',targets:[42,165,255],width:8},questions:[
c('Associe « porte ouverte : vrai/faux » au bon type.','Booléen',['Nombre entier','Image'],'Cette information ne possède que deux états possibles.'),
c('Associe « nombre de passages : 37 » au bon type.','Nombre entier',['Booléen','Caractère'],'Un comptage donne un nombre entier.'),
num('Combien de combinaisons peut-on former avec 3 bits ?',8,'2 × 2 × 2 = 8 combinaisons.'),
num('Quelle est la plus grande valeur entière naturelle sur 8 bits ?',255,'256 valeurs, à partir de zéro : de 0 à 255.'),
num('Quelle est la valeur de 10100101₂ ?',165,'128 + 32 + 4 + 1 = 165.'),
num('Nombre minimal de bits pour représenter 12 états différents ?',4,'3 bits donnent 8 codes, insuffisants ; 4 bits en donnent 16.'),
num('Nombre minimal de bits pour coder tous les entiers de 0 à 100 inclus ?',7,'Il faut 101 codes. 6 bits : 64 codes ; 7 bits : 128 codes.'),
yes('Un octet suffit pour coder les 300 entiers de 0 à 299.',false,'Un octet ne donne que 256 combinaisons.'),
num('Nombre minimal de bits pour ces 300 valeurs ?',9,'8 bits : 256 codes ; 9 bits : 512 codes.'),
c('Un capteur doit transmettre 256 avec un seul octet non signé. Que faut-il faire ?','Adapter le format pour disposer de plus de bits',['Envoyer 255 en prétendant que c’est exact','Supprimer un chiffre'],'256 dépasse le maximum 255 ; le format doit permettre de représenter la valeur.')],summary:['n bits donnent 2ⁿ combinaisons.','Un entier naturel non signé sur 8 bits va de 0 à 255.','Choisir un codage exige de compter tous les états ou toutes les valeurs possibles.']},
{title:'Construire et transmettre une trame',goal:'Lire un format de message et calculer une taille et une durée de transmission.',timing:'Découverte 5 min · Atelier 20 min · Calculs 20 min · Bilan 10 min',context:'Une station météo scolaire transmet une petite trame. Pour cet exercice, elle envoie toujours quatre octets dans le même ordre : lettre S, identifiant de station, température entière de 0 à 50 °C, humidité entière de 0 à 100 %.',lesson:'Le récepteur doit connaître le format : le même octet peut représenter un caractère ou une mesure selon sa position. Notre trame pédagogique contient 4 octets, soit 32 bits. Durée de transmission = nombre de bits ÷ débit en bits par seconde. Les calculs ignorent les informations supplémentaires des protocoles et les délais du réseau.',lab:{type:'frame'},questions:[
c('Que signifie le premier octet 01010011 dans ce format ?','Le caractère S',['La température 83 °C','L’humidité 83 %'],'Le format impose une lettre S au début ; son code décimal est 83.'),
num('Décode l’identifiant 00001100₂.',12,'8 + 4 = 12.'),
num('Décode la température 00011001₂, en °C.',25,'16 + 8 + 1 = 25 °C.'),
num('Décode l’humidité 00111100₂, en %.',60,'32 + 16 + 8 + 4 = 60 %.'),
num('Combien de bits contient une trame de 4 octets ?',32,'4 × 8 = 32 bits.'),
num('Combien d’octets pour 30 trames ?',120,'30 × 4 = 120 octets.'),
num('À 16 bits/s, combien de secondes pour une trame ?',2,'32 ÷ 16 = 2 secondes dans notre modèle.'),
num('À 64 bits/s, combien de secondes pour une trame ?',0.5,'32 ÷ 64 = 0,5 seconde.'),
c('Une température de −5 °C doit être envoyée. Notre format convient-il ?','Non, il faut définir un codage adapté',['Oui, sans modifier la convention','Oui, en supprimant le signe'],'La convention donnée ne prévoit que les températures entières de 0 à 50 °C.'),
c('Coder une donnée en binaire la rend-il secrète ?','Non, ce n’est pas un chiffrement',['Oui, seuls les ordinateurs peuvent la lire','Oui, quel que soit le code'],'Le codage représente l’information. Le chiffrement vise à la protéger contre une lecture non autorisée.')],summary:['Une trame respecte une organisation connue de l’émetteur et du récepteur.','Taille en bits = nombre d’octets × 8. Durée = bits ÷ débit en bits/s.','Représenter une information en binaire ne la chiffre pas.']},
{title:'Des couleurs aux codes hexadécimaux',goal:'Manipuler les composantes RVB et comprendre l’intérêt de l’hexadécimal.',timing:'Observation 5 min · Atelier 20 min · Défis 20 min · Bilan 10 min',context:'Tu règles les couleurs d’un afficheur. Chaque pixel utilise trois composantes : rouge, vert et bleu, chacune codée sur 8 bits.',lesson:'Dans ce modèle RVB, chaque composante va de 0 à 255. Un pixel utilise donc 24 bits, soit 3 octets. L’hexadécimal est une écriture en base 16 utilisant 0 à 9 puis A à F (10 à 15). Un chiffre hexadécimal représente 4 bits ; deux représentent un octet. FF₁₆ = 255. Dans #RRGGBB, les paires indiquent rouge, vert, bleu. Cette découverte est un prolongement ; l’octal n’est pas nécessaire ici.',lab:{type:'rgb',targets:[[255,0,0],[0,255,255],[128,128,128]]},questions:[
num('Combien d’octets pour un pixel RVB de 24 bits ?',3,'24 ÷ 8 = 3 octets.'),
c('Associe #0000FF à sa couleur.','Bleu',['Rouge','Vert'],'Rouge = 0, vert = 0, bleu = 255.'),
c('Associe #FFFFFF à sa couleur.','Blanc',['Noir','Rouge'],'Les trois composantes sont au maximum.'),
c('Associe #000000 à sa couleur.','Noir',['Blanc','Jaune'],'Les trois composantes sont nulles.'),
num('Quelle est la valeur décimale du chiffre hexadécimal A ?',10,'Après 9 viennent A = 10, B = 11, …, F = 15.'),
num('Combien de bits représente un chiffre hexadécimal ?',4,'4 bits offrent 16 combinaisons, comme les 16 chiffres hexadécimaux.'),
num('Avec la méthode 1 × 16 + 0, quelle est la valeur décimale de 10₁₆ ?',16,'La position de gauche représente les groupes de 16.'),
num('Combien d’octets pour les pixels d’une image RVB de 20 × 10 ?',600,'20 × 10 × 3 = 600 octets, sans en-tête ni compression.'),
num('Pour 8 × 8 pixels, combien de fois plus de données en RVB 24 bits qu’en noir et blanc 1 bit ?',24,'Le nombre de pixels est identique ; chaque pixel utilise 24 fois plus de bits.'),
c('L’hexadécimal permet-il, à lui seul, de compresser les données binaires ?','Non, il représente les mêmes valeurs plus lisiblement',['Oui, il supprime des informations','Oui, il divise automatiquement le fichier par quatre'],'Une notation plus courte pour nous ne constitue pas une compression des données.')],summary:['En RVB sur 24 bits : 3 composantes de 0 à 255, soit 3 octets par pixel.','Un chiffre hexadécimal correspond à 4 bits ; FF₁₆ = 255.','#RRGGBB indique rouge, vert, bleu. Une notation hexadécimale ne compresse pas les données.']}
]}};
