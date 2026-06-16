#!/usr/bin/env python3
import os
import glob
import re

# Base workspace directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# CSS rules to append to the end of style.css
CSS_APPEND = """
/* ========================================================
   Mobile UX Spruce Up (Automated Rollout)
   ======================================================== */
@media (max-width: 768px) {
  .nav-menu {
    position: fixed !important;
    top: 0 !important;
    right: -100% !important;
    left: auto !important;
    width: 80% !important;
    max-width: 320px !important;
    height: 100vh !important;
    background-color: rgba(250, 249, 246, 0.95) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-left: 1px solid rgba(255, 255, 255, 0.4) !important;
    box-shadow: -10px 0 40px rgba(0,0,0,0.1) !important;
    padding: 120px 40px 60px !important;
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), right 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
    z-index: 1000 !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    transform: none !important;
    opacity: 1 !important;
    pointer-events: auto !important;
  }
  
  .nav-menu.open {
    right: 0 !important;
  }
  
  .nav-menu ul {
    flex-direction: column !important;
    align-items: flex-start !important;
    gap: 2.25rem !important;
    width: 100% !important;
  }
  
  .nav-menu ul li {
    width: 100% !important;
    opacity: 0;
    transform: translateX(30px);
    transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.4s ease;
    transition-delay: calc(var(--item-index, 0) * 0.08s);
  }
  
  .nav-menu.open ul li {
    opacity: 1 !important;
    transform: translateX(0) !important;
  }
  
  .nav-link {
    font-size: 1.15rem !important;
    display: block !important;
    width: 100% !important;
    font-weight: 400 !important;
    letter-spacing: 0.05em !important;
    color: #1a1a1a !important;
  }
  
  .nav-link.btn-olive, .nav-link.btn-primary, .nav-link.btn, .nav-link[class*="btn-"] {
    text-align: center !important;
    padding: 1rem !important;
    border-radius: 8px !important;
    margin-top: 1rem !important;
    color: #fff !important;
  }
  
  /* Drawer decoration footer */
  .nav-menu::after {
    content: "Local Business Showcase" !important;
    display: block !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #666 !important;
    border-top: 1px solid rgba(0, 0, 0, 0.1) !important;
    padding-top: 2rem !important;
    margin-top: auto !important;
  }
}

/* Nav Drawer Backdrop Overlay */
.nav-drawer-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(18, 18, 16, 0.25);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.4s ease;
  z-index: 999;
}
.nav-drawer-backdrop.visible {
  opacity: 1;
  pointer-events: auto;
}

/* Floating Bottom Navigation Bar */
.mobile-bottom-bar {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translate(-50%, 120px);
  width: 90%;
  max-width: 420px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(25px);
  -webkit-backdrop-filter: blur(25px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 50px;
  box-shadow: 0 12px 35px rgba(18, 18, 16, 0.15);
  z-index: 998;
  display: none;
  justify-content: space-around;
  padding: 8px 12px;
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.4s ease;
  opacity: 0;
}

.mobile-bottom-bar.visible {
  transform: translate(-50%, 0);
  opacity: 1;
}

.bottom-bar-action {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  color: #333;
  font-size: 0.72rem;
  font-weight: 500;
  gap: 3px;
  padding: 8px 16px;
  border-radius: 30px;
  transition: background-color 0.2s ease, transform 0.1s ease;
}

.bottom-bar-action:active {
  transform: scale(0.95);
  background-color: rgba(0, 0, 0, 0.08);
}

.bottom-bar-action svg {
  width: 20px;
  height: 20px;
  stroke: currentColor;
  stroke-width: 1.5;
  fill: none;
}

@media (max-width: 768px) {
  .mobile-bottom-bar {
    display: flex;
  }
  
  /* Horizontal swipe carousels on mobile */
  .mobile-swipe-carousel {
    display: flex !important;
    overflow-x: auto !important;
    scroll-snap-type: x mandatory !important;
    gap: 1.5rem !important;
    padding: 1rem 1.5rem 2rem !important;
    margin-left: -1.5rem !important;
    margin-right: -1.5rem !important;
    scrollbar-width: none !important;
    -webkit-overflow-scrolling: touch;
    grid-template-columns: none !important;
  }
  
  .mobile-swipe-carousel::-webkit-scrollbar {
    display: none !important;
  }
  
  .mobile-swipe-carousel > * {
    scroll-snap-align: center !important;
    flex: 0 0 85% !important;
    max-width: 85% !important;
    margin: 0 !important;
  }
}
"""

# JS implementation content
JS_CONTENT = """// Mobile UX Drawer & Bottom Bar Controllers
document.addEventListener('DOMContentLoaded', () => {
  const menuToggle = document.getElementById('menu-toggle');
  const primaryNav = document.getElementById('primary-navigation');
  
  if (menuToggle && primaryNav) {
    // Inject backdrop overlay
    if (!document.querySelector('.nav-drawer-backdrop')) {
      const navBackdrop = document.createElement('div');
      navBackdrop.className = 'nav-drawer-backdrop';
      document.body.appendChild(navBackdrop);
      
      // Toggle handling
      const toggleMenu = (forceClose = false) => {
        const isOpen = forceClose ? false : !primaryNav.classList.contains('open');
        if (isOpen) {
          primaryNav.classList.add('open');
          primaryNav.setAttribute('data-visible', 'true');
          menuToggle.classList.add('menu-toggle-active');
          menuToggle.setAttribute('aria-expanded', 'true');
          navBackdrop.classList.add('visible');
          document.body.style.overflow = 'hidden';
        } else {
          primaryNav.classList.remove('open');
          primaryNav.setAttribute('data-visible', 'false');
          menuToggle.classList.remove('menu-toggle-active');
          menuToggle.setAttribute('aria-expanded', 'false');
          navBackdrop.classList.remove('visible');
          document.body.style.overflow = '';
        }
      };

      // Set index properties for stagger transition delays
      const navItems = primaryNav.querySelectorAll('ul li');
      navItems.forEach((item, index) => {
        item.style.setProperty('--item-index', index);
      });

      menuToggle.addEventListener('click', (e) => {
        e.stopImmediatePropagation();
        toggleMenu();
      });

      navBackdrop.addEventListener('click', () => toggleMenu(true));

      const navLinks = primaryNav.querySelectorAll('.nav-link');
      navLinks.forEach(link => {
        link.addEventListener('click', () => toggleMenu(true));
      });
    }
  }

  // Floating Bottom Navigation Scroll Behavior
  const bottomBar = document.getElementById('mobile-bottom-bar');
  if (bottomBar) {
    window.addEventListener('scroll', () => {
      if (window.innerWidth <= 768) {
        if (window.scrollY < 100) {
          bottomBar.classList.remove('visible');
        } else {
          bottomBar.classList.add('visible');
        }
      }
    }, { passive: true });
  }
});
"""

def process_project(proj_path):
  proj_name = os.path.basename(proj_path)
  
  # 1. Identify style.css file
  css_file = None
  possible_css = [
      os.path.join(proj_path, "src", "style.css"),
      os.path.join(proj_path, "style.css")
  ]
  for p in possible_css:
    if os.path.exists(p):
      css_file = p
      break
      
  # 2. Identify main.js file
  js_file = None
  possible_js = [
      os.path.join(proj_path, "src", "main.js"),
      os.path.join(proj_path, "main.js")
  ]
  for p in possible_js:
    if os.path.exists(p):
      js_file = p
      break

  # 3. Identify all HTML files in project root
  html_files = glob.glob(os.path.join(proj_path, "*.html"))

  if not css_file or not js_file or not html_files:
    print(f"Skipping {proj_name}: Missing core files (CSS: {css_file}, JS: {js_file}, HTML: {len(html_files)})")
    return

  print(f"Processing {proj_name}...")

  # A. Write mobile-ux.js
  mobile_ux_path = os.path.join(os.path.dirname(js_file), "mobile-ux.js")
  with open(mobile_ux_path, "w") as f:
    f.write(JS_CONTENT)

  # B. Prepend import to main.js if not already imported, and heal literal \\n escapes
  with open(js_file, "r") as f:
    js_data = f.read()
  
  # Heal literal backslash-n sequences
  js_data = js_data.replace("import './mobile-ux.js';\\\\n", "import './mobile-ux.js';\n")
  js_data = js_data.replace("import './mobile-ux.js';\\n", "import './mobile-ux.js';\n")
  
  if "mobile-ux.js" not in js_data:
    # Prepend import statement with proper newline
    js_data = "import './mobile-ux.js';\n" + js_data
  
  # Write cleaned and updated JS
  with open(js_file, "w") as f:
    f.write(js_data)

  # C. Append CSS styles if not already appended, and heal literal \\n escapes
  with open(css_file, "r") as f:
    css_data = f.read()
  
  # Heal literal backslash-n sequences in CSS
  css_data = css_data.replace("\\n", "\n")
  # Heal incorrect transition syntax if present
  css_data = css_data.replace("transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important, right 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;", "transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), right 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;")
  
  if "Mobile UX Spruce Up" not in css_data:
    css_data += "\n" + CSS_APPEND
  
  with open(css_file, "w") as f:
    f.write(css_data)

  # D. Process HTML files to add bottom nav bar and scroll snapping carousels
  # Determine dynamic URLs based on existing pages
  existing_basenames = [os.path.basename(h) for h in html_files]
  
  services_url = "index.html#services"
  services_label = "Services"
  if "tapas.html" in existing_basenames:
    services_url = "tapas.html"
    services_label = "Tapas"
  elif "packages.html" in existing_basenames:
    services_url = "packages.html"
    services_label = "Packages"
  elif "services.html" in existing_basenames:
    services_url = "services.html"
    services_label = "Services"

  builder_url = "index.html#quote"
  builder_label = "Quote"
  if "planner.html" in existing_basenames:
    builder_url = "planner.html"
    builder_label = "Builder"
  elif "estimator.html" in existing_basenames:
    builder_url = "estimator.html"
    builder_label = "Estimator"

  inquire_url = "index.html#contact"
  if "contact.html" in existing_basenames:
    inquire_url = "contact.html"

  bottom_nav_html = f"""  <!-- Floating Sticky Bottom Action Bar for Mobile -->
  <nav class="mobile-bottom-bar" id="mobile-bottom-bar">
    <a href="index.html" class="bottom-bar-action">
      <svg viewBox="0 0 24 24"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
      <span>Home</span>
    </a>
    <a href="{services_url}" class="bottom-bar-action">
      <svg viewBox="0 0 24 24"><line x1="12" y1="2" x2="12" y2="22"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
      <span>{services_label}</span>
    </a>
    <a href="{builder_url}" class="bottom-bar-action">
      <svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
      <span>{builder_label}</span>
    </a>
    <a href="{inquire_url}" class="bottom-bar-action">
      <svg viewBox="0 0 24 24"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
      <span>Inquire</span>
    </a>
  </nav>
"""

  for h_path in html_files:
    with open(h_path, "r") as f:
      html_data = f.read()

    # 1. Inject bottom nav bar before </body> if not present
    if "mobile-bottom-bar" not in html_data:
      html_data = html_data.replace("</body>", bottom_nav_html + "\\n</body>")

    # 2. Inject scroll snaps into grid classes for testimonials, packages, etc.
    grid_classes_to_carousel = [
        "packages-grid", "testimonials-grid", "services-grid", "pricing-grid", "features-grid"
    ]
    for g_cls in grid_classes_to_carousel:
      # Replace only if it doesn't already have mobile-swipe-carousel
      pattern = re.compile(rf'class="([^"]*?\\b{g_cls}\\b[^"]*?)"')
      matches = pattern.findall(html_data)
      for match in matches:
        if "mobile-swipe-carousel" not in match:
          new_class = match + " mobile-swipe-carousel"
          html_data = html_data.replace(f'class="{match}"', f'class="{new_class}"')

    with open(h_path, "w") as f:
      f.write(html_data)

# Categories to process
folders = ["catering-events", "lifestyle-outdoors", "trades-mechanical", "plumbing-gas", "pest-cleaning"]

for cat in folders:
  cat_path = os.path.join(BASE_DIR, cat)
  if not os.path.exists(cat_path):
    continue
  for sub in os.listdir(cat_path):
    sub_path = os.path.join(cat_path, sub)
    if os.path.isdir(sub_path):
      # Skip node_modules, dist and the pilot
      if sub in ["node_modules", "dist", "riviera-yeppoon"]:
        continue
      process_project(sub_path)

print("All projects updated with Mobile UX components!")
