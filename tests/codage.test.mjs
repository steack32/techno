import assert from 'node:assert/strict';
import {courses} from '../site/codage/content.js';
import {assess} from '../site/objective.js';
for(const [level,course] of Object.entries(courses)){
 assert.equal(course.sessions.length,3);
 for(const session of course.sessions){
  assert.equal(session.questions.length,10);
  for(const q of session.questions){assert.equal(assess('',q).state,'retry');assert.equal(assess(String(q.answer),q).state,'good');if(q.choices){assert.equal(new Set(q.choices).size,q.choices.length);for(const wrong of q.choices.filter(v=>v!==q.answer))assert.equal(assess(wrong,q).state,'retry')}else assert.equal(assess(String(q.answer+1),q).state,'retry')}
  if(session.lab.type==='pixels'){assert.equal(session.lab.patterns.length,8);assert(session.lab.patterns.every(r=>/^[01]{8}$/.test(r)))}
 }
}
// Check quantities independently of the answer-assessment implementation.
assert.equal(courses['4eme'].sessions[2].questions[9].answer,16*16/8);
assert.equal(courses['3eme'].sessions[0].questions[5].answer,Math.ceil(Math.log2(12)));
assert.equal(courses['3eme'].sessions[1].questions[7].answer,4*8/64);
assert.equal(courses['3eme'].sessions[2].questions[7].answer,20*10*24/8);
console.log('PASS : 6 séances, 60 questions fermées, corrigés et calculs de codage.');
