"""Post-process the docs2md output for 'Food Law extra notes.pdf' into a
clean, structured Markdown file with TOC and per-regulation H2 sections.

Steps:
  - Strip eur-lex page headers (date/time stamps) and footers (URLs, page nums)
  - De-duplicate the repeated title that appears above & below the masthead
  - Split into H2 sections at each 'SUMMARY OF:'
  - Promote ALL-CAPS subheadings (WHAT IS THE AIM, KEY POINTS, ...) to H3
  - Generate a TOC at the top
"""

import re
from pathlib import Path

ROOT = Path("/home/helinko/Work/fipdes-law-exam-prep/00_resources")
SRC = ROOT / "Food Law extra notes.pdf.md"
OUT = ROOT / "Food Law extra notes.md"


SUBHEADS = {
    "WHAT IS THE AIM OF THE REGULATION?",
    "WHAT IS THE AIM OF THE REGULATIONS?",
    "WHAT IS THE AIM OF THIS REGULATION?",
    "WHAT IS THE AIM OF THE DIRECTIVE?",
    "KEY POINTS",
    "FROM WHEN DOES THE REGULATION APPLY?",
    "FROM WHEN DOES THIS REGULATION APPLY?",
    "FROM WHEN DO THE REGULATIONS APPLY?",
    "BACKGROUND",
    "KEY TERMS",
    "MAIN DOCUMENT",
    "MAIN DOCUMENTS",
    "RELATED DOCUMENTS",
    "RELATED ACTS",
}


def slug(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def is_page_header(line: str) -> bool:
    s = line.lstrip("\x0c").strip()
    # date/time stamp like "5/14/26, 8:49 AM"
    if re.match(r"^\d+/\d+/\d+,\s*\d+:\d+\s*[AP]M$", s):
        return True
    return False


def is_page_footer(line: str) -> bool:
    s = line.strip()
    if s.startswith("https://eur-lex.europa.eu/"):
        return True
    if re.match(r"^\d+/\d+$", s):  # page number like "1/5"
        return True
    return False


def main():
    raw = SRC.read_text(encoding="utf-8")
    lines = raw.split("\n")

    # ── 1. Strip page headers/footers ─────────────────────────────────────────
    cleaned = []
    for line in lines:
        if is_page_header(line) or is_page_footer(line):
            continue
        # Drop the form-feed character if alone or remnant
        line = line.lstrip("\x0c")
        cleaned.append(line)

    # Collapse 3+ blank lines to 2
    text = "\n".join(cleaned)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    # ── 2. Split at 'SUMMARY OF:' lines ───────────────────────────────────────
    parts = re.split(r"(?m)^SUMMARY OF:\s*$", text)
    # parts[0] = preamble (page header title chunk before first SUMMARY OF)
    # parts[1..] = each regulation section (content following 'SUMMARY OF:')

    # The section title appears just BEFORE 'SUMMARY OF:' in the preamble of
    # the *previous* part. So we walk through parts and pair each section
    # with the title from the trailing lines of the previous chunk.

    sections = []  # list of (title, body)
    for i in range(1, len(parts)):
        # title comes from end of parts[i-1]
        prev_chunk = parts[i - 1].rstrip()
        # The title is the last non-empty contiguous block of 1–2 lines that
        # are short text, NOT a subhead.
        title_lines = []
        for line in reversed(prev_chunk.split("\n")):
            if not line.strip():
                if title_lines:
                    break
                continue
            if line.strip().upper() in SUBHEADS:
                break
            title_lines.append(line.strip())
            if len(title_lines) >= 3:
                break
        title_lines.reverse()
        title = " ".join(title_lines).strip()
        # Some titles are duplicated (e.g. "Authorisation procedure for additives, enzymes and ﬂavourings"
        # followed by "Authorisation procedure for additives, enzymes and / flavourings"). Pick the longest.
        if len(title_lines) > 1:
            candidates = title_lines + [" ".join(title_lines)]
            title = max(candidates, key=len)

        body = parts[i].strip()
        sections.append((title, body))

    # ── 3. For each section, strip repeated page-header titles from the body ─
    def normalize(s: str) -> str:
        s = re.sub(r"\s+", " ", s).strip()
        # Normalize en-dash, em-dash, hyphen to a single character for matching
        s = re.sub(r"[—–-]", "-", s)
        return s.lower()

    cleaned_sections = []
    for title, body in sections:
        title_norm = normalize(title)
        variants = {title_norm}
        # Also match the portion before any dash (eur-lex truncates titles at wrap)
        if "-" in title_norm:
            variants.add(title_norm.split("-", 1)[0].strip())
        body_lines = body.split("\n")
        out_lines = []
        for line in body_lines:
            ln = normalize(line)
            if ln in variants:
                continue
            out_lines.append(line)
        new_body = "\n".join(out_lines)
        # Collapse extra blank lines created by removals
        new_body = re.sub(r"\n{3,}", "\n\n", new_body).strip()
        cleaned_sections.append((title, new_body))

    # ── 4. Promote ALL-CAPS subheads to H3 ────────────────────────────────────
    def promote(body: str) -> str:
        new_lines = []
        for line in body.split("\n"):
            if line.strip().upper() in SUBHEADS:
                # Title-case the heading nicely
                heading = line.strip().title().replace("Eu", "EU").replace("Of", "of").replace("The", "the").replace("A ", "a ")
                # restore capitalisation of first word
                heading = heading[0].upper() + heading[1:] if heading else heading
                new_lines.append(f"### {heading}")
            else:
                new_lines.append(line)
        return "\n".join(new_lines)

    # ── 5. Build final markdown ───────────────────────────────────────────────
    out_parts = []
    out_parts.append("# Food Law — Extra Notes (Eur-Lex Regulation Summaries)")
    out_parts.append("")
    out_parts.append("> Companion document to **2026 Food Law slides.md** for the TFCA1402 module.")
    out_parts.append("> Source: Eur-Lex *legal-content / summaries* pages for the key food-law regulations.")
    out_parts.append("")
    out_parts.append("Each section below summarises one regulation: what it aims to do, its key "
                     "points, when it applies, background context, key terms, and links to the "
                     "underlying legal acts.")
    out_parts.append("")

    # TOC
    out_parts.append("## Table of Contents")
    out_parts.append("")
    for i, (title, _) in enumerate(cleaned_sections, 1):
        anchor = f"summary-{i}"
        out_parts.append(f"{i}. **[{title}](#{anchor})**")
    out_parts.append("")
    out_parts.append("---")
    out_parts.append("")

    # Sections
    for i, (title, body) in enumerate(cleaned_sections, 1):
        anchor = f"summary-{i}"
        out_parts.append(f'<a id="{anchor}"></a>')
        out_parts.append("")
        out_parts.append(f"## {i}. {title}")
        out_parts.append("")
        out_parts.append(promote(body))
        out_parts.append("")
        out_parts.append("---")
        out_parts.append("")

    md = "\n".join(out_parts)
    # Final tidy: collapse 3+ blank lines
    md = re.sub(r"\n{3,}", "\n\n", md)
    OUT.write_text(md, encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"  Size: {len(md):,} chars, {md.count(chr(10)):,} lines")
    print(f"  Sections: {len(cleaned_sections)}")
    for i, (title, _) in enumerate(cleaned_sections, 1):
        print(f"    {i}. {title}")


if __name__ == "__main__":
    main()
