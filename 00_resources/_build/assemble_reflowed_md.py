"""Assemble a SEPARATE markdown file containing only the lectures that have
been fully reviewed and reflowed through Phase H (layout + semantic analysis).

Reads:
  - _build/lecture_boundaries.json
  - _build/slides_md/slide_NNN.md (Phase H reflowed per-slide markdown)

Writes:
  - 2026 Food Law slides — reflowed.md

A lecture is included only if EVERY slide in it has a corresponding
_build/slides_md/slide_NNN.md file. Lectures with any gap are listed at the
bottom as "Pending Phase H review".
"""

import json
from pathlib import Path

ROOT = Path("/home/helinko/Work/fipdes-law-exam-prep/00_resources")
BOUNDARIES = ROOT / "_build" / "lecture_boundaries.json"
SLIDES_MD = ROOT / "_build" / "slides_md"
OUT = ROOT / "2026 Food Law slides — reflowed.md"


def main():
    boundaries = json.loads(BOUNDARIES.read_text(encoding="utf-8"))

    # Determine which lectures are fully reflowed
    reflowed_lectures = []
    pending_lectures = []
    for b in boundaries:
        slides_in_lec = list(range(b["start_slide"], b["end_slide"] + 1))
        have_md = [n for n in slides_in_lec if (SLIDES_MD / f"slide_{n:03d}.md").exists()]
        coverage = len(have_md) / len(slides_in_lec)
        if coverage == 1.0:
            reflowed_lectures.append(b)
        else:
            pending_lectures.append((b, len(have_md), len(slides_in_lec)))

    parts = []

    # ── Header ─────────────────────────────────────────────────────────────────
    parts.append("# 2026 Food Law (TFCA1402) — Slides (Reflowed)")
    parts.append("")
    parts.append("> **This is the Phase H output.** Only lectures where every slide has been "
                 "visually reviewed and reformatted with layout + semantic analysis are included "
                 "below. Lectures still pending review are listed at the end.")
    parts.append("")
    parts.append("> **Module:** MSc Culinary Innovation and Food Product Development")
    parts.append("> **Lecturer:** Sheona Foley")
    parts.append("> **Semester:** Spring 2026 (28 Jan – 29 Apr)")
    parts.append("")
    parts.append("Each slide section embeds the rendered page image plus a clean markdown "
                 "rendering of its content (tables, lists, subheadings, definitions) chosen by "
                 "looking at both the visual layout and the semantic role of each text fragment.")
    parts.append("")

    # ── TOC of reflowed lectures ──────────────────────────────────────────────
    parts.append("## Table of Contents — Reflowed Lectures")
    parts.append("")
    for b in reflowed_lectures:
        anchor = f"lecture-{b['lecture']}"
        parts.append(
            f"{b['lecture']}. **[Lecture {b['lecture']} — Week {b['week']} "
            f"({b['date']}): {b['title']}](#{anchor})**  "
            f"_(slides {b['start_slide']}–{b['end_slide']}, {b['n_slides']} slides)_"
        )
    parts.append("")
    if pending_lectures:
        parts.append("### Pending Phase H review")
        parts.append("")
        for b, have, total in pending_lectures:
            parts.append(
                f"- Lecture {b['lecture']} — Week {b['week']} ({b['date']}): "
                f"{b['title']} — _{have}/{total} slides reflowed_"
            )
        parts.append("")
    parts.append("---")
    parts.append("")

    # ── Reflowed lectures ─────────────────────────────────────────────────────
    for b in reflowed_lectures:
        anchor = f"lecture-{b['lecture']}"
        parts.append(f'<a id="{anchor}"></a>')
        parts.append("")
        parts.append(f"# Lecture {b['lecture']} — Week {b['week']} ({b['date']}): {b['title']}")
        parts.append("")
        parts.append(f"**Topics:** {b['topics']}")
        parts.append("")
        parts.append(f"**Slides:** {b['start_slide']}–{b['end_slide']} ({b['n_slides']} slides)")
        parts.append("")
        for n in range(b["start_slide"], b["end_slide"] + 1):
            md_path = SLIDES_MD / f"slide_{n:03d}.md"
            parts.append(f"## Slide {n}")
            parts.append("")
            parts.append(md_path.read_text(encoding="utf-8").rstrip())
            parts.append("")
        parts.append("---")
        parts.append("")

    # ── Footer ────────────────────────────────────────────────────────────────
    if pending_lectures:
        parts.append("## Not yet reflowed")
        parts.append("")
        parts.append("The following lectures still use the raw text extraction in "
                     "`2026 Food Law slides.md`. They will be migrated here once Phase H "
                     "review covers all of their slides.")
        parts.append("")
        for b, have, total in pending_lectures:
            parts.append(
                f"- **Lecture {b['lecture']} — Week {b['week']} ({b['date']}): "
                f"{b['title']}** — _{have}/{total} slides reviewed_"
            )

    md = "\n".join(parts)
    OUT.write_text(md, encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"  Size: {len(md):,} chars, {md.count(chr(10)):,} lines")
    print(f"  Reflowed lectures: {len(reflowed_lectures)} of {len(boundaries)}")
    for b in reflowed_lectures:
        print(f"    L{b['lecture']}: slides {b['start_slide']}-{b['end_slide']} ({b['n_slides']} slides) — {b['title'][:60]}")
    if pending_lectures:
        print(f"  Pending: {len(pending_lectures)}")
        for b, have, total in pending_lectures:
            print(f"    L{b['lecture']}: {have}/{total} slides — {b['title'][:60]}")


if __name__ == "__main__":
    main()
