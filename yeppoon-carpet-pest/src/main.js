// Yeppoon Carpet & Pest Main JS

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


  // --- Booking Engine State & Logic ---
  const serviceBtns = document.querySelectorAll('.service-toggle-btn');
  const dayBtns = document.querySelectorAll('.day-btn');
  const timeBtns = document.querySelectorAll('.time-btn');

  const sumServicesEl = document.getElementById('sum-services');
  const sumScheduleEl = document.getElementById('sum-schedule');
  const sumTotalEl = document.getElementById('sum-total');
  const bookingNotesField = document.getElementById('e-booking-notes');

  let selectedServices = {
    carpet: { active: true, name: 'Carpet Steam Clean', cost: 160 },
    pest: { active: false, name: 'Eco Pest Shield', cost: 140 },
    tile: { active: false, name: 'Tile & Grout Scrub', cost: 190 },
    sofa: { active: false, name: 'Upholstery Refresh', cost: 120 }
  };

  let selectedDay = 'Monday';
  let selectedTime = 'Morning (8 AM - 12 PM)';

  function calculateBooking() {
    let total = 0;
    let serviceNames = [];

    // Sum service costs
    Object.keys(selectedServices).forEach(key => {
      if (selectedServices[key].active) {
        total += selectedServices[key].cost;
        serviceNames.push(selectedServices[key].name);
      }
    });

    // Handle no service case
    if (serviceNames.length === 0) {
      sumServicesEl.textContent = "None selected";
      sumTotalEl.textContent = "$0";
      bookingNotesField.value = "Please choose a service above.";
      return;
    }

    // Update displays
    sumServicesEl.textContent = serviceNames.join(', ');
    sumScheduleEl.textContent = `${selectedDay} (${selectedTime.split(' ')[0]})`;
    sumTotalEl.textContent = `$${total}`;

    // Update booking notes field
    bookingNotesField.value = `SERVICES: ${serviceNames.join(' + ')}\nSCHEDULE: ${selectedDay} at ${selectedTime}\nESTIMATED TOTAL: $${total}`;
  }

  // Handle service card toggles
  serviceBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const serviceKey = btn.dataset.service;
      const isActive = btn.classList.contains('active');

      if (isActive) {
        btn.classList.remove('active');
        selectedServices[serviceKey].active = false;
      } else {
        btn.classList.add('active');
        selectedServices[serviceKey].active = true;
      }

      calculateBooking();
    });
  });

  // Handle Day selector
  dayBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      // Ignore click if fully booked
      if (btn.querySelector('.day-slots').textContent === 'Fully Booked') {
        return;
      }

      dayBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      selectedDay = btn.dataset.day;

      calculateBooking();
    });
  });

  // Handle Time selector
  timeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      timeBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      selectedTime = btn.dataset.time;

      calculateBooking();
    });
  });

  // Run initial scheduler state
  calculateBooking();

  // Handle "Confirm Details" btn
  const confirmBtn = document.getElementById('confirm-engine-details');
  confirmBtn.addEventListener('click', () => {
    // Scroll automatically to form
    const formElement = document.getElementById('contact');
    formElement.scrollIntoView({ behavior: 'smooth' });
  });


  // --- Booking Form Submit handling ---
  const bookingForm = document.getElementById('engine-contact-form');
  const successAlert = document.getElementById('engine-success');

  bookingForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const submitBtn = document.getElementById('btn-submit-engine');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Locking In Reservation Details...';

    setTimeout(() => {
      submitBtn.textContent = 'Slot Confirmed!';
      successAlert.classList.remove('hidden');
      bookingForm.reset();

      // Reset widgets
      serviceBtns.forEach(btn => btn.classList.remove('active'));
      // Keep default carpet active
      document.querySelector('[data-service="carpet"]').classList.add('active');
      Object.keys(selectedServices).forEach(k => selectedServices[k].active = (k === 'carpet'));

      dayBtns.forEach(btn => btn.classList.remove('active'));
      document.querySelector('[data-day="Monday"]').classList.add('active');
      selectedDay = 'Monday';

      timeBtns.forEach(btn => btn.classList.remove('active'));
      document.querySelector('.time-btn').classList.add('active');
      selectedTime = 'Morning (8 AM - 12 PM)';

      calculateBooking();

      setTimeout(() => {
        successAlert.classList.add('hidden');
        submitBtn.disabled = false;
        submitBtn.textContent = 'Submit Booking Slot';
      }, 8000);
    }, 1500);
  });
});
