document.getElementById('quoteForm').addEventListener('submit', function(e) {
  e.preventDefault();
  
  // Basic simulation of form submission
  const btn = this.querySelector('button');
  const originalText = btn.textContent;
  btn.textContent = 'Sending...';
  btn.disabled = true;
  
  setTimeout(() => {
    this.classList.add('hidden');
    document.getElementById('formSuccess').classList.remove('hidden');
  }, 1000);
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    document.querySelector(this.getAttribute('href')).scrollIntoView({
      behavior: 'smooth'
    });
  });
});
