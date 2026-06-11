document.getElementById('finance-form').addEventListener('submit', (e) => {
  e.preventDefault();
  const btn = e.target.querySelector('button');
  const originalText = btn.textContent;
  
  btn.textContent = 'Processing...';
  btn.style.opacity = '0.7';
  
  setTimeout(() => {
    btn.textContent = 'Application Submitted!';
    btn.style.background = '#4cd137'; // success green
    e.target.reset();
    
    setTimeout(() => {
      btn.textContent = originalText;
      btn.style.background = ''; // reset to default css
      btn.style.opacity = '1';
    }, 3000);
  }, 1500);
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    document.querySelector(this.getAttribute('href')).scrollIntoView({
      behavior: 'smooth'
    });
  });
});
