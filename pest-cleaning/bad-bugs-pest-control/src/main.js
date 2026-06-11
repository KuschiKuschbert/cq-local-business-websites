import './style.css';
// Bad Bugs Pest Control Main JS

document.addEventListener('DOMContentLoaded', () => {
  // --- Mobile Menu Toggle ---
  const mobileToggle = document.getElementById('mobile-toggle');
  const navMenu = document.getElementById('nav-menu');
  
  mobileToggle.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    // Basic lines animation
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


  // --- Sector Selection Handlers ---
  const sectorButtons = document.querySelectorAll('.sector-cta');
  const propertyDropdown = document.getElementById('c-type');

  sectorButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const sector = btn.dataset.sector;
      if (sector) {
        propertyDropdown.value = sector;
      }
    });
  });


  // --- Interactive Bug Identifier Logic ---
  const bugItems = document.querySelectorAll('.bug-check-item');
  const panelHeadline = document.getElementById('panel-headline');
  const panelDescription = document.getElementById('panel-description');
  const gaugeFill = document.getElementById('gauge-fill');
  const meterLevelText = document.getElementById('meter-level-text');
  const statusCard = document.getElementById('status-card');
  const panelAction = document.getElementById('panel-action');
  const panelCtaBtn = document.getElementById('panel-cta-btn');

  // We will configure the SVG gauge arc length
  // Circumference of our gauge path (approx) = ~251px
  // Dasharray: 251, Dashoffset: 251 (empty) -> 0 (full)
  gaugeFill.style.strokeDasharray = "251";
  gaugeFill.style.strokeDashoffset = "251"; // Start empty

  // Map levels to stroke offsets and colors
  const gaugeConfig = {
    zero: { offset: 251, color: '#222222', text: 'ZERO DETECTED' },
    low: { offset: 200, color: '#00c853', text: 'LOW RISK' },
    medium: { offset: 150, color: '#ffd600', text: 'MODERATE RISK' },
    high: { offset: 90, color: '#ff6d00', text: 'HIGH RISK' },
    critical: { offset: 20, color: '#d50000', text: 'SEVERE DANGER' }
  };

  let selectedBugName = "";

  bugItems.forEach(item => {
    item.addEventListener('click', () => {
      // Toggle active states
      const isActive = item.classList.contains('active');
      
      bugItems.forEach(i => i.classList.remove('active'));
      
      if (!isActive) {
        item.classList.add('active');
        
        // Read data attributes
        const bugKey = item.dataset.bug;
        const riskLevel = item.dataset.risk; // low, medium, high, critical
        const dangerDesc = item.dataset.danger;
        const name = item.querySelector('h4').textContent;
        selectedBugName = name;

        // Update Gauge
        const config = gaugeConfig[riskLevel] || gaugeConfig.zero;
        gaugeFill.style.strokeDashoffset = config.offset;
        gaugeFill.style.stroke = config.color;
        meterLevelText.textContent = config.text;
        meterLevelText.style.color = config.color;

        // Update details text
        panelHeadline.textContent = name;
        panelDescription.textContent = dangerDesc;

        // Adjust Card Styling based on risk
        statusCard.classList.add('alert-active');
        panelAction.classList.remove('hidden');

        // Setup CTA custom response details
        panelCtaBtn.textContent = `Eradicate ${name} Now`;
        
      } else {
        // Reset to default
        resetGauge();
      }
    });
  });

  function resetGauge() {
    gaugeFill.style.strokeDashoffset = "251";
    gaugeFill.style.stroke = "#222222";
    meterLevelText.textContent = "ZERO DETECTED";
    meterLevelText.style.color = "var(--gray-light)";
    
    panelHeadline.textContent = "Select a pest to inspect risk";
    panelDescription.textContent = "Ticks/check items on the left to see localized danger alerts and mitigation strategies.";
    
    statusCard.classList.remove('alert-active');
    panelAction.classList.add('hidden');
    selectedBugName = "";
  }

  // Pre-fill contact form on click of warning panel button
  panelCtaBtn.addEventListener('click', () => {
    if (selectedBugName) {
      const msgField = document.getElementById('c-message');
      msgField.value = `INSPECTION REQUESTED: Urgent control needed for ${selectedBugName} spotted at this location. Please call back immediately.`;
    }
  });


  // --- Contact Form Submission Handling ---
  const contactForm = document.getElementById('contact-form');
  const successAlert = document.getElementById('contact-success');

  contactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const submitBtn = document.getElementById('btn-submit-contact');
    submitBtn.disabled = true;
    submitBtn.textContent = 'TRANSMITTING ROUTE DATA...';

    setTimeout(() => {
      submitBtn.textContent = 'DEPLOYED';
      successAlert.classList.remove('hidden');
      contactForm.reset();
      resetGauge();

      setTimeout(() => {
        successAlert.classList.add('hidden');
        submitBtn.disabled = false;
        submitBtn.textContent = 'Deploy Response Team';
      }, 8000);
    }, 1500);
  });
});
