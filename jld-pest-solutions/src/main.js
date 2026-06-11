// JLD Pest Solutions Main JS

document.addEventListener('DOMContentLoaded', () => {
  // --- Navbar Scroll Handling ---
  const navbar = document.getElementById('navbar');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  });

  // --- Mobile Menu Toggle ---
  const mobileToggle = document.getElementById('mobile-toggle');
  const navMenu = document.getElementById('nav-menu');
  mobileToggle.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    mobileToggle.classList.toggle('active');
    // Simple burger lines transformation
    const spans = mobileToggle.querySelectorAll('span');
    if (navMenu.classList.contains('active')) {
      spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
      spans[1].style.opacity = '0';
      spans[2].style.transform = 'rotate(-45deg) translate(7px, -8px)';
    } else {
      spans[0].style.transform = 'none';
      spans[1].style.opacity = '1';
      spans[2].style.transform = 'none';
    }
  });

  // Close menu when clicking a link
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


  // --- Interactive Plan Configurator Logic ---
  const houseOptions = document.querySelectorAll('.option-btn');
  const pestCheckboxCards = document.querySelectorAll('.pest-checkbox-card');
  const calcPriceEl = document.getElementById('calc-price');
  const calcPlanDescEl = document.getElementById('calc-plan-desc');
  const calcFeaturesEl = document.getElementById('calc-features');
  const recommendedPlanBadge = document.getElementById('recommended-plan-badge');
  const planDropdown = document.getElementById('book-plan');

  let selectedSize = 'small'; // default
  let activePests = {
    insects: true,
    rodents: true,
    termites: false,
    fleas: false
  };

  // Base prices
  const basePrices = {
    small: 100,
    medium: 170,
    large: 230
  };

  // Pest add-on costs
  const pestCosts = {
    insects: 40,
    rodents: 50,
    termites: 150,
    fleas: 60
  };

  function calculatePlan() {
    let price = basePrices[selectedSize];
    let selectedPestCount = 0;
    
    // Add cost of selected pests
    Object.keys(activePests).forEach(pest => {
      if (activePests[pest]) {
        price += pestCosts[pest];
        selectedPestCount++;
      }
    });

    // Update Price Display
    calcPriceEl.textContent = price;

    // Update Plan Name and Badge based on choices
    let planName = "Custom Eco Shield";
    let planDescription = "";
    
    if (activePests.termites) {
      planName = "Eco-Complete + Termite";
      recommendedPlanBadge.textContent = "Eco-Ultimate Barrier";
      planDescription = `Premium structural inspection and botanical shield for a ${selectedSize} Yeppoon home.`;
    } else if (activePests.insects && activePests.rodents && !activePests.fleas) {
      planName = "Eco-Guard Premium";
      recommendedPlanBadge.textContent = "Eco-Guard Premium";
      planDescription = `Perfect general residential pest & rodent barrier for a ${selectedSize} Capricorn Coast property.`;
    } else if (selectedPestCount <= 1) {
      planName = "Eco-Essential";
      recommendedPlanBadge.textContent = "Eco-Essential";
      planDescription = `Targeted local barrier for single pest concerns in a ${selectedSize} property.`;
    } else {
      planName = "Custom Eco Shield";
      recommendedPlanBadge.textContent = "Custom Shield";
      planDescription = `Specialized botanical defense program tailored to your exact property specifications.`;
    }

    calcPlanDescEl.textContent = planDescription;

    // Build feature lists dynamically
    let featuresHTML = '';
    if (activePests.insects) {
      featuresHTML += `<div class="preview-feature-item">🌿 Cockroaches, Ants, Spiders internal & skirting treatment</div>`;
    }
    if (activePests.rodents) {
      featuresHTML += `<div class="preview-feature-item">🐭 Safe botanical rodent baiting stations</div>`;
    }
    if (activePests.termites) {
      featuresHTML += `<div class="preview-feature-item">🔍 Thermal imaging and radar termite sweep</div>`;
    }
    if (activePests.fleas) {
      featuresHTML += `<div class="preview-feature-item">🐶 Pet-friendly end-of-lease flea treatment</div>`;
    }
    featuresHTML += `<div class="preview-feature-item">🗓️ 12-Month service guarantee validation</div>`;

    calcFeaturesEl.innerHTML = featuresHTML;

    // Auto-update booking form selection details
    // We update the option or store it in window.customPlanDetails
    window.customPlanName = `${planName} ($${price})`;
  }

  // Handle House Size Selection
  houseOptions.forEach(btn => {
    btn.addEventListener('click', () => {
      houseOptions.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      selectedSize = btn.dataset.size;
      calculatePlan();
    });
  });

  // Handle Pest Selection Checkboxes
  pestCheckboxCards.forEach(card => {
    card.addEventListener('click', () => {
      const checkbox = card.querySelector('.hidden-chk');
      const pestKey = card.dataset.pest;

      checkbox.checked = !checkbox.checked;
      activePests[pestKey] = checkbox.checked;

      if (checkbox.checked) {
        card.classList.add('checked');
      } else {
        card.classList.remove('checked');
      }

      calculatePlan();
    });
  });

  // Run initial calculation
  calculatePlan();

  // --- CTA Button actions ---
  // If user clicks "Choose" on pricing table, set booking form values and scroll
  const pricingButtons = document.querySelectorAll('.plan-select-btn');
  pricingButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      const planName = btn.dataset.planName;
      if (planName) {
        planDropdown.value = planName;
      }
    });
  });

  const customPlanBtn = document.getElementById('select-custom-plan');
  customPlanBtn.addEventListener('click', () => {
    // If selecting custom plan, set dropdown value to Custom
    planDropdown.value = "Custom Plan";
    const notesField = document.getElementById('book-notes');
    notesField.value = `Hi, I built a custom plan using the interactive tool: Size: ${selectedSize.toUpperCase()}, Pests: ${Object.keys(activePests).filter(k => activePests[k]).join(', ')}. Price: $${calcPriceEl.textContent}.`;
  });

  // --- Booking Form Submit handling ---
  const bookingForm = document.getElementById('booking-form');
  const successMessage = document.getElementById('booking-success-message');

  bookingForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const btn = document.getElementById('btn-submit-booking');
    btn.disabled = true;
    btn.textContent = 'Processing Request...';

    setTimeout(() => {
      btn.textContent = 'Requested Successfully!';
      successMessage.classList.remove('hidden');
      bookingForm.reset();
      
      // Auto hide after 8 seconds
      setTimeout(() => {
        successMessage.classList.add('hidden');
        btn.disabled = false;
        btn.textContent = 'Request Booking Details';
      }, 8000);
    }, 1200);
  });
});
