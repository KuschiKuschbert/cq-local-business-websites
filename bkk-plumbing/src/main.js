// BKK Plumbing Interactive Logic

document.addEventListener('DOMContentLoaded', () => {
  // Booking Form Submission & Success Overlay
  const bookingForm = document.getElementById('booking-form');
  const formSuccess = document.getElementById('form-success');
  const btnSuccessClose = document.getElementById('btn-success-close');

  if (bookingForm && formSuccess) {
    bookingForm.addEventListener('submit', (e) => {
      e.preventDefault();
      // Show overlay
      formSuccess.classList.add('active');
      bookingForm.reset();
    });
  }

  if (btnSuccessClose && formSuccess) {
    btnSuccessClose.addEventListener('click', () => {
      formSuccess.classList.remove('active');
    });
  }

  // Cost Estimator Wizard Logic
  const estimatorTask = document.getElementById('estimator-task');
  const locationButtons = document.querySelectorAll('.loc-btn');
  const previewTask = document.getElementById('preview-task');
  const previewLocation = document.getElementById('preview-location');
  const previewTotalCost = document.getElementById('preview-total-cost');
  const btnEstimatorBook = document.getElementById('btn-estimator-book');
  const serviceSelect = document.getElementById('service');

  let selectedTaskName = "Burst Pipe / Leak";
  let selectedLocationName = "Rockhampton Local ($99)";
  let activeDispatchFee = 99;

  function updateEstimator() {
    if (estimatorTask && previewTask && previewLocation && previewTotalCost) {
      // Get task details
      const selectedOption = estimatorTask.options[estimatorTask.selectedIndex];
      selectedTaskName = selectedOption.text.split(' / ')[0];
      
      // Update preview text
      previewTask.textContent = selectedTaskName;
      previewLocation.textContent = selectedLocationName;
      
      // Calculate total dispatch cost (Base dispatch fee only)
      previewTotalCost.textContent = `$${activeDispatchFee.toFixed(2)}`;
    }
  }

  // Bind Task Select Change
  if (estimatorTask) {
    estimatorTask.addEventListener('change', () => {
      updateEstimator();
      
      // Automatically sync select task to the actual booking form dropdown below
      if (serviceSelect) {
        serviceSelect.value = estimatorTask.value;
      }
    });
  }

  // Bind Location Button Clicks
  locationButtons.forEach(button => {
    button.addEventListener('click', () => {
      // Toggle active state
      locationButtons.forEach(btn => btn.classList.remove('active'));
      button.classList.add('active');
      
      // Get fee & name
      activeDispatchFee = parseFloat(button.getAttribute('data-fee'));
      selectedLocationName = button.textContent;
      
      updateEstimator();
    });
  });

  // Proceed Button Scroll & Sync
  if (btnEstimatorBook) {
    btnEstimatorBook.addEventListener('click', (e) => {
      // Smooth scroll is handled via CSS, but let's sync select options
      if (serviceSelect && estimatorTask) {
        serviceSelect.value = estimatorTask.value;
      }
    });
  }

  // Run initial calculations
  updateEstimator();
});
