"""Auto-reflow the remaining slides (149-564) that don't yet have manual
slides_md output. Uses text-pattern heuristics to convert raw text into
structured markdown with an image embed, H3 title, and reformatted body.

This is intentionally a baseline: produces clean markdown for every slide
so the final assembled document is uniformly well-formatted. Any slide where
the heuristic does a poor job can be manually re-edited later.
"""

import re
from pathlib import Path

ROOT = Path("/home/helinko/Work/fipdes-law-exam-prep/00_resources")
TEXT_DIR = ROOT / "_build" / "slides_text"
MD_DIR = ROOT / "_build" / "slides_md"
L_DIR = ROOT / "_build" / "slides_layout"

# These slides are course-title repeats (per Phase C boundary detection)
COURSE_TITLE_SLIDES = {228, 301, 349, 425, 479, 512}

# Slides handled manually (Lectures 1 & 2 + L3 batch so far)
ALREADY_DONE = set(int(p.stem.split("_")[1]) for p in MD_DIR.glob("slide_*.md"))


def detect_bullets(text: str) -> list[str]:
    """Detect bullet markers in text — returns list of marker patterns found."""
    found = []
    if re.search(r"^\s*[•●▪]\s+", text, re.MULTILINE):
        found.append("•")
    if re.search(r"^o[A-Z]", text, re.MULTILINE) or re.search(r"^\s*o\s+", text, re.MULTILINE):
        found.append("o")
    if re.search(r"^\s*[❑❖✦]\s+", text, re.MULTILINE):
        found.append("❑")
    if re.search(r"^\s*[➢➣]\s+", text, re.MULTILINE):
        found.append("➢")
    if re.search(r"^\s*-\s+", text, re.MULTILINE):
        found.append("-")
    return found


def has_numbered_list(text: str) -> bool:
    """Detect a numbered list pattern (lines starting with N. or N.)"""
    return bool(re.search(r"^\s*(\d{1,2}|[ivxIVX]+|[a-d])[.)]\s+\S", text, re.MULTILINE))


def split_title_and_body(text: str) -> tuple[str, str]:
    """Pull out a likely title from the first non-empty line(s).

    Heuristic: title is up to 3 short consecutive non-empty lines at the start
    that don't contain bullet markers and are < 80 chars each.
    """
    lines = text.split("\n")
    title_lines = []
    body_start_idx = 0
    for i, line in enumerate(lines):
        s = line.strip()
        if not s:
            if title_lines:
                body_start_idx = i + 1
                break
            continue
        # Stop if line looks like body (bullets, long text, etc.)
        if re.match(r"^[•●▪oO❑❖✦➢➣\-]\s|^\d{1,2}[.)]\s|^[a-d][.)]\s", s):
            break
        if len(s) > 100:
            break
        title_lines.append(s)
        if len(title_lines) >= 3:
            body_start_idx = i + 1
            break
    title = " — ".join(title_lines).strip()
    body = "\n".join(lines[body_start_idx:]).strip() if body_start_idx else ""
    if not body and not title_lines:
        return "", text.strip()
    if not body:
        body = "\n".join(lines[len(title_lines):]).strip()
    return title, body


def normalize_bullets(text: str) -> str:
    """Convert various bullet markers to markdown '-' bullets."""
    out = []
    for line in text.split("\n"):
        # Numbered: leave as-is (markdown supports 1. 2. 3.)
        if re.match(r"^\s*\d{1,2}[.)]\s+", line):
            out.append(re.sub(r"^\s*(\d{1,2})[.)]\s+", r"\1. ", line))
            continue
        # Roman/letter sub-bullets
        if re.match(r"^\s*[a-d][.)]\s+", line):
            out.append("    " + re.sub(r"^\s*([a-d])[.)]\s+", r"\1. ", line))
            continue
        if re.match(r"^\s*[ivxIVX]+[.)]\s+", line):
            out.append("    " + re.sub(r"^\s*([ivxIVX]+)[.)]\s+", r"\1. ", line))
            continue
        # Bullets
        m = re.match(r"^\s*([•●▪❑❖✦➢➣])\s*(.*)$", line)
        if m:
            out.append(f"- {m.group(2).strip()}")
            continue
        # 'o' bullets (common in this deck)
        m = re.match(r"^o([A-Z].*)$", line)
        if m:
            out.append(f"- {m.group(1).strip()}")
            continue
        m = re.match(r"^\s*o\s+(.*)$", line)
        if m:
            out.append(f"- {m.group(1).strip()}")
            continue
        # Plain dash bullet at line start
        m = re.match(r"^\s*-\s+(.*)$", line)
        if m:
            out.append(f"- {m.group(1).strip()}")
            continue
        out.append(line)
    return "\n".join(out)


def reflow(page: int, text: str) -> tuple[str, str]:
    """Returns (layout_label, markdown_block)."""
    text = text.strip()
    if not text:
        return ("blank", f"![Slide {page}](food_law_slides/slide_{page:03d}.png)\n\n*(No extractable text — see image above.)*\n")

    if page in COURSE_TITLE_SLIDES:
        return ("course_title_template", f"""![Slide {page}](food_law_slides/slide_{page:03d}.png)

### Food Law & Regulatory Environment — *Course Title Slide*

*(Course title slide — see image for module / lecturer / date metadata.)*

Raw text:

```
{text}
```
""")

    title, body = split_title_and_body(text)
    layout_parts = []
    if has_numbered_list(body):
        layout_parts.append("numbered_list")
    bullets = detect_bullets(body)
    if bullets:
        layout_parts.append(f"bulleted_list({'/'.join(bullets)})")
    if not layout_parts:
        layout_parts.append("paragraphs")
    layout = "title_hr_body + " + ", ".join(layout_parts) if title else ", ".join(layout_parts)

    body_md = normalize_bullets(body)
    # Trim multiple blank lines to max 2
    body_md = re.sub(r"\n{3,}", "\n\n", body_md).strip()

    # Build the markdown
    parts = [f"![Slide {page}](food_law_slides/slide_{page:03d}.png)\n"]
    if title:
        parts.append(f"### {title}\n")
    if body_md:
        parts.append(body_md + "\n")
    return (layout, "\n".join(parts))


def main():
    import json
    n_written = 0
    n_skipped = 0
    for page in range(1, 565):
        if page in ALREADY_DONE:
            n_skipped += 1
            continue
        text_path = TEXT_DIR / f"slide_{page:03d}.txt"
        text = text_path.read_text(encoding="utf-8") if text_path.exists() else ""
        layout, md = reflow(page, text)
        (MD_DIR / f"slide_{page:03d}.md").write_text(md, encoding="utf-8")
        (L_DIR / f"slide_{page:03d}.json").write_text(
            json.dumps({"page": page, "layout": layout, "auto_generated": True}, indent=2),
            encoding="utf-8",
        )
        n_written += 1
    print(f"Auto-reflowed: {n_written} slides")
    print(f"Skipped (already manual): {n_skipped} slides")


if __name__ == "__main__":
    main()
