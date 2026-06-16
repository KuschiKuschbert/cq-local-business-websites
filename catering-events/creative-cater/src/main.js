import './mobile-ux.js';
import './style.css';

// Packages configuration
const packagesInfo = {
  soiree: {
    name: 'The Soirée Package',
    price: 65,
  },
  luxe: {
    name: 'The Luxe Wedding',
    price: 95,
  },
  reserve: {
    name: 'The Reserve Estate',
    price: 145,
  }
};

document.addEventListener('DOMContentLoaded', () => {
  // 1. Sticky Header scroll styling
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

  menuToggle.addEventListener('click', () => {
    const isVisible = primaryNav.getAttribute('data-visible') === 'true';
    if (!isVisible) {
      primaryNav.setAttribute('data-visible', 'true');
      menuToggle.setAttribute('aria-expanded', 'true');
    } else {
      primaryNav.setAttribute('data-visible', 'false');
      menuToggle.setAttribute('aria-expanded', 'false');
    }
  });

  // Close mobile navigation when a link is clicked
  const navLinks = document.querySelectorAll('.nav-link');
  navLinks.forEach(link => {
    link.addEventListener('click', () => {
      primaryNav.setAttribute('data-visible', 'false');
      menuToggle.setAttribute('aria-expanded', 'false');
    });
  });

  // 3. Showcase Filter Tabs
  const filterTabs = document.querySelectorAll('.filter-tab');
  const showcaseCards = document.querySelectorAll('.showcase-card');

  filterTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      // Set active tab styling
      filterTabs.forEach(t => {
        t.classList.remove('active');
        t.setAttribute('aria-selected', 'false');
      });
      tab.classList.add('active');
      tab.setAttribute('aria-selected', 'true');

      // Filter logic
      const filterValue = tab.getAttribute('data-filter');
      showcaseCards.forEach(card => {
        const category = card.getAttribute('data-category');
        if (filterValue === 'all' || category === filterValue) {
          card.style.display = 'flex';
          setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'scale(1)';
          }, 10);
        } else {
          card.style.opacity = '0';
          card.style.transform = 'scale(0.95)';
          setTimeout(() => {
            card.style.display = 'none';
          }, 400); // match standard transition speed
        }
      });
    });
  });

  // 4. Mobile Trailer Package Selector Buttons
  const selectPackageBtns = document.querySelectorAll('.btn-select-package');
  const packageCards = document.querySelectorAll('.package-card');
  const packageSelectElement = document.getElementById('input-package');

  function updateSelectedPackageUI(packageId) {
    // Update package cards border/highlights
    packageCards.forEach(card => {
      card.classList.remove('selected');
      const cardSelectBtn = card.querySelector('.btn-select-package');
      if (card.getAttribute('data-package') === packageId) {
        card.classList.add('selected');
        if (cardSelectBtn) {
          cardSelectBtn.innerText = 'Selected';
          cardSelectBtn.classList.remove('btn-gold-outline');
          cardSelectBtn.classList.add('btn-gold');
        }
      } else {
        if (cardSelectBtn) {
          cardSelectBtn.innerText = 'Select Package';
          if (!card.classList.contains('featured')) {
            cardSelectBtn.classList.add('btn-gold-outline');
            cardSelectBtn.classList.remove('btn-gold');
          }
        }
      }
    });

    // Sync select input in estimator
    packageSelectElement.value = packageId;
    calculateEstimate();
  }

  selectPackageBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      const packageId = e.target.getAttribute('data-package');
      updateSelectedPackageUI(packageId);
      
      // Smooth scroll to estimator
      document.getElementById('estimator').scrollIntoView({ behavior: 'smooth' });
    });
  });

  // Highlight default selected card on load
  updateSelectedPackageUI('luxe');

  // 5. Interactive Pricing Estimator Calculations
  const guestsSlider = document.getElementById('input-guests');
  const guestsValLabel = document.getElementById('val-guests');
  
  const addonOysters = document.getElementById('addon-oysters');
  const addonCocktails = document.getElementById('addon-cocktails');
  const addonSliders = document.getElementById('addon-sliders');

  // Results labels
  const summaryPackageName = document.getElementById('summary-package-name');
  const summaryGuests = document.getElementById('summary-guests');
  const summaryBaseCost = document.getElementById('summary-base-cost');
  const summaryAddonsCost = document.getElementById('summary-addons-cost');
  const totalInvestment = document.getElementById('total-investment');

  function calculateEstimate() {
    const guestCount = parseInt(guestsSlider.value, 10);
    const selectedPkgId = packageSelectElement.value;
    const pkg = packagesInfo[selectedPkgId];

    // Label Update
    guestsValLabel.innerText = guestCount;
    summaryGuests.innerText = `${guestCount} guests`;
    
    // Base package cost calculation
    const baseRate = pkg.price;
    const baseTotal = baseRate * guestCount;

    // Addons calculations
    let addonsPerGuestRate = 0;
    if (addonOysters.checked) addonsPerGuestRate += parseFloat(addonOysters.value);
    if (addonCocktails.checked) addonsPerGuestRate += parseFloat(addonCocktails.value);
    if (addonSliders.checked) addonsPerGuestRate += parseFloat(addonSliders.value);
    
    const addonsTotal = addonsPerGuestRate * guestCount;
    const grandTotal = baseTotal + addonsTotal;

    // Display updates
    summaryPackageName.innerText = pkg.name;
    summaryBaseCost.innerText = `$${baseTotal.toLocaleString()}`;
    summaryAddonsCost.innerText = `$${addonsTotal.toLocaleString()}`;
    totalInvestment.innerText = `$${grandTotal.toLocaleString()}`;
  }

  // Bind inputs
  guestsSlider.addEventListener('input', calculateEstimate);
  packageSelectElement.addEventListener('change', (e) => {
    updateSelectedPackageUI(e.target.value);
  });
  
  addonOysters.addEventListener('change', calculateEstimate);
  addonCocktails.addEventListener('change', calculateEstimate);
  addonSliders.addEventListener('change', calculateEstimate);

  // Initial pricing calculation call
  calculateEstimate();

  // 6. Apply Quote to Inquiry Form
  const applyQuoteBtn = document.getElementById('btn-quote-apply');
  const formGuestsInput = document.getElementById('form-guests');
  const formPackageDetailsInput = document.getElementById('form-details-package');

  applyQuoteBtn.addEventListener('click', () => {
    const guestCount = guestsSlider.value;
    const selectedPkgId = packageSelectElement.value;
    const pkg = packagesInfo[selectedPkgId];

    // Build addons text
    let selectedAddons = [];
    if (addonOysters.checked) selectedAddons.push('Oyster Shucking Bar');
    if (addonCocktails.checked) selectedAddons.push('Premium Cocktails');
    if (addonSliders.checked) selectedAddons.push('Midnight Snack Box');

    const addonsText = selectedAddons.length > 0 ? ` + Add-ons (${selectedAddons.join(', ')})` : '';
    
    // Fill in form values
    formGuestsInput.value = guestCount;
    formPackageDetailsInput.value = `${pkg.name}${addonsText}`;

    // Add subtle visual cue to inputs that were updated
    formGuestsInput.style.borderColor = 'var(--color-gold)';
    formPackageDetailsInput.style.borderColor = 'var(--color-gold)';
    setTimeout(() => {
      formGuestsInput.style.borderColor = '';
      formPackageDetailsInput.style.borderColor = '';
    }, 1500);

    // Smooth scroll to form
    document.getElementById('inquiry').scrollIntoView({ behavior: 'smooth' });
  });

  // 7. Elegant Form Submit Simulation
  const inquiryForm = document.getElementById('wedding-inquiry-form');
  const formStatus = document.getElementById('form-status');
  const submitBtn = document.getElementById('form-submit-btn');
  const btnText = submitBtn.querySelector('.btn-text');
  const btnSpinner = submitBtn.querySelector('.btn-spinner');

  inquiryForm.addEventListener('submit', (e) => {
    e.preventDefault();

    // Show loading spinner & disable button
    submitBtn.disabled = true;
    btnText.style.opacity = '0.5';
    btnSpinner.style.display = 'inline-block';

    // Simulate server request
    setTimeout(() => {
      submitBtn.disabled = false;
      btnText.style.opacity = '1';
      btnSpinner.style.display = 'none';

      // Show gorgeous success notification
      formStatus.innerText = 'Thank you. Your inquiry has been secured. Our lead catering concierge will contact you within 24 hours to schedule a bespoke menu design session.';
      formStatus.className = 'form-status success';
      formStatus.style.display = 'block';

      // Reset form fields
      inquiryForm.reset();
      
      // Re-fill default packages & recalculate estimator
      updateSelectedPackageUI('luxe');
      calculateEstimate();

      // Scroll form status into view
      formStatus.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 1800);
  });
});
