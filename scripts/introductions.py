"""Mini-cours, traces écrites et dessins vectoriels originaux.

Les pages AVANT précèdent l'activité ; les pages APRÈS sont distribuées à la correction.
"""
from math import atan2, cos, sin
from html import escape
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Flowable, Paragraph, PageBreak, Spacer

INK=colors.HexColor('#172b43'); BLUE=colors.HexColor('#175b9a')
ORANGE=colors.HexColor('#a6520b'); PALE=colors.HexColor('#eef3f8')

INTRO={
'5e': {
 'title': 'Comprendre un objet technique',
 'hook': 'Pourquoi un cartable possède-t-il des bretelles, une poignée et une fermeture ?',
 'before': [
  [('p','Un objet technique est conçu et fabriqué par des êtres humains pour répondre à un besoin. Pour l’étudier, on précise son usage et on observe les choix de conception.'),
   ('diagram','bag'),
   ('table',(['Mot à connaître','Exemple du cartable'],[
    ['Besoin : une nécessité ou une attente.','Transporter ses affaires scolaires.'],
    ['Fonction d’usage : le service rendu par l’objet.','Permettre à un élève de transporter ses affaires. On utilise un verbe à l’infinitif.'],
    ['Composant : une pièce ou un élément de l’objet.','La bretelle permet de porter le cartable sur l’épaule.'],
    ['Matériau : la matière d’un composant.','La bretelle de notre modèle est en tissu de polyester.'],
    ['Contrainte : une exigence à respecter.','Supporter la charge, être confortable et limiter la masse.']
   ])),
   ('h','Vérification orale'),
   ('p','1. « Bretelle » : composant ou matériau ? 2. À quoi sert le cartable ? 3. Une grande poche peut-elle aussi avoir un inconvénient ?')]
 ],
 'after': [
  ('h','La trace écrite à conserver'),
  ('p','Un objet technique répond à un besoin. Sa fonction d’usage indique le service qu’il rend ; elle se formule avec un verbe à l’infinitif. L’objet est constitué de composants qui ont chacun un rôle. Ces composants sont fabriqués dans des matériaux. Les choix de conception doivent respecter des contraintes, par exemple la résistance, la sécurité, la masse ou le coût.'),
  ('p','Une amélioration doit être justifiée par l’attente d’un utilisateur. Elle peut présenter un inconvénient : augmenter la capacité d’un cartable peut aussi augmenter son encombrement.'),
  ('diagram','bag'),
  ('h','La méthode à réutiliser'),
  ('p','Identifier l’utilisateur et son besoin ; écrire la fonction d’usage ; associer chaque composant à son rôle et à son matériau ; repérer une contrainte ; proposer puis justifier une amélioration.'),
  ('h','Exemple de phrase précise'),
  ('p','« La bretelle sert à porter le cartable. Dans ce modèle, elle est en tissu de polyester. L’élargir peut mieux répartir l’appui sur l’épaule, mais rend le cartable plus encombrant. »'),
  ('p','À retenir : « bretelle » désigne un élément ; « polyester » désigne sa matière. Les matériaux varient selon les modèles.')
 ],
 'script': [
  ('0-5 min | Accroche','Afficher ou faire ouvrir le dessin du cartable. Demander : « Pourquoi toutes ces pièces ? » Prendre deux réponses et les reformuler avec un verbe : porter, fermer, contenir. Annoncer : « Vous allez expliquer comment un objet répond au besoin d’un utilisateur. »'),
  ('5-8 min | Besoin et fonction','Dire : « Le besoin est de transporter des affaires. Le cartable rend ce service : permettre à un élève de les transporter. Sa fonction ne se résume pas à sa couleur ou à sa marque. Plusieurs objets peuvent répondre à un même besoin. »'),
  ('8-10 min | Composant et matériau','Pointer une bretelle : « Voici un composant. Dans notre modèle, il est fabriqué en tissu de polyester : c’est le matériau. La bretelle est la pièce ; le polyester est sa matière. » Faire répondre : « La poignée, pièce ou matière ? » Réponse : pièce.'),
  ('10-12 min | Contrainte et contrôle','Dire : « Le cartable doit supporter la charge tout en restant transportable. Une poche supplémentaire augmente la capacité mais peut augmenter l’encombrement. » Réponses aux questions orales : composant ; transporter les affaires ; encombrement ou masse possible. Transition : « Appliquez cette méthode à l’un des trois objets de la fiche. »')
 ],
 'activity': '12-16 : choisir l’objet, lire sa fiche et traiter Q1-Q2. 16-26 : compléter Q3 sur trois composants. 26-37 : traiter Q4-Q5. En binôme, changer de pilote vers 24 minutes. Le défi reste facultatif.',
 'correction': '37-41 : faire expliquer une association composant / rôle / matériau. 41-45 : comparer deux améliorations et leurs limites. 45-47 : compléter la synthèse de l’activité. Ne pas lire les trois corrigés en entier.',
 'trace_use': 'Distribuer la page APRÈS. Faire lire la trace et repérer les cinq mots essentiels. Si les élèves écrivent au clavier, faire produire seulement une phrase associant une pièce, son rôle et son matériau.',
 'priority': 'Conserver Q1 à Q5. Si nécessaire, fournir les amorces et limiter l’amélioration à deux phrases. Ne pas exiger le défi.'
},
'4e': {
 'title': 'Commander avec des conditions',
 'hook': 'Pour autoriser une action, faut-il parfois vérifier plusieurs conditions ?',
 'before': [
  [('p','Un capteur fournit une information sur l’environnement. Le programme traite les informations et commande un actionneur, qui réalise une action grâce à l’énergie reçue.'),
   ('p','Une condition est une affirmation qui peut être vraie ou fausse. Exemple : « le nombre mesuré est inférieur à 30 ». À la valeur 30, cette condition est fausse.'),
   ('diagram','logic'),
   ('table',(['A : badge valide','B : code correct','A ET B','A OU B'],[
    ['Faux','Faux','Faux','Faux'],['Faux','Vrai','Faux','Vrai'],['Vrai','Faux','Faux','Vrai'],['Vrai','Vrai','Vrai','Vrai']
   ])),
   ('h','Écrire une règle complète'),
   ('p','SI la condition est vraie ALORS réaliser l’action SINON réaliser l’autre action. Pour une commande automatique, le programme réévalue régulièrement les informations.'),
   ('h','Vérification orale'),
   ('p','Avec un badge valide et un code incorrect, quelle règle autorise l’accès : ET, OU, les deux ou aucune ?')]
 ],
 'after': [
  ('h','La trace écrite à conserver'),
  ('p','Les capteurs fournissent des informations. Le programme les traite et commande un actionneur. Une condition est vraie ou fausse. Avec ET, les deux conditions doivent être vraies. Avec OU, au moins une condition doit être vraie, y compris lorsque les deux sont vraies. On vérifie un programme avec plusieurs essais, notamment aux valeurs limites.'),
  ('h','La règle corrigée de notre éclairage'),
  ('p','Répéter en continu : SI luminosité < 30 ET présence détectée ALORS allumer la lampe SINON éteindre la lampe.'),
  ('diagram','light_rule'),
  ('table',(['Situation','Résultat et justification'],[
   ['Luminosité 10, personne absente','Éteinte : la condition de présence est fausse.'],
   ['Luminosité 29, personne présente','Allumée : les deux conditions sont vraies.'],
   ['Luminosité 30, personne présente','Éteinte : 30 n’est pas strictement inférieur à 30.'],
   ['Luminosité 80, personne présente','Éteinte : la condition de faible luminosité est fausse.']
  ])),
  ('p','Dans le simulateur, la luminosité est un indice de 0 à 100, pas une mesure en lux. Le modèle ne comporte ni temporisation ni réglage différent pour l’allumage et l’extinction.')
 ],
 'script': [
  ('0-5 min | Accroche','Demander : « Pour entrer dans une salle, peut-on exiger un badge et un code ? Peut-on accepter l’un ou l’autre ? » Faire apparaître deux règles possibles sans encore corriger l’éclairage de l’activité.'),
  ('5-7 min | Information et condition','Dire : « Un capteur fournit une information, le programme la traite, un actionneur agit. Une condition peut être vraie ou fausse. 29 < 30 est vrai ; 30 < 30 est faux. » Le seuil est un nombre choisi pour comparer la mesure.'),
  ('7-10 min | ET et OU','Suivre le dessin puis la table. Dire : « ET exige les deux. OU accepte au moins une condition, et accepte aussi les deux. » Faire examiner badge valide / code incorrect : ET faux, OU vrai. Préciser que badge et code constituent un exemple de logique, pas les capteurs du couloir.'),
  ('10-12 min | Règle complète','Dire : « Écrivons toujours ce qui se passe si la condition est vraie et si elle est fausse : SI… ALORS… SINON… » Demander le résultat de la question orale : OU seulement. Transition : « La règle du couloir contient une erreur. Prouvez-la par un essai, puis corrigez-la. »')
 ],
 'activity': '12-16 : lire le besoin, traiter Q1 et prévoir les essais. 16-24 : tester les cinq cas avec OU et expliquer un contre-exemple en Q3. 24-33 : corriger, cliquer sur Appliquer, refaire les cinq essais, rédiger Q4. 33-37 : traiter Q5 à la valeur 30. Q6 et le défi sont des prolongements si le temps le permet.',
 'correction': '37-41 : faire présenter un essai qui invalide OU. 41-45 : écrire la règle avec ET et justifier le cas 30. 45-47 : compléter la synthèse et, si possible, expliquer oralement Q6 : à 40 avec présence, seuil 30 donne éteinte, seuil 50 donne allumée.',
 'trace_use': 'Distribuer la page APRÈS seulement à la correction. Faire lire la trace et écrire ou dicter la règle corrigée. Revenir au seuil 30 avant le bilan.',
 'priority': 'Q1 à Q5 et les cinq essais avant/après correction sont prioritaires. Q6 est un prolongement ; ne pas raccourcir les essais pour la terminer.'
},
'3e': {
 'title': 'Information et énergie : deux rôles',
 'hook': 'Un détecteur de présence fournit-il l’énergie qui fait briller une lampe ?',
 'before': [
  [('p','Dans un système automatisé, la chaîne d’information acquiert des informations, les traite et communique des ordres. La chaîne d’énergie fournit et transforme l’énergie nécessaire à l’action.'),
   ('diagram','lamp_chains'),
   ('h','Suivre deux trajets différents'),
   ('p','Information : une présence est détectée ; la carte traite cette information ; la liaison transmet un ordre au module de puissance.'),
   ('p','Énergie : le bloc d’alimentation fournit l’énergie électrique ; le module de puissance en autorise le transfert ; la LED la convertit en énergie lumineuse, avec des pertes thermiques.'),
   ('h','Le lien entre les chaînes'),
   ('p','L’ordre arrive au bloc DISTRIBUER. Le détecteur ne fournit pas l’énergie qui éclaire. Le module de puissance reçoit à la fois une commande et l’énergie à distribuer.'),
   ('p','Ce modèle d’éclairage ne sépare pas de fonction TRANSMETTRE après la LED. Toutes les fonctions ne correspondent pas toujours à des composants distincts. Nous étudierons les quatre fonctions sur un système motorisé.'),
   ('h','Vérification orale'),
   ('p','La carte choisit-elle un ordre ou produit-elle la lumière ? La LED fournit-elle principalement une information de présence ou une action d’éclairage ?')],
  [('p','Une fonction décrit ce que fait une partie du système. Un composant est la solution matérielle qui assure cette fonction. On classe les composants selon leur rôle dans le modèle étudié.'),
   ('h','Chaîne d’information : trois fonctions'),
   ('table',(['Fonction','Ce qu’elle réalise'],[
    ['ACQUÉRIR','Recueillir une information de l’environnement ou une demande de l’utilisateur.'],
    ['TRAITER','Appliquer un programme ou une règle pour déterminer la réponse.'],
    ['COMMUNIQUER','Transmettre une information ou un ordre ; dans notre étude, vers la chaîne d’énergie.']
   ])),
   ('h','Chaîne d’énergie : quatre fonctions'),
   ('table',(['Fonction','Ce qu’elle réalise'],[
    ['ALIMENTER','Fournir l’énergie nécessaire sous une forme adaptée.'],
    ['DISTRIBUER','Autoriser, interrompre ou régler le transfert d’énergie selon un ordre.'],
    ['CONVERTIR','Transformer une forme d’énergie en une autre.'],
    ['TRANSMETTRE','Acheminer l’énergie ou le mouvement vers l’élément qui réalise l’action.']
   ])),
   ('h','Deux composants à distinguer'),
   ('p','Un capteur fournit une information : présence, position, température… Un actionneur réalise une action en convertissant l’énergie reçue : par exemple, un moteur transforme l’énergie électrique en énergie mécanique.'),
   ('h','Une erreur à éviter'),
   ('p','Un capteur et une carte électronique ont eux aussi besoin d’énergie. Cela ne les classe pas automatiquement dans la chaîne d’énergie : on considère ici leur rôle d’acquisition ou de traitement de l’information.'),
   ('p','Pour l’activité : utilise ce vocabulaire pour associer les composants du portail à leurs fonctions. Une flèche représente un transfert ; précise s’il s’agit d’une information, d’un ordre ou d’énergie.')]
 ],
 'after': [
  ('h','La trace écrite à conserver'),
  ('p','La chaîne d’information acquiert, traite et communique des informations. Elle envoie un ordre au bloc distribuer de la chaîne d’énergie. La chaîne d’énergie alimente, distribue, convertit et transmet l’énergie pour réaliser l’action. Un capteur fournit une information ; un moteur est un actionneur qui convertit l’énergie électrique en énergie mécanique.'),
  ('diagram','gate'),
  ('p','Dans ce modèle de portail, le moteur produit une rotation. Le pignon et la crémaillère transmettent le mouvement et transforment cette rotation en translation du portail.'),
  ('h','Ce que signifient les flèches'),
  ('p','Bleu : informations et ordre de commande. Orange : transferts d’énergie. L’énergie est électrique jusqu’au moteur, puis mécanique après le moteur. Les pertes ne sont pas représentées.'),
  ('h','À comprendre, au-delà des mots'),
  ('p','La carte appartient à la chaîne d’information par son rôle de traitement, même si elle est alimentée électriquement. Si le moteur tourne mais que le pignon n’engrène plus avec la crémaillère, la fonction transmettre est défaillante.'),
  ('p','Le schéma décrit le modèle simplifié de l’activité : fermeture seulement, bouton maintenu, aucun obstacle et portail non déjà fermé. Il ne constitue pas un schéma de câblage.')
 ],
 'script': [
  ('0-5 min | Accroche','Faire ouvrir la première page du cours. Demander : « Le détecteur fournit-il l’énergie qui fait briller la lampe ? » Accepter les hypothèses. Annoncer : « Nous allons distinguer ce qui informe et commande de ce qui fournit l’énergie nécessaire à l’action. »'),
  ('5-8 min | Lire le modèle d’éclairage','Suivre les flèches bleues : détecteur, carte, liaison, ordre vers distribuer. Puis les flèches orange : alimentation, module de puissance, LED. Dire : « Le module reçoit un ordre et autorise le transfert d’énergie. La LED convertit cette énergie en lumière. » Réponses orales : la carte détermine l’ordre ; la LED réalise l’éclairage.'),
  ('8-10 min | Nommer les fonctions','Passer à la deuxième page. Lire les trois fonctions d’information puis les quatre fonctions d’énergie. Dire : « Dans la lampe, nous n’isolons pas transmettre. Sur un système motorisé, une transmission peut relier le moteur à la partie mobile. Une fonction n’est pas un nom de pièce. »'),
  ('10-12 min | Vérifier et lancer','Demander : « Une carte alimentée en électricité appartient-elle forcément à la chaîne d’énergie ? » Réponse : non, son rôle est de traiter. « Quel bloc reçoit l’ordre ? » Réponse : distribuer. Transition : « Avec le vocabulaire sous les yeux, identifiez maintenant les composants des deux chaînes du portail. »')
 ],
 'activity': '12-17 : lire le modèle et traiter Q1-Q2 en réponses courtes. 17-29 : construire les chaînes (Q3) et traiter Q4 ; fournir les fonctions dans l’ordre aux élèves fragiles. 29-37 : tester les quatre situations de Q5, avec changement de pilote après deux essais. Q6-Q7 sont traitées oralement en correction ; les plus rapides peuvent les rédiger.',
 'correction': '37-41 : compléter le schéma et suivre l’ordre vers distribuer. 41-44 : discuter Q6 (transmettre défaillante) et Q7 (carte classée par son rôle). 44-47 : vérifier les quatre ordres, puis compléter la synthèse. Faire citer électrique en entrée et mécanique en sortie du moteur.',
 'trace_use': 'Distribuer la page APRÈS avec le schéma déjà complété. Ne pas demander de recopier les sept cases en cinq minutes. Faire suivre les flèches et écrire une phrase : « L’ordre arrive au bloc distribuer ; le moteur convertit l’énergie électrique en énergie mécanique. »',
 'priority': 'Priorité à Q1-Q5, au trajet de l’ordre et à la conversion du moteur. Q6-Q7 sont discutées collectivement. La mémorisation exacte des sept fonctions se consolidera après cette séance.'
}}

def adapt_lessons(lessons):
    for lesson in lessons:
        d=INTRO[lesson['level']]
        lesson['timeline']=[
          ['0-5 min','Accroche',d['hook']],
          ['5-12 min','Cours illustré','Suivre le script AVANT ; définir le vocabulaire et vérifier oralement la compréhension.'],
          ['12-37 min','Activité sur PC',d['activity']],
          ['37-47 min','Correction',d['correction']],
          ['47-52 min','Trace écrite',d['trace_use']],
          ['52-55 min','Bilan individuel','Répondre au billet de sortie puis télécharger les réponses. Réserver la dernière minute à l’enregistrement ; en binôme, chacun répond dans sa case.']
        ]

class Illustration(Flowable):
    def __init__(self,kind):
        super().__init__(); self.kind=kind; self.width=515
        self.height={'bag':190,'logic':154,'light_rule':175,'lamp_chains':210}[kind]
    def text(self,x,y,w,s,size=10,bold=False,color=INK,align=0):
        st=ParagraphStyle('drawing',fontName='LessonBold' if bold else 'Lesson',fontSize=size,leading=size*1.28,textColor=color,alignment=align)
        p=Paragraph(escape(s).replace('\n','<br/>'),st);_,h=p.wrap(w,500);p.drawOn(self.canv,x,y-h)
    def box(self,x,y,w,h,title,detail='',col=BLUE):
        c=self.canv;c.setStrokeColor(col);c.setFillColor(colors.white);c.roundRect(x,y,w,h,5,stroke=1,fill=1)
        self.text(x+6,y+h-7,w-12,title,9.4,True,col,1)
        if detail:self.text(x+6,y+h-25,w-12,detail,9,False,INK,1)
    def arrow(self,x1,y1,x2,y2,col=BLUE):
        c=self.canv;c.setStrokeColor(col);c.setFillColor(col);c.setLineWidth(1.3);c.line(x1,y1,x2,y2)
        a=atan2(y2-y1,x2-x1);p=c.beginPath();p.moveTo(x2,y2);p.lineTo(x2-6*cos(a-.5),y2-6*sin(a-.5));p.lineTo(x2-6*cos(a+.5),y2-6*sin(a+.5));p.close();c.drawPath(p,fill=1,stroke=0)
    def draw(self):
        c=self.canv;k=self.kind;c.setLineWidth(1.3)
        if k=='bag':
            c.setStrokeColor(BLUE);c.setFillColor(PALE)
            c.roundRect(184,30,146,130,15,fill=1,stroke=1)
            c.roundRect(230,155,53,24,9,fill=0,stroke=1)
            c.roundRect(181,22,17,128,7,fill=0,stroke=1)
            c.roundRect(316,22,17,128,7,fill=0,stroke=1)
            c.roundRect(204,40,105,50,6,fill=0,stroke=1);c.line(203,102,310,102)
            for x in range(205,311,9):c.line(x,99,x,105)
            self.text(2,173,158,'Poignée\nSaisir le cartable',10,True);self.arrow(151,149,243,168)
            self.text(352,169,160,'Bretelle\nPorter sur l’épaule\nTissu de polyester',10);self.arrow(349,135,329,121)
            self.text(2,99,158,'Fermeture à glissière\nOuvrir et fermer\nDents en plastique',10);self.arrow(154,76,219,102)
            self.text(352,73,160,'Poche\nRanger de petits objets\nTissu de polyester',10);self.arrow(347,44,301,57)
            self.text(50,17,415,'Dessin d’un modèle simplifié : les matériaux peuvent varier.',8.2,False,INK,1)
        elif k=='logic':
            self.box(2,86,235,61,'A : BADGE VALIDE','Une condition vraie ou fausse')
            self.box(278,86,235,61,'B : CODE CORRECT','Une autre condition')
            self.box(2,5,235,61,'RÈGLE A ET B','Les deux conditions sont vraies.')
            self.box(278,5,235,61,'RÈGLE A OU B','Au moins une condition est vraie.')
        elif k=='light_rule':
            self.box(65,119,385,49,'Luminosité < 30 ET présence ?')
            self.arrow(163,119,163,82);self.arrow(352,119,352,82)
            self.text(102,113,50,'VRAI',9,True);self.text(366,113,60,'FAUX',9,True)
            self.box(68,30,190,51,'ALLUMER','Les deux conditions sont vraies.')
            self.box(294,30,190,51,'ÉTEINDRE','Au moins une est fausse.')
            self.text(60,19,430,'Le programme réévalue régulièrement les informations.',8.6,False,INK,1)
        elif k=='lamp_chains':
            self.text(0,207,515,'INFORMATION : recueillir, décider, envoyer un ordre',10,True,BLUE)
            xs=[0,177,354];w=160
            for x,t,d in zip(xs,['ACQUÉRIR','TRAITER','COMMUNIQUER'],['Détecteur de présence','Carte de commande','Liaison de commande']):self.box(x,129,w,51,t,d,BLUE)
            for a,b in zip(xs,xs[1:]):self.arrow(a+w,154,b,154)
            self.text(0,88,515,'ÉNERGIE : fournir, distribuer, convertir',10,True,ORANGE)
            for x,t,d in zip(xs,['ALIMENTER','DISTRIBUER','CONVERTIR'],['Bloc d’alimentation','Module de puissance','Lampe LED']):self.box(x,19,w,51,t,d,ORANGE)
            for a,b in zip(xs,xs[1:]):self.arrow(a+w,44,b,44,ORANGE)
            c.setStrokeColor(BLUE);c.line(434,129,434,105);c.line(434,105,257,105);self.arrow(257,105,257,70,BLUE)
            self.text(305,121,95,'ordre',9,True,BLUE)
            self.text(23,13,307,'Énergie électrique entre ces blocs',8.5,False,ORANGE)
            self.text(359,13,155,'Action : éclairer',8.5,True,ORANGE)

def course_story(lesson,P,table,Chain,phase=None):
    d=INTRO[lesson['level']];story=[]
    pages=[]
    if phase!='after':
        pages += [('AVANT L’ACTIVITÉ',b) for b in d['before']]
    if phase!='before':pages += [('APRÈS LA CORRECTION',d['after'])]
    for i,(label,blocks) in enumerate(pages):
        if i:story.append(PageBreak())
        story += [P(lesson['level'].upper()+'  |  '+label,'meta'),P(d['title'],'title')]
        for kind,value in blocks:
            if kind in ('p','h'):story.append(P(value,'h' if kind=='h' else 'body'))
            elif kind=='table':story += [table(*value),Spacer(1,9)]
            elif kind=='diagram':story += [Chain(True) if value=='gate' else Illustration(value),Spacer(1,10)]
    return story

def script_story(lesson,P):
    d=INTRO[lesson['level']]
    story=[P(lesson['level'].upper()+'  |  PAROLES ET QUESTIONS DU PROFESSEUR','meta'),P('Conduire le cours d’introduction','title')]
    for title,body in d['script']:story += [P(title,'h'),P(body)]
    story += [P('Pour tenir en 55 minutes','h'),P(d['priority']),P('Si une notion bloque','h'),P('Prendre un exemple oral supplémentaire puis donner l’amorce de réponse. Conserver le bilan individuel ; reporter les prolongements à la séance suivante.')]
    return story

def intro_markdown(lesson):
    d=INTRO[lesson['level']]
    s='# '+lesson['level']+' - Cours illustré et trace écrite\n\n'
    s+='[Cours avant activité](exports/'+lesson['level']+'-cours-avant.pdf) · [Trace après correction](exports/'+lesson['level']+'-trace-apres.pdf)\n\n'
    for title,body in d['script']:s+='## '+title+'\n\n'+body+'\n\n'
    s+='## Trace écrite\n\n'+ '\n\n'.join(value for kind,value in d['after'] if kind=='p')+'\n\n'
    s+='## Priorités\n\n'+d['priority']+'\n'
    return s
