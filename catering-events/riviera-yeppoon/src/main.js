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

  // 8. Event Builder Wizard Engine
  const formatPrice = (val) => '$' + val.toLocaleString('en-AU', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  
  const diningSelect = document.getElementById('wiz-dining-select');

  const weddingDiningOptions = [
    { value: 'portofino', text: 'Portofino Cocktail Hour + Canapes — $90 pp', price: 90, type: 'per-head' },
    { value: 'amalfi-3', text: 'Amalfi 3-Course Plated — $109 pp', price: 109, type: 'per-head' },
    { value: 'amalfi-2', text: 'Amalfi 2-Course Plated — $89 pp', price: 89, type: 'per-head' },
    { value: 'taormina', text: 'Taormina Canapes + Plated Main — $88 pp', price: 88, type: 'per-head' },
    { value: 'tavola-entree', text: 'La Tavola Feast (Entree & Main) — $90 pp', price: 90, type: 'per-head' },
    { value: 'tavola-main', text: 'La Tavola Feast (Main Only) — $80 pp', price: 80, type: 'per-head' },
    { value: 'gyros', text: 'Gyros Buffet — $32 pp', price: 32, type: 'per-head' }
  ];

  const partyDiningOptions = [
    { value: 'gyros', text: 'Gyros Bar Buffet — $32 pp', price: 32, type: 'per-head' },
    { value: 'grazing-1m', text: '1-Meter Grazing Table (up to 30 guests) — $650 flat', price: 650, type: 'flat' },
    { value: 'grazing-1m-styled', text: '1-Meter Grazing Table Styled — $820 flat', price: 820, type: 'flat' },
    { value: 'grazing-2m', text: '2-Meter Grazing Table (up to 60 guests) — $1250 flat', price: 1250, type: 'flat' },
    { value: 'grazing-2m-styled', text: '2-Meter Grazing Table Styled — $1485 flat', price: 1485, type: 'flat' },
    { value: 'grazing-3m', text: '3-Meter Grazing Table (up to 90 guests) — $1999 flat', price: 1999, type: 'flat' },
    { value: 'grazing-3m-styled', text: '3-Meter Grazing Table Styled — $2178 flat', price: 2178, type: 'flat' },
    { value: 'platter-charcuterie', text: 'Charcuterie & Cheese Platter — $100 flat', price: 100, type: 'flat' },
    { value: 'platter-seafood', text: 'Cold Seafood Platter — $160 flat', price: 160, type: 'flat' },
    { value: 'platter-sausage', text: 'Hot Sausage Rolls & Pies Platter — $75 flat', price: 75, type: 'flat' },
    { value: 'platter-quiche', text: 'Mini Quiches & Spinach Rolls Platter — $75 flat', price: 75, type: 'flat' },
    { value: 'platter-pastries', text: 'Mixed Pastries Box — $120 flat', price: 120, type: 'flat' },
    { value: 'platter-sliders', text: 'Slider Board (Beef & Pulled Pork) — $175 flat', price: 175, type: 'flat' },
    { value: 'platter-calamari', text: 'Calamari & Chips Box — $175 flat', price: 175, type: 'flat' }
  ];

  function populateDiningDropdown(occasion) {
    if (!diningSelect) return;
    diningSelect.innerHTML = '';
    const options = occasion === 'wedding' ? weddingDiningOptions : partyDiningOptions;
    options.forEach(opt => {
      const optionEl = document.createElement('option');
      optionEl.value = opt.value;
      optionEl.textContent = opt.text;
      diningSelect.appendChild(optionEl);
    });
  }

  let currentStep = 1;
  const totalSteps = 4;
  
  function updateStepUI() {
    for (let i = 1; i <= totalSteps; i++) {
      const panel = document.getElementById(`wiz-panel-${i}`);
      const progStep = document.getElementById(`prog-step-${i}`);
      
      if (panel) {
        if (i === currentStep) {
          panel.classList.remove('hidden');
        } else {
          panel.classList.add('hidden');
        }
      }
      
      if (progStep) {
        progStep.classList.toggle('active', i === currentStep);
        progStep.classList.toggle('completed', i < currentStep);
      }
    }
  }

  const btnNext1 = document.getElementById('btn-wiz-next-1');
  const btnNext2 = document.getElementById('btn-wiz-next-2');
  const btnNext3 = document.getElementById('btn-wiz-next-3');
  
  const btnPrev2 = document.getElementById('btn-wiz-prev-2');
  const btnPrev3 = document.getElementById('btn-wiz-prev-3');
  const btnPrev4 = document.getElementById('btn-wiz-prev-4');
  
  if (btnNext1) btnNext1.addEventListener('click', () => { currentStep = 2; updateStepUI(); });
  if (btnNext2) btnNext2.addEventListener('click', () => { currentStep = 3; updateStepUI(); });
  if (btnNext3) btnNext3.addEventListener('click', () => { currentStep = 4; updateStepUI(); });
  
  if (btnPrev2) btnPrev2.addEventListener('click', () => { currentStep = 1; updateStepUI(); });
  if (btnPrev3) btnPrev3.addEventListener('click', () => { currentStep = 2; updateStepUI(); });
  if (btnPrev4) btnPrev4.addEventListener('click', () => { currentStep = 3; updateStepUI(); });

  const occWedding = document.getElementById('occ-wedding');
  const occParty = document.getElementById('occ-party');
  
  const labelWedding = document.querySelector('label[for="occ-wedding"]');
  const labelParty = document.querySelector('label[for="occ-party"]');
  
  const wedPackagesContainer = document.getElementById('wiz-wed-packages');
  const partyPackagesContainer = document.getElementById('wiz-party-packages');
  const linenBox = document.getElementById('wiz-linen-box');
  
  function handleOccasionChange(occasion) {
    if (occasion === 'wedding') {
      if (labelWedding) labelWedding.classList.add('active');
      if (labelParty) labelParty.classList.remove('active');
      
      if (wedPackagesContainer) wedPackagesContainer.classList.remove('hidden');
      if (partyPackagesContainer) partyPackagesContainer.classList.add('hidden');
      if (linenBox) linenBox.classList.remove('hidden');
      
      populateDiningDropdown('wedding');
    } else {
      if (labelParty) labelParty.classList.add('active');
      if (labelWedding) labelWedding.classList.remove('active');
      
      if (wedPackagesContainer) wedPackagesContainer.classList.add('hidden');
      if (partyPackagesContainer) partyPackagesContainer.classList.remove('hidden');
      if (linenBox) linenBox.classList.add('hidden');
      
      populateDiningDropdown('party');
    }
    
    // Reset highlights on occasion change
    initializeCardHighlights();
    calculateReceipt();
  }
  
  if (occWedding) occWedding.addEventListener('change', () => handleOccasionChange('wedding'));
  if (occParty) occParty.addEventListener('change', () => handleOccasionChange('party'));

  const wedPkgRadios = document.querySelectorAll('input[name="wedding-pkg"]');
  wedPkgRadios.forEach(radio => {
    radio.addEventListener('change', () => {
      wedPkgRadios.forEach(r => {
        const card = document.querySelector(`label[for="${r.id}"]`);
        if (card) {
          card.classList.toggle('active', r.checked);
        }
      });
      calculateReceipt();
    });
  });

  const partyPkgRadios = document.querySelectorAll('input[name="party-pkg"]');
  partyPkgRadios.forEach(radio => {
    radio.addEventListener('change', () => {
      partyPkgRadios.forEach(r => {
        const card = document.querySelector(`label[for="${r.id}"]`);
        if (card) {
          card.classList.toggle('active', r.checked);
        }
      });
      calculateReceipt();
    });
  });

  function initializeCardHighlights() {
    wedPkgRadios.forEach(r => {
      const card = document.querySelector(`label[for="${r.id}"]`);
      if (card) card.classList.toggle('active', r.checked);
    });
    partyPkgRadios.forEach(r => {
      const card = document.querySelector(`label[for="${r.id}"]`);
      if (card) card.classList.toggle('active', r.checked);
    });
  }

  const drinksSelect = document.getElementById('wiz-drinks-select');
  const spiritsBox = document.getElementById('wiz-spirits-box');
  const cocktailsBox = document.getElementById('wiz-cocktails-box');
  
  function updateDrinksBoxes() {
    if (!drinksSelect) return;
    const drinksVal = drinksSelect.value;
    const isNone = (drinksVal === 'none');
    
    if (isNone) {
      const spiritsCheckbox = document.getElementById('wiz-add-spirits');
      const cocktailsCheckbox = document.getElementById('wiz-add-cocktails');
      if (spiritsCheckbox) spiritsCheckbox.checked = false;
      if (cocktailsCheckbox) cocktailsCheckbox.checked = false;
    }
    
    if (spiritsBox) spiritsBox.style.display = isNone ? 'none' : 'block';
    if (cocktailsBox) cocktailsBox.style.display = isNone ? 'none' : 'block';
  }
  
  if (drinksSelect) {
    drinksSelect.addEventListener('change', () => {
      updateDrinksBoxes();
      calculateReceipt();
    });
  }

  function calculateReceipt() {
    const occChecked = document.querySelector('input[name="occasion-type"]:checked');
    const occasionType = occChecked ? occChecked.value : 'wedding';
    
    const guestSlider = document.getElementById('wiz-guests-slider');
    const guests = guestSlider ? parseInt(guestSlider.value, 10) : 40;
    
    // Update guest display
    const guestsDisplay = document.getElementById('wiz-guests-display');
    if (guestsDisplay) guestsDisplay.textContent = guests;
    
    // Package price calculation
    let venueHire = 0;
    let venuePkgName = '';
    
    if (occasionType === 'wedding') {
      const wedPkgChecked = document.querySelector('input[name="wedding-pkg"]:checked');
      const wedPkg = wedPkgChecked ? wedPkgChecked.value : 'kiss-commit';
      
      if (wedPkg === 'kiss-commit') {
        venueHire = 2000;
        venuePkgName = 'Kiss & Commit Package';
      } else if (wedPkg === 'vows-vino') {
        venueHire = 4000;
        venuePkgName = 'Vows & Vino Package';
      } else if (wedPkg === 'big-day') {
        venueHire = guests <= 40 ? 6000 : 8000;
        venuePkgName = `The Big Day Package (${guests <= 40 ? '≤40' : '>40'} guests)`;
        // Update label in Step 2 if element exists
        const bigDayPriceLabel = document.getElementById('wiz-bigday-price-label');
        if (bigDayPriceLabel) {
          bigDayPriceLabel.textContent = guests <= 40 ? '$6,000 + GST' : '$8,000 + GST';
        }
      }
    } else {
      venueHire = 0;
      venuePkgName = 'Free Room Hire Celebration';
    }
    
    // Date checks
    const dateInput = document.getElementById('wiz-event-date');
    const dateVal = dateInput ? dateInput.value : '';
    let isSunday = false;
    let isWeekday = false;
    let dateText = '';
    
    if (dateVal) {
      const [year, month, day] = dateVal.split('-').map(Number);
      const dateObj = new Date(year, month - 1, day);
      const dayOfWeek = dateObj.getDay();
      isSunday = (dayOfWeek === 0);
      isWeekday = (dayOfWeek >= 1 && dayOfWeek <= 4);
      
      const daySuffix = (d) => {
        if (d > 3 && d < 21) return 'th';
        switch (d % 10) {
          case 1:  return "st";
          case 2:  return "nd";
          case 3:  return "rd";
          default: return "th";
        }
      };
      
      const monthNames = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
      ];
      
      dateText = `${dateObj.toLocaleDateString('en-AU', { weekday: 'long' })}, ${day}${daySuffix(day)} of ${monthNames[dateObj.getMonth()]} ${year}`;
    }
    
    // Weekday discount (Weddings only, Mon-Thu)
    let weekdayDiscount = 0;
    if (occasionType === 'wedding' && isWeekday && venueHire > 0) {
      weekdayDiscount = 1000;
    }
    
    // Dining cost calculation
    let foodCost = 0;
    let diningName = 'None';
    const selectedDiningVal = diningSelect ? diningSelect.value : '';
    const optionsList = occasionType === 'wedding' ? weddingDiningOptions : partyDiningOptions;
    const selectedDining = optionsList.find(o => o.value === selectedDiningVal);
    
    if (selectedDining) {
      diningName = selectedDining.text.split(' — ')[0];
      if (selectedDining.type === 'per-head') {
        foodCost = selectedDining.price * guests;
      } else {
        foodCost = selectedDining.price;
      }
    }
    
    // Seafood Fountain check
    let seafoodFountainCost = 0;
    const seafoodFountainCheckbox = document.getElementById('wiz-seafood-fountain');
    const hasSeafoodFountain = seafoodFountainCheckbox && seafoodFountainCheckbox.checked;
    if (hasSeafoodFountain) {
      seafoodFountainCost = (25 * guests) + 100;
    }
    
    // Beverage cost calculation
    let beverageCost = 0;
    let drinksName = 'None';
    const drinksSelectVal = drinksSelect ? drinksSelect.value : 'none';
    
    if (drinksSelectVal === 'house') {
      beverageCost = 75 * guests;
      drinksName = 'House Beverage Package';
    } else if (drinksSelectVal === 'deluxe') {
      beverageCost = 110 * guests;
      drinksName = 'Deluxe Beverage Package';
    } else {
      drinksName = 'Cash Bar / Custom Tab';
    }
    
    // Drinks add-ons
    let spiritsCost = 0;
    const spiritsCheckbox = document.getElementById('wiz-add-spirits');
    const hasSpirits = spiritsCheckbox && spiritsCheckbox.checked;
    if (hasSpirits && drinksSelectVal !== 'none') {
      spiritsCost = 16 * guests;
    }
    
    let cocktailsCost = 0;
    const cocktailsCheckbox = document.getElementById('wiz-add-cocktails');
    const hasCocktails = cocktailsCheckbox && cocktailsCheckbox.checked;
    if (hasCocktails && drinksSelectVal !== 'none') {
      cocktailsCost = 22 * guests;
    }
    
    // Upgrades: Linen (weddings only)
    let linenCost = 0;
    const linenCheckbox = document.getElementById('wiz-linen-upgrade');
    const hasLinen = linenCheckbox && linenCheckbox.checked && occasionType === 'wedding';
    const tablesCount = Math.ceil(guests / 10);
    if (hasLinen) {
      linenCost = tablesCount * 40;
    }
    
    // Math totals
    const subtotalBeforeDiscounts = venueHire + foodCost + seafoodFountainCost + beverageCost + spiritsCost + cocktailsCost + linenCost;
    const subtotal = subtotalBeforeDiscounts - weekdayDiscount;
    
    let sundaySurcharge = 0;
    if (isSunday) {
      sundaySurcharge = subtotal * 0.10;
    }
    
    const gstVal = (subtotal + sundaySurcharge) * 0.10;
    const totalVal = subtotal + sundaySurcharge + gstVal;
    
    // Update Receipt Summary UI elements
    const subtotalEl = document.getElementById('receipt-subtotal');
    const gstEl = document.getElementById('receipt-gst');
    const totalEl = document.getElementById('receipt-total');
    
    if (subtotalEl) subtotalEl.textContent = formatPrice(subtotal);
    if (gstEl) gstEl.textContent = formatPrice(gstVal);
    if (totalEl) totalEl.textContent = formatPrice(totalVal);
    
    // Render Receipt Items dynamically
    const receiptItemsContainer = document.getElementById('wiz-receipt-items');
    if (receiptItemsContainer) {
      receiptItemsContainer.innerHTML = '';
      
      // Helper function to append item rows to receipt list
      const appendRow = (label, value, isNegative = false) => {
        const row = document.createElement('div');
        row.className = 'receipt-row';
        if (isNegative) {
          row.style.color = '#a94442';
        }
        
        const labelSpan = document.createElement('span');
        labelSpan.textContent = label;
        
        const valueSpan = document.createElement('span');
        valueSpan.textContent = isNegative ? `-${formatPrice(value)}` : formatPrice(value);
        if (isNegative) valueSpan.style.color = '#a94442';
        
        row.appendChild(labelSpan);
        row.appendChild(valueSpan);
        receiptItemsContainer.appendChild(row);
      };
      
      // 1. Venue Hire
      if (occasionType === 'wedding' || venueHire > 0) {
        appendRow(`Venue Hire (${venuePkgName})`, venueHire);
      } else {
        appendRow('Venue Hire (Free Room Hire Promotion)', 0);
      }
      
      // 2. Weekday Discount
      if (weekdayDiscount > 0) {
        appendRow('Weekday Venue Discount (Mon-Thu)', weekdayDiscount, true);
      }
      
      // 3. Dining Menu
      if (foodCost > 0) {
        const details = selectedDining && selectedDining.type === 'per-head' ? ` ($${selectedDining.price} pp)` : '';
        appendRow(`Dining: ${diningName}${details}`, foodCost);
      }
      
      // 4. Seafood Fountain
      if (hasSeafoodFountain) {
        appendRow(`Seafood Fountain ($25 pp + $100)`, seafoodFountainCost);
      }
      
      // 5. Beverage Package
      if (beverageCost > 0) {
        const pp = drinksSelectVal === 'house' ? 75 : 110;
        appendRow(`Beverages: ${drinksName} ($${pp} pp)`, beverageCost);
      }
      
      // 6. Spirits Addon
      if (hasSpirits && drinksSelectVal !== 'none') {
        appendRow('Beverage Upgrade: Spirits (+$16 pp)', spiritsCost);
      }
      
      // 7. Cocktails Addon
      if (hasCocktails && drinksSelectVal !== 'none') {
        appendRow('Beverage Upgrade: Cocktails (+$22 pp)', cocktailsCost);
      }
      
      // 8. Linen Upgrade
      if (hasLinen) {
        appendRow(`Linen Upgrade (${tablesCount} tables @ $40)`, linenCost);
      }
      
      // 9. Sunday Surcharge
      if (sundaySurcharge > 0) {
        appendRow('Sunday Surcharge (10%)', sundaySurcharge);
      }
    }
    
    // Minimum spend check for Parties
    const minWarningEl = document.getElementById('receipt-min-warning');
    if (occasionType === 'party') {
      const fbSpend = foodCost + seafoodFountainCost + beverageCost + spiritsCost + cocktailsCost;
      const requiresMinWarning = fbSpend < 3000;
      if (minWarningEl) {
        minWarningEl.classList.toggle('hidden', !requiresMinWarning);
      }
    } else {
      if (minWarningEl) minWarningEl.classList.add('hidden');
    }
    
    return {
      occasionType,
      guests,
      venuePkgName,
      venueHire,
      weekdayDiscount,
      diningName,
      foodCost,
      hasSeafoodFountain,
      seafoodFountainCost,
      drinksName,
      beverageCost,
      hasSpirits,
      spiritsCost,
      hasCocktails,
      cocktailsCost,
      hasLinen,
      linenCost,
      tablesCount,
      dateVal,
      dateText,
      subtotal,
      isSunday,
      sundaySurcharge,
      gstVal,
      totalVal
    };
  }

  const guestSlider = document.getElementById('wiz-guests-slider');
  if (guestSlider) guestSlider.addEventListener('input', calculateReceipt);
  
  const eventDateInput = document.getElementById('wiz-event-date');
  if (eventDateInput) eventDateInput.addEventListener('change', calculateReceipt);
  
  if (diningSelect) diningSelect.addEventListener('change', calculateReceipt);
  
  const seafoodFountainCheckbox = document.getElementById('wiz-seafood-fountain');
  if (seafoodFountainCheckbox) seafoodFountainCheckbox.addEventListener('change', calculateReceipt);
  
  const linenCheckbox = document.getElementById('wiz-linen-upgrade');
  if (linenCheckbox) linenCheckbox.addEventListener('change', calculateReceipt);
  
  const spiritsCheckbox = document.getElementById('wiz-add-spirits');
  if (spiritsCheckbox) spiritsCheckbox.addEventListener('change', calculateReceipt);
  
  const cocktailsCheckbox = document.getElementById('wiz-add-cocktails');
  if (cocktailsCheckbox) cocktailsCheckbox.addEventListener('change', calculateReceipt);

  function handleHandoff() {
    // Validate date input first
    const dateInput = document.getElementById('wiz-event-date');
    if (dateInput && !dateInput.value) {
      alert('Please select a preferred event date in Step 4 before submitting.');
      currentStep = 4;
      updateStepUI();
      dateInput.focus();
      return;
    }

    const summary = calculateReceipt();
    if (!summary) return;
    
    // Pre-fill Enquiry Type
    if (contactServiceSelect) {
      if (summary.occasionType === 'wedding') {
        contactServiceSelect.value = 'wedding';
      } else {
        contactServiceSelect.value = 'private-event';
      }
    }
    
    // Pre-fill Preferred Package
    if (contactPackageSelect) {
      if (summary.occasionType === 'wedding') {
        const wedPkgChecked = document.querySelector('input[name="wedding-pkg"]:checked');
        const wedPkg = wedPkgChecked ? wedPkgChecked.value : 'kiss-commit';
        contactPackageSelect.value = wedPkg;
      } else {
        contactPackageSelect.value = 'party-hire';
      }
    }
    
    // Pre-fill Message
    const contactMessage = document.getElementById('contact-message');
    if (contactMessage) {
      let msg = `=========================================\n`;
      msg += `RIVIERA EVENT PLANNER SUMMARY\n`;
      msg += `=========================================\n`;
      msg += `Occasion: ${summary.occasionType === 'wedding' ? 'Beachfront Wedding' : 'Private Celebration / Party'}\n`;
      msg += `Venue Package: ${summary.venuePkgName} (${formatPrice(summary.venueHire)} excl. GST)\n`;
      if (summary.weekdayDiscount > 0) {
        msg += `Weekday Discount Applied: -${formatPrice(summary.weekdayDiscount)}\n`;
      }
      msg += `Date of Event: ${summary.dateText ? summary.dateText : 'Not specified yet'}\n`;
      msg += `Number of Guests: ${summary.guests} guests\n`;
      msg += `Dining Menu Style: ${summary.diningName} (${formatPrice(summary.foodCost)} excl. GST)\n`;
      if (summary.hasSeafoodFountain) {
        msg += `Catering Upgrade: 3-Tier Seafood Fountain (${formatPrice(summary.seafoodFountainCost)} excl. GST)\n`;
      }
      msg += `Beverages: ${summary.drinksName} (${formatPrice(summary.beverageCost)} excl. GST)\n`;
      if (summary.hasSpirits) {
        msg += `Drinks Upgrade: Basic Spirits (${formatPrice(summary.spiritsCost)} excl. GST)\n`;
      }
      if (summary.hasCocktails) {
        msg += `Drinks Upgrade: Signature Cocktails (${formatPrice(summary.cocktailsCost)} excl. GST)\n`;
      }
      if (summary.hasLinen) {
        msg += `Venue Upgrade: Natural French Linen Tablecloths for ${summary.tablesCount} tables (${formatPrice(summary.linenCost)} excl. GST)\n`;
      }
      msg += `-----------------------------------------\n`;
      msg += `Subtotal (excl. GST): ${formatPrice(summary.subtotal)}\n`;
      if (summary.isSunday) {
        msg += `Sunday Surcharge (10%): ${formatPrice(summary.sundaySurcharge)}\n`;
      }
      msg += `GST (10%): ${formatPrice(summary.gstVal)}\n`;
      msg += `-----------------------------------------\n`;
      msg += `Estimated Total: ${formatPrice(summary.totalVal)} (GST Incl.)\n`;
      msg += `=========================================\n\n`;
      msg += `Hi Sally, I've built this event plan using your Riviera Event Wizard. I'd love to discuss availability and details!`;
      
      contactMessage.value = msg;
    }
    
    // Scroll to contact form
    const contactSection = document.getElementById('contact');
    if (contactSection) {
      contactSection.scrollIntoView({ behavior: 'smooth' });
    }
  }
  
  const btnWizSubmit = document.getElementById('btn-wiz-submit');
  const btnReceiptEnquire = document.getElementById('btn-receipt-enquire');
  
  if (btnWizSubmit) btnWizSubmit.addEventListener('click', handleHandoff);
  if (btnReceiptEnquire) btnReceiptEnquire.addEventListener('click', handleHandoff);

  // Initial setup call
  handleOccasionChange('wedding');
  updateStepUI();
});
