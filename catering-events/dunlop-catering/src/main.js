import './style.css';

document.addEventListener('DOMContentLoaded', () => {
  // --- DOM Selectors ---
  
  // Mobile Nav Toggle
  const navToggleBtn = document.getElementById('nav-toggle-btn');
  const mainNav = document.getElementById('main-nav');
  
  // Package Quick Select Buttons
  const selectPackageBtns = document.querySelectorAll('.select-package-btn');
  
  // Wedding Menu Builder
  const weddingMains = document.getElementsByName('wedding-mains');
  const weddingSides = document.getElementsByName('wedding-sides');
  const weddingDesserts = document.getElementsByName('wedding-desserts');
  const weddingApplyBtn = document.getElementById('wedding-apply-btn');
  
  // Interactive Calculator
  const guestSlider = document.getElementById('guest-slider');
  const guestCountVal = document.getElementById('guest-count-val');
  const calcPackageSelect = document.getElementById('calc-package');
  const addonChecks = document.getElementsByName('addons');
  
  // Calculator Display Rows
  const scaledPriceHead = document.getElementById('scaled-price-head');
  const breakdownBase = document.getElementById('breakdown-base');
  const breakdownPremiumRow = document.getElementById('breakdown-premium-row');
  const breakdownPremium = document.getElementById('breakdown-premium');
  const breakdownAddons = document.getElementById('breakdown-addons');
  const breakdownTotal = document.getElementById('breakdown-total');
  const weddingSummaryBox = document.getElementById('wedding-summary-box');
  const weddingMenuSummaryList = document.getElementById('wedding-menu-summary-list');
  const weddingPremiumNotice = document.getElementById('wedding-premium-notice');
  const calcApplyToFormBtn = document.getElementById('calc-apply-to-form-btn');
  
  // Form Elements
  const cateringForm = document.getElementById('catering-quote-form');
  const formName = document.getElementById('form-name');
  const formEmail = document.getElementById('form-email');
  const formPhone = document.getElementById('form-phone');
  const formDate = document.getElementById('form-date');
  const formVenue = document.getElementById('form-venue');
  const formGuests = document.getElementById('form-guests');
  const formPackage = document.getElementById('form-package');
  const formAddonsContainer = document.getElementById('form-addons-tags-container');
  
  // Dialog Elements
  const quoteSuccessDialog = document.getElementById('quote-success-dialog');
  const dialogCloseBtn = document.getElementById('dialog-close-btn');
  const dialogQuoteRef = document.getElementById('dialog-quote-ref');
  const dialogGuests = document.getElementById('dialog-guests');
  const dialogPackage = document.getElementById('dialog-package');
  const dialogWeddingMenuRow = document.getElementById('dialog-wedding-menu-row');
  const dialogWeddingMenuDetails = document.getElementById('dialog-wedding-menu-details');
  const dialogAddonsDetails = document.getElementById('dialog-addons-details');
  const dialogTotal = document.getElementById('dialog-total');
  const dialogUserEmail = document.getElementById('dialog-user-email');

  // --- Pricing Models ---
  const packagesPricing = {
    classic: { name: 'The Classic Spit Roast', 49: 45, 99: 38, 199: 32, max: 28 },
    buffet: { name: 'The Grand Feast Buffet', 49: 55, 99: 48, 199: 42, max: 38 },
    grazing: { name: 'Rustic Grazing & Roast', 49: 65, 99: 58, 199: 52, max: 48 },
    wedding: { name: 'Bespoke Wedding Menu', 49: 75, 99: 68, 199: 62, max: 58 }
  };

  // --- 1. Mobile Navigation Toggle ---
  if (navToggleBtn && mainNav) {
    navToggleBtn.addEventListener('click', () => {
      mainNav.classList.toggle('open');
      navToggleBtn.classList.toggle('open');
    });
    
    // Close nav when list link is clicked on mobile
    mainNav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        mainNav.classList.remove('open');
        navToggleBtn.classList.remove('open');
      });
    });
  }

  // --- 2. Wedding Menu Checklist Constraints (Mains max 3, Sides max 4, Desserts max 2) ---
  const setupCheckboxLimit = (checkboxes, maxLimit, groupName) => {
    checkboxes.forEach(cb => {
      cb.addEventListener('change', () => {
        const checkedCount = Array.from(checkboxes).filter(c => c.checked).length;
        if (checkedCount > maxLimit) {
          cb.checked = false;
          alert(`You can select a maximum of ${maxLimit} ${groupName} for the wedding menu.`);
        }
        updateCalculatorEstimate();
      });
    });
  };

  setupCheckboxLimit(weddingMains, 3, 'mains');
  setupCheckboxLimit(weddingSides, 4, 'sides');
  setupCheckboxLimit(weddingDesserts, 2, 'desserts');

  // --- 3. Live Calculator Engine ---
  const getSelectedWeddingItems = () => {
    const mains = Array.from(weddingMains).filter(c => c.checked).map(c => c.getAttribute('data-name'));
    const sides = Array.from(weddingSides).filter(c => c.checked).map(c => c.getAttribute('data-name'));
    const desserts = Array.from(weddingDesserts).filter(c => c.checked).map(c => c.getAttribute('data-name'));
    return { mains, sides, desserts };
  };

  const getWeddingPremium = () => {
    let premium = 0;
    weddingMains.forEach(cb => {
      if (cb.checked && cb.hasAttribute('data-premium')) {
        premium += parseFloat(cb.getAttribute('data-premium'));
      }
    });
    return premium; // e.g. +$5 per head if Salmon is checked
  };

  const updateCalculatorEstimate = () => {
    const guests = parseInt(guestSlider.value);
    const selectedPkgKey = calcPackageSelect.value;
    const pricingObj = packagesPricing[selectedPkgKey];
    
    guestCountVal.textContent = guests;
    
    // Determine cost per head based on scaled ranges
    let costPerHead = pricingObj.max;
    if (guests <= 49) {
      costPerHead = pricingObj['49'];
    } else if (guests <= 99) {
      costPerHead = pricingObj['99'];
    } else if (guests <= 199) {
      costPerHead = pricingObj['199'];
    }
    
    let baseCost = costPerHead * guests;
    let premiumCost = 0;
    
    // Toggle Wedding Summary Box in Calculator
    if (selectedPkgKey === 'wedding') {
      weddingSummaryBox.classList.remove('hidden');
      breakdownPremiumRow.classList.remove('hidden');
      
      const menu = getSelectedWeddingItems();
      weddingMenuSummaryList.innerHTML = '';
      
      const allSelectedItems = [...menu.mains, ...menu.sides, ...menu.desserts];
      if (allSelectedItems.length === 0) {
        weddingMenuSummaryList.innerHTML = '<li>No items selected yet.</li>';
      } else {
        allSelectedItems.forEach(item => {
          const li = document.createElement('li');
          li.textContent = item;
          weddingMenuSummaryList.appendChild(li);
        });
      }
      
      const premiumPerHead = getWeddingPremium();
      if (premiumPerHead > 0) {
        premiumCost = premiumPerHead * guests;
        weddingPremiumNotice.textContent = `Includes premium ingredient surcharge: +$${premiumPerHead}.00 per head.`;
      } else {
        weddingPremiumNotice.textContent = '';
      }
    } else {
      weddingSummaryBox.classList.add('hidden');
      breakdownPremiumRow.classList.add('hidden');
    }
    
    // Calculate Addons
    let addonsTotal = 0;
    addonChecks.forEach(cb => {
      if (cb.checked) {
        if (cb.hasAttribute('data-price-head')) {
          addonsTotal += parseFloat(cb.getAttribute('data-price-head')) * guests;
        } else if (cb.hasAttribute('data-price-flat')) {
          addonsTotal += parseFloat(cb.getAttribute('data-price-flat'));
        }
      }
    });

    const totalEstimate = baseCost + premiumCost + addonsTotal;
    
    // Render Pricing Results
    scaledPriceHead.textContent = `$${(costPerHead + (selectedPkgKey === 'wedding' ? getWeddingPremium() : 0)).toFixed(2)} per guest`;
    breakdownBase.textContent = `$${baseCost.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    breakdownPremium.textContent = `$${premiumCost.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    breakdownAddons.textContent = `$${addonsTotal.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    breakdownTotal.textContent = `$${totalEstimate.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    
    // Proactively sync calculator variables with Form fields
    formGuests.value = guests;
    formPackage.value = selectedPkgKey;
    updateFormAddonsSummary();
  };

  // Listeners for calculator controls
  if (guestSlider) {
    guestSlider.addEventListener('input', updateCalculatorEstimate);
  }
  if (calcPackageSelect) {
    calcPackageSelect.addEventListener('change', updateCalculatorEstimate);
  }
  addonChecks.forEach(cb => {
    cb.addEventListener('change', updateCalculatorEstimate);
  });

  // --- 4. Wedding Custom Apply Button ---
  if (weddingApplyBtn) {
    weddingApplyBtn.addEventListener('click', (e) => {
      e.preventDefault();
      // Set calculator package selection to wedding
      calcPackageSelect.value = 'wedding';
      updateCalculatorEstimate();
      // Smooth scroll down to the calculator
      document.getElementById('calculator').scrollIntoView({ behavior: 'smooth' });
    });
  }

  // --- 5. Quick Select Package buttons ---
  selectPackageBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const pkg = btn.getAttribute('data-package');
      calcPackageSelect.value = pkg;
      updateCalculatorEstimate();
      document.getElementById('calculator').scrollIntoView({ behavior: 'smooth' });
    });
  });

  // --- 6. Form Sync & Addon Tag Rendering ---
  const updateFormAddonsSummary = () => {
    formAddonsContainer.innerHTML = '';
    const selectedAddons = [];
    
    addonChecks.forEach(cb => {
      if (cb.checked) {
        const label = cb.closest('.addon-checkbox-card').querySelector('.title').textContent.split('+')[0].trim();
        selectedAddons.push(label);
      }
    });

    if (selectedAddons.length === 0) {
      formAddonsContainer.innerHTML = '<span class="no-tags">None selected. Adjust in calculator above if required.</span>';
    } else {
      selectedAddons.forEach(addon => {
        const tag = document.createElement('span');
        tag.className = 'addon-tag';
        tag.textContent = addon;
        formAddonsContainer.appendChild(tag);
      });
    }
  };

  // Sync Form guest counts back to slider if typed in manually
  if (formGuests) {
    formGuests.addEventListener('change', () => {
      const val = parseInt(formGuests.value);
      if (val >= 20 && val <= 1000) {
        guestSlider.value = Math.min(val, 500); // Caps slider visual track at 500
        updateCalculatorEstimate();
      }
    });
  }

  // Sync Form Package select box back to calculator package select
  if (formPackage) {
    formPackage.addEventListener('change', () => {
      calcPackageSelect.value = formPackage.value;
      updateCalculatorEstimate();
    });
  }

  // --- 7. Custom Form Validation & Dialog Submission ---
  const showFieldError = (field, errorEl, message) => {
    const parent = field.closest('.form-group');
    parent.classList.add('invalid');
    errorEl.textContent = message;
  };

  const clearFieldError = (field, errorEl) => {
    const parent = field.closest('.form-group');
    parent.classList.remove('invalid');
    errorEl.textContent = '';
  };

  if (cateringForm) {
    cateringForm.addEventListener('submit', (e) => {
      e.preventDefault();
      
      let isValid = true;
      
      // Name validation
      if (!formName.value.trim()) {
        showFieldError(formName, document.getElementById('name-error'), 'Full name is required.');
        isValid = false;
      } else {
        clearFieldError(formName, document.getElementById('name-error'));
      }
      
      // Email validation
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!formEmail.value.trim()) {
        showFieldError(formEmail, document.getElementById('email-error'), 'Email address is required.');
        isValid = false;
      } else if (!emailRegex.test(formEmail.value.trim())) {
        showFieldError(formEmail, document.getElementById('email-error'), 'Please enter a valid email address.');
        isValid = false;
      } else {
        clearFieldError(formEmail, document.getElementById('email-error'));
      }
      
      // Phone validation
      if (!formPhone.value.trim()) {
        showFieldError(formPhone, document.getElementById('phone-error'), 'Phone number is required.');
        isValid = false;
      } else {
        clearFieldError(formPhone, document.getElementById('phone-error'));
      }
      
      // Date validation
      if (!formDate.value) {
        showFieldError(formDate, document.getElementById('date-error'), 'Event date is required.');
        isValid = false;
      } else {
        const selectedDate = new Date(formDate.value);
        const today = new Date();
        today.setHours(0,0,0,0);
        if (selectedDate < today) {
          showFieldError(formDate, document.getElementById('date-error'), 'Please select a future date.');
          isValid = false;
        } else {
          clearFieldError(formDate, document.getElementById('date-error'));
        }
      }
      
      // Venue validation
      if (!formVenue.value.trim()) {
        showFieldError(formVenue, document.getElementById('venue-error'), 'Venue location or suburb is required.');
        isValid = false;
      } else {
        clearFieldError(formVenue, document.getElementById('venue-error'));
      }
      
      // Guests count check
      const guestNum = parseInt(formGuests.value);
      if (isNaN(guestNum) || guestNum < 20) {
        showFieldError(formGuests, document.getElementById('guests-error'), 'Minimum guest count is 20.');
        isValid = false;
      } else {
        clearFieldError(formGuests, document.getElementById('guests-error'));
      }
      
      if (!isValid) {
        // Find first invalid input and focus it
        const firstInvalid = cateringForm.querySelector('.form-group.invalid input, .form-group.invalid select');
        if (firstInvalid) firstInvalid.focus();
        return;
      }
      
      // Form is valid - Prepare Dialog Modal Data
      const guests = parseInt(formGuests.value);
      const packageKey = formPackage.value;
      const totalAmountStr = breakdownTotal.textContent;
      
      // Generate random Quote reference number
      const randomRef = Math.floor(10000 + Math.random() * 90000);
      
      dialogQuoteRef.textContent = randomRef;
      dialogGuests.textContent = guests;
      dialogPackage.textContent = packagesPricing[packageKey].name;
      dialogTotal.textContent = totalAmountStr;
      dialogUserEmail.textContent = formEmail.value.trim();
      
      // Check for Wedding selections
      if (packageKey === 'wedding') {
        dialogWeddingMenuRow.classList.remove('hidden');
        const menu = getSelectedWeddingItems();
        const mainsStr = menu.mains.length > 0 ? `Mains: ${menu.mains.join(', ')}` : 'No mains selected';
        const sidesStr = menu.sides.length > 0 ? `Sides: ${menu.sides.join(', ')}` : 'No sides selected';
        const dessertsStr = menu.desserts.length > 0 ? `Desserts: ${menu.desserts.join(', ')}` : 'No desserts selected';
        dialogWeddingMenuDetails.innerHTML = `${mainsStr}<br>${sidesStr}<br>${dessertsStr}`;
      } else {
        dialogWeddingMenuRow.classList.add('hidden');
      }
      
      // Collect Add-ons
      const addons = [];
      addonChecks.forEach(cb => {
        if (cb.checked) {
          addons.push(cb.closest('.addon-checkbox-card').querySelector('.title').textContent.split('+')[0].trim());
        }
      });
      dialogAddonsDetails.textContent = addons.length > 0 ? addons.join(', ') : 'None selected';
      
      // Open native `<dialog>` modal
      if (quoteSuccessDialog) {
        quoteSuccessDialog.showModal();
      }
    });
  }

  // Dialog Close handler
  if (dialogCloseBtn && quoteSuccessDialog) {
    dialogCloseBtn.addEventListener('click', () => {
      quoteSuccessDialog.close();
      // Reset form and calculator
      if (cateringForm) {
        cateringForm.reset();
      }
      guestSlider.value = 80;
      calcPackageSelect.value = 'buffet';
      addonChecks.forEach(cb => cb.checked = false);
      weddingMains.forEach(cb => cb.checked = true); // Reset defaults
      weddingSides.forEach((cb, idx) => cb.checked = idx < 4);
      weddingDesserts.forEach((cb, idx) => cb.checked = idx < 2);
      
      // Reset maple salmon unchecked
      document.querySelector('input[value="salmon"]').checked = false;
      
      updateCalculatorEstimate();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // --- Initial Estimator Trigger ---
  updateCalculatorEstimate();
});
