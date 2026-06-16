#!/usr/bin/env python3
import os
import subprocess
import sys

# Directory mapping to target design engine settings
NICHE_MAPPING = {
    "catering-events": {
        "archetype": "editorial",
        "palette": "obsidian-dark"
    },
    "lifestyle-outdoors": {
        "archetype": "editorial",
        "palette": "sage-garden"
    },
    "trades-mechanical": {
        "archetype": "brutalist",
        "palette": "desert-gold"
    },
    "plumbing-gas": {
        "archetype": "brutalist",
        "palette": "obsidian-dark"
    },
    "pest-cleaning": {
        "archetype": "nordic",
        "palette": "terracotta-clay"
    }
}

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    installer_script = os.path.join(root_dir, "apply-design-engine.py")

    if not os.path.exists(installer_script):
        print("Error: apply-design-engine.py missing from workspace root.")
        sys.exit(1)

    print("Starting bulk rollout of the Cap Coast Design Engine...")
    success_count = 0
    fail_count = 0

    for niche_folder, settings in NICHE_MAPPING.items():
        niche_path = os.path.join(root_dir, niche_folder)
        if not os.path.isdir(niche_path):
            continue

        print(f"\nProcessing niche category: {niche_folder}")
        
        # List all subfolders (individual project directories)
        for subfolder in os.listdir(niche_path):
            subfolder_path = os.path.join(niche_path, subfolder)
            if not os.path.isdir(subfolder_path):
                continue
            
            # Verify if it's a project folder (contains index.html or package.json)
            if not os.path.exists(os.path.join(subfolder_path, "index.html")):
                continue

            print(f" -> Updating: {niche_folder}/{subfolder}")
            
            # Execute apply-design-engine.py
            cmd = [
                sys.executable, 
                installer_script, 
                subfolder_path, 
                "--archetype", settings["archetype"], 
                "--palette", settings["palette"]
            ]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                success_count += 1
            except subprocess.CalledProcessError as e:
                print(f"    [FAIL] Error rolling out to {subfolder}: {e.stderr}")
                fail_count += 1

    print(f"\nBulk Rollout Completed!")
    print(f"Successfully updated: {success_count} sites.")
    if fail_count > 0:
        print(f"Failed to update:     {fail_count} sites.")

if __name__ == "__main__":
    main()
