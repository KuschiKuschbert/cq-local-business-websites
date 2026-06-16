import './mobile-ux.js';
import './style.css';
// Craig Hill Diagnostic Wizard Logic
const symptomDetails = {
  toilet: {
    title: 'Toilet Overflowing',
    desc: 'Likely a structural block down-line. Please avoid flushing additional water. We recommend emergency camera inspections to locate tree roots or structural collapse.'
  },
  shower: {
    title: 'Slow Shower / Basin Drainage',
    desc: 'Commonly caused by local grease, hair, or soap scale build-up. A hydro-jet flushing or simple chemical wash will restore full flow capacity.'
  },
  yard: {
    title: 'Gurgling Pipes / Sewer Odours',
    desc: 'Indicates high ventilation blocks or sewer pipe surcharge. Keep clear of boundary access caps until we inspect with digital tracking tools.'
  }
};

document.querySelectorAll('.selector-option').forEach(option => {
  option.addEventListener('click', () => {
    document.querySelectorAll('.selector-option').forEach(o => o.classList.remove('active'));
    option.classList.add('active');
    
    const symptom = option.getAttribute('data-symptom');
    document.getElementById('symptom-input').value = symptom;
    
    // Update Feedback Info box
    const info = symptomDetails[symptom];
    document.getElementById('feedback-title').textContent = info.title;
    document.getElementById('feedback-desc').textContent = info.desc;
  });
});

document.getElementById('diagnostic-form').addEventListener('submit', function(e) {
  e.preventDefault();
  const alert = document.getElementById('booking-success');
  alert.classList.remove('visually-hidden');
  e.target.reset();
  setTimeout(() => {
    alert.classList.add('visually-hidden');
  }, 6000);
});
