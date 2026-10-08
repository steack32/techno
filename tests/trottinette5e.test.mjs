import assert from 'node:assert/strict';
import test from 'node:test';
import {trottinette5e as bank} from '../worker/trottinette5e.js';

const competence=n=>n===10?'Vert +':n>=8?'Vert':n>=4?'Jaune':'Rouge';

test('la banque 5e a 20 questions valides, dix par compétence',()=>{
  assert.equal(bank.level,'5e');
  assert.equal(bank.scoring,'competencies');
  assert.equal(bank.mode,'individual');
  assert.equal(bank.minutes,25);
  assert.equal(bank.bank.length,20);
  assert.deepEqual(bank.competencyOfSkill,[0,0,1,1]);
  assert.equal(bank.skills.length,4);
  assert.equal(bank.competencies.length,2);
  const counts=[0,0];
  bank.bank.forEach((variants,index)=>{
    assert.equal(variants.length,1);
    const [prompt,correct,wrong,explanation]=variants[0];
    assert.equal(typeof prompt,'string');
    assert.ok(prompt.length>8);
    assert.equal(wrong.length,3);
    assert.equal(new Set([correct,...wrong]).size,4);
    assert.equal(typeof explanation,'string');
    counts[bank.competencyOfSkill[Math.floor(index/5)]]++;
  });
  assert.deepEqual(counts,[10,10]);
});

test('les niveaux suivent le barème du site, sans note sur 20',()=>{
  assert.equal(competence(10),'Vert +');
  assert.equal(competence(9),'Vert');
  assert.equal(competence(8),'Vert');
  assert.equal(competence(7),'Jaune');
  assert.equal(competence(4),'Jaune');
  assert.equal(competence(3),'Rouge');
  assert.equal(competence(0),'Rouge');
});
