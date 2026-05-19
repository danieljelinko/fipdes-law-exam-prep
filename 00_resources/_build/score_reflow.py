"""Quality scoring for Phase H reflowed slide markdown files.

Scans every _build/slides_md/slide_NNN.md and assigns a 0-100 score based on
detectable failure patterns. Slides scoring < 70 are flagged for manual review.

Writes:
  _build/reflow_quality.json  — per-slide scores, flags, and summary stats
  (stdout) — summary table + list of flagged slides

Usage:
  python score_reflow.py
  python score_reflow.py --threshold 60   # only flag below 60
"""

import argparse
import json
import re
from pathlib import Path

ROOT = Path("/home/helinko/Work/fipdes-law-exam-prep/00_resources")
MD_DIR = ROOT / "_build" / "slides_md"
TEXT_DIR = ROOT / "_build" / "slides_text"
L_DIR = ROOT / "_build" / "slides_layout"
OUT = ROOT / "_build" / "reflow_quality.json"


def first_h3(md: str) -> str | None:
    m = re.search(r"^### (.+)$", md, re.MULTILINE)
    return m.group(1) if m else None


def score_slide(n: int, threshold: int) -> dict:
    md_path = MD_DIR / f"slide_{n:03d}.md"
    txt_path = TEXT_DIR / f"slide_{n:03d}.txt"
    layout_path = L_DIR / f"slide_{n:03d}.json"

    if not md_path.exists():
        return {"page": n, "score": 0, "flags": ["md_missing"], "auto_generated": False}

    md = md_path.read_text(encoding="utf-8")
    raw_txt = txt_path.read_text(encoding="utf-8") if txt_path.exists() else ""
    layout_data = json.loads(layout_path.read_text()) if layout_path.exists() else {}
    auto = layout_data.get("auto_generated", False)

    flags: list[str] = []
    score = 100

    # ── Title checks ──────────────────────────────────────────────
    h3 = first_h3(md)
    if h3:
        # 3+ em-dashes in title (columnar join artefact)
        if h3.count(" — ") >= 2:
            flags.append("title-em-dash-3+")
            score -= 25
        # Title too long
        if len(h3) > 90:
            flags.append("title-too-long")
            score -= 15
        # Title starts with a bullet symbol
        if h3[0] in "❑•●▪➢➣✦❖":
            flags.append("title-starts-bullet")
            score -= 15
        # Title contains bracket/paren-heavy patterns indicating garbled extraction
        if h3.count("(") + h3.count(")") > 4:
            flags.append("title-paren-heavy")
            score -= 10

    # ── Body checks ───────────────────────────────────────────────
    # Unconverted bullet symbols
    if "❑" in md:
        flags.append("unconverted-bullet-❑")
        score -= 10

    # Columnar leakage: 8+ spaces before lowercase
    if re.search(r"^\s{8,}[a-z]", md, re.MULTILINE):
        flags.append("columnar-leakage")
        score -= 20

    # Inline title-label artefact (short ALL-CAPS or CamelCase word on its own line)
    for line in md.split("\n"):
        s = line.strip()
        if 1 <= len(s.split()) <= 3 and s == s.title() and len(s) < 30 and not s.startswith(("#", "!", "-", "*", ">", "|")):
            if re.search(r"[A-Z]", s) and not re.match(r"^\d", s):
                flags.append("inline-title-fragment")
                score -= 10
                break

    # Orphan numbered items (just "1." alone on a line)
    if re.search(r"^\d{1,2}\.\s*$", md, re.MULTILINE):
        flags.append("empty-numbered-item")
        score -= 15

    # ── Coverage check ────────────────────────────────────────────
    if raw_txt.strip():
        raw_words = set(re.findall(r"\b\w{5,}\b", raw_txt.lower()))
        md_words = set(re.findall(r"\b\w{5,}\b", md.lower()))
        if raw_words:
            coverage = len(raw_words & md_words) / len(raw_words)
            if coverage < 0.80:
                flags.append(f"low-coverage-{coverage:.0%}")
                score -= 25
            elif coverage < 0.90:
                flags.append(f"medium-coverage-{coverage:.0%}")
                score -= 10

    score = max(0, score)
    return {
        "page": n,
        "score": score,
        "flags": flags,
        "auto_generated": auto,
        "needs_review": score < threshold,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", type=int, default=70)
    args = parser.parse_args()

    results = []
    for n in range(1, 565):
        results.append(score_slide(n, args.threshold))

    OUT.write_text(json.dumps(results, indent=2), encoding="utf-8")

    total = len(results)
    flagged = [r for r in results if r.get("needs_review")]
    auto_flagged = [r for r in flagged if r.get("auto_generated")]
    manual_flagged = [r for r in flagged if not r.get("auto_generated")]

    print(f"\n{'='*60}")
    print(f"Reflow Quality Report  (threshold={args.threshold})")
    print(f"{'='*60}")
    print(f"Total slides:        {total}")
    print(f"Flagged for review:  {len(flagged)}  ({100*len(flagged)/total:.0f}%)")
    print(f"  Auto-generated:    {len(auto_flagged)}")
    print(f"  Manual (check!):   {len(manual_flagged)}")

    from collections import Counter
    all_flags = Counter()
    for r in results:
        for f in r.get("flags", []):
            base = re.sub(r"-\d+%$", "", f)
            all_flags[base] += 1
    print(f"\nFlag distribution:")
    for flag, cnt in all_flags.most_common(10):
        print(f"  {flag}: {cnt}")

    if flagged:
        print(f"\nSlides needing review (score < {args.threshold}):")
        for r in sorted(flagged, key=lambda x: x["score"]):
            auto_tag = "[AUTO]" if r.get("auto_generated") else "[MANUAL]"
            print(f"  Slide {r['page']:3d} {auto_tag}  score={r['score']:3d}  {', '.join(r['flags'])}")

    print(f"\nFull results written to: {OUT}")


if __name__ == "__main__":
    main()
