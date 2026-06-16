import './mobile-ux.js';
import './style.css';
// Truflow Plumbing JS
document.getElementById('truflow-form').addEventListener('submit', function(e) {
  e.preventDefault();
  const alert = document.getElementById('truflow-success');
  alert.classList.remove('visually-hidden');
  e.target.reset();
  setTimeout(() => {
    alert.classList.add('visually-hidden');
  }, 6000);
});
