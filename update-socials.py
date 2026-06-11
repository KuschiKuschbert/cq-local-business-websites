#!/usr/bin/env python3
"""
update-socials.py
Injects social media links (or a 'no socials found' warning) into the footer
of each of the 26 local business websites.
"""

import re
import os

BASE = os.path.dirname(os.path.abspath(__file__))

# -------------------------------------------------------------------
# Social media data gathered from research agents + direct site fetch
# -------------------------------------------------------------------
SOCIALS = {
    # Catering
    "catering-events/creative-cater": {
        "facebook": "https://www.facebook.com/creativecateryeppoon",
        "instagram": "https://www.instagram.com/creativecater",
        "note": None,
    },
    "catering-events/dunlop-catering": {
        "facebook": None, "instagram": None,
        "note": "No social media profiles found for this business.",
    },
    "catering-events/evolution-catering": {
        "facebook": None, "instagram": None,
        "note": "No social media profiles found for this business.",
    },
    "catering-events/tasteful-creations": {
        "facebook": None, "instagram": None,
        "note": "No social media profiles found for this business.",
    },
    # Lifestyle / Outdoors
    "lifestyle-outdoors/coffee-and-co": {
        "facebook": "https://www.facebook.com/profile.php?id=100094704168577",
        "instagram": None,
        "note": None,
    },
    "lifestyle-outdoors/studio-bohemia": {
        "facebook": None, "instagram": None,
        "note": "No social media profiles found for this business.",
    },
    "lifestyle-outdoors/the-lawn-ranger": {
        "facebook": None, "instagram": None,
        "note": "No social media profiles found for this business.",
    },
    "lifestyle-outdoors/fantastic-landscaping": {
        "facebook": None, "instagram": None,
        "note": "No social media profiles found for this business.",
    },
    "lifestyle-outdoors/mal-earthworks": {
        "facebook": "https://www.facebook.com/M.A.LEarthworks",
        "instagram": None,
        "note": None,
    },
    # Trades / Mechanical
    "trades-mechanical/budget-electrical-cq": {
        "facebook": None, "instagram": None,
        "note": "Facebook page exists but URL could not be confirmed. Visit budgetelectrical.com.au to find the link.",
    },
    "trades-mechanical/fg-mechanical": {
        "facebook": None, "instagram": None,
        "note": "No social media profiles found for this business.",
    },
    "trades-mechanical/leons-dingo-hire": {
        "facebook": None, "instagram": None,
        "note": "No social media profiles found for this business.",
    },
    "trades-mechanical/richardson-motors": {
        "facebook": None, "instagram": None,
        "note": "No social media profiles found for this business.",
    },
    # Plumbing / Gas
    "plumbing-gas/bkk-plumbing": {
        "facebook": None, "instagram": None,
        "note": "No social media profiles found for this business.",
    },
    "plumbing-gas/craig-hill-plumbing": {
        "facebook": None, "instagram": None,
        "note": "No social media profiles found for this business.",
    },
    "plumbing-gas/grant-goltz-plumbing": {
        "facebook": None, "instagram": None,
        "note": "No social media profiles found for this business.",
    },
    "plumbing-gas/keppel-bay-plumbing": {
        "facebook": None, "instagram": None,
        "note": "No social media profiles found for this business.",
    },
    "plumbing-gas/mar-lin-plumbing": {
        "facebook": None, "instagram": None,
        "note": "No social media profiles found for this business.",
    },
    "plumbing-gas/toons-plumbing": {
        "facebook": None, "instagram": None,
        "note": "No social media profiles found for this business.",
    },
    "plumbing-gas/truflow-plumbing": {
        "facebook": None, "instagram": None,
        "note": "No social media profiles found for this business.",
    },
    # Pest / Cleaning
    "pest-cleaning/bad-bugs-pest-control": {
        "facebook": None, "instagram": None,
        "note": "No social media profiles found for this business.",
    },
    "pest-cleaning/bonds-termite-management": {
        "facebook": None, "instagram": None,
        "note": "No social media profiles found for this business.",
    },
    "pest-cleaning/jld-pest-solutions": {
        "facebook": None, "instagram": None,
        "note": "Facebook page confirmed to exist. Search 'JLD Pest Solutions Yeppoon' on Facebook to find the page.",
    },
    "pest-cleaning/sanclassic-cleaning": {
        "facebook": "https://www.facebook.com/SanClassic",
        "instagram": "https://www.instagram.com/sanclassic_cleaning/",
        "note": None,
    },
    "pest-cleaning/total-pest-carpet": {
        "facebook": None, "instagram": None,
        "note": "No social media profiles found for this business.",
    },
    "pest-cleaning/yeppoon-carpet-pest": {
        "facebook": "https://www.facebook.com/Yeppoon-Carpet-Cleaning-Pest-Control-1066950320032591/",
        "instagram": None,
        "note": None,
    },
}

# -------------------------------------------------------------------
# SVG icons (inline, no emoji dependency)
# -------------------------------------------------------------------
FB_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" '
    'fill="currentColor" aria-hidden="true"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7'
    'a1 1 0 0 1 1-1h3z"/></svg>'
)
IG_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" '
    'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
    'aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/>'
    '<path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/>'
    '<line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>'
)
WARN_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" '
    'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
    'aria-hidden="true"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 '
    '3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/>'
    '<line x1="12" y1="17" x2="12.01" y2="17"/></svg>'
)


def build_social_html(fb, ig, note):
    """Build the social block HTML to inject before </footer>."""
    lines = [
        '',
        '    <!-- Social Media Links (auto-generated) -->',
        '    <div class="social-links-bar" style="'
        'text-align:center;padding:0.75rem 1rem 0.5rem;'
        'border-top:1px solid rgba(255,255,255,0.12);margin-top:0.75rem;'
        'display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:0.75rem;">',
    ]

    if fb:
        lines.append(
            f'      <a href="{fb}" target="_blank" rel="noopener noreferrer" '
            f'aria-label="Facebook" '
            f'style="display:inline-flex;align-items:center;gap:0.4rem;'
            f'color:inherit;opacity:0.85;text-decoration:none;font-size:0.875rem;">'
            f'{FB_SVG} Facebook</a>'
        )
    if ig:
        lines.append(
            f'      <a href="{ig}" target="_blank" rel="noopener noreferrer" '
            f'aria-label="Instagram" '
            f'style="display:inline-flex;align-items:center;gap:0.4rem;'
            f'color:inherit;opacity:0.85;text-decoration:none;font-size:0.875rem;">'
            f'{IG_SVG} Instagram</a>'
        )

    if note and not fb and not ig:
        lines.append(
            f'      <span style="display:inline-flex;align-items:center;gap:0.4rem;'
            f'font-size:0.8rem;opacity:0.65;font-style:italic;">'
            f'{WARN_SVG} {note}</span>'
        )
    elif note:
        lines.append(
            f'      <span style="display:inline-flex;align-items:center;gap:0.4rem;'
            f'font-size:0.8rem;opacity:0.65;font-style:italic;">'
            f'{WARN_SVG} {note}</span>'
        )

    lines.append('    </div>')
    return '\n'.join(lines) + '\n'


# -------------------------------------------------------------------
# Main injection loop
# -------------------------------------------------------------------
def inject(path_key, data):
    html_path = os.path.join(BASE, path_key.replace("/", os.sep), "index.html")
    if not os.path.exists(html_path):
        print(f"  ⚠️  NOT FOUND: {html_path}")
        return

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Remove any previously injected social block so we stay idempotent
    content = re.sub(
        r'\n\s*<!-- Social Media Links \(auto-generated\) -->.*?</div>\n',
        '',
        content,
        flags=re.DOTALL
    )

    social_html = build_social_html(data["facebook"], data["instagram"], data.get("note"))

    # Insert just before the closing </footer> tag
    if "</footer>" in content:
        content = content.replace("</footer>", social_html + "  </footer>", 1)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(content)

        fb_status = "✅" if data["facebook"] else "—"
        ig_status = "✅" if data["instagram"] else "—"
        warn_status = f"⚠️  {data['note']}" if data.get("note") else ""
        print(f"  {path_key}")
        print(f"     FB: {fb_status}  IG: {ig_status}  {warn_status}")
    else:
        print(f"  ❌  No </footer> found in {html_path}")


print("\n🔗 Updating social media links across all 26 websites...\n")
for key, info in SOCIALS.items():
    inject(key, info)

print("\n✅  Done! All sites updated.\n")
