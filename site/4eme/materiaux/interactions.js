import {calculate,materials} from './model.js';
import {esc} from './content.js';
export function setupInteractions({read,write,notice}){
 const f=n=>Number(n).toLocaleString('fr-FR',{maximumFractionDigits:2});
 for(const lab of document.querySelectorAll('[data-lab]')){
  const number=Number(lab.dataset.lab),controls=[...lab.querySelectorAll('[data-setting]')];
  const settings=()=>Object.fromEntries(controls.map(el=>[el.dataset.setting,el.value]));
  const render=()=>{
   const p=settings();const hollow=controls.find(el=>el.dataset.setting==='shape');hollow.options[1].disabled=p.material==='bois';
   if(p.material==='bois'&&p.shape==='creux'){hollow.value='plein';p.shape='plein';}
   const result=calculate(p),d=Math.min(result.deflection*12,85),h=Number(p.thickness),color=materials[p.material].color;
   const section=p.shape==='creux'?`<rect x="614" y="${128-h}" width="90" height="${h}" fill="${color}"/><rect x="620" y="${134-h}" width="78" height="${Math.max(h-12,2)}" fill="white"/>`:`<rect x="614" y="${128-h}" width="90" height="${h}" fill="${color}"/>`;
   lab.querySelector('[data-drawing]').innerHTML=`<svg viewBox="0 0 760 260" role="img" aria-label="Pièce sur deux appuis. Flèche ${f(result.deflection)} millimètres. Section ${p.shape==='plein'?'pleine':'creuse'}."><path d="M65 120H535" stroke="#aebfc5" stroke-dasharray="6 5" stroke-width="3"/><path d="M65 120Q300 ${120+2*d} 535 120" stroke="${color}" stroke-width="12" fill="none"/><path d="M70 130l-20 28h40zM530 130l-20 28h40z" fill="#1d5661"/><path d="M300 35v60m-8-10l8 10 8-10" stroke="#c06824" stroke-width="4" fill="none"/><text x="300" y="24" text-anchor="middle">${p.load} kg au centre</text><path d="M70 210H530m-460-5v10m460-10v10" stroke="#1d5661" stroke-width="2"/><text x="300" y="239" text-anchor="middle">Portée : ${p.span} cm</text>${section}<text x="660" y="74" text-anchor="middle">Section</text><text x="660" y="157" text-anchor="middle">Hauteur : ${h} mm</text><text x="660" y="181" text-anchor="middle">Largeur : 25 cm</text></svg>`;
   lab.querySelector('[data-results]').innerHTML=`<div class="metrics"><p><span>Flèche calculée</span><strong>${f(result.deflection)} mm</strong></p><p><span>Masse de la pièce</span><strong>${f(result.mass)} kg</strong></p></div>${!result.valid?'<p class="feedback retry">Grande déformation : le modèle des petites déformations n’est plus adapté. Ce résultat ne permet pas de conclure.</p>':''}${number===4?`<p class="feedback ${result.pass?'good':'retry'}">${result.pass?'Les quatre contraintes du défi sont respectées dans le modèle.':'Défi à ajuster : '+[Number(p.span)!==80?'portée à remettre à 80 cm':'',Number(p.load)!==10?'charge à remettre à 10 kg':'',result.mass>2?'masse supérieure à 2 kg':'',result.deflection>3?'flèche supérieure à 3 mm':''].filter(Boolean).join(' ; ')+'.'}</p>`:''}`;
   return {p,result};
  };
  for(const el of controls)el.onchange=render;
  lab.querySelector('[data-reset]').onclick=()=>{for(const el of controls)el.value=String({material:'bois',span:80,thickness:15,shape:'plein',load:10}[el.dataset.setting]);render()};
  lab.querySelector('[data-record]').onclick=()=>{
   const {p,result}=render();const text=`${materials[p.material].name} ; portée ${p.span} cm ; hauteur ${p.thickness} mm ; section ${p.shape==='plein'?'pleine':'creuse'} ; charge ${p.load} kg ; flèche ${f(result.deflection)} mm ; masse ${f(result.mass)} kg.${!result.valid?' Modèle hors domaine des petites déformations.':''}`;
   const key=number===4?'s4_solution':[1,2,3].map(i=>'s3_trial'+i).find(id=>!read(id));
   if(!key){notice('Tes trois essais sont remplis. Efface le champ de l’essai à remplacer avant d’en enregistrer un nouveau.');return;}
   if(number===4&&read(key)&&!confirm('Remplacer la solution enregistrée par ce réglage ?'))return;
   write(key,text);lab.querySelector('[data-record-status]').textContent=number===4?'Solution copiée dans ton carnet.':'Essai copié dans le champ '+key.slice(-1)+'.';
  };render();
 }
 const descriptions={Traction:'Deux actions tirent la pièce : elle s’allonge.',Compression:'Deux actions poussent sur la pièce : elle se raccourcit. Une pièce élancée peut aussi flamber.',Flexion:'La charge courbe la pièce entre ses appuis.',Torsion:'Deux actions de rotation opposées tordent la pièce.'};
 function effortDiagram(animate=false){
  const mode=document.querySelector('#effort-mode').value;
  const paths={Traction:'M130 90H65m15-9l-15 9 15 9M510 90h65m-15-9l15 9-15 9',Compression:'M55 90h80m-15-9l15 9-15 9M585 90h-80m15-9l-15 9 15 9',Flexion:'M320 15v55m-9-15l9 15 9-15',Torsion:'M130 55C70 10 70 160 130 120m-13-4l13 4-4 13M510 120C570 170 570 10 510 55m4-13l-4 13 13 4'};
  const shape=mode==='Flexion'?'<path d="M155 90Q320 180 485 90" stroke="#2a8390" stroke-width="22" fill="none"/><path d="M155 106l-17 24h34zM485 106l-17 24h34z" fill="#183c49"/>':mode==='Torsion'?'<path d="M150 67Q250 150 320 90T490 67L490 112Q390 30 320 90T150 112Z" fill="#2a8390"/>':`<rect x="150" y="75" width="340" height="32" rx="5" fill="#2a8390" class="${mode==='Traction'?'stretch':'squash'}"/>`;
  document.querySelector('#effort-drawing').innerHTML=`<svg class="${animate?'play-effort':''}" viewBox="0 0 640 185" role="img" aria-label="${esc(descriptions[mode])}">${shape}<path d="${paths[mode]}" fill="none" stroke="#c06824" stroke-width="5"/><text x="320" y="176" text-anchor="middle">${mode}</text></svg>`;
  document.querySelector('#effort-explanation').textContent=descriptions[mode];
 }
 document.querySelector('#effort-mode').onchange=()=>effortDiagram();document.querySelector('#animate-effort').onclick=()=>effortDiagram(true);effortDiagram();
 let loaded=false,hasLoaded=false,hasBroken=false;
 function deform(){const mode=document.querySelector('#deform-mode').value;const bent=loaded||(mode==='plastic'&&hasLoaded),broken=hasBroken;
 const state=broken?(loaded?'La pièce casse : c’est une rupture.':'La charge est retirée, mais la pièce reste cassée.'):loaded?'La pièce se déforme sous la charge.':mode==='plastic'&&hasLoaded?'La charge est retirée : la pièce reste déformée.':!hasLoaded?'Éprouvette neuve, avant chargement.':'La charge est retirée : la pièce retrouve sa forme initiale.';
 document.querySelector('#deform-drawing').innerHTML=`<svg viewBox="0 0 640 185" role="img" aria-label="${state}"><path d="M100 70H540" stroke="#bac8cc" stroke-dasharray="5 5" stroke-width="2"/><path d="${broken?'M100 70L295 135M345 135L540 70':bent?'M100 70Q320 170 540 70':'M100 70H540'}" fill="none" stroke="#2a8390" stroke-width="16"/>${loaded?'<path d="M320 10v45m-8-10l8 10 8-10" fill="none" stroke="#c06824" stroke-width="4"/>':''}<text x="320" y="175" text-anchor="middle">${loaded?'Charge appliquée':'Charge retirée / avant essai'}</text></svg>`;
 document.querySelector('#deform-explanation').textContent=state;
 }

 document.querySelector('#deform-mode').onchange=()=>{loaded=false;hasLoaded=false;hasBroken=false;deform()};
 document.querySelector('#load-piece').onclick=()=>{loaded=true;hasLoaded=true;hasBroken=document.querySelector('#deform-mode').value==='break';deform()};
 document.querySelector('#unload-piece').onclick=()=>{loaded=false;deform()};deform();
}
