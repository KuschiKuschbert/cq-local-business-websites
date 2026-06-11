import './style.css';

// State Management
const state = {
  cake: {
    tiers: 3,
    sponge: 'vanilla',
    filling: 'champagne',
    topping: 'gold-leaf',
    price: 480
  },
  donut: {
    base: 'classic',
    frosting: 'blush',
    topping: 'rainbow'
  },
  enquiryItems: []
};

// Color mappings for SVGs
const colors = {
  sponge: {
    vanilla: '#fffbeb',
    chocolate: '#4c1d95',
    raspberry: '#fda4af',
    lemon: '#fef08a'
  },
  filling: {
    champagne: '#fef3c7',
    caramel: '#b45309',
    passionfruit: '#fbbf24',
    rose: '#fecdd3'
  },
  donutBase: {
    classic: '#e89c31',
    chocolate: '#3b1807',
    'red-velvet': '#881337'
  },
  donutFrosting: {
    blush: '#fda4af',
    'white-choc': '#fffdf5',
    'gold-honey': '#fbbf24'
  }
};

/* ----------------------------------------------------
   DONUT VISUALIZER LOGIC
   ---------------------------------------------------- */
function initDonutVisualizer() {
  const baseButtons = document.querySelectorAll('#donut-base-options .pill-btn');
  const frostingButtons = document.querySelectorAll('#donut-frosting-options .pill-btn');
  const toppingButtons = document.querySelectorAll('#donut-topping-options .pill-btn');
  
  baseButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      baseButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.donut.base = btn.dataset.value;
      updateDonutSVG();
    });
  });

  frostingButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      frostingButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.donut.frosting = btn.dataset.value;
      updateDonutSVG();
    });
  });

  toppingButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      toppingButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.donut.topping = btn.dataset.value;
      updateDonutSVG();
    });
  });

  // Run initial draw
  updateDonutSVG();
}

function updateDonutSVG() {
  const baseEl = document.getElementById('donut-base');
  const frostingEl = document.getElementById('donut-frosting');
  const toppingsGroup = document.getElementById('donut-toppings-group');

  if (baseEl) baseEl.setAttribute('fill', colors.donutBase[state.donut.base]);
  if (frostingEl) frostingEl.setAttribute('fill', colors.donutFrosting[state.donut.frosting]);

  if (toppingsGroup) {
    toppingsGroup.innerHTML = ''; // Clear previous toppings

    if (state.donut.topping === 'rainbow') {
      // Draw pastel color sprinkles
      const colorsList = ['#f43f5e', '#fbbf24', '#60a5fa', '#34d399', '#ffffff'];
      const paths = [
        'M 65 90 Q 68 90 70 91',
        'M 135 95 Q 138 98 139 100',
        'M 100 85 Q 103 84 105 86',
        'M 80 120 Q 83 122 85 121',
        'M 120 115 Q 121 113 123 112',
        'M 55 105 Q 58 107 60 106',
        'M 145 110 Q 148 108 149 109',
        'M 85 98 Q 87 96 89 97',
        'M 115 98 Q 117 96 119 97'
      ];
      
      paths.forEach((d, i) => {
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', d);
        path.setAttribute('stroke', colorsList[i % colorsList.length]);
        path.setAttribute('stroke-width', '4');
        path.setAttribute('stroke-linecap', 'round');
        path.setAttribute('fill', 'none');
        toppingsGroup.appendChild(path);
      });
    } else if (state.donut.topping === 'gold-leaf') {
      // Draw organic metallic gold flecks
      const flecks = [
        { cx: 70, cy: 95, rx: 6, ry: 3, rot: 15 },
        { cx: 125, cy: 90, rx: 8, ry: 4, rot: -20 },
        { cx: 90, cy: 118, rx: 5, ry: 2.5, rot: 45 },
        { cx: 135, cy: 110, rx: 6, ry: 3, rot: -10 }
      ];
      
      flecks.forEach(f => {
        const ellipse = document.createElementNS('http://www.w3.org/2000/svg', 'ellipse');
        ellipse.setAttribute('cx', f.cx.toString());
        ellipse.setAttribute('cy', f.cy.toString());
        ellipse.setAttribute('rx', f.rx.toString());
        ellipse.setAttribute('ry', f.ry.toString());
        ellipse.setAttribute('transform', `rotate(${f.rot} ${f.cx} ${f.cy})`);
        ellipse.setAttribute('fill', 'url(#gold-grad)');
        toppingsGroup.appendChild(ellipse);
      });
    } else if (state.donut.topping === 'pearls') {
      // Draw white/blush round sugar pearls
      const pearls = [
        { cx: 62, cy: 98, r: 3.5 },
        { cx: 138, cy: 94, r: 3.5 },
        { cx: 95, cy: 82, r: 4 },
        { cx: 80, cy: 115, r: 3 },
        { cx: 122, cy: 118, r: 4.5 },
        { cx: 110, cy: 122, r: 3 }
      ];
      
      pearls.forEach(p => {
        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circle.setAttribute('cx', p.cx.toString());
        circle.setAttribute('cy', p.cy.toString());
        circle.setAttribute('r', p.r.toString());
        circle.setAttribute('fill', '#ffffff');
        circle.setAttribute('stroke', '#fda4af');
        circle.setAttribute('stroke-width', '1');
        toppingsGroup.appendChild(circle);
      });
    }
  }
}

/* ----------------------------------------------------
   CAKE VISUALIZER LOGIC
   ---------------------------------------------------- */
function initCakeVisualizer() {
  const tierCards = document.querySelectorAll('#cake-tiers-select .selector-card');
  const spongeCards = document.querySelectorAll('#cake-sponge-select .selector-card');
  const fillingCards = document.querySelectorAll('#cake-filling-select .selector-card');
  const toppingCards = document.querySelectorAll('#cake-topping-select .selector-card');
  
  tierCards.forEach(card => {
    card.addEventListener('click', () => {
      tierCards.forEach(c => c.classList.remove('active'));
      card.classList.add('active');
      state.cake.tiers = parseInt(card.dataset.tiers);
      updateCakeVisuals();
    });
  });

  spongeCards.forEach(card => {
    card.addEventListener('click', () => {
      spongeCards.forEach(c => c.classList.remove('active'));
      card.classList.add('active');
      state.cake.sponge = card.dataset.sponge;
      updateCakeVisuals();
    });
  });

  fillingCards.forEach(card => {
    card.addEventListener('click', () => {
      fillingCards.forEach(c => c.classList.remove('active'));
      card.classList.add('active');
      state.cake.filling = card.dataset.filling;
      updateCakeVisuals();
    });
  });

  toppingCards.forEach(card => {
    card.addEventListener('click', () => {
      toppingCards.forEach(c => c.classList.remove('active'));
      card.classList.add('active');
      state.cake.topping = card.dataset.topping;
      updateCakeVisuals();
    });
  });

  document.getElementById('add-cake-to-inquiry-btn')?.addEventListener('click', () => {
    const cakeDesc = `Custom Cake: ${state.cake.tiers}-Tier (${state.cake.sponge} sponge, ${state.cake.filling} filling, with ${state.cake.topping})`;
    addEnquiryItem({
      id: 'custom-cake',
      name: cakeDesc,
      price: state.cake.price
    });
  });

  // Initial update
  updateCakeVisuals();
}

function updateCakeVisuals() {
  const tier1 = document.getElementById('cake-tier-1');
  const tier2 = document.getElementById('cake-tier-2');
  const tier3 = document.getElementById('cake-tier-3');
  const decorGroup = document.getElementById('cake-decorations');

  // Handle tier visibility and height adjustment
  if (state.cake.tiers === 3) {
    tier1.classList.remove('hidden-tier');
    tier2.classList.remove('hidden-tier');
    tier3.classList.remove('hidden-tier');
    tier1.style.transform = 'translateY(0)';
    tier2.style.transform = 'translateY(0)';
    tier3.style.transform = 'translateY(0)';
  } else if (state.cake.tiers === 2) {
    tier1.classList.remove('hidden-tier');
    tier2.classList.remove('hidden-tier');
    tier3.classList.add('hidden-tier');
    // Shift remaining two tiers down to look settled on stand
    tier2.style.transform = 'translateY(80px)';
    tier1.style.transform = 'translateY(80px)';
  } else if (state.cake.tiers === 1) {
    tier1.classList.remove('hidden-tier');
    tier2.classList.add('hidden-tier');
    tier3.classList.add('hidden-tier');
    // Shift top tier down to look settled on stand
    tier1.style.transform = 'translateY(165px)';
  }

  // Update sponge colors
  const spongeColor = colors.sponge[state.cake.sponge];
  const creamColor = colors.filling[state.cake.filling];

  // Base cake body can be sponge color, top ellipse is frosting/sponge interface
  const tier1Body = tier1.querySelector('.tier-body');
  const tier1Top = tier1.querySelector('.tier-top');
  const tier1Cream = tier1.querySelector('.tier-cream');

  const tier2Body = tier2.querySelector('.tier-body');
  const tier2Top = tier2.querySelector('.tier-top');
  const tier2Cream = tier2.querySelector('.tier-cream');

  const tier3Body = tier3.querySelector('.tier-body');
  const tier3Top = tier3.querySelector('.tier-top');
  const tier3Cream = tier3.querySelector('.tier-cream');

  // Set colors
  if (tier1Body) tier1Body.setAttribute('fill', spongeColor);
  if (tier1Top) tier1Top.setAttribute('fill', '#ffffff');
  if (tier1Cream) tier1Cream.setAttribute('fill', creamColor);

  if (tier2Body) tier2Body.setAttribute('fill', spongeColor);
  if (tier2Top) tier2Top.setAttribute('fill', '#ffffff');
  if (tier2Cream) tier2Cream.setAttribute('fill', creamColor);

  if (tier3Body) tier3Body.setAttribute('fill', spongeColor);
  if (tier3Top) tier3Top.setAttribute('fill', '#ffffff');
  if (tier3Cream) tier3Cream.setAttribute('fill', creamColor);

  // Render toppings decoration on the SVG
  if (decorGroup) {
    decorGroup.innerHTML = '';
    
    // Position helpers based on current tiers setup
    let topY = 90;
    let midY = 190;
    let bottomY = 290;
    
    if (state.cake.tiers === 2) {
      topY = 170; // tier 1 shifted
      midY = 270; // tier 2 shifted
    } else if (state.cake.tiers === 1) {
      topY = 255; // tier 1 shifted
    }

    if (state.cake.topping === 'gold-leaf') {
      // Golden drip paths or flecks
      const goldFleck = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      if (state.cake.tiers === 3) {
        goldFleck.setAttribute('d', `
          M 130 ${topY} L 140 ${topY+10} L 145 ${topY}
          M 110 ${midY} L 120 ${midY+15} L 125 ${midY+5}
          M 90 ${bottomY} L 105 ${bottomY+20} L 115 ${bottomY+10}
          M 210 ${topY} Q 220 ${topY+15} 225 ${topY}
        `);
      } else if (state.cake.tiers === 2) {
        goldFleck.setAttribute('d', `
          M 130 ${topY} L 140 ${topY+10} L 145 ${topY}
          M 110 ${midY} L 120 ${midY+15} L 125 ${midY+5}
        `);
      } else {
        goldFleck.setAttribute('d', `
          M 130 ${topY} L 140 ${topY+10} L 145 ${topY}
        `);
      }
      goldFleck.setAttribute('fill', 'none');
      goldFleck.setAttribute('stroke', 'url(#gold-grad)');
      goldFleck.setAttribute('stroke-width', '4');
      goldFleck.setAttribute('stroke-linecap', 'round');
      decorGroup.appendChild(goldFleck);
    } else if (state.cake.topping === 'flowers') {
      // Draw pastel flowers (using circles) at junctions
      const flowers = [];
      if (state.cake.tiers === 3) {
        flowers.push({ cx: 135, cy: topY, r: 8, fill: '#fda4af' });
        flowers.push({ cx: 112, cy: midY, r: 10, fill: '#fb7185' });
        flowers.push({ cx: 90, cy: bottomY, r: 12, fill: '#fda4af' });
        flowers.push({ cx: 238, cy: midY, r: 8, fill: '#fef08a' });
      } else if (state.cake.tiers === 2) {
        flowers.push({ cx: 135, cy: topY, r: 8, fill: '#fda4af' });
        flowers.push({ cx: 112, cy: midY, r: 10, fill: '#fb7185' });
      } else {
        flowers.push({ cx: 135, cy: topY, r: 10, fill: '#fda4af' });
        flowers.push({ cx: 215, cy: topY, r: 8, fill: '#fef08a' });
      }

      flowers.forEach(f => {
        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circle.setAttribute('cx', f.cx.toString());
        circle.setAttribute('cy', f.cy.toString());
        circle.setAttribute('r', f.r.toString());
        circle.setAttribute('fill', f.fill);
        circle.setAttribute('stroke', '#ffffff');
        circle.setAttribute('stroke-width', '2');
        decorGroup.appendChild(circle);

        // Core of flower
        const core = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        core.setAttribute('cx', f.cx.toString());
        core.setAttribute('cy', f.cy.toString());
        core.setAttribute('r', (f.r / 3).toString());
        core.setAttribute('fill', '#f59e0b');
        decorGroup.appendChild(core);
      });
    } else if (state.cake.topping === 'berries') {
      // Draw little berry clusters on cake top
      const berries = [
        { cx: 160, cy: topY - 2, r: 3, fill: '#be123c' },
        { cx: 165, cy: topY - 4, r: 4, fill: '#991b1b' },
        { cx: 172, cy: topY - 3, r: 3, fill: '#f43f5e' },
        { cx: 180, cy: topY - 5, r: 4.5, fill: '#be123c' }
      ];

      berries.forEach(b => {
        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circle.setAttribute('cx', b.cx.toString());
        circle.setAttribute('cy', b.cy.toString());
        circle.setAttribute('r', b.r.toString());
        circle.setAttribute('fill', b.fill);
        decorGroup.appendChild(circle);
      });
    }
  }

  // Calculate pricing
  let basePrice = 120; // 1 Tier
  if (state.cake.tiers === 2) basePrice = 270;
  if (state.cake.tiers === 3) basePrice = 410;

  // Add flavour additions
  let spongePremium = 0;
  if (state.cake.sponge === 'chocolate') spongePremium = 15;
  if (state.cake.sponge === 'raspberry') spongePremium = 25;
  if (state.cake.sponge === 'lemon') spongePremium = 20;

  let fillingPremium = 0;
  if (state.cake.filling === 'rose') fillingPremium = 20;
  if (state.cake.filling === 'caramel') fillingPremium = 15;
  if (state.cake.filling === 'passionfruit') fillingPremium = 10;

  let toppingPremium = 0;
  if (state.cake.topping === 'gold-leaf') toppingPremium = 35;
  if (state.cake.topping === 'flowers') toppingPremium = 25;
  if (state.cake.topping === 'berries') toppingPremium = 15;

  state.cake.price = basePrice + spongePremium + fillingPremium + toppingPremium;

  // Render price and details in text
  const priceTag = document.getElementById('cake-price-tag');
  const summaryText = document.getElementById('cake-summary-text');
  
  if (priceTag) priceTag.innerText = `$${state.cake.price}`;
  if (summaryText) {
    const spongeLabel = document.querySelector(`#cake-sponge-select [data-sponge="${state.cake.sponge}"] .selector-title`).innerText;
    const fillingLabel = document.querySelector(`#cake-filling-select [data-filling="${state.cake.filling}"] .selector-title`).innerText;
    const toppingLabel = document.querySelector(`#cake-topping-select [data-topping="${state.cake.topping}"] .selector-title`).innerText;
    summaryText.innerText = `${state.cake.tiers}-Tier cake designed with delicious ${spongeLabel} layers, gourmet ${fillingLabel} cream, decorated with luxury ${toppingLabel}.`;
  }
}

/* ----------------------------------------------------
   ENQUIRY SELECTION SYNC
   ---------------------------------------------------- */
function addEnquiryItem(item) {
  // If item already exists, remove it first to avoid duplicates
  state.enquiryItems = state.enquiryItems.filter(i => i.id !== item.id);
  state.enquiryItems.push(item);
  renderEnquirySummary();
}

function removeEnquiryItem(id) {
  state.enquiryItems = state.enquiryItems.filter(i => i.id !== id);
  renderEnquirySummary();
}

function renderEnquirySummary() {
  const listEl = document.getElementById('selected-items-list');
  if (!listEl) return;

  listEl.innerHTML = '';

  if (state.enquiryItems.length === 0) {
    listEl.innerHTML = '<li class="empty-notice">No custom items applied yet. Design a cake or select a package to auto-fill.</li>';
    return;
  }

  state.enquiryItems.forEach(item => {
    const li = document.createElement('li');
    li.innerHTML = `
      ${item.name} ($${item.price})
      <button class="remove-selection" data-id="${item.id}">Remove</button>
    `;
    listEl.appendChild(li);
  });

  // Bind remove buttons
  document.querySelectorAll('.remove-selection').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const id = btn.dataset.id;
      removeEnquiryItem(id);
    });
  });
}

function initEventHandlers() {
  // Package select buttons
  document.querySelectorAll('.select-package-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const packageName = btn.dataset.package;
      let price = 0;
      if (packageName.includes('Bridal Suite')) price = 650;
      if (packageName.includes('Showstopper')) price = 1250;
      if (packageName.includes('Soirée')) price = 380;

      addEnquiryItem({
        id: 'package',
        name: `Package: ${packageName}`,
        price: price
      });

      // Smooth scroll to inquiry form
      document.getElementById('inquiry')?.scrollIntoView({ behavior: 'smooth' });
    });
  });

  // Donut wall hire select buttons
  document.querySelectorAll('.select-wall-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const wallName = btn.dataset.wall;
      let price = 290;
      if (wallName.includes('Acrylic')) price = 450;

      addEnquiryItem({
        id: 'donut-wall',
        name: `Hire: ${wallName}`,
        price: price
      });

      // Smooth scroll to inquiry form
      document.getElementById('inquiry')?.scrollIntoView({ behavior: 'smooth' });
    });
  });

  // Inquiry Form Submission
  const form = document.getElementById('event-inquiry-form');
  const dialog = document.getElementById('success-dialog');
  const closeDialogBtn = document.getElementById('close-dialog-btn');
  const dialogSummaryEl = document.getElementById('dialog-submission-summary');

  if (form && dialog) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();

      // Collect form values
      const name = document.getElementById('client-name').value;
      const email = document.getElementById('client-email').value;
      const date = document.getElementById('event-date').value;
      const eventType = document.getElementById('event-type').value;

      // Build summary message
      let itemsSummary = '';
      if (state.enquiryItems.length > 0) {
        itemsSummary = 'Selections applied:<br>' + state.enquiryItems.map(item => `• ${item.name} ($${item.price})`).join('<br>');
      } else {
        itemsSummary = 'General Inquiry Request';
      }

      if (dialogSummaryEl) {
        dialogSummaryEl.innerHTML = `
          <strong>Aesthetic Proposal for:</strong> ${name}<br>
          <strong>Date:</strong> ${date} | <strong>Event:</strong> ${eventType}<br>
          <br>
          ${itemsSummary}
        `;
      }

      // Show native dialog (trigger native top layer animation style)
      dialog.showModal();

      // Clear the state/form
      form.reset();
      state.enquiryItems = [];
      renderEnquirySummary();
    });
  }

  if (closeDialogBtn && dialog) {
    closeDialogBtn.addEventListener('click', () => {
      dialog.close();
    });
  }
}

/* ----------------------------------------------------
   INIT APPLICATION
   ---------------------------------------------------- */
document.addEventListener('DOMContentLoaded', () => {
  initDonutVisualizer();
  initCakeVisualizer();
  initEventHandlers();
});

// For HMR / direct call in Vite where DOMContentLoaded might have already fired
if (document.readyState === 'interactive' || document.readyState === 'complete') {
  initDonutVisualizer();
  initCakeVisualizer();
  initEventHandlers();
}
