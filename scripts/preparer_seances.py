"""Révision compacte : exécuter python scripts/preparer_seances.py."""
from pathlib import Path
import shutil, zipfile
from pypdf import PdfReader, PdfWriter
import generer_supports as g
from introductions import Illustration
P,T=g.P,g.table
PB=g.PageBreak
ROOT=g.ROOT

def title(level,text):
    return [P(level+' | TECHNOLOGIE | À CONSERVER DANS LE PORTE-VUES','meta'),P(text,'title'),P('Nom : __________________________  Classe : __________','small')]

def bilan(text):
    return [P('Bilan individuel - sans aide','h'),P(text),g.AnswerLines(2)]

def base():
    for lesson in g.LESSONS:
        lesson['prerequisites'] += ' La classe a déjà étudié les réseaux, la programmation avec mBot et la modélisation 3D avec SketchUp ou Sweet Home 3D.'
        lesson['aides'].insert(0,'Deux élèves par PC : un pilote manipule, un lecteur vérifie et explique. Inverser les rôles vers la 24e minute ; chacun répond à son bilan individuel.')
    g.LESSONS[0]['aides'].insert(0,'Pour les deux élèves ayant besoin d’un guidage renforcé : remplacer l’activité numérique par 5e-parcours-guide.pdf. Un seul objet, lecture orale des consignes, pointage et choix à cocher. Voir le protocole du guide.')
    g.main()

base()
B=g.BUNDLE
# Livret complet : les cours et les traces tiennent ensemble sur un recto verso.
s=title('5e','Comprendre un objet technique')
s += [P('Avant l’activité : observer et nommer','h'),P('Un objet technique est conçu et fabriqué par des êtres humains pour répondre à un besoin.'),Illustration('bag'),T(['Notion','Ce qu’elle signifie','Exemple'],[
['Besoin','Une nécessité ou une attente.','Transporter des affaires.'],['Fonction d’usage','Le service rendu par l’objet.','Permettre de transporter ses affaires scolaires.'],['Composant','Une pièce ou un élément.','Une bretelle.'],['Matériau','La matière d’un composant.','Le tissu de polyester du modèle.'],['Contrainte','Une exigence à respecter.','Résister au poids des affaires.']],[1,1.6,1.6]),P('À l’oral : la poignée est-elle un composant ou un matériau ? À quoi sert-elle ?','h'),P('Les matériaux sont des données du modèle étudié : une image seule ne permet pas de les identifier avec certitude.','small'),PB()]
s += title('5e','Analyser et justifier')
s += [P('Sur PC : travailler à deux','h'),P('Ouvrez 5e-activite.html. Choisissez un objet et lisez sa fiche. Répondez aux questions 1 à 5. Le pilote utilise le clavier ; le lecteur vérifie la fiche et explique les réponses. Inversez les rôles au signal du professeur.'),T(['Étape','Question à se poser'],[['1. Identifier','À qui sert l’objet ? Quel besoin satisfait-il ?'],['2. Décrire','Quelle pièce ? Quel rôle ? Quel matériau ?'],['3. Justifier','Quelle contrainte ? Quelle solution permet de la respecter ?'],['4. Améliorer','Pour quel utilisateur ? Avec quel intérêt et quelle limite ?']],[1,3]),P('Après la correction : l’essentiel','h'),P('La fonction d’usage indique le service rendu. Les composants sont les éléments de l’objet ; les matériaux sont les matières qui les constituent. Les choix de conception doivent respecter des contraintes : résistance, sécurité, masse, coût… Une amélioration se justifie par un besoin précis.'),P('Exemple : élargir les bretelles peut mieux répartir l’appui sur les épaules. Cela peut aussi augmenter leur encombrement.'),P('Lien avec la modélisation 3D','h'),P('Avec SketchUp ou Sweet Home 3D, modifier une dimension doit servir un usage : prévoir une largeur de passage suffisante, par exemple. Une forme n’est pas seulement un choix esthétique.')]
s += bilan('Un casque protège la tête. Donne sa fonction d’usage, puis un composant et un matériau possible pour ce composant.')
s += [P('Sur PC : enregistrez les réponses du binôme avant de fermer le navigateur. Le bilan ci-dessus se fait individuellement sur papier.','small')]
g.build_pdf(g.OUT/'5e-cours-et-bilan.pdf',s,'5e - Comprendre un objet technique')

s=title('4e','Commander avec des conditions')
s += [P('Avant l’activité : retrouver ce que fait mBot','h'),P('Un capteur fournit une information. Le programme la traite et commande un actionneur. Dans mBot, les moteurs sont des actionneurs : ils convertissent l’énergie électrique en mouvement.'),P('Une condition est une affirmation vraie ou fausse : par exemple « luminosité < 30 ». À 29, elle est vraie ; à 30, elle est fausse.'),Illustration('logic'),T(['A','B','A ET B','A OU B'],[['Faux','Faux','Faux','Faux'],['Faux','Vrai','Faux','Vrai'],['Vrai','Faux','Faux','Vrai'],['Vrai','Vrai','Vrai','Vrai']]),P('ET : les deux conditions sont vraies. OU : au moins une est vraie, y compris si les deux sont vraies.'),P('SI une condition est vraie ALORS réaliser une action SINON réaliser l’autre action. Le programme réévalue régulièrement les informations.'),P('À l’oral : badge valide et code incorrect. Quelle règle autorise l’accès : ET ou OU ?','h'),PB()]
s += title('4e','Tester et corriger une règle')
s += [P('Sur PC : prouver l’erreur puis la corriger','h'),P('Ouvrez 4e-activite.html. Traitez Q1 à Q5. Prévoyez les résultats, testez les cinq situations avec la règle OU, puis corrigez et recommencez. Inversez les rôles à mi-activité. Q6 et le défi sont facultatifs.'),P('Après la correction : la règle à conserver','h'),P('Répéter en continu : SI luminosité < 30 ET présence détectée ALORS allumer la lampe SINON éteindre la lampe.'),Illustration('light_rule'),T(['Luminosité','Présence','Lampe avec ET'],[['10','Non','Éteinte'],['29','Oui','Allumée'],['30','Oui','Éteinte'],['80','Oui','Éteinte']]),P('Tester un programme permet de vérifier qu’il répond au besoin. Un seul contre-exemple suffit à montrer qu’une règle est incorrecte. Toujours tester les valeurs limites.'),P('Ici, la luminosité est un indice de 0 à 100, pas une mesure en lux. Le simulateur ne comporte pas de temporisation.','small')]
s += bilan('Avec luminosité = 30 et présence détectée, la lampe s’allume-t-elle si le seuil reste 30 ? Justifie avec le signe <.')
g.build_pdf(g.OUT/'4e-cours-et-bilan.pdf',s,'4e - Commander avec des conditions')

s=title('3e','Information et énergie')
s += [P('Avant l’activité : deux rôles différents','h'),P('La chaîne d’information recueille et traite des informations, puis communique des ordres. La chaîne d’énergie fournit et transforme l’énergie nécessaire à l’action. Comme sur mBot, le capteur informe ; le moteur agit.'),Illustration('lamp_chains'),T(['Chaîne','Fonction','Rôle'],[['Information','ACQUÉRIR','Recueillir une mesure ou une demande.'],['Information','TRAITER','Appliquer un programme pour décider.'],['Information','COMMUNIQUER','Transmettre une information ou un ordre.'],['Énergie','ALIMENTER','Fournir l’énergie sous une forme adaptée.'],['Énergie','DISTRIBUER','Autoriser ou régler son transfert.'],['Énergie','CONVERTIR','Transformer une forme d’énergie en une autre.'],['Énergie','TRANSMETTRE','Acheminer l’énergie ou le mouvement.']],[.85,1.2,2.5]),P('Dans ce modèle d’éclairage, on ne distingue pas de bloc TRANSMETTRE après la LED. L’énergie électrique devient lumière et chaleur. Le détecteur ne fournit pas l’énergie qui éclaire.','small'),PB()]
s += title('3e','Un portail, deux chaînes')
s += [P('Sur PC : appliquer au portail','h'),P('Ouvrez 3e-activite.html. Lisez les documents, associez chaque composant à sa fonction et analysez une panne. Inversez les rôles à mi-activité. Le professeur précise les questions prioritaires.'),P('Après la correction : schéma de référence','h'),g.Chain(True),P('Énergie électrique : de l’alimentation au moteur. Énergie mécanique : du moteur au pignon et à la crémaillère, puis au portail. Les flèches d’information transportent des signaux et des ordres.','small'),P('Ce qu’il faut retenir','h'),P('L’ordre issu de la chaîne d’information arrive au bloc DISTRIBUER. Le moteur est un actionneur : il convertit l’énergie électrique en énergie mécanique. Les capteurs et la carte consomment aussi de l’énergie, mais on les classe ici selon leur rôle d’acquisition ou de traitement.'),P('Une fonction décrit ce qui est fait ; un composant est la solution matérielle qui assure cette fonction. Le modèle ne détaille pas toutes les alimentations ni les pertes d’énergie.')]
s += bilan('Donne un capteur du portail et sa fonction. Explique ce que convertit le moteur et où arrive l’ordre de commande.')
g.build_pdf(g.OUT/'3e-cours-et-bilan.pdf',s,'3e - Chaînes d’information et d’énergie')

# Parcours différencié, titre neutre pour les élèves.
s=title('5e','Mon parcours guidé : le cartable')
s += [P('1. Observe le cartable','h'),Illustration('bag'),P('2. Coche une seule réponse','h'),P('Le cartable sert à :<br/>[  ] transporter des affaires &nbsp;&nbsp; [  ] éclairer une pièce','body',True),g.Spacer(1,15),P('3. Relie chaque pièce à son rôle','h'),T(['Pièce','Trace les liens','Rôle'],[['Poignée','','Ouvrir et fermer'],['Bretelle','','Prendre le sac à la main'],['Fermeture','','Porter le sac sur l’épaule']],[1,1,1.5]),P('Tu peux suivre les traits avec ton doigt avant de les tracer.','small'),P('4. Entoure les deux pièces','h'),P('bretelle &nbsp;&nbsp;&nbsp; tissu &nbsp;&nbsp;&nbsp; poignée','body',True),PB()]
s += title('5e','Pièce et matière')
s += [P('5. Lis avec de l’aide si nécessaire','h'),P('Dans notre modèle, la bretelle est en tissu.<br/><b>Bretelle = pièce.</b><br/><b>Tissu = matière.</b>','body',True),P('Complète avec : bretelle - tissu'),P('La pièce s’appelle : ________________________'),P('Sa matière est le : ________________________'),g.Spacer(1,18),P('6. Choisis une amélioration utile','h'),P('Le sac est inconfortable sur les épaules. Coche la solution utile.<br/><br/>[  ] Des bretelles plus larges et rembourrées.<br/><br/>[  ] Un dessin d’étoile sur la poche.','body',True),P('Explique ton choix à l’oral au professeur.','small'),g.Spacer(1,18),P('Mon cours à conserver','h'),P('<b>Un objet technique rend un service.</b><br/>Le cartable permet de transporter des affaires.<br/>Une <b>pièce</b> est une partie de l’objet : la bretelle.<br/>Une <b>matière</b> sert à fabriquer une pièce : le tissu.','body',True),P('Je vérifie seul','h'),P('Entoure une pièce : &nbsp;&nbsp; poignée &nbsp;&nbsp; tissu','body',True),P('Coche une matière : &nbsp;&nbsp; [  ] fermeture &nbsp;&nbsp; [  ] tissu','body',True)]
g.build_pdf(g.OUT/'5e-parcours-guide.pdf',s,'5e - Mon parcours guidé')

intro=[P('TECHNOLOGIE | MODE D’EMPLOI','meta'),P('Préparer et distribuer','title'),P('Trois séances de 55 minutes. Rythme déclaré : 1 h 30 par semaine. Ces supports couvrent une séance par niveau ; le complément hebdomadaire dépend de l’emploi du temps réel.'),T(['Niveau','À imprimer par élève','À garder sur PC'],[['5e','5e-cours-et-bilan.pdf : 2 pages','5e-activite.html'],['5e, parcours guidé','5e-parcours-guide.pdf : 2 pages, à la place du livret standard','Image à observer si utile'],['4e','4e-cours-et-bilan.pdf : 2 pages','4e-activite.html'],['3e','3e-cours-et-bilan.pdf : 2 pages','3e-activite.html']],[1,2,1.4]),P('Impression : une feuille A4 recto verso par élève. Ne pas ajouter les anciennes fiches d’activité ni les cours AVANT/APRÈS : le nouveau livret les remplace pour l’impression. Les activités longues restent numériques.'),P('Déroulement commun','h'),T(['Temps','Action'],[['0-5 min','Accroche, lien avec mBot ou la modélisation.'],['5-12 min','Cours explicite sur la première page.'],['12-37 min','Activité à deux par PC ; inversion des rôles vers 24 min.'],['37-47 min','Correction collective des exercices essentiels.'],['47-52 min','Lire et annoter la synthèse au verso, ranger au porte-vues.'],['52-55 min','Bilan individuel sur papier et sauvegarde numérique.']],[1,3]),P('Le verso contient la synthèse corrigée : demander de rester au recto jusqu’à la mise en commun. Les dernières réponses individuelles se font sur papier, sans recopier le même bilan dans le HTML. Anticiper la sauvegarde dès la 50e minute si elle prend du temps.'),PB(),P('5e | ACCOMPAGNEMENT','meta'),P('Un parcours vraiment accessible','title'),P('Objectifs : identifier le service rendu, reconnaître une pièce et distinguer pièce/matière. La contrainte et l’amélioration sont abordées par un choix concret ; aucune définition abstraite à mémoriser.'),P('Organisation','h'),P('Distribuer uniquement le parcours guidé aux deux élèves. Elles suivent l’accroche commune puis avancent à leur rythme. Ne pas les obliger à terminer aussi l’activité standard. Elles peuvent travailler sur papier et observer leur propre sac, ou l’image sur PC.'),T(['Temps','Aide prévue'],[['12-17 min','Lire la question 2, laisser pointer puis cocher.'],['17-25 min','Montrer une pièce à la fois ; faire dire son rôle avant de relier.'],['25-32 min','Reprendre pièce/matière avec une vraie bretelle. Une consigne à la fois.'],['32-37 min','Choix d’amélioration puis explication orale courte.'],['Correction','Valoriser une association correcte ; lire le cours avec elles.'],['Bilan','Lire les mots si nécessaire, sans désigner la bonne réponse.']],[1,3]),P('Corrigé du parcours','h'),P('2 : transporter des affaires. 3 : poignée / prendre à la main ; bretelle / porter sur l’épaule ; fermeture / ouvrir et fermer. 4 : bretelle et poignée. 5 : bretelle ; tissu. 6 : bretelles plus larges et rembourrées. Bilan : poignée ; tissu.'),P('Critères observables','h'),P('L’élève reconnaît le service rendu, associe au moins deux pièces à leur rôle et distingue une pièce de sa matière. Une réponse orale ou pointée est recevable ; ne pas pénaliser l’orthographe.'),P('Les pages suivantes donnent les scripts et les corrigés détaillés. Pour le bilan papier de 4e : lampe éteinte, car 30 n’est pas strictement inférieur à 30. Pour le bilan de 3e : cellule ou fin de course / acquérir ; énergie électrique vers mécanique ; ordre vers distribuer.'),P('Illustration du cartable : générée par IA, sans marque, pour observer les pièces. Les matériaux sont fournis comme données du modèle ; ils ne sont pas déduits de l’image. Schémas fonctionnels originaux.','small')]
g.build_pdf(g.OUT/'mode-emploi.pdf',intro,'Guide - Organisation et différenciation')
w=PdfWriter()
for p in [g.OUT/'mode-emploi.pdf',g.OUT/'guide-professeur.pdf']:
    w.append(str(p), pages=(1,len(PdfReader(p).pages)) if p.name=='guide-professeur.pdf' else None)
from io import BytesIO
from reportlab.pdfgen import canvas
for i,page in enumerate(w.pages):
    buf=BytesIO();c=canvas.Canvas(buf,pagesize=g.A4)
    c.setFillColor(g.colors.white);c.rect(480,15,80,15,fill=1,stroke=0)
    c.setFont('Lesson',8);c.setFillColor(g.INK);c.drawRightString(g.PAGE_W-40,22,str(i+1));c.save()
    page.merge_page(PdfReader(buf).pages[0])
with open(g.OUT/'guide-professeur-revise.pdf','wb') as f:w.write(f)
# Dossier de distribution sans doublons imprimables.
DEST=ROOT/'output'/'seances-technologie'
for sub in ['a-imprimer','activites-numeriques','professeur','sources']:(DEST/sub).mkdir(parents=True,exist_ok=True)
for name in ['5e-cours-et-bilan.pdf','4e-cours-et-bilan.pdf','3e-cours-et-bilan.pdf','5e-parcours-guide.pdf']:
    shutil.copyfile(g.OUT/name,DEST/'a-imprimer'/name)
for lev in ['5e','4e','3e']:shutil.copyfile(B/'eleves'/f'{lev}-activite.html',DEST/'activites-numeriques'/f'{lev}-activite.html')
shutil.copyfile(g.OUT/'guide-professeur-revise.pdf',DEST/'professeur'/'guide-professeur.pdf')
for p in (B/'professeur').glob('*.md'):shutil.copyfile(p,DEST/'professeur'/p.name)
for p in (ROOT/'scripts').glob('*.py'):shutil.copyfile(p,DEST/'sources'/p.name)
(DEST/'sources'/'ressources/images').mkdir(parents=True,exist_ok=True)
shutil.copyfile(ROOT/'ressources/images/cartable.png',DEST/'sources/ressources/images/cartable.png')
(DEST/'LIRE-MOI.md').write_text('''# Séances de technologie

Une séance de 55 minutes par niveau. Deux élèves par PC. Documents sans date de séance.

## À imprimer

- 5e : `a-imprimer/5e-cours-et-bilan.pdf`, une feuille recto verso par élève.
- Pour les deux élèves accompagnées : `a-imprimer/5e-parcours-guide.pdf` à la place du livret standard, une feuille recto verso.
- 4e et 3e : le fichier cours-et-bilan du niveau, une feuille recto verso.
- Les élèves rangent ce support au porte-vues. Les bilans individuels se font dessus.

## Sur les PC

Ouvrir le HTML du niveau dans `activites-numeriques`. Les documents et simulateurs sont inclus. Cocher le mode binôme ; alterner le clavier. Télécharger les réponses avant fermeture puis remettre le fichier par le canal habituel. Pas d’envoi automatique. Les bilans individuels sont déjà sur papier : ne pas les recopier au clavier.

Consulter `professeur/guide-professeur.pdf` : organisation, accompagnement, scripts et corrigés détaillés.

La synthèse se trouve au verso : demander de rester au recto avant la correction. Conserver le dossier professeur hors du dossier distribué aux élèves.

## Sources modifiables

Les scripts Python sont dans sources/. Pour régénérer, placer les cinq scripts dans un sous-dossier scripts/ et conserver ressources/images/cartable.png à côté de ce sous-dossier. Installer reportlab et pypdf, puis exécuter python scripts/preparer_seances.py. Les fichiers Markdown des explications et corrigés sont dans professeur/.

L’illustration réaliste du cartable a été créée avec ImageGen (IA), sur fond blanc, sans texte ni marque, pour montrer poignée, bretelles et fermeture. Les schémas sont vectoriels et les modèles techniques simplifiés. Les matériaux ne sont pas déduits de la seule image.
''')
archive=ROOT/'output'/'seances-technologie.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(DEST.rglob('*')):
        if p.is_file():z.write(p,Path('seances-technologie')/p.relative_to(DEST))
for p in (DEST/'a-imprimer').glob('*.pdf'):
    n=len(PdfReader(p).pages)
    assert n==2,(p,n)
    print(p.name,n)
print(archive)
