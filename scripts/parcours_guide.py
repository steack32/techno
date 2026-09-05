"""Parcours très guidé de 5e : une lampe, des choix simples, une idée à retenir."""
from copy import deepcopy

def guided_lesson(base):
 x=deepcopy(base);x['guided']=True;x['title']='Une lampe pour éclairer';x['objective']='Dire à quoi sert la lampe et distinguer une pièce de son matériau.'
 x['question']='À quoi sert une lampe de bureau ?'
 x['pages']=[[
  {'type':'visual','name':'lampe'},
  {'type':'p','text':'La lampe éclaire le bureau. Le socle, en acier, maintient la lampe debout. La coque, en plastique, protège les éléments. Le diffuseur, en plastique translucide, répartit la lumière.'},
  {'type':'choice','id':'usage','label':'1. La lampe permet de','options':['Choisir','éclairer le bureau','déplacer une personne','mettre l’air en mouvement']},
  {'type':'choice','id':'piece','label':'2. Quelle pièce maintient la lampe debout ?','options':['Choisir','le diffuseur','le socle','la coque']},
  {'type':'choice','id':'matiere','label':'3. Le socle est fabriqué en','options':['Choisir','acier','papier','caoutchouc']},
  {'type':'choice','id':'amelioration','label':'4. La lampe tombe facilement. Quelle amélioration choisir ?','options':['Choisir','un socle plus large','une couleur différente']},
  {'type':'p','text':'À retenir : un composant est une pièce, par exemple le socle. Un matériau est la matière de cette pièce, par exemple l’acier.'},
  {'type':'exit','id':'bilan','label':'5. Complète : la lampe permet d’__________. Le socle est une __________. L’acier est un __________.','lines':2},
 ]]
 x['correction']=[['Parcours guidé','1. Éclairer le bureau. 2. Le socle. 3. Acier. 4. Un socle plus large. 5. Éclairer ; pièce (ou composant) ; matériau.']]
 return x
