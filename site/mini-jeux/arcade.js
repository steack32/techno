const API = '/api/mini-jeux';
const ADMIN = '/api/evaluations/teacher/mini-jeux';
const MAX_CODE = 512 * 1024;
const byId = id => document.getElementById(id);
const playLink = id => '/mini-jeux/jouer/?id=' + encodeURIComponent(id);
const element = (tag, className, text) => {
  const item = document.createElement(tag);
  if (className) item.className = className;
  if (text) item.textContent = text;
  return item;
};

async function api(url, data) {
  const options = {credentials: 'same-origin', cache: 'no-store', headers: {Accept:'application/json'}};
  if (data !== undefined) {
    options.method = 'POST';
    options.headers['Content-Type'] = 'application/json';
    options.body = JSON.stringify(data);
  }
  let response;
  try { response = await fetch(url, options); }
  catch { throw new Error('La connexion a été interrompue. Réessaie dans un instant.'); }
  const body = await response.json().catch(() => null);
  if (!response.ok || !body) {
    const error = new Error(body?.error || 'Le service est momentanément indisponible.');
    error.status = response.status;
    throw error;
  }
  return body;
}
function message(node, text, error = false) {
  node.textContent = text;
  node.classList.toggle('is-error', error);
}

function gallery(teacher) {
  const endpoint = teacher ? ADMIN : API;
  const list = byId('liste'), filter = byId('classe-filtre'), note = byId('list-message');
  const more = byId('suite'), retry = byId('reessayer');
  let next = null, revision = 0, lastAppend = false, isOpen = true;
  let activeClass = new URLSearchParams(location.search).get('classe') || '';

  function setState(open) {
    isOpen = open;
    if (teacher) {
      byId('prof-outils').hidden = false;
      byId('etat-depot').textContent = open ? 'Les élèves peuvent publier leurs jeux.' : 'Les dépôts sont fermés. Les jeux restent jouables.';
      byId('basculer-depot').textContent = open ? 'Fermer les dépôts' : 'Rouvrir les dépôts';
    }
  }
  function card(game) {
    const article = element('article', 'arcade-card teinte-' + (parseInt(game.id[0],16) % 4));
    article.append(element('p', 'arcade-class', 'Classe ' + game.classe), element('h2', '', game.title));
    if (teacher) article.append(element('p', 'arcade-auteurs', game.firstA + ' et ' + game.firstB));
    const actions = element('div','arcade-actions'), play = element('a','arcade-button primary','Jouer');
    play.href = playLink(game.id);
    play.setAttribute('aria-label', 'Jouer à ' + game.title);
    actions.append(play);
    if (teacher) {
      const remove = element('button','arcade-button secondary retirer','Retirer');
      remove.type = 'button';
      remove.setAttribute('aria-label','Retirer ' + game.title);
      remove.addEventListener('click', async () => {
        if (!window.confirm('Retirer « ' + game.title + ' » de la galerie ? Son lien cessera de fonctionner.')) return;
        remove.disabled = true;
        try {
          await api(ADMIN + '/retirer',{id:game.id,confirm:true});
          await load(false);
        } catch (error) { message(note,error.message,true); remove.disabled = false; }
      });
      actions.append(remove);
    }
    article.append(actions);
    return article;
  }
  function displayClasses(classes) {
    filter.replaceChildren(new Option('Toutes les classes',''));
    for (const name of classes) filter.add(new Option(name,name));
    if (activeClass && !classes.includes(activeClass)) filter.add(new Option(activeClass,activeClass));
    filter.value = activeClass;
  }
  async function load(append) {
    const current = ++revision;
    lastAppend = append;
    retry.hidden = true;
    more.disabled = true;
    if (!append) { list.replaceChildren(); next = null; more.hidden = true; byId('vide').hidden = true; }
    list.setAttribute('aria-busy','true');
    message(note,'Chargement des jeux…');
    const query = new URLSearchParams();
    if (activeClass) query.set('classe',activeClass);
    if (append && next !== null) query.set('avant',String(next));
    try {
      const data = await api(endpoint + (query.size ? '?' + query : ''));
      if (current !== revision) return;
      if (teacher) byId('prof-acces').hidden = true;
      setState(data.ouvert);
      displayClasses(data.classes);
      for (const game of data.jeux) list.append(card(game));
      next = data.avant;
      const count = list.childElementCount;
      more.hidden = next === null;
      byId('vide').hidden = count > 0 || Boolean(activeClass);
      const countText = count ? count + (count === 1 ? ' jeu affiché' : ' jeux affichés') + (next !== null ? ' · D’autres jeux sont disponibles.' : '.') : '';
      message(note, count ? countText : (activeClass ? 'Aucun jeu publié pour cette classe.' : ''));
    } catch (error) {
      if (current !== revision) return;
      if (teacher && error.status === 401) {
        byId('prof-acces').hidden = false;
        byId('prof-outils').hidden = true;
        list.replaceChildren();
        more.hidden = true;
        message(note,'');
      } else {
        retry.hidden = false;
        more.hidden = true;
        message(note,error.message,true);
      }
    } finally {
      if (current === revision) { list.setAttribute('aria-busy','false'); more.disabled = false; }
    }
  }
  filter.addEventListener('change', () => {
    activeClass = filter.value;
    const url = new URL(location.href);
    if (activeClass) url.searchParams.set('classe',activeClass); else url.searchParams.delete('classe');
    history.replaceState(null,'',url);
    load(false);
  });
  more.addEventListener('click', () => load(true));
  retry.addEventListener('click', () => load(lastAppend));
  if (teacher) {
    const toggle = byId('basculer-depot');
    toggle.addEventListener('click', async () => {
      toggle.disabled = true;
      try { setState((await api(ADMIN + '/depot',{ouvert:!isOpen})).ouvert); }
      catch (error) { message(note,error.message,true); }
      finally { toggle.disabled = false; }
    });
  }
  load(false);
}

function submission() {
  const form = byId('depot-form'), fields = byId('depot-champs'), note = byId('depot-message');
  const code = byId('code'), file = byId('file');
  let requestId = crypto.randomUUID(), reading = 0, closed = false;
  form.addEventListener('input', () => { requestId = crypto.randomUUID(); });
  const submit = form.querySelector('button[type=submit]');
  code.addEventListener('input', () => { reading++; code.setCustomValidity(''); submit.disabled = false; });
  file.addEventListener('change', async () => {
    const chosen = file.files[0], attempt = ++reading;
    if (!chosen) { submit.disabled = false; return; }
    if (chosen.size > MAX_CODE) {
      file.value = '';
      submit.disabled = false;
      message(note,'Choisis un fichier de 512 Kio maximum.',true);
      return;
    }
    submit.disabled = true;
    try {
      const text = await chosen.text();
      if (attempt !== reading) return;
      code.value = text;
      code.setCustomValidity('');
      requestId = crypto.randomUUID();
      message(note,'Le code du fichier a été copié dans le formulaire.');
    } catch { if (attempt === reading) message(note,'Le fichier ne peut pas être lu. Tu peux coller son code.',true); }
    finally { if (attempt === reading) submit.disabled = false; }
  });
  api(API + '/depot').then(state => {
    if (!state.ouvert) {
      closed = true; fields.disabled = true;
      message(note,'Les dépôts sont fermés. Les jeux déjà publiés restent dans la galerie.');
    }
  }).catch(() => { /* An open form can still submit after a temporary connection failure. */ });
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (closed || fields.disabled || submit.disabled) return;
    if (new TextEncoder().encode(code.value).byteLength > MAX_CODE) {
      code.setCustomValidity('Le code dépasse 512 Kio.'); code.reportValidity(); return;
    }
    const payload = Object.fromEntries(new FormData(form));
    payload.requestId = requestId;
    fields.disabled = true;
    message(note,'Publication du jeu…');
    try {
      const game = await api(API,payload);
      byId('recu-titre').textContent = game.title + ' · Classe ' + game.classe;
      byId('recu-jouer').href = playLink(game.id);
      form.reset(); form.hidden = true;
      const receipt = byId('recu');
      receipt.hidden = false; receipt.focus();
    } catch (error) {
      message(note,error.message,true);
      fields.disabled = closed;
    }
  });
}

async function player() {
  const id = new URLSearchParams(location.search).get('id'), note = byId('jeu-message');
  if (!id || !/^[0-9a-f-]{36}$/i.test(id)) { message(note,'Ce lien de jeu est incomplet. Choisis un jeu dans la galerie.',true); return; }
  try {
    const game = await api(API + '/' + encodeURIComponent(id));
    document.title = game.title + ' · Mini-jeux';
    byId('jeu-titre').textContent = game.title;
    byId('jeu-classe').textContent = 'Classe ' + game.classe;
    const frame = byId('jeu'), stage = byId('jeu-cadre'), fullscreen = byId('plein-ecran');
    frame.title = 'Jouer à ' + game.title;
    const source = API + '/' + encodeURIComponent(game.id) + '/contenu';
    frame.src = source;
    stage.hidden = false;
    message(note,'');
    byId('relancer').addEventListener('click',() => { frame.src = source; frame.focus(); });
    if (document.fullscreenEnabled && stage.requestFullscreen) {
      fullscreen.hidden = false;
      fullscreen.addEventListener('click',async () => {
        try { if (document.fullscreenElement) await document.exitFullscreen(); else await stage.requestFullscreen(); }
        catch { message(note,'Le navigateur ne permet pas le plein écran.',true); }
      });
      document.addEventListener('fullscreenchange',() => {
        fullscreen.textContent = document.fullscreenElement ? 'Quitter le plein écran' : 'Plein écran';
      });
    }
  } catch (error) { message(note,error.message,true); }
}

const page = document.querySelector('[data-page]')?.dataset.page;
if (page === 'galerie' || page === 'professeur') gallery(page === 'professeur');
if (page === 'depot') submission();
if (page === 'jouer') player();
