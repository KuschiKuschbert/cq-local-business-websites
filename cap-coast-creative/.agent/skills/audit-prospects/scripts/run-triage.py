#!/usr/bin/env python3
import os
import sys
import importlib.util

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(script_dir))))
    
    audit_script_path = os.path.join(project_root, ".agent", "skills", "verify-integrity", "scripts", "run-audit.py")
    
    if not os.path.exists(audit_script_path):
        print(f"❌ Could not find audit script at {audit_script_path}")
        sys.exit(1)
        
    # Dynamically load the audit module
    spec = importlib.util.spec_from_file_location("run_audit", audit_script_path)
    run_audit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(run_audit)
    
    categories = ["catering-events", "lifestyle-outdoors", "trades-mechanical", "plumbing-gas", "pest-cleaning"]
    
    prospects = []
    
    for cat in categories:
        cat_path = os.path.join(project_root, cat)
        if not os.path.exists(cat_path):
            continue
            
        folders = sorted([f for f in os.listdir(cat_path) if os.path.isdir(os.path.join(cat_path, f)) and f not in ["node_modules", "dist"]])
        
        for folder in folders:
            site_path = os.path.join(cat_path, folder)
            res = run_audit.audit_site(site_path, cat, folder)
            
            # If the site fails the audit, or has warnings, or is not marked as built, it's a candidate
            # Wait, let's also read WORKSPACE.md to see if it's marked as built
            # For now, if the audit fails, it definitely needs transformation!
            if res["status"] == "FAIL":
                prospects.append({
                    "folder": f"{cat}/{folder}",
                    "niche": run_audit.CATEGORY_RULES[cat]["niche"],
                    "price_tier": res["pricing_tier"],
                    "errors": res["errors"],
                    "warnings": res["warnings"]
                })
                
    print("\n📋 THE HIVE - Digital Transformation Prospects Triage\n")
    if not prospects:
        print("🎉 **All 26 website mockups are fully compliant and modern! No triage candidates found.**\n")
        sys.exit(0)
        
    print("The following websites rely on basic/incomplete structures or have validation discrepancies:")
    print("These are high-priority candidates for digital transformation optimization:\n")
    
    print("| Folder / Prospect | Niche Category | Monthly Tier | Outstanding Issues / Missing Components |")
    print("| :--- | :--- | :--- | :--- |")
    
    for p in prospects:
        issues = []
        for err in p["errors"]:
            issues.append(f"🔴 {err}")
        for warn in p["warnings"]:
            issues.append(f"🟡 {warn}")
        issues_str = "<br>".join(issues)
        
        print(f"| **{p['folder']}** | {p['niche']} | **{p['price_tier']}** | {issues_str} |")
        
    print()
    sys.exit(0)

if __name__ == "__main__":
    main()
