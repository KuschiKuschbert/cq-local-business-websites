import './mobile-ux.js';
import './style.css';

document.addEventListener('DOMContentLoaded', () => {
  // Mobile Nav Drawer Toggle
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

  // Interactive Quote Scope Estimator
  const taskSelect = document.getElementById('calc-task-select');
  const sizeSlider = document.getElementById('calc-size-slider');
  const sizeDisplay = document.getElementById('calc-size-display');
  const terrainBtns = document.querySelectorAll('.terrain-btn');

  const scopeTask = document.getElementById('scope-task');
  const scopeSize = document.getElementById('scope-size');
  const scopeSoil = document.getElementById('scope-soil');
  
  const calcDuration = document.getElementById('calc-duration');
  const calcMachinery = document.getElementById('calc-machinery');
  const proceedBtn = document.getElementById('btn-estimator-proceed');

  // Booking Form Fields
  const bookingTask = document.getElementById('booking-task');
  const bookingSize = document.getElementById('booking-size');

  let activeTask = 'shed-pad';
  let activeSize = 100;
  let activeSoil = 'soil'; // soil, clay, rock

  const taskMetadata = {
    'shed-pad': {
      name: 'Shed Pad Prep',
      baseDaysPerSqm: 0.008,
      machinery: '5T Excavator + Bobcat',
      slug: 'shed-pad'
    },
    'driveway': {
      name: 'Gravel Driveway Laying',
      baseDaysPerSqm: 0.006,
      machinery: 'Bobcat + Smooth Drum Roller',
      slug: 'driveway'
    },
    'clearing': {
      name: 'Land Clearing & Stumps',
      baseDaysPerSqm: 0.012,
      machinery: '8T Heavy Excavator + Mulcher',
      slug: 'clearing'
    },
    'trenching': {
      name: 'Trench Excavation',
      baseDaysPerSqm: 0.004,
      machinery: '1.7T Micro Digger / Excavator',
      slug: 'trenching'
    }
  };

  const soilNames = {
    'soil': 'Flat / Dry Soil',
    'clay': 'Sticky Heavy Clay',
    'rock': 'Rocky / Sloped Terrain'
  };

  const soilMultipliers = {
    'soil': 1.0,
    'clay': 1.3,
    'rock': 1.8
  };

  function runEstimation() {
    const taskObj = taskMetadata[activeTask];
    const baseDays = taskObj.baseDaysPerSqm;
    const soilMult = soilMultipliers[activeSoil];

    // Calculate raw duration
    let rawDuration = activeSize * baseDays * soilMult;

    // Boundary limits (no job is less than a half day)
    if (rawDuration < 0.5) rawDuration = 0.5;

    // Round to nearest half day (0.5)
    const finalDuration = Math.round(rawDuration * 2) / 2;

    // Update estimator displays
    if (scopeTask) scopeTask.textContent = taskObj.name;
    if (scopeSize) scopeSize.textContent = `${activeSize} sqm`;
    if (scopeSoil) scopeSoil.textContent = soilNames[activeSoil];

    if (calcDuration) {
      calcDuration.textContent = `${finalDuration} Day${finalDuration !== 1 ? 's' : ''}`;
    }
    if (calcMachinery) {
      calcMachinery.textContent = taskObj.machinery;
    }
  }

  // Estimator Action Listeners
  if (taskSelect) {
    taskSelect.addEventListener('change', (e) => {
      activeTask = e.target.value;
      runEstimation();
    });
  }

  if (sizeSlider) {
    sizeSlider.addEventListener('input', (e) => {
      activeSize = parseInt(e.target.value, 10);
      if (sizeDisplay) {
        sizeDisplay.textContent = `${activeSize} sqm`;
      }
      runEstimation();
    });
  }

  terrainBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      terrainBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      activeSoil = btn.dataset.soilVal;
      runEstimation();
    });
  });

  // Sync details to booking form
  if (proceedBtn) {
    proceedBtn.addEventListener('click', () => {
      if (bookingTask) {
        bookingTask.value = activeTask;
      }
      if (bookingSize) {
        // Map size to select option bounds
        if (activeSize <= 70) {
          bookingSize.value = '50';
        } else if (activeSize > 70 && activeSize <= 300) {
          bookingSize.value = '150';
        } else if (activeSize > 300 && activeSize <= 750) {
          bookingSize.value = '500';
        } else {
          bookingSize.value = '1000';
        }
      }

      // Scroll to booking form
      const bookingSection = document.getElementById('booking');
      if (bookingSection) {
        bookingSection.scrollIntoView({ behavior: 'smooth' });
      }
    });
  }

  // Form submit & overlay trigger
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

  // Initial calculation run
  runEstimation();
});
