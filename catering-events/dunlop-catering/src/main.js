import './mobile-ux.js';
import './style.css';

document.addEventListener('DOMContentLoaded', () => {
  // --- DOM Selectors ---

  // Mobile navigation
  const navToggleBtn = document.getElementById('nav-toggle-btn');
  const mainNav = document.getElementById('main-nav');

  // Package select button bindings
  const selectPackageBtns = document.querySelectorAll('.select-package-btn');

  // Custom Wedding Menu Checklist
  const weddingMains = document.getElementsByName('wedding-mains');
  const weddingSides = document.getElementsByName('wedding-sides');
  const weddingDesserts = document.getElementsByName('wedding-desserts');
  const weddingApplyBtn = document.getElementById('wedding-apply-btn');

  // Interactive Live Estimator
  const guestSlider = document.getElementById('guest-slider');
  const guestCountVal = document.getElementById('guest-count-val');
  const calcPackageSelect = document.getElementById('calc-package');
  const addonChecks = document.getElementsByName('addons');

  // Calculator Breakdown Displays
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

  // Inquiry Form Fields
  const cateringForm = document.getElementById('catering-quote-form');
  const formName = document.getElementById('form-name');
  const formEmail = document.getElementById('form-email');
  const formPhone = document.getElementById('form-phone');
  const formDate = document.getElementById('form-date');
  const formVenue = document.getElementById('form-venue');
  const formPackage = document.getElementById('form-package');
  const formAddonsContainer = document.getElementById('form-addons-tags-container');
  const formAddonsTagsList = document.getElementById('form-addons-tags-list');
  const ackPricingCheck = document.getElementById('ack-pricing');

  // Modal Dialog Info
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

  // --- Pricing Setup ---
  // Tiered Pricing based on Guest count size. Larger crowds get bulk discounts.
  const packageTierPrices = {
    classic: { name: 'The Classic Spit Roast', 49: 45, 99: 38, 199: 32, max: 28 },
    buffet: { name: 'The Grand Feast Buffet', 49: 55, 99: 48, 199: 42, max: 38 },
    grazing: { name: 'Rustic Grazing & Roast', 49: 65, 99: 58, 199: 52, max: 48 },
    wedding: { name: 'Bespoke Wedding Menu', 49: 75, 99: 68, 199: 62, max: 58 }
  };

  // State to hold custom wedding menu items
  let activeWeddingMenu = {
    mains: [],
    sides: [],
    desserts: [],
    premiumExtra: 0
  };

  // --- 1. Mobile Menu Action ---
  if (navToggleBtn && mainNav) {
    navToggleBtn.addEventListener('click', () => {
      mainNav.classList.toggle('open');
      navToggleBtn.classList.toggle('open');
    });

    mainNav.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        mainNav.classList.remove('open');
        navToggleBtn.classList.remove('open');
      });
    });
  }

  // --- 2. Checkbox Limit Logic ---
  const applyLimitConstraint = (elements, maxLimit, category) => {
    elements.forEach(el => {
      el.addEventListener('change', () => {
        const checkedCount = Array.from(elements).filter(cb => cb.checked).length;
        if (checkedCount > maxLimit) {
          el.checked = false;
          alert(`You can select a maximum of ${maxLimit} ${category} options.`);
        }
      });
    });
  };

  applyLimitConstraint(weddingMains, 3, 'Mains');
  applyLimitConstraint(weddingSides, 4, 'Sides');
  applyLimitConstraint(weddingDesserts, 2, 'Dessert');

  // --- 3. Compile and apply custom wedding selections ---
  if (weddingApplyBtn) {
    weddingApplyBtn.addEventListener('click', (e) => {
      e.preventDefault();

      const selectedMains = Array.from(weddingMains).filter(cb => cb.checked);
      const selectedSides = Array.from(weddingSides).filter(cb => cb.checked);
      const selectedDesserts = Array.from(weddingDesserts).filter(cb => cb.checked);

      if (selectedMains.length === 0 || selectedSides.length === 0) {
        alert('Please select at least 1 Main and 1 Side dish to design your wedding menu.');
        return;
      }

      // Calculate any premium additions (e.g. Salmon)
      let premiumCost = 0;
      selectedMains.forEach(cb => {
        const premiumVal = parseFloat(cb.getAttribute('data-premium') || 0);
        premiumCost += premiumVal;
      });

      activeWeddingMenu = {
        mains: selectedMains.map(cb => cb.getAttribute('data-name')),
        sides: selectedSides.map(cb => cb.getAttribute('data-name')),
        desserts: selectedDesserts.map(cb => cb.getAttribute('data-name')),
        premiumExtra: premiumCost
      };

      // Set package to wedding and trigger calculation update
      if (calcPackageSelect) {
        calcPackageSelect.value = 'wedding';
        // Dispatch event to update view
        calcPackageSelect.dispatchEvent(new Event('change'));
      }

      // Smooth scroll to calculator
      const calcSection = document.getElementById('calculator');
      if (calcSection) {
        calcSection.scrollIntoView({ behavior: 'smooth' });
      }
    });
  }

  // --- 4. Package Quick selection buttons ---
  selectPackageBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      const pkg = btn.getAttribute('data-package');
      if (calcPackageSelect) {
        calcPackageSelect.value = pkg;
        calcPackageSelect.dispatchEvent(new Event('change'));
      }
    });
  });

  // --- 5. Calculation Logic ---
  const calculateTierHeadPrice = (pkgKey, count) => {
    const rates = packageTierPrices[pkgKey];
    if (!rates) return 0;

    if (count <= 49) return rates[49];
    if (count <= 99) return rates[99];
    if (count <= 199) return rates[199];
    return rates.max;
  };

  const updateCalculatorEstimate = () => {
    if (!guestSlider || !calcPackageSelect) return;

    const count = parseInt(guestSlider.value);
    const pkgKey = calcPackageSelect.value;
    
    // Update Slider Count Indicator
    if (guestCountVal) guestCountVal.textContent = count;

    // Calculate Head Cost
    let baseHeadCost = calculateTierHeadPrice(pkgKey, count);
    let totalHeadCost = baseHeadCost;

    // Add Wedding selections details
    if (pkgKey === 'wedding') {
      if (weddingSummaryBox) weddingSummaryBox.classList.remove('hidden');
      
      // Render selection layout preview
      if (weddingMenuSummaryList) {
        weddingMenuSummaryList.innerHTML = '';
        const allSelections = [
          ...activeWeddingMenu.mains,
          ...activeWeddingMenu.sides,
          ...activeWeddingMenu.desserts
        ];

        if (allSelections.length === 0) {
          weddingMenuSummaryList.innerHTML = '<li>No dishes selected yet. Use the wedding designer above to choose dishes.</li>';
        } else {
          allSelections.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            weddingMenuSummaryList.appendChild(li);
          });
        }
      }

      // Apply premium extras
      if (activeWeddingMenu.premiumExtra > 0) {
        totalHeadCost += activeWeddingMenu.premiumExtra;
        if (weddingPremiumNotice) {
          weddingPremiumNotice.textContent = `*Includes +$${activeWeddingMenu.premiumExtra.toFixed(2)}/head premium selection surcharge.`;
        }
      } else if (weddingPremiumNotice) {
        weddingPremiumNotice.textContent = '';
      }

      if (breakdownPremiumRow) breakdownPremiumRow.style.display = 'flex';
      if (breakdownPremium) {
        breakdownPremium.textContent = `$${(activeWeddingMenu.premiumExtra * count).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
      }
    } else {
      if (weddingSummaryBox) weddingSummaryBox.classList.add('hidden');
      if (breakdownPremiumRow) breakdownPremiumRow.style.display = 'none';
    }

    // Calculations
    const baseTotalCost = baseHeadCost * count;
    
    // Calculate Add-ons
    let addonsTotalCost = 0;
    const activeAddonNames = [];
    addonChecks.forEach(cb => {
      if (cb.checked) {
        const headCost = parseFloat(cb.getAttribute('data-price-head') || 0);
        const flatCost = parseFloat(cb.getAttribute('data-price-flat') || 0);
        addonsTotalCost += (headCost * count) + flatCost;

        const label = cb.closest('.addon-tile').querySelector('.tile-txt').childNodes[0].textContent.trim();
        activeAddonNames.push(label);
      }
    });

    const finalGrandEstimate = (totalHeadCost * count) + addonsTotalCost;

    // Render displays
    if (scaledPriceHead) {
      scaledPriceHead.innerHTML = `$${totalHeadCost.toFixed(2)} <small>/ guest</small>`;
    }
    if (breakdownBase) {
      breakdownBase.textContent = `$${baseTotalCost.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    }
    if (breakdownAddons) {
      breakdownAddons.textContent = `$${addonsTotalCost.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    }
    if (breakdownTotal) {
      breakdownTotal.textContent = `$${finalGrandEstimate.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    }

    // Live update inquiry form matching state
    if (formPackage) formPackage.value = pkgKey;
    
    // Update addon tags visual feedback in form
    if (formAddonsContainer && formAddonsTagsList) {
      if (activeAddonNames.length > 0) {
        formAddonsContainer.style.display = 'block';
        formAddonsTagsList.innerHTML = '';
        activeAddonNames.forEach(name => {
          const tag = document.createElement('span');
          tag.className = 'tag-badge';
          tag.textContent = name;
          formAddonsTagsList.appendChild(tag);
        });
      } else {
        formAddonsContainer.style.display = 'none';
      }
    }
  };

  // Event Listeners for controls
  if (guestSlider) guestSlider.addEventListener('input', updateCalculatorEstimate);
  if (calcPackageSelect) calcPackageSelect.addEventListener('change', updateCalculatorEstimate);
  addonChecks.forEach(cb => cb.addEventListener('change', updateCalculatorEstimate));

  // Initialize
  updateCalculatorEstimate();

  // Load quote metrics directly into inquiry form fields
  if (calcApplyToFormBtn) {
    calcApplyToFormBtn.addEventListener('click', (e) => {
      e.preventDefault();
      
      const count = guestSlider.value;
      const pkg = calcPackageSelect.value;
      
      const targetFormGuests = document.getElementById('form-guests'); // fallbacks if custom markup fields are updated
      
      // Update form fields
      if (formPackage) formPackage.value = pkg;
      
      const notesArea = document.getElementById('form-notes');
      if (notesArea) {
        let text = `Estimated headcount: ${count} guests. `;
        if (pkg === 'wedding' && (activeWeddingMenu.mains.length > 0)) {
          text += `Custom Wedding Menu Selections:\n`;
          text += `- Mains: ${activeWeddingMenu.mains.join(', ')}\n`;
          text += `- Sides: ${activeWeddingMenu.sides.join(', ')}\n`;
          text += `- Desserts: ${activeWeddingMenu.desserts.join(', ')}\n`;
        }
        notesArea.value = text;
      }

      // Smooth scroll to inquiry form
      const quoteSection = document.getElementById('quote');
      if (quoteSection) {
        quoteSection.scrollIntoView({ behavior: 'smooth' });
      }
    });
  }

  // --- 6. Form Submission Dialog modal handler ---
  if (cateringForm) {
    cateringForm.addEventListener('submit', (e) => {
      e.preventDefault();

      // Simple validation check
      if (!formName.value || !formEmail.value || !formPhone.value || !formDate.value || !formVenue.value) {
        alert('Please fill out all required fields marked with an asterisk (*).');
        return;
      }

      if (!ackPricingCheck || !ackPricingCheck.checked) {
        alert('Please check and accept the 24-hour response guarantee checkbox.');
        return;
      }

      const count = guestSlider.value;
      const pkgKey = calcPackageSelect.value;
      const rates = packageTierPrices[pkgKey];

      // Populate dialog displays
      if (dialogGuests) dialogGuests.textContent = count;
      if (dialogPackage) dialogPackage.textContent = rates ? rates.name : pkgKey;
      if (dialogUserEmail) dialogUserEmail.textContent = formEmail.value;
      
      // Addons dialog tags
      if (dialogAddonsDetails) {
        const activeAddonNames = [];
        addonChecks.forEach(cb => {
          if (cb.checked) {
            const label = cb.closest('.addon-tile').querySelector('.tile-txt').childNodes[0].textContent.trim();
            activeAddonNames.push(label);
          }
        });
        dialogAddonsDetails.textContent = activeAddonNames.length > 0 ? activeAddonNames.join(', ') : 'None';
      }

      // Wedding selections inside dialog
      if (dialogWeddingMenuRow && dialogWeddingMenuDetails) {
        if (pkgKey === 'wedding') {
          dialogWeddingMenuRow.classList.remove('hidden');
          const allItems = [...activeWeddingMenu.mains, ...activeWeddingMenu.sides, ...activeWeddingMenu.desserts];
          dialogWeddingMenuDetails.textContent = allItems.join(', ');
        } else {
          dialogWeddingMenuRow.classList.add('hidden');
        }
      }

      // Total estimate dialog display
      if (dialogTotal && breakdownTotal) {
        dialogTotal.textContent = breakdownTotal.textContent;
      }

      // Generate random quote reference code
      if (dialogQuoteRef) {
        dialogQuoteRef.textContent = `DNP-${Math.floor(1000 + Math.random() * 9000)}`;
      }

      // Open Modal
      if (quoteSuccessDialog) {
        quoteSuccessDialog.showModal();
      }
    });
  }

  // Close success dialog modal
  if (dialogCloseBtn && quoteSuccessDialog) {
    dialogCloseBtn.addEventListener('click', () => {
      quoteSuccessDialog.close();
      if (cateringForm) cateringForm.reset();
      // Reset checklist state
      activeWeddingMenu = { mains: [], sides: [], desserts: [], premiumExtra: 0 };
      updateCalculatorEstimate();
    });
  }
});
