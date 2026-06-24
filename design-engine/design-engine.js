/**
 * Cap Coast Design Engine - JS Micro-interactions & Core Logic
 */

document.addEventListener('DOMContentLoaded', () => {
  initNoiseOverlay();

  // Skip cursor follower on premium/luxury sites that opt out
  if (document.body.dataset.deCursor !== 'off') {
    initCursorFollower();
  }

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
  const cursorType = document.body.dataset.deCursorType || 'default';
  
  // Create exact center tracking dot
  const dot = document.createElement('div');
  dot.className = 'de-cursor-dot';
  document.body.appendChild(dot);

  // Create outer spring-lag follower ring
  const follower = document.createElement('div');
  follower.className = `de-cursor-follower de-cursor-${cursorType}`;
  document.body.appendChild(follower);

  // Span for dynamic hover labels inside follower
  const labelSpan = document.createElement('span');
  labelSpan.style.display = 'none';
  follower.appendChild(labelSpan);

  let mouseX = -100, mouseY = -100;
  let dotX = -100, dotY = -100;
  let followerX = -100, followerY = -100;
  let velX = 0, velY = 0;

  window.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
  });

  // Easing/latency customized per niche
  let easing = 0.12;
  if (cursorType === 'editorial') {
    easing = 0.07; // elegant lag
  } else if (cursorType === 'trade') {
    easing = 0.22; // crisp snap
  }

  // Smooth animation loop
  function animate() {
    // Immediate track for inner dot
    const dotDx = mouseX - dotX;
    const dotDy = mouseY - dotY;
    dotX += dotDx * 0.45;
    dotY += dotDy * 0.45;
    dot.style.left = `${dotX}px`;
    dot.style.top = `${dotY}px`;

    // Spring-physics lag track for outer follower ring
    const dx = mouseX - followerX;
    const dy = mouseY - followerY;
    
    velX = dx * easing;
    velY = dy * easing;
    
    followerX += velX;
    followerY += velY;

    follower.style.left = `${followerX}px`;
    follower.style.top = `${followerY}px`;
    
    if (!follower.classList.contains('de-hover-active')) {
      follower.style.transform = `translate(-50%, -50%) scale(1)`;
    }
    
    requestAnimationFrame(animate);
  }
  animate();

  // Hover feedback tailored for premium conversion context
  const clickables = document.querySelectorAll('a, button, .de-btn, .de-grid-item, input, textarea, select');
  clickables.forEach(item => {
    item.addEventListener('mouseenter', () => {
      follower.classList.add('de-hover-active');
      dot.classList.add('de-hover-active');
      
      // Select appropriate hover label text based on element context
      let labelText = 'Go';
      if (item.tagName === 'INPUT' || item.tagName === 'TEXTAREA' || item.tagName === 'SELECT') {
        labelText = 'Type';
      } else if (item.getAttribute('href') === '#booking' || item.classList.contains('de-btn') && item.textContent.toLowerCase().includes('book')) {
        labelText = 'Book';
      } else if (item.classList.contains('de-grid-item')) {
        labelText = 'View';
      } else if (item.textContent.toLowerCase().includes('estimate') || item.getAttribute('href') === '#estimator') {
        labelText = 'Calc';
      }
      
      labelSpan.textContent = labelText;
      labelSpan.style.display = 'block';
    });

    item.addEventListener('mouseleave', () => {
      follower.classList.remove('de-hover-active');
      dot.classList.remove('de-hover-active');
      labelSpan.style.display = 'none';
      if (cursorType !== 'nordic') {
        follower.style.transform = `translate(-50%, -50%) scale(1)`;
      }
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
