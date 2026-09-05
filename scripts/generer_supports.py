"""Génère les supports Markdown, HTML et PDF par niveau et par séquence.

Exécution : python scripts/generer_supports.py
Dépendance pour les PDF : reportlab. Les activités produites sont autonomes.
"""
from pathlib import Path
from html import escape
import json, shutil, reportlab
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Flowable
from contenus import LESSONS, SOURCES
from activites import make_html, diagram_svg
from portail import portal_drawing, portal_svg, COMPONENTS
from visuels import objects_drawing, light_drawing, visual_svg
from parcours_guide import guided_lesson

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output'/'pdf'
OUT.mkdir(parents=True,exist_ok=True)

fontdir=Path(reportlab.__file__).resolve().parent/'fonts'
fallback=Path('/usr/share/fonts/truetype/dejavu')
if fallback.joinpath('DejaVuSans.ttf').exists():
    normal=fallback/'DejaVuSans.ttf'; bold=fallback/'DejaVuSans-Bold.ttf'
else:
    normal=fontdir/'Vera.ttf'; bold=fontdir/'VeraBd.ttf'
pdfmetrics.registerFont(TTFont('Lesson',str(normal)))
pdfmetrics.registerFont(TTFont('LessonBold',str(bold)))
pdfmetrics.registerFontFamily('Lesson',normal='Lesson',bold='LessonBold',italic='Lesson',boldItalic='LessonBold')
INK=colors.HexColor('#172b43'); BLUE=colors.HexColor('#175b9a'); ORANGE=colors.HexColor('#a6520b'); LINE=colors.HexColor('#cad5df')
PAGE_W,PAGE_H=A4
WIDTH=PAGE_W-80
S={
 'body':ParagraphStyle('body',fontName='Lesson',fontSize=10.2,leading=14.2,spaceAfter=7,textColor=INK),
 'small':ParagraphStyle('small',fontName='Lesson',fontSize=8.8,leading=11.8,spaceAfter=6,textColor=INK),
 'title':ParagraphStyle('title',fontName='LessonBold',fontSize=21,leading=25,spaceAfter=8,textColor=INK),
 'h':ParagraphStyle('h',fontName='LessonBold',fontSize=12.4,leading=16,spaceBefore=6,spaceAfter=7,textColor=BLUE,keepWithNext=True),
 'q':ParagraphStyle('q',fontName='LessonBold',fontSize=10,leading=13.6,spaceBefore=7,spaceAfter=4,textColor=INK,keepWithNext=True),
 'cell':ParagraphStyle('cell',fontName='Lesson',fontSize=9.1,leading=12.2,spaceAfter=0,textColor=INK),
 'cellhead':ParagraphStyle('cellhead',fontName='LessonBold',fontSize=9,leading=11.7,spaceAfter=0,textColor=INK),
 'meta':ParagraphStyle('meta',fontName='LessonBold',fontSize=8.5,leading=11,spaceAfter=7,textColor=BLUE),
}

def P(text,style='body',raw=False):
    return Paragraph(text if raw else escape(text),S[style])

class AnswerLines(Flowable):
    def __init__(self,n=2):
        Flowable.__init__(self); self.n=n; self.width=WIDTH; self.height=15*n+3
    def draw(self):
        c=self.canv;c.setStrokeColor(LINE);c.setLineWidth(.5)
        for i in range(self.n): c.line(0,3+i*15,self.width,3+i*15)

class Chain(Flowable):
    def __init__(self,filled=False):
        Flowable.__init__(self);self.width=WIDTH;self.height=190 if filled else 151;self.filled=filled
    def arrow(self,x1,y1,x2,y2,col):
        c=self.canv;c.setStrokeColor(col);c.setFillColor(col);c.setLineWidth(1)
        c.line(x1,y1,x2,y2)
        import math
        a=math.atan2(y2-y1,x2-x1);p=c.beginPath();p.moveTo(x2,y2)
        p.lineTo(x2-5*math.cos(a-.5),y2-5*math.sin(a-.5));p.lineTo(x2-5*math.cos(a+.5),y2-5*math.sin(a+.5));p.close();c.drawPath(p,fill=1,stroke=0)
    def box(self,x,y,w,h,title,detail,col):
        c=self.canv;c.setStrokeColor(col);c.setFillColor(colors.white);c.roundRect(x,y,w,h,3,fill=1,stroke=1)
        c.setFillColor(col);c.setFont('LessonBold',8.6);c.drawCentredString(x+w/2,y+h-13,title)
        st=ParagraphStyle('node',fontName='Lesson',fontSize=7.8,leading=9.3,alignment=1,textColor=INK)
        p=Paragraph(escape(detail).replace('\n','<br/>'),st);_,ph=p.wrap(w-8,h-18);p.drawOn(c,x+4,y+h-18-ph)
    def draw(self):
        c=self.canv;h=self.height;w=WIDTH
        top_y=h-64;bottom_y=28;bh=45 if self.filled else 35
        c.setFont('LessonBold',9);c.setFillColor(BLUE);c.drawString(0,h-8,"CHAÎNE D'INFORMATION")
        topx=[34,204,374];topw=112
        texts=['1 : bouton / 2 : cellules\n3 : fin de course','4 : carte programmable','5 : liaison de commande'] if self.filled else ['Repère(s) + composant(s) ?']*3
        for x,title,detail in zip(topx,['ACQUÉRIR','TRAITER','COMMUNIQUER'],texts): self.box(x,top_y,topw,bh,title,detail,BLUE)
        for a,b in zip(topx,topx[1:]): self.arrow(a+topw,top_y+bh/2,b,top_y+bh/2,BLUE)
        c.setFillColor(ORANGE);c.drawString(0,bottom_y+bh+9,"CHAÎNE D'ÉNERGIE")
        bx=[0,131,262,393];bw=122
        texts=['Réseau + 6 : bloc\nd’alimentation 24 V','7 : module de puissance','8 : moteur électrique','9 : pignon + crémaillère'] if self.filled else ['Repère(s) + composant(s) ?']*4
        for x,title,detail in zip(bx,['ALIMENTER','DISTRIBUER','CONVERTIR','TRANSMETTRE'],texts): self.box(x,bottom_y,bw,bh,title,detail,ORANGE)
        for a,b in zip(bx,bx[1:]): self.arrow(a+bw,bottom_y+bh/2,b,bottom_y+bh/2,ORANGE)
        middle=top_y-13;c.setStrokeColor(BLUE);c.line(topx[2]+56,top_y,topx[2]+56,middle);c.line(topx[2]+56,middle,bx[1]+bw/2,middle);self.arrow(bx[1]+bw/2,middle,bx[1]+bw/2,bottom_y+bh,BLUE)
        c.setFillColor(BLUE);c.setFont('Lesson',8.3);c.drawString(270,middle+3,'ordre')
        self.arrow(bx[-1]+bw/2,bottom_y,bx[-1]+bw/2,14,ORANGE);c.setFillColor(ORANGE);c.drawRightString(w,3,'Action : déplacement du portail')

def table(headers,rows,ratios=None,answer=False):
    n=len(headers);ratios=ratios or [1]*n
    widths=[WIDTH*r/sum(ratios) for r in ratios]
    data=[[P(x,'cellhead') for x in headers]]+[[P(x,'cell') if x else '' for x in row] for row in rows]
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    commands=[('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#eef3f8')),('GRID',(0,0),(-1,-1),.5,LINE),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]
    if answer: commands.append(('BOTTOMPADDING',(0,1),(-1,-1),11))
    t.setStyle(TableStyle(commands));return t

def header(canvas,doc):
    canvas.setStrokeColor(LINE);canvas.setLineWidth(.6);canvas.line(40,35,PAGE_W-40,35)
    canvas.setFont('Lesson',8);canvas.setFillColor(INK)
    canvas.drawString(40,22,'Technologie au collège')
    canvas.drawRightString(PAGE_W-40,22,f'{doc.page}')

def build_pdf(path,story,title):
    doc=SimpleDocTemplate(str(path),pagesize=A4,leftMargin=40,rightMargin=40,topMargin=35,bottomMargin=44,title=title,author='Ressources pédagogiques - Technologie',pageCompression=1)
    doc.build(story,onFirstPage=header,onLaterPages=header)
    from pypdf import PdfReader, PdfWriter
    reader=PdfReader(path)
    writer=PdfWriter()
    writer.clone_document_from_reader(reader)
    metadata={str(k):str(v) for k,v in (reader.metadata or {}).items() if k not in ('/CreationDate','/ModDate')}
    writer.metadata=None
    writer.add_metadata(metadata)
    with open(path,'wb') as stream: writer.write(stream)

def student_block(b):
    typ=b['type']
    if typ=='visual':
        d=light_drawing() if b['name']=='eclairage' else objects_drawing(b['name']=='lampe')
        target=260 if b['name']=='lampe' else WIDTH
        scale=target/d.width;d.scale(scale,scale);d.width*=scale;d.height*=scale
        return [d,Spacer(1,6)]
    if typ=='p':return [P(b['text'])]
    if typ=='h':return [P(b['text'],'h')]
    if typ=='q':return [P(b['label'],'q'),AnswerLines(b['lines'])]
    if typ=='exit':return [P(b['label'],'q'),AnswerLines(b['lines'])]
    if typ=='choice':return [P(b['label'],'q'),P(' / '.join(b['options'][1:])+'  (entoure ton choix)','small')]
    if typ=='sim':
        text='Sur PC : utilise le laboratoire de la fiche interactive. Sur papier : applique les règles du document pour prévoir les résultats.'
        if b['name']=='light': text+=' Règle initiale : SI luminosité < 30 OU présence ALORS allumer SINON éteindre.'
        return [P(text,'small')]
    if typ=='diagram':return [Chain()]
    if typ=='table':
        ratios=[1,2,2.8] if len(b['headers'])==3 else [1,2]
        return [table(b['headers'],b['rows'],ratios),Spacer(1,7)]
    if typ=='answer_table':
        rows=[]
        for r in range(b['rows']):rows.append([(b['fixed'][r] if b.get('fixed') else '')]+['']*(len(b['headers'])-1))
        ratios=([1.35,1] if len(b['headers'])==2 else None)
        return [P(b['label'],'q'),table(b['headers'],rows,ratios,True),Spacer(1,6)]
    raise ValueError(typ)

def portal_page(corrected=False):
    drawing=portal_drawing(corrected)
    scale=WIDTH/drawing.width
    drawing.scale(scale,scale);drawing.width*=scale;drawing.height*=scale
    rows=[]
    for i in range(5):
        cells=[]
        for j in (i,i+5):
            if j<len(COMPONENTS):
                n,name,fn=COMPONENTS[j];cells += [n,(name+' / '+fn) if corrected else '________________________']
            else:cells += ['','']
        rows.append(cells)
    return [P('Repérer les composants du portail','title'),P('Vue pédagogique simplifiée, sans échelle. '+('Corrigé : les numéros sont repris dans les deux chaînes.' if corrected else 'Complète la légende avec le tableau des composants de la page suivante.'),'small'),drawing,Spacer(1,8),table(['Repère','Composant'+(' / fonction' if corrected else ''),'Repère','Composant'+(' / fonction' if corrected else '')],rows,[.6,2.02,.6,2.02]),Spacer(1,6),P('Le faisceau de détection passe devant le vantail. La cible mobile rejoint le capteur fixe à la fin de la fermeture. Le pignon tourne et entraîne la crémaillère solidaire du vantail.','small')]

def student_pdf(lesson,path):
    story=[]
    if lesson['level']=='3e':
        story=[P('3E  |  SÉANCE 1  |  FICHE ÉLÈVE  |  1/4','meta')]+portal_page()+[PageBreak()]
    for i,page in enumerate(lesson['pages']):
        if i:story.append(PageBreak())
        story.append(P(f"{lesson['level'].upper()}  |  SÉANCE 1  |  FICHE ÉLÈVE  |  {i+1+(lesson['level']=='3e')}/{len(lesson['pages'])+(lesson['level']=='3e')}",'meta'))
        if i==0:
            story += [P(lesson['title'],'title'),P(lesson['question']),P('Nom : __________________________  Classe : __________','small')]
        for b in page:story+=student_block(b)
    build_pdf(path,story,lesson['level']+' - '+lesson['title'])

def guided_student_pdf(lesson,path):
    styles=[S['small'],S['body'],S['q']]
    saved=[(style.fontSize,style.leading) for style in styles]
    try:
        for style in styles:style.fontSize=11;style.leading=15
        student_pdf(lesson,path)
    finally:
        for style,(size,leading) in zip(styles,saved):style.fontSize=size;style.leading=leading

def md_table(headers,rows):
    def safe(s):return str(s).replace('|','/').replace('\n',' ')
    return '| '+' | '.join(map(safe,headers))+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+''.join('| '+' | '.join(map(safe,r))+' |\n' for r in rows)+'\n'

def md_student(lesson):
    s=f"# {lesson['level']} - {lesson['title']}\n\n{lesson['question']}\n\n**Durée : 55 minutes.** PC avec navigateur ; aucun compte ni accès Internet nécessaire après distribution du fichier.\n\n"
    if lesson['level']=='3e':
        s+='## Observer et légender le portail\n\n![Vue du portail à légender](documents/portail-eleve.svg)\n\nAssocier les repères 1 à 9 aux composants du tableau.\n\n'
    for i,page in enumerate(lesson['pages']):
        s+=f'## Partie {i+1}\n\n'
        for b in page:
            t=b['type']
            if t=='visual':s+='![Illustration pédagogique](documents/'+b['name']+'.svg)\n\n'
            elif t=='p':s+=b['text']+'\n\n'
            elif t=='h':s+='### '+b['text']+'\n\n'
            elif t in ('q','exit'):s+='**'+b['label']+'**\n\nRéponse :\n\n'
            elif t=='choice':s+='**'+b['label']+' :** '+', '.join(b['options'][1:])+'.\n\n'
            elif t=='table':s+=md_table(b['headers'],b['rows'])
            elif t=='answer_table':s+='**'+b['label']+'**\n\n'+md_table(b['headers'],[[(b['fixed'][r] if b.get('fixed') else '')]+['']*(len(b['headers'])-1) for r in range(b['rows'])])
            elif t=='diagram':s+='![Les deux chaînes fonctionnelles](documents/chaines-a-completer.svg)\n\n'
            elif t=='sim':s+='Ouvrir [l’activité numérique](activite-eleve.html) pour utiliser le laboratoire ; sur papier, appliquer la règle décrite pour prévoir le résultat.\n\n'
    return s

def md_teacher(lesson):
    s=f"# {lesson['level']} - Fiche professeur\n\n## {lesson['title']}\n\n**Durée de la séance : 55 minutes.**\n\n"
    s+='**Objectif :** '+lesson['objective']+'\n\n**Prérequis :** '+lesson['prerequisites']+'\n\n**Programme :** '+lesson['programme']+'\n\n'
    s+='## Support de réponse\n\nChoisir le papier OU le numérique pour les réponses, sans double saisie. Sur papier, utiliser les simulations sur PC et écrire dans la fiche. Sur PC, compléter les champs et télécharger le travail. Conserver la fiche papier dans le porte-vues.\n\n'
    s+='## Préparation\n\nDéposer `activite-eleve.html` sur les PC ou dans un espace de distribution habituel. Le fichier peut être copié par clé USB ou dossier partagé et ouvert par double-clic. Un PC par élève ou par binôme suffit. Les documents ne demandent aucun téléchargement pendant la séance. Vérifier une fois que le navigateur autorise l’ouverture du fichier et le téléchargement des réponses. Prévoir le fichier PDF en solution de repli.\n\n'
    s+='Les élèves téléchargent un fichier texte et le remettent par le canal habituel de la classe ; aucun envoi automatique ni compte n’est prévu. En binôme, alterner le clavier et demander deux billets de sortie distincts.\n\n'
    s+='## Déroulement\n\n'+md_table(['Temps','Étape','Conduite de séance'],lesson['timeline'])
    s+='## Critères de réussite\n\n'+''.join('- '+x+'\n' for x in lesson['success'])+'\n'
    s+='## Aides et points de vigilance\n\n'+''.join('- '+x+'\n' for x in lesson['aides'])+'\n'+lesson['vigilance']+'\n\n'
    s+='## Bilan et suite\n\n'+lesson['assessment']+'\n\nSuite possible : '+lesson['next']+'\n\n'
    s+='## Références\n\n'+''.join(f'- [{title}]({url})\n' for title,url in SOURCES)+'\n'
    return s

def md_correction(lesson):
    illustration='![Portail corrigé](documents/portail-corrige.svg)\n\n' if lesson['level']=='3e' else ''
    return '# '+lesson['level']+' - Corrigé\n\n'+illustration+''.join('## '+label+'\n\n'+answer+'\n\n' for label,answer in lesson['correction'])+'## Évaluation formative\n\n'+lesson['assessment']+'\n'

def guide_pdf(lesson,path):
    story=[P(lesson['level'].upper()+'  |  GUIDE PROFESSEUR','meta'),P(lesson['title'],'title'),P('Objectif : '+lesson['objective']),P('Séance de 55 minutes. Deux élèves par PC.'),P('Préparation','h'),P('Télécharger activite-eleve.html depuis le dossier de cette séquence et le distribuer aux élèves. Le fichier s’ouvre dans un navigateur. Distribuer uniquement les supports élèves ; ce guide et S01-corrige.md contiennent les réponses.'),P('En binôme, alterner le clavier et demander un bilan individuel à chaque élève. Faire télécharger les réponses avant de fermer la page, puis vérifier leur remise par le canal habituel.'),P('Choisir le papier ou le numérique comme support de réponse. Sur papier, les PC servent aux simulations ; éviter toute double saisie.'),P('Les documents imprimés sont conservés dans le porte-vues. Ne pas dépasser deux feuilles recto verso par élève et par séance.'),P('Prérequis : '+lesson['prerequisites']),P('Compétences','h'),P(lesson['programme']),PageBreak(),P('Déroulement de la séance','title'),table(['Temps','Étape','Action du professeur'],lesson['timeline'],[.7,1.05,3.35]),Spacer(1,8),P('Aides et différenciation','h')]
    story += [P(x,'small') for x in lesson['aides']]
    story += [P('Point de vigilance','h'),P(lesson['vigilance'],'small'),P('Suite possible : '+lesson['next'],'small'),PageBreak(),P('Réponses et critères de réussite','title')]
    for label,answer in lesson['correction']:
        story.append(P('<b>'+escape(label)+'</b> - '+escape(answer),'small',True))
    story += [P('Billet de sortie : barème facultatif','h'),P(lesson['assessment'])]
    if lesson['level']=='3e':
        story += [PageBreak()]+portal_page(True)
        story += [PageBreak(),P('Schéma de référence','title'),P('Deux chaînes qui coopèrent','h'),Chain(True),Spacer(1,12),P('La chaîne d’information envoie un ordre au bloc distribuer de la chaîne d’énergie. Les deux chaînes ont besoin d’énergie pour fonctionner. Les pertes et les alimentations des capteurs ne sont pas détaillées.')]
    story += [P('Références pédagogiques','h')]
    for title,url in SOURCES:
        story.append(P('<link href="'+escape(url,quote=True)+'" color="#175b9a">'+escape(title)+'</link>','small',True))
    story.append(P('Les documents et modèles techniques sont des créations pédagogiques simplifiées. Vérifier leur rattachement au programme applicable.','small'))
    build_pdf(path,story,lesson['level']+' - Guide professeur - '+lesson['title'])

def main():
    for lesson in LESSONS:
        folder=ROOT/lesson['level']/lesson['slug'];folder.mkdir(parents=True,exist_ok=True)
        for name,contents in [('activite-eleve.html',make_html(lesson)),('S01-eleve.md',md_student(lesson)),('S01-professeur.md',md_teacher(lesson)),('S01-corrige.md',md_correction(lesson))]:(folder/name).write_text(contents,encoding='utf-8')
        if lesson['level'] in ('5e','4e'):
            (folder/'documents').mkdir(exist_ok=True)
            visual='objets' if lesson['level']=='5e' else 'eclairage'
            (folder/'documents'/(visual+'.svg')).write_text(visual_svg(visual))
        if lesson['level']=='3e':
            (folder/'documents').mkdir(exist_ok=True)
            for corrected,filename in [(False,'portail-eleve.svg'),(True,'portail-corrige.svg')]:
                (folder/'documents'/filename).write_text(portal_svg(corrected),encoding='utf-8')
            (folder/'documents'/'chaines-a-completer.svg').write_text(diagram_svg(),encoding='utf-8')
        name=f"{lesson['level']}-fiche-eleve.pdf";pdf=OUT/name;student_pdf(lesson,pdf)
        (folder/'exports').mkdir(exist_ok=True);shutil.copyfile(pdf,folder/'exports'/name)
        guide=folder/'exports'/'guide-professeur.pdf'
        guide_pdf(lesson,guide)
        folder.joinpath('README.md').write_text(f"""# {lesson['level']} - {lesson['title']}

## Séquence : {lesson['title']}

{lesson['question']}

**Objectif :** {lesson['objective']}

| Séance | Durée | Supports élèves | Supports professeur |
| --- | --- | --- | --- |
| Séance 1 : étude et bilan | 55 minutes | [Activité numérique](activite-eleve.html) · [PDF élève](exports/{name}) · [Source modifiable](S01-eleve.md) | [Déroulement](S01-professeur.md) · [Corrigé](S01-corrige.md) · [Guide PDF](exports/guide-professeur.pdf) |

Pour utiliser l'activité HTML, télécharger le fichier puis l'ouvrir dans un navigateur. Deux élèves par PC ; chacun répond au bilan individuel. Télécharger les réponses avant de fermer la page.

Les PDF sont rangés dans `exports/` et les documents complémentaires dans `documents/` lorsqu'ils sont nécessaires.

[Autres séquences du niveau](../README.md) · [Accueil](../../README.md)
""",encoding='utf-8')
        if lesson['level']=='5e':
            adapted=guided_lesson(lesson)
            (folder/'activite-guidee.html').write_text(make_html(adapted))
            guided_student_pdf(adapted,folder/'exports'/'5e-parcours-guide.pdf')
            (folder/'S01-guide-corrige.md').write_text(md_correction(adapted))
            (folder/'S01-guide-eleve.md').write_text(md_student(adapted))
            (folder/'documents'/'lampe.svg').write_text(visual_svg('lampe'))
            index=folder/'README.md'
            index.write_text(index.read_text()+'\n## Parcours très guidé\n\nPour les élèves en grande difficulté : choisir ce parcours à la place du parcours ordinaire.\n\n- [Activité numérique guidée](activite-guidee.html)\n- [Fiche guidée à imprimer](exports/5e-parcours-guide.pdf)\n- [Corrigé du parcours guidé](S01-guide-corrige.md)\n- [Vue des objets](documents/objets.svg)\n')
        if lesson['level']=='4e':
            index=folder/'README.md'
            index.write_text(index.read_text()+'\n[Schéma de la commande de l’éclairage](documents/eclairage.svg)\n')
        if lesson['level']=='3e':
            index=folder/'README.md'
            index.write_text(index.read_text()+'\n## Vues du portail\n\n- [Vue élève à légender](documents/portail-eleve.svg)\n- [Vue du coffret corrigée](documents/portail-corrige.svg) ; légende complète dans le guide professeur.\n\nLa fiche élève comprend quatre pages, soit deux feuilles recto verso. La vue est intégrée à l’activité HTML, utilisable sans fichier image séparé.\n')
    print('Supports générés par niveau et par séquence, sans dates ni archives.')

if __name__=='__main__':main()
