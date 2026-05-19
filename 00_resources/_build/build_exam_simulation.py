#!/usr/bin/env python3
"""Build fully inlined active-recall simulation files."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MASTER = ROOT / "00_resources" / "2026 Food Law slides \u2014 reflowed.md"
QUESTIONS_DIR = ROOT / "00_resources" / "exam-prep" / "questions"
OUTPUT_DIR = ROOT / "00_resources" / "exam-simulation"


SESSIONS = [
    (
        "lecture-01-active-recall.md",
        "Lecture 1",
        "Introduction to Food Law & EU Institutions",
        27,
        660,
        "lecture-01-questions.md",
    ),
    (
        "lecture-02-active-recall.md",
        "Lecture 2",
        "General Principles of Food Law \u2014 Reg (EC) 178/2002, EFSA, FSAI",
        661,
        1851,
        "lecture-02-questions.md",
    ),
    (
        "lecture-03-active-recall.md",
        "Lecture 3",
        "Food Information to Consumers \u2014 FIC Regulation (EU) 1169/2011",
        1852,
        3311,
        "lecture-03-questions.md",
    ),
    (
        "lecture-04-active-recall.md",
        "Lecture 4",
        "Nutrition & Health Claims \u2014 Reg (EC) 1924/2006",
        3312,
        4309,
        "lecture-04-questions.md",
    ),
    (
        "lecture-05-active-recall.md",
        "Lecture 5",
        "Voluntary Terms (Vegan, Gluten-Free, Organic) & Food Fraud Introduction",
        4310,
        5025,
        "lecture-05-questions.md",
    ),
    (
        "lecture-06-active-recall.md",
        "Lecture 6",
        "The Hygiene Package & HACCP \u2014 Reg (EC) 852/2004",
        5026,
        6252,
        "lecture-06-questions.md",
    ),
    (
        "lecture-07-active-recall.md",
        "Lecture 7",
        "Foods of Animal Origin \u2014 Reg (EC) 853/2004",
        6253,
        7078,
        "lecture-07-questions.md",
    ),
    (
        "cross-cutting-active-recall.md",
        "Cross-Cutting Themes",
        "Exam Debate Topics \u2014 General Food Law, Plant-Based Terms, Greenwashing",
        7079,
        None,
        "cross-cutting-questions.md",
    ),
]


def template(lecture_n: str, title: str, lecture_content: str, questions_content: str) -> str:
    return f"""# TFCA1402 Food Regulatory Affairs \u2014 Active Recall Session
# {lecture_n}: {title}

> **How to use:** Copy the entire content of this file (from the line below this box
> to the very end) and paste it as your **first message** into a fresh
> ChatGPT or Claude chat. The AI will ask you exam questions one at a time
> and grade your recall against the lecture material.

---

You are an exam-preparation study partner for TFCA1402 Food Regulatory Affairs
(TU Dublin, MSc Culinary Innovation and Food Product Development, lecturer Sheona
Foley). We are practising **active recall**: you will ask exam questions one at a
time, and I will write what I remember from memory \u2014 without looking at any notes.
After each answer, compare my recall against the lecture content I have provided
below and produce a structured assessment.

## Your instructions

1. Read the LECTURE CONTENT and QUESTIONS sections at the bottom of this message.
2. Ask me the **first** question from the QUESTIONS section. State it clearly,
   word-for-word as written. Do **not** reveal the answer outline or any hints.
3. Wait for me to type my free-recall answer before doing anything else.
4. When I have submitted my answer, produce the following three things:

   **a. Comparison table**

   A markdown table with columns: Concept | Recall | Notes.
   - List every key concept, regulation, article number, case example, and
     definition that the source material expects for this question.
   - Mark each row: \u2713 (correctly covered), \u301c (partially covered), or
     \u2717 (missed entirely).
   - In Notes, say what was good or what was missing \u2014 be specific.

   **b. Focused study list**

   A short bullet list of exactly what I need to go back and read, citing
   slide numbers or article numbers where possible.

   **c. Legislation-reference check**

   List every regulation and article number I should have cited in my answer
   but did not. Format citations exactly as the slides do, e.g.:
   "Reg (EC) No 178/2002, Article 7 \u2014 Precautionary Principle"
   These citations earn extra marks on the real exam \u2014 flag missing ones clearly.

5. After producing the three items above, ask: "Ready for the next question, or
   would you like to revisit this one?"
6. After all questions in the QUESTIONS section have been answered, produce a
   final **session summary table**:

   | Topic area | Performance | Priority to review |
   |---|---|---|
   | e.g. Risk Analysis | Strong / OK / Needs work | Yes / No |

## Rules

- **NEVER reveal the answer, outline, or any hints before I attempt recall.**
  If I ask for the answer, remind me to try from memory first.
- Compare my answers strictly against the LECTURE CONTENT provided below.
  Do not add facts from your training data that are not in the slides.
- Always use the exact regulation citation format from the slides, e.g.
  "Reg (EC) No 852/2004, Article 5" \u2014 not shortened forms.
- Be encouraging but precise. The real exam marking deducts for
  "KNOWLEDGE AND REFERENCES MISSING" \u2014 make those gaps visible.
- If I write "skip" in response to a question, move to the next question
  without giving the answer, but flag the skipped question in the final
  summary.

---

## LECTURE CONTENT

<<<BEGIN LECTURE CONTENT>>>

{lecture_content.rstrip()}

<<<END LECTURE CONTENT>>>

---

## QUESTIONS

<<<BEGIN QUESTIONS>>>

{questions_content.rstrip()}

<<<END QUESTIONS>>>

---

Begin now: ask me the first question from the QUESTIONS section above.
"""


def line_slice(lines: list[str], start: int, end: int | None) -> str:
    start_index = start - 1
    end_index = end if end is not None else len(lines)
    return "".join(lines[start_index:end_index])


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    master_lines = MASTER.read_text(encoding="utf-8").splitlines(keepends=True)

    for filename, lecture_n, title, start, end, questions_file in SESSIONS:
        question_path = QUESTIONS_DIR / questions_file
        if not question_path.exists():
            raise FileNotFoundError(f"Missing question file: {question_path}")

        lecture_content = line_slice(master_lines, start, end)
        questions_content = question_path.read_text(encoding="utf-8")
        output = template(lecture_n, title, lecture_content, questions_content)
        output_path = OUTPUT_DIR / filename
        output_path.write_text(output, encoding="utf-8")
        print(f"Wrote {output_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
