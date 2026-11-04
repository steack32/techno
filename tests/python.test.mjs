import assert from 'node:assert/strict';
import {registerHooks} from 'node:module';
import {DatabaseSync} from 'node:sqlite';
import {python4e,python3e} from '../worker/python.js';
registerHooks({resolve(spec,ctx,next){if(spec==='cloudflare:workers')return{url:'data:text/javascript,export class DurableObject{constructor(ctx,env){this.ctx=ctx;this.env=env}}',shortCircuit:true};return next(spec,ctx)}});
const {EvaluationStore}=await import('../worker/index.js');
const db=new DatabaseSync(':memory:');
const sql={exec(query,...args){if(!args.length&&query.startsWith('CREATE')){db.exec(query);return{toArray:()=>[]}}return{toArray:()=>db.prepare(query).all(...args)}}};
// Cloudflare executes even INSERT/UPDATE statements eagerly.
const oldExec=sql.exec;sql.exec=(...args)=>{const rows=oldExec(...args).toArray();return{toArray:()=>rows}};
const store=new EvaluationStore({storage:{sql,transactionSync:fn=>fn()}},{});
const password='test-only-password-for-python';
const hash=Buffer.from(await crypto.subtle.digest('SHA-256',new TextEncoder().encode('login:'+password))).toString('hex');
sql.exec('INSERT INTO settings VALUES(?,?)','passwordHash',hash);
sql.exec('INSERT INTO settings VALUES(?,?)','banks',JSON.stringify({legacy:{...python3e,title:'Existing assessment'}}));
const oldPython=JSON.parse(JSON.stringify(python3e).replaceAll('for _ in range(', 'for i in range('));
delete oldPython.version;
sql.exec('UPDATE settings SET value=? WHERE key=?',JSON.stringify({legacy:{...python3e,title:'Existing assessment'},python3e:oldPython,python4e:{...oldPython,level:'4e',scoring:'competencies'}}),'banks');
// Existing sessions prevent historical first-install defaults from being created.
sql.exec('INSERT INTO sessions VALUES(?,?,?,?)','legacy','LEGACYCODE',JSON.stringify({id:'legacy',assessment:'legacy',label:'Existing',mode:'individual',open:false}),0);
let cookie='';
async function call(path,body,token,teacher=false){return store.fetch(new Request('https://test.invalid/api/evaluations'+path,{method:body===undefined?'GET':'POST',headers:{...(body===undefined?{}:{'Content-Type':'application/json'}),...(token?{Authorization:'Bearer '+token}:{}),...(teacher?{Cookie:cookie}:{})},body:body===undefined?undefined:JSON.stringify(body)}))}
let r=await call('/teacher/login',{password});assert.equal(r.status,200);cookie=r.headers.get('set-cookie').split(';')[0];
assert.equal((await call('/teacher')).status,401);
const banks=await(await call('/teacher',undefined,undefined,true)).json();assert.ok(banks.assessments.some(b=>b.id==='legacy'));assert.ok(banks.assessments.some(b=>b.id==='python4e'));
for(const bank of [python4e,python3e]){assert.equal(bank.bank.length,10);for(const [[prompt,correct,wrong,explain]] of bank.bank){assert.equal(new Set([correct,...wrong]).size,4);assert.ok(explain);assert.doesNotMatch(prompt+correct+wrong.join(),/walk\(|jump\(|get_height|read_number/);}}
assert.equal((await call('/teacher/create',{assessment:'python4e',label:'Sans classe'},undefined,true)).status,400);
assert.equal((await call('/teacher/create',{assessment:'python4e',label:'Binôme',classe:'401',mode:'pair'},undefined,true)).status,400);
let codes=[];
for(const [assessment,classe] of [['python3e','301'],['python4e','401']]){
 const session=await(await call('/teacher/create',{assessment,classe,label:'Python '+classe},undefined,true)).json();codes.push(session.code);
 assert.equal((await call('/session?code=INVALIDE')).status,404);
 assert.equal((await call('/join',{code:session.code,classe:classe[0]+'02',students:[{first:'Camille',initial:'T'}]})).status,400);
 const identity={code:session.code,classe,students:[{first:'Camille',initial:'T'}]};
 const joined=await(await call('/join',identity)).json();assert.ok(joined.token);const a=joined.attempt;
 assert.equal(a.questions.length,10);assert.equal(a.pointsPerQuestion,2);assert.equal(a.skills.length,2);assert.equal(a.scoring,assessment==='python4e'?'competencies':'points');
 assert.ok(a.questions.every(q=>!('correct'in q)&&!('explanation'in q)));
 assert.equal((await call('/join',identity)).status,409);
 const stored=JSON.parse(store.one('SELECT data FROM attempts WHERE id=?',a.id).data);
 const answers=Object.fromEntries(stored.questions.map(q=>[q.id,q.correct]));
 r=await call('/save',{revision:0,answers},joined.token);assert.equal(r.status,200);
 assert.equal((await call('/save',{revision:0,answers},joined.token)).status,409);
 const finished=await(await call('/finish',{revision:1},joined.token)).json();assert.equal(finished.result.total,20);assert.deepEqual(finished.result.skills.map(s=>s.level),['Très bonne maîtrise','Très bonne maîtrise']);assert.equal(finished.reveal,false);
 const csv=await(await call('/teacher/export?session='+session.id,undefined,undefined,true)).text();assert.ok(csv.includes('Très bonne maîtrise'));assert.equal(csv.split('\r\n')[1].split(';')[5],assessment==='python4e'?'""':'"20"');
 assert.equal((await call('/teacher/reveal',{session:session.id},undefined,true)).status,409);
 await call('/teacher/close',{session:session.id},undefined,true);
 assert.equal((await call('/join',{...identity,students:[{first:'Autre',initial:'T'}]})).status,409);
 await call('/teacher/reveal',{session:session.id},undefined,true);
 const revealed=await(await call('/state',undefined,joined.token)).json();assert.ok(revealed.questions.every(q=>q.correct&&q.explanation));
 // Exact mastery boundaries, using the actual API grading implementation.
 for(const [correctCount,expected] of [[0,'Maîtrise insuffisante'],[1,'Maîtrise insuffisante'],[2,'Maîtrise fragile'],[3,'Maîtrise fragile'],[4,'Maîtrise satisfaisante'],[5,'Très bonne maîtrise']]){
  const fake={...stored,finished:Date.now(),answers:Object.fromEntries([0,1].flatMap(skill=>stored.questions.filter(q=>q.skill===skill).slice(0,correctCount).map(q=>[q.id,q.correct])))};
  const result=store.safeAttempt(fake,assessment==='python3e'?python3e:python4e,session).result;
  assert.equal(result.total,correctCount*4);assert.ok(result.skills.every(s=>s.level===expected));
 }
}
assert.notEqual(codes[0],codes[1]);
assert.ok(store.getBanks().legacy);
assert.equal(store.getBanks().python3e.version,python3e.version);
assert.doesNotMatch(JSON.stringify(store.getBanks().python3e),/for i in range/);
const saved={finished:null,questions:[{id:'q',prompt:'for i in range(3):',choices:[{id:'c',label:'for i in range(5):'}],correct:'c'}]};
const displayed=store.safeAttempt(saved,python3e,{assessment:'python3e'});
assert.equal(displayed.questions[0].prompt,'for _ in range(3):');
assert.deepEqual(displayed.questions[0].choices,[{id:'c',label:'for _ in range(5):'}]);
assert.equal(saved.questions[0].prompt,'for i in range(3):');
console.log('PASS Python: 10 questions FR, two levels, codes/classes, authentication, save/revision, scores/mastery, CSV, closing/reveal, existing data retained');
