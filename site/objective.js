// Shared, accessible self-checks. Old free responses keep their original keys.
export const escape=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export const choice=(label,answer,wrong,explanation)=>({label,answer,choices:[answer,...wrong],explanation});
export const observation=(label,choices)=>({label,choices,observation:true});
export const numeric=(label,answer,explanation,tolerance=0)=>({label,answer,type:'number',explanation,tolerance});
function ordered(values,id){const n=[...id].reduce((s,c)=>s+c.charCodeAt(0),0)%values.length;return [...values.slice(n),...values.slice(0,n)];}
export function question(id,label,spec,labels,{legacy=false}={}){
 if(!spec)throw Error('Question sans définition : '+id);
 if(legacy)labels[id]='Ancienne réponse · '+label;
 if(spec.parts)return spec.parts.map((p,i)=>question(id+(legacy?'_v2':'')+'_'+(i+1),p.label,p,labels)).join('');
 const key=id+(legacy?'_v2':'');label=spec.label||label;labels[key]=label;
 if(spec.type==='output')return `<div class="question"><label for="${key}">${escape(label)}</label><output id="${key}" data-answer class="recorded-answer"></output><p class="small">Rempli automatiquement avec le bouton du simulateur.</p></div>`;
 const attrs=`id="${key}" data-answer aria-describedby="${key}-feedback"`;
 const field=spec.type==='number'?`<input ${attrs} type="number" inputmode="decimal" step="any" min="${spec.min??0}" max="${spec.max??1000000000}">`:`<select ${attrs}><option value="">Choisir…</option>${ordered(spec.choices,key).map(v=>`<option value="${escape(v)}">${escape(v)}</option>`).join('')}</select>`;
 const config=escape(JSON.stringify(spec));
 return `<div class="question objective" data-spec="${config}"><label for="${key}">${escape(label)}</label>${field}<button type="button" class="secondary objective-check">${spec.observation?'Vérifier la saisie':'Vérifier ma réponse'}</button><p id="${key}-feedback" class="feedback" role="status"></p></div>`;
}
export function assess(value,spec){
 if(String(value??'').trim()==='')return {state:'retry',text:'Choisis une réponse ou saisis une valeur avant de vérifier.'};
 if(spec.type==='number'&&(!Number.isFinite(Number(value))||Number(value)<(spec.min??0)||Number(value)>(spec.max??1000000000)))return {state:'retry',text:`Entre une valeur entre ${spec.min??0} et ${spec.max??1000000000}.`};
 if(spec.observation)return {state:'recorded',text:'Relevé saisi. Compare-le au résultat affiché dans le logiciel : le site ne peut pas vérifier cette observation.'};
 const ok=spec.type==='number'?Math.abs(Number(value)-spec.answer)<=(spec.tolerance||1e-9):value===spec.answer;
 return {state:ok?'good':'retry',text:(ok?'Bonne réponse. ':'À revoir. ')+(spec.explanation||'')+(ok?'':' Tu peux modifier ta réponse et réessayer.')};
}
export function setupObjectives(root=document){
 for(const el of root.querySelectorAll('.objective')){
  const input=el.querySelector('[data-answer]'),feedback=el.querySelector('.feedback'),spec=JSON.parse(el.dataset.spec);
  const verify=()=>{const r=assess(input.value,spec);feedback.textContent=r.text;feedback.className='feedback '+r.state;input.setAttribute('aria-invalid',r.state==='retry'?'true':'false');};
  el.querySelector('.objective-check').onclick=verify;
  input.addEventListener('change',verify);
  input.addEventListener('input',()=>{feedback.textContent='';input.removeAttribute('aria-invalid')});
 }
 // Existing grouped matching exercises also give feedback on each association.
 for(const b of root.querySelectorAll('.check-answer')){
  const ids=b.dataset.ids.split(','),answers=JSON.parse(b.dataset.correct);
  ids.forEach((id,i)=>{const input=root.querySelector('#'+id);if(!input||input.closest('.objective'))return;
   const feedback=document.createElement('p');feedback.className='feedback';feedback.id=id+'-feedback';feedback.setAttribute('role','status');input.after(feedback);input.setAttribute('aria-describedby',feedback.id);
   input.addEventListener('change',()=>{const ok=input.value===answers[i];feedback.className='feedback '+(ok?'good':'retry');feedback.textContent=!input.value?'Choisis une réponse.':ok?'Bonne association.':`À revoir : ${answers[i]}. ${b.dataset.message} Réessaie.`;b.nextElementSibling.textContent='';});
  });
 }
}
export function renderArchive(root,answers,labels){
 root.querySelector('.legacy-answers')?.remove();
 const entries=Object.entries(answers).filter(([id,v])=>v&&labels[id]?.startsWith('Ancienne réponse'));
 if(!entries.length)return;
 const details=document.createElement('details');details.className='legacy-answers card';details.innerHTML='<summary>Mes anciennes réponses · lecture seule</summary>'+entries.map(([id,v])=>`<h3>${escape(labels[id])}</h3><p>${escape(v)}</p>`).join('');root.append(details);
}
