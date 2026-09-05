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
 d=Drawing(900,600)
 ink=HexColor('#203247');blue=HexColor('#175b9a');orange=HexColor('#9c4a0b');gray=HexColor('#e9edf0')
 def rect(x,y,w,h,fill=white,stroke=ink):d.add(Rect(x,y,w,h,fillColor=fill,strokeColor=stroke,strokeWidth=1.5))
 def line(x,y,X,Y,color=ink,dash=None,width=1.5):d.add(Line(x,y,X,Y,strokeColor=color,strokeWidth=width,strokeDashArray=dash))
 def txt(x,y,s,size=15,color=ink):d.add(String(x,y,s,fontName='Helvetica',fontSize=size,fillColor=color))
 def arrow(x,y,X,Y,color=ink,dash=None):
  line(x,y,X,Y,color,dash,2)
  import math
  a=math.atan2(Y-y,X-x)
  d.add(Polygon([X,Y,X-10*cos(a-.4),Y-10*sin(a-.4),X-10*cos(a+.4),Y-10*sin(a+.4)],fillColor=color,strokeColor=color))
 def tag(n,x,y,X,Y):
  line(x,y,X,Y);d.add(Circle(x,y,12,fillColor=white,strokeColor=ink,strokeWidth=2));txt(x-4,y-5,str(n),15)
 def gear(x,y):
  points=[]
  for i in range(48):
   a=i*2*pi/48;rr=18 if i%4 in (0,3) else 23;points.extend([x+rr*cos(a),y+rr*sin(a)])
  d.add(Polygon(points,fillColor=gray,strokeColor=ink,strokeWidth=1.5));d.add(Circle(x,y,5,fillColor=white,strokeColor=ink))
 txt(16,576,'A. PORTAIL COULISSANT - VUE DE FACE, CÔTÉ INTÉRIEUR',18)
 # opening on left; leaf partly retracted on right; closing moves left.
 rect(65,328,34,188,gray);rect(480,328,34,188,gray)
 txt(30,523,'Pilier',14);txt(457,523,'Pilier',14)
 rect(248,352,520,145,gray)
 for x in range(270,757,27):line(x,362,x,487)
 rect(248,352,520,10,white);rect(248,487,520,10,white)
 for x in (292,724):d.add(Circle(x,343,9,fillColor=white,strokeColor=ink,strokeWidth=2))
 line(30,333,846,333,width=3);txt(697,309,'Rail au sol',14)
 arrow(415,542,260,542);txt(265,558,'Sens de fermeture',15)
 txt(310,511,'Vantail mobile',15)
 # beam parallel to gate in offset plane (front elevation schematic)
 rect(72,404,20,28,white);rect(486,404,20,28,white)
 line(93,418,486,418,blue,[6,5],2);txt(129,432,'Faisceau devant le vantail',14,blue)
 tag(2,149,475,82,418);line(149,463,496,428)
 # button at left
 rect(17,459,24,33,gray);d.add(Circle(29,475,7,fillColor=white,strokeColor=ink));tag(1,29,544,29,492)
 # rack underneath gate, motor fixed near right pillar
 rect(252,396,508,8,white)
 for x in range(256,754,12):rect(x,392,5,4,gray)
 rect(527,331,74,61,white);gear(555,369);txt(569,374,'M',17)
 tag(8,626,324,589,352);tag(9,690,408,662,400)
 # limit sensor fixed near motor, target fixed to moving leaf, displaced to right while open
 rect(603,376,12,19,gray);rect(751,377,14,12,white)
 tag(3,610,499,609,389);txt(603,470,'Capteur fixe',14)
 txt(726,446,'Cible mobile',14);line(765,440,758,389)
 # cabinet separate inset
 rect(805,377,64,106,gray);txt(800,495,'Coffret',14);line(805,377,875,283,dash=[4,4]);line(869,377,888,283,dash=[4,4])
 txt(16,285,'B. COFFRET DE COMMANDE - BLOCS SÉPARÉS POUR LA LECTURE',18)
 txt(16,256,'Les blocs peuvent être réunis dans un même boîtier sur un portail réel.',14)
 rect(200,35,681,197,HexColor('#f8f9fa'))
 # information flows across top
 txt(18,206,'Entrées 1, 2 et 3',15,blue);arrow(155,200,226,200,blue,[5,4])
 rect(230,166,180,57);txt(244,187,'Carte programmable' if corrected else 'Bloc à identifier',15)
 tag(4,250,230,250,222)
 arrow(410,194,632,194,blue,[5,4]);tag(5,511,225,511,194)
 rect(636,164,222,60);txt(650,187,'Module de puissance' if corrected else 'Bloc à identifier',15)
 tag(7,832,236,832,222)
 # energy path on bottom routed to power module then motor
 txt(24,104,'Réseau électrique',15,orange);arrow(166,110,230,110,orange)
 rect(230,72,210,65);txt(244,112,'Alimentation 24 V' if corrected else 'Bloc à identifier',15);txt(244,89,'Sortie : énergie électrique',13)
 tag(6,249,149,249,137)
 line(440,108,745,108,orange,width=2);arrow(745,108,745,164,orange)
 line(858,183,880,183,orange,width=2);line(880,183,880,58,orange,width=2);arrow(880,58,635,58,orange)
 txt(475,51,'Vers le moteur 8',15,orange)
 txt(20,14,'Pointillés : information / ordre. Trait plein fléché : énergie. Traits fins : repérage des pièces.',14)
 return d

def portal_svg(corrected=False,legend=True):
 d=portal_drawing(corrected)
 if legend:
  full=Drawing(900,790)
  group=Group(*d.contents);group.translate(0,190);full.add(group)
  for i,(n,name,fn) in enumerate(COMPONENTS):
   col=i//5;row=i%5
   text=n+' - '+(name+' / '+fn if corrected else '_________________________________')
   full.add(String(20+col*450,160-row*31,text,fontName='Helvetica',fontSize=14,fillColor=HexColor('#203247')))
  d=full
 return renderSVG.drawToString(d).replace('<svg ', '<svg role="img" aria-label="Vue du portail coulissant et détail du coffret de commande" ',1)
