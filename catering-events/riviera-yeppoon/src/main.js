// Import stylesheet for Vite build pipeline
import './style.css';

document.addEventListener('DOMContentLoaded', () => {
  
  // 1. Header Scroll Styling
  const header = document.getElementById('main-header');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  });

  // 2. Mobile Navigation Toggle
  const menuToggle = document.getElementById('menu-toggle');
  const primaryNav = document.getElementById('primary-navigation');
  
  if (menuToggle && primaryNav) {
    menuToggle.addEventListener('click', () => {
      const isOpen = primaryNav.classList.toggle('open');
      menuToggle.classList.toggle('menu-toggle-active');
      menuToggle.setAttribute('aria-expanded', isOpen);
    });

    // Close menu when clicking nav links
    const navLinks = primaryNav.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
      link.addEventListener('click', () => {
        primaryNav.classList.remove('open');
        menuToggle.classList.remove('menu-toggle-active');
        menuToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // 3. Sunday Tapas Booking Engine
  const bookingDateSelect = document.getElementById('booking-date');
  const bookingForm = document.getElementById('tapas-booking-form');
  const bookingConfirmPanel = document.getElementById('booking-confirm-panel');
  const confirmDetails = document.getElementById('confirm-details');
  const bookingResetBtn = document.getElementById('booking-reset-btn');

  // Generate the next 6 Sundays dynamically starting from today
  function populateSundays() {
    if (!bookingDateSelect) return;
    
    // Set baseline date to June 15, 2026 (local time is Monday June 15)
    const today = new Date('2026-06-15');
    let sundaysCount = 0;
    
    // Scan forward day by day to find Sundays
    let current = new Date(today);
    while (sundaysCount < 6) {
      current.setDate(current.getDate() + 1);
      if (current.getDay() === 0) { // Sunday is 0
        sundaysCount++;
        
        // Format date beautifully
        const day = current.getDate();
        const monthNames = [
          "January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"
        ];
        const month = monthNames[current.getMonth()];
        const year = current.getFullYear();
        
        // Ordinal suffix
        let suffix = "th";
        if (day === 1 || day === 21 || day === 31) suffix = "st";
        else if (day === 2 || day === 22) suffix = "nd";
        else if (day === 3 || day === 23) suffix = "rd";
        
        const dateStr = `Sunday, ${day}${suffix} of ${month} ${year}`;
        const optionVal = `${year}-${String(current.getMonth()+1).padStart(2,'0')}-${String(day).padStart(2,'0')}`;
        
        const option = document.createElement('option');
        option.value = optionVal;
        option.textContent = dateStr;
        bookingDateSelect.appendChild(option);
      }
    }
  }

  populateSundays();

  // Handle booking form submission
  if (bookingForm) {
    bookingForm.addEventListener('submit', (e) => {
      e.preventDefault();
      
      const guests = document.getElementById('booking-guests').value;
      const dateOption = bookingDateSelect.options[bookingDateSelect.selectedIndex].text;
      const time = document.getElementById('booking-time').value;
      
      // Update confirmation details
      if (confirmDetails) {
        confirmDetails.innerHTML = `Table reserved for <strong>${guests} guests</strong> on <strong>${dateOption}</strong> at <strong>${time} PM</strong>.`;
      }
      
      // Toggle panels
      bookingForm.classList.add('hidden');
      bookingConfirmPanel.classList.remove('hidden');
    });
  }

  // Reset booking form
  if (bookingResetBtn && bookingForm && bookingConfirmPanel) {
    bookingResetBtn.addEventListener('click', () => {
      bookingForm.reset();
      bookingConfirmPanel.classList.add('hidden');
      bookingForm.classList.remove('hidden');
    });
  }

  // 4. Sunday Tapas Menu Tabs
  const tabTapas = document.getElementById('tab-tapas');
  const tabDrinks = document.getElementById('tab-drinks');
  const panelTapas = document.getElementById('menu-tapas-panel');
  const panelDrinks = document.getElementById('menu-drinks-panel');

  if (tabTapas && tabDrinks && panelTapas && panelDrinks) {
    tabTapas.addEventListener('click', () => {
      tabTapas.classList.add('active');
      tabTapas.setAttribute('aria-selected', 'true');
      tabDrinks.classList.remove('active');
      tabDrinks.setAttribute('aria-selected', 'false');
      
      panelTapas.style.display = 'block';
      panelDrinks.style.display = 'none';
    });

    tabDrinks.addEventListener('click', () => {
      tabDrinks.classList.add('active');
      tabDrinks.setAttribute('aria-selected', 'true');
      tabTapas.classList.remove('active');
      tabTapas.setAttribute('aria-selected', 'false');
      
      panelDrinks.style.display = 'block';
      panelTapas.style.display = 'none';
    });
  }

  // 5. Catering Menu Tabs
  const catTabPlatters = document.getElementById('cat-tab-platters');
  const catTabBuffet = document.getElementById('cat-tab-buffet');
  const catPanelPlatters = document.getElementById('cat-panel-platters');
  const catPanelBuffet = document.getElementById('cat-panel-buffet');

  if (catTabPlatters && catTabBuffet && catPanelPlatters && catPanelBuffet) {
    catTabPlatters.addEventListener('click', () => {
      catTabPlatters.classList.add('active');
      catTabPlatters.setAttribute('aria-selected', 'true');
      catTabBuffet.classList.remove('active');
      catTabBuffet.setAttribute('aria-selected', 'false');
      
      catPanelPlatters.style.display = 'block';
      catPanelBuffet.style.display = 'none';
    });

    catTabBuffet.addEventListener('click', () => {
      catTabBuffet.classList.add('active');
      catTabBuffet.setAttribute('aria-selected', 'true');
      catTabPlatters.classList.remove('active');
      catTabPlatters.setAttribute('aria-selected', 'false');
      
      catPanelBuffet.style.display = 'block';
      catPanelPlatters.style.display = 'none';
    });
  }

  // 6. Wedding Package Selection Actions
  const selectPkgBtns = document.querySelectorAll('.select-pkg-btn');
  const enquiryForm = document.getElementById('event-enquiry-form');
  const contactServiceSelect = document.getElementById('contact-service');
  const contactPackageSelect = document.getElementById('contact-package');

  selectPkgBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const pkgName = btn.getAttribute('data-package');
      
      // Auto-set selects
      if (contactServiceSelect) contactServiceSelect.value = 'wedding';
      if (contactPackageSelect) {
        if (pkgName === 'Kiss & Commit') contactPackageSelect.value = 'kiss-commit';
        else if (pkgName === 'Vows & Vino') contactPackageSelect.value = 'vows-vino';
        else if (pkgName === 'The Big Day') contactPackageSelect.value = 'big-day';
      }
      
      // Scroll smoothly to contact
      const contactSection = document.getElementById('contact');
      if (contactSection) {
        contactSection.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // 7. Event Enquiry Form Submission
  const enquirySubmitForm = document.getElementById('event-enquiry-form');
  const contactFeedback = document.getElementById('contact-feedback');

  if (enquirySubmitForm && contactFeedback) {
    enquirySubmitForm.addEventListener('submit', (e) => {
      e.preventDefault();
      
      // Simple fade-out form and fade-in feedback
      enquirySubmitForm.classList.add('hidden');
      contactFeedback.classList.remove('hidden');
    });
  }
});
