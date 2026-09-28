// Independent workbook storage; no migration of the existing evaluation tables.
const reply=(v,status=200)=>Response.json(v,{status,headers:{'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'}});
export function initPonts(sql){sql.exec('CREATE TABLE IF NOT EXISTS ponts_workbooks (id TEXT PRIMARY KEY, token TEXT UNIQUE NOT NULL, data TEXT NOT NULL, updated INTEGER NOT NULL)');}
export function validateWorkbook(value){
 if(!value||typeof value!=='object'||Array.isArray(value)||!value.answers||typeof value.answers!=='object'||Array.isArray(value.answers))throw Error('Réponses non valides.');
 const entries=Object.entries(value.answers);
 if(entries.length>180||entries.some(([k,v])=>!/^s[1-5]_[a-z0-9_]{1,50}$/.test(k)||typeof v!=='string'||v.length>2500))throw Error('Une réponse est trop longue ou non valide.');
 if(!Number.isInteger(value.lesson)||value.lesson<1||value.lesson>5||typeof value.guided!=='boolean')throw Error('Séance non valide.');
 return {answers:Object.fromEntries(entries),lesson:value.lesson,guided:value.guided};
}
export async function pontsRoute(store,req,path){
 const teacher=path.startsWith('/teacher/ponts');
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
  if(path==='/teacher/ponts'&&req.method==='GET'){
   const rows=store.sql.exec('SELECT data FROM ponts_workbooks ORDER BY updated DESC LIMIT 5000').toArray();
   return reply({workbooks:rows.map(r=>{const d=JSON.parse(r.data);return {id:d.id,created:d.created,updated:d.updated,submitted:d.submitted,lesson:d.lesson,guided:d.guided,answered:Object.values(d.answers).filter(v=>v.trim()).length}})});
  }
  const id=req.method==='GET'?new URL(req.url).searchParams.get('id'):b?.id;
  if(typeof id!=='string'||!/^P-[A-F0-9]{12}$/.test(id))return reply({error:'Copie non valide.'},400);
  const r=store.one('SELECT data FROM ponts_workbooks WHERE id=?',id);if(!r)return reply({error:'Copie introuvable.'},404);
  if(path==='/teacher/ponts/review'&&req.method==='GET')return reply(JSON.parse(r.data));
  if(path==='/teacher/ponts/delete'&&req.method==='POST'&&b.confirm===true){store.sql.exec('DELETE FROM ponts_workbooks WHERE id=?',id);return reply({ok:true});}
  return reply({error:'Action inconnue.'},400);
 }
 if(path==='/ponts/create'&&req.method==='POST'){
  store.limited('ponts-create:'+(req.headers.get('cf-connecting-ip')||'local'),180,3600000);
  if(store.one('SELECT count(*) AS n FROM ponts_workbooks').n>=5000)return reply({error:'Le professeur doit archiver des copies avant de continuer.'},409);
  const token=crypto.randomUUID().replaceAll('-','').toUpperCase();
  const id='P-'+crypto.randomUUID().replaceAll('-','').slice(0,12).toUpperCase();
  const d={id,created:Date.now(),updated:Date.now(),submitted:null,revision:0,answers:{},lesson:1,guided:b?.guided===true};
  store.sql.exec('INSERT INTO ponts_workbooks VALUES(?,?,?,?)',id,token,JSON.stringify(d),d.updated);return reply({token,workbook:d},201);
 }
 const token=req.headers.get('authorization')?.replace(/^Bearer /,'');
 if(!token||! /^[A-F0-9]{32}$/.test(token))return reply({error:'Code de reprise non valide.'},401);
 const row=store.one('SELECT data FROM ponts_workbooks WHERE token=?',token);if(!row)return reply({error:'Code inconnu ou copie supprimée.'},401);
 const d=JSON.parse(row.data);
 if(path==='/ponts/state'&&req.method==='GET')return reply(d);
 if((path==='/ponts/save'||path==='/ponts/submit')&&req.method==='POST'){
  if(b?.revision!==d.revision)return reply({error:'Cette copie a changé sur un autre onglet ou poste. Télécharge ta sauvegarde, puis quitte et reprends avec ton code.'},409);
  let clean;try{clean=validateWorkbook(b)}catch(e){return reply({error:e.message},400)}
  if(clean.guided!==d.guided)return reply({error:'Ce carnet appartient à un autre parcours.'},400);
  Object.assign(d,clean,{revision:d.revision+1,updated:Date.now(),submitted:path.endsWith('/submit')?Date.now():null});
  store.sql.exec('UPDATE ponts_workbooks SET data=?,updated=? WHERE id=?',JSON.stringify(d),d.updated,d.id);return reply(d);
 }
 return reply({error:'Page introuvable.'},404);
}
