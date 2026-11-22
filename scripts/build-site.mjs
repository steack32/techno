import {copyFileSync,cpSync,mkdirSync,rmSync,writeFileSync,readFileSync,statSync} from 'node:fs';
import {dirname,resolve} from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..'),out=resolve(root,'dist');
const catalog=JSON.parse(readFileSync(resolve(root,'site/catalogue.json'),'utf8'));
const levels=['5eme','4eme','3eme'];
const label=level=>level[0]+'e';
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const path=l=>`/${l.level}/${l.slug}/`;
const files=l=>[...new Set([...(l.sessions||[]).map(s=>s.pdf),'eleves/sur-pc/ressources.html','eleves/a-imprimer/fiche-eleve.pdf',...(l.guided?['eleves/sur-pc/observation-guidee.html','eleves/a-imprimer/parcours-guide.pdf']:[])])];
// Only the explicitly listed pupil resources are published; teacher files stay private.
const seen=new Set();for(const l of catalog){if(!levels.includes(l.level)||!/^[a-z0-9-]+$/.test(l.slug)||seen.has(path(l)))throw Error('Entrée de catalogue incorrecte');seen.add(path(l));for(const f of l.source?files(l).map(f=>l.source+'/'+f):[l.page])if(!statSync(resolve(root,f)).isFile())throw Error('Source manquante : '+f);}
const nav=`<nav class="site-nav" aria-label="Navigation principale"><a class="site-brand" href="/">Mon espace techno</a><div class="site-links"><details class="level-menu"><summary>Niveaux</summary><div>${levels.map(l=>`<a href="/${l}/">${label(l)}</a>`).join('')}</div></details><a href="/mini-jeux/">Mini-jeux</a><a href="/evaluations/">Contrôles</a></div></nav>`;
const arcadeCard='<aside class="portal-note arcade-entry" data-resource data-keywords="minijeux jeux vidéo HTML IA intelligence artificielle ChatGPT Gemini"><h2>Atelier mini-jeux</h2><p>Publie le jeu HTML de ton binôme et essaie ceux des autres classes.</p><a href="/mini-jeux/deposer/">Déposer un jeu</a> · <a href="/mini-jeux/">Voir la galerie</a></aside>';
const footer='<footer class="portal-footer">Espace élèves · Technologie<br><a href="/professeur/">Espace professeur</a></footer>';
const crumbs=(l,activity)=>`<nav class="breadcrumbs" aria-label="Fil d’Ariane"><a href="/">Accueil</a> / <a href="/${l.level}/">${label(l.level)}</a> / ${activity ? `<a href="${path(l)}">${esc(l.title)}</a> / <span aria-current="page">${esc(activity)}</span>` : `<span aria-current="page">${esc(l.title)}</span>`}</nav>`;
const page=(title,body)=>`<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(title)} · Technologie</title><link rel="stylesheet" href="/navigation.css"></head><body class="portal">${nav}<main>${body}</main>${footer}</body></html>`;
const write=(file,body)=>{const p=resolve(out,file);mkdirSync(dirname(p),{recursive:true});writeFileSync(p,body);};
const enhance=(html,l,activity)=>html.replace('</head>','<link rel="stylesheet" href="/navigation.css"></head>').replace(/<body([^>]*)>/,`<body$1>${nav}`).replace(/<main([^>]*)>/,`<main$1>${crumbs(l,activity)}`).replaceAll('href="/3e/','href="/3eme/').replaceAll('href="/4e/','href="/4eme/').replaceAll('href="/5e/','href="/5eme/');
rmSync(out,{recursive:true,force:true});mkdirSync(out,{recursive:true});
for(const file of ['navigation.css','catalogue.js','objective.js','objective-questions.js','digital-activities.js'])copyFileSync(resolve(root,'site',file),resolve(out,file));
const levelCards = levels.map(level => {
  const count = catalog.filter(lesson => lesson.level === level).length;
  const plural = count > 1 ? 's' : '';
  return `<article class="portal-card"><h2>${label(level)}</h2>
    <p>${count} séquence${plural} disponible${plural}</p>
    <a class="portal-button" href="/${level}/">Cours de ${label(level)}</a></article>`;
});
write('index.html', page('Mon espace techno', `
  <h1>Choisis ton niveau</h1><p>Retrouve la séance indiquée par ton professeur.</p>
  <section class="portal-grid" aria-label="Niveaux">${levelCards.join('')}</section>
  ${arcadeCard}
  <aside class="portal-note"><h2>Tu as un contrôle ?</h2><p>Prépare le code donné par ton professeur.</p>
    <a href="/evaluations/">Commencer un contrôle</a></aside>`));

const assessmentTopics = {
  '5eme': 'Les ponts ou la trottinette électrique',
  '4eme': 'Python (Py-rates, niveaux 1 à 5) ou la trottinette électrique',
  '3eme': 'Python (Py-rates, niveaux 1 à 5) ou Mission Savon',
};
for (const level of levels) {
  const lessons = catalog.filter(lesson => lesson.level === level);
  const arcade = level === '5eme' ? '' : arcadeCard;
  const resources = lessons.length + 1 + (arcade ? 1 : 0);
  const cards = lessons.map((lesson, index) => {
    const bridges = lesson.slug === 'ponts';
    return `<article class="portal-card" data-sequence data-resource>
      <span class="portal-tag">Séquence ${index + 1} · ${lesson.count || 1} séance${lesson.count > 1 ? 's' : ''}</span>
      <h2>${esc(lesson.title)}</h2><p>${esc(lesson.description)}</p>
      <a class="portal-button" href="${path(lesson)}" aria-label="${bridges ? 'Parcours normal des ponts' : 'Ouvrir la séquence ' + esc(lesson.title)}">${bridges ? 'Parcours normal' : 'Ouvrir la séquence'}</a>
      ${bridges ? '<p><a class="portal-button" href="/5eme/ponts-guides/">Parcours guidé</a></p>' : ''}
    </article>`;
  });
  write(level + '/index.html', page('Les ressources de ' + label(level), `
    <nav class="breadcrumbs" aria-label="Fil d’Ariane"><a href="/">Accueil</a> / <span aria-current="page">${label(level)}</span></nav>
    <h1>Les ressources de ${label(level)}</h1>
    <div class="portal-search">
      <label for="sequence-search">Rechercher une ressource</label>
      <div class="search-controls"><input id="sequence-search" type="search" placeholder="Un titre, un thème…">
      <button id="clear-search" type="button" hidden>Effacer la recherche</button></div>
    </div>
    <p id="search-status" role="status">${resources} ressources disponibles</p>
    <section class="portal-grid" aria-label="Séquences">${cards.join('')}</section>
    ${arcade}
    <aside class="portal-note" data-resource data-keywords="évaluations contrôles QCM${level !== '5eme' ? ' pyrates' : ''}">
      <h2>Contrôles de ${label(level)}</h2>
      <p>${assessmentTopics[level]}. Prépare le code donné en classe.</p>
      <a href="/evaluations/">Accéder à l’évaluation</a>
    </aside>
    <script src="/catalogue.js" defer></script>`));
}
for(const l of catalog){const dest=l.level+'/'+l.slug;
 if(l.page){let html=readFileSync(resolve(root,l.page),'utf8').replace(/<header class="top">[\s\S]*?<\/header>/,'');html=html.replace('href="/">Toutes les séquences','href="/'+l.level+'/">Toutes les séquences');write(dest+'/index.html',enhance(html,l));for(const asset of l.assets||[]){if(!/^[a-zA-Z0-9_./-]+$/.test(asset)||asset.includes('..')||asset.startsWith('/'))throw Error('Asset non valide');const target=resolve(out,dest,asset);mkdirSync(dirname(target),{recursive:true});copyFileSync(resolve(root,dirname(l.page),asset),target);}}
 else{for(const file of files(l)){const source=resolve(root,l.source,file),target=dest+'/'+file;if(file.endsWith('.html'))write(target,enhance(readFileSync(source,'utf8'),l,file.endsWith('observation-guidee.html')?'Activité guidée':'Activité sur ordinateur'));else{mkdirSync(dirname(resolve(out,target)),{recursive:true});copyFileSync(source,resolve(out,target));}}
 if(l.sessions){write(dest+'/index.html',page(l.title,`${crumbs(l)}<span class="portal-tag">${label(l.level)} · Séquence</span><h1>${esc(l.title)}</h1><p>${esc(l.description)}</p><section class="portal-grid" aria-label="Séances">${l.sessions.map((s,i)=>`<article class="portal-card"><span class="portal-tag">Séance ${i+1}</span><h2>${esc(s.title)}</h2><p>${esc(s.description)}</p><a class="portal-button" href="${path(l)}eleves/sur-pc/ressources.html#digital-${i===0?'chain':'portal'}">Ouvrir l’activité interactive →</a><p><a href="${path(l)}${esc(s.pdf)}">Fiche élève · PDF recto verso</a></p></article>`).join('')}</section><aside class="portal-note"><strong>Observer et simuler</strong><p><a href="${path(l)}eleves/sur-pc/ressources.html">Observer le portail et tester sa fermeture →</a></p></aside>`));}
 else write(dest+'/index.html',page(l.title,`${crumbs(l)}<span class="portal-tag">${label(l.level)} · Séquence</span><h1>${esc(l.title)}</h1><p>${esc(l.description)}</p><section class="portal-card"><span class="portal-tag">Séance 1 · 55 minutes</span><h2>${esc(l.session)}</h2><p>Travaille en binôme sur ordinateur. Conserve la fiche dans ton porte-vues.</p><p><a class="portal-button" href="${path(l)}eleves/sur-pc/ressources.html">Ouvrir l’activité →</a></p><p><a href="${path(l)}eleves/a-imprimer/fiche-eleve.pdf">Fiche élève à imprimer · PDF</a></p>${l.guided?`<details><summary>Parcours accompagné</summary><p><a href="${path(l)}eleves/sur-pc/observation-guidee.html">Ouvrir l’activité guidée</a></p><p><a href="${path(l)}eleves/a-imprimer/parcours-guide.pdf">Fiche accompagnée · PDF</a></p></details>`:''}</section>`));}
}
mkdirSync(resolve(out,'5eme/ponts-guides'),{recursive:true});
write('5eme/ponts-guides/index.html',enhance(readFileSync(resolve(root,'site/5eme/ponts-guides/index.html'),'utf8'),{level:'5eme',title:'Les ponts · Parcours guidé'}));
copyFileSync(resolve(root,'site/5eme/ponts/guided-content.js'),resolve(out,'5eme/ponts/guided-content.js'));
const arcadeAssets='/mini-jeux/';
const arcadeRoutes = [
 ['mini-jeux','galerie','Galerie des mini-jeux'],
 ['mini-jeux/deposer','depot','Déposer notre mini-jeu'],
 ['mini-jeux/jouer','jouer','Jouer au mini-jeu'],
 ['professeur/mini-jeux','professeur','Mini-jeux des binômes']
];
for(const [route,source,title] of arcadeRoutes){
 const body=readFileSync(resolve(root,'site/mini-jeux',source+'.html'),'utf8');
 const head='<meta name="robots" content="noindex,nofollow"><meta name="referrer" content="no-referrer"><link rel="stylesheet" href="'+arcadeAssets+'arcade.css"><script type="module" src="'+arcadeAssets+'arcade.js"></script>';
 write(route+'/index.html',page(title,body).replace('</head>',head+'</head>'));
}
for(const asset of ['arcade.js','arcade.css'])copyFileSync(resolve(root,'site/mini-jeux',asset),resolve(out,'mini-jeux',asset));
for(const dir of ['codage','evaluations','professeur'])cpSync(resolve(root,'site',dir),resolve(out,dir),{recursive:true});
// Keep stable asset URLs for older tabs. New pages load the matching renderer.
const evaluationPages = ['evaluations/index.html','professeur/index.html'];
const versionedAssets = [
  ['evaluations/app.js', evaluationPages],
  ['evaluations/style.css', evaluationPages],
  ['catalogue.js', levels.map(level => level + '/index.html')],
  ['mini-jeux/arcade.js', arcadeRoutes.map(([route]) => route + '/index.html')],
];
for (const [asset, pages] of versionedAssets) {
  const contents = readFileSync(resolve(out, asset));
  const version = createHash('sha256').update(contents).digest('hex').slice(0, 16);
  const dot = asset.lastIndexOf('.');
  const versioned = asset.slice(0, dot) + '.' + version + asset.slice(dot);
  write(versioned, contents);
  for (const entry of pages) {
    const html = readFileSync(resolve(out, entry), 'utf8');
    write(entry, html.replaceAll('"/' + asset + '"', '"/' + versioned + '"'));
  }
}
write('404.html',page('Page introuvable','<h1>Page introuvable</h1><p>Retrouve les ressources depuis ton niveau.</p><a class="portal-button" href="/">Revenir à l’accueil</a>'));
write('_redirects',levels.map(l=>`/${l[0]}e /${l}/ 301\n/${l[0]}e/* /${l}/:splat 301`).join('\n')+'\n');
const commonHeaders='/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n';
const arcadeHeaders=`\n  Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; frame-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'self'\n  X-Robots-Tag: noindex, nofollow\n  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=()\n`;
write('_headers',commonHeaders+'/mini-jeux/*'+arcadeHeaders+'/professeur/mini-jeux/*'+arcadeHeaders);
console.log(`Site prêt : ${levels.length} niveaux, ${catalog.length} séquences ; ressources professeur exclues.`);

