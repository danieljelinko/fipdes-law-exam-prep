"""Assemble the final structured slides markdown.

Reads:
  - _build/lecture_boundaries.json
  - _build/slides_text/slide_NNN.txt (per-slide text)

Writes:
  - 2026 Food Law slides.md  (final, with TOC, lecture H1s, slide H2s, embedded images)

Image paths are relative (food_law_slides/slide_NNN.png) so the document is
portable as long as it stays in 00_resources/.
"""

import json
import re
from pathlib import Path

ROOT = Path("/home/helinko/Work/fipdes-law-exam-prep/00_resources")
BOUNDARIES = ROOT / "_build" / "lecture_boundaries.json"
SLIDES_TEXT = ROOT / "_build" / "slides_text"
SLIDES_MD = ROOT / "_build" / "slides_md"  # Phase H reflowed markdown (preferred when present)
OUT = ROOT / "2026 Food Law slides.md"


def slug(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def render_slide_text(raw: str) -> str:
    """Clean per-slide raw text for markdown embedding.

    - Trim trailing whitespace.
    - Collapse 3+ blank lines to 2.
    - Leave the rest as-is (already pre-cleaned in extract_slides.py).
    """
    if not raw:
        return ""
    lines = [ln.rstrip() for ln in raw.split("\n")]
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def main():
    boundaries = json.loads(BOUNDARIES.read_text(encoding="utf-8"))
    parts = []

    # ── Header / front matter ─────────────────────────────────────────────────
    parts.append("# 2026 Food Law (TFCA1402) — Slides")
    parts.append("")
    parts.append("> **Module:** MSc Culinary Innovation and Food Product Development")
    parts.append("> **Lecturer:** Sheona Foley")
    parts.append("> **Semester:** Spring 2026 (28 Jan – 29 Apr)")
    parts.append(f"> **Total slides:** 564 · **Lectures:** {len(boundaries)}")
    parts.append("")
    parts.append("This document is auto-assembled from the original 564-slide PowerPoint export. "
                 "Each slide section embeds its rendered image (`food_law_slides/slide_NNN.png`) and "
                 "the best of two text extractions (pdfminer.six and pdftotext). Empty image-only "
                 "slides have hand-written descriptive captions.")
    parts.append("")

    # ── Table of Contents ─────────────────────────────────────────────────────
    parts.append("## Table of Contents")
    parts.append("")
    for b in boundaries:
        anchor = f"lecture-{b['lecture']}"
        parts.append(
            f"{b['lecture']}. **[Lecture {b['lecture']} — Week {b['week']} ({b['date']}): {b['title']}](#{anchor})**  "
            f"_(slides {b['start_slide']}–{b['end_slide']}, {b['n_slides']} slides)_"
        )
    parts.append("")
    parts.append("---")
    parts.append("")

    # ── Lectures ──────────────────────────────────────────────────────────────
    for b in boundaries:
        anchor = f"lecture-{b['lecture']}"
        # H1 lecture heading with explicit anchor
        parts.append(f'<a id="{anchor}"></a>')
        parts.append("")
        parts.append(f"# Lecture {b['lecture']} — Week {b['week']} ({b['date']}): {b['title']}")
        parts.append("")
        parts.append(f"**Topics:** {b['topics']}")
        parts.append("")
        parts.append(f"**Slides:** {b['start_slide']}–{b['end_slide']} ({b['n_slides']} slides)")
        parts.append("")

        # Per-slide H2 sections
        for n in range(b["start_slide"], b["end_slide"] + 1):
            parts.append(f"## Slide {n}")
            parts.append("")

            # Phase H: prefer reflowed markdown if present
            md_path = SLIDES_MD / f"slide_{n:03d}.md"
            if md_path.exists():
                parts.append(md_path.read_text(encoding="utf-8").rstrip())
                parts.append("")
                continue

            # Fallback: raw text + image (pre-Phase-H format)
            slide_text = (SLIDES_TEXT / f"slide_{n:03d}.txt").read_text(encoding="utf-8")
            slide_text = render_slide_text(slide_text)
            parts.append(f"![Slide {n}](food_law_slides/slide_{n:03d}.png)")
            parts.append("")
            if slide_text:
                parts.append(slide_text)
            else:
                parts.append("*(No extractable text — see image above.)*")
            parts.append("")

        parts.append("---")
        parts.append("")

    md = "\n".join(parts)
    OUT.write_text(md, encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"  Size: {len(md):,} chars, {md.count(chr(10)):,} lines")
    print(f"  Lectures (# Lecture): {md.count(chr(10) + '# Lecture')}")
    print(f"  Slides (## Slide):    {md.count(chr(10) + '## Slide')}")
    print(f"  Image embeds (![Slide): {md.count('![Slide')}")


if __name__ == "__main__":
    main()
