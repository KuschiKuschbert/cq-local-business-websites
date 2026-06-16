#!/usr/bin/env python3
import os
from common import clean, p, read_csv, rel, slug, today, write_csv

CSV = p("private_concepts.csv")
OUT = p("private_concepts")
FIELDS = ["date","business","region","niche","concept_path","readiness","primary_cta","notes"]


def cta(niche):
    n = (niche or "").lower()
    if "market" in n:
        return "View stallholder info"
    if "gallery" in n:
        return "See workshops"
    if "pizza" in n:
        return "View menu"
    return "Make an enquiry"


def css():
    return """@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;700;800&family=Outfit:wght@500;700;800&display=swap');
:root{--ink:#10201d;--muted:#58716a;--paper:#f7fbf7;--mint:#b9dccd;--sun:#e6c46d;--reef:#175d57;--line:#d8e6df}
*{box-sizing:border-box}body{margin:0;font-family:Inter,Arial,sans-serif;background:var(--paper);color:var(--ink);line-height:1.5}
.notice{background:#13221f;color:#e9f6ef;text-align:center;padding:10px 16px;font-size:14px}.wrap{width:min(1120px,calc(100% - 32px));margin:0 auto}
header{padding:20px 0;display:flex;justify-content:space-between;gap:16px;align-items:center}.brand{font-family:Outfit,sans-serif;font-weight:800;font-size:22px}.pill{border:1px solid var(--line);border-radius:999px;padding:8px 12px;color:var(--muted)}
.hero{min-height:68vh;display:grid;grid-template-columns:1.1fr .9fr;gap:36px;align-items:center;padding:48px 0 72px}.kicker{font-weight:800;color:var(--reef);text-transform:uppercase;font-size:13px;letter-spacing:.08em}
h1{font-family:Outfit,sans-serif;font-size:clamp(42px,7vw,76px);line-height:.95;margin:12px 0 18px;letter-spacing:0}p{font-size:18px;color:var(--muted);max-width:62ch}.actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:26px}
a.button{background:var(--reef);color:white;text-decoration:none;border-radius:8px;padding:14px 18px;font-weight:800;transition:.18s}a.button:hover{transform:translateY(-2px);background:#0f4843}.ghost{background:white!important;color:var(--reef)!important;border:1px solid var(--line)}
.panel{background:white;border:1px solid var(--line);border-radius:8px;padding:22px;box-shadow:0 18px 50px rgba(18,40,35,.12)}.market-card{aspect-ratio:4/3;background:linear-gradient(135deg,var(--mint),#fff7d8);display:grid;place-items:center;border-radius:8px;margin-bottom:18px;color:var(--reef);font-family:Outfit;font-size:28px;font-weight:800;text-align:center;padding:18px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:30px 0 60px}.card{background:white;border:1px solid var(--line);border-radius:8px;padding:20px}.card strong{display:block;font-family:Outfit;font-size:20px;margin-bottom:8px}
footer{border-top:1px solid var(--line);padding:24px 0;color:var(--muted)}@media(max-width:760px){.hero,.grid{grid-template-columns:1fr}header{align-items:flex-start;flex-direction:column}h1{font-size:44px}}
"""


def html(row, brief):
    business = clean(row.get("business"))
    region = clean(row.get("region"))
    niche = clean(row.get("niche"))
    action = cta(niche)
    opportunity = clean(brief.get("primary_opportunity"), "Turn social attention into clear visitor and enquiry information.")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{business} Concept | {region}</title>
  <meta name="description" content="Internal concept mockup for {business} in {region}. Not client-approved or public.">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="notice">Internal concept only. Not requested, approved, endorsed, or live for {business}.</div>
  <div class="wrap">
    <header>
      <div class="brand">{business}</div>
      <div class="pill">{region} concept</div>
    </header>
    <main>
      <section class="hero">
        <div>
          <div class="kicker">{niche}</div>
          <h1>A clearer home for market day information.</h1>
          <p>{opportunity}</p>
          <div class="actions">
            <a class="button" href="#stallholders">{action}</a>
            <a class="button ghost" href="#visit">Plan a visit</a>
          </div>
        </div>
        <aside class="panel">
          <div class="market-card">Fresh produce<br>local makers<br>weekend visitors</div>
          <p>This panel would use approved photos, hours, stallholder details, and social links only after approval.</p>
        </aside>
      </section>
      <section class="grid" id="stallholders">
        <article class="card"><strong>For Stallholders</strong><span>Simple requirements, enquiry path, and what to prepare.</span></article>
        <article class="card"><strong>For Visitors</strong><span>When to come, where to park, and what to expect.</span></article>
        <article class="card"><strong>For Updates</strong><span>Social feed link and notices without relying only on social posts.</span></article>
      </section>
    </main>
    <footer id="visit">Private Cap Coast Creative concept. Promotion and outreach both need separate approval.</footer>
  </div>
</body>
</html>
"""


briefs = {clean(row.get("business"), "").casefold(): row for row in read_csv(p("intake_opportunity_briefs.csv"))}
verify = {clean(row.get("business"), "").casefold(): row for row in read_csv(p("intake_verification.csv"))}
rows = []
os.makedirs(OUT, exist_ok=True)
for row in read_csv(p("prospect_intake.csv")):
    business = clean(row.get("business"), "")
    if not business:
        continue
    gate = verify.get(business.casefold(), {})
    brief = briefs.get(business.casefold(), {})
    if gate.get("readiness") != "promotion-review-ready" or not brief:
        continue
    folder = os.path.join(OUT, slug(business))
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "index.html"), "w", encoding="utf-8") as handle:
        handle.write(html(row, brief))
    with open(os.path.join(folder, "style.css"), "w", encoding="utf-8") as handle:
        handle.write(css())
    rows.append({"date": today(), "business": business, "region": clean(row.get("region")), "niche": clean(row.get("niche")), "concept_path": rel(os.path.join(folder, "index.html")), "readiness": gate.get("readiness"), "primary_cta": cta(row.get("niche")), "notes": "Private internal concept only; not approved, published, or sent."})
write_csv(CSV, rows, FIELDS)
print("\n".join(row["concept_path"] for row in rows) if rows else "No evidence-ready intake rows for private concept generation.")
