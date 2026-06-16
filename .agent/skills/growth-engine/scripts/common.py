import csv
import os
import re
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
WORKING = os.path.join(ROOT, ".agent", "memory", "working")


def p(*parts):
    return os.path.join(WORKING, *parts)


def rel(path):
    return os.path.relpath(path, ROOT)


def read_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows, fields):
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def clean(value, fallback="-"):
    value = (value or "").strip()
    return value if value else fallback


def slug(value):
    value = clean(value, "untitled").lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "untitled"


def today():
    return datetime.now().strftime("%Y-%m-%d")
