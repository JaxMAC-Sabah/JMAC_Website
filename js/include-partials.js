async function loadPartial(targetId, url) {
  const el = document.getElementById(targetId);
  if (!el) return;
  const res = await fetch(url, { cache: 'no-cache' });
  el.innerHTML = await res.text();

  // If this is the header, wire up the dropdown
  if (url.includes('header.html')) initHeaderDropdown(el);
}

function initHeaderDropdown(scope=document) {
  const btn = scope.querySelector('.dropbtn');
  const menu = scope.querySelector('.dropdown-menu');
  if (!btn || !menu) return;

  btn.addEventListener('click', (e) => {
    const isOpen = btn.getAttribute('aria-expanded') === 'true';
    btn.setAttribute('aria-expanded', !isOpen);
    scope.querySelector('.dropdown').classList.toggle('open', !isOpen);
    e.stopPropagation();
  });

  document.addEventListener('click', (e) => {
    if (scope.querySelector('.dropdown').classList.contains('open') &&
        !btn.contains(e.target) &&
        !menu.contains(e.target)) {
      scope.querySelector('.dropdown').classList.remove('open');
      btn.setAttribute('aria-expanded','false');
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  loadPartial('site-header', '/partials/header.html');
  loadPartial('site-footer', '/partials/footer.html'); // if you add a footer later
});
