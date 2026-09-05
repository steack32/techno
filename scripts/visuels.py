"""Illustrations pédagogiques vectorielles pour les objets et l'éclairage."""
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line, Polygon, String
from reportlab.graphics import renderSVG
from reportlab.lib.colors import HexColor,white

def objects_drawing(lamp_only=False):
 d=Drawing(900,220);ink=HexColor('#24364b');gray=HexColor('#edf1f5')
 def text(x,y,t):d.add(String(x,y,t,fontName='Helvetica',fontSize=15,fillColor=ink))
 def line(x,y,X,Y):d.add(Line(x,y,X,Y,strokeColor=ink,strokeWidth=2))
 def circle(x,y,r):d.add(Circle(x,y,r,fillColor=white,strokeColor=ink,strokeWidth=2))
 def poly(points):d.add(Polygon(points,fillColor=gray,strokeColor=ink,strokeWidth=2))
 if not lamp_only:
  text(10,198,'VÉLO DE VILLE')
  circle(58,77,36);circle(238,77,36)
  for a,b in [((58,77),(104,153)),((104,153),(150,77)),((58,77),(150,77)),((104,153),(208,153)),((208,153),(150,77)),((208,153),(238,77)),((208,153),(200,173)),((200,173),(224,173)),((94,158),(116,158))]:line(*a,*b)
  circle(150,77,10);line(150,77,163,61);line(157,60,172,60)
  line(58,83,150,86);line(58,72,150,68)
  text(8,16,'Pneu');line(36,30,40,43)
  text(110,16,'Chaîne');line(132,30,111,72)
  text(247,164,'Cadre');line(251,150,169,119)
  line(307,10,307,200)
 x=335
 text(x,198,'LAMPE RECHARGEABLE')
 poly([x+90,45,x+171,45,x+186,34,x+74,34])
 line(x+128,45,x+128,146);line(x+128,146,x+160,154)
 poly([x+128,160,x+180,160,x+195,142,x+118,142])
 line(x+122,137,x+191,137)
 text(x+8,17,'Socle');line(x+55,27,x+92,37)
 text(x+189,175,'Coque');line(x+202,164,x+180,153)
 text(x+192,109,'Diffuseur');line(x+220,123,x+178,137)
 if not lamp_only:
  line(637,10,637,200)
  text(653,198,'VENTILATEUR USB')
  circle(758,124,51)
  poly([748,125,727,151,752,158,764,132]);poly([759,132,786,147,795,119,772,117]);poly([769,116,758,84,736,98,747,120]);circle(758,124,7)
  for xx in (732,746,760,774,788):line(xx,88,xx,160)
  line(758,73,758,47);poly([726,36,790,36,784,46,732,46])
  text(817,167,'Grille');line(820,156,801,144)
  text(817,100,'Pales');line(817,108,780,124)
  text(811,28,'Socle');line(812,39,782,40)
 if lamp_only:
  # Crop the lamp panel, preserving vector geometry and readable labels.
  from reportlab.graphics.shapes import Group
  cropped=Drawing(320,220);g=Group(*d.contents);g.translate(-330,0);cropped.add(g);return cropped
 return d

def light_drawing():
 d=Drawing(900,145);ink=HexColor('#24364b');blue=HexColor('#175b9a')
 def box(x,y,w,h,label):
  d.add(Rect(x,y,w,h,fillColor=white,strokeColor=ink,strokeWidth=2));d.add(String(x+12,y+h/2-5,label,fontName='Helvetica',fontSize=16,fillColor=ink))
 def arrow(x,y,X,Y):
  d.add(Line(x,y,X,Y,strokeColor=blue,strokeWidth=2));d.add(Polygon([X,Y,X-9,Y+5,X-9,Y-5],fillColor=blue,strokeColor=blue))
 box(10,89,225,42,'Capteur de luminosité');box(10,12,225,42,'Capteur de présence')
 box(368,51,230,52,'Carte programmable');box(705,51,180,52,'Lampe LED')
 for y in (110,33):
  d.add(Line(235,y,290,y,strokeColor=blue,strokeWidth=2));d.add(Line(290,y,290,77,strokeColor=blue,strokeWidth=2))
 arrow(290,77,368,77);arrow(598,77,705,77)
 d.add(String(251,134,'Informations',fontName='Helvetica',fontSize=14,fillColor=blue));d.add(String(619,105,'Ordre',fontName='Helvetica',fontSize=14,fillColor=blue))
 d.add(String(366,20,'Appliquer une règle',fontName='Helvetica',fontSize=14,fillColor=ink))
 return d

def visual_svg(name):
 d=light_drawing() if name=='eclairage' else objects_drawing(name=='lampe')
 s=renderSVG.drawToString(d);return s[s.index('<svg '):].replace('<svg ','<svg role="img" aria-label="'+('Capteurs, traitement et commande de la lampe' if name=='eclairage' else 'Composants des objets étudiés')+'" ',1)
