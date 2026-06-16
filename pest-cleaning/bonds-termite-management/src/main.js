import './mobile-ux.js';
import './style.css';
// Bonds Termite Management Main JS

document.addEventListener('DOMContentLoaded', () => {
  // --- Mobile Menu Toggle ---
  const mobileToggle = document.getElementById('mobile-toggle');
  const navMenu = document.getElementById('nav-menu');
  
  mobileToggle.addEventListener('click', () => {
    navMenu.classList.toggle('active');
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


  // --- Risk Assessment Logic ---
  const optButtons = document.querySelectorAll('.risk-opt-btn');
  const riskScoreVal = document.getElementById('risk-score-value');
  const riskMeterFill = document.getElementById('meter-fill');
  const riskRatingBadge = document.getElementById('risk-rating-badge');
  const verdictHeadline = document.getElementById('verdict-headline');
  const verdictDescription = document.getElementById('verdict-description');
  const recommendedSystemEl = document.getElementById('recommended-system');
  const riskCard = document.getElementById('risk-result-card');
  const systemDropdown = document.getElementById('t-system');

  let riskFactors = {
    age: 1, // default "new"
    soil: 2, // default "sand"
    history: 1 // default "none"
  };

  function calculateRisk() {
    const totalScore = riskFactors.age + riskFactors.soil + riskFactors.history;
    riskScoreVal.textContent = totalScore;

    // Fill percent width
    const fillPercent = Math.min((totalScore / 16) * 100, 100);
    riskMeterFill.style.width = `${fillPercent}%`;

    // Reset alert classes
    riskCard.className = "status-card";

    let rating = "LOW RISK";
    let system = "Annual Thermal Radar Inspection";
    let headline = "Standard Precaution Advisory";
    let desc = "Your home has a lower risk index. However, yearly thermal inspections are still recommended under Australian standard guidelines.";

    if (totalScore >= 11) {
      rating = "SEVERE THREAT";
      riskCard.classList.add('severe-alert');
      system = "Termidor Chemical Trench Barrier";
      headline = "URGENT Containment Required";
      desc = "Your structure shows heavy susceptibility. Active neighboring history or aged timbers pose immediate danger. We recommend installing an active chemical barrier.";
    } else if (totalScore >= 6) {
      rating = "ELEVATED RISK";
      riskCard.classList.add('elevated-alert');
      system = "Sentricon AlwaysActive Baiting Network";
      headline = "Protective Guarding Recommended";
      desc = "Vulnerability parameters are high. Placing subterranean bait monitoring stations is highly suggested to capture termite migration trends around boundaries.";
    }

    riskRatingBadge.textContent = rating;
    recommendedSystemEl.textContent = system;
    verdictHeadline.textContent = headline;
    verdictDescription.textContent = desc;

    // Update Form system readout if custom
    if (systemDropdown.value.startsWith('Risk Assessment')) {
      systemDropdown.value = `Risk: ${rating} (${system})`;
    }
  }

  // Handle assessment buttons
  optButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const groupName = btn.dataset.group;
      const points = parseInt(btn.dataset.points);

      // Deselect siblings in group
      document.querySelectorAll(`[data-group="${groupName}"]`).forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      riskFactors[groupName] = points;
      calculateRisk();
    });
  });

  // Run initial calculation
  calculateRisk();

  // "Book Assessment" button action
  const claimAssessmentBtn = document.getElementById('claim-assessment-btn');
  claimAssessmentBtn.addEventListener('click', () => {
    const rating = riskRatingBadge.textContent;
    const recommendedSystem = recommendedSystemEl.textContent;
    systemDropdown.value = `Risk: ${rating} (${recommendedSystem})`;

    const notes = document.getElementById('t-notes');
    notes.value = `Hi, I ran the online assessment tool.\nScore: ${riskScoreVal.textContent}/16 (${rating}).\nRecommended Defense: ${recommendedSystem}. Please deploy inspectors to certify local soil conditions.`;
  });

  // Handle select system on pricing grid
  const barrierSelectBtns = document.querySelectorAll('.barrier-select-btn');
  barrierSelectBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const systemName = btn.dataset.system;
      if (systemName) {
        systemDropdown.value = systemName;
        const notes = document.getElementById('t-notes');
        notes.value = `Hi, I would like to request a quotation package for the ${systemName} barrier network. Please call me back.`;
      }
    });
  });


  // --- Form Submission Handling ---
  const termiteForm = document.getElementById('termite-form');
  const successAlert = document.getElementById('termite-success');

  termiteForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const submitBtn = document.getElementById('btn-submit-termite');
    submitBtn.disabled = true;
    submitBtn.textContent = 'ALLOCATING CERTIFIED SURVEYORS...';

    setTimeout(() => {
      submitBtn.textContent = 'SURVEY SCHEDULED';
      successAlert.classList.remove('hidden');
      termiteForm.reset();

      // Reset options
      optButtons.forEach(b => b.classList.remove('active'));
      document.querySelector('[data-group="age"][data-value="new"]').classList.add('active');
      document.querySelector('[data-group="soil"][data-value="sand"]').classList.add('active');
      document.querySelector('[data-group="history"][data-value="none"]').classList.add('active');

      riskFactors = { age: 1, soil: 2, history: 1 };
      calculateRisk();

      setTimeout(() => {
        successAlert.classList.add('hidden');
        submitBtn.disabled = false;
        submitBtn.textContent = 'Deploy Structural Inspectors';
      }, 8000);
    }, 1500);
  });
});
