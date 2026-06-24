#!/usr/bin/env python3
import os
from common import clean, p, read_csv, rel, today, write_csv

FIELDS = [
    "date",
    "region",
    "niche",
    "source_family",
    "query",
    "quality_score",
    "use_when",
    "evidence_to_capture",
    "failure_pattern",
    "safe_next_action",
    "notes",
]

DIRECTORIES = {
    "Kawana Rockhampton": ["Direct owned website search", "Google Business Profile style result", "Rockhampton business directory", "Facebook public page"],
    "Rockhampton": ["Direct owned website search", "Google Business Profile style result", "Rockhampton business directory", "Capricorn Enterprise", "Facebook public page"],
    "Yeppoon": ["Direct owned website search", "Google Business Profile style result", "Yeppoon Capricorn Coast", "Capricorn Enterprise", "Facebook public page"],
    "Emu Park": ["Direct owned website search", "Google Business Profile style result", "Emu Park Online", "Yeppoon Capricorn Coast", "Facebook public page"],
    "Capricorn Coast": ["Direct owned website search", "Google Business Profile style result", "Yeppoon Capricorn Coast", "Capricorn Enterprise", "Facebook public page"],
}

NICHE_TERMS = {
    "cafe restaurant bar catering": ["cafe", "restaurant", "bar", "catering", "takeaway"],
    "cleaning pest control": ["cleaning", "pest control", "termite", "carpet cleaning"],
    "landscaping excavation mini digger": ["landscaping", "earthmoving", "mini digger", "excavation"],
    "salon beauty barber": ["hair salon", "beauty", "barber", "skin"],
    "art gallery workshops market": ["gallery", "workshop", "market", "artist"],
}


def attempt_failures(region, niche, attempts):
    failures = 0
    haystack_terms = [region.casefold()] + [term.casefold() for term in NICHE_TERMS.get(niche, [])]
    for attempt in attempts:
        text = " ".join([
            attempt.get("business", ""),
            attempt.get("query", ""),
            attempt.get("notes", ""),
            attempt.get("next_action", ""),
        ]).casefold()
        if haystack_terms[0] in text and any(term in text for term in haystack_terms[1:]):
            if attempt.get("result", "").startswith("no_"):
                failures += 1
    return failures


def source_family_failures(region, niche, source_family, attempts):
    failures = 0
    region_term = region.casefold()
    source_term = source_family.casefold()
    niche_terms = [term.casefold() for term in NICHE_TERMS.get(niche, [])]
    for attempt in attempts:
        text = " ".join([
            attempt.get("business", ""),
            attempt.get("query", ""),
            attempt.get("source_checked", ""),
            attempt.get("notes", ""),
            attempt.get("next_action", ""),
        ]).casefold()
        if region_term in text and source_term in text and any(term in text for term in niche_terms):
            if attempt.get("result", "").startswith("no_"):
                failures += 1
    return failures


attempts = read_csv(p("research_attempts.csv"))
rows = []
for lane in read_csv(p("research_controller.csv")):
    region = clean(lane.get("region"))
    niche = clean(lane.get("niche"))
    failures = attempt_failures(region, niche, attempts)
    for source_family in DIRECTORIES.get(region, ["Google Business Profile style result", "Facebook public page"]):
        family_failures = source_family_failures(region, niche, source_family, attempts)
        for term in NICHE_TERMS.get(niche, [niche]):
            if source_family == "Facebook public page":
                query = f'"{region}" "{term}" site:facebook.com'
                score = 92
                evidence = "business-owned public page URL, visible business name, region match, activity signal"
            elif source_family == "Google Business Profile style result":
                query = f'"{region}" "{term}" "Google" "reviews"'
                score = 88
                evidence = "business name, public profile/result URL, website/social link, region match"
            elif source_family == "Direct owned website search":
                query = f'"{region}" "{term}" "official website"'
                score = 90
                evidence = "owned website URL, business name, region match, website/service gap or conversion issue"
            else:
                query = f'"{source_family}" "{term}" "{region}"'
                score = 84
                evidence = "directory page URL, business name, category, linked website/social or clear website gap"
            if failures:
                if source_family == "Facebook public page":
                    score -= min(failures * 10, 36)
                else:
                    score += 10
                    score -= min(failures * 2, 8)
            if family_failures:
                score -= min(family_failures * 12, 36)
            use_when = "Use before broad web search, especially after locality pages dominate results."
            if failures >= 2 and source_family == "Facebook public page":
                use_when = "Use only after directory, map-style, or named-candidate sources fail."
            elif family_failures >= 2:
                use_when = "Cool down this source family; use only after a genuinely different source route fails."
            elif failures >= 2:
                use_when = "Use now because generic social search has repeatedly returned weak locality/background results."
            rows.append({
                "date": today(),
                "region": region,
                "niche": niche,
                "source_family": source_family,
                "query": query,
                "quality_score": str(score),
                "use_when": use_when,
                "evidence_to_capture": evidence,
                "failure_pattern": f"{failures} prior lane failures / {family_failures} source-family failures",
                "safe_next_action": "Research only; log source checked, capture intake only with public business-owned evidence.",
                "notes": "No contact, account login, scraping behind login, form submission, or social interaction.",
            })

rows.sort(key=lambda row: (-int(row["quality_score"]), row["region"], row["niche"], row["source_family"]))
write_csv(p("source_quality_map.csv"), rows, FIELDS)

os.makedirs(p("source_quality_maps"), exist_ok=True)
path = p("source_quality_maps", f"{today()}.md")
with open(path, "w", encoding="utf-8") as handle:
    handle.write("# Source Quality Map\n\n")
    handle.write(f"- Date: {today()}\n")
    handle.write(f"- Source routes: {len(rows)}\n")
    handle.write("- Safety: research-only source routing.\n\n")
    handle.write("## Highest Quality Routes\n\n")
    for row in rows[:12]:
        handle.write(f"- {row['region']} / {row['niche']} / {row['source_family']}: `{row['query']}` ({row['quality_score']})\n")

print(rel(path))
