import assert from 'node:assert/strict';
import {assess} from '../site/objective.js';
import {activities,renderActivity} from '../site/digital-activities.js';
import {calculate} from '../site/4eme/materiaux/model.js';
const decode=s=>s.replace(/&quot;/g,'"').replace(/&#39;/g,"'").replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&');
let count=0;
for(const file of ['5eme/ponts/content.js','5eme/ponts/guided-content.js','4eme/materiaux/content.js']){
 const {content,labels}=await import('../site/'+file);const html=content().join('');
 assert.ok(!/<textarea|contenteditable|type="text"/.test(html),file+' has open fields');
 const ids=[...html.matchAll(/id="([^"]+)" data-answer/g)].map(m=>m[1]);
 assert.equal(new Set(ids).size,ids.length);assert.ok(Object.keys(labels).length<=180,'legacy and new answers fit server limit');
 for(const id of ids){assert.ok(labels[id]);assert.match(id,/^s[1-5]_[a-z0-9_]{1,50}$/);}
 for(const [id,label] of Object.entries(labels))if(label.startsWith('Ancienne réponse'))assert.ok(!ids.includes(id),'old response must not be overwritten by new fields');
 // Every question is either self-checking, read-only generated output, a task checklist,
 // or an association covered by a group checker. No uncorrected knowledge selects.
 const grouped=new Set([...html.matchAll(/data-ids="([^"]+)"/g)].flatMap(m=>m[1].split(',')));
 for(const m of html.matchAll(/<div class="question"><label for="([^"]+)">[^<]*<\/label><select/g))assert.ok(grouped.has(m[1]),m[1]+' lacks correction');
 validate(html);
}
for(const name of Object.keys(activities))validate(renderActivity(name));
function validate(html){for(const [,raw] of html.matchAll(/data-spec="([^"]+)"/g)){
 const s=JSON.parse(decode(raw));count++;
 assert.equal(assess('',s).state,'retry');
 if(s.observation){assert.equal(assess(s.type==='number'?'125':s.choices[0],s).state,'recorded');continue;}
 if(s.type==='number'){assert.equal(assess(String(s.answer),s).state,'good');assert.equal(assess('NaN',s).state,'retry');assert.equal(assess(String(s.answer+100),s).state,'retry');}
 else {assert.ok(s.choices.includes(s.answer));assert.equal(assess(s.answer,s).state,'good');for(const wrong of s.choices.filter(v=>v!==s.answer))assert.equal(assess(wrong,s).state,'retry');}
 assert.ok(s.explanation);
}}
assert.equal(assess('0',{type:'number',answer:0}).state,'good');
assert.equal(assess('-1',{type:'number',observation:true}).state,'retry');
const ref=calculate();assert.equal(ref.mass/calculate({span:40}).mass,2);assert.ok(Math.abs(ref.deflection/calculate({thickness:30}).deflection-8)<1e-10);
console.log(`PASS : ${count} self-checks; blank, wrong, right, numeric and observed answers; legacy keys preserved; no free response fields.`);
