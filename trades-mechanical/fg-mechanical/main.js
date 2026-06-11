import './style.css'

document.getElementById('year').textContent = new Date().getFullYear();

document.getElementById('bookingForm').addEventListener('submit', (e) => {
  e.preventDefault();
  
  const btn = e.target.querySelector('button');
  const originalText = btn.textContent;
  
  btn.textContent = 'Booking...';
  btn.style.backgroundColor = 'var(--accent-red-hover)';
  
  // Simulate API call
  setTimeout(() => {
    btn.textContent = 'Service Booked!';
    btn.style.backgroundColor = '#4CAF50'; // Green success
    e.target.reset();
    
    setTimeout(() => {
      btn.textContent = originalText;
      btn.style.backgroundColor = '';
    }, 3000);
  }, 1500);
});
