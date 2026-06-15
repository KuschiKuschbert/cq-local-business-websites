document.addEventListener('DOMContentLoaded', () => {

  // ==========================================
  // STATE MANAGEMENT
  // ==========================================
  let currentNiche = 'plumbing';
  let deviceView = 'tablet';
  
  const pricingTiers = {
    plumbing: 249,
    cafe: 199,
    landscaping: 299,
    pest: 249
  };

  const ticketDefaults = {
    plumbing: { val: 220, max: 1000, step: 10, unit: 'residential service calls' },
    cafe: { val: 35, max: 150, step: 5, unit: 'pre-orders or bookings' },
    landscaping: { val: 450, max: 1500, step: 25, unit: 'excavations or yard cuts' },
    pest: { val: 180, max: 800, step: 10, unit: 'standard pest sprays' }
  };

  // ==========================================
  // SELECTORS
  // ==========================================
  const nicheCards = document.querySelectorAll('.niche-card');
  const ticketSlider = document.getElementById('ticket-slider');
  const ticketValDisplay = document.getElementById('ticket-val-display');
  const pricingAmount = document.getElementById('pricing-amount');
  const roiJobsNeeded = document.getElementById('roi-jobs-needed');
  const roiUnitName = document.getElementById('roi-unit-name');
  
  const checkOnTime = document.getElementById('check-ontime');
  const checkCleanup = document.getElementById('check-cleanup');
  const checkPolice = document.getElementById('check-police');
  const checkWaitlist = document.getElementById('check-waitlist');
  
  const toggleRowOnTime = document.getElementById('toggle-opt-ontime');
  const toggleRowCleanup = document.getElementById('toggle-opt-cleanup');
  const toggleRowPolice = document.getElementById('toggle-opt-police');
  const toggleRowWaitlist = document.getElementById('toggle-opt-waitlist');
  
  const simWebContent = document.getElementById('sim-web-content');
  const simFrame = document.getElementById('sim-frame');
  const deviceTabletBtn = document.getElementById('device-tablet');
  const deviceMobileBtn = document.getElementById('device-mobile');

  // ==========================================
  // DYNAMIC SIMULATOR WEBSITES GENERATION
  // ==========================================
  
  function renderSimulatedWebsite() {
    if (!simWebContent) return;
    
    const showOnTime = checkOnTime.checked && !toggleRowOnTime.classList.contains('hidden');
    const showCleanup = checkCleanup.checked && !toggleRowCleanup.classList.contains('hidden');
    const showPolice = checkPolice.checked && !toggleRowPolice.classList.contains('hidden');
    const showWaitlist = checkWaitlist.checked && !toggleRowWaitlist.classList.contains('hidden');

    let htmlContent = '';

    if (currentNiche === 'plumbing') {
      htmlContent = `
        <header class="sim-header">
          <div class="sim-logo">💧 Keppel Bay Plumbing</div>
          <span class="sim-phone">📞 0400 999 999</span>
        </header>
        
        <div class="sim-hero">
          <span class="sim-hero-badge">On-Time & Professional</span>
          <h2>Central Queensland's High-Quality Plumbers</h2>
          <p>Prompt plumbing, gas fitting, and emergency drainage camera repairs across Yeppoon and Rockhampton.</p>
          <a href="#" class="sim-hero-cta">Request Fast Diagnostics</a>
        </div>
        
        <div class="sim-badge-row">
          ${showOnTime ? `
            <div class="sim-badge-card">
              <span class="sim-badge-icon">⏱️</span>
              <div class="sim-badge-content">
                <h4>On-Time Payout Guarantee</h4>
                <p>If we arrive late for our scheduled window, we pay you $50 on the spot.</p>
              </div>
            </div>
          ` : ''}
          
          ${showCleanup ? `
            <div class="sim-badge-card">
              <span class="sim-badge-icon">✨</span>
              <div class="sim-badge-content">
                <h4>Pristine Worksite Promise</h4>
                <p>We wear boot covers and clean every pipe shaving. No dirty footprints left behind.</p>
              </div>
            </div>
          ` : ''}
        </div>
        
        <div class="sim-form-container">
          <div class="sim-form-title">Request a $99 Callout Quote</div>
          <form class="sim-form-box" onsubmit="return false;">
            <input type="text" placeholder="Your Name" class="sim-input" required>
            <input type="text" placeholder="Service Needed" class="sim-input" required>
            
            ${showWaitlist ? `
              <div class="sim-estimator-widget">
                <h4>⚡ Live Dispatch Status</h4>
                <div class="sim-slider-row">
                  <span>Current Queue Wait:</span>
                  <span class="sim-est-val">Fast (90 mins)</span>
                </div>
              </div>
            ` : ''}
            
            <button class="sim-btn">Submit Service Request</button>
          </form>
        </div>
      `;
    } else if (currentNiche === 'cafe') {
      htmlContent = `
        <header class="sim-header">
          <div class="sim-logo">☕ Coffee & Co. Cafe</div>
          <span class="sim-phone">📍 Anzac Pde, Yeppoon</span>
        </header>
        
        <div class="sim-hero" style="background: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)), radial-gradient(circle, var(--color-gold) 0%, transparent 80%);">
          <span class="sim-hero-badge" style="background-color: #d39e82; color: #fff;">Yeppoon Beach Front</span>
          <h2>Craft Coffee & Fresh Coastal Bites</h2>
          <p>Locally roasted specialty beans, fresh pastries, and custom gluten-free menus.</p>
          <a href="#" class="sim-hero-cta" style="background-color: #b87a5d;">See Daily Specials</a>
        </div>
        
        <div class="sim-badge-row" style="background-color: #faf6f0;">
          ${showCleanup ? `
            <div class="sim-badge-card">
              <span class="sim-badge-icon">🥛</span>
              <div class="sim-badge-content">
                <h4>Allergy-Safe Double Check</h4>
                <p>We use dedicated separate blenders and group spaces for dairy-free and gluten-free preparation.</p>
              </div>
            </div>
          ` : ''}
        </div>
        
        <div class="sim-form-container">
          <div class="sim-form-title" style="color: #b87a5d;">Order Coffee Ahead</div>
          <form class="sim-form-box" onsubmit="return false;">
            <input type="text" placeholder="Pick up Name" class="sim-input" required>
            <select class="sim-input">
              <option>Flat White (Regular)</option>
              <option>Latte (Oat Milk)</option>
              <option>Cold Brew with Sweet Foam</option>
            </select>
            
            ${showWaitlist ? `
              <div class="sim-estimator-widget" style="background-color: #fcf8f2;">
                <h4>⏳ Queue skip pre-order</h4>
                <div class="sim-slider-row">
                  <span>Estimated Pickup In:</span>
                  <span class="sim-est-val" style="color: #b87a5d;">10 minutes</span>
                </div>
              </div>
            ` : ''}
            
            <button class="sim-btn" style="background-color: #b87a5d;">Order & Pay At Counter</button>
          </form>
        </div>
      `;
    } else if (currentNiche === 'landscaping') {
      htmlContent = `
        <header class="sim-header">
          <div class="sim-logo">🌿 Fantastic Landscaping</div>
          <span class="sim-phone">📞 Call 0400 333 444</span>
        </header>
        
        <div class="sim-hero">
          <span class="sim-hero-badge" style="background-color: #134e5e; color: #fff;">Capricorn Landscapes</span>
          <h2>Outstanding Gardens & Turf Setups</h2>
          <p>Complete backyard transformations, premium lawn installations, and site excavation work.</p>
          <a href="#" class="sim-hero-cta" style="background-color: #134e5e;">View Design Portfolio</a>
        </div>
        
        <div class="sim-badge-row">
          ${showCleanup ? `
            <div class="sim-badge-card">
              <span class="sim-badge-icon">🧹</span>
              <div class="sim-badge-content">
                <h4>Spotless Site Clean Guarantee</h4>
                <p>We blow down paths and remove all lawn cuttings. Your yard looks clean immediately.</p>
              </div>
            </div>
          ` : ''}
          
          ${showOnTime ? `
            <div class="sim-badge-card">
              <span class="sim-badge-icon">🏗️</span>
              <div class="sim-badge-content">
                <h4>Dial-Before-You-Dig Badge</h4>
                <p>We check utility locations before excavation starts, protecting your power and fiber cables.</p>
              </div>
            </div>
          ` : ''}
        </div>
        
        <div class="sim-form-container">
          <div class="sim-form-title">Consultation Booking Request</div>
          <form class="sim-form-box" onsubmit="return false;">
            <input type="text" placeholder="Your Property Suburb" class="sim-input" required>
            
            ${showWaitlist ? `
              <div class="sim-estimator-widget" style="background-color: #e6f0ed;">
                <h4>📅 Design Project Waitlist</h4>
                <div class="sim-slider-row">
                  <span>Next Available Slot:</span>
                  <span class="sim-est-val" style="color: #134e5e;">Within 3 weeks</span>
                </div>
              </div>
            ` : ''}
            
            <button class="sim-btn" style="background-color: #134e5e;">Submit Enquiry</button>
          </form>
        </div>
      `;
    } else if (currentNiche === 'pest') {
      htmlContent = `
        <header class="sim-header">
          <div class="sim-logo">🐜 JLD Pest Solutions</div>
          <span class="sim-phone">🛡️ Fully Insured</span>
        </header>
        
        <div class="sim-hero">
          <span class="sim-hero-badge" style="background-color: #757f9a; color: #fff;">Safeguard Your Home</span>
          <h2>Safe, Effective Pest & Termite Control</h2>
          <p>Friendly cockroach sprays, flea sprays, and full chemical termite barriers across Central QLD.</p>
          <a href="#" class="sim-hero-cta" style="background-color: #4b5563;">Get a Spider Spray Quote</a>
        </div>
        
        <div class="sim-badge-row">
          ${showPolice ? `
            <div class="sim-badge-card">
              <span class="sim-badge-icon">👮</span>
              <div class="sim-badge-content">
                <h4>Police Cleared Technicians</h4>
                <p>Fully background checked and certified for your security and safety.</p>
              </div>
            </div>
          ` : ''}
          
          ${showCleanup ? `
            <div class="sim-badge-card">
              <span class="sim-badge-icon">📋</span>
              <div class="sim-badge-content">
                <h4>Price-Lock Guarantee</h4>
                <p>The price quoted is the price paid. We have zero surprise travel or surcharge fees.</p>
              </div>
            </div>
          ` : ''}
        </div>
        
        <div class="sim-form-container">
          <div class="sim-form-title">Request Rapid Treatment quote</div>
          <form class="sim-form-box" onsubmit="return false;">
            <input type="text" placeholder="Number of Bedrooms" class="sim-input" required>
            
            ${showWaitlist ? `
              <div class="sim-estimator-widget">
                <h4>🛡️ Treatment Warranty</h4>
                <div class="sim-slider-row">
                  <span>Free Retreat Period:</span>
                  <span class="sim-est-val">12 Months</span>
                </div>
              </div>
            ` : ''}
            
            <button class="sim-btn" style="background-color: #4b5563;">Get Immediate Price</button>
          </form>
        </div>
      `;
    }

    simWebContent.innerHTML = htmlContent;
  }

  // ==========================================
  // CONFIGURATION INTERFACE CONTROLLER
  // ==========================================
  
  function updateInteractiveControls() {
    // Hide all sliders by default
    toggleRowOnTime.classList.add('hidden');
    toggleRowCleanup.classList.add('hidden');
    toggleRowPolice.classList.add('hidden');
    toggleRowWaitlist.classList.add('hidden');

    // Customize inputs based on active industry
    if (currentNiche === 'plumbing') {
      toggleRowOnTime.classList.remove('hidden');
      toggleRowOnTime.querySelector('.toggle-title').textContent = 'On-Time Guarantee ($50 Payout)';
      toggleRowOnTime.querySelector('.toggle-desc').textContent = 'Offer clients $50 if late. Eliminates tradie delay anxiety.';
      
      toggleRowCleanup.classList.remove('hidden');
      toggleRowCleanup.querySelector('.toggle-title').textContent = 'Pristine Worksite Promise';
      toggleRowCleanup.querySelector('.toggle-desc').textContent = 'Guarantees no dirty footprints or debris left behind.';
      
      toggleRowWaitlist.classList.remove('hidden');
      toggleRowWaitlist.querySelector('.toggle-title').textContent = 'Live Queue Dispatch Tracker';
      toggleRowWaitlist.querySelector('.toggle-desc').textContent = 'Shows current dispatch load and approximate wait times.';
    } 
    else if (currentNiche === 'cafe') {
      toggleRowCleanup.classList.remove('hidden');
      toggleRowCleanup.querySelector('.toggle-title').textContent = 'Allergy-Safe Workspace Badge';
      toggleRowCleanup.querySelector('.toggle-desc').textContent = 'Prompts kitchen space separation rules for dietary filters.';
      
      toggleRowWaitlist.classList.remove('hidden');
      toggleRowWaitlist.querySelector('.toggle-title').textContent = 'Queue-Skip Estimated Timer';
      toggleRowWaitlist.querySelector('.toggle-desc').textContent = 'Indicates pick-up availability waiting times.';
    } 
    else if (currentNiche === 'landscaping') {
      toggleRowOnTime.classList.remove('hidden');
      toggleRowOnTime.querySelector('.toggle-title').textContent = 'Dial-Before-You-Dig Certificate';
      toggleRowOnTime.querySelector('.toggle-desc').textContent = 'Incorporate utility infrastructure checks before excavation.';
      
      toggleRowCleanup.classList.remove('hidden');
      toggleRowCleanup.querySelector('.toggle-title').textContent = 'Spotless Site Cleanup Guarantee';
      toggleRowCleanup.querySelector('.toggle-desc').textContent = 'Guarantees paths are blown down and green waste is cleared.';
      
      toggleRowWaitlist.classList.remove('hidden');
      toggleRowWaitlist.querySelector('.toggle-title').textContent = 'Design Phase Waitlist Tracker';
      toggleRowWaitlist.querySelector('.toggle-desc').textContent = 'Communicates start availability to generate immediate bookings.';
    } 
    else if (currentNiche === 'pest') {
      toggleRowPolice.classList.remove('hidden');
      toggleRowPolice.querySelector('.toggle-title').textContent = 'Police-Cleared Technician Badge';
      toggleRowPolice.querySelector('.toggle-desc').textContent = 'Establishes background check safety verification.';
      
      toggleRowCleanup.classList.remove('hidden');
      toggleRowCleanup.querySelector('.toggle-title').textContent = 'Locked-In Price Guarantee';
      toggleRowCleanup.querySelector('.toggle-desc').textContent = 'Warrants no additional travel surcharges post consultation.';
      
      toggleRowWaitlist.classList.remove('hidden');
      toggleRowWaitlist.querySelector('.toggle-title').textContent = '12-Month Spray Warranty';
      toggleRowWaitlist.querySelector('.toggle-desc').textContent = 'Guarantees a free respray if pests return within a year.';
    }

    // Adjust ROI slider rules
    const rules = ticketDefaults[currentNiche];
    ticketSlider.max = rules.max;
    ticketSlider.step = rules.step;
    ticketSlider.value = rules.val;
    roiUnitName.textContent = rules.unit + ' per month to break even.';

    // Set pricing amounts
    pricingAmount.textContent = pricingTiers[currentNiche];

    calculateROI();
    renderSimulatedWebsite();
  }

  // ==========================================
  // ROI CALCULATION ENGINE
  // ==========================================
  function calculateROI() {
    const fee = pricingTiers[currentNiche];
    const ticketValue = parseFloat(ticketSlider.value);
    ticketValDisplay.textContent = `$${ticketValue}`;

    const jobs = fee / ticketValue;
    if (jobs < 10) {
      roiJobsNeeded.textContent = jobs.toFixed(1);
    } else {
      roiJobsNeeded.textContent = Math.ceil(jobs);
    }
  }

  // ==========================================
  // EVENT LISTENERS: CONTROLS
  // ==========================================
  
  // Industry Cards Click
  nicheCards.forEach(card => {
    card.addEventListener('click', () => {
      nicheCards.forEach(c => c.classList.remove('active'));
      card.classList.add('active');
      currentNiche = card.dataset.niche;
      updateInteractiveControls();
      
      // Update background glow color slightly to reflect choices
      const glows = {
        plumbing: 'radial-gradient(circle, rgba(99, 102, 241, 0.09) 0%, transparent 60%)',
        cafe: 'radial-gradient(circle, rgba(200, 177, 149, 0.12) 0%, transparent 60%)',
        landscaping: 'radial-gradient(circle, rgba(19, 78, 94, 0.12) 0%, transparent 60%)',
        pest: 'radial-gradient(circle, rgba(117, 127, 154, 0.12) 0%, transparent 60%)'
      };
      document.querySelector('.simulator-glow').style.background = glows[currentNiche];
    });
  });

  // Slider change
  ticketSlider.addEventListener('input', calculateROI);

  // Checkboxes change
  checkOnTime.addEventListener('change', renderSimulatedWebsite);
  checkCleanup.addEventListener('change', renderSimulatedWebsite);
  checkPolice.addEventListener('change', renderSimulatedWebsite);
  checkWaitlist.addEventListener('change', renderSimulatedWebsite);

  // Device Frame Viewport toggles
  deviceTabletBtn.addEventListener('click', () => {
    deviceMobileBtn.classList.remove('active');
    deviceTabletBtn.classList.add('active');
    simFrame.classList.remove('mobile-view');
    simFrame.classList.add('tablet-view');
    renderSimulatedWebsite();
  });

  deviceMobileBtn.addEventListener('click', () => {
    deviceTabletBtn.classList.remove('active');
    deviceMobileBtn.classList.add('active');
    simFrame.classList.remove('tablet-view');
    simFrame.classList.add('mobile-view');
    renderSimulatedWebsite();
  });


  // ==========================================
  // LEAD CAPTURE DRAWER CONTROLS
  // ==========================================
  const leadDrawer = document.getElementById('lead-drawer-container');
  const btnOpenDrawer = document.getElementById('btn-open-drawer');
  const btnCloseDrawer = document.getElementById('btn-close-drawer');
  const overlayBtn = document.getElementById('drawer-overlay-btn');
  
  const drawerForm = document.getElementById('drawer-lead-form');
  const drawerSuccess = document.getElementById('drawer-success-box');
  const btnSuccessClose = document.getElementById('btn-success-close');

  function openDrawer() {
    leadDrawer.classList.add('active');
  }

  function closeDrawer() {
    leadDrawer.classList.remove('active');
    // Reset form states if complete
    setTimeout(() => {
      drawerForm.classList.remove('hidden');
      drawerSuccess.classList.add('hidden');
      drawerForm.reset();
    }, 400);
  }

  btnOpenDrawer.addEventListener('click', openDrawer);
  btnCloseDrawer.addEventListener('click', closeDrawer);
  overlayBtn.addEventListener('click', closeDrawer);
  btnSuccessClose.addEventListener('click', closeDrawer);

  // Form submit intercept
  drawerForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const bizName = document.getElementById('lead-biz-name').value;
    const ownerName = document.getElementById('lead-owner-name').value;
    const contact = document.getElementById('lead-contact').value;

    document.getElementById('val-owner-name').textContent = ownerName;
    document.getElementById('val-biz-name').textContent = bizName;
    document.getElementById('val-contact').textContent = contact;

    drawerForm.classList.add('hidden');
    drawerSuccess.classList.remove('hidden');
  });


  // ==========================================
  // FAQ MODAL CONTROLS
  // ==========================================
  const faqModal = document.getElementById('faqs-modal');
  const btnOpenFaqs = document.getElementById('btn-open-faqs');
  const btnCloseModal = document.getElementById('btn-close-modal');

  btnOpenFaqs.addEventListener('click', () => {
    faqModal.classList.remove('hidden');
  });

  btnCloseModal.addEventListener('click', () => {
    faqModal.classList.add('hidden');
  });

  faqModal.addEventListener('click', (e) => {
    if (e.target === faqModal) {
      faqModal.classList.add('hidden');
    }
  });


  // ==========================================
  // INITIAL RUN
  // ==========================================
  // Set default tabs active
  updateInteractiveControls();

});
