import assert from 'node:assert/strict';
import {calculate} from '../site/4eme/materiaux/model.js';
import {content,titles,labels} from '../site/4eme/materiaux/content.js';
const ref=calculate();
assert.ok(Math.abs(ref.deflection-1.4882133333333334)<1e-10);assert.ok(Math.abs(ref.mass-1.8)<1e-10);
assert.ok(ref.pass);assert.equal(calculate({load:0}).deflection,0);
assert.ok(Math.abs(calculate({thickness:30}).deflection-ref.deflection/8)<1e-10);
assert.ok(Math.abs(calculate({span:40}).deflection-ref.deflection/8)<1e-10);
assert.ok(Math.abs(calculate({load:20}).deflection-ref.deflection*2)<1e-10);
const full=calculate({material:'aluminium',thickness:20}),hollow=calculate({material:'aluminium',thickness:20,shape:'creux'});
assert.ok(hollow.mass<full.mass);assert.ok(hollow.deflection>full.deflection);assert.ok(hollow.pass);
assert.throws(()=>calculate({material:'bois',shape:'creux'}));assert.throws(()=>calculate({thickness:-1}));
let passing=0;for(const material of ['bois','aluminium','acier'])for(const thickness of [10,15,20,25,30])for(const shape of material==='bois'?['plein']:['plein','creux']){const r=calculate({material,thickness,shape});assert.ok(Number.isFinite(r.deflection)&&r.mass>0);if(r.pass)passing++;}assert.ok(passing>=2);
const pages=content();assert.equal(pages.length,4);assert.equal(titles.length,4);const ids=[];
for(const [i,page] of pages.entries())for(const m of page.matchAll(/id="(s\d_[^"]+)"/g)){assert.ok(m[1].startsWith('s'+(i+1)+'_'));assert.ok(labels[m[1]]);ids.push(m[1]);}
assert.equal(ids.length,new Set(ids).size);
console.log(`PASS : physique, contraintes, ${passing} solutions possibles, quatre séances, ${ids.length} réponses distinctes`);
