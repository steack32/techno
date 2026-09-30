from pathlib import Path as FilePath
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.graphics.shapes import Drawing,Line,Rect,String,Polygon,Path
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
BASE=FilePath(__file__).resolve().parents[1]
for name,file in [('DejaVu','DejaVuSans.ttf'),('DejaVu-Bold','DejaVuSans-Bold.ttf')]:pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
pdfmetrics.registerFontFamily('DejaVu',normal='DejaVu',bold='DejaVu-Bold')
ink=colors.HexColor('#193e49');teal=colors.HexColor('#167b83');pale=colors.HexColor('#edf5f4');orange=colors.HexColor('#b86229')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyM',fontName='DejaVu',fontSize=9.5,leading=14,textColor=ink,spaceAfter=7))
styles.add(ParagraphStyle(name='SmallM',parent=styles['BodyM'],fontSize=8,leading=11))
styles.add(ParagraphStyle(name='TitleM',parent=styles['BodyM'],fontName='DejaVu-Bold',fontSize=23,leading=28,spaceAfter=10))
styles.add(ParagraphStyle(name='HeadingM',parent=styles['BodyM'],fontName='DejaVu-Bold',fontSize=12,leading=16,spaceBefore=10,spaceAfter=7,textColor=teal))
P=lambda s,sty='BodyM':Paragraph(s,styles[sty])
def table(rows,widths):
 t=Table([[P(c,'SmallM') for c in r] for r in rows],colWidths=widths,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),pale),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#c8d7d9')),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]));return t

def efforts():
 d=Drawing(495,111)
 for i,(label,verb) in enumerate([('Traction','Tirer'),('Compression','Pousser'),('Flexion','Courber'),('Torsion','Tordre')]):
  x=i*125;d.add(Rect(x,0,119,106,fillColor=pale,strokeColor=None));d.add(String(x+59,87,label,fontName='DejaVu-Bold',fontSize=9,textAnchor='middle',fillColor=ink));d.add(String(x+59,12,verb,fontName='DejaVu',fontSize=8,textAnchor='middle',fillColor=ink))
  if i<2:
   d.add(Rect(x+30,44,60,12,fillColor=teal,strokeColor=None))
   for a,b in ([(x+28,x+8),(x+92,x+112)] if i==0 else [(x+7,x+28),(x+112,x+92)]):
    d.add(Line(a,50,b,50,strokeColor=orange,strokeWidth=2));k=1 if b>a else -1;d.add(Polygon([b,50,b-6*k,54,b-6*k,46],fillColor=orange,strokeColor=None))
  elif i==2:
   path=Path(strokeColor=teal,strokeWidth=7);path.moveTo(x+20,55);path.curveTo(x+40,32,x+80,32,x+100,55);d.add(path);d.add(Line(x+60,74,x+60,51,strokeColor=orange,strokeWidth=2));d.add(Polygon([x+60,48,x+56,55,x+64,55],fillColor=orange,strokeColor=None))
  else:
   d.add(Polygon([x+23,38,x+96,62,x+96,38,x+23,62],fillColor=teal,strokeColor=None));d.add(String(x+8,48,'↻',fontName='DejaVu',fontSize=23,fillColor=orange));d.add(String(x+95,35,'↺',fontName='DejaVu',fontSize=23,fillColor=orange))
 return d

def shelf():
 d=Drawing(495,112);d.add(Line(48,74,440,74,strokeWidth=9,strokeColor=colors.HexColor('#b78956')))
 for x in [52,437]:d.add(Polygon([x,65,x-13,45,x+13,45],fillColor=ink,strokeColor=None))
 p=Path(strokeColor=orange,strokeWidth=2);p.moveTo(52,70);p.curveTo(155,25,332,25,437,70);d.add(p)
 d.add(Line(245,109,245,85,strokeColor=orange,strokeWidth=2));d.add(Polygon([245,80,240,88,250,88],fillColor=orange,strokeColor=None));d.add(String(270,97,'Charge centrale',fontName='DejaVu',fontSize=8,fillColor=ink));d.add(Line(52,17,437,17,strokeColor=ink));d.add(String(245,2,'Portée : distance entre les appuis',fontName='DejaVu',fontSize=8,textAnchor='middle',fillColor=ink));d.add(String(278,54,'Flèche : affaissement maximal',fontName='DejaVu',fontSize=8,fillColor=orange));return d

def footer(c,doc):
 c.setStrokeColor(teal);c.line(48,40,547,40);c.setFont('DejaVu',8);c.setFillColor(ink);c.drawString(48,27,'Technologie · Matériaux et résistance · Synthèse');c.drawRightString(547,27,f'{doc.page} / 2')
flow=[P('MATÉRIAUX ET RÉSISTANCE','TitleM'),P('Comprendre avant de choisir','HeadingM'),P('Un objet doit répondre à un besoin tout en respectant plusieurs contraintes. Son comportement dépend du <b>matériau</b>, de sa <b>forme</b>, de ses <b>dimensions</b>, des <b>appuis</b> et de la <b>charge</b>.'),P('1. Quatre familles de matériaux','HeadingM'),table([['<b>Famille</b>','<b>Exemples</b>'],['Métalliques','Acier, aluminium, cuivre'],['Organiques','Bois, coton, nombreux polymères (plastiques)'],['Minéraux / céramiques','Verre, porcelaine, terre cuite'],['Composites','Résine + fibres de verre ; béton armé']],[157,338]),P('Une famille ne suffit pas à prévoir toutes les propriétés d’un matériau. Un objet peut associer plusieurs matériaux.','SmallM'),P('2. Des propriétés à ne pas confondre','HeadingM'),table([['<b>Propriété</b>','<b>Ce qu’elle décrit</b>'],['Masse volumique','La masse pour un volume donné. À volume égal, le matériau de plus faible masse volumique donne la pièce la plus légère.'],['Rigidité','L’opposition à la déformation élastique. Une pièce rigide se déforme peu sous une charge donnée.'],['Résistance mécanique','La capacité à supporter une sollicitation sans défaillance : déformation permanente, rupture…'],['Autres critères','Humidité, corrosion, fabrication, coût, durée de vie et impact environnemental.']],[157,338]),P('3. Quatre sollicitations','HeadingM'),efforts(),P('Un objet peut subir plusieurs sollicitations en même temps. Une pièce comprimée et élancée peut aussi se courber : c’est le <b>flambement</b>.','SmallM'),PageBreak(),P('TESTER ET JUSTIFIER','TitleM'),P('4. Après le retrait de la charge','HeadingM'),table([['<b>Observation</b>','<b>Conclusion</b>'],['La pièce reprend sa forme.','Déformation <b>élastique</b> : réversible.'],['La pièce reste déformée.','Déformation <b>permanente</b> : irréversible.'],['La pièce est cassée.','<b>Rupture</b>. Un matériau fragile peut casser sans déformation permanente visible.']],[235,260]),P('<b>Rigide ne veut pas dire incassable.</b> Une plaque de verre peut se déformer peu, mais casser sous un choc.'),P('5. Comprendre la flexion d’une étagère','HeadingM'),shelf(),P('À matériau, charge et appuis fixés, une section pleine plus épaisse se déforme moins, mais sa masse augmente. Rapprocher les appuis réduit aussi la flèche.'),P('À dimensions extérieures identiques, un caisson creux est plus léger et moins rigide que la section pleine correspondante. Sa forme peut offrir un compromis intéressant entre masse et rigidité.'),P('6. Réaliser une comparaison valable','HeadingM'),P('<b>1.</b> Formuler une prévision.<br/><b>2.</b> Choisir un réglage de référence.<br/><b>3.</b> Modifier <b>un seul paramètre</b> et conserver les autres.<br/><b>4.</b> Noter les réglages, la masse et la flèche.<br/><b>5.</b> Comparer les résultats et expliquer le compromis.'),P('7. Le défi du coin lecture','HeadingM'),P('Portée : <b>80 cm</b> · Charge centrale : <b>10 kg</b><br/>Masse de la pièce : <b>2 kg maximum</b> · Flèche : <b>3 mm maximum</b>'),P('<b>Limites du modèle :</b> le simulateur étudie la rigidité élastique. Il ne calcule ni la rupture, ni les fixations, ni le poids propre, ni le vieillissement. Réussir le défi ne suffit pas à valider une construction réelle.','SmallM'),P('Pour aller plus loin : University of Cambridge, « Stiffness » ; Iowa State University, « Beam Deflection Formulae ».','SmallM')]
out=BASE/'site/4eme/materiaux/synthese-materiaux.pdf'
SimpleDocTemplate(str(out),pagesize=(595.28,841.89),rightMargin=50,leftMargin=50,topMargin=40,bottomMargin=52,title='Matériaux et résistance - Synthèse',author='Technologie').build(flow,onFirstPage=footer,onLaterPages=footer)
print(out)
