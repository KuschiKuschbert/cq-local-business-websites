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
  const follower = document.createElement('div');
  follower.className = `de-cursor-follower de-cursor-${cursorType}`;
  document.body.appendChild(follower);

  let mouseX = 0, mouseY = 0;
  let followerX = 0, followerY = 0;
  let velX = 0, velY = 0;

  window.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
  });

  // Easing/latency customized per niche
  let easing = 0.15;
  if (cursorType === 'editorial') {
    easing = 0.08; // elegant lag
  } else if (cursorType === 'trade') {
    easing = 0.25; // crisp snap
  }

  // Smooth animation loop
  function animate() {
    const dx = mouseX - followerX;
    const dy = mouseY - followerY;
    
    velX = dx * easing;
    velY = dy * easing;
    
    followerX += velX;
    followerY += velY;

    follower.style.left = `${followerX}px`;
    follower.style.top = `${followerY}px`;
    
    // Playful squash/stretch only for nordic archetype
    if (cursorType === 'nordic') {
      const speed = Math.sqrt(velX * velX + velY * velY);
      const scaleX = 1 + Math.min(speed * 0.04, 0.5);
      const scaleY = 1 - Math.min(speed * 0.03, 0.3);
      const angle = Math.atan2(velY, velX) * (180 / Math.PI);
      follower.style.transform = `translate(-50%, -50%) rotate(${angle}deg) scale(${scaleX}, ${scaleY})`;
    }
    
    requestAnimationFrame(animate);
  }
  animate();

  // Hover feedback tailored for each niche type
  const clickables = document.querySelectorAll('a, button, .de-btn, .de-grid-item, input, textarea');
  clickables.forEach(item => {
    item.addEventListener('mouseenter', () => {
      if (cursorType === 'trade') {
        follower.style.transform = 'translate(-50%, -50%) scale(1.5)';
        follower.style.border = '2px solid var(--color-primary)';
        follower.style.backgroundColor = 'transparent';
        follower.style.borderRadius = '0px';
      } else if (cursorType === 'editorial') {
        follower.style.transform = 'translate(-50%, -50%) scale(2.5)';
        follower.style.opacity = '0.35';
        follower.style.backgroundColor = 'var(--color-primary)';
      } else {
        follower.style.transform = 'translate(-50%, -50%) scale(2)';
        follower.style.backgroundColor = 'rgba(255, 255, 255, 0.9)';
        follower.style.mixBlendMode = 'difference';
      }
    });
    item.addEventListener('mouseleave', () => {
      if (cursorType === 'trade') {
        follower.style.transform = 'translate(-50%, -50%) scale(1)';
        follower.style.border = 'none';
        follower.style.backgroundColor = 'var(--color-primary)';
        follower.style.borderRadius = '0px';
      } else if (cursorType === 'editorial') {
        follower.style.transform = 'translate(-50%, -50%) scale(1)';
        follower.style.opacity = '1';
        follower.style.backgroundColor = 'transparent';
      } else {
        follower.style.transform = 'translate(-50%, -50%) scale(1)';
        follower.style.backgroundColor = 'var(--color-primary)';
        follower.style.mixBlendMode = 'difference';
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
