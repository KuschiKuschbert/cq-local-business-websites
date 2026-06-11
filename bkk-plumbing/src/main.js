// BKK Plumbing Interactive Logic
document.getElementById('booking-form').addEventListener('submit', function(e) {
  e.preventDefault();
  const formSuccess = document.getElementById('form-success');
  formSuccess.classList.remove('visually-hidden');
  
  // Reset form inputs after booking request submission simulation
  e.target.reset();
  
  setTimeout(() => {
    formSuccess.classList.add('visually-hidden');
  }, 6000);
});
