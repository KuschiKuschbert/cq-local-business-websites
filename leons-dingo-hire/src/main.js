import './style.css';

document.addEventListener('DOMContentLoaded', () => {
  // Mobile Nav Drawer
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

  // Rate Calculator Configurator
  const daysSlider = document.getElementById('days-slider');
  const daysValDisplay = document.getElementById('days-val-display');
  
  const machineBtns = document.querySelectorAll('[data-machine-val]');
  const modeBtns = document.querySelectorAll('[data-mode-val]');
  const modeHelperText = document.getElementById('mode-helper');
  const attachmentChecks = document.querySelectorAll('.attach-check');
  
  const configMachine = document.getElementById('config-machine');
  const configMode = document.getElementById('config-mode');
  const configDays = document.getElementById('config-days');
  const configAttachments = document.getElementById('config-attachments');
  
  const totalRateDisplay = document.getElementById('calc-total-rate');
  const proceedBtn = document.getElementById('btn-calc-proceed');

  // Booking inputs to sync
  const bookingMachineSelect = document.getElementById('booking-machine-select');
  const bookingModeSelect = document.getElementById('booking-mode-select');
  const bookingDurationInput = document.getElementById('booking-duration');

  let activeMachine = 'k9-4'; // k9-4 or k9-3
  let activeMode = 'dry'; // dry or wet
  let activeDays = 1; // 1 to 7
  let selectedAttachments = [];

  const baseRates = {
    'k9-4': 195, // dry day rate
    'k9-3': 180
  };

  const machineNames = {
    'k9-4': 'Dingo K9-4 Narrow-Track',
    'k9-3': 'Dingo K9-3 Wheeled'
  };

  const modeNames = {
    dry: 'Dry Hire (DIY operator)',
    wet: 'Wet Hire (Includes Professional Operator)'
  };

  const modeDescriptions = {
    dry: 'Dry hire: Pick up or delivered. You drive.',
    wet: 'Wet hire: Machine comes with a ticketed operator. Surcharge of +$550/day.'
  };

  function updateRate() {
    const dailyBase = baseRates[activeMachine];
    
    // Multi-day discount factor
    let discountFactor = 1.0;
    if (activeDays === 2) discountFactor = 0.95;
    else if (activeDays === 3) discountFactor = 0.90;
    else if (activeDays >= 4 && activeDays <= 6) discountFactor = 0.85;
    else if (activeDays >= 7) discountFactor = 0.80; // 20% off weekly rate

    let machineCostPerDay = dailyBase * discountFactor;
    
    // Wet hire surcharge (adds operator flat rate per day)
    let operatorSurcharge = 0;
    if (activeMode === 'wet') {
      operatorSurcharge = 550; // flat $550 operator cost per day
    }

    // Attachment cost calculation
    let attachmentCostPerDay = 0;
    selectedAttachments.forEach(item => {
      attachmentCostPerDay += item.rate;
    });

    const totalCalculated = Math.round((machineCostPerDay + operatorSurcharge + attachmentCostPerDay) * activeDays);

    // Update displays
    if (totalRateDisplay) {
      animateCounter(totalRateDisplay, totalCalculated);
    }

    // Update config panel text
    if (configMachine) configMachine.textContent = machineNames[activeMachine];
    if (configMode) configMode.textContent = modeNames[activeMode];
    if (configDays) configDays.textContent = `${activeDays} Day${activeDays > 1 ? 's' : ''} Hire`;
    
    if (configAttachments) {
      if (selectedAttachments.length === 0) {
        configAttachments.textContent = '4-in-1 Bucket only';
      } else {
        const names = selectedAttachments.map(item => item.name.charAt(0).toUpperCase() + item.name.slice(1));
        configAttachments.textContent = `4-in-1 Bucket + ${names.join(', ')}`;
      }
    }
  }

  function animateCounter(element, targetValue) {
    const start = parseInt(element.textContent, 10) || 0;
    const duration = 300;
    const startTime = performance.now();

    function update(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
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

  // Event Listeners for Configurator
  if (daysSlider) {
    daysSlider.addEventListener('input', (e) => {
      activeDays = parseInt(e.target.value, 10);
      if (daysValDisplay) daysValDisplay.textContent = `${activeDays} Day${activeDays > 1 ? 's' : ''}`;
      updateRate();
    });
  }

  machineBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      machineBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeMachine = btn.dataset.machineVal;
      updateRate();
    });
  });

  modeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      modeBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeMode = btn.dataset.modeVal;
      
      if (modeHelperText) {
        modeHelperText.textContent = modeDescriptions[activeMode];
      }
      
      updateRate();
    });
  });

  attachmentChecks.forEach(check => {
    check.addEventListener('change', () => {
      selectedAttachments = [];
      attachmentChecks.forEach(c => {
        if (c.checked) {
          selectedAttachments.push({
            name: c.value,
            rate: parseInt(c.dataset.rate, 10)
          });
        }
      });
      updateRate();
    });
  });

  // Select Machine CTAs in fleet catalog
  const hireSelectBtns = document.querySelectorAll('.hire-select-btn');
  hireSelectBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const selectedMachine = btn.dataset.machine;
      
      if (selectedMachine.includes('Narrow-Track')) activeMachine = 'k9-4';
      if (selectedMachine.includes('Wheeled')) activeMachine = 'k9-3';

      // Sync active button in calculator
      machineBtns.forEach(b => {
        if (b.dataset.machineVal === activeMachine) {
          b.classList.add('active');
        } else {
          b.classList.remove('active');
        }
      });

      updateRate();

      // Scroll to calculator
      const calcSection = document.getElementById('hire-calculator');
      if (calcSection) {
        calcSection.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // Proceed from Rate Calculator to Booking
  if (proceedBtn) {
    proceedBtn.addEventListener('click', () => {
      if (bookingMachineSelect) {
        bookingMachineSelect.value = activeMachine === 'k9-4' ? 'K9-4 Narrow-Track' : 'K9-3 Wheeled';
      }
      if (bookingModeSelect) {
        bookingModeSelect.value = activeMode;
      }
      if (bookingDurationInput) {
        bookingDurationInput.value = activeDays;
      }

      // Scroll to booking form
      const bookingSection = document.getElementById('booking');
      if (bookingSection) {
        bookingSection.scrollIntoView({ behavior: 'smooth' });
      }
    });
  }

  // Booking Form Submission
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

  // Run initial calculator run
  updateRate();
});
