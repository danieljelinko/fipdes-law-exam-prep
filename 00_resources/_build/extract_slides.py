"""Extract per-slide text from the slides PDF using pdfminer.six (primary)
with pdftotext (-layout) as fallback. Picks the better of the two per page.

Outputs one text file per page: _build/slides_text/slide_NNN.txt
and a manifest JSON _build/slides_text/_manifest.json with per-page stats.
"""

import json
import re
import subprocess
from pathlib import Path

from pdfminer.high_level import extract_text

ROOT = Path("/home/helinko/Work/fipdes-law-exam-prep/00_resources")
PDF = ROOT / "2026 Food Law slides.pdf"
OUT = ROOT / "_build" / "slides_text"
OUT.mkdir(parents=True, exist_ok=True)

N_PAGES = 564


def collapse_letterspacing(text: str) -> str:
    """Collapse 'L E C T U E R' -> 'LECTUER' on lines where most tokens are single chars.

    Heuristic: on a line, if >=60% of whitespace-separated tokens are single chars
    AND the line has at least 4 tokens, strip the spaces between single chars.
    """
    out = []
    for line in text.split("\n"):
        toks = line.split()
        if len(toks) >= 4:
            single = sum(1 for t in toks if len(t) == 1)
            if single / len(toks) >= 0.6:
                # collapse runs of single-char tokens
                fixed = re.sub(r"(?:(?<=^)|(?<=\s))(\S)(?:\s\S)+", lambda m: m.group(0).replace(" ", ""), line)
                out.append(fixed)
                continue
        out.append(line)
    return "\n".join(out)


def pdftotext_page(page: int) -> str:
    r = subprocess.run(
        ["pdftotext", "-layout", "-nopgbrk", "-f", str(page), "-l", str(page), str(PDF), "-"],
        capture_output=True, text=True, check=False,
    )
    return r.stdout if r.returncode == 0 else ""


def pdfminer_page(page: int) -> str:
    try:
        return extract_text(str(PDF), page_numbers=[page - 1]) or ""
    except Exception as e:
        return ""


def alnum_ratio(s: str) -> float:
    if not s.strip():
        return 0.0
    chars = [c for c in s if not c.isspace()]
    if not chars:
        return 0.0
    a = sum(1 for c in chars if c.isalnum())
    return a / len(chars)


def pick_best(a: str, b: str) -> tuple[str, str]:
    """Returns (chosen_text, source_label)."""
    la, lb = len(a.strip()), len(b.strip())
    ra, rb = alnum_ratio(a), alnum_ratio(b)

    # Empty cases
    if la == 0 and lb == 0:
        return "", "none"
    if la == 0:
        return b, "pdftotext"
    if lb == 0:
        return a, "pdfminer"

    # Strongly prefer non-junk
    if ra > 0.5 and rb < 0.3:
        return a, "pdfminer"
    if rb > 0.5 and ra < 0.3:
        return b, "pdftotext"

    # Otherwise prefer the one with more content (slightly favor pdfminer for linearization)
    if la >= 0.85 * lb:
        return a, "pdfminer"
    return b, "pdftotext"


def main():
    manifest = []
    for page in range(1, N_PAGES + 1):
        raw_a = pdfminer_page(page)
        raw_b = pdftotext_page(page)
        chosen, src = pick_best(raw_a, raw_b)
        chosen = collapse_letterspacing(chosen)

        # Trim trailing whitespace on each line; collapse 3+ blank lines to 2
        chosen = "\n".join(line.rstrip() for line in chosen.split("\n"))
        chosen = re.sub(r"\n{3,}", "\n\n", chosen).strip()

        out_path = OUT / f"slide_{page:03d}.txt"
        out_path.write_text(chosen, encoding="utf-8")

        manifest.append({
            "page": page,
            "source": src,
            "len_chars": len(chosen),
            "len_words": len(chosen.split()),
            "len_pdfminer": len(raw_a.strip()),
            "len_pdftotext": len(raw_b.strip()),
        })

        if page % 50 == 0 or page == 1 or page == N_PAGES:
            print(f"  page {page:3d}/564  src={src:9s}  chars={len(chosen):5d}  words={len(chosen.split()):4d}")

    (OUT / "_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    # Summary
    n_pdfminer = sum(1 for m in manifest if m["source"] == "pdfminer")
    n_pdftotext = sum(1 for m in manifest if m["source"] == "pdftotext")
    n_empty = sum(1 for m in manifest if m["len_chars"] == 0)
    short_slides = [m["page"] for m in manifest if 0 < m["len_chars"] < 20]
    print()
    print(f"Done. {n_pdfminer} from pdfminer, {n_pdftotext} from pdftotext, {n_empty} empty.")
    print(f"Short (<20 chars, non-empty): {len(short_slides)} -> {short_slides[:20]}{'...' if len(short_slides) > 20 else ''}")


if __name__ == "__main__":
    main()
