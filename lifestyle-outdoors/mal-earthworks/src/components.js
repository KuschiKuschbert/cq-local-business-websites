/**
 * Cap Coast Component Library - Shared Niche Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  initPricingSliders();
  initReviewSliders();
});

/**
 * Multiplies slider value by a base multiplier to estimate service cost
 */
function initPricingSliders() {
  const sliders = document.querySelectorAll('.de-slider-input');
  
  sliders.forEach(slider => {
    const parentCard = slider.closest('.de-pricing-slider-card');
    if (!parentCard) return;
    
    const valueDisplay = parentCard.querySelector('.de-slider-val-output');
    const costDisplay = parentCard.querySelector('.de-pricing-val');
    
    const multiplier = parseFloat(slider.dataset.multiplier) || 1.0;
    const baseFee = parseFloat(slider.dataset.baseFee) || 0.0;
    const unitFormat = slider.dataset.unit || '';
    
    function updateDisplay() {
      const val = parseInt(slider.value, 10);
      if (valueDisplay) {
        valueDisplay.textContent = `${val}${unitFormat}`;
      }
      if (costDisplay) {
        const total = baseFee + (val * multiplier);
        costDisplay.textContent = `$${Math.round(total)}`;
      }
    }
    
    slider.addEventListener('input', updateDisplay);
    updateDisplay(); // trigger initial run
  });
}

/**
 * Initializes auto-scrolling Star Rating/Review Carousels
 */
function initReviewSliders() {
  const tracks = document.querySelectorAll('.de-reviews-track');
  
  tracks.forEach(track => {
    const container = track.closest('.de-reviews-container');
    if (!container) return;
    
    const cards = track.querySelectorAll('.de-review-card');
    if (cards.length <= 1) return;
    
    let currentIndex = 0;
    const scrollInterval = 4000; // 4 seconds
    
    function getSlidesPerView() {
      return window.innerWidth >= 768 ? 2 : 1;
    }
    
    function nextSlide() {
      const slidesPerView = getSlidesPerView();
      const maxIndex = Math.max(0, cards.length - slidesPerView);
      
      currentIndex++;
      if (currentIndex > maxIndex) {
        currentIndex = 0;
      }
      
      const offset = currentIndex * (100 / slidesPerView);
      track.style.transform = `translateX(-${offset}%)`;
    }
    
    let intervalId = setInterval(nextSlide, scrollInterval);
    
    // Pause auto-scroll on hover
    container.addEventListener('mouseenter', () => clearInterval(intervalId));
    container.addEventListener('mouseleave', () => {
      intervalId = setInterval(nextSlide, scrollInterval);
    });
    
    // Re-adjust offset on window resize
    window.addEventListener('resize', () => {
      const slidesPerView = getSlidesPerView();
      const maxIndex = Math.max(0, cards.length - slidesPerView);
      if (currentIndex > maxIndex) {
        currentIndex = maxIndex;
      }
      const offset = currentIndex * (100 / slidesPerView);
      track.style.transform = `translateX(-${offset}%)`;
    });
  });
}
