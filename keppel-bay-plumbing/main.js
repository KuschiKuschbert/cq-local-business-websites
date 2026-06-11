// Mobile menu toggle functionality
document.addEventListener('DOMContentLoaded', () => {
  const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
  const navLinks = document.querySelector('.nav-links');
  
  // Basic toggle for mobile menu (in a real app, this would expand a styled side-drawer or dropdown)
  if(mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', () => {
      if (navLinks.style.display === 'flex') {
        navLinks.style.display = 'none';
      } else {
        navLinks.style.display = 'flex';
        navLinks.style.flexDirection = 'column';
        navLinks.style.position = 'absolute';
        navLinks.style.top = '100%';
        navLinks.style.left = '0';
        navLinks.style.width = '100%';
        navLinks.style.background = 'rgba(255, 255, 255, 0.95)';
        navLinks.style.padding = '1rem';
        navLinks.style.boxShadow = '0 10px 15px -3px rgba(0, 0, 0, 0.1)';
      }
    });
  }

  // Add scroll event for navbar blur effect
  const navbar = document.querySelector('.navbar');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      navbar.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
    } else {
      navbar.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.05)';
    }
  });
});
