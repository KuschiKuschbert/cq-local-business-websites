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

  // 3. Sunday Tapas booking variables (OpenTable Integration)
  const bookingDateSelect = document.getElementById('booking-date');
  const bookingForm = document.getElementById('tapas-booking-form');
  const bookingConfirmPanel = document.getElementById('booking-confirm-panel');
  const confirmDetails = document.getElementById('confirm-details');
  const bookingManualLink = document.getElementById('booking-manual-link');
  const bookingResetBtn = document.getElementById('booking-reset-btn');

  // Generate the next 6 Sundays dynamically starting from today
  function populateSundays() {
    if (!bookingDateSelect) return;
    
    // Set baseline date to June 15, 2026 (local time is Monday June 15)
    const today = new Date('2026-06-15');
    let sundaysCount = 0;
    
    let current = new Date(today);
    while (sundaysCount < 6) {
      current.setDate(current.getDate() + 1);
      if (current.getDay() === 0) { // Sunday is 0
        sundaysCount++;
        
        const day = current.getDate();
        const monthNames = [
          "January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"
        ];
        const month = monthNames[current.getMonth()];
        const year = current.getFullYear();
        
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

  // Handle booking form submission (links up to live OpenTable)
  if (bookingForm) {
    bookingForm.addEventListener('submit', (e) => {
      e.preventDefault();
      
      const guests = document.getElementById('booking-guests').value;
      const dateVal = bookingDateSelect.value; // e.g. "2026-06-21"
      const dateOption = bookingDateSelect.options[bookingDateSelect.selectedIndex].text;
      const timeRequested = document.getElementById('booking-time').value; // e.g. "1:30 PM"
      
      // If guests is 8+ (enquiry)
      if (guests === '8') {
        const contactSection = document.getElementById('contact');
        const contactServiceSelect = document.getElementById('contact-service');
        const contactMessage = document.getElementById('contact-message');
        
        if (contactServiceSelect) contactServiceSelect.value = 'private-event';
        if (contactMessage) {
          contactMessage.value = `Hi Sally, I'd like to enquire about booking a Sunday Tapas table for a large group of 8 or more guests on ${dateOption} around ${timeRequested}.`;
        }
        if (contactSection) {
          contactSection.scrollIntoView({ behavior: 'smooth' });
        }
        return;
      }
      
      // Parse time to 24h format
      let time24 = "12:00";
      const match = timeRequested.match(/(\d+):(\d+)\s*(AM|PM)/i);
      if (match) {
        let hr = parseInt(match[1]);
        const min = match[2];
        const ampm = match[3].toUpperCase();
        if (ampm === 'PM' && hr !== 12) hr += 12;
        if (ampm === 'AM' && hr === 12) hr = 0;
        time24 = `${String(hr).padStart(2, '0')}:${min}`;
      }
      
      // Construct OpenTable URL
      // Format: https://www.opentable.com.au/r/riviera-yeppoon-cooee-bay?covers=2&dateTime=2026-06-21T13:30
      const otUrl = `https://www.opentable.com.au/r/riviera-yeppoon-cooee-bay?covers=${guests}&dateTime=${dateVal}T${time24}`;
      
      // Attempt to open in a new window/tab
      window.open(otUrl, '_blank');
      
      // Show confirmation panel on our site
      if (confirmDetails) {
        confirmDetails.innerHTML = `Opening reservation page on OpenTable for <strong>${guests} guests</strong> on <strong>${dateOption}</strong> at <strong>${timeRequested}</strong>...`;
      }
      if (bookingManualLink) {
        bookingManualLink.href = otUrl;
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

  // 4. Sunday Tapas Menu Tabs (Tapas, Cocktails, Wine/Beer)
  const tabTapas = document.getElementById('tab-tapas');
  const tabCocktails = document.getElementById('tab-cocktails');
  const tabWineBeer = document.getElementById('tab-wine-beer');
  
  const panelTapas = document.getElementById('menu-tapas-panel');
  const panelCocktails = document.getElementById('menu-cocktails-panel');
  const panelWineBeer = document.getElementById('menu-wine-beer-panel');

  const tapasTabs = [tabTapas, tabCocktails, tabWineBeer];
  const tapasPanels = [panelTapas, panelCocktails, panelWineBeer];

  function switchTapasTab(activeIndex) {
    tapasTabs.forEach((tab, index) => {
      if (tab) {
        const isActive = index === activeIndex;
        tab.classList.toggle('active', isActive);
        tab.setAttribute('aria-selected', isActive ? 'true' : 'false');
      }
    });
    tapasPanels.forEach((panel, index) => {
      if (panel) {
        panel.style.display = index === activeIndex ? 'block' : 'none';
      }
    });
  }

  if (tabTapas) tabTapas.addEventListener('click', () => switchTapasTab(0));
  if (tabCocktails) tabCocktails.addEventListener('click', () => switchTapasTab(1));
  if (tabWineBeer) tabWineBeer.addEventListener('click', () => switchTapasTab(2));

  // 5. Catering Menu Tabs (Finger Food, Meats/Sides)
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
  const contactServiceSelect = document.getElementById('contact-service');
  const contactPackageSelect = document.getElementById('contact-package');

  selectPkgBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const pkgName = btn.getAttribute('data-package');
      
      if (contactServiceSelect) contactServiceSelect.value = 'wedding';
      if (contactPackageSelect) {
        if (pkgName === 'Kiss & Commit') contactPackageSelect.value = 'kiss-commit';
        else if (pkgName === 'Vows & Vino') contactPackageSelect.value = 'vows-vino';
        else if (pkgName === 'The Big Day') contactPackageSelect.value = 'big-day';
      }
      
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
      
      enquirySubmitForm.classList.add('hidden');
      contactFeedback.classList.remove('hidden');
    });
  }
});
