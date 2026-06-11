// Total Pest & Carpet Main JS

document.addEventListener('DOMContentLoaded', () => {
  // --- Mobile Menu Toggle ---
  const mobileToggle = document.getElementById('mobile-toggle');
  const navMenu = document.getElementById('nav-menu');
  
  mobileToggle.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    const spans = mobileToggle.querySelectorAll('span');
    if (navMenu.classList.contains('active')) {
      spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
      spans[1].style.opacity = '0';
      spans[2].style.transform = 'rotate(-45deg) translate(6px, -7px)';
    } else {
      spans[0].style.transform = 'none';
      spans[1].style.opacity = '1';
      spans[2].style.transform = 'none';
    }
  });

  // Close menu when clicking link
  const navLinks = document.querySelectorAll('.nav-link');
  navLinks.forEach(link => {
    link.addEventListener('click', () => {
      navMenu.classList.remove('active');
      const spans = mobileToggle.querySelectorAll('span');
      spans[0].style.transform = 'none';
      spans[1].style.opacity = '1';
      spans[2].style.transform = 'none';
    });
  });


  // --- Quote Calculator Logic ---
  const sliderBedrooms = document.getElementById('num-bedrooms');
  const sliderLiving = document.getElementById('num-living');
  const valBedrooms = document.getElementById('val-bedrooms');
  const valLiving = document.getElementById('val-living');
  
  const checkCards = document.querySelectorAll('.calc-check-card');
  const calcTotalEl = document.getElementById('calc-total');
  const breakdownList = document.getElementById('quote-breakdown-list');
  const formPackageInput = document.getElementById('q-package');

  // Rates
  const rateBedroom = 40;
  const rateLiving = 55;
  const ratesAddons = {
    hallway: 20,
    stairs: 45,
    sanitiser: 30,
    'flea-pest': 90
  };

  let activeAddons = {
    hallway: false,
    stairs: false,
    sanitiser: false,
    'flea-pest': false
  };

  function updateCalculator() {
    const bedrooms = parseInt(sliderBedrooms.value);
    const living = parseInt(sliderLiving.value);

    // Update Slider text
    valBedrooms.textContent = bedrooms === 1 ? `1 Bedroom` : `${bedrooms} Bedrooms`;
    valLiving.textContent = living === 1 ? `1 Room` : `${living} Rooms`;

    // Calculate sum
    let total = 0;
    let breakdownHTML = '';

    if (bedrooms > 0) {
      const cost = bedrooms * rateBedroom;
      total += cost;
      breakdownHTML += `<div class="breakdown-row"><span>${bedrooms} Bedrooms steam clean</span><strong>$${cost}</strong></div>`;
    }

    if (living > 0) {
      const cost = living * rateLiving;
      total += cost;
      breakdownHTML += `<div class="breakdown-row"><span>${living} Living rooms steam clean</span><strong>$${cost}</strong></div>`;
    }

    // Addons
    Object.keys(activeAddons).forEach(key => {
      if (activeAddons[key]) {
        const cost = ratesAddons[key];
        total += cost;
        
        let label = "";
        if (key === 'hallway') label = "Hallway treatment";
        if (key === 'stairs') label = "Flight of stairs steam";
        if (key === 'sanitiser') label = "Deluxe sanitisation flush";
        if (key === 'flea-pest') label = "End-of-lease Flea Spray";

        breakdownHTML += `<div class="breakdown-row"><span>+ ${label}</span><strong>$${cost}</strong></div>`;
      }
    });

    breakdownHTML += `<div class="breakdown-row total"><span>Estimated Total</span><strong>$${total}</strong></div>`;
    
    // Render breakdown and total
    breakdownList.innerHTML = breakdownHTML;
    calcTotalEl.textContent = total;

    // Update Form input text
    if (formPackageInput.value.startsWith('Custom')) {
      formPackageInput.value = `Custom Quote ($${total})`;
    }
  }

  // Handle slide inputs
  sliderBedrooms.addEventListener('input', updateCalculator);
  sliderLiving.addEventListener('input', updateCalculator);

  // Handle addon card toggles
  checkCards.forEach(card => {
    card.addEventListener('click', () => {
      const addonKey = card.dataset.addon;
      const isChecked = card.classList.contains('checked');

      if (isChecked) {
        card.classList.remove('checked');
        activeAddons[addonKey] = false;
      } else {
        card.classList.add('checked');
        activeAddons[addonKey] = true;
      }
      
      updateCalculator();
    });
  });

  // Run initial calculator render
  updateCalculator();


  // --- Package Selector Buttons ---
  const pkgButtons = document.querySelectorAll('.pkg-select');
  pkgButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const pkgName = btn.dataset.pkgName;
      if (pkgName) {
        formPackageInput.value = pkgName;
        // Optionally fill notes field
        const notes = document.getElementById('q-notes');
        notes.value = `Hi, I would like to book the ${pkgName}. Please contact me to secure a slot.`;
      }
    });
  });

  // Re-enable Custom quote selector when booking via calculator
  const claimQuoteBtn = document.getElementById('claim-quote-btn');
  claimQuoteBtn.addEventListener('click', () => {
    formPackageInput.value = `Custom Quote ($${calcTotalEl.textContent})`;
    const notes = document.getElementById('q-notes');
    notes.value = `Hi, I would like to book my custom quote. Details: ${sliderBedrooms.value} Bedrooms, ${sliderLiving.value} Living rooms. Addons: ${Object.keys(activeAddons).filter(k => activeAddons[k]).join(', ')}.`;
  });


  // --- Form Submission Handling ---
  const quoteForm = document.getElementById('quote-form');
  const successMsg = document.getElementById('quote-success-message');

  quoteForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const btn = document.getElementById('btn-submit-quote');
    btn.disabled = true;
    btn.textContent = 'Verifying Area Slots...';

    setTimeout(() => {
      btn.textContent = 'Quote Secured!';
      successMsg.classList.remove('hidden');
      quoteForm.reset();
      
      // Reset addon classes
      checkCards.forEach(card => card.classList.remove('checked'));
      Object.keys(activeAddons).forEach(k => activeAddons[k] = false);
      sliderBedrooms.value = 3;
      sliderLiving.value = 1;
      updateCalculator();

      setTimeout(() => {
        successMsg.classList.add('hidden');
        btn.disabled = false;
        btn.textContent = 'Request Booking With This Quote';
      }, 8000);
    }, 1200);
  });
});
