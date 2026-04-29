(function () {
  'use strict';

  // ===== THEME SELECTOR: light / dark / cyberpunk / solarized =====
  const THEME_KEY = 'wb-theme';
  const THEMES = ['light', 'dark', 'cyberpunk', 'solarized'];
  const body = document.body;
  const select = document.getElementById('theme-select');

  function apply(theme) {
    body.classList.remove('dark', 'cyberpunk', 'solarized');
    if (theme === 'dark') body.classList.add('dark');
    else if (theme === 'cyberpunk') body.classList.add('cyberpunk');
    else if (theme === 'solarized') body.classList.add('solarized');
    if (select && select.value !== theme) select.value = theme;
  }

  function readStored() {
    const s = localStorage.getItem(THEME_KEY);
    if (THEMES.indexOf(s) !== -1) return s;
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  apply(readStored());

  if (select) {
    select.addEventListener('change', function () {
      const next = select.value;
      if (THEMES.indexOf(next) === -1) return;
      localStorage.setItem(THEME_KEY, next);
      apply(next);
    });
  }

  // ===== COPY BUTTONS ON <pre> =====
  function attachCopyButtons() {
    const pres = document.querySelectorAll('.markdown-body pre');
    pres.forEach(function (pre) {
      if (pre.querySelector('.copy-btn')) return;
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'copy-btn';
      btn.setAttribute('aria-label', 'Copy code');
      btn.textContent = 'Copy';
      btn.addEventListener('click', function () {
        const code = pre.querySelector('code') || pre;
        const text = code.innerText;
        navigator.clipboard.writeText(text).then(function () {
          btn.textContent = 'Copied';
          btn.classList.add('copied');
          setTimeout(function () {
            btn.textContent = 'Copy';
            btn.classList.remove('copied');
          }, 1600);
        });
      });
      pre.appendChild(btn);
    });
  }
  attachCopyButtons();
})();
