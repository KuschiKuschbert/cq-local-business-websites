import keppelCruiseUrl from './keppel_cruise.png';
import brutalistGymUrl from './brutalist_gym.png';
import gymTrainerUrl from './gym_trainer.png';
import cafeModernUrl from './cafe_modern.png';
import plumbingModernUrl from './plumbing_modern.png';
import landscapingModernUrl from './landscaping_modern.png';
import landscapingBeforeUrl from './landscaping_before.png';
import pestModernUrl from './pest_modern.png';


document.addEventListener('DOMContentLoaded', () => {

  // ==========================================
  // STATE MANAGEMENT
  // ==========================================
  let currentView = 'home'; // 'home' or 'sandbox'
  let currentNiche = 'plumbing';
  let deviceView = 'desktop';
  let cafeCartCount = 0;
  let activePestTab = 'risk';
  let gymActivePage = 'home'; // 'home' | 'workouts' | 'enquire'
  let gymCompletedWorkouts = 0;
  
  const pricingTiers = {
    plumbing: 249,
    cafe: 199,
    landscaping: 299,
    pest: 249,
    tour: 299,
    gym: 249
  };

  const ticketDefaults = {
    plumbing: { val: 220, max: 1000, step: 10, unit: 'residential service calls' },
    cafe: { val: 35, max: 150, step: 5, unit: 'pre-orders or bookings' },
    landscaping: { val: 450, max: 1500, step: 25, unit: 'excavations or yard cuts' },
    pest: { val: 180, max: 800, step: 10, unit: 'standard pest sprays' },
    tour: { val: 120, max: 500, step: 10, unit: 'ticket bookings' },
    gym: { val: 45, max: 200, step: 5, unit: 'monthly memberships' }
  };

  // ==========================================
  // SELECTORS
  // ==========================================
  const bodyEl = document.body;
  const viewHome = document.getElementById('view-home');
  const viewSandbox = document.getElementById('view-sandbox');
  
  const linkHome = document.getElementById('link-home');
  const linkSandbox = document.getElementById('link-sandbox');
  const linkPricing = document.getElementById('link-pricing');
  const linkFaqs = document.getElementById('link-faqs');
  const logoHome = document.getElementById('logo-nav-home');
  
  const heroBtnSandbox = document.getElementById('hero-btn-sandbox');
  const heroVisualBtn = document.getElementById('hero-visual-btn');
  const btnBackHome = document.getElementById('btn-back-home');
  
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
  const deviceDesktopBtn = document.getElementById('device-desktop');
  const deviceTabletBtn = document.getElementById('device-tablet');
  const deviceMobileBtn = document.getElementById('device-mobile');

  // ==========================================
  // VIEW ROUTING CONTROLLER
  // ==========================================
  
  function switchView(viewName) {
    if (viewName === 'home') {
      currentView = 'home';
      bodyEl.classList.remove('view-state-sandbox');
      bodyEl.classList.add('view-state-home');
      
      viewSandbox.classList.add('hidden');
      viewHome.classList.remove('hidden');
      
      linkSandbox.classList.remove('active');
      linkHome.classList.add('active');
      
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } else if (viewName === 'sandbox') {
      currentView = 'sandbox';
      bodyEl.classList.remove('view-state-home');
      bodyEl.classList.add('view-state-sandbox');
      
      viewHome.classList.add('hidden');
      viewSandbox.classList.remove('hidden');
      
      linkHome.classList.remove('active');
      linkSandbox.classList.add('active');
      
      window.scrollTo({ top: 0 });
      
      // Force immediate simulator layout calculation and render
      updateInteractiveControls();
    }
  }

  // Navigation Links listeners
  if (linkHome) linkHome.addEventListener('click', (e) => { e.preventDefault(); switchView('home'); });
  if (logoHome) logoHome.addEventListener('click', (e) => { e.preventDefault(); switchView('home'); });
  if (linkSandbox) linkSandbox.addEventListener('click', (e) => { e.preventDefault(); switchView('sandbox'); });
  
  // Hash nav smooth scrolling overrides for homepage
  if (linkPricing) {
    linkPricing.addEventListener('click', (e) => {
      e.preventDefault();
      switchView('home');
      setTimeout(() => {
        const target = document.getElementById('pricing-section');
        if (target) target.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    });
  }

  if (linkFaqs) {
    linkFaqs.addEventListener('click', (e) => {
      e.preventDefault();
      switchView('home');
      setTimeout(() => {
        const target = document.getElementById('faq-section');
        if (target) target.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    });
  }

  // Hero section buttons switcher
  if (heroBtnSandbox) heroBtnSandbox.addEventListener('click', () => switchView('sandbox'));
  if (heroVisualBtn) heroVisualBtn.addEventListener('click', () => switchView('sandbox'));
  if (btnBackHome) btnBackHome.addEventListener('click', () => switchView('home'));

  // Card select hooks from home page pricing
  document.querySelectorAll('[data-niche-select]').forEach(btn => {
    btn.addEventListener('click', () => {
      const niche = btn.dataset.nicheSelect;
      currentNiche = niche;
      cafeCartCount = 0;
      gymActivePage = 'home';
      gymCompletedWorkouts = 0;
      
      // Update active niche card in sandbox sidebar console
      nicheCards.forEach(card => {
        if (card.dataset.niche === niche) {
          card.classList.add('active');
        } else {
          card.classList.remove('active');
        }
      });

      switchView('sandbox');
    });
  });

  // ==========================================
  // DYNAMIC SIMULATOR WEBSITES GENERATION
  // ==========================================
  
  function renderSimulatedWebsite() {
    if (!simWebContent) return;
    
    // Update ambient background matching the niche
    const ambientBg = document.getElementById('sim-ambient-bg');
    if (ambientBg) {
      let ambientImgUrl = '';
      if (currentNiche === 'plumbing') ambientImgUrl = plumbingModernUrl;
      else if (currentNiche === 'cafe') ambientImgUrl = cafeModernUrl;
      else if (currentNiche === 'landscaping') ambientImgUrl = landscapingModernUrl;
      else if (currentNiche === 'pest') ambientImgUrl = pestModernUrl;
      else if (currentNiche === 'tour') ambientImgUrl = keppelCruiseUrl;
      else if (currentNiche === 'gym') ambientImgUrl = brutalistGymUrl;
      
      ambientBg.style.backgroundImage = ambientImgUrl ? `url('${ambientImgUrl}')` : 'none';
    }
    
    const showOnTime = checkOnTime.checked && !toggleRowOnTime.classList.contains('hidden');
    const showCleanup = checkCleanup.checked && !toggleRowCleanup.classList.contains('hidden');
    const showPolice = checkPolice.checked && !toggleRowPolice.classList.contains('hidden');
    const showWaitlist = checkWaitlist.checked && !toggleRowWaitlist.classList.contains('hidden');

    let htmlContent = '';

    if (currentNiche === 'plumbing') {
      htmlContent = `
        <div class="simulated-website sim-niche-plumbing">
          <header class="sim-header">
            <div class="sim-logo"><i data-lucide="droplet" style="width: 14px; height: 14px; stroke-width: 2.5px; color: #38bdf8; display: inline-block; vertical-align: middle; margin-right: 4px;"></i> Keppel Bay Plumbing</div>
            <span class="sim-phone"><i data-lucide="phone" style="width: 12px; height: 12px; stroke-width: 2.5px; display: inline-block; vertical-align: middle; margin-right: 4px;"></i> 0400 999 999</span>
          </header>
          
          <div class="sim-plumbing-grid">
            <div class="sim-plumbing-left">
              <div class="sim-tech-banner">
                <span class="sim-status-indicator">
                  <span class="sim-status-beacon"></span>
                  Emergency Dispatch: ACTIVE
                </span>
                <span style="font-size: 0.72rem; opacity: 0.8; font-family: monospace;">Yeppoon & Rocky</span>
              </div>
              
              <div class="sim-plumbing-hero">
                <span class="sim-hero-badge">24/7 Rapid Response</span>
                <h2>Central QLD's Emergency Plumber</h2>
                <p>Direct dispatch to residential hot water failures, burst pipes, and gas fitting emergencies.</p>
                <a href="tel:0400999999" class="sim-plumbing-hero-cta"><i data-lucide="phone-call" style="width: 12px; height: 12px; display: inline-block; vertical-align: middle; margin-right: 6px;"></i> Call Dispatch Now</a>
              </div>
              
              <div class="sim-plumbing-image-box" style="margin-top: 1rem; border-radius: 12px; overflow: hidden; height: 110px; border: 1px solid rgba(56, 189, 248, 0.15); margin-bottom: 1rem;">
                <img src="${plumbingModernUrl}" style="width: 100%; height: 100%; object-fit: cover; display: block;" alt="Emergency Plumbing Equipment">
              </div>
              
              <div class="sim-ticker-box">
                <div class="sim-ticker-title"><i data-lucide="activity" style="width: 14px; height: 14px; color: #38bdf8;"></i> Active Estimated Response Times</div>
                <div class="sim-ticker-list">
                  <div class="sim-ticker-item">
                    <span class="loc">Yeppoon (Coastal)</span>
                    <span class="time">25-40 mins</span>
                  </div>
                  <div class="sim-ticker-item">
                    <span class="loc">Rockhampton (City)</span>
                    <span class="time">30-50 mins</span>
                  </div>
                  <div class="sim-ticker-item">
                    <span class="loc">Gracemere / Outskirts</span>
                    <span class="time">45-65 mins</span>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="sim-plumbing-right">
              <div class="sim-badge-row">
                ${showOnTime ? `
                  <div class="sim-badge-card">
                    <span class="sim-badge-icon"><i data-lucide="clock" style="width: 24px; height: 24px; stroke-width: 2px; color: #38bdf8;"></i></span>
                    <div class="sim-badge-content">
                      <h4>On-Time Payout Guarantee</h4>
                      <p>We arrive on time, or we pay you $50. No excuses.</p>
                    </div>
                  </div>
                ` : ''}
                
                ${showCleanup ? `
                  <div class="sim-badge-card">
                    <span class="sim-badge-icon"><i data-lucide="sparkles" style="width: 24px; height: 24px; stroke-width: 2px; color: #38bdf8;"></i></span>
                    <div class="sim-badge-content">
                      <h4>Pristine Site Promise</h4>
                      <p>We clean up every metal shaving and boot footprint before we leave.</p>
                    </div>
                  </div>
                ` : ''}
              </div>
              
              <div class="sim-form-container">
                <div class="sim-form-title">Priority Online Dispatch Form</div>
                <form class="sim-form-box" onsubmit="return false;">
                  <input type="text" placeholder="Your Name" class="sim-input" required>
                  <input type="text" placeholder="Problem Details" class="sim-input" required>
                  
                  ${showWaitlist ? `
                    <div class="sim-estimator-widget">
                      <h4><i data-lucide="zap" style="width: 14px; height: 14px; color: #38bdf8; display: inline-block; vertical-align: middle; margin-right: 4px;"></i> Dispatch Status</h4>
                      <div class="sim-slider-row">
                        <span>Queue Load:</span>
                        <span class="sim-est-val">Light (Immediate)</span>
                      </div>
                    </div>
                  ` : ''}
                  
                  <button class="sim-btn">Request Dispatcher Call</button>
                </form>
              </div>
            </div>
          </div>
        </div>
      `;
    } else if (currentNiche === 'cafe') {
      htmlContent = `
        <div class="simulated-website sim-niche-cafe">
          <header class="sim-header">
            <div class="sim-logo">Coffee & Co.</div>
            <span class="sim-cart-badge"><i data-lucide="shopping-cart" style="width: 12px; height: 12px; stroke-width: 2.5px; display: inline-block; vertical-align: middle; margin-right: 4px;"></i> Cart (<span class="sim-cart-val">${cafeCartCount}</span>)</span>
          </header>
          
          <div class="sim-cafe-layout">
            <div class="sim-cafe-hero">
              <span class="sim-cafe-hero-badge">Est. 2018 — Yeppoon Foreshore</span>
              <h2>Specialty Coffee & Beachside Eats</h2>
              <p>A curated menu of house-roasted single origin beans, seasonal coastal bites, and fresh house-baked gluten-free pastries.</p>
            </div>
            
            <div class="sim-cafe-image-card" style="border-radius: 12px; overflow: hidden; height: 125px; border: 1px solid rgba(93, 64, 55, 0.15); margin-bottom: 1rem;">
              <img src="${cafeModernUrl}" style="width: 100%; height: 100%; object-fit: cover; display: block;" alt="Specialty Cafe Bar">
            </div>
            
            <div>
              <div class="sim-cafe-menu-title">Beachfront Pre-Order Menu</div>
              <div class="sim-cafe-menu-list">
                <div class="sim-cafe-menu-row">
                  <div class="sim-cafe-menu-details">
                    <span class="sim-cafe-menu-name">Flat White</span>
                    <span class="sim-cafe-menu-desc">House signature dark roast espresso blend, microfoam.</span>
                  </div>
                  <span class="sim-cafe-menu-leader"></span>
                  <div class="sim-cafe-menu-action">
                    <span class="sim-cafe-menu-price">$4.50</span>
                    <button class="sim-cafe-add-btn">Add</button>
                  </div>
                </div>
                <div class="sim-cafe-menu-row">
                  <div class="sim-cafe-menu-details">
                    <span class="sim-cafe-menu-name">Iced Latte</span>
                    <span class="sim-cafe-menu-desc">Double espresso shot poured over ice and chilled milk.</span>
                  </div>
                  <span class="sim-cafe-menu-leader"></span>
                  <div class="sim-cafe-menu-action">
                    <span class="sim-cafe-menu-price">$6.00</span>
                    <button class="sim-cafe-add-btn">Add</button>
                  </div>
                </div>
                <div class="sim-cafe-menu-row">
                  <div class="sim-cafe-menu-details">
                    <span class="sim-cafe-menu-name">Avocado Toast</span>
                    <span class="sim-cafe-menu-desc">Smashed local avo, marinated feta, cherry tomatoes on sourdough.</span>
                  </div>
                  <span class="sim-cafe-menu-leader"></span>
                  <div class="sim-cafe-menu-action">
                    <span class="sim-cafe-menu-price">$16.50</span>
                    <button class="sim-cafe-add-btn">Add</button>
                  </div>
                </div>
              </div>
            </div>

            ${showCleanup ? `
              <div class="sim-badge-row">
                <div class="sim-badge-card">
                  <span class="sim-badge-icon"><i data-lucide="heart" style="width: 24px; height: 24px; stroke-width: 2px; color: #5d4037;"></i></span>
                  <div class="sim-badge-content">
                    <h4>Allergy-Safe Separate Blenders</h4>
                    <p>Strict kitchen guidelines to eliminate soy, almond, and gluten cross-contact.</p>
                  </div>
                </div>
              </div>
            ` : ''}
            
            <div class="sim-form-container">
              <div class="sim-form-title">Table Reservation Request</div>
              <form class="sim-form-box" onsubmit="return false;">
                <input type="text" placeholder="Name" class="sim-input" required>
                
                ${showWaitlist ? `
                  <div class="sim-estimator-widget">
                    <h4><i data-lucide="hourglass" style="width: 14px; height: 14px; color: #5d4037; display: inline-block; vertical-align: middle; margin-right: 4px;"></i> Live Peak Wait Time</h4>
                    <div class="sim-slider-row">
                      <span>Approx. Wait:</span>
                      <span class="sim-est-val">5-10 minutes</span>
                    </div>
                  </div>
                ` : ''}
                
                <button class="sim-btn">Reserve Beachfront Table</button>
              </form>
            </div>
            
            ${cafeCartCount > 0 ? `
              <div class="sim-cafe-floating-checkout">
                <p><i data-lucide="coffee" style="width: 14px; height: 14px; display: inline-block; vertical-align: middle; margin-right: 4px;"></i> Pre-Order: ${cafeCartCount} item${cafeCartCount > 1 ? 's' : ''}</p>
                <button class="sim-cafe-checkout-btn">Checkout Now</button>
              </div>
            ` : ''}
          </div>
        </div>
      `;
    } else if (currentNiche === 'landscaping') {
      htmlContent = `
        <div class="simulated-website sim-niche-landscaping">
          <header class="sim-header">
            <div class="sim-logo"><i data-lucide="sprout" style="width: 16px; height: 16px; color: #1e3a24; display: inline-block; vertical-align: middle; margin-right: 4px;"></i> Fantastic Landscaping</div>
            <span class="sim-phone"><i data-lucide="phone" style="width: 12px; height: 12px; display: inline-block; vertical-align: middle; margin-right: 4px;"></i> 0400 333 444</span>
          </header>
          
          <div class="sim-landscaping-layout">
            <div class="sim-landscaping-left">
              <div class="sim-landscaping-hero">
                <span class="sim-landscaping-hero-badge">Yeppoon & Capricorn Coast</span>
                <h2>High-End Backyard Design & Earthworks</h2>
                <p>Premium turf laying, structural retaining walls, and custom resort-style landscaping designs tailored for local conditions.</p>
                <a href="#" class="sim-landscaping-hero-cta">Request Design Consult</a>
              </div>
              
              <div class="sim-before-after-widget">
                <div class="sim-ba-image sim-ba-before" style="background-image: url('${landscapingBeforeUrl}');">
                  <span class="sim-ba-img-label" style="background-color: rgba(0,0,0,0.65);">Dry Clay Ground (Before)</span>
                </div>
                <div class="sim-ba-image sim-ba-after" style="background-image: url('${landscapingModernUrl}');">
                  <span class="sim-ba-img-label" style="background-color: #1e3a24;">Premium Couch Turf (After)</span>
                </div>
                <input type="range" min="0" max="100" value="50" class="sim-ba-range-slider">
                <div class="sim-ba-divider"></div>
                <div class="sim-ba-handle"><i data-lucide="arrow-left-right" style="width: 14px; height: 14px;"></i></div>
              </div>
            </div>
            
            <div class="sim-landscaping-right">
              <div class="sim-badge-row">
                ${showCleanup ? `
                  <div class="sim-badge-card">
                    <span class="sim-badge-icon"><i data-lucide="sparkles" style="width: 24px; height: 24px; color: #1e3a24;"></i></span>
                    <div class="sim-badge-content">
                      <h4>Spotless Green Cleanup</h4>
                      <p>We blow down paths and remove all green waste. Your garden is ready to enjoy immediately.</p>
                    </div>
                  </div>
                ` : ''}
                
                ${showOnTime ? `
                  <div class="sim-badge-card">
                    <span class="sim-badge-icon"><i data-lucide="compass" style="width: 24px; height: 24px; color: #1e3a24;"></i></span>
                    <div class="sim-badge-content">
                      <h4>Dial-Before-You-Dig Verified</h4>
                      <p>We double check underground services before we break ground, ensuring property safety.</p>
                    </div>
                  </div>
                ` : ''}
              </div>
              
              <div class="sim-form-container">
                <div class="sim-form-title">Consultation Booking</div>
                <form class="sim-form-box" onsubmit="return false;">
                  <input type="text" placeholder="Suburb location" class="sim-input" required>
                  
                  ${showWaitlist ? `
                    <div class="sim-estimator-widget">
                      <h4><i data-lucide="calendar" style="width: 14px; height: 14px; color: #1e3a24; display: inline-block; vertical-align: middle; margin-right: 4px;"></i> Project Waitlist</h4>
                      <div class="sim-slider-row">
                        <span>Start Window:</span>
                        <span class="sim-est-val">Within 2-3 Weeks</span>
                      </div>
                    </div>
                  ` : ''}
                  
                  <button class="sim-btn">Submit Yard Enquiry</button>
                </form>
              </div>
            </div>
          </div>
        </div>
      `;
    } else if (currentNiche === 'pest') {
      htmlContent = `
        <div class="simulated-website sim-niche-pest">
          <header class="sim-header">
            <div class="sim-logo"><i data-lucide="shield" style="width: 15px; height: 15px; color: #212529; display: inline-block; vertical-align: middle; margin-right: 4px;"></i> JLD Pest Solutions</div>
            <span class="sim-phone"><i data-lucide="shield-check" style="width: 12px; height: 12px; display: inline-block; vertical-align: middle; margin-right: 4px;"></i> License #12288</span>
          </header>
          
          <div class="sim-pest-portal">
            <aside class="sim-pest-sidebar">
              <div class="sim-pest-side-link ${activePestTab === 'risk' ? 'active' : ''}" data-tab="risk"><i data-lucide="clipboard-check" style="width: 14px; height: 14px;"></i> Risk Analyzer</div>
              <div class="sim-pest-side-link ${activePestTab === 'warranty' ? 'active' : ''}" data-tab="warranty"><i data-lucide="award" style="width: 14px; height: 14px;"></i> Warranties</div>
            </aside>
            
            <main class="sim-pest-portal-body">
              <div class="sim-pest-image-banner" style="border-radius: 8px; overflow: hidden; height: 95px; border: 1px solid #dee2e6; margin-bottom: 0.75rem;">
                <img src="${pestModernUrl}" style="width: 100%; height: 100%; object-fit: cover; display: block;" alt="Accredited Safe Home">
              </div>
              ${activePestTab === 'risk' ? `
                <div class="sim-pest-hero">
                  <h2>SaaS Diagnostic Pest & Termite Board</h2>
                  <p>Select pest threat parameters below to generate an estimate calculation and treatment strategy.</p>
                </div>
                
                <div class="sim-threat-grid">
                  <button class="sim-threat-btn active" data-type="spiders">
                    <i data-lucide="bug" style="width: 16px; height: 16px;"></i>
                    <div class="sim-threat-name">Spiders</div>
                  </button>
                  <button class="sim-threat-btn" data-type="termites">
                    <i data-lucide="activity" style="width: 16px; height: 16px;"></i>
                    <div class="sim-threat-name">Termites</div>
                  </button>
                  <button class="sim-threat-btn" data-type="rodents">
                    <i data-lucide="shield-alert" style="width: 16px; height: 16px;"></i>
                    <div class="sim-threat-name">Rodents</div>
                  </button>
                </div>
                
                <div class="sim-diagnostic-card">
                  <div class="sim-diag-title">Active Selection: Spiders & Ants Treatment</div>
                  <div class="sim-diag-desc">Child-safe residual exterior and interior spray barrier. Targeted dusting in voids.</div>
                  <div class="sim-diag-price-row">
                    <span class="sim-diag-price-label">Estimated Service:</span>
                    <span class="sim-diag-price">$180</span>
                  </div>
                </div>
                
                <div class="sim-pest-risk-calculator">
                  <h4>Interactive Suburb Risk Checklist</h4>
                  <div class="sim-risk-checklist">
                    <label class="sim-risk-label">
                      <input type="checkbox" class="sim-risk-check" value="25" checked>
                      Wood rot/timber decay present (+25% risk)
                    </label>
                    <label class="sim-risk-label">
                      <input type="checkbox" class="sim-risk-check" value="20">
                      Close proximity to bushland (+20% risk)
                    </label>
                    <label class="sim-risk-label">
                      <input type="checkbox" class="sim-risk-check" value="15">
                      Humid damp subflooring (+15% risk)
                    </label>
                  </div>
                  <div class="sim-risk-output">
                    <span style="font-size: 0.72rem; font-weight: 600; color: #495057;">Current Calculated Risk:</span>
                    <span class="sim-risk-score-badge low" id="sim-risk-score">Low Risk (25%)</span>
                  </div>
                </div>
              ` : `
                <div class="sim-pest-hero">
                  <h2>Fully Accredited Local Warranties</h2>
                  <p>Our work is backed by our rock-solid Capricorn Coast performance certificates.</p>
                </div>
                <div class="sim-badge-row">
                  <div class="sim-badge-card" style="margin-bottom: 0.5rem;">
                    <span class="sim-badge-icon"><i data-lucide="shield-check" style="width: 24px; height: 24px; color: #212529;"></i></span>
                    <div class="sim-badge-content">
                      <h4>12-Month Re-Spray Protection</h4>
                      <p>If ants or common spiders return within a year, we will spray again completely free.</p>
                    </div>
                  </div>
                  <div class="sim-badge-card">
                    <span class="sim-badge-icon"><i data-lucide="award" style="width: 24px; height: 24px; color: #212529;"></i></span>
                    <div class="sim-badge-content">
                      <h4>$100,000 Termite Damage Indemnity</h4>
                      <p>All full termite treatment barriers qualify for chemical warranty security coverage.</p>
                    </div>
                  </div>
                </div>
              `}

              <div class="sim-badge-row">
                ${showPolice ? `
                  <div class="sim-badge-card">
                    <span class="sim-badge-icon"><i data-lucide="user-check" style="width: 24px; height: 24px; color: #212529;"></i></span>
                    <div class="sim-badge-content">
                      <h4>Police Cleared Technicians</h4>
                      <p>For your comfort and absolute safety in and around your home.</p>
                    </div>
                  </div>
                ` : ''}
                
                ${showCleanup ? `
                  <div class="sim-badge-card">
                    <span class="sim-badge-icon"><i data-lucide="lock" style="width: 24px; height: 24px; color: #212529;"></i></span>
                    <div class="sim-badge-content">
                      <h4>Locked-In Flat Quotes</h4>
                      <p>We guarantee no extra travel costs or hourly surcharges after booking.</p>
                    </div>
                  </div>
                ` : ''}
              </div>
              
              <div class="sim-form-container">
                <div class="sim-form-title">Priority Diagnostic Booking</div>
                <form class="sim-form-box" onsubmit="return false;">
                  <input type="text" placeholder="Owner / Address" class="sim-input" required>
                  
                  ${showWaitlist ? `
                    <div class="sim-estimator-widget">
                      <h4><i data-lucide="shield" style="width: 14px; height: 14px; color: #212529; display: inline-block; vertical-align: middle; margin-right: 4px;"></i> Treatment Warranty</h4>
                      <div class="sim-slider-row">
                        <span>Warranty Period:</span>
                        <span class="sim-est-val">12-Month Guarantee</span>
                      </div>
                    </div>
                  ` : ''}
                  
                  <button class="sim-btn">Request Technician Visit</button>
                </form>
              </div>
            </main>
          </div>
        </div>
      `;
    } else if (currentNiche === 'tour') {
      htmlContent = `
        <div class="simulated-website sim-niche-tour">
          <header class="sim-header">
            <div class="sim-logo"><i data-lucide="ship" style="width: 15px; height: 15px; color: #f97316; display: inline-block; vertical-align: middle; margin-right: 4px;"></i> Keppel Cruises</div>
            <span class="sim-phone"><i data-lucide="phone" style="width: 12px; height: 12px; display: inline-block; vertical-align: middle; margin-right: 4px;"></i> Bookings: 07 4930 1111</span>
          </header>
          
          <div class="sim-tour-nav-tip">&larr; Swipe Horizontally to Explore Deck &rarr;</div>
          
          <div class="sim-tour-horizontal-scroll">
            
            <!-- Panel 1: Story Intro -->
            <div class="sim-tour-card-panel">
              <div>
                <span class="sim-tour-panel-tag">Explore Keppel Islands</span>
                <h2 style="margin-top: 0.5rem; margin-bottom: 0.75rem;">Great Keppel Island Day Cruise</h2>
                <p>Sail across pristine turquoise waters of Keppel Bay. Hop off at secluded white-sand beaches, snorkel untouched reef shelves, and enjoy local fresh buffets.</p>
              </div>
              <a href="#" class="sim-tour-cta-btn">Book Cruise Seat</a>
            </div>
            
            <!-- Panel Image: Keppel Serenity -->
            <div class="sim-tour-card-panel" style="background: url('${keppelCruiseUrl}') no-repeat center center; background-size: cover; position: relative;">
              <div style="background: linear-gradient(to top, rgba(15, 23, 42, 0.95) 0%, rgba(15, 23, 42, 0.2) 60%, rgba(15, 23, 42, 0) 100%); position: absolute; inset: 0; border-radius: 15px; display: flex; flex-direction: column; justify-content: flex-end; padding: 1.5rem;">
                <span class="sim-tour-panel-tag" style="color: #fb923c;">Our Vessel</span>
                <h2 style="margin-top: 0.3rem; margin-bottom: 0.25rem; font-size: 1.4rem;">Keppel Serenity</h2>
                <p style="color: #cbd5e1; font-size: 0.75rem; margin: 0; line-height: 1.4;">Premium 15m sailing catamaran featuring open decks, dual trampolines, and shaded lounges.</p>
              </div>
            </div>
            
            <!-- Panel 2: Inclusions & Badges -->
            <div class="sim-tour-card-panel">
              <div>
                <span class="sim-tour-panel-tag">What's On Board</span>
                <h2 style="margin-top: 0.5rem; margin-bottom: 0.75rem;">Premium Trip Inclusions</h2>
                <div class="sim-tour-grid" style="margin-top: 1rem;">
                  <div class="sim-tour-item">
                    <h4>Meals</h4>
                    <p>Included</p>
                  </div>
                  <div class="sim-tour-item">
                    <h4>Gear</h4>
                    <p>Free Snorkel</p>
                  </div>
                  <div class="sim-tour-item">
                    <h4>Guide</h4>
                    <p>Marine Biol</p>
                  </div>
                </div>
                
                <div class="sim-badge-row" style="margin-top: 1.25rem;">
                  ${showOnTime ? `
                    <div class="sim-badge-card" style="background-color: #111827; border: 1px solid rgba(249, 115, 22, 0.2);">
                      <span class="sim-badge-icon"><i data-lucide="compass" style="width: 24px; height: 24px; color: #fb923c;"></i></span>
                      <div class="sim-badge-content">
                        <h4 style="color:#fff;">Seasick Refund Policy</h4>
                        <p style="color:#94a3b8;">Full seat credit refund if water swell exceeds 1.8 meters.</p>
                      </div>
                    </div>
                  ` : ''}
                  ${showCleanup ? `
                    <div class="sim-badge-card" style="background-color: #111827; border: 1px solid rgba(249, 115, 22, 0.2);">
                      <span class="sim-badge-icon"><i data-lucide="leaf" style="width: 24px; height: 24px; color: #fb923c;"></i></span>
                      <div class="sim-badge-content">
                        <h4 style="color:#fff;">Marine Eco Label</h4>
                        <p style="color:#94a3b8;">100% carbon-offset, reef-safe emissions cert.</p>
                      </div>
                    </div>
                  ` : ''}
                </div>
              </div>
            </div>

            <!-- Panel 3: Reservation -->
            <div class="sim-tour-card-panel">
              <div>
                <span class="sim-tour-panel-tag">Secure Your Spot</span>
                <h2 style="margin-top: 0.5rem; margin-bottom: 0.75rem;">Online Pre-Booking</h2>
                <form class="sim-form-box" onsubmit="return false;" style="background: transparent; border: none; padding:0;">
                  <input type="text" placeholder="Passes (e.g. 2 Adults)" class="sim-input" style="background-color: #0f172a; border-color: rgba(249, 115, 22, 0.3); color:#fff;" required>
                  
                  ${showWaitlist ? `
                    <div class="sim-estimator-widget" style="background-color: #0f172a; border: 1px solid rgba(249, 115, 22, 0.2); padding: 0.75rem; margin-top: 0.5rem;">
                      <h4 style="color:#fff; font-size: 0.75rem;"><i data-lucide="users" style="width: 12px; height: 12px; color: #f97316; display: inline-block; vertical-align: middle; margin-right: 4px;"></i> Seats Remaining</h4>
                      <div class="sim-slider-row">
                        <span>Next Cruise (9:00 AM):</span>
                        <span class="sim-est-val" style="color: #fb923c; font-size: 0.85rem;">14 Slots Left</span>
                      </div>
                    </div>
                  ` : ''}
                  
                  <button class="sim-tour-cta-btn" style="border:none; cursor:pointer; width:100%; margin-top: 0.5rem;">Reserve Seat</button>
                </form>
              </div>
            </div>
            
          </div>
        </div>
      `;
    } else if (currentNiche === 'gym') {
      htmlContent = `
        <div class="simulated-website sim-niche-gym">
          <header class="sim-header" style="display: flex; justify-content: space-between; align-items: center; border-bottom: 3.5px solid #000; padding: 0.75rem 1rem;">
            <div class="sim-logo" style="font-size: 0.9rem; font-weight: 900; text-transform: uppercase;"><i data-lucide="dumbbell" style="width: 15px; height: 15px; color: #000; display: inline-block; vertical-align: middle; margin-right: 4px;"></i> Rocky Strength</div>
            <nav class="sim-gym-navbar" style="display: flex; gap: 0.25rem;">
              <a href="#" class="sim-gym-nav-link ${gymActivePage === 'home' ? 'active' : ''}" data-gym-page="home" style="font-size: 0.7rem;">Home</a>
              <a href="#" class="sim-gym-nav-link ${gymActivePage === 'workouts' ? 'active' : ''}" data-gym-page="workouts" style="font-size: 0.7rem;">Schedule</a>
              <a href="#" class="sim-gym-nav-link ${gymActivePage === 'enquire' ? 'active' : ''}" data-gym-page="enquire" style="font-size: 0.7rem;">Join</a>
            </nav>
          </header>
          
          <div class="sim-gym-body" style="padding: 1rem; display: flex; flex-direction: column; gap: 1rem;">
            ${gymActivePage === 'home' ? `
              
              <!-- Gym Banner Facility Hero -->
              <div class="sim-brutalist-card" style="padding: 0; overflow: hidden; border: 3.5px solid #000; box-shadow: 4px 4px 0px #000; height: 125px; position: relative;">
                <img src="${brutalistGymUrl}" style="width: 100%; height: 100%; object-fit: cover; display: block; filter: brightness(0.45);" alt="Rocky Power Gym Facility">
                <div style="position: absolute; inset: 0; padding: 1rem; display: flex; flex-direction: column; justify-content: flex-end; color: #fff;">
                  <span style="font-family: var(--font-mono); font-size: 0.6rem; letter-spacing: 0.1em; color: #facc15; text-transform: uppercase;">[ 24/7 Heavy Strength ]</span>
                  <h3 style="font-size: 1.15rem; font-weight: 900; text-transform: uppercase; margin: 0.25rem 0;">Rocky Strength & Power</h3>
                </div>
              </div>

              <div class="sim-brutalist-card" style="background-color: #fff; border: 3.5px solid #000; box-shadow: 4px 4px 0px #000; padding: 1rem; display: flex; flex-direction: column; gap: 0.5rem;">
                <span class="sim-brutalist-title" style="font-size: 0.72rem; font-weight:900; background-color: #facc15; border: 2px solid #000; padding: 0.15rem 0.35rem; align-self: flex-start;">No Contracts. No Gimmicks.</span>
                <p style="font-size: 0.75rem; font-weight:600; line-height: 1.4; margin: 0.25rem 0;">Capricorn Coast's premier facility for powerlifting, weightlifting, and athletic development. Featuring competition grade racks and calibrated plates.</p>
                <button class="sim-brutalist-btn" data-gym-page="enquire" style="width: 100%; margin-top: 0.25rem;">Claim Free 3-Day Pass</button>
              </div>
              
              <div class="sim-badge-row" style="display: flex; flex-direction: column; gap: 0.75rem;">
                ${showOnTime ? `
                  <div class="sim-badge-card" style="border: 3px solid #000; box-shadow: 4px 4px 0px #000; background-color: #fff; padding: 0.75rem; display: flex; gap: 0.75rem; align-items: center;">
                    <span class="sim-badge-icon" style="flex-shrink: 0;"><i data-lucide="key" style="width: 20px; height: 20px; color: #000;"></i></span>
                    <div class="sim-badge-content">
                      <h4 style="font-weight:900; font-size: 0.75rem; margin: 0;">24/7 Key Access</h4>
                      <p style="font-size: 0.68rem; color: #333; margin: 0.15rem 0 0 0;">Secure swipe access keys included for all members.</p>
                    </div>
                  </div>
                ` : ''}
                ${showCleanup ? `
                  <div class="sim-badge-card" style="border: 3px solid #000; box-shadow: 4px 4px 0px #000; background-color: #fff; padding: 0.75rem; display: flex; gap: 0.75rem; align-items: center;">
                    <span class="sim-badge-icon" style="flex-shrink: 0;"><i data-lucide="user-check" style="width: 20px; height: 20px; color: #000;"></i></span>
                    <div class="sim-badge-content">
                      <h4 style="font-weight:900; font-size: 0.75rem; margin: 0;">Accredited Coaches Only</h4>
                      <p style="font-size: 0.68rem; color: #333; margin: 0.15rem 0 0 0;">All trainers hold ASCA Strength & Conditioning certifications.</p>
                    </div>
                  </div>
                ` : ''}
              </div>
            ` : gymActivePage === 'workouts' ? `
              
              <!-- Coaching banner -->
              <div class="sim-brutalist-card" style="padding: 0; overflow: hidden; border: 3.5px solid #000; box-shadow: 4px 4px 0px #000; height: 115px;">
                <img src="${gymTrainerUrl}" style="width: 100%; height: 100%; object-fit: cover; display: block;" alt="Rocky Strength Coach Team">
              </div>
              
              <div class="sim-brutalist-card" style="background-color: #fff; border: 3.5px solid #000; box-shadow: 4px 4px 0px #000; padding: 1rem;">
                <span class="sim-brutalist-title" style="font-size: 0.72rem; font-weight:900; background-color: #000; color: #fff; border: 2px solid #000; padding: 0.15rem 0.35rem; align-self: flex-start; margin-bottom: 0.5rem;">Daily Group Sessions</span>
                
                <div class="sim-gym-timetable" style="display: flex; flex-direction: column; gap: 0.5rem; margin-top: 0.5rem;">
                  <div style="display: flex; justify-content: space-between; align-items: center; border: 2px solid #000; padding: 0.5rem; background-color: #fff; font-size: 0.7rem; font-weight: 800;">
                    <div>
                      <span style="color:#e65100;">06:00 AM</span> — Powerlifting
                    </div>
                    <button class="sim-brutalist-btn" style="padding: 0.2rem 0.5rem; font-size: 0.6rem; box-shadow: none;" onclick="this.textContent='Booked'; this.disabled=true;">Book Spot</button>
                  </div>
                  
                  <div style="display: flex; justify-content: space-between; align-items: center; border: 2px solid #000; padding: 0.5rem; background-color: #fff; font-size: 0.7rem; font-weight: 800;">
                    <div>
                      <span style="color:#e65100;">05:30 PM</span> — Olympic Lifting
                    </div>
                    <button class="sim-brutalist-btn" style="padding: 0.2rem 0.5rem; font-size: 0.6rem; box-shadow: none;" onclick="this.textContent='Booked'; this.disabled=true;">Book Spot</button>
                  </div>

                  <div style="display: flex; justify-content: space-between; align-items: center; border: 2px solid #000; padding: 0.5rem; background-color: #fff; font-size: 0.7rem; font-weight: 800;">
                    <div>
                      <span style="color:#e65100;">06:30 PM</span> — Strength & Cond
                    </div>
                    <button class="sim-brutalist-btn" style="padding: 0.2rem 0.5rem; font-size: 0.6rem; box-shadow: none;" onclick="this.textContent='Booked'; this.disabled=true;">Book Spot</button>
                  </div>
                </div>
              </div>
            ` : `
              
              <!-- Grayscaled Coaching Image -->
              <div class="sim-brutalist-card" style="padding: 0; overflow: hidden; border: 3.5px solid #000; box-shadow: 4px 4px 0px #000; height: 110px;">
                <img src="${gymTrainerUrl}" style="width: 100%; height: 100%; object-fit: cover; display: block; filter: grayscale(1);" alt="Intake Consultation Coaching">
              </div>
              
              <div class="sim-brutalist-card" style="background-color: #fff; border: 3.5px solid #000; box-shadow: 4px 4px 0px #000; padding: 1rem;">
                <span class="sim-brutalist-title" style="font-size: 0.72rem; font-weight:900; background-color: #facc15; border: 2px solid #000; padding: 0.15rem 0.35rem; align-self: flex-start; margin-bottom: 0.5rem;">Choose Membership</span>
                
                <div style="display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 0.75rem;">
                  <div style="border: 2px solid #000; padding: 0.5rem; background-color: #fff; font-size: 0.7rem; display: flex; justify-content: space-between; align-items: center; font-weight: 800;">
                    <span>Standard Access</span>
                    <span style="color:#e65100;">$18/wk</span>
                  </div>
                  <div style="border: 2px solid #000; padding: 0.5rem; background-color: #fff; font-size: 0.7rem; display: flex; justify-content: space-between; align-items: center; font-weight: 800;">
                    <span>Coached Athlete</span>
                    <span style="color:#e65100;">$45/wk</span>
                  </div>
                </div>

                <form class="sim-form-box" onsubmit="alert('Pass Issued! Check your SMS.'); return false;" style="background:transparent; border:none; padding:0; display: flex; flex-direction: column; gap: 0.5rem;">
                  <input type="text" placeholder="Your Name" class="sim-input" style="border: 2px solid #000; padding: 0.4rem; font-size: 0.72rem; font-weight: 700; background-color:#fff;" required>
                  <input type="tel" placeholder="Mobile Number" class="sim-input" style="border: 2px solid #000; padding: 0.4rem; font-size: 0.72rem; font-weight: 700; background-color:#fff;" required>
                  
                  ${showWaitlist ? `
                    <div class="sim-estimator-widget" style="background-color: #fff; border: 2.5px solid #000; box-shadow: 2px 2px 0px #000; padding: 0.5rem; margin-top: 0.25rem;">
                      <h4 style="font-weight:900; font-size: 0.65rem; margin: 0;"><i data-lucide="activity" style="width: 10px; height: 10px; color: #000; display: inline-block; vertical-align: middle; margin-right: 4px;"></i> Facility Volume</h4>
                      <div class="sim-slider-row" style="display: flex; justify-content: space-between; font-size: 0.65rem; margin-top: 0.25rem;">
                        <span>Occupancy:</span>
                        <span style="font-weight: 900;">Moderate (42%)</span>
                      </div>
                    </div>
                  ` : ''}
                  
                  <button class="sim-brutalist-btn" style="margin-top:0.25rem; width: 100%;">Get Free Trial Pass</button>
                </form>
              </div>
            `}
          </div>
        </div>
      `;
    }

    simWebContent.innerHTML = htmlContent;
    if (window.lucide) {
      window.lucide.createIcons();
    }
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
    else if (currentNiche === 'tour') {
      toggleRowOnTime.classList.remove('hidden');
      toggleRowOnTime.querySelector('.toggle-title').textContent = 'Seasick Refund Policy Badge';
      toggleRowOnTime.querySelector('.toggle-desc').textContent = 'Promotes refund if water swell exceeds limit.';
      
      toggleRowCleanup.classList.remove('hidden');
      toggleRowCleanup.querySelector('.toggle-title').textContent = 'Marine-Safe Eco Label';
      toggleRowCleanup.querySelector('.toggle-desc').textContent = 'Guarantees eco-sustainable reef-friendly engines.';
      
      toggleRowWaitlist.classList.remove('hidden');
      toggleRowWaitlist.querySelector('.toggle-title').textContent = 'Available Seats Live Counter';
      toggleRowWaitlist.querySelector('.toggle-desc').textContent = 'Display remaining deck slots on the next cruise.';
    }
    else if (currentNiche === 'gym') {
      toggleRowOnTime.classList.remove('hidden');
      toggleRowOnTime.querySelector('.toggle-title').textContent = '24/7 Access Badge';
      toggleRowOnTime.querySelector('.toggle-desc').textContent = 'Highlights secure swipe access keycard system.';
      
      toggleRowCleanup.classList.remove('hidden');
      toggleRowCleanup.querySelector('.toggle-title').textContent = 'Certified Trainers Label';
      toggleRowCleanup.querySelector('.toggle-desc').textContent = 'Prompts professional diagnostic coaching checks.';
      
      toggleRowWaitlist.classList.remove('hidden');
      toggleRowWaitlist.querySelector('.toggle-title').textContent = 'Peak Capacity Tracker';
      toggleRowWaitlist.querySelector('.toggle-desc').textContent = 'Displays live active club attendance volume.';
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
      cafeCartCount = 0; // Reset cart when niche changes
      gymActivePage = 'home';
      gymCompletedWorkouts = 0;
      updateInteractiveControls();
      
      // Update background glow color slightly to reflect choices
      const glows = {
        plumbing: 'radial-gradient(circle, rgba(99, 102, 241, 0.09) 0%, transparent 60%)',
        cafe: 'radial-gradient(circle, rgba(200, 177, 149, 0.12) 0%, transparent 60%)',
        landscaping: 'radial-gradient(circle, rgba(19, 78, 94, 0.12) 0%, transparent 60%)',
        pest: 'radial-gradient(circle, rgba(117, 127, 154, 0.12) 0%, transparent 60%)',
        tour: 'radial-gradient(circle, rgba(249, 115, 22, 0.12) 0%, transparent 60%)',
        gym: 'radial-gradient(circle, rgba(250, 204, 21, 0.12) 0%, transparent 60%)'
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
  if (deviceDesktopBtn) {
    deviceDesktopBtn.addEventListener('click', () => {
      deviceTabletBtn.classList.remove('active');
      deviceMobileBtn.classList.remove('active');
      deviceDesktopBtn.classList.add('active');
      simFrame.classList.remove('tablet-view', 'mobile-view');
      simFrame.classList.add('desktop-view');
      deviceView = 'desktop';
      renderSimulatedWebsite();
    });
  }

  if (deviceTabletBtn) {
    deviceTabletBtn.addEventListener('click', () => {
      deviceDesktopBtn.classList.remove('active');
      deviceMobileBtn.classList.remove('active');
      deviceTabletBtn.classList.add('active');
      simFrame.classList.remove('desktop-view', 'mobile-view');
      simFrame.classList.add('tablet-view');
      deviceView = 'tablet';
      renderSimulatedWebsite();
    });
  }

  if (deviceMobileBtn) {
    deviceMobileBtn.addEventListener('click', () => {
      deviceDesktopBtn.classList.remove('active');
      deviceTabletBtn.classList.remove('active');
      deviceMobileBtn.classList.add('active');
      simFrame.classList.remove('desktop-view', 'tablet-view');
      simFrame.classList.add('mobile-view');
      deviceView = 'mobile';
      renderSimulatedWebsite();
    });
  }

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

  // Bind drawer events
  if (btnOpenDrawer) btnOpenDrawer.addEventListener('click', openDrawer);
  if (btnCloseDrawer) btnCloseDrawer.addEventListener('click', closeDrawer);
  if (overlayBtn) overlayBtn.addEventListener('click', closeDrawer);
  if (btnSuccessClose) btnSuccessClose.addEventListener('click', closeDrawer);

  const heroBtnMockup = document.getElementById('hero-btn-mockup');
  const navBtnMockup = document.getElementById('nav-btn-mockup');
  const ctaBtnOpenDrawer = document.getElementById('cta-btn-open-drawer');

  if (heroBtnMockup) heroBtnMockup.addEventListener('click', openDrawer);
  if (navBtnMockup) navBtnMockup.addEventListener('click', openDrawer);
  if (ctaBtnOpenDrawer) ctaBtnOpenDrawer.addEventListener('click', openDrawer);

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
  // HOMEPAGE ACCORDION FAQS CONTROLLER
  // ==========================================
  document.querySelectorAll('.accordion-header').forEach(header => {
    header.addEventListener('click', () => {
      const item = header.parentElement;
      const body = header.nextElementSibling;
      const isAlreadyActive = item.classList.contains('active');
      
      // Close all other accordion items
      document.querySelectorAll('.accordion-item').forEach(otherItem => {
        otherItem.classList.remove('active');
        otherItem.querySelector('.accordion-body').style.maxHeight = '0';
      });

      if (!isAlreadyActive) {
        item.classList.add('active');
        body.style.maxHeight = body.scrollHeight + 'px';
      }
    });
  });

  // ==========================================
  // SIMULATOR INTERACTIVE WIDGET DELEGATION
  // ==========================================
  if (simWebContent) {
    // 1. Inputs (Before-After Slider dragging)
    simWebContent.addEventListener('input', (e) => {
      const range = e.target.closest('.sim-ba-range-slider');
      if (range) {
        const val = range.value;
        const widget = range.closest('.sim-before-after-widget');
        const afterImg = widget.querySelector('.sim-ba-after');
        const divider = widget.querySelector('.sim-ba-divider');
        const handle = widget.querySelector('.sim-ba-handle');
        if (afterImg) afterImg.style.width = `${val}%`;
        if (divider) divider.style.left = `${val}%`;
        if (handle) handle.style.left = `${val}%`;
      }
    });

    // 2. Change events (Risk calculator checkboxes)
    simWebContent.addEventListener('change', (e) => {
      const check = e.target.closest('.sim-risk-check');
      if (check) {
        const widget = check.closest('.sim-pest-risk-calculator');
        const checks = widget.querySelectorAll('.sim-risk-check');
        let score = 25; // Base risk score
        checks.forEach(c => {
          if (c.checked) {
            score += parseInt(c.value);
          }
        });
        const badge = widget.querySelector('#sim-risk-score');
        if (badge) {
          badge.textContent = score <= 30 ? `Low Risk (${score}%)` : score <= 55 ? `Medium Risk (${score}%)` : `High Risk (${score}%)`;
          badge.className = 'sim-risk-score-badge ' + (score <= 30 ? 'low' : score <= 55 ? 'med' : 'high');
        }
      }
    });

    // 3. Click events (Cafe add, Cafe Checkout, Pest tabs, Pest active threat switch)
    simWebContent.addEventListener('click', (e) => {
      // Cafe Add to Order
      const cafeAddBtn = e.target.closest('.sim-cafe-add-btn');
      if (cafeAddBtn) {
        cafeCartCount++;
        renderSimulatedWebsite();
        return;
      }

      // Cafe Checkout Transmit
      const cafeCheckoutBtn = e.target.closest('.sim-cafe-checkout-btn');
      if (cafeCheckoutBtn) {
        const parent = cafeCheckoutBtn.closest('.sim-cafe-floating-checkout');
        parent.innerHTML = "<p><i data-lucide='check-circle' style='width: 14px; height: 14px; display: inline-block; vertical-align: middle; margin-right: 4px; color: #22c55e;'></i> Order Sent to Barista!</p>";
        cafeCartCount = 0;
        
        const cartVal = simWebContent.querySelector('.sim-cart-val');
        if (cartVal) cartVal.textContent = '0';
        
        setTimeout(() => {
          renderSimulatedWebsite();
        }, 1800);
        return;
      }

      // Pest Portal Tabs Switcher
      const pestTabLink = e.target.closest('.sim-pest-side-link');
      if (pestTabLink) {
        activePestTab = pestTabLink.dataset.tab;
        renderSimulatedWebsite();
        return;
      }

      // Pest Threat buttons
      const threatBtn = e.target.closest('.sim-threat-btn');
      if (threatBtn) {
        const threats = simWebContent.querySelectorAll('.sim-threat-btn');
        threats.forEach(btn => btn.classList.remove('active'));
        threatBtn.classList.add('active');
        
        const type = threatBtn.dataset.type;
        const diagTitle = simWebContent.querySelector('.sim-diag-title');
        const diagDesc = simWebContent.querySelector('.sim-diag-desc');
        const diagPrice = simWebContent.querySelector('.sim-diag-price');
        
        if (type === 'spiders') {
          diagTitle.textContent = 'Active Selection: Spiders & Ants Treatment';
          diagDesc.textContent = 'Child-safe residual exterior and interior spray barrier. Targeted dusting in voids.';
          diagPrice.textContent = '$180';
        } else if (type === 'termites') {
          diagTitle.textContent = 'Active Selection: Termite Colony Elimination';
          diagDesc.textContent = 'Accredited sub-floor foaming barriers and perimeter soil matrix grid stations.';
          diagPrice.textContent = '$950';
        } else if (type === 'rodents') {
          diagTitle.textContent = 'Active Selection: Rodent Control & baiting';
          diagDesc.textContent = 'Safety locked structural feeding grid stations in cavity roof spaces and walls.';
          diagPrice.textContent = '$220';
        }
        return;
      }

      // Gym Inner Navigation Switcher
      const gymNavBtn = e.target.closest('[data-gym-page]');
      if (gymNavBtn) {
        gymActivePage = gymNavBtn.dataset.gymPage;
        renderSimulatedWebsite();
        return;
      }

      // Gym exercise rep checklist count
      const gymRowCheck = e.target.closest('.sim-gym-check');
      if (gymRowCheck) {
        const checks = simWebContent.querySelectorAll('.sim-gym-check');
        let count = 0;
        checks.forEach(c => {
          if (c.checked) count++;
        });
        gymCompletedWorkouts = count;
        renderSimulatedWebsite();
        return;
      }
    });
  }


  // ==========================================
  // INITIAL RUN
  // ==========================================
  switchView('home');

  if (window.lucide) {
    window.lucide.createIcons();
  }
});
