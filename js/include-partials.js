function initProjectsDropdown(scope=document){
  //locate where is button and menu are, and wrapper in which they exist 
  const btn = document.querySelector('.dropbtn');
  const menu = document.querySelector('.dropdown-content');
  const wrapper = document.querySelector('.dropdown');
  if (!btn || !menu || !wrapper) return; //bail if any part is missing

  function openMenu(){
    wrapper.classList.add('open'); //useful for providing class hook for styling etc 
    btn.setAttribute('aria-expanded', 'true');
    menu.hidden = false;
  }
  function closeMenu(){
    wrapper.classList.remove('open');
    btn.setAttribute('aria-expanded', 'false');
    menu.hidden = true;
  }
  function toggleMenu(){
    const isOpen = btn.getAttribute('aria-expanded') === 'true';
    isOpen ? closeMenu() : openMenu();
}
  btn.addEventListener('click', function (event) {
    event.stopPropagation(); // don’t let doc click close it immediately
    toggleMenu();
  });
  document.addEventListener('click', function (event) {
    // If click is outside the wrapper, close
    if (!wrapper.contains(event.target)) closeMenu();
  });
  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') closeMenu();
  });
}

async function loadPartial(targetId, url) {
  const insertionLocation = document.getElementById(targetId);
  if (!insertionLocation) return; // no find location do nothing

  try {
    // Get the HTML file over the network
    const response = await fetch(url);
    const html = await response.text();

    // Insert it into the page
    insertionLocation.innerHTML = html;

    // If this was the header, wire up its dropdown now that elements exist
    if (url.includes('header_test.html')) {
      initProjectsDropdown(insertionLocation);
    }
  } catch (error) {
    console.error('Failed to load partial:', url, error);
  }
}
// Run after the DOM exists
document.addEventListener('DOMContentLoaded', () => {
  loadPartial('site-header', '/partials/header_test.html');
});