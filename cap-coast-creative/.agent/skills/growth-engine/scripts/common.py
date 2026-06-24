import csv
import fcntl
import hashlib
import os
import re
import tempfile
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


def locked_csv_update(path, fields, update):
    digest = hashlib.sha256(os.path.abspath(path).encode("utf-8")).hexdigest()[:16]
    lock_path = os.path.join(tempfile.gettempdir(), f"cap-coast-creative-{digest}.lock")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(lock_path, "w", encoding="utf-8") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        rows = read_csv(path)
        next_rows = update(rows)
        write_csv(path, rows if next_rows is None else next_rows, fields)
        fcntl.flock(lock, fcntl.LOCK_UN)


def clean(value, fallback="-"):
    value = (value or "").strip()
    return value if value else fallback


def slug(value):
    value = clean(value, "untitled").lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "untitled"


def today():
    return datetime.now().strftime("%Y-%m-%d")
