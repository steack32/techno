"""Published paper activities use the same closed questions as the digital activities."""
import json,subprocess
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from visuels import light_drawing
from portail import portal_drawing
ROOT=Path(__file__).resolve().parents[1]
data=json.loads(subprocess.check_output(['node','--input-type=module','-e',"import {activities} from './site/digital-activities.js';console.log(JSON.stringify(activities))"],cwd=ROOT,text=True))
for name,file in [('DejaVu','DejaVuSans.ttf'),('DejaVu-Bold','DejaVuSans-Bold.ttf')]:pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
pdfmetrics.registerFontFamily('DejaVu',normal='DejaVu',bold='DejaVu-Bold')
s=getSampleStyleSheet();ink=colors.HexColor('#193e49')
for name,size,leading,bold in [('Text',9,12,False),('Title',19,23,True),('Question',9,12,True),('Small',8,11,False)]:
 s.add(ParagraphStyle(name=name+'O',fontName='DejaVu-Bold' if bold else 'DejaVu',fontSize=size,leading=leading,textColor=ink,spaceAfter=5))
P=lambda t,style='Text':Paragraph(t,s[style+'O'])
paths={'lighting':'4e/eclairage-automatique/eleves/a-imprimer/fiche-eleve.pdf','chain':'3e/chaines-information-energie/eleves/a-imprimer/fiche-eleve.pdf','portal':'3e/chaines-information-energie/eleves/a-imprimer/seance2-portail-automatique.pdf'}
urls={'lighting':'4eme/eclairage-automatique','chain':'3eme/chaines-information-energie','portal':'3eme/chaines-information-energie'}
for name,activity in data.items():
 def footer(c,doc):
  c.setFont('DejaVu',7);c.setFillColor(ink);c.drawString(42,32,'Technologie · QCM, associations et calculs · '+str(doc.page)+' / 2');c.drawString(42,21,'Correction interactive : techno.terrier.workers.dev/'+urls[name]+'/')
 flow=[];qs=activity['questions'];split=9 if name!='portal' else 10
 for page,items in enumerate([qs[:split],qs[split:]]):
  if page:flow.append(PageBreak())
  flow.extend([P(escape(activity['title']) if not page else 'Tester et vérifier','Title'),P('Coche une réponse par question. Pour les associations, choisis la fonction. Pour les calculs, donne une valeur. Retrouve chaque correction dans l’activité numérique.','Small')])
  if not page:
   flow.append(P(escape(activity['intro'])))
   if name=='lighting':
    d=light_drawing();d.scale(.56,.56);d.width*=.56;d.height*=.56;flow.append(d)
   elif name=='portal':
    flow.append(P('<b>Repères :</b> bouton / cellules / fin de course → carte → liaison de commande ; alimentation → module de puissance → moteur → pignon et crémaillère.','Small'))
  for i,q in enumerate(items,start=1 if not page else split+1):
   if q.get('type')=='number':body='Valeur : ....................'
   else:
    values=q['choices'];offset=(sum(map(ord,f'{name}_{i}')))%len(values);values=values[offset:]+values[:offset]
    body=' &nbsp; '.join('□ '+escape(v) for v in values)
   flow.append(KeepTogether([P(str(i)+'. '+escape(q['label']),'Question'),P(body,'Small'),Spacer(1,5)]))
  if page:flow.extend([Spacer(1,5),P('<b>À retenir :</b> '+{'lighting':'ET exige toutes les conditions ; OU en exige au moins une. Une inégalité stricte exclut la valeur limite. Après une correction, on refait les essais.','chain':'La chaîne d’information acquiert, traite et communique. La chaîne d’énergie alimente, distribue, convertit et transmet. Stocker l’énergie permet de décaler son utilisation.','portal':'La carte traite les informations et commande le module de puissance. Le moteur convertit l’énergie ; la transmission entraîne le portail. Un diagnostic cherche une cause compatible avec les observations.'}[name])])
 out=ROOT/paths[name];SimpleDocTemplate(str(out),pagesize=(595.28,841.89),leftMargin=42,rightMargin=42,topMargin=32,bottomMargin=48,title=activity['title'],author='Technologie').build(flow,onFirstPage=footer,onLaterPages=footer)
 from pypdf import PdfReader
 count=len(PdfReader(str(out)).pages)
 if count!=2:raise RuntimeError(f'{name}: {count} pages instead of 2')
 print(out.relative_to(ROOT),count,'pages')
