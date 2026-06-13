#!/usr/bin/env python3
import os
import re
import sys
from html.parser import HTMLParser

# -------------------------------------------------------------------
# Configuration & Category mappings based on PREFERENCES.md and LESSONS.md
# -------------------------------------------------------------------

# Mappings of niches/subfolders to pricing and rule sets
CATEGORY_RULES = {
    "catering-events": {
        "default_price": "$249/mo",
        "niche": "Catering & Events",
        "special_prices": {
            "tasteful-creations": "$199/mo"
        },
        "badge_keywords": []
    },
    "lifestyle-outdoors": {
        "default_price": "$199/mo", # Cafes, Salons, Lawn Care
        "niche": "Lifestyle & Outdoors",
        "special_prices": {
            "fantastic-landscaping": "$299/mo",
            "mal-earthworks": "$299/mo"
        },
        "badge_keywords": [] # Checked dynamically per site below
    },
    "trades-mechanical": {
        "default_price": "$249/mo",
        "niche": "Trades & Mechanical",
        "badge_keywords": []
    },
    "plumbing-gas": {
        "default_price": "$249/mo",
        "niche": "Plumbing & Gas",
        "badge_keywords": ["on-time", "$99"] # "On-Time or We Pay You $50" + "$99 diagnostic"
    },
    "pest-cleaning": {
        "default_price": "$249/mo",
        "niche": "Pest & Cleaning",
        "special_prices": {
            "bonds-termite-management": "$299/mo" # Specialty Pest
        },
        "badge_keywords": ["police", "liability", "lock"] # Police checks, liability, price-lock
    }
}

# -------------------------------------------------------------------
# HTML Parser to extract elements, IDs, titles, H1s, and raw text
# -------------------------------------------------------------------
class WebAuditParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title_content = ""
        self.in_title = False
        self.h1_count = 0
        self.in_h1 = False
        self.ids = []
        self.form_elements_without_id = []
        self.all_text = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # Track Title
        if tag == "title":
            self.in_title = True
            
        # Track H1s
        if tag == "h1":
            self.h1_count += 1
            self.in_h1 = True

        # Track IDs
        if "id" in attrs_dict:
            self.ids.append((tag, attrs_dict["id"]))

        # Track Form elements missing IDs or names
        if tag in ["form", "input", "select", "textarea"]:
            # Buttons and checkboxes sometimes lack ids but forms/inputs/textareas shouldn't
            # We flag them if they have neither id nor name nor aria-label
            if "id" not in attrs_dict and "name" not in attrs_dict and "aria-label" not in attrs_dict:
                self.form_elements_without_id.append(tag)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "h1":
            self.in_h1 = False

    def handle_data(self, data):
        cleaned = data.strip()
        if not cleaned:
            return
        
        if self.in_title:
            self.title_content += cleaned
        
        # Save all text for keyword checks
        self.all_text.append(cleaned)

# -------------------------------------------------------------------
# Main Audit runner
# -------------------------------------------------------------------
def audit_site(dir_path, parent_name, folder_name):
    html_path = os.path.join(dir_path, "index.html")
    if not os.path.exists(html_path):
        return {
            "status": "FAIL",
            "errors": ["Missing index.html file."]
        }

    # Verify style files exist
    # Look for style.css in root or src/
    style_exists = False
    style_paths = [
        os.path.join(dir_path, "style.css"),
        os.path.join(dir_path, "src", "style.css")
    ]
    for p in style_paths:
        if os.path.exists(p):
            style_exists = True
            break
            
    # Also scan for any css import/reference inside source if not directly found
    if not style_exists:
        src_path = os.path.join(dir_path, "src")
        if os.path.exists(src_path):
            for root, _, files in os.walk(src_path):
                if any(f.endswith(".css") for f in files):
                    style_exists = True
                    break

    errors = []
    warnings = []

    if not style_exists:
        errors.append("Missing style.css (checked root, src/ and src/ subdirs).")

    # Read and parse index.html
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
    except Exception as e:
        return {
            "status": "FAIL",
            "errors": [f"Could not read index.html: {str(e)}"]
        }

    parser = WebAuditParser()
    parser.feed(html_content)

    # 1. Title verification
    title = parser.title_content.strip()
    if not title:
        errors.append("Empty <title> tag.")
    elif any(x in title.lower() for x in ["vite app", "vite+react", "react app", "template"]):
        errors.append(f"Default/Placeholder title tag: '{title}'")
    elif len(title) < 8:
        warnings.append(f"Title is very short: '{title}'")

    # 2. H1 Count verification
    if parser.h1_count == 0:
        errors.append("No <h1> element found on page (SEO violation).")
    elif parser.h1_count > 1:
        errors.append(f"Multiple <h1> elements found ({parser.h1_count}). Only one <h1> is allowed per page.")

    # 3. Unique ID checks
    id_counts = {}
    for tag, element_id in parser.ids:
        id_counts[element_id] = id_counts.get(element_id, 0) + 1
        
    duplicates = [element_id for element_id, count in id_counts.items() if count > 1]
    if duplicates:
        errors.append(f"Duplicate HTML IDs found: {', '.join(duplicates)}")

    # 4. Form controls missing identifying attributes
    if parser.form_elements_without_id:
        warnings.append(f"Form control elements missing id/name: {', '.join(parser.form_elements_without_id)}")

    # Combine all parsed text into a single lowercase string for keyword check
    full_text = " ".join(parser.all_text).lower()

    # 5. Pricing tier mapping verification
    category_info = CATEGORY_RULES.get(parent_name, {})
    expected_price = category_info.get("special_prices", {}).get(folder_name, category_info.get("default_price", "$249/mo"))

    # 6. Trust badge validation matching niche category
    if parent_name == "plumbing-gas":
        # Check On-Time & $99 call-out
        if "on-time" not in full_text and "late" not in full_text:
            errors.append("Missing 'On-Time Guarantee' panels/badges.")
        if "99" not in full_text:
            errors.append("Missing '$99 flat-rate diagnostics call-out' pricing panels or acknowledgment check.")
            
    elif parent_name == "pest-cleaning":
        # Check Police clearance, Liability, Price-Lock
        if "police" not in full_text:
            errors.append("Missing 'Police-Cleared/Checked Technicians' badge/trust panel.")
        if "liability" not in full_text and "insur" not in full_text:
            errors.append("Missing '$20M Public Liability Insurance' or coverage badge.")
        if "lock" not in full_text and "guarantee" not in full_text:
            warnings.append("Missing 'Price-Lock' badge/acknowledgment.")
            
    elif parent_name == "lifestyle-outdoors":
        if folder_name == "fantastic-landscaping":
            if "pristine" not in full_text:
                errors.append("Missing 'Pristine Site Guarantee' for landscaping cleanup.")
        elif folder_name == "mal-earthworks":
            if "byda" not in full_text and "before you dig" not in full_text:
                errors.append("Missing 'BYDA Underground Utility Checks' badge/guarantee.")
            if "pristine" not in full_text:
                errors.append("Missing 'Pristine Site Guarantee' or waste cleanup statement.")
            if "access" not in full_text:
                warnings.append("Missing machinery/access width confirmations.")
        elif folder_name == "the-lawn-ranger":
            if "gate" not in full_text:
                warnings.append("Missing 'Closed-Gate' guarantee.")
            if "rain" not in full_text and "weather" not in full_text:
                warnings.append("Missing 'Rain-Delay/Reschedule' panel.")

    elif parent_name == "trades-mechanical" and folder_name == "leons-dingo-hire":
        if "access" not in full_text:
            warnings.append("Missing tight-access width badges (e.g. 800mm narrow access).")
        if "hire" not in full_text and "rate" not in full_text:
            warnings.append("Missing rate card or hire options description.")

    status = "FAIL" if errors else "PASS"
    return {
        "status": status,
        "errors": errors,
        "warnings": warnings,
        "pricing_tier": expected_price,
        "title": title
    }

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    print(f"\n🔍 Running HIVE Web Integrity Audit across mockups in workspace...")
    print(f"   Workspace root: {base_dir}\n")

    categories = ["catering-events", "lifestyle-outdoors", "trades-mechanical", "plumbing-gas", "pest-cleaning"]
    total_sites = 0
    passed_sites = 0
    failed_sites = 0
    
    report_lines = []

    for cat in categories:
        cat_path = os.path.join(base_dir, cat)
        if not os.path.exists(cat_path):
            print(f"⚠️  Category directory not found: {cat}")
            continue

        print(f"📁 Niches in '{cat}':")
        folders = sorted([f for f in os.listdir(cat_path) if os.path.isdir(os.path.join(cat_path, f)) and f not in ["node_modules", "dist"]])
        
        for folder in folders:
            site_path = os.path.join(cat_path, folder)
            total_sites += 1
            
            res = audit_site(site_path, cat, folder)
            
            if res["status"] == "PASS":
                passed_sites += 1
                status_icon = "✅ PASS"
            else:
                failed_sites += 1
                status_icon = "❌ FAIL"
                
            print(f"  {status_icon} - {cat}/{folder} (Subscription: {res.get('pricing_tier', 'N/A')})")
            
            if res["status"] == "FAIL" or res.get("warnings"):
                for err in res.get("errors", []):
                    print(f"     └─ 🔴 ERROR: {err}")
                for warn in res.get("warnings", []):
                    print(f"     └─ 🟡 WARNING: {warn}")
                    
            report_lines.append({
                "category": cat,
                "folder": folder,
                "status": res["status"],
                "errors": res.get("errors", []),
                "warnings": res.get("warnings", []),
                "pricing_tier": res.get("pricing_tier", "N/A"),
                "title": res.get("title", "N/A")
            })
            
        print()

    print("-------------------------------------------------------------------")
    print(f"📊 SUMMARY: Audited {total_sites} directories.")
    print(f"   Passed: {passed_sites}")
    print(f"   Failed: {failed_sites}")
    print("-------------------------------------------------------------------")

    if failed_sites > 0:
        print("\n❌ Audit failed. Please resolve the errors highlighted above.\n")
        sys.exit(1)
    else:
        print("\n✅ All sites passed integrity verification!\n")
        sys.exit(0)

if __name__ == "__main__":
    main()
