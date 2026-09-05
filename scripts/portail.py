"""Vue pédagogique vectorielle du portail, commune aux SVG, HTML et PDF."""
from reportlab.graphics.shapes import Drawing, Rect, Line, Circle, String, Polygon, Group
from reportlab.graphics import renderSVG
from reportlab.lib.colors import HexColor, white
from math import sin, cos, pi

COMPONENTS = [
 ('1','Bouton de fermeture','Acquérir'),
 ('2','Paire de cellules de détection','Acquérir'),
 ('3','Capteur de fin de course','Acquérir'),
 ('4','Carte programmable','Traiter'),
 ('5','Liaison de commande','Communiquer'),
 ('6','Bloc d’alimentation 24 V','Alimenter'),
 ('7','Module de puissance','Distribuer'),
 ('8','Moteur électrique','Convertir'),
 ('9','Pignon et crémaillère','Transmettre'),
]

def portal_drawing(corrected=False):
 # Toutes les positions ci-dessous sont exprimées depuis le haut de la page.
 H=740;d=Drawing(900,H)
 ink=HexColor('#203247');blue=HexColor('#175b9a');orange=HexColor('#91460e');gray=HexColor('#edf0f3')
 def rect(x,y,w,h,fill=white,stroke=ink):d.add(Rect(x,H-y-h,w,h,fillColor=fill,strokeColor=stroke,strokeWidth=1.8))
 def line(x,y,X,Y,color=ink,dash=None,width=1.8):d.add(Line(x,H-y,X,H-Y,strokeColor=color,strokeWidth=width,strokeDashArray=dash))
 def txt(x,y,s,size=17,color=ink):d.add(String(x,H-y,s,fontName='Helvetica',fontSize=size,fillColor=color))
 def circle(x,y,r,fill=white):d.add(Circle(x,H-y,r,fillColor=fill,strokeColor=ink,strokeWidth=1.8))
 def arrow(x,y,X,Y,color=ink,dash=None):
  line(x,y,X,Y,color,dash,2.3)
  import math
  a=math.atan2(Y-y,X-x)
  d.add(Polygon([X,H-Y,X-11*cos(a-.45),H-(Y-11*sin(a-.45)),X-11*cos(a+.45),H-(Y-11*sin(a+.45))],fillColor=color,strokeColor=color))
 def badge(n,x,y,X=None,Y=None):
  if X is not None:line(x,y,X,Y)
  circle(x,y,14);txt(x-5,y+6,str(n),18)
 def heading(y,title):
  rect(0,y-23,900,32,gray,gray);txt(12,y,title,18)
 def gear(x,y,r=31):
  pts=[]
  for i in range(48):
   a=i*pi/24;rr=r if i%4 in (0,3) else r-5;pts.extend([x+rr*cos(a),H-y+rr*sin(a)])
  d.add(Polygon(pts,fillColor=gray,strokeColor=ink,strokeWidth=2));circle(x,y,7)
 heading(24,'A. VUE D’ENSEMBLE - PORTAIL PARTIELLEMENT OUVERT')
 # Le vantail ferme le passage en coulissant vers le pilier gauche.
 rect(105,84,34,147,gray);rect(494,84,34,147,gray)
 rect(307,99,459,113,white)
 for x in range(330,758,43):line(x,103,x,207,width=1.2)
 line(307,110,766,110);line(307,201,766,201)
 circle(348,222,9);circle(727,222,9);line(60,232,800,232,width=3)
 txt(333,89,'Vantail mobile',17);arrow(425,58,276,58);txt(270,49,'Fermeture',17)
 # Capteurs visibles devant le vantail ; un même repère pour la paire.
 rect(111,140,22,34);circle(122,157,6)
 rect(500,140,22,34);circle(511,157,6)
 line(136,157,496,157,blue,[8,6],2.8)
 rect(192,164,250,25,white,white);txt(202,182,'Faisceau devant le vantail',16,blue)
 badge(2,170,209,122,166);badge(2,540,66,511,140)
 rect(27,113,34,48,gray);circle(44,137,10);badge(1,44,77,44,113)
 # Seulement la zone à observer : ses pièces sont agrandies en B.
 rect(576,186,62,45,gray);txt(592,215,'M',19)
 line(564,183,650,183,dash=[5,4]);line(650,183,650,237,dash=[5,4])
 line(650,237,564,237,dash=[5,4]);line(564,237,564,183,dash=[5,4])
 txt(671,252,'Détails en B',16);line(667,244,650,221)
 txt(68,252,'Rail au sol',16)
 heading(285,'B. AGRANDISSEMENTS - TRANSMISSION ET FIN DE COURSE')
 line(465,302,465,473,HexColor('#c0c9d2'))
 # Engrènement : les dents du pignon atteignent celles de la crémaillère.
 txt(16,315,'Transmission du mouvement',17)
 rect(57,342,340,13,gray)
 for x in range(61,392,17):rect(x,355,8,9,gray)
 gear(199,394,31)
 arrow(145,333,80,333,orange)
 line(230,394,279,394,orange,width=4)
 rect(279,369,108,55,gray);txt(307,403,'M',25)
 badge(9,31,390,110,351);line(44,399,168,394)
 badge(8,420,398,387,398)
 txt(60,452,'Rotation du pignon → translation du vantail',16)
 # La cible est solidaire du vantail et se déplace vers le capteur fixe.
 txt(490,315,'Détection de la position fermée',17)
 rect(659,342,213,13,gray);txt(702,335,'Vantail',16)
 rect(713,355,33,32,gray)
 arrow(705,402,605,402,blue);txt(704,422,'Cible mobile',16)
 rect(546,359,39,42,white);circle(578,380,4)
 line(546,405,546,438);line(526,438,589,438,width=3)
 badge(3,513,376,546,380)
 txt(525,461,'Capteur fixe',16)
 txt(702,461,'À l’arrivée de la cible :',16);txt(702,481,'position fermée détectée.',16)
 heading(510,'C. COFFRET DE COMMANDE - BLOCS FONCTIONNELS')
 # Information : aucun croisement avec les transferts d'énergie.
 txt(8,570,'Entrées',17,blue);txt(8,590,'1, 2 et 3',17,blue)
 arrow(98,578,172,578,blue,[7,5])
 rect(175,550,218,60);txt(190,585,'Carte programmable' if corrected else 'Bloc à identifier',17)
 badge(4,187,537)
 arrow(393,578,623,578,blue,[7,5]);badge(5,500,554,500,578)
 rect(625,550,238,60);txt(639,585,'Module de puissance' if corrected else 'Bloc à identifier',17)
 badge(7,848,537)
 # Réseau -> alimentation -> module de puissance -> moteur.
 txt(8,671,'Réseau',17,orange);arrow(82,671,172,671,orange)
 rect(175,642,230,55);txt(190,677,'Alimentation 24 V' if corrected else 'Bloc à identifier',17)
 badge(6,187,628)
 line(405,670,688,670,orange,width=2.3);arrow(688,670,688,610,orange)
 line(825,610,825,648,orange,width=2.3);arrow(825,648,775,648,orange)
 txt(746,681,'Vers moteur 8',17,orange)
 txt(12,730,'Pointillés : information / ordre. Flèches pleines : énergie ou mouvement. Traits fins : repérage.',16)
 return d

def portal_svg(corrected=False,legend=True):
 d=portal_drawing(corrected)
 if legend:
  full=Drawing(900,d.height+190)
  group=Group(*d.contents);group.translate(0,190);full.add(group)
  for i,(n,name,fn) in enumerate(COMPONENTS):
   col=i//5;row=i%5
   text=n+' - '+(name+' / '+fn if corrected else '_________________________________')
   full.add(String(20+col*450,160-row*31,text,fontName='Helvetica',fontSize=14,fillColor=HexColor('#203247')))
  d=full
 return renderSVG.drawToString(d).replace('<svg ', '<svg role="img" aria-label="Portail coulissant, agrandissements de la transmission et de la fin de course, coffret de commande" ',1)
