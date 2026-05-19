"""Auto-reflow v2 — smarter heuristic-based slide markdown generation.

Improvements over v1 (auto_reflow_remaining.py):
1. Title fragment reassembly — detects short non-bullet lines interleaved with
   body content (classic two-column layout artefact) and merges them to a title.
2. Smarter title joining — joins with space instead of " — " when lines form a
   continuous phrase (lowercase continuation, no terminal punctuation).
3. Bullet matching without space — handles "❑Word" (no space after bullet symbol).
4. Wrapped-line collapse — merges soft-wrapped continuation lines back into their
   parent bullet/numbered item.
5. Sub-bullet detection — indented bullets become nested markdown lists.
6. List cleanup — strips trailing semicolons from numbered/lettered list items.
7. URL re-stitching — joins broken URL fragments into a single line.

Only processes slides where layout JSON has "auto_generated": true.
Preserves all manually-edited slides untouched.
"""

import json
import re
from pathlib import Path

ROOT = Path("/home/helinko/Work/fipdes-law-exam-prep/00_resources")
TEXT_DIR = ROOT / "_build" / "slides_text"
MD_DIR = ROOT / "_build" / "slides_md"
L_DIR = ROOT / "_build" / "slides_layout"

COURSE_TITLE_SLIDES = {228, 301, 349, 425, 479, 512}

# ── helpers ──────────────────────────────────────────────────────────────────

BULLET_PAT = re.compile(r"^(\s*)([•●▪❑❖✦➢➣o])\s*(.*)$")
BULLET_NO_SPACE = re.compile(r"^(\s*)([•●▪❑❖✦➢➣])(\S.*)$")   # ❑Word
NUMBERED_PAT = re.compile(r"^\s*(\d{1,2})[.)]\s+(.+)$")
LETTER_PAT = re.compile(r"^\s*([a-d])[.)]\s+(.+)$")
ROMAN_PAT = re.compile(r"^\s*([ivxIVX]+)[.)]\s+(.+)$")
URL_FRAG = re.compile(r"^https?://\S*$|^\S+/\S+$")   # loose URL fragment


def _is_bullet_line(line: str) -> bool:
    s = line.strip()
    return bool(
        BULLET_PAT.match(line)
        or BULLET_NO_SPACE.match(line)
        or NUMBERED_PAT.match(s)
        or LETTER_PAT.match(s)
        or ROMAN_PAT.match(s)
        or re.match(r"^\s*-\s+", line)
    )


def _is_title_candidate(s: str) -> bool:
    """Short non-bullet plain text — typical left-column title fragment."""
    if not s or len(s) > 50:
        return False
    if _is_bullet_line(s):
        return False
    if re.match(r"^\d{1,2}[.)]", s):
        return False
    return True


def stitch_urls(lines: list[str]) -> list[str]:
    """Join consecutive lines that look like URL fragments."""
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # if line looks like a URL fragment and next line also does, join them
        stripped = line.strip()
        if stripped.startswith("http") and i + 1 < len(lines):
            next_s = lines[i + 1].strip()
            if next_s and not next_s.startswith("http") and not next_s.startswith("!") and "/" in next_s and " " not in next_s:
                out.append(stripped + next_s)
                i += 2
                continue
        out.append(line)
        i += 1
    return out


def extract_column_title(lines: list[str]) -> tuple[str, list[str]]:
    """
    Detect left-column title fragments interleaved with body lines.
    Pattern: short (≤4 word) non-bullet fragments appear BETWEEN longer body lines.
    Collect them → join as title; return body with those fragments removed.
    """
    body_lines = [l for l in lines if l.strip()]   # non-empty
    if not body_lines:
        return "", lines

    # First pass: identify pure title-fragment lines
    # Heuristic: if 3+ consecutive fragments are ≤4 words each and non-bullet,
    # they're likely a title column leaking in.
    title_frags: list[str] = []
    body_out: list[str] = []

    for line in lines:
        s = line.strip()
        if not s:
            body_out.append(line)
            continue
        word_count = len(s.split())
        if word_count <= 4 and _is_title_candidate(s) and not any(c in s for c in ".,:;!?"):
            title_frags.append(s)
        else:
            body_out.append(line)

    # Only treat as title if we found 2-4 consistent short fragments
    # AND there are substantial body lines remaining
    real_body = [l for l in body_out if l.strip()]
    if 2 <= len(title_frags) <= 5 and len(real_body) >= 2:
        # Join title fragments sensibly
        title = " ".join(title_frags)
        return title, body_out

    return "", lines


def smart_title_join(lines: list[str]) -> str:
    """
    Join title candidate lines. Use space when lines form a continuous phrase
    (lowercase start of continuation, no terminal punctuation on prior line).
    Use ' — ' only when lines are clearly distinct phrases.
    """
    if not lines:
        return ""
    if len(lines) == 1:
        return lines[0].strip()

    parts = [lines[0].strip()]
    for line in lines[1:]:
        s = line.strip()
        prev = parts[-1]
        # Continuation: prev ends without terminal punct AND curr starts lowercase
        if not re.search(r"[.!?:;]$", prev) and s and s[0].islower():
            parts[-1] = prev + " " + s
        # Continuation: prev ends mid-word (hyphen or very short, no punct)
        elif prev.endswith("-") or (len(prev.split()) <= 2 and not re.search(r"[.!?]$", prev)):
            parts[-1] = prev.rstrip("-") + s
        else:
            parts.append(s)

    return " — ".join(parts) if len(parts) > 1 else parts[0]


def split_title_and_body_v2(text: str) -> tuple[str, str]:
    """
    Improved title/body splitter:
    1. First try to detect column-title fragments interleaved in body.
    2. Fall back to leading-lines heuristic with smart join.
    """
    lines = text.split("\n")
    stripped_lines = [l.strip() for l in lines]

    # Strategy 1: column-title interleaving detection
    title, remaining_lines = extract_column_title(lines)
    if title:
        body = "\n".join(remaining_lines).strip()
        return title, body

    # Strategy 2: leading-lines heuristic (up to 3 short non-bullet lines)
    title_lines: list[str] = []
    body_start = 0
    for i, line in enumerate(lines):
        s = line.strip()
        if not s:
            if title_lines:
                body_start = i + 1
                break
            continue
        if _is_bullet_line(line):
            break
        if re.match(r"^\d{1,2}[.)]\s", s):
            break
        if len(s) > 100:
            break
        title_lines.append(s)
        if len(title_lines) >= 3:
            body_start = i + 1
            break

    if not title_lines:
        return "", text.strip()

    title = smart_title_join(title_lines)
    # Cap title length — if > 80 chars, only first line is title, rest goes to body
    if len(title) > 80 and len(title_lines) > 1:
        title = title_lines[0].strip()
        body_start = 1  # re-include remaining lines in body

    body_lines = lines[body_start:] if body_start else lines[len(title_lines):]
    body = "\n".join(body_lines).strip()
    return title, body


def normalize_bullets_v2(text: str) -> str:
    """
    Improved bullet normalisation:
    - Handles ❑/•/etc. with or without trailing space.
    - Preserves/detects nesting via indentation.
    - Collapses wrapped continuation lines.
    - Cleans trailing semicolons from list items.
    """
    lines = text.split("\n")
    lines = stitch_urls(lines)
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        raw = line

        # Numbered list items (top level)
        m = re.match(r"^\s*(\d{1,2})[.)]\s+(.*)$", line)
        if m:
            num, content = m.group(1), m.group(2).strip()
            # Gobble continuation lines
            i += 1
            while i < len(lines):
                nxt = lines[i]
                ns = nxt.strip()
                if not ns:
                    break
                if _is_bullet_line(nxt) or re.match(r"^\s*(\d{1,2})[.)]\s", nxt):
                    break
                if re.match(r"^\s{4,}", nxt) and not _is_bullet_line(nxt):
                    # Indented sub-item — don't gobble
                    break
                content = content + " " + ns
                i += 1
            content = content.rstrip(";").strip()
            out.append(f"{num}. {content}")
            continue

        # Letter sub-items (a. b. c. d.)
        m = re.match(r"^\s*([a-d])[.)]\s+(.*)$", line)
        if m:
            ltr, content = m.group(1), m.group(2).strip()
            i += 1
            while i < len(lines):
                nxt = lines[i].strip()
                if not nxt or _is_bullet_line(lines[i]):
                    break
                content = content + " " + nxt
                i += 1
            content = content.rstrip(";").strip()
            out.append(f"    - {ltr}) {content}")
            continue

        # Roman sub-items (i. ii. iii.)
        m = re.match(r"^\s*([ivxIVX]+)[.)]\s+(.*)$", line)
        if m:
            rom, content = m.group(1), m.group(2).strip()
            i += 1
            while i < len(lines):
                nxt = lines[i].strip()
                if not nxt or _is_bullet_line(lines[i]):
                    break
                content = content + " " + nxt
                i += 1
            content = content.rstrip(";").strip()
            out.append(f"    - {rom}. {content}")
            continue

        # Bullet with or without space (❑Word or ❑ Word)
        m = re.match(r"^(\s*)([•●▪❑❖✦➢➣o])\s*(.*)", line)
        if m:
            indent = len(m.group(1))
            content = m.group(3).strip()
            if not content and m.group(2) == "o":
                # lone "o" — check if it's actually a bullet without content
                i += 1
                continue
            prefix = "    - " if indent >= 4 else "- "
            # Gobble continuation lines
            i += 1
            while i < len(lines):
                nxt = lines[i]
                ns = nxt.strip()
                if not ns:
                    break
                if _is_bullet_line(nxt):
                    break
                # continuation must not start with capital after a prior sentence end
                if re.search(r"[.!?]$", content) and ns[0:1].isupper():
                    break
                content = content + " " + ns
                i += 1
            content = content.rstrip(";").strip()
            out.append(f"{prefix}{content}")
            continue

        # Plain dash bullet
        m = re.match(r"^\s*-\s+(.*)", line)
        if m:
            content = m.group(1).strip()
            i += 1
            while i < len(lines):
                nxt = lines[i].strip()
                if not nxt or _is_bullet_line(lines[i]):
                    break
                content = content + " " + nxt
                i += 1
            out.append(f"- {content}")
            continue

        # 'o' bullet (no other char variant)
        m = re.match(r"^\s*o\s+(.*)", line)
        if m:
            content = m.group(1).strip()
            out.append(f"- {content}")
            i += 1
            continue

        # 'o' bullet without space: oWord
        m = re.match(r"^o([A-Z].*)", line)
        if m:
            content = m.group(1).strip()
            out.append(f"- {content}")
            i += 1
            continue

        out.append(raw)
        i += 1

    result = "\n".join(out)
    result = re.sub(r"\n{3,}", "\n\n", result).strip()
    return result


# ── main reflow function ──────────────────────────────────────────────────────

def img_path(page: int) -> str:
    return f"food_law_slides/slide_{page:03d}.png"


def reflow_v2(page: int, text: str) -> tuple[str, str]:
    """Returns (layout_label, markdown_block)."""
    text = text.strip()
    if not text:
        return ("blank", f"![Slide {page}]({img_path(page)})\n\n*(No extractable text — see image above.)*\n")

    if page in COURSE_TITLE_SLIDES:
        return ("course_title_template", f"""![Slide {page}]({img_path(page)})

### Food Law & Regulatory Environment — *Course Title Slide*

*(Course title slide — see image for module / lecturer / date metadata.)*

Raw text:

```
{text}
```
""")

    lines = text.split("\n")
    lines = stitch_urls(lines)
    text = "\n".join(lines)

    title, body = split_title_and_body_v2(text)

    layout_parts: list[str] = []
    if re.search(r"^\s*\d{1,2}[.)]\s", body, re.MULTILINE):
        layout_parts.append("numbered_list")
    bullets_found: list[str] = []
    for sym in ["•", "❑", "➢", "o", "-"]:
        if sym in body:
            bullets_found.append(sym)
    if bullets_found:
        layout_parts.append(f"bulleted_list({'|'.join(bullets_found)})")
    if not layout_parts:
        layout_parts.append("paragraphs")
    layout = ("title_hr_body + " if title else "") + ", ".join(layout_parts)

    body_md = normalize_bullets_v2(body)
    body_md = re.sub(r"\n{3,}", "\n\n", body_md).strip()

    parts = [f"![Slide {page}]({img_path(page)})\n"]
    if title:
        parts.append(f"### {title}\n")
    if body_md:
        parts.append(body_md + "\n")
    return (layout, "\n".join(parts))


# ── entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    n_written = n_skipped_manual = n_skipped_missing = 0
    for page in range(1, 565):
        layout_path = L_DIR / f"slide_{page:03d}.json"
        if not layout_path.exists():
            n_skipped_missing += 1
            continue
        layout_data = json.loads(layout_path.read_text(encoding="utf-8"))
        if not layout_data.get("auto_generated", False):
            n_skipped_manual += 1
            continue

        text_path = TEXT_DIR / f"slide_{page:03d}.txt"
        text = text_path.read_text(encoding="utf-8") if text_path.exists() else ""
        layout_label, md = reflow_v2(page, text)
        (MD_DIR / f"slide_{page:03d}.md").write_text(md, encoding="utf-8")
        layout_data["layout"] = layout_label
        layout_data["reflow_version"] = 2
        layout_path.write_text(json.dumps(layout_data, indent=2), encoding="utf-8")
        n_written += 1

    print(f"Re-reflowed (v2): {n_written} auto-generated slides")
    print(f"Preserved (manual): {n_skipped_manual} slides")
    print(f"Skipped (no layout JSON): {n_skipped_missing}")


if __name__ == "__main__":
    main()
