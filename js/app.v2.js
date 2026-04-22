function setupMenuToggle() {
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.nav-menu-div');

  const closeMenu = () => {
    nav.classList.toggle('open');
    toggle.setAttribute(
      'aria-expanded',
      nav.classList.contains('open')
    );
  }

  toggle.addEventListener('click', closeMenu);
  nav.addEventListener('click', closeMenu);
}

setupMenuToggle();

