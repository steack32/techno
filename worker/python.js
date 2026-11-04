// Py-rates.org levels A–E (1–5), verified against its GameManager and language help.
// Curriculum: https://www.education.gouv.fr/sites/default/files/ensel802_annexe.pdf
const q=(prompt,correct,wrong,explanation)=>[[prompt,correct,wrong,explanation]];
const common={version:'python-v3-reasoning',title:'Python · Py-rates · Niveaux 1 à 5',minutes:20,mode:'individual',pointsPerQuestion:2,masteryLabels:true,requireClass:true,
 competencies:['Comprendre et modifier un programme associé à une fonctionnalité d’un objet ou d’un système technique','Concevoir, écrire, tester et mettre au point un programme'],
 competencyOfSkill:[0,1],skills:['Lire et comprendre un programme','Compléter et corriger un programme'],bank:[
 q("Le pirate est orienté vers la droite →. Dans quelle direction est-il orienté à la fin ?\n\navancer()\ngauche()\navancer()\ndroite()\navancer()","Vers la droite →",["Vers le haut ↑", "Vers la gauche ←", "Vers le bas ↓"],"Il tourne à gauche, puis à droite. Les déplacements ne changent pas son orientation."),
 q('Combien de fois avancer() est-elle exécutée ?\n\nfor _ in range(3):\n    avancer()\navancer()', '4 fois',['3 fois','2 fois','6 fois'],'Trois appels sont dans la boucle ; le dernier, sans indentation, est exécuté une fois après la boucle.'),
 q("La bouteille contient le nombre 3. Quelles hauteurs sont utilisées pour les deux sauts, dans l’ordre ?\n\nhauteur = lire_nombre()\nsauter_hauteur(hauteur)\nhauteur = 1\nsauter_hauteur(hauteur)","3 puis 1",["3 puis 3", "1 puis 1", "1 puis 3"],"La variable hauteur contient d’abord 3, puis sa valeur est remplacée par 1."),
 q("Quelles instructions de déplacement sont exécutées, dans l’ordre ?\n\ndirection = \"dro\"\nif direction == \"gau\":\n    gauche()\nelse:\n    droite()\navancer()","droite() puis avancer()",["gauche() puis avancer()", "droite() uniquement", "gauche(), puis droite(), puis avancer()"],"Le programme exécute le bloc else, puis avancer(), qui est en dehors de la condition."),
 q('mesurer_hauteur() renvoie 2. Quelle instruction est exécutée ?\n\nhauteur = mesurer_hauteur()\nif hauteur == 0:\n    avancer()\nelif hauteur == 1:\n    sauter()\nelse:\n    sauter_haut()', 'sauter_haut()',['avancer()','sauter()','sauter() puis sauter_haut()'],'Les deux comparaisons sont fausses. Le programme exécute la branche else.'),
 q('On veut avancer exactement 5 fois. Quelle ligne remplace les pointillés ?\n\n...\n    avancer()', 'for _ in range(5):',['for _ in range(4):','if _ == 5:','for _ in range(5)'],'range(5) provoque cinq répétitions. Les deux-points sont nécessaires.'),
 q('On veut répéter trois fois : avancer puis sauter. Quel programme convient ?', 'for _ in range(3):\n    avancer()\n    sauter()',['for _ in range(3):\n    avancer()\nsauter()','for _ in range(3):\n    sauter()\n    avancer()','for _ in range(2):\n    avancer()\n    sauter()'],'Les deux instructions doivent être indentées dans la boucle, dans l’ordre avancer() puis sauter().'),
 q('La hauteur des obstacles change. On veut sauter à la hauteur indiquée par la bouteille. Quelle instruction remplace les pointillés ?\n\nhauteur = lire_nombre()\n...', 'sauter_hauteur(hauteur)',['sauter_hauteur(1)','sauter_hauteur("hauteur")','hauteur = sauter_hauteur()'],'Il faut utiliser la valeur de la variable hauteur, sans guillemets, comme argument.'),
 q('Quelle ligne corrige le test ci-dessous ?\n\nif direction = "gau":\n    gauche()', 'if direction == "gau":',['if direction = "gau"','if direction == gau:','else direction == "gau":'],'== compare deux valeurs ; = sert à affecter une valeur. La chaîne de caractères reste entre guillemets.'),
 q('Le pirate doit avancer pour une hauteur de 0, sauter pour 1, sauter haut sinon. Quelle ligne remplace les pointillés ?\n\nhauteur = mesurer_hauteur()\nif hauteur == 0:\n    avancer()\n...\n    sauter()\nelse:\n    sauter_haut()', 'elif hauteur == 1:',['else hauteur == 1:','elif hauteur == 0:','elif hauteur = 1:'],'elif ajoute un deuxième test. Pour la hauteur 1, sauter() sera exécutée ; pour 2, ce sera sauter_haut().')
]};
export const python4e={...common,level:'4e',scoring:'competencies'};
export const python3e={...common,level:'3e',scoring:'points'};

// Keep saved attempts readable without changing question/choice IDs or grades.
export const pythonLoopNotation=text=>text.replaceAll("for i in range(","for _ in range(").replaceAll("if i == 5:","if _ == 5:");
