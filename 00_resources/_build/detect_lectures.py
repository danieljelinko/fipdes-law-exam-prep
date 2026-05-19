"""Auto-detect lecture boundaries from per-slide texts.

Strategy:
1. Find title slides matching "Week N: <date>" or "Lecture N: <date>" patterns.
2. Filter out the Module Outline (early slides 1-5) where every week is mentioned.
3. Build lecture intervals [start_slide, end_slide].

Output: _build/lecture_boundaries.json
"""

import json
import re
from pathlib import Path

ROOT = Path("/home/helinko/Work/fipdes-law-exam-prep/00_resources")
SLIDES_DIR = ROOT / "_build" / "slides_text"
N_PAGES = 564

# Module Outline parsed from slides 1-3: weeks with dates and topics.
# (Confirmed from earlier pdftotext sample.)
MODULE_OUTLINE = [
    (1,  "28 January 2026",  "Introduction and Overview of Module; The EU Institutions"),
    (2,  "4 February 2026",  "General Principles of Food Law Regulation (EC) No. 178/2002; EFSA, FSAI and DG Sante"),
    (3,  "11 February 2026", "Fieldtrip: Hospitality Exposition at the RDS (Asynchronous FSAI eModules)"),
    (4,  "18 February 2026", "Introduction to Food Information to Consumers (FIC) Regulation 1169/2011"),
    (5,  "25 February 2026", "Nutrition and Health Claims"),
    (6,  "4 March 2026",     "Additives, Flavourings and Supplements; Voluntary Terms (Free-From, Gluten Free, Vegetarian, Vegan, GMO, Organic)"),
    (7,  "11 March 2026",    "(Week 7 — see slides)"),
    (8,  "18 March 2026",    "The Hygiene Package & Food Safety Culture; FSAI Workshop"),
    (9,  "25 March 2026",    "The Hygiene Package and foods of animal origin"),
    (10, "15 April 2026",    "Food Fraud and other emerging issues"),
    (11, "22 April 2026",    "Final Lecture: Debate Topics, Revision and preparation for Exam"),
    (12, "29 April 2026",    "NPD Showcase — NO LECTURE"),
]

# Patterns indicating a per-week/lecture title slide
DATE_RE = re.compile(
    r"\b(\d{1,2})\s*(st|nd|rd|th)?\s*"
    r"(january|february|march|april|may)\s*2026\b",
    re.IGNORECASE,
)
WEEK_LECTURE_RE = re.compile(
    r"\b(week|lecture)\s+(\d{1,2})\b",
    re.IGNORECASE,
)


def load_slide(page: int) -> str:
    f = SLIDES_DIR / f"slide_{page:03d}.txt"
    return f.read_text(encoding="utf-8") if f.exists() else ""


def is_title_like(text: str) -> bool:
    """Title slides tend to be short."""
    return 0 < len(text.strip()) < 400


def find_candidates() -> list[tuple[int, int, str]]:
    """Return list of (page, week_num, snippet)."""
    candidates = []
    # Skip the Module Outline (pages 1-5) since they list all 12 weeks.
    for page in range(6, N_PAGES + 1):
        text = load_slide(page)
        if not is_title_like(text):
            continue
        # Need both a date AND a week/lecture number
        wm = WEEK_LECTURE_RE.search(text)
        dm = DATE_RE.search(text)
        if wm and dm:
            week_num = int(wm.group(2))
            if 1 <= week_num <= 12:
                snippet = " ".join(text.split())[:100]
                candidates.append((page, week_num, snippet))
    return candidates


def build_boundaries(candidates: list[tuple[int, int, str]]) -> list[dict]:
    """Build 12 lecture intervals.

    Use first occurrence of each week-number as its start.
    Lecture 1 starts at slide 1 by definition.
    """
    first_per_week = {}
    for page, week_num, snippet in candidates:
        if week_num not in first_per_week:
            first_per_week[week_num] = (page, snippet)

    boundaries = []
    # Lecture 1 always starts at slide 1
    starts = {1: 1}
    for week_num in range(2, 13):
        if week_num in first_per_week:
            starts[week_num] = first_per_week[week_num][0]
        else:
            starts[week_num] = None  # to fill in later

    # Forward-fill missing starts using the next known
    sorted_weeks = sorted(starts.keys())
    for i, w in enumerate(sorted_weeks):
        if starts[w] is None:
            # use prev_start + 1 as a fallback; will be flagged in output
            for j in range(i - 1, -1, -1):
                if starts[sorted_weeks[j]] is not None:
                    starts[w] = starts[sorted_weeks[j]] + 1
                    break

    # End slide = (next start - 1) or 564 for last lecture
    week_starts_sorted = sorted([(w, starts[w]) for w in starts])
    for idx, (w, s) in enumerate(week_starts_sorted):
        e = week_starts_sorted[idx + 1][1] - 1 if idx + 1 < len(week_starts_sorted) else N_PAGES
        title = next((t for (wn, _, t) in MODULE_OUTLINE if wn == w), f"Week {w}")
        date = next((d for (wn, d, _) in MODULE_OUTLINE if wn == w), "")
        boundaries.append({
            "lecture": w,
            "week": w,
            "date": date,
            "title": title,
            "start_slide": s,
            "end_slide": e,
            "n_slides": e - s + 1,
            "auto_detected": s != 1 or w == 1,
        })
    return boundaries


def main():
    cands = find_candidates()
    print(f"Found {len(cands)} candidate title slides:")
    for page, wn, snippet in cands:
        print(f"  slide {page:3d}  Week {wn:2d}  | {snippet}")
    print()

    boundaries = build_boundaries(cands)
    print("Proposed lecture boundaries:")
    print(f"{'Lecture':>7}  {'Week':>4}  {'Slides':>14}  {'Count':>5}  Title")
    print("-" * 110)
    for b in boundaries:
        rng = f"{b['start_slide']:3d}-{b['end_slide']:3d}"
        print(f"  {b['lecture']:>5}  {b['week']:>4}  {rng:>14}  {b['n_slides']:>5}  {b['title'][:60]}")

    out = ROOT / "_build" / "lecture_boundaries.json"
    out.write_text(json.dumps(boundaries, indent=2), encoding="utf-8")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
