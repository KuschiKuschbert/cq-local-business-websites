import './mobile-ux.js';
import './style.css';
// Toons Pricing Estimator Logic
const drainSlider = document.getElementById('drain-length');
const gasSlider = document.getElementById('gas-points');
const tierSelect = document.getElementById('service-tier');

const lengthVal = document.getElementById('length-val');
const gasVal = document.getElementById('gas-val');
const priceVal = document.getElementById('price-val');

function calculateEstimate() {
  const drainLen = parseInt(drainSlider.value);
  const gasPoints = parseInt(gasSlider.value);
  const tier = parseFloat(tierSelect.value);
  
  lengthVal.textContent = drainLen;
  gasVal.textContent = gasPoints;
  
  // Base rates: drainage $50/m, gas points $150/ea
  const baseCost = (drainLen * 50) + (gasPoints * 170);
  const total = Math.round(baseCost * tier);
  
  priceVal.textContent = total;
}

drainSlider.addEventListener('input', calculateEstimate);
gasSlider.addEventListener('input', calculateEstimate);
tierSelect.addEventListener('change', calculateEstimate);

// Initial calculation
calculateEstimate();

document.getElementById('estimator-form').addEventListener('submit', function(e) {
  e.preventDefault();
  const alert = document.getElementById('estimator-success');
  alert.classList.remove('visually-hidden');
  e.target.reset();
  setTimeout(() => {
    alert.classList.add('visually-hidden');
  }, 6000);
});
