// Grant Goltz Plumbing Tab & Booking Logic
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    
    btn.classList.add('active');
    const tabId = btn.getAttribute('data-tab');
    document.getElementById(tabId).classList.add('active');
  });
});

document.getElementById('contact-form').addEventListener('submit', function(e) {
  e.preventDefault();
  const alert = document.getElementById('contact-success');
  alert.classList.remove('visually-hidden');
  e.target.reset();
  setTimeout(() => {
    alert.classList.add('visually-hidden');
  }, 5000);
});
