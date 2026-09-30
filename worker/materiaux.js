// Independent workbook storage; no migration of the existing evaluation tables.
const reply=(v,status=200)=>Response.json(v,{status,headers:{'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'}});
export function initMateriaux(sql){sql.exec('CREATE TABLE IF NOT EXISTS materiaux_classes (id TEXT PRIMARY KEY, classe TEXT NOT NULL)');sql.exec('CREATE TABLE IF NOT EXISTS materiaux_access (classe TEXT PRIMARY KEY, through INTEGER NOT NULL)');sql.exec('CREATE TABLE IF NOT EXISTS materiaux_workbooks (id TEXT PRIMARY KEY, token TEXT UNIQUE NOT NULL, data TEXT NOT NULL, updated INTEGER NOT NULL)');}
export function validateWorkbook(value){
 if(!value||typeof value!=='object'||Array.isArray(value)||!value.answers||typeof value.answers!=='object'||Array.isArray(value.answers))throw Error('Réponses non valides.');
 const entries=Object.entries(value.answers);
 if(entries.length>180||entries.some(([k,v])=>!/^s[1-4]_[a-z0-9_]{1,50}$/.test(k)||typeof v!=='string'||v.length>2500))throw Error('Une réponse est trop longue ou non valide.');
 if(!Number.isInteger(value.lesson)||value.lesson<1||value.lesson>4||typeof value.guided!=='boolean')throw Error('Séance non valide.');
 return {answers:Object.fromEntries(entries),lesson:value.lesson,guided:value.guided};
}
const className=value=>typeof value==='string'&&/^[A-Za-z0-9À-ÿ ()_-]{0,30}$/.test(value.trim())?value.trim().toUpperCase():null;
const access=(store,id)=>{const classe=store.one('SELECT classe FROM materiaux_classes WHERE id=?',id)?.classe||'';return store.one('SELECT through FROM materiaux_access WHERE classe=?',classe)?.through??4;};
const pupil=(store,d)=>({...d,openThrough:access(store,d.id)});
export async function materiauxRoute(store,req,path){
 const teacher=path.startsWith('/teacher/materiaux');
 if(teacher)store.teacher(req);
 if(!['GET','POST'].includes(req.method))return reply({error:'Méthode non autorisée.'},405);
 let b;
 if(req.method==='POST'){
  if(req.headers.get('sec-fetch-site')==='cross-site'||(req.headers.get('origin')&&req.headers.get('origin')!==new URL(req.url).origin))return reply({error:'Requête non autorisée.'},403);
  if(!req.headers.get('content-type')?.includes('application/json'))return reply({error:'Format non accepté.'},415);
  if(Number(req.headers.get('content-length')||0)>100000)return reply({error:'Copie trop volumineuse.'},413);
  const raw=await req.text();if(raw.length>100000)return reply({error:'Copie trop volumineuse.'},413);
  try{b=JSON.parse(raw)}catch{return reply({error:'Formulaire non valide.'},400)}
 }
 if(teacher){
  if(path==='/teacher/materiaux/access'&&req.method==='POST'){
   const classe=className(b?.classe);if(classe===null||!Number.isInteger(b?.through)||b.through<1||b.through>4)return reply({error:'Classe ou séance non valide.'},400);
   store.sql.exec('INSERT OR REPLACE INTO materiaux_access VALUES(?,?)',classe,b.through);return reply({ok:true});
  }
  if(path==='/teacher/materiaux'&&req.method==='GET'){
   const rows=store.sql.exec('SELECT data FROM materiaux_workbooks ORDER BY updated DESC LIMIT 5000').toArray();
   return reply({access:store.sql.exec('SELECT classe,through FROM materiaux_access ORDER BY classe').toArray(),workbooks:rows.map(r=>{const d=JSON.parse(r.data);return {classe:store.one('SELECT classe FROM materiaux_classes WHERE id=?',d.id)?.classe||'',id:d.id,created:d.created,updated:d.updated,submitted:d.submitted,lesson:d.lesson,guided:d.guided,answered:Object.values(d.answers).filter(v=>v.trim()).length}})});
  }
  const id=req.method==='GET'?new URL(req.url).searchParams.get('id'):b?.id;
  if(typeof id!=='string'||!/^M-[A-F0-9]{12}$/.test(id))return reply({error:'Copie non valide.'},400);
  const r=store.one('SELECT data FROM materiaux_workbooks WHERE id=?',id);if(!r)return reply({error:'Copie introuvable.'},404);
  if(path==='/teacher/materiaux/class'&&req.method==='POST'){
   const classe=className(b?.classe);if(classe===null)return reply({error:'Classe non valide (30 caractères maximum).'},400);
   store.sql.exec('INSERT OR REPLACE INTO materiaux_classes VALUES(?,?)',id,classe);return reply({ok:true});
  }
  if(path==='/teacher/materiaux/review'&&req.method==='GET')return reply(JSON.parse(r.data));
  if(path==='/teacher/materiaux/delete'&&req.method==='POST'&&b.confirm===true){store.sql.exec('DELETE FROM materiaux_workbooks WHERE id=?',id);return reply({ok:true});}
  return reply({error:'Action inconnue.'},400);
 }
 if(path==='/materiaux/create'&&req.method==='POST'){
  store.limited('materiaux-create:'+(req.headers.get('cf-connecting-ip')||'local'),180,3600000);
  if(store.one('SELECT count(*) AS n FROM materiaux_workbooks').n>=5000)return reply({error:'Le professeur doit archiver des copies avant de continuer.'},409);
  const token=crypto.randomUUID().replaceAll('-','').toUpperCase();
  const id='M-'+crypto.randomUUID().replaceAll('-','').slice(0,12).toUpperCase();
  const d={id,created:Date.now(),updated:Date.now(),submitted:null,revision:0,answers:{},lesson:1,guided:b?.guided===true};
  store.sql.exec('INSERT INTO materiaux_workbooks VALUES(?,?,?,?)',id,token,JSON.stringify(d),d.updated);return reply({token,workbook:pupil(store,d)},201);
 }
 const token=req.headers.get('authorization')?.replace(/^Bearer /,'');
 if(!token||! /^[A-F0-9]{32}$/.test(token))return reply({error:'Code de reprise non valide.'},401);
 const row=store.one('SELECT data FROM materiaux_workbooks WHERE token=?',token);if(!row)return reply({error:'Code inconnu ou copie supprimée.'},401);
 const d=JSON.parse(row.data);
 if(path==='/materiaux/access'&&req.method==='GET')return reply({openThrough:access(store,d.id)});
 if(path==='/materiaux/state'&&req.method==='GET')return reply(pupil(store,d));
 if((path==='/materiaux/save'||path==='/materiaux/submit')&&req.method==='POST'){
  if(b?.revision!==d.revision)return reply({error:'Cette copie a changé sur un autre onglet ou poste. Télécharge ta sauvegarde, puis quitte et reprends avec ton code.'},409);
  let clean;try{clean=validateWorkbook(b)}catch(e){return reply({error:e.message},400)}
  if(clean.guided!==d.guided)return reply({error:'Ce carnet appartient à un autre parcours.'},400);
  const through=access(store,d.id);
  for(const key of new Set([...Object.keys(d.answers),...Object.keys(clean.answers)])){
   if(Number(key[1])>through&&(clean.answers[key]||'')!==(d.answers[key]||''))return reply({error:'Cette séance n’est pas encore ouverte par le professeur.'},403);
  }
  clean.lesson=Math.min(clean.lesson,through);
  Object.assign(d,clean,{revision:d.revision+1,updated:Date.now(),submitted:path.endsWith('/submit')?Date.now():null});
  store.sql.exec('UPDATE materiaux_workbooks SET data=?,updated=? WHERE id=?',JSON.stringify(d),d.updated,d.id);return reply(pupil(store,d));
 }
 return reply({error:'Page introuvable.'},404);
}
