import './style.css';

// --- Menu Data ---
const MENU_ITEMS = [
  // Corporate Lunch Collection
  {
    id: 'corp-1',
    name: 'Executive Bento Box',
    category: 'corporate',
    price: '$24.50',
    description: 'Teriyaki glazed salmon, wild rice, sesame crunch greens, house pickled ginger, and dynamic edamame salad.',
    serving: 'Per Box',
    dietary: ['GF', 'DF'],
    gradientClass: 'card-grad-1'
  },
  {
    id: 'corp-2',
    name: 'Artisanal Flatbread Platter',
    category: 'corporate',
    price: '$18.00',
    description: 'Assorted stone-baked flatbreads with beetroot hummus, roasted artichokes, and marinated feta cheese.',
    serving: 'Min. 10 Guests',
    dietary: ['V'],
    gradientClass: 'card-grad-2'
  },
  {
    id: 'corp-3',
    name: 'Harvest Wellness Bowl',
    category: 'corporate',
    price: '$16.50',
    description: 'Organic red quinoa, maple roasted sweet potatoes, avocado fan, edamame, and tahini-ginger emulsion.',
    serving: 'Per Bowl',
    dietary: ['VG', 'GF', 'DF'],
    gradientClass: 'card-grad-3'
  },
  
  // Conference Buffet Collection
  {
    id: 'buffet-1',
    name: 'Coastal Harvest Buffet',
    category: 'buffet',
    price: '$45.00',
    description: 'Pan-seared local sea bass, grass-fed chargrilled strip loin, seasonal root vegetables, citrus rocket salad.',
    serving: 'Per Guest',
    dietary: ['GF'],
    gradientClass: 'card-grad-4'
  },
  {
    id: 'buffet-2',
    name: 'Mediterranean Table',
    category: 'buffet',
    price: '$38.50',
    description: 'Slow-roasted lemon herb chicken, house-made falafel, traditional village salad, saffron rice, pita and tzatziki.',
    serving: 'Per Guest',
    dietary: [],
    gradientClass: 'card-grad-5'
  },
  {
    id: 'buffet-3',
    name: 'Plant-Based Feast',
    category: 'buffet',
    price: '$42.00',
    description: 'Charred cauliflower steak, wild forest mushroom risotto, grilled asparagus spears, artisanal dairy-free tarts.',
    serving: 'Per Guest',
    dietary: ['VG', 'GF'],
    gradientClass: 'card-grad-6'
  },
  
  // Wedding Canapé Collection
  {
    id: 'wedding-1',
    name: 'Truffled Beef Tartare',
    category: 'wedding',
    price: '$6.50',
    description: 'Hand-cut premium tenderloin, black truffle aioli, crispy capers, micro greens on toasted sourdough round.',
    serving: 'Per Piece',
    dietary: [],
    gradientClass: 'card-grad-1'
  },
  {
    id: 'wedding-2',
    name: 'Citrus Cured Kingfish',
    category: 'wedding',
    price: '$7.00',
    description: 'Local kingfish, finger lime caviar, avocado cream, pickled radish on a sesame wonton crisp.',
    serving: 'Per Piece',
    dietary: ['DF'],
    gradientClass: 'card-grad-2'
  },
  {
    id: 'wedding-3',
    name: 'Wild Mushroom Arancini',
    category: 'wedding',
    price: '$5.50',
    description: 'Crisp arborio rice, wild forest mushrooms, fontina core, truffle dust, fried sage leaf.',
    serving: 'Per Piece',
    dietary: ['V'],
    gradientClass: 'card-grad-6'
  }
];

// --- DOM References ---
const menuGrid = document.querySelector('#menu-items-grid');
const filterButtons = document.querySelectorAll('.filter-btn');
const header = document.querySelector('#header');
const mobileMenuBtn = document.querySelector('#mobile-menu-btn');
const mobileOverlay = document.querySelector('#mobile-overlay');
const mobileLinks = document.querySelectorAll('.mobile-nav-link');

const bookingForm = document.querySelector('#booking-request-form');
const successCard = document.querySelector('#booking-success');
const resetFormBtn = document.querySelector('#btn-reset-form');

// --- Initialization ---
document.addEventListener('DOMContentLoaded', () => {
  renderMenuItems('all');
  initHeaderScroll();
  initMobileNav();
  initMenuFilters();
  initBookingForm();
});

// --- Menu Rendering & Filtering ---
function renderMenuItems(filter = 'all') {
  if (!menuGrid) return;
  
  // Clear grid
  menuGrid.innerHTML = '';
  
  // Filter items
  const filteredItems = filter === 'all' 
    ? MENU_ITEMS 
    : MENU_ITEMS.filter(item => item.category === filter);
    
  // Build and insert HTML
  filteredItems.forEach(item => {
    const cardHtml = `
      <div class="menu-item-card" data-category="${item.category}" id="menu-item-${item.id}">
        <div class="menu-item-image ${item.gradientClass}">
          <span class="menu-item-price">${item.price}</span>
          <span class="menu-item-badge">${item.category}</span>
        </div>
        <div class="menu-item-info">
          <h3 class="menu-item-name">${item.name}</h3>
          <p class="menu-item-desc">${item.description}</p>
          <div class="menu-item-meta">
            <div class="menu-item-diet">
              ${item.dietary.map(diet => `
                <span class="diet-tag ${diet.toLowerCase() === 'gf' ? 'gf' : diet.toLowerCase() === 'v' ? 'v' : 'vg'}">
                  ${diet}
                </span>
              `).join('')}
            </div>
            <span class="menu-item-serving">${item.serving}</span>
          </div>
        </div>
      </div>
    `;
    menuGrid.insertAdjacentHTML('beforeend', cardHtml);
  });
}

function initMenuFilters() {
  filterButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      // Toggle active states
      filterButtons.forEach(b => {
        b.classList.remove('active');
        b.setAttribute('aria-selected', 'false');
      });
      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');
      
      const filterValue = btn.getAttribute('data-filter');
      
      // Animate grid out and in
      if (menuGrid) {
        menuGrid.style.opacity = '0';
        setTimeout(() => {
          renderMenuItems(filterValue);
          menuGrid.style.opacity = '1';
        }, 200);
      }
    });
  });
}

// --- Navigation Scroll Effect ---
function initHeaderScroll() {
  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  });
}

// --- Mobile Navigation ---
function initMobileNav() {
  if (!mobileMenuBtn || !mobileOverlay) return;

  mobileMenuBtn.addEventListener('click', () => {
    const isExpanded = mobileMenuBtn.getAttribute('aria-expanded') === 'true';
    mobileMenuBtn.setAttribute('aria-expanded', !isExpanded);
    mobileMenuBtn.classList.toggle('active');
    mobileOverlay.classList.toggle('active');
    document.body.style.overflow = isExpanded ? '' : 'hidden'; // Lock scrolling
  });

  // Close menu when links are clicked
  mobileLinks.forEach(link => {
    link.addEventListener('click', () => {
      mobileMenuBtn.setAttribute('aria-expanded', 'false');
      mobileMenuBtn.classList.remove('active');
      mobileOverlay.classList.remove('active');
      document.body.style.overflow = '';
    });
  });
}

// --- Booking Form Handling & Validation ---
function initBookingForm() {
  if (!bookingForm) return;

  bookingForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    if (validateForm()) {
      const submitBtn = document.querySelector('#btn-submit-booking');
      submitBtn.classList.add('loading');
      
      // Extract data
      const formData = new FormData(bookingForm);
      const name = formData.get('name');
      const email = formData.get('email');
      const eventType = formData.get('eventType');
      const guestCount = formData.get('guestCount');
      
      // Format Event Type Label
      let eventTypeLabel = 'Custom Gathering';
      if (eventType === 'corporate') eventTypeLabel = 'Corporate Lunch';
      if (eventType === 'buffet') eventTypeLabel = 'Conference Buffet';
      if (eventType === 'wedding') eventTypeLabel = 'Wedding Canapés';
      
      // Simulate API submission delay
      setTimeout(() => {
        submitBtn.classList.remove('loading');
        
        // Show Success card
        bookingForm.classList.add('hidden');
        successCard.classList.add('active');
        
        // Populate Summary details
        document.querySelector('#summary-ref').textContent = `EVO-${Math.floor(10000 + Math.random() * 90000)}`;
        document.querySelector('#summary-email').textContent = email;
        document.querySelector('#summary-type').textContent = eventTypeLabel;
        document.querySelector('#summary-guests').textContent = `${guestCount} guests`;
      }, 1500);
    }
  });

  if (resetFormBtn) {
    resetFormBtn.addEventListener('click', () => {
      bookingForm.reset();
      successCard.classList.remove('active');
      bookingForm.classList.remove('hidden');
      
      // Clear validation marks
      const groups = bookingForm.querySelectorAll('.form-group');
      groups.forEach(g => g.classList.remove('invalid'));
    });
  }
}

function validateForm() {
  let isValid = true;
  
  // Fields
  const nameInput = document.querySelector('#client-name');
  const emailInput = document.querySelector('#client-email');
  const eventSelect = document.querySelector('#event-type');
  const dateInput = document.querySelector('#event-date');
  const guestsInput = document.querySelector('#guest-count');
  
  // Reset
  const groups = bookingForm.querySelectorAll('.form-group');
  groups.forEach(g => g.classList.remove('invalid'));
  
  // Validation checks
  if (!nameInput.value.trim()) {
    showError(nameInput, 'name-error');
    isValid = false;
  }
  
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailInput.value.trim() || !emailRegex.test(emailInput.value)) {
    showError(emailInput, 'email-error');
    isValid = false;
  }
  
  if (!eventSelect.value) {
    showError(eventSelect, 'event-error');
    isValid = false;
  }
  
  if (!dateInput.value) {
    showError(dateInput, 'date-error');
    isValid = false;
  }
  
  const guestVal = parseInt(guestsInput.value, 10);
  if (isNaN(guestVal) || guestVal < 10) {
    showError(guestsInput, 'guests-error');
    isValid = false;
  }
  
  return isValid;
}

function showError(inputElement, errorId) {
  const group = inputElement.closest('.form-group');
  if (group) {
    group.classList.add('invalid');
  }
}
