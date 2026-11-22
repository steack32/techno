import assert from 'node:assert/strict';
import {registerHooks} from 'node:module';
import {DatabaseSync} from 'node:sqlite';

registerHooks({resolve(spec, context, next) {
  if (spec === 'cloudflare:workers') return {url:'data:text/javascript,export class DurableObject{constructor(ctx,env){this.ctx=ctx;this.env=env}}',shortCircuit:true};
  return next(spec,context);
}});
const {default: worker, EvaluationStore} = await import('../worker/index.js');
const db = new DatabaseSync(':memory:');
const sql = {exec(query, ...args) {
  if (!args.length && query.startsWith('CREATE')) { db.exec(query); return {toArray:() => []}; }
  const rows = db.prepare(query).all(...args);
  return {toArray:() => rows};
}};
const ctx = {storage:{sql,transactionSync(callback) {
  db.exec('BEGIN');
  try { const value = callback(); db.exec('COMMIT'); return value; }
  catch (error) { db.exec('ROLLBACK'); throw error; }
}}};
let store = new EvaluationStore(ctx,{});
const env = {EVALUATIONS:{getByName(name) { assert.equal(name,'college-v1'); return store; }}};
const base = '/api/mini-jeux', admin = '/api/evaluations/teacher/mini-jeux';
const origin = 'https://college.example';
const cookie = 'techno_teacher=' + 'a'.repeat(64);
sql.exec('INSERT INTO auth VALUES(?,?)','a'.repeat(64),Date.now()+60000);
const form = {
  classe:'301', firstA:'Élia', firstB:'Noé', requestId:crypto.randomUUID(), title:'',
  html:'<!doctype html><html lang="fr"><head><title>Étoiles &amp; lunes</title></head><body><button id="point">0</button><script>let score=0;document.getElementById("point").onclick=()=>document.getElementById("point").textContent=++score;</script></body></html>'
};
function call(path, data, headers = {}, method = data === undefined ? 'GET' : 'POST') {
  return worker.fetch(new Request(origin + path, {
    method, headers:{...(data === undefined ? {} : {'Content-Type':'application/json',Origin:origin}),...headers},
    ...(data === undefined ? {} : {body:JSON.stringify(data)})
  }),env);
}
assert.deepEqual(await (await call(base)).json(),{jeux:[], avant:null, classes:[], ouvert:true});
assert.equal((await call(base + '/depot')).status,200);
assert.equal((await call(admin)).status,401);
assert.equal((await call(admin + '/depot',{ouvert:false})).status,401);
assert.equal((await call(base,{...form, firstB:''})).status,400);
assert.equal((await call(base,{...form, html:'pas un document'})).status,400);
assert.equal((await call(base,{...form, html:'<!-- document incomplet'})).status,400);
assert.equal((await call(base,{...form, html:'<html>' + 'é'.repeat(270000) + '</html>'})).status,413);
assert.equal((await call(base,form,{'Content-Type':'text/plain'})).status,415);
assert.equal((await call(base,form,{Origin:'null'})).status,403);
assert.equal((await call(base,form,{Origin:'https://exemple.invalid'})).status,403);
assert.equal((await call(base,form,{'Sec-Fetch-Site':'cross-site'})).status,403);
const submitted = await call(base,form); assert.equal(submitted.status,201);
const saved = await submitted.json();
assert.equal(saved.title,'Étoiles & lunes'); assert.equal(saved.classe,'301');
assert.equal((await call(base,form)).status,200);
assert.equal((await call(base,{...form, title:'Un autre jeu'})).status,409);
store = new EvaluationStore(ctx,{});
const list = await (await call(base)).json(); assert.equal(list.jeux.length,1);
const detail = await (await call(base + '/' + saved.id)).json();
for (const item of [detail, list.jeux[0]]) {
  assert.deepEqual(Object.keys(item).sort(),['classe','created','id','title']);
  assert.equal(item.title,'Étoiles & lunes');
}
assert.deepEqual(Object.keys(saved).sort(),['classe','id','title']);
const contentURL = base + '/' + saved.id + '/contenu';
const framed = await call(contentURL,undefined,{'Sec-Fetch-Dest':'iframe','Sec-Fetch-Site':'same-origin'});
assert.equal(await framed.text(),form.html);
const policy = framed.headers.get('Content-Security-Policy');
assert.match(policy,/^sandbox allow-scripts;/); assert.doesNotMatch(policy,/allow-same-origin/);
for (const value of ["connect-src 'none'", "form-action 'none'", "frame-src 'none'", "frame-ancestors 'self'"]) assert.ok(policy.includes(value));
assert.equal(framed.headers.get('X-Content-Type-Options'),'nosniff');
const redirect = await call(contentURL,undefined,{'Sec-Fetch-Dest':'document'});
assert.equal(redirect.status,303); assert.equal(redirect.headers.get('Location'),'/mini-jeux/jouer/?id=' + saved.id);
assert.equal((await call(contentURL)).status,403);
assert.equal((await call(contentURL,undefined,{'Sec-Fetch-Dest':'iframe','Sec-Fetch-Site':'cross-site'})).status,403);
const teacherGames = await (await call(admin,undefined,{Cookie:cookie})).json();
assert.equal(teacherGames.jeux[0].firstA,form.firstA); assert.equal(teacherGames.jeux[0].firstB,form.firstB);
assert.equal((await call(admin + '/depot',{ouvert:false},{Cookie:cookie})).status,200);
assert.deepEqual(await (await call(base + '/depot')).json(),{ouvert:false});
assert.equal((await call(base,{...form,requestId:crypto.randomUUID()})).status,403);
assert.equal((await call(base,form)).status,200); // Receipt for a previously successful submission survives closing.
assert.equal((await call(base + '/' + saved.id)).status,200);
await call(admin + '/depot',{ouvert:true},{Cookie:cookie});
for (let n = 0; n < 26; n++) {
  const result = await call(base,{...form, title:'Parcours ' + n, classe:'4e B', requestId:crypto.randomUUID()});
  assert.equal(result.status,201);
}
const p1 = await (await call(base + '?classe=4e%20B')).json(); assert.equal(p1.jeux.length,24); assert.ok(p1.avant);
const p2 = await (await call(base + '?classe=4e%20B&avant=' + p1.avant)).json();
assert.equal(p2.jeux.length,2); assert.equal(p2.avant,null);
assert.equal(new Set([...p1.jeux,...p2.jeux].map(game => game.id)).size,26);
assert.deepEqual(p1.classes,['301','4e B']);
assert.equal((await call(base + '?avant=abc')).status,400);
assert.equal((await call(admin + '/retirer',{id:saved.id,confirm:true})).status,401);
assert.equal((await call(admin + '/retirer',{id:saved.id,confirm:false},{Cookie:cookie})).status,400);
assert.equal((await call(admin + '/retirer',{id:saved.id,confirm:true},{Cookie:cookie})).status,200);
assert.equal((await call(base + '/' + saved.id)).status,404);
assert.equal((await call(contentURL,undefined,{'Sec-Fetch-Dest':'iframe'})).status,404);
assert.equal((await (await call(base + '?classe=301')).json()).jeux.length,0);
const withComments = await call(base,{...form,requestId:crypto.randomUUID(),html:'<!-- activité -->\n<!-- jeu -->\n<html><body>Départ</body></html>'});
assert.equal(withComments.status,201);
assert.equal((await withComments.json()).title,'Jeu de la classe 301');
console.log('PASS mini-jeux : double envoi, conservation, confidentialité, lecture isolée, classes, pagination, fermeture et retrait professeur.');
