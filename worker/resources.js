const TYPES=new Set(['application/pdf','application/vnd.openxmlformats-officedocument.wordprocessingml.document','video/mp4','image/jpeg','image/png']);
const respond=(v,status=200)=>Response.json(v,{status,headers:{'Cache-Control':'no-store'}});
export function resourceTables(sql){sql.exec('CREATE TABLE IF NOT EXISTS resource_files (slug TEXT PRIMARY KEY, meta TEXT NOT NULL); CREATE TABLE IF NOT EXISTS resource_parts (slug TEXT NOT NULL, n INTEGER NOT NULL, data TEXT NOT NULL, PRIMARY KEY(slug,n));');}
export async function uploadResource(sql,ctx,b){
 if(!/^[a-z0-9][a-z0-9.-]{1,110}$/.test(b.slug)||typeof b.title!=='string'||b.title.length>150||!TYPES.has(b.type)||typeof b.public!=='boolean'||typeof b.data!=='string'||!Number.isInteger(b.size)||b.size<1||b.size>8000000)return respond({error:'Ressource non valide.'},400);
 let bytes;try{bytes=Uint8Array.from(atob(b.data),c=>c.charCodeAt(0));}catch{return respond({error:'Fichier non valide.'},400)}
 if(bytes.length!==b.size)return respond({error:'Taille incohérente.'},400);
 const digest=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes)),v=>v.toString(16).padStart(2,'0')).join('');
 if(digest!==b.sha256)return respond({error:'Empreinte incohérente.'},400);
 const meta={slug:b.slug,title:b.title,type:b.type,public:b.public,size:b.size,sha256:digest};
 ctx.storage.transactionSync(()=>{sql.exec('DELETE FROM resource_parts WHERE slug=?',b.slug);for(let i=0;i<b.data.length;i+=262144)sql.exec('INSERT INTO resource_parts VALUES(?,?,?)',b.slug,i/262144,b.data.slice(i,i+262144));sql.exec('INSERT OR REPLACE INTO resource_files VALUES(?,?)',b.slug,JSON.stringify(meta));});return respond({ok:true,slug:b.slug,sha256:digest});
}
export function listResources(sql){return respond({resources:sql.exec('SELECT meta FROM resource_files ORDER BY slug').toArray().map(r=>JSON.parse(r.meta))});}
export function serveResource(sql,req,slug,teacher){
 const row=sql.exec('SELECT meta FROM resource_files WHERE slug=?',slug).toArray()[0];if(!row)return respond({error:'Ressource introuvable.'},404);
 const m=JSON.parse(row.meta);if(!m.public&&!teacher)return respond({error:'Ressource introuvable.'},404);
 let start=0,end=m.size-1,status=200;const range=req.headers.get('range');
 if(range){const v=/^bytes=(\d*)-(\d*)$/.exec(range);if(!v||(!v[1]&&!v[2]))return new Response(null,{status:416,headers:{'Content-Range':`bytes */${m.size}`}});if(!v[1])start=Math.max(0,m.size-Number(v[2]));else{start=Number(v[1]);if(v[2])end=Math.min(end,Number(v[2]));}if(start>end||start>=m.size)return new Response(null,{status:416,headers:{'Content-Range':`bytes */${m.size}`}});status=206;}
 const bytes=new Uint8Array(end-start+1),first=Math.floor(start/196608),last=Math.floor(end/196608);
 for(const r of sql.exec('SELECT n,data FROM resource_parts WHERE slug=? AND n>=? AND n<=? ORDER BY n',slug,first,last).toArray()){const raw=Uint8Array.from(atob(r.data),c=>c.charCodeAt(0));const offset=r.n*196608,lo=Math.max(start,offset),hi=Math.min(end+1,offset+raw.length);bytes.set(raw.subarray(lo-offset,hi-offset),lo-start);}
 const headers={'Content-Type':m.type,'Content-Length':String(bytes.length),'Accept-Ranges':'bytes','Cache-Control':teacher?'no-store':'public, max-age=300','X-Content-Type-Options':'nosniff','Content-Disposition':`${m.type.includes('wordprocessing')?'attachment':'inline'}; filename="${slug}"`};if(status===206)headers['Content-Range']=`bytes ${start}-${end}/${m.size}`;
 return new Response(req.method==='HEAD'?null:bytes,{status,headers});
}
