/**
 * MARGAM AI – Tamil language toggle support
 */
(function () {
  const langToggle = document.getElementById('langToggle');
  const html = document.documentElement;

  function getLang() {
    return html.getAttribute('data-lang') || 'en';
  }

  function setLang(lang) {
    html.setAttribute('data-lang', lang);
    document.querySelectorAll('[data-en][data-ta]').forEach(el => {
      const text = lang === 'ta' ? (el.getAttribute('data-ta') || el.textContent) : (el.getAttribute('data-en') || el.textContent);
      if (el.tagName === 'INPUT' || el.tagName === 'OPTION') return;
      if (el.getAttribute('data-lang-skip')) return;
      el.textContent = text;
    });
    if (langToggle) {
      langToggle.querySelector('span').textContent = lang === 'ta' ? 'English' : 'தமிழ்';
    }
  }

  if (langToggle) {
    langToggle.addEventListener('click', () => {
      const next = getLang() === 'en' ? 'ta' : 'en';
      setLang(next);
    });
  }
})();
