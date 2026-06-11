import './style.css';
// Mar-lin Call back Handler
document.getElementById('callback-form').addEventListener('submit', function(e) {
  e.preventDefault();
  const alert = document.getElementById('cb-success');
  alert.classList.remove('visually-hidden');
  e.target.reset();
  setTimeout(() => {
    alert.classList.add('visually-hidden');
  }, 6000);
});
