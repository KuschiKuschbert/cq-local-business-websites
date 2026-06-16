#!/usr/bin/env python3
"""
make-mockup.py
Bootstraps a new premium local business website mockup Vite project
integrated with the Cap Coast Design Engine and Component Library.
"""

import os
import sys
import json
import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser(description="Bootstrap a new business website mockup.")
    parser.add_argument("category", choices=["catering-events", "lifestyle-outdoors", "trades-mechanical", "plumbing-gas", "pest-cleaning"], help="Business niche category folder")
    parser.add_argument("name", help="Slug/name for the mockup folder (e.g. yeppoon-gardens)")
    parser.add_argument("--archetype", choices=["brutalist", "editorial", "nordic"], help="Design archetype (default based on category)")
    parser.add_argument("--palette", choices=["obsidian-dark", "terracotta-clay", "sage-garden", "desert-gold"], help="Color palette (default based on category)")
    args = parser.parse_args()

    # Determine defaults based on category
    category_defaults = {
        "catering-events": {"archetype": "editorial", "palette": "obsidian-dark"},
        "lifestyle-outdoors": {"archetype": "editorial", "palette": "sage-garden"},
        "trades-mechanical": {"archetype": "brutalist", "palette": "desert-gold"},
        "plumbing-gas": {"archetype": "brutalist", "palette": "obsidian-dark"},
        "pest-cleaning": {"archetype": "nordic", "palette": "terracotta-clay"},
    }

    arch = args.archetype or category_defaults[args.category]["archetype"]
    pal = args.palette or category_defaults[args.category]["palette"]

    root_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.join(root_dir, args.category, args.name)

    if os.path.exists(project_dir):
        print(f"Error: Directory already exists at {project_dir}")
        sys.exit(1)

    print(f"Creating new mockup at: {project_dir}")
    os.makedirs(os.path.join(project_dir, "src"), exist_ok=True)
    os.makedirs(os.path.join(project_dir, "public"), exist_ok=True)

    # 1. Write package.json
    pkg_content = {
        "name": args.name,
        "version": "0.0.0",
        "private": True,
        "type": "module",
        "scripts": {
            "dev": "vite",
            "build": "vite build",
            "preview": "vite preview"
        },
        "devDependencies": {
            "vite": "^8.0.12"
        }
    }
    with open(os.path.join(project_dir, "package.json"), "w", encoding="utf-8") as f:
        json.dump(pkg_content, f, indent=2)

    # 2. Write gitignore
    gitignore_content = "node_modules\ndist\n.DS_Store\n"
    with open(os.path.join(project_dir, ".gitignore"), "w", encoding="utf-8") as f:
        f.write(gitignore_content)

    # 3. Write basic index.html template
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{args.name.replace('-', ' ').title()} | Yeppoon Local Service</title>
</head>
<body>
  <header style="padding: 2rem; text-align: center;">
    <h1>{args.name.replace('-', ' ').title()}</h1>
    <p>Premium local service serving Capricorn Coast</p>
  </header>

  <main>
    <!-- Component Library: Cost Estimator pricing slider -->
    <section style="padding: 3rem 1rem;">
      <div class="de-pricing-slider-card">
        <h3>Estimated Quote calculator</h3>
        <p class="subtitle">Drag the slider to calculate pricing estimate instantly.</p>
        <div class="de-slider-group">
          <div class="de-slider-label">
            <span>Project Size / Scope</span>
            <span class="de-slider-val-output">50</span>
          </div>
          <input type="range" class="de-slider-input" min="10" max="200" value="50" data-multiplier="12.5" data-base-fee="150" data-unit=" sqm">
        </div>
        <div class="de-pricing-result">
          Estimated Cost: <span class="de-pricing-val">$0</span>
        </div>
      </div>
    </section>

    <!-- Component Library: Reviews Star Ratings Slider -->
    <section style="padding: 3rem 1rem; max-width: 800px; margin: 0 auto;">
      <h2 style="text-align: center; margin-bottom: 2rem;">Customer Reviews</h2>
      <div class="de-reviews-container">
        <div class="de-reviews-track">
          <div class="de-review-card">
            <div class="de-stars">
              <!-- Star SVGs -->
              <svg viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
              <svg viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
              <svg viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
              <svg viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
              <svg viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
            </div>
            <p class="de-review-text">"Fantastic service! Quick response times and very professional team."</p>
            <div class="de-review-author">Sarah Jenkins</div>
            <div class="de-review-source">Local Yeppoon Resident</div>
          </div>
          <div class="de-review-card">
            <div class="de-stars">
              <svg viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
              <svg viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
              <svg viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
              <svg viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
              <svg viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
            </div>
            <p class="de-review-text">"High attention to detail. Recommended without hesitation."</p>
            <div class="de-review-author">David Miller</div>
            <div class="de-review-source">Verified Customer</div>
          </div>
        </div>
      </div>
    </section>
  </main>

  <footer style="padding: 2rem; text-align: center; margin-top: 3rem; opacity: 0.7;">
    <p>&copy; 2026 {args.name.replace('-', ' ').title()}. All rights reserved.</p>
  </footer>
</body>
</html>
"""
    with open(os.path.join(project_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)

    # 4. Invoke apply-design-engine.py to configure archetype and palette
    print(f"Applying design styling: Archetype={arch}, Palette={pal}")
    apply_script = os.path.join(root_dir, "apply-design-engine.py")
    subprocess.run([
        sys.executable,
        apply_script,
        project_dir,
        "--archetype", arch,
        "--palette", pal
    ], check=True)

    print("\n🎉 Mockup successfully created and integrated with the Cap Coast Design Engine!")
    print(f"Run standard commands to review:")
    print(f"  cd {args.category}/{args.name} && npm install && npm run dev\n")

if __name__ == "__main__":
    main()
