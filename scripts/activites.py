"""Génération des fiches interactives autonomes, sans dépendance réseau."""
from html import escape as esc
import json
from portail import portal_svg, COMPONENTS

CSS = '''
:root{--ink:#16283e;--blue:#175b9a;--energy:#b65b12;--line:#cfdae5;--paper:#fff;--bg:#edf2f6}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 Arial,sans-serif}
main{max-width:1000px;margin:26px auto;padding:30px 38px;background:var(--paper);border-top:8px solid var(--blue)}
header{border-bottom:1px solid var(--line);padding-bottom:20px;margin-bottom:24px}.meta{font-size:14px;font-weight:bold;letter-spacing:.06em;color:var(--blue)}
h1{font-size:30px;line-height:1.18;margin:8px 0 14px}h2{font-size:23px;line-height:1.25;margin:22px 0 12px}p{margin:12px 0}
.objective{background:#edf5fc;padding:12px 16px;border-left:4px solid var(--blue)}.identity{display:flex;gap:16px;flex-wrap:wrap}.identity label{flex:1;min-width:200px}
input,select,textarea,button{font:inherit}input[type=text],input[type=number],select,textarea{width:100%;padding:9px;border:1px solid #8399ad;border-radius:4px;background:white;color:var(--ink)}
input[type=checkbox]{width:20px;height:20px;vertical-align:middle}textarea{display:block;margin:7px 0 20px;min-height:86px;resize:vertical}
label.question{display:block;font-weight:bold;margin-top:17px}input:focus-visible,textarea:focus-visible,select:focus-visible,button:focus-visible{outline:3px solid #1583bf;outline-offset:3px}
button{padding:10px 17px;cursor:pointer;border:1px solid var(--blue);border-radius:4px;background:var(--blue);color:#fff;font-weight:bold}button.secondary{background:#fff;color:var(--blue)}
table{width:100%;border-collapse:collapse;font-size:15px;margin:12px 0 22px}th,td{border:1px solid var(--line);padding:10px;vertical-align:top;text-align:left}th{background:#eef3f8}td textarea{font-size:16px;min-width:80px;min-height:65px;margin:0}.table-wrap{overflow-x:auto}
.step{border-top:2px solid var(--line);padding-top:10px;margin-top:30px}.step:first-of-type{border:0;margin-top:0;padding:0}.small{font-size:14px;color:#43556a}
.sim{margin:24px 0;padding:20px;border:2px solid #bdd0e1;background:#f5f9fd}.controls{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.controls label{display:block}.controls input[type=range]{width:100%}
.rule{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:16px 0}.rule select{width:auto;min-width:76px}.rule input{width:88px}.live{display:flex;gap:18px;align-items:center;padding:16px 0}.lamp{display:inline-block;flex:none;width:48px;height:48px;background:#9eacb8;border:3px solid #6d7e8e;border-radius:50%}.lamp.on{background:#ffd245;border-color:#a46500}
.state{font-size:21px;font-weight:bold}.active-rule{font-family:monospace;font-size:16px;overflow-wrap:anywhere}.chain{width:100%;height:auto}.portal-view svg{width:100%;height:auto}.portal-labels{display:grid;grid-template-columns:1fr 1fr;gap:0 20px}.toolbar{display:flex;flex-wrap:wrap;gap:12px;margin:22px 0}.feedback{min-height:28px;color:#164f28;font-weight:bold}
.exit{border:2px solid var(--blue);padding:15px;margin:22px 0}.exit textarea{margin-bottom:5px}.extra-person[hidden]{display:none}
@media(max-width:650px){main{margin:0;padding:22px 16px}.controls{grid-template-columns:1fr}h1{font-size:26px}table{font-size:14px}}
@media print{body{background:white;font-size:11pt}main{max-width:none;margin:0;padding:0;border:0}.toolbar,button,.sim{display:none}textarea{border:0;border-bottom:1px solid #777;min-height:55px}.step{break-before:page}header{break-after:avoid}table{font-size:9pt}.exit{break-inside:avoid}}
'''

BASE_JS = r'''
const root = document.querySelector('main');
const fields = () => [...root.querySelectorAll('[data-answer]')];
let dirty = false;
root.addEventListener('input', e => {if(e.target.matches('[data-answer]')) dirty=true;});
document.getElementById('paired').addEventListener('change',e=>{
 document.querySelectorAll('.extra-person').forEach(el=>el.hidden=!e.target.checked);
});
document.getElementById('export').addEventListener('click',()=>{
 const lines=[document.title,''];
 fields().forEach(el=>{
  if(el.closest('.extra-person')?.hidden)return;
  lines.push((el.dataset.answer||el.id)+' : '+(el.value.trim()||'[non renseigné]'),'');
 });
 const body=lines.join('\n');
 const blob=new Blob(['\ufeff'+body],{type:'text/plain;charset=utf-8'});
 const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;
 const name=document.getElementById('student').value.normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9_-]+/gi,'-').slice(0,50)||'eleve';
 a.download=LEVEL+'-seance1-'+name+'.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
 dirty=false;document.getElementById('saved').textContent='Téléchargement demandé. Vérifie le fichier dans tes téléchargements et remets-le au professeur.';
});
document.getElementById('print').addEventListener('click',()=>window.print());
window.addEventListener('beforeunload',e=>{if(dirty){e.preventDefault();e.returnValue='';}});
'''

LIGHT_HTML = '''
<section class="sim" aria-labelledby="light-title"><h2 id="light-title">Laboratoire : éclairage du couloir</h2>
<div class="controls"><label for="lum">Luminosité : <output id="lum-out">80</output> / 100<input id="lum" type="range" min="0" max="100" value="80" step="1"></label>
<label for="presence"><input type="checkbox" id="presence"> Une personne est présente</label></div>
<p>Modifie la règle de commande, puis applique-la.</p>
<div class="rule"><span>SI luminosité</span><label><span class="small">Comparaison</span><select id="cmp" aria-label="Comparaison"><option value="lt">&lt;</option><option value="le">≤</option><option value="gt">&gt;</option></select></label>
<label><span class="small">Seuil</span><input id="threshold" aria-label="Seuil" type="number" min="0" max="100" step="1" value="30"></label>
<label><span class="small">Liaison logique</span><select id="logic" aria-label="Liaison logique"><option value="or">OU</option><option value="and">ET</option></select></label><span>présence</span><button type="button" id="apply">Appliquer</button></div>
<p>ALORS allumer la lampe ; SINON l'éteindre.</p><p id="rule-error" role="alert"></p>
<p class="active-rule" id="active-rule"></p>
<div class="live" aria-live="polite"><span class="lamp" id="lamp" aria-hidden="true"></span><span id="lamp-state" class="state"></span></div>
<p class="small">Fais une prévision avant de manipuler. Le résultat affiché correspond à ta règle appliquée : il n'indique pas si elle respecte le besoin.</p></section>
'''

LIGHT_JS = '''
let active={cmp:'lt',logic:'or',threshold:30};
function updateLight(){
 const value=Number(document.getElementById('lum').value), present=document.getElementById('presence').checked;
 const c=active.cmp==='lt'?value<active.threshold:active.cmp==='le'?value<=active.threshold:value>active.threshold;
 const on=active.logic==='and'?c&&present:c||present;
 document.getElementById('lum-out').value=value;
 document.getElementById('lamp').classList.toggle('on',on);
 document.getElementById('lamp-state').textContent=on?'Lampe allumée':'Lampe éteinte';
 document.getElementById('lamp-state').dataset.on=String(on);
 document.getElementById('active-rule').textContent='Règle appliquée : luminosité '+({lt:'<',le:'≤',gt:'>'}[active.cmp])+' '+active.threshold+' '+(active.logic==='and'?'ET':'OU')+' présence';
}
document.getElementById('lum').addEventListener('input',updateLight);
document.getElementById('presence').addEventListener('change',updateLight);
document.getElementById('apply').addEventListener('click',()=>{
 const field=document.getElementById('threshold');
 if(!field.validity.valid||field.value.trim()===''){document.getElementById('rule-error').textContent='Choisis un seuil entier entre 0 et 100.';return;}
 document.getElementById('rule-error').textContent='';
 active={cmp:document.getElementById('cmp').value,logic:document.getElementById('logic').value,threshold:Number(field.value)};updateLight();
});updateLight();
'''

GATE_HTML = '''
<section class="sim" aria-labelledby="gate-title"><h2 id="gate-title">Laboratoire : autoriser la fermeture</h2>
<p>Choisis la situation ; observe l'ordre envoyé. Il s'agit d'une simulation de la décision, sans animation du déplacement.</p>
<div class="controls"><label><input id="request" type="checkbox"> Bouton de fermeture appuyé</label>
<label><input id="obstacle" type="checkbox"> Obstacle dans le passage</label>
<label><input id="closed" type="checkbox"> Portail déjà complètement fermé</label></div>
<p id="gate-state" class="state" aria-live="polite"></p>
<p id="gate-detail"></p></section>
'''

GATE_JS = '''
function updateGate(){
 const request=document.getElementById('request').checked, obstacle=document.getElementById('obstacle').checked, closed=document.getElementById('closed').checked;
 const move=request&&!obstacle&&!closed;
 const state=document.getElementById('gate-state');state.textContent=move?'Ordre : fermer':'Ordre : arrêt';state.dataset.move=String(move);
 document.getElementById('gate-detail').textContent=move?'Le module de puissance alimente le moteur : le mouvement est autorisé.':'Le module de puissance n’alimente pas le moteur pour fermer.';
}
['request','obstacle','closed'].forEach(id=>document.getElementById(id).addEventListener('change',updateGate));updateGate();
'''

def diagram_svg():
    boxes=[]
    for row,y,labels,color in [(0,32,['ACQUÉRIR','TRAITER','COMMUNIQUER'],'#175b9a'),(1,165,['ALIMENTER','DISTRIBUER','CONVERTIR','TRANSMETTRE'],'#b65b12')]:
        positions=[55,295,535] if row==0 else [10,205,400,595]
        width=170
        for x,label in zip(positions,labels):
            boxes.append(f'<rect x="{x}" y="{y}" width="{width}" height="58" rx="3" fill="white" stroke="{color}" stroke-width="2"/><text x="{x+width/2}" y="{y+25}" text-anchor="middle" font-size="16" font-weight="bold" fill="{color}">{label}</text><text x="{x+width/2}" y="{y+45}" text-anchor="middle" font-size="11" fill="#405369">repère(s) et composant(s) ?</text>')
        for left,right in zip(positions,positions[1:]):
            boxes.append(f'<path d="M{left+width} {y+29} H{right-9}" stroke="{color}" stroke-width="2" fill="none" marker-end="url(#arrow-{row})"/>')
    return '<svg class="chain" viewBox="0 0 785 280" role="img" aria-label="Chaîne d’information : acquérir, traiter, communiquer. Un ordre va vers distribuer. Chaîne d’énergie : alimenter, distribuer, convertir, transmettre, puis action sur le portail." xmlns="http://www.w3.org/2000/svg"><defs><marker id="arrow-0" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8Z" fill="#175b9a"/></marker><marker id="arrow-1" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8Z" fill="#b65b12"/></marker></defs><text x="10" y="20" font-size="16" fill="#175b9a">INFORMATION</text><text x="10" y="152" font-size="16" fill="#b65b12">ÉNERGIE</text>'+''.join(boxes)+'<path d="M620 90 V115 H290 V155" fill="none" stroke="#175b9a" stroke-width="2" marker-end="url(#arrow-0)"/><text x="400" y="108" font-size="16" fill="#175b9a">ordre</text><path d="M680 223 V244" fill="none" stroke="#b65b12" stroke-width="2" marker-end="url(#arrow-1)"/><text x="550" y="268" font-size="15" fill="#b65b12">Action : déplacement du portail</text></svg>'

def field(identifier,label,lines=2):
    return f'<label class="question" for="{esc(identifier)}">{esc(label)}</label><textarea id="{esc(identifier)}" data-answer="{esc(label)}" rows="{lines+1}"></textarea>'

def block_html(b):
    t=b['type']
    if t=='p': return '<p>'+esc(b['text'])+'</p>'
    if t=='h': return '<h2>'+esc(b['text'])+'</h2>'
    if t=='q': return field(b['id'],b['label'],b['lines'])
    if t=='choice': return f'<label class="question" for="{b["id"]}">{esc(b["label"])}</label><select id="{b["id"]}" data-answer="{esc(b["label"])}">'+''.join('<option>'+esc(o)+'</option>' for o in b['options'])+'</select>'
    if t=='exit':
        return '<section class="exit"><h2>Bilan individuel</h2>'+field(b['id']+'-a',b['label']+' (élève 1)',b['lines'])+'<div class="extra-person" hidden>'+field(b['id']+'-b',b['label']+' (élève 2)',b['lines'])+'</div></section>'
    if t=='diagram': return diagram_svg()
    if t=='sim': return LIGHT_HTML if b['name']=='light' else GATE_HTML
    if t in ('table','answer_table'):
        out=('<p><strong>'+esc(b['label'])+'</strong></p>') if t=='answer_table' else ''
        out+='<div class="table-wrap"><table><thead><tr>'+''.join('<th scope="col">'+esc(h)+'</th>' for h in b['headers'])+'</tr></thead><tbody>'
        if t=='table':
            for row in b['rows']: out+='<tr>'+''.join('<td>'+esc(v)+'</td>' for v in row)+'</tr>'
        else:
            for r in range(b['rows']):
                out+='<tr>'
                for c,h in enumerate(b['headers']):
                    if c==0 and b.get('fixed'): out+='<th scope="row">'+esc(b['fixed'][r])+'</th>'
                    else:
                        label=f'{b["label"]} | '+(b['fixed'][r] if b.get('fixed') else f'Ligne {r+1}')+' | '+h
                        out+=f'<td><textarea rows="2" id="{b["id"]}-{r}-{c}" aria-label="{esc(label)}" data-answer="{esc(label)}"></textarea></td>'
                out+='</tr>'
        return out+'</tbody></table></div>'
    raise ValueError(t)

def make_html(lesson):
    content=''.join('<section class="step">'+''.join(block_html(b) for b in page)+'</section>' for page in lesson['pages'])
    if lesson['level']=='3e':
        svg=portal_svg(False,legend=False)
        svg=svg[svg.index('<svg '):]
        fields=''.join(field('repere-'+n,'Repère '+n+' : nom du composant',1) for n,_,_ in COMPONENTS)
        content='<section class="step"><h2>Observer et légender le portail</h2><p>Identifie les neuf repères à l’aide du tableau des composants ci-dessous. Le dessin est une vue pédagogique simplifiée, sans échelle. Le faisceau passe devant le vantail. La cible mobile rejoint le capteur fixe en fin de fermeture.</p><div class="portal-view">'+svg+'</div><div class="portal-labels">'+fields+'</div></section>'+content
    js=BASE_JS + (LIGHT_JS if lesson['level']=='4e' else GATE_JS if lesson['level']=='3e' else '')
    return f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(lesson['level'])} - {esc(lesson['title'])}</title><style>{CSS}</style></head>
<body><main><header><div class="meta">TECHNOLOGIE · {esc(lesson['level'].upper())} · SÉANCE 1 · 55 MIN</div><h1>{esc(lesson['title'])}</h1><p>{esc(lesson['question'])}</p><p class="objective">Objectif : {esc(lesson['objective'])}</p>
<div class="identity"><label for="student">Prénom et nom<input id="student" type="text" autocomplete="off" data-answer="Élève 1"></label><label for="classe">Classe<input id="classe" type="text" autocomplete="off" data-answer="Classe"></label></div>
<p><label><input id="paired" type="checkbox"> Nous travaillons à deux sur ce PC</label></p><div class="extra-person" hidden><label for="student2">Prénom et nom du second élève<input id="student2" type="text" autocomplete="off" data-answer="Élève 2"></label></div>
<p class="small">Écris tes réponses dans les cases. Télécharge-les avant de fermer la page ; rien n'est envoyé automatiquement au professeur. En binôme, alternez le clavier et répondez chacun au bilan individuel.</p></header>
{content}<div class="toolbar"><button type="button" id="export">Télécharger mes réponses</button><button class="secondary" type="button" id="print">Imprimer mon travail</button></div><p id="saved" class="feedback" role="status"></p></main>
<script>const LEVEL={json.dumps(lesson['level'])};{js}</script></body></html>'''
