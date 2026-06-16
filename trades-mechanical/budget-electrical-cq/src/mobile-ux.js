// Mobile UX Drawer & Bottom Bar Controllers
document.addEventListener('DOMContentLoaded', () => {
  const menuToggle = document.getElementById('menu-toggle');
  const primaryNav = document.getElementById('primary-navigation');
  
  if (menuToggle && primaryNav) {
    // Inject backdrop overlay
    if (!document.querySelector('.nav-drawer-backdrop')) {
      const navBackdrop = document.createElement('div');
      navBackdrop.className = 'nav-drawer-backdrop';
      document.body.appendChild(navBackdrop);
      
      // Toggle handling
      const toggleMenu = (forceClose = false) => {
        const isOpen = forceClose ? false : !primaryNav.classList.contains('open');
        if (isOpen) {
          primaryNav.classList.add('open');
          primaryNav.setAttribute('data-visible', 'true');
          menuToggle.classList.add('menu-toggle-active');
          menuToggle.setAttribute('aria-expanded', 'true');
          navBackdrop.classList.add('visible');
          document.body.style.overflow = 'hidden';
        } else {
          primaryNav.classList.remove('open');
          primaryNav.setAttribute('data-visible', 'false');
          menuToggle.classList.remove('menu-toggle-active');
          menuToggle.setAttribute('aria-expanded', 'false');
          navBackdrop.classList.remove('visible');
          document.body.style.overflow = '';
        }
      };

      // Set index properties for stagger transition delays
      const navItems = primaryNav.querySelectorAll('ul li');
      navItems.forEach((item, index) => {
        item.style.setProperty('--item-index', index);
      });

      menuToggle.addEventListener('click', (e) => {
        e.stopImmediatePropagation();
        toggleMenu();
      });

      navBackdrop.addEventListener('click', () => toggleMenu(true));

      const navLinks = primaryNav.querySelectorAll('.nav-link');
      navLinks.forEach(link => {
        link.addEventListener('click', () => toggleMenu(true));
      });
    }
  }

  // Floating Bottom Navigation Scroll Behavior
  const bottomBar = document.getElementById('mobile-bottom-bar');
  if (bottomBar) {
    window.addEventListener('scroll', () => {
      if (window.innerWidth <= 768) {
        if (window.scrollY < 100) {
          bottomBar.classList.remove('visible');
        } else {
          bottomBar.classList.add('visible');
        }
      }
    }, { passive: true });
  }
});
