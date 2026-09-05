"""Génère les supports Markdown, HTML et PDF pour la semaine du 7 septembre.

Exécution : python scripts/generer_semaine.py
Dépendance pour les PDF : reportlab. Les activités produites sont autonomes.
"""
from pathlib import Path
from html import escape
import json, shutil, zipfile, reportlab
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Flowable
from contenus_semaine import LESSONS, SOURCES
from activites import make_html, diagram_svg

ROOT=Path(__file__).resolve().parents[1]
WEEK=ROOT/'semaines'/'2026-09-07'
OUT=ROOT/'output'/'pdf'
BUNDLE=ROOT/'output'/'semaine-2026-09-07'
for path in (WEEK,OUT,BUNDLE): path.mkdir(parents=True,exist_ok=True)

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
        texts=['Bouton + cellule +\ncapteur de fin de course','Carte programmable','Liaison de commande'] if self.filled else ['Composant(s) ?']*3
        for x,title,detail in zip(topx,['ACQUÉRIR','TRAITER','COMMUNIQUER'],texts): self.box(x,top_y,topw,bh,title,detail,BLUE)
        for a,b in zip(topx,topx[1:]): self.arrow(a+topw,top_y+bh/2,b,top_y+bh/2,BLUE)
        c.setFillColor(ORANGE);c.drawString(0,bottom_y+bh+9,"CHAÎNE D'ÉNERGIE")
        bx=[0,131,262,393];bw=122
        texts=['Réseau + bloc\nd’alimentation 24 V','Module de puissance','Moteur électrique','Pignon + crémaillère'] if self.filled else ['Composant(s) ?']*4
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
    canvas.drawString(40,22,'Technologie - semaine du 7 au 11 septembre 2026')
    canvas.drawRightString(PAGE_W-40,22,f'{doc.page}')

def build_pdf(path,story,title):
    doc=SimpleDocTemplate(str(path),pagesize=A4,leftMargin=40,rightMargin=40,topMargin=35,bottomMargin=44,title=title,author='Ressources pédagogiques - Technologie',pageCompression=1)
    doc.build(story,onFirstPage=header,onLaterPages=header)

def student_block(b):
    typ=b['type']
    if typ=='p':return [P(b['text'])]
    if typ=='h':return [P(b['text'],'h')]
    if typ=='q':return [P(b['label'],'q'),AnswerLines(b['lines'])]
    if typ=='exit':return [P(b['label'],'q'),AnswerLines(b['lines'])]
    if typ=='choice':return [P(b['label']+' : ______________________________________','q')]
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

def student_pdf(lesson,path):
    story=[]
    for i,page in enumerate(lesson['pages']):
        if i:story.append(PageBreak())
        story.append(P(f"{lesson['level'].upper()}  |  SÉANCE 1  |  FICHE ÉLÈVE  |  {i+1}/{len(lesson['pages'])}",'meta'))
        if i==0:
            story += [P(lesson['title'],'title'),P(lesson['question']),P('Nom : __________________________  Classe : __________  Date : __________','small')]
        for b in page:story+=student_block(b)
    build_pdf(path,story,lesson['level']+' - '+lesson['title'])

def md_table(headers,rows):
    def safe(s):return str(s).replace('|','/').replace('\n',' ')
    return '| '+' | '.join(map(safe,headers))+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+''.join('| '+' | '.join(map(safe,r))+' |\n' for r in rows)+'\n'

def md_student(lesson):
    s=f"# {lesson['level']} - {lesson['title']}\n\n{lesson['question']}\n\n**Durée : 55 minutes.** PC avec navigateur ; aucun compte ni accès Internet nécessaire après distribution du fichier.\n\n"
    for i,page in enumerate(lesson['pages']):
        s+=f'## Partie {i+1}\n\n'
        for b in page:
            t=b['type']
            if t=='p':s+=b['text']+'\n\n'
            elif t=='h':s+='### '+b['text']+'\n\n'
            elif t in ('q','exit'):s+='**'+b['label']+'**\n\nRéponse :\n\n'
            elif t=='choice':s+='**'+b['label']+' :** '+', '.join(b['options'][1:])+'.\n\n'
            elif t=='table':s+=md_table(b['headers'],b['rows'])
            elif t=='answer_table':s+='**'+b['label']+'**\n\n'+md_table(b['headers'],[[(b['fixed'][r] if b.get('fixed') else '')]+['']*(len(b['headers'])-1) for r in range(b['rows'])])
            elif t=='diagram':s+='![Les deux chaînes fonctionnelles](documents/chaines-a-completer.svg)\n\n'
            elif t=='sim':s+='Ouvrir [l’activité numérique](activite-eleve.html) pour utiliser le laboratoire ; sur papier, appliquer la règle décrite pour prévoir le résultat.\n\n'
    return s

def md_teacher(lesson):
    s=f"# {lesson['level']} - Fiche professeur\n\n## {lesson['title']}\n\n**55 minutes ; une séance pour la semaine du 7 au 11 septembre 2026.**\n\n"
    s+='**Objectif :** '+lesson['objective']+'\n\n**Prérequis :** '+lesson['prerequisites']+'\n\n**Programme :** '+lesson['programme']+'\n\n'
    s+='## Préparation\n\nDéposer `activite-eleve.html` sur les PC ou dans un espace de distribution habituel. Le fichier peut être copié par clé USB ou dossier partagé et ouvert par double-clic. Un PC par élève ou par binôme suffit. Les documents ne demandent aucun téléchargement pendant la séance. Vérifier une fois que le navigateur autorise l’ouverture du fichier et le téléchargement des réponses. Prévoir le fichier PDF en solution de repli.\n\n'
    s+='Les élèves téléchargent un fichier texte et le remettent par le canal habituel de la classe ; aucun envoi automatique ni compte n’est prévu. En binôme, alterner le clavier et demander deux billets de sortie distincts.\n\n'
    s+='## Déroulement\n\n'+md_table(['Temps','Étape','Conduite de séance'],lesson['timeline'])
    s+='## Critères de réussite\n\n'+''.join('- '+x+'\n' for x in lesson['success'])+'\n'
    s+='## Aides et points de vigilance\n\n'+''.join('- '+x+'\n' for x in lesson['aides'])+'\n'+lesson['vigilance']+'\n\n'
    s+='## Bilan et suite\n\n'+lesson['assessment']+'\n\nSuite possible : '+lesson['next']+'\n\n'
    s+='## Références\n\n'+''.join(f'- [{title}]({url})\n' for title,url in SOURCES)+'\n'
    return s

def md_correction(lesson):
    return '# '+lesson['level']+' - Corrigé\n\n'+''.join('## '+label+'\n\n'+answer+'\n\n' for label,answer in lesson['correction'])+'## Évaluation formative\n\n'+lesson['assessment']+'\n'

def guide_pdf(path):
    story=[P('TECHNOLOGIE  |  GUIDE PROFESSEUR','meta'),P('Trois séances prêtes pour la semaine','title'),P('Du 7 au 11 septembre 2026 - 5e, 4e et 3e - 55 minutes par niveau'),P('PC uniquement. Les trois activités numériques sont autonomes : un navigateur suffit. Aucun compte, logiciel spécialisé ou connexion Internet n’est nécessaire une fois les fichiers distribués.'),table(['Niveau','Séance','Production attendue'],[[x['level'],x['title'],x['objective']] for x in LESSONS],[.5,1.5,2.4]),Spacer(1,12),P('Avant le premier cours','h')]
    for text in [
        'Extraire le dossier ZIP. Dans eleves/, copier le fichier HTML du niveau sur les PC, ou le distribuer dans un dossier partagé. Un double-clic ouvre l’activité dans le navigateur.',
        'Distribuer seulement le fichier du niveau concerné aux élèves. Le dossier professeur/ contient les corrigés. Le dépôt GitHub étant public, ses corrigés sont également accessibles publiquement.',
        'Prévoir un PC par élève ou par binôme. À deux, faire alterner le clavier ; la case de travail en binôme fait apparaître un second bilan individuel.',
        'En fin de séance, faire cliquer sur « Télécharger mes réponses », puis vérifier la remise du fichier texte par le canal habituel. La page ne transmet rien automatiquement et ne conserve pas de réponse après fermeture.',
        'Les PDF élèves constituent une solution de repli et peuvent être imprimés. Le guide fournit les réponses et un barème facultatif pour le billet de sortie.',
    ]:story.append(P(text))
    story+=[P('Hypothèses retenues','h'),P('Aucun prérequis logiciel spécialisé ; une séance introductive par niveau ; priorité aux chaînes d’information et d’énergie pour les 3e. Si le créneau ne dure que 50 minutes, réduire la mise en commun de 5 minutes en conservant le bilan individuel.')]
    for lesson in LESSONS:
        story += [PageBreak(),P(lesson['level'].upper()+'  |  DÉROULEMENT','meta'),P(lesson['title'],'title'),P('Objectif : '+lesson['objective']),P('Prérequis : '+lesson['prerequisites'],'small'),table(['Temps','Étape','Action du professeur'],lesson['timeline'],[.7,1.05,3.35]),Spacer(1,8),P('Aides et différenciation','h')]
        story += [P(x,'small') for x in lesson['aides']]
        story += [P('Point de vigilance','h'),P(lesson['vigilance'],'small'),P('Suite possible : '+lesson['next'],'small'),PageBreak(),P(lesson['level'].upper()+'  |  CORRIGÉ','meta'),P('Réponses et critères de réussite','title')]
        for label,answer in lesson['correction']:
            story.append(P('<b>'+escape(label)+'</b> - '+escape(answer),'small',True))
        story += [P('Billet de sortie : barème facultatif','h'),P(lesson['assessment'])]
    story += [PageBreak(),P('3e  |  SCHÉMA DE RÉFÉRENCE','meta'),P('Deux chaînes qui coopèrent','title'),Chain(True),Spacer(1,12),P('Lire le schéma','h'),P('La chaîne d’information envoie un ordre au bloc distribuer de la chaîne d’énergie. Les deux chaînes ont besoin d’énergie pour fonctionner : elles sont distinguées selon les fonctions étudiées. Les pertes d’énergie et les alimentations des capteurs ne sont pas détaillées.'),P('Rattachement pédagogique','h')]
    for lesson in LESSONS:story.append(P(lesson['level']+' : '+lesson['programme'],'small'))
    story += [P('Sources officielles consultées le 5 septembre 2026','h')]
    for title,url in SOURCES:story.append(P('<link href="'+escape(url,quote=True)+'" color="#175b9a">'+escape(title)+'</link>','small',True))
    story.append(P('Les contextes techniques, tableaux, questions, simulations et schémas de ce dossier sont des créations pédagogiques originales. Les modèles sont simplifiés et ne décrivent pas un produit commercial précis.','small'))
    build_pdf(path,story,'Guide professeur - Technologie - 7 septembre 2026')

def main():
    (BUNDLE/'eleves').mkdir(parents=True,exist_ok=True);(BUNDLE/'professeur').mkdir(exist_ok=True)
    for lesson in LESSONS:
        folder=ROOT/lesson['level']/('S01-'+lesson['slug']);folder.mkdir(parents=True,exist_ok=True)
        for name,contents in [('activite-eleve.html',make_html(lesson)),('S01-eleve.md',md_student(lesson)),('S01-professeur.md',md_teacher(lesson)),('S01-corrige.md',md_correction(lesson))]:(folder/name).write_text(contents,encoding='utf-8')
        if lesson['level']=='3e':
            (folder/'documents').mkdir(exist_ok=True);(folder/'documents'/'chaines-a-completer.svg').write_text(diagram_svg(),encoding='utf-8')
        name=f"{lesson['level']}-fiche-eleve.pdf";pdf=OUT/name;student_pdf(lesson,pdf)
        (folder/'exports').mkdir(exist_ok=True);shutil.copyfile(pdf,folder/'exports'/name)
        shutil.copyfile(pdf,BUNDLE/'eleves'/name);shutil.copyfile(folder/'activite-eleve.html',BUNDLE/'eleves'/(lesson['level']+'-activite.html'))
        shutil.copyfile(folder/'S01-professeur.md',BUNDLE/'professeur'/(lesson['level']+'-professeur.md'));shutil.copyfile(folder/'S01-corrige.md',BUNDLE/'professeur'/(lesson['level']+'-corrige.md'))
        folder.joinpath('README.md').write_text(f"# {lesson['level']} - {lesson['title']}\n\nPremière séance de 55 minutes, prévue pour la semaine du 7 au 11 septembre 2026.\n\n{lesson['question']}\n\n- [Activité élève autonome sur PC](activite-eleve.html) : télécharger le fichier, puis l'ouvrir dans le navigateur. GitHub affiche son code lorsque l'on clique directement dessus.\n- [Fiche élève imprimable](exports/{name})\n- [Fiche élève modifiable](S01-eleve.md)\n- [Déroulement professeur](S01-professeur.md)\n- [Corrigé](S01-corrige.md)\n\nMatériel : un PC par élève ou binôme. Tous les documents nécessaires sont inclus. Les élèves téléchargent leurs réponses en texte puis les remettent au professeur.\n\n[Vue d'ensemble de la semaine](../../semaines/2026-09-07/README.md)\n",encoding='utf-8')
    guide=OUT/'guide-professeur.pdf';guide_pdf(guide);shutil.copyfile(guide,BUNDLE/'professeur'/'guide-professeur.pdf');shutil.copyfile(guide,WEEK/'guide-professeur.pdf')
    readme="""# Séances de technologie - semaine du 7 au 11 septembre 2026

Une séance de 55 minutes pour chaque niveau, avec uniquement des PC.

## Utilisation immédiate

1. Extraire ce dossier ZIP.
2. Ouvrir le guide professeur dans professeur/ pour le déroulement et les corrigés.
3. Distribuer le fichier HTML du niveau, situé dans eleves/. Un double-clic l'ouvre dans un navigateur ; aucun compte ni installation n'est nécessaire.
4. Les élèves complètent les cases et cliquent sur « Télécharger mes réponses ». Ils remettent ensuite le fichier texte par le canal habituel. Aucune réponse n'est envoyée automatiquement. Télécharger avant de fermer la page.
5. À deux sur un PC, cocher le travail en binôme, alterner le clavier et répondre chacun au bilan individuel.

Les PDF élèves peuvent être imprimés. Ne distribuer aux élèves que leur activité ; le dossier professeur/ contient les corrigés.

## Séances

- 5e : Un objet, un besoin, des solutions. Choisir un objet, identifier ses composants et justifier une amélioration.
- 4e : Allumer seulement quand c'est utile. Tester une règle avec OU, la corriger avec ET et vérifier le cas limite.
- 3e : Un portail, deux chaînes. Étudier les chaînes d'information et d'énergie d'un portail automatique.

Le navigateur conserve les réponses uniquement tant que la page reste ouverte. Les simulations ne nécessitent pas Internet. Les modèles techniques sont volontairement simplifiés.
"""
    (BUNDLE/'LIRE-MOI.md').write_text(readme,encoding='utf-8')
    index='# Semaine du 7 au 11 septembre 2026\n\nTrois premières séances de 55 minutes, utilisables avec des PC uniquement.\n\n'
    index+=md_table(['Niveau','Séance et documents','Priorité'],[[x['level'],f"[{x['title']}](../../{x['level']}/S01-{x['slug']}/README.md)",x['objective']] for x in LESSONS])
    index+='[Télécharger le dossier complet](seances-technologie-2026-09-07.zip) · [Guide professeur](guide-professeur.pdf)\n\n'+readme.split('## Utilisation immédiate',1)[1]
    (WEEK/'README.md').write_text(index,encoding='utf-8')
    archive=ROOT/'output'/'seances-technologie-2026-09-07.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for path in sorted(BUNDLE.rglob('*')):
            if path.is_file():z.write(path,Path('semaine-2026-09-07')/path.relative_to(BUNDLE))
    shutil.copyfile(archive,WEEK/archive.name)
    print(json.dumps({'pdfs':[str(OUT/(x['level']+'-fiche-eleve.pdf')) for x in LESSONS]+[str(guide)],'zip':str(archive)},ensure_ascii=False))

if __name__=='__main__':main()
