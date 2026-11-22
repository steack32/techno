const input = document.getElementById('sequence-search');
const reset = document.getElementById('clear-search');
const status = document.getElementById('search-status');
const lessons = document.querySelector('.portal-grid');

function normalize(text) {
  return text.normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, ' ')
    .trim();
}

const resourceSelector = '[data-resource], [data-sequence]';
const resources = Array.from(document.querySelectorAll(resourceSelector), card => ({
  card,
  text: normalize(card.textContent + ' ' + (card.dataset.keywords || '')),
}));

function filterResources() {
  const query = normalize(input.value);
  const words = query ? query.split(' ') : [];
  let count = 0;
  for (const {card, text} of resources) {
    const matches = words.every(word => text.includes(word));
    card.hidden = !matches;
    if (matches) count++;
  }
  lessons.hidden = !lessons.querySelector('[data-sequence]:not([hidden])');
  if (reset) reset.hidden = !input.value;
  const plural = count > 1 ? 's' : '';
  const state = query ? 'affichée' : 'disponible';
  status.textContent = count
    ? `${count} ressource${plural} ${state}${plural}`
    : 'Aucune ressource trouvée. Essaie un autre mot ou efface la recherche.';
}

input.addEventListener('input', filterResources);
reset?.addEventListener('click', () => {
  input.value = '';
  filterResources();
  input.focus();
});
window.addEventListener('pageshow', filterResources);
filterResources();
