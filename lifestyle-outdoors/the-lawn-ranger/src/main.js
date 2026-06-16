import './mobile-ux.js';
import './style.css';

document.addEventListener('DOMContentLoaded', () => {
  // Mobile Navigation Drawer Toggle
  const menuToggle = document.getElementById('mobile-menu-toggle');
  const mobileDrawer = document.getElementById('mobile-drawer');

  if (menuToggle && mobileDrawer) {
    menuToggle.addEventListener('click', () => {
      const expanded = menuToggle.getAttribute('aria-expanded') === 'true';
      menuToggle.setAttribute('aria-expanded', !expanded);
      mobileDrawer.setAttribute('aria-hidden', expanded);
      menuToggle.classList.toggle('active');
    });

    // Close mobile menu when a link is clicked
    const mobileLinks = mobileDrawer.querySelectorAll('a');
    mobileLinks.forEach(link => {
      link.addEventListener('click', () => {
        menuToggle.setAttribute('aria-expanded', 'false');
        mobileDrawer.setAttribute('aria-hidden', 'true');
        menuToggle.classList.remove('active');
      });
    });
  }

  // Quote Calculator Logic
  const sizeSlider = document.getElementById('size-slider');
  const sizeDisplay = document.getElementById('size-val-display');
  
  const planToggles = document.querySelectorAll('.plan-toggle');
  const freqCards = document.querySelectorAll('.freq-card');
  
  const summaryPlan = document.getElementById('summary-plan');
  const summarySize = document.getElementById('summary-size');
  const summaryFreq = document.getElementById('summary-frequency');
  
  const finalPrice = document.getElementById('calc-final-price');
  const finalPeriod = document.getElementById('calc-period');
  
  const proceedBtn = document.getElementById('btn-quote-proceed');
  const bookingPackageSelect = document.getElementById('booking-package');
  const bookingSizeSelect = document.getElementById('booking-size');

  let currentPlan = 'pro'; // basic, pro, elite
  let currentSize = 250; // sqm
  let currentFreq = 'fortnightly'; // weekly, fortnightly, monthly

  const planBasePrices = {
    basic: 49,
    pro: 79,
    elite: 149
  };

  const planNames = {
    basic: 'Ranger Basic',
    pro: 'Ranger Pro',
    elite: 'Ranger Elite'
  };

  function calculatePrice() {
    const base = planBasePrices[currentPlan];
    
    // Size multiplier: 250sqm is base line. 
    // +0.15% per sqm away from 250.
    const sizeDiff = currentSize - 250;
    const sizeMultiplier = 1 + (sizeDiff * 0.0012);
    
    // Freq multiplier
    let freqMultiplier = 1.0;
    let periodText = '/ fortnightly visit';
    
    if (currentFreq === 'weekly') {
      freqMultiplier = 0.9; // 10% discount
      periodText = '/ weekly visit';
    } else if (currentFreq === 'fortnightly') {
      freqMultiplier = 1.0;
      periodText = '/ fortnightly visit';
    } else if (currentFreq === 'monthly') {
      freqMultiplier = 1.15; // 15% surcharge for overgrown lawns
      periodText = '/ monthly visit';
    }

    const calculated = Math.round(base * sizeMultiplier * freqMultiplier);
    // Keep minimum bounds
    const finalVal = Math.max(calculated, Math.round(base * 0.5));

    // Update Displays
    if (finalPrice) {
      animateCounter(finalPrice, finalVal);
    }
    if (finalPeriod) {
      finalPeriod.textContent = periodText;
    }
    
    // Update summary text
    if (summaryPlan) summaryPlan.textContent = planNames[currentPlan];
    if (summarySize) summarySize.textContent = `${currentSize} sqm`;
    if (summaryFreq) summaryFreq.textContent = currentFreq.charAt(0).toUpperCase() + currentFreq.slice(1);
  }

  function animateCounter(element, targetValue) {
    const start = parseInt(element.textContent, 10) || 0;
    const duration = 400; // ms
    const startTime = performance.now();

    function update(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      // Ease out quad
      const ease = progress * (2 - progress);
      const currentVal = Math.round(start + (targetValue - start) * ease);
      
      element.textContent = currentVal;

      if (progress < 1) {
        requestAnimationFrame(update);
      } else {
        element.textContent = targetValue;
      }
    }

    requestAnimationFrame(update);
  }

  // Event Listeners for Calculator
  if (sizeSlider) {
    sizeSlider.addEventListener('input', (e) => {
      currentSize = parseInt(e.target.value, 10);
      if (sizeDisplay) sizeDisplay.textContent = `${currentSize} sqm`;
      calculatePrice();
    });
  }

  planToggles.forEach(toggle => {
    toggle.addEventListener('click', () => {
      planToggles.forEach(btn => btn.classList.remove('active'));
      toggle.classList.add('active');
      currentPlan = toggle.dataset.pkgVal;
      calculatePrice();
    });
  });

  freqCards.forEach(card => {
    card.addEventListener('click', () => {
      freqCards.forEach(c => c.classList.remove('active'));
      card.classList.add('active');
      currentFreq = card.dataset.freq;
      calculatePrice();
    });
  });

  // Package Card CTA selector buttons
  const selectPkgBtns = document.querySelectorAll('.select-pkg-btn');
  selectPkgBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const selectedPkg = btn.dataset.package;
      
      // Update package selectors
      if (selectedPkg === 'Ranger Basic') currentPlan = 'basic';
      if (selectedPkg === 'Ranger Pro') currentPlan = 'pro';
      if (selectedPkg === 'Ranger Elite') currentPlan = 'elite';

      // Sync toggles in calculator
      planToggles.forEach(toggle => {
        if (toggle.dataset.pkgVal === currentPlan) {
          toggle.classList.add('active');
        } else {
          toggle.classList.remove('active');
        }
      });

      calculatePrice();

      // Scroll to calculator
      const calcSection = document.getElementById('quote-calculator');
      if (calcSection) {
        calcSection.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // Proceed from quote to booking
  if (proceedBtn) {
    proceedBtn.addEventListener('click', () => {
      // Sync package
      if (bookingPackageSelect) {
        if (currentPlan === 'basic') bookingPackageSelect.value = 'Ranger Basic';
        if (currentPlan === 'pro') bookingPackageSelect.value = 'Ranger Pro';
        if (currentPlan === 'elite') bookingPackageSelect.value = 'Ranger Elite';
      }
      
      // Sync size select
      if (bookingSizeSelect) {
        if (currentSize <= 150) {
          bookingSizeSelect.value = '100';
        } else if (currentSize <= 350) {
          bookingSizeSelect.value = '250';
        } else if (currentSize <= 750) {
          bookingSizeSelect.value = '500';
        } else {
          bookingSizeSelect.value = '1000';
        }
      }

      // Scroll to booking form
      const bookingSection = document.getElementById('booking');
      if (bookingSection) {
        bookingSection.scrollIntoView({ behavior: 'smooth' });
      }
    });
  }

  // Booking Form Submission & Success Modal
  const bookingForm = document.getElementById('booking-form');
  const successOverlay = document.getElementById('form-success');
  const successCloseBtn = document.getElementById('btn-success-close');

  if (bookingForm && successOverlay) {
    bookingForm.addEventListener('submit', (e) => {
      e.preventDefault();
      
      // Perform local animation show
      successOverlay.setAttribute('aria-hidden', 'false');
      
      // Reset Form
      bookingForm.reset();
    });
  }

  if (successCloseBtn && successOverlay) {
    successCloseBtn.addEventListener('click', () => {
      successOverlay.setAttribute('aria-hidden', 'true');
    });
  }

  // Initial Calculation
  calculatePrice();
});
