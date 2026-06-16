/**
 * Cap Coast Design Engine - JS Micro-interactions & Core Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  initNoiseOverlay();
  initCursorFollower();
  initKineticTypography();
  initScrollReveal();
});

/**
 * Injects a noise/grain texture overlay dynamically to enhance organic aesthetic depth
 */
function initNoiseOverlay() {
  if (!document.querySelector('.de-noise-overlay')) {
    const overlay = document.createElement('div');
    overlay.className = 'de-noise-overlay';
    document.body.appendChild(overlay);
  }
}

/**
 * Implements a sleek cursor follower with premium desktop micro-animation feedback
 */
function initCursorFollower() {
  const follower = document.createElement('div');
  follower.className = 'de-cursor-follower';
  document.body.appendChild(follower);

  let mouseX = 0, mouseY = 0;
  let followerX = 0, followerY = 0;

  window.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
  });

  // Smooth ease-out animation loop for the custom cursor
  function animate() {
    const dx = mouseX - followerX;
    const dy = mouseY - followerY;
    followerX += dx * 0.15;
    followerY += dy * 0.15;

    follower.style.left = `${followerX}px`;
    follower.style.top = `${followerY}px`;
    requestAnimationFrame(animate);
  }
  animate();

  // Hover feedback for buttons, links and active items
  const clickables = document.querySelectorAll('a, button, .de-btn, .de-grid-item, input, textarea');
  clickables.forEach(item => {
    item.addEventListener('mouseenter', () => {
      follower.style.transform = 'translate(-50%, -50%) scale(2)';
      follower.style.backgroundColor = 'rgba(255, 255, 255, 0.9)';
      follower.style.mixBlendMode = 'difference';
    });
    item.addEventListener('mouseleave', () => {
      follower.style.transform = 'translate(-50%, -50%) scale(1)';
      follower.style.backgroundColor = 'var(--color-primary)';
      follower.style.mixBlendMode = 'difference';
    });
  });
}

/**
 * Automatically parses elements marked with class '.de-kinetic-text' and splits text 
 * into individual character structures to enable elegant staggered animations.
 */
function initKineticTypography() {
  const textElements = document.querySelectorAll('.de-kinetic-text');
  
  textElements.forEach(el => {
    const rawText = el.textContent.trim();
    el.textContent = ''; // clear original text
    
    const words = rawText.split(' ');
    
    words.forEach((word, wordIndex) => {
      const wordSpan = document.createElement('span');
      wordSpan.className = 'de-kinetic-word';
      
      const chars = word.split('');
      chars.forEach((char, charIndex) => {
        const charSpan = document.createElement('span');
        charSpan.className = 'de-kinetic-letter';
        charSpan.textContent = char;
        // set transition delay for staggered hover lift
        charSpan.style.transitionDelay = `${charIndex * 0.03}s`;
        wordSpan.appendChild(charSpan);
      });
      
      el.appendChild(wordSpan);
      
      // Add spaces between words
      if (wordIndex < words.length - 1) {
        el.appendChild(document.createTextNode(' '));
      }
    });
  });
}

/**
 * Tracks viewport scrolling and animates elements as they enter the screen
 */
function initScrollReveal() {
  const reveals = document.querySelectorAll('.de-reveal');
  
  const observerOptions = {
    root: null, // viewport
    threshold: 0.15, // trigger when 15% of the element is visible
    rootMargin: '0px 0px -50px 0px' // offset to ensure smooth entrance
  };
  
  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
        // Stop observing once reveal trigger is processed
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);
  
  reveals.forEach(el => {
    observer.observe(el);
  });
}
