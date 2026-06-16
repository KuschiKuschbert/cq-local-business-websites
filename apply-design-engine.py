#!/usr/bin/env python3
import os
import sys
import shutil
import argparse
import re

def main():
    parser = argparse.ArgumentParser(description="Apply Cap Coast Design Engine to a target website.")
    parser.add_argument("project_path", help="Relative or absolute path to the website directory (e.g., catering-events/creative-cater)")
    parser.add_argument("--archetype", choices=["brutalist", "editorial", "nordic"], default="brutalist", help="Design archetype style (default: brutalist)")
    parser.add_argument("--palette", choices=["obsidian-dark", "terracotta-clay", "sage-garden", "desert-gold"], default="obsidian-dark", help="Color palette preset (default: obsidian-dark)")
    args = parser.parse_args()

    project_dir = os.path.abspath(args.project_path)
    if not os.path.isdir(project_dir):
        print(f"Error: Directory '{args.project_path}' does not exist.")
        sys.exit(1)

    print(f"Applying Design Engine to {project_dir} using:")
    print(f"  - Archetype: {args.archetype}")
    print(f"  - Palette:   {args.palette}")

    # Paths of Design Engine core files
    root_dir = os.path.dirname(os.path.abspath(__file__))
    de_css_src = os.path.join(root_dir, "design-engine", "design-engine.css")
    de_js_src = os.path.join(root_dir, "design-engine", "design-engine.js")

    if not os.path.exists(de_css_src) or not os.path.exists(de_js_src):
        print("Error: Design engine core files missing from root. Run script from workspace root.")
        sys.exit(1)

    # Determine destination folder inside the target project (we support Vite src/ or standard projects)
    src_dir = os.path.join(project_dir, "src")
    if os.path.isdir(src_dir):
        # Vite structure
        de_css_dest = os.path.join(src_dir, "design-engine.css")
        de_js_dest = os.path.join(src_dir, "design-engine.js")
        relative_css = "./src/design-engine.css"
        relative_js = "./src/design-engine.js"
    else:
        # Static website structure
        de_css_dest = os.path.join(project_dir, "design-engine.css")
        de_js_dest = os.path.join(project_dir, "design-engine.js")
        relative_css = "./design-engine.css"
        relative_js = "./design-engine.js"

    # Copy files
    shutil.copy2(de_css_src, de_css_dest)
    shutil.copy2(de_js_src, de_js_dest)
    print(f"Copied assets to target directory.")

    # 1. Update index.html
    html_path = os.path.join(project_dir, "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Inject stylesheet reference in <head>
        if "design-engine.css" not in html_content:
            head_close = "</head>"
            css_tag = f'  <link rel="stylesheet" href="{relative_css}">\n'
            html_content = html_content.replace(head_close, css_tag + head_close)

        # Inject script reference in <body> or <head>
        if "design-engine.js" not in html_content:
            body_close = "</body>"
            js_tag = f'  <script type="module" src="{relative_js}"></script>\n'
            html_content = html_content.replace(body_close, js_tag + body_close)

        # Inject theme attributes in the <body> tag
        body_pattern = r'<body([^>]*)>'
        match = re.search(body_pattern, html_content)
        if match:
            attrs = match.group(1)
            # Remove existing design engine attributes if present
            attrs = re.sub(r'\s*data-de-archetype="[^"]*"', '', attrs)
            attrs = re.sub(r'\s*data-de-palette="[^"]*"', '', attrs)
            # Add new attributes
            new_body = f'<body{attrs} data-de-archetype="{args.archetype}" data-de-palette="{args.palette}">'
            html_content = re.sub(body_pattern, new_body, html_content)

        # Enhance key tags (buttons, cards, headings) with engine selectors
        # Stagger cards/sections with de-reveal
        html_content = re.sub(r'class="([^"]*card[^"]*)"', r'class="\1 de-reveal"', html_content)
        # Add de-btn to custom action buttons
        html_content = re.sub(r'class="([^"]*btn[^"]*)"', r'class="\1 de-btn"', html_content)
        # Stagger section entrance reveals
        html_content = re.sub(r'<section([^>]*)>', r'<section\1 class="de-reveal">', html_content)
        # Apply kinetic titles to main h1
        html_content = re.sub(r'<h1([^>]*)>([^<]*)</h1>', r'<h1\1 class="de-kinetic-text">\2</h1>', html_content)

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print("Updated index.html templates with layout anchors and classes.")
    else:
        print("Warning: index.html not found, skipped template injection.")

    print("Successfully applied the Design Engine styling layer!")

if __name__ == "__main__":
    main()
