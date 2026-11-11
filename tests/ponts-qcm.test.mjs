import assert from 'node:assert/strict';
import {readFileSync,existsSync,writeFileSync} from 'node:fs';
import {registerHooks} from 'node:module';
import {DatabaseSync} from 'node:sqlite';
import {ponts5e,ponts5eAdapte} from '../worker/ponts-qcm.js';
import {python3e} from '../worker/python.js';
registerHooks({resolve(spec,ctx,next){if(spec==='cloudflare:workers')return {url:'data:text/javascript,export class DurableObject{constructor(ctx,env){this.ctx=ctx;this.env=env}}',shortCircuit:true};return next(spec,ctx)}});
const {EvaluationStore}=await import('../worker/index.js');
const db=new DatabaseSync(':memory:');
const sql={exec(query,...args){if(!args.length&&query.startsWith('CREATE')){db.exec(query);return{toArray:()=>[]}}const rows=db.prepare(query).all(...args);return{toArray:()=>rows}}};
const store=new EvaluationStore({storage:{sql,transactionSync:fn=>fn()}},{});
const password='local-test-ponts-only';
const hash=Buffer.from(await crypto.subtle.digest('SHA-256',new TextEncoder().encode('login:'+password))).toString('hex');
sql.exec('INSERT INTO settings VALUES(?,?)','passwordHash',hash);
sql.exec('INSERT INTO settings VALUES(?,?)','banks',JSON.stringify({legacy:python3e}));
sql.exec('INSERT INTO sessions VALUES(?,?,?,?)','legacy','LEGACY',JSON.stringify({id:'legacy',assessment:'legacy',label:'Existant',mode:'individual',open:false}),0);
let cookie='';
async function call(path,body,token,teacher=false){return store.fetch(new Request('https://test.invalid/api/evaluations'+path,{method:body===undefined?'GET':'POST',headers:{...(body===undefined?{}:{'Content-Type':'application/json'}),...(token?{Authorization:'Bearer '+token}:{}),...(teacher?{Cookie:cookie}:{})},body:body===undefined?undefined:JSON.stringify(body)}))}
const login=await call('/teacher/login',{password});assert.equal(login.status,200);cookie=login.headers.get('set-cookie').split(';')[0];
assert.equal((await call('/teacher')).status,401);
assert.ok(store.getBanks().legacy);assert.equal(store.getBanks().ponts5e.version,ponts5e.version);
assert.equal(ponts5e.bank.length,20);
for(const [[prompt,correct,wrong,explanation,media]] of ponts5e.bank){assert.ok(prompt&&explanation);assert.equal(new Set([correct,...wrong]).size,4);if(media?.image){assert.ok(existsSync('site'+media.image.src));if(!media.image.src.endsWith('.svg'))continue;const svg=readFileSync('site'+media.image.src,'utf8');assert.ok(svg.includes('viewBox'));assert.doesNotMatch(svg,/<script|<text/);}}
assert.equal((await call('/teacher/create',{assessment:'ponts5e',label:'Sans classe'},null,true)).status,400);
assert.equal((await call('/teacher/create',{assessment:'ponts5e',label:'Binôme',classe:'503',mode:'pair'},null,true)).status,400);
const session=await(await call('/teacher/create',{assessment:'ponts5e',label:'Ponts 503',classe:'503'},null,true)).json();
assert.equal(session.minutes,25);
assert.equal((await call('/join',{code:session.code,classe:'505',students:[{first:'Test',initial:'T'}]})).status,400);
let preview;
for(const [n,score] of [[20,20],[0,0],[13,13]]){
 const identity={code:session.code,classe:'503',students:[{first:['Alice','Benoît','Camille'][[20,0,13].indexOf(n)],initial:'T'}]};
 const joined=await(await call('/join',identity)).json();assert.ok(joined.token);const a=joined.attempt;
 assert.equal(a.questions.length,20);assert.equal(a.skills.length,5);assert.equal(a.pointsPerQuestion,1);
 for(let i=0;i<5;i++)assert.equal(a.questions.filter(q=>q.skill===i).length,4);
 assert.ok(a.questions.every(q=>!('correct'in q)&&!('explanation'in q)));
 assert.equal(a.questions.filter(q=>q.media?.image).length,9);assert.equal(a.questions.filter(q=>q.media?.table).length,1);
 assert.equal((await call('/join',identity)).status,409);
 const stored=JSON.parse(store.one('SELECT data FROM attempts WHERE id=?',a.id).data);
 assert.equal(stored.questions.filter(q=>q.competency===0).length,10);assert.equal(stored.questions.filter(q=>q.competency===1).length,10);
 const answers=Object.fromEntries(stored.questions.slice(0,n).map(q=>[q.id,q.correct]));
 assert.equal((await call('/save',{revision:0,answers},joined.token)).status,200);
 assert.equal((await call('/save',{revision:0,answers},joined.token)).status,409);
 const resumed=await(await call('/state',undefined,joined.token)).json();assert.deepEqual(resumed.answers,answers);
 const finished=await(await call('/finish',{revision:1},joined.token)).json();assert.equal(finished.result.total,score);assert.equal(finished.reveal,false);
 assert.equal((await(await call('/save',{revision:1,answers:{}},joined.token)).json()).result.total,score);
 if(n===20)preview={attempt:a,finished,stored,token:joined.token,session};
}
const csv=await(await call('/teacher/export?session='+session.id,undefined,null,true)).text();assert.ok(csv.includes('"20"'));assert.ok(csv.includes('"13"'));assert.ok(csv.includes('"0"'));
assert.equal((await call('/teacher/reveal',{session:session.id},null,true)).status,409);
await call('/teacher/close',{session:session.id},null,true);await call('/teacher/reveal',{session:session.id},null,true);
const revealed=await(await call('/state',undefined,preview.token)).json();assert.ok(revealed.questions.every(q=>q.correct&&q.explanation));
assert.equal(store.session('legacy').label,'Existant');
if(process.env.PONTS_PREVIEW_FILE)writeFileSync(process.env.PONTS_PREVIEW_FILE,JSON.stringify({...preview,revealed}));
console.log('PASS QCM ponts: 20 questions, 5 parties, 4 photos, 5 schémas, notes 0/13/20, reprise, CSV, clôture/corrigé, conservation des anciennes séances.');

assert.doesNotMatch(JSON.stringify(ponts5e.bank),/flambement/i);
assert.equal(store.getBanks().ponts5eAdapte.version,ponts5eAdapte.version);
assert.equal(ponts5eAdapte.bank.length,10);
for(const [[prompt,correct,wrong,explanation]] of ponts5eAdapte.bank){assert.ok(prompt&&explanation);assert.ok([2,3].includes(new Set([correct,...wrong]).size));}
const adapted=await(await call('/teacher/create',{assessment:'ponts5eAdapte',label:'Ponts adapté 503',classe:'503'},null,true)).json();
assert.notEqual(adapted.code,session.code);
for(const n of [0,5,10]){
 const joined=await(await call('/join',{code:adapted.code,classe:'503',students:[{first:({0:'David',5:'Emma',10:'Farid'})[n],initial:'T'}]})).json();
 const a=joined.attempt;assert.equal(a.questions.length,10);assert.equal(a.pointsPerQuestion,2);
 assert.ok(a.questions.every(q=>[2,3].includes(q.choices.length)&&!('correct'in q)));
 for(let i=0;i<5;i++)assert.equal(a.questions.filter(q=>q.skill===i).length,2);
 const stored=JSON.parse(store.one('SELECT data FROM attempts WHERE id=?',a.id).data);
 const answers=Object.fromEntries(stored.questions.slice(0,n).map(q=>[q.id,q.correct]));
 assert.equal((await call('/save',{revision:0,answers},joined.token)).status,200);
 const finished=await(await call('/finish',{revision:1},joined.token)).json();
 assert.equal(finished.result.total,n*2);assert.equal(finished.result.skills.reduce((s,c)=>s+c.max,0),20);
 if(n===10&&process.env.ADAPTE_PREVIEW_FILE)writeFileSync(process.env.ADAPTE_PREVIEW_FILE,JSON.stringify({attempt:a,finished,stored,token:joined.token,session:adapted}));
}
const adaptedCsv=await(await call('/teacher/export?session='+adapted.id,undefined,null,true)).text();
for(const score of [0,10,20])assert.ok(adaptedCsv.includes('"'+score+'"'));
console.log('PASS parcours adapté: 10 questions, 2/3 choix, 5 parties, code distinct, notes 0/10/20 et export.');
