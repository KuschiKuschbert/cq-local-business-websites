import './style.css';

document.addEventListener('DOMContentLoaded', () => {
  // Mobile Nav Drawer Toggle
  const menuToggle = document.getElementById('mobile-menu-toggle');
  const mobileDrawer = document.getElementById('mobile-drawer');

  if (menuToggle && mobileDrawer) {
    menuToggle.addEventListener('click', () => {
      const expanded = menuToggle.getAttribute('aria-expanded') === 'true';
      menuToggle.setAttribute('aria-expanded', !expanded);
      mobileDrawer.setAttribute('aria-hidden', expanded);
      menuToggle.classList.toggle('active');
    });

    const mobileLinks = mobileDrawer.querySelectorAll('a');
    mobileLinks.forEach(link => {
      link.addEventListener('click', () => {
        menuToggle.setAttribute('aria-expanded', 'false');
        mobileDrawer.setAttribute('aria-hidden', 'true');
        menuToggle.classList.remove('active');
      });
    });
  }

  // Portfolio Gallery Filters
  const filterBtns = document.querySelectorAll('.filter-btn');
  const portfolioCards = document.querySelectorAll('#portfolio-grid .portfolio-card');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      // Toggle active states on tabs
      filterBtns.forEach(b => {
        b.classList.remove('active');
        b.setAttribute('aria-selected', 'false');
      });
      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');

      const filterValue = btn.dataset.filter;

      portfolioCards.forEach(card => {
        const category = card.dataset.category;
        
        if (filterValue === 'all' || category === filterValue) {
          card.classList.remove('hide');
        } else {
          card.classList.add('hide');
        }
      });
    });
  });

  // Testimonial Carousel
  const track = document.getElementById('testimonial-track');
  const indicators = document.querySelectorAll('#carousel-indicators .indicator');
  let currentIndex = 0;
  let autoPlayTimer = null;

  function goToSlide(index) {
    currentIndex = index;
    if (track) {
      track.style.transform = `translateX(-${currentIndex * 33.3333}%)`;
    }
    
    // Update dots
    indicators.forEach((dot, idx) => {
      if (idx === currentIndex) {
        dot.classList.add('active');
      } else {
        dot.classList.remove('active');
      }
    });
  }

  function startAutoplay() {
    autoPlayTimer = setInterval(() => {
      let nextIndex = (currentIndex + 1) % indicators.length;
      goToSlide(nextIndex);
    }, 6000);
  }

  function stopAutoplay() {
    if (autoPlayTimer) {
      clearInterval(autoPlayTimer);
    }
  }

  indicators.forEach(dot => {
    dot.addEventListener('click', () => {
      stopAutoplay();
      const index = parseInt(dot.dataset.index, 10);
      goToSlide(index);
      startAutoplay();
    });
  });

  // Start rotation on load
  if (track && indicators.length > 0) {
    startAutoplay();
  }

  // Package select button synchronizer
  const selectPkgBtns = document.querySelectorAll('.select-pkg-btn');
  const bookingPackageSelect = document.getElementById('booking-package');

  selectPkgBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const selectedPkg = btn.dataset.pkg;
      
      if (bookingPackageSelect) {
        bookingPackageSelect.value = selectedPkg;
      }

      // Scroll to form
      const formSection = document.getElementById('consultation');
      if (formSection) {
        formSection.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // Form Submit & Success modal
  const bookingForm = document.getElementById('booking-form');
  const successOverlay = document.getElementById('form-success');
  const successCloseBtn = document.getElementById('btn-success-close');

  if (bookingForm && successOverlay) {
    bookingForm.addEventListener('submit', (e) => {
      e.preventDefault();
      successOverlay.setAttribute('aria-hidden', 'false');
      bookingForm.reset();
    });
  }

  if (successCloseBtn && successOverlay) {
    successCloseBtn.addEventListener('click', () => {
      successOverlay.setAttribute('aria-hidden', 'true');
    });
  }
});
