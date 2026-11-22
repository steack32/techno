const PUBLIC = '/api/mini-jeux';
const TEACHER = '/api/evaluations/teacher/mini-jeux';
const UUID = /^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/i;
const MAX_CODE = 512 * 1024;
const MAX_BODY = 2 * MAX_CODE + 8192;
const PAGE_SIZE = 24;
const MAX_GAMES = 1000;
const encoder = new TextEncoder();

const privateHeaders = {
  'Cache-Control': 'no-store',
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'no-referrer',
  'Cross-Origin-Resource-Policy': 'same-origin',
  'X-Robots-Tag': 'noindex, nofollow'
};
const gamePolicy = [
  'sandbox allow-scripts', "default-src 'none'", "script-src 'unsafe-inline'",
  "style-src 'unsafe-inline'", "img-src data: blob:", "font-src data:",
  "media-src data: blob:", "connect-src 'none'", "object-src 'none'",
  "frame-src 'none'", "worker-src 'none'", "form-action 'none'",
  "base-uri 'none'", "frame-ancestors 'self'"
].join('; ');

export function initMiniJeux(sql) {
  sql.exec(`CREATE TABLE IF NOT EXISTS arcade_games (
    seq INTEGER PRIMARY KEY AUTOINCREMENT, id TEXT NOT NULL UNIQUE,
    request_key TEXT NOT NULL UNIQUE, payload_hash TEXT NOT NULL,
    title TEXT NOT NULL, classe TEXT NOT NULL, first_a TEXT NOT NULL, first_b TEXT NOT NULL,
    html TEXT NOT NULL, created INTEGER NOT NULL
  ); CREATE INDEX IF NOT EXISTS arcade_games_class ON arcade_games(classe, seq);`);
}

function json(data, status = 200) {
  return Response.json(data, {status, headers: privateHeaders});
}
class FormError extends Error {
  constructor(status, message) { super(message); this.status = status; }
}
function reject(status, message) { throw new FormError(status, message); }

async function readForm(request, max) {
  const origin = request.headers.get('Origin');
  if ((origin !== null && origin !== new URL(request.url).origin) || request.headers.get('Sec-Fetch-Site') === 'cross-site') {
    reject(403, 'Envoie le formulaire depuis le site de technologie.');
  }
  if (request.headers.get('Content-Type')?.split(';')[0].trim().toLowerCase() !== 'application/json') {
    reject(415, 'Ce formulaire doit être envoyé depuis la page de dépôt.');
  }
  const tooLarge = () => reject(413, 'Le fichier HTML peut peser jusqu’à 512 Kio.');
  if (Number(request.headers.get('Content-Length')) > max) tooLarge();
  const reader = request.body?.getReader();
  if (!reader) reject(400, 'Le formulaire est vide.');
  const decoder = new TextDecoder('utf-8', {fatal: true});
  let text = '', bytes = 0;
  try {
    for (;;) {
      const {value, done} = await reader.read();
      if (done) break;
      bytes += value.byteLength;
      if (bytes > max) { await reader.cancel(); tooLarge(); }
      text += decoder.decode(value, {stream: true});
    }
    const data = JSON.parse(text + decoder.decode());
    if (!data || typeof data !== 'object' || Array.isArray(data)) reject(400, 'Formulaire invalide.');
    return data;
  } catch (error) {
    if (error instanceof FormError) throw error;
    reject(400, 'Impossible de lire le formulaire.');
  } finally { reader.releaseLock(); }
}

function cleanText(value) {
  return typeof value === 'string' ? value.normalize('NFC').trim().replace(/\s+/gu, ' ') : '';
}
function classroom(value) {
  const label = cleanText(value).toUpperCase();
  if (!/^[3-6][\p{L}\p{M}\p{N} .-]{0,15}$/u.test(label)) reject(400, 'Indique ta classe, par exemple 301 ou 4e B.');
  return label.replace(/^([3-6])(?:ÈME|EME|E)(?=$|[ .-])/, '$1e');
}
function firstName(value) {
  const name = cleanText(value);
  if (name.length > 40 || !/^\p{L}[\p{L}\p{M} ’'\u02bb\u02bc-]*$/u.test(name)) reject(400, 'Renseigne les deux prénoms du binôme (40 caractères maximum chacun).');
  return name;
}
function cleanTitle(value) {
  return cleanText(value).replace(/[\p{Cc}\p{Cf}]/gu, '');
}
function titleFromHtml(html) {
  const title = /<title\b[^>]*>([^<]{1,500})<\/title\s*>/i.exec(html)?.[1] || '';
  const named = {amp:'&',lt:'<',gt:'>',quot:'"',apos:"'",nbsp:' ',eacute:'é',egrave:'è',agrave:'à',ccedil:'ç',ecirc:'ê'};
  return cleanTitle(title.replace(/&(amp|lt|gt|quot|apos|nbsp|eacute|egrave|agrave|ccedil|ecirc|#\d{1,7}|#x[\da-f]{1,6});/gi, (match, key) => {
    const entity = key.toLowerCase();
    if (!entity.startsWith('#')) return named[entity];
    const number = entity[1] === 'x' ? parseInt(entity.slice(2), 16) : Number(entity.slice(1));
    return number > 0 && number <= 0x10ffff && !(number >= 0xd800 && number <= 0xdfff) ? String.fromCodePoint(number) : '';
  })).slice(0, 80);
}
function gameCode(raw) {
  if (typeof raw !== 'string') reject(400, 'Colle le code HTML du jeu ou choisis son fichier.');
  let html = raw.trim();
  const fenced = /^\x60{3}(?:html)?\s*\r?\n([\s\S]*?)\r?\n\x60{3}$/i.exec(html);
  if (fenced) html = fenced[1].trim();
  if (encoder.encode(html).byteLength > MAX_CODE) reject(413, 'Le fichier HTML peut peser jusqu’à 512 Kio.');
  let start = 0;
  while (html.startsWith('<!--', start)) {
    const end = html.indexOf('-->', start + 4);
    if (end === -1) break;
    start = end + 3;
    while (start < html.length && /\s/.test(html[start])) start++;
  }
  if (!/^(?:<!doctype\s+html\b|<(?:html|head|body)(?=[\s>]))/i.test(html.slice(start, start + 128))) {
    reject(400, 'Colle tout le document HTML, à partir de <!DOCTYPE html> ou de <html>.');
  }
  return html;
}
function accepting(store) {
  return store.one('SELECT value FROM settings WHERE key=?', 'arcadeAccepting')?.value !== '0';
}
function list(store, url, teacher) {
  const filter = url.searchParams.get('classe');
  const before = url.searchParams.get('avant');
  const cursor = before === null ? null : Number(before);
  if (before !== null && (!Number.isSafeInteger(cursor) || cursor < 1)) reject(400, 'Page de galerie invalide.');
  const params = [], conditions = [];
  if (filter) { conditions.push('classe = ?'); params.push(classroom(filter)); }
  if (cursor !== null) { conditions.push('seq < ?'); params.push(cursor); }
  const where = conditions.length ? ' WHERE ' + conditions.join(' AND ') : '';
  const fields = 'seq, id, title, classe, created' + (teacher ? ', first_a AS firstA, first_b AS firstB' : '');
  const rows = store.sql.exec('SELECT ' + fields + ' FROM arcade_games' + where + ' ORDER BY seq DESC LIMIT ?', ...params, PAGE_SIZE + 1).toArray();
  const shown = rows.slice(0, PAGE_SIZE);
  return json({
    jeux: shown.map(({seq, ...game}) => game),
    avant: rows.length > PAGE_SIZE ? shown.at(-1).seq : null,
    classes: store.sql.exec('SELECT DISTINCT classe FROM arcade_games ORDER BY classe').toArray().map(row => row.classe),
    ouvert: accepting(store)
  });
}
function receipt(game, status) {
  return json({id: game.id, title: game.title, classe: game.classe}, status);
}
async function publish(store, request) {
  const form = await readForm(request, MAX_BODY);
  const classe = classroom(form.classe), a = firstName(form.firstA), b = firstName(form.firstB);
  const html = gameCode(form.html), customTitle = cleanTitle(form.title);
  if (customTitle.length > 80) reject(400, 'Choisis un titre de 80 caractères maximum.');
  const title = customTitle || titleFromHtml(html) || 'Jeu de la classe ' + classe;
  if (typeof form.requestId !== 'string' || !UUID.test(form.requestId)) reject(400, 'Recharge le formulaire avant de publier.');
  const fingerprint = await crypto.subtle.digest('SHA-256', encoder.encode(JSON.stringify([classe, a, b, title, html])));
  const hash = Array.from(new Uint8Array(fingerprint), byte => byte.toString(16).padStart(2, '0')).join('');
  // No await from this point: a retry or another simultaneous submission cannot split the decision and insert.
  return store.ctx.storage.transactionSync(() => {
    const previous = store.one('SELECT id, title, classe, payload_hash FROM arcade_games WHERE request_key=?', form.requestId);
    if (previous) {
      if (previous.payload_hash !== hash) reject(409, 'Le formulaire a changé. Recharge la page pour déposer une autre version.');
      return receipt(previous, 200);
    }
    if (!accepting(store)) reject(403, 'Les dépôts sont fermés. Ton code reste dans le formulaire.');
    if (store.one('SELECT COUNT(*) AS n FROM arcade_games').n >= MAX_GAMES) reject(409, 'La galerie est pleine. Préviens ton professeur.');
    const ip = request.headers.get('CF-Connecting-IP') || 'local';
    store.limited('arcade-ip:' + ip, 90, 10 * 60_000);
    store.limited('arcade-publications', 240, 60 * 60_000);
    const id = crypto.randomUUID();
    store.sql.exec('INSERT INTO arcade_games(id,request_key,payload_hash,title,classe,first_a,first_b,html,created) VALUES(?,?,?,?,?,?,?,?,?)',
      id, form.requestId, hash, title, classe, a, b, html, Date.now());
    return receipt({id, title, classe}, 201);
  });
}

function gameDocument(store, request, id) {
  // Normal navigation always lands on the trusted player. Only an embedded document receives HTML.
  const dest = request.headers.get('Sec-Fetch-Dest');
  if (dest === 'document') return new Response(null, {status: 303, headers: {...privateHeaders, Location: '/mini-jeux/jouer/?id=' + id}});
  if (dest !== 'iframe' || request.headers.get('Sec-Fetch-Site') === 'cross-site') {
    return new Response('Ouvre ce jeu depuis la galerie avec un navigateur récent.', {status: 403, headers: {...privateHeaders, 'Content-Type':'text/plain; charset=utf-8'}});
  }
  const row = store.one('SELECT html FROM arcade_games WHERE id=?', id);
  if (!row) return new Response('Ce jeu a été retiré de la galerie.', {status:404, headers:{...privateHeaders,'Content-Type':'text/plain; charset=utf-8'}});
  return new Response(request.method === 'HEAD' ? null : row.html, {headers: {
    ...privateHeaders, 'Content-Type': 'text/html; charset=utf-8', 'Content-Security-Policy': gamePolicy,
    'X-Frame-Options': 'SAMEORIGIN', 'Vary': 'Sec-Fetch-Dest, Sec-Fetch-Site', 'X-DNS-Prefetch-Control': 'off',
    'Permissions-Policy': 'camera=(), microphone=(), geolocation=(), payment=(), usb=(), display-capture=()'
  }});
}

async function route(store, request, url) {
  const path = url.pathname, method = request.method;
  if (path === TEACHER || path.startsWith(TEACHER + '/')) {
    store.teacher(request);
    if (method === 'GET' && path === TEACHER) return list(store, url, true);
    if (method === 'POST' && path === TEACHER + '/depot') {
      const form = await readForm(request, 4096);
      if (typeof form.ouvert !== 'boolean') reject(400, 'État du dépôt invalide.');
      store.sql.exec('INSERT OR REPLACE INTO settings(key,value) VALUES(?,?)', 'arcadeAccepting', form.ouvert ? '1' : '0');
      return json({ouvert: form.ouvert});
    }
    if (method === 'POST' && path === TEACHER + '/retirer') {
      const form = await readForm(request, 4096);
      if (typeof form.id !== 'string' || !UUID.test(form.id) || form.confirm !== true) reject(400, 'Confirme le retrait du jeu.');
      store.sql.exec('DELETE FROM arcade_games WHERE id=?', form.id);
      return json({ok:true});
    }
    return json({error:'Action inconnue.'}, 404);
  }
  if (path === PUBLIC && method === 'GET') return list(store, url, false);
  if (path === PUBLIC && method === 'POST') return publish(store, request);
  if (path === PUBLIC + '/depot' && method === 'GET') return json({ouvert:accepting(store)});
  if (path.startsWith(PUBLIC + '/')) {
    const [id, resource, ...rest] = path.slice(PUBLIC.length + 1).split('/');
    if (UUID.test(id) && !rest.length) {
      if (!resource && method === 'GET') {
        const row = store.one('SELECT id, title, classe, created FROM arcade_games WHERE id=?', id);
        return row ? json(row) : json({error:'Ce jeu a été retiré ou son lien est incorrect.'}, 404);
      }
      if (resource === 'contenu' && (method === 'GET' || method === 'HEAD')) return gameDocument(store, request, id);
    }
  }
  return json({error:'Jeu ou page introuvable.'}, 404);
}
export async function miniJeuxRoute(store, request, url) {
  try { return await route(store, request, url); }
  catch (error) {
    if (error instanceof FormError) return json({error: error.message}, error.status);
    throw error;
  }
}
