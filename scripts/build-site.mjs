import { copyFileSync, cpSync, mkdirSync, rmSync, writeFileSync, readFileSync, statSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const out = resolve(root, 'dist');
// Explicit student-only allowlist. Never copy the repository root or teacher folders.
const lessons = [
  { level: '5e', title: 'Un objet du quotidien', folder: '5e/objet-du-quotidien', text: 'Observer un objet et comprendre à quel besoin il répond.', guided: true },
  { level: '4e', title: 'Un éclairage automatique', folder: '4e/eclairage-automatique', text: 'Explorer les capteurs et les règles de commande.' },
  { level: '3e', title: 'Un portail, deux chaînes', folder: '3e/chaines-information-energie', text: 'Suivre les informations et les transferts d’énergie.' }
];
const files = lessons.flatMap(l => [
  `${l.folder}/eleves/sur-pc/ressources.html`,
  `${l.folder}/eleves/a-imprimer/fiche-eleve.pdf`,
  ...(l.guided ? [`${l.folder}/eleves/sur-pc/observation-guidee.html`, `${l.folder}/eleves/a-imprimer/parcours-guide.pdf`] : [])
]);
// Fail before cleaning the previous build if any source is missing.
for (const file of files) {
  if (!statSync(resolve(root, file)).isFile()) throw new Error(`Fichier manquant : ${file}`);
}
const template = readFileSync(resolve(root, 'site/index.html'), 'utf8');
rmSync(out, { recursive: true, force: true });
mkdirSync(out, { recursive: true });
for (const file of files) {
  const dest = resolve(out, file);
  mkdirSync(dirname(dest), { recursive: true });
  copyFileSync(resolve(root, file), dest);
}
const cards = lessons.map(l => `<article><span class="level">${l.level}</span><h2>${l.title}</h2><p>${l.text}</p><a class="button" href="/${l.folder}/eleves/sur-pc/ressources.html">Ouvrir l’activité <span aria-hidden="true">→</span></a><a class="sheet" href="/${l.folder}/eleves/a-imprimer/fiche-eleve.pdf">Fiche élève · PDF</a>${l.guided ? `<details><summary>Parcours guidé</summary><a class="sheet" href="/${l.folder}/eleves/sur-pc/observation-guidee.html">Activité accompagnée</a><a class="sheet" href="/${l.folder}/eleves/a-imprimer/parcours-guide.pdf">Fiche accompagnée · PDF</a></details>` : ''}</article>`).join('\n');
writeFileSync(resolve(out, 'index.html'), template.replace('<!-- LESSONS -->', cards));
cpSync(resolve(root, 'site/evaluations'), resolve(out, 'evaluations'), { recursive: true });
cpSync(resolve(root, 'site/professeur'), resolve(out, 'professeur'), { recursive: true });
writeFileSync(resolve(out, '404.html'), '<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page introuvable</title><main><h1>Page introuvable</h1><p>Cette ressource n’est pas disponible.</p><a href="/">Revenir aux activités</a></main></html>');
writeFileSync(resolve(out, '_headers'), '/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n');
console.log(`Site prêt : ${files.length} ressources élèves ; aucun dossier professeur publié.`);
