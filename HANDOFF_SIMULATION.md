# Supplementary Handoff: Building the Exam-Simulation Files
# (Read alongside HANDOFF.md — this covers Task 8 in full detail)

---

## What these files are

Each `exam-simulation/lecture-NN-active-recall.md` file is a **single, complete markdown document** the user copies entirely and pastes as their first message into a fresh ChatGPT or Claude chat. The LLM then runs an active-recall exam-prep session automatically.

**The files are NOT templates with markers.** The lecture content and questions are literally inlined in the final file — the user copies once and is done. No assembly required.

There are 8 files to build:

| File | Lecture content source (line range in reflowed.md) | Questions source |
|---|---|---|
| `lecture-01-active-recall.md` | lines 27–660 | `exam-prep/questions/lecture-01-questions.md` |
| `lecture-02-active-recall.md` | lines 661–1851 | `exam-prep/questions/lecture-02-questions.md` |
| `lecture-03-active-recall.md` | lines 1852–3311 | `exam-prep/questions/lecture-03-questions.md` |
| `lecture-04-active-recall.md` | lines 3312–4309 | `exam-prep/questions/lecture-04-questions.md` |
| `lecture-05-active-recall.md` | lines 4310–5025 | `exam-prep/questions/lecture-05-questions.md` |
| `lecture-06-active-recall.md` | lines 5026–6252 | `exam-prep/questions/lecture-06-questions.md` |
| `lecture-07-active-recall.md` | lines 6253–7078 | `exam-prep/questions/lecture-07-questions.md` |
| `cross-cutting-active-recall.md` | lines 7079–end | `exam-prep/questions/cross-cutting-questions.md` |

**Master source path:**
`/home/helinko/Work/fipdes-law-exam-prep/00_resources/2026 Food Law slides — reflowed.md`

**Questions path:**
`/home/helinko/Work/fipdes-law-exam-prep/00_resources/exam-prep/questions/`

**Output directory** (create it if it does not exist):
`/home/helinko/Work/fipdes-law-exam-prep/00_resources/exam-simulation/`

---

## Exact format of every finished file

Build each file using **exactly** the structure below. Replace `{LECTURE_N}`, `{LECTURE_TITLE}`, `{LECTURE_CONTENT}`, and `{QUESTIONS_CONTENT}` with the real values. Everything else is boilerplate — copy it verbatim for every file.

```
# TFCA1402 Food Regulatory Affairs — Active Recall Session
# {LECTURE_N}: {LECTURE_TITLE}

> **How to use:** Copy the entire content of this file (from the line below this box
> to the very end) and paste it as your **first message** into a fresh
> ChatGPT or Claude chat. The AI will ask you exam questions one at a time
> and grade your recall against the lecture material.

---

You are an exam-preparation study partner for TFCA1402 Food Regulatory Affairs
(TU Dublin, MSc Culinary Innovation and Food Product Development, lecturer Sheona
Foley). We are practising **active recall**: you will ask exam questions one at a
time, and I will write what I remember from memory — without looking at any notes.
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
   - Mark each row: ✓ (correctly covered), 〜 (partially covered), or
     ✗ (missed entirely).
   - In Notes, say what was good or what was missing — be specific.

   **b. Focused study list**

   A short bullet list of exactly what I need to go back and read, citing
   slide numbers or article numbers where possible.

   **c. Legislation-reference check**

   List every regulation and article number I should have cited in my answer
   but did not. Format citations exactly as the slides do, e.g.:
   "Reg (EC) No 178/2002, Article 7 — Precautionary Principle"
   These citations earn extra marks on the real exam — flag missing ones clearly.

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
  "Reg (EC) No 852/2004, Article 5" — not shortened forms.
- Be encouraging but precise. The real exam marking deducts for
  "KNOWLEDGE AND REFERENCES MISSING" — make those gaps visible.
- If I write "skip" in response to a question, move to the next question
  without giving the answer, but flag the skipped question in the final
  summary.

---

## LECTURE CONTENT

<<<BEGIN LECTURE CONTENT>>>

{LECTURE_CONTENT}

<<<END LECTURE CONTENT>>>

---

## QUESTIONS

<<<BEGIN QUESTIONS>>>

{QUESTIONS_CONTENT}

<<<END QUESTIONS>>>

---

Begin now: ask me the first question from the QUESTIONS section above.
```

---

## Step-by-step instructions for the agent building these files

### Step 1 — Ensure question files exist

Before building any simulation file, the matching question file must exist and be complete. Check:

```
ls /home/helinko/Work/fipdes-law-exam-prep/00_resources/exam-prep/questions/
```

If any `lecture-NN-questions.md` or `cross-cutting-questions.md` files are missing, write those first (see HANDOFF.md Tasks 1–5).

### Step 2 — Create the output directory

```bash
mkdir -p "/home/helinko/Work/fipdes-law-exam-prep/00_resources/exam-simulation"
```

### Step 3 — For each file, read the two inputs

Use the Read tool (not Bash cat) to read:

1. The lecture slice from the master source — use `offset` and `limit` parameters:
   - `file_path`: `/home/helinko/Work/fipdes-law-exam-prep/00_resources/2026 Food Law slides — reflowed.md`
   - `offset`: the start line for that lecture (see table above)
   - `limit`: number of lines to read = (end line − start line)
   
   The master source file is large. Read each lecture in chunks if needed (the Read tool returns up to 2000 lines per call). For lectures longer than 2000 lines, make multiple Read calls and concatenate the results.

   Lecture line-count reference:
   - L1: 634 lines (27–660) — fits in one Read call
   - L2: 1191 lines (661–1851) — needs two Read calls (e.g. 661+1000, then 1661+191)
   - L3: 1460 lines (1852–3311) — needs two Read calls
   - L4: 998 lines (3312–4309) — fits in one Read call
   - L5: 716 lines (4310–5025) — fits in one Read call
   - L6: 1227 lines (5026–6252) — needs two Read calls
   - L7: 826 lines (6253–7078) — fits in one Read call
   - L8+L9 (cross-cutting): lines 7079 to end — check actual end with `wc -l`

2. The question file — read the full file:
   - `file_path`: `/home/helinko/Work/fipdes-law-exam-prep/00_resources/exam-prep/questions/lecture-NN-questions.md`

### Step 4 — Write the simulation file

Use the Write tool to write the complete combined file to:
`/home/helinko/Work/fipdes-law-exam-prep/00_resources/exam-simulation/lecture-NN-active-recall.md`

Substitute into the boilerplate template:
- `{LECTURE_N}` → e.g. `Lecture 4`
- `{LECTURE_TITLE}` → copy the lecture title from the heading in the reflowed.md, e.g. `Nutrition & Health Claims`
- `{LECTURE_CONTENT}` → the full text read from the reflowed.md for that lecture (all chunks concatenated, with newlines preserved)
- `{QUESTIONS_CONTENT}` → the full text of the matching questions file

**Critical:** Do NOT leave `{placeholder}` text in the final files. The content must be fully inlined.

### Step 5 — Verify the file

After writing, the file should:
- Contain the string `<<<BEGIN LECTURE CONTENT>>>` exactly once
- Contain the string `<<<END LECTURE CONTENT>>>` exactly once
- Contain real slide text between those markers (not a placeholder)
- Contain the questions text after `<<<BEGIN QUESTIONS>>>`
- End with "Begin now: ask me the first question from the QUESTIONS section above."

Quick check:
```bash
grep -c "<<<BEGIN LECTURE CONTENT>>>" "/home/helinko/Work/fipdes-law-exam-prep/00_resources/exam-simulation/lecture-04-active-recall.md"
# should return: 1
wc -l "/home/helinko/Work/fipdes-law-exam-prep/00_resources/exam-simulation/lecture-04-active-recall.md"
# should be well over 200 lines (content is large)
```

---

## Substitution values for each file

### lecture-01-active-recall.md
- `{LECTURE_N}` = `Lecture 1`
- `{LECTURE_TITLE}` = `Introduction to Food Law & EU Institutions`
- Lecture content: reflowed.md lines 27–660
- Questions: `lecture-01-questions.md`

### lecture-02-active-recall.md
- `{LECTURE_N}` = `Lecture 2`
- `{LECTURE_TITLE}` = `General Principles of Food Law — Reg (EC) 178/2002, EFSA, FSAI`
- Lecture content: reflowed.md lines 661–1851
- Questions: `lecture-02-questions.md`

### lecture-03-active-recall.md
- `{LECTURE_N}` = `Lecture 3`
- `{LECTURE_TITLE}` = `Food Information to Consumers — FIC Regulation (EU) 1169/2011`
- Lecture content: reflowed.md lines 1852–3311
- Questions: `lecture-03-questions.md`

### lecture-04-active-recall.md
- `{LECTURE_N}` = `Lecture 4`
- `{LECTURE_TITLE}` = `Nutrition & Health Claims — Reg (EC) 1924/2006`
- Lecture content: reflowed.md lines 3312–4309
- Questions: `lecture-04-questions.md`

### lecture-05-active-recall.md
- `{LECTURE_N}` = `Lecture 5`
- `{LECTURE_TITLE}` = `Voluntary Terms (Vegan, Gluten-Free, Organic) & Food Fraud Introduction`
- Lecture content: reflowed.md lines 4310–5025
- Questions: `lecture-05-questions.md`

### lecture-06-active-recall.md
- `{LECTURE_N}` = `Lecture 6`
- `{LECTURE_TITLE}` = `The Hygiene Package & HACCP — Reg (EC) 852/2004`
- Lecture content: reflowed.md lines 5026–6252
- Questions: `lecture-06-questions.md`

### lecture-07-active-recall.md
- `{LECTURE_N}` = `Lecture 7`
- `{LECTURE_TITLE}` = `Foods of Animal Origin — Reg (EC) 853/2004`
- Lecture content: reflowed.md lines 6253–7078
- Questions: `lecture-07-questions.md`

### cross-cutting-active-recall.md
- `{LECTURE_N}` = `Cross-Cutting Themes`
- `{LECTURE_TITLE}` = `Exam Debate Topics — General Food Law, Plant-Based Terms, Greenwashing`
- Lecture content: reflowed.md lines 7079 to end of file (revision lectures cover all themes)
- Questions: `cross-cutting-questions.md`

---

## What a correct finished file looks like (abbreviated example)

Below is what the first ~60 lines of `lecture-04-active-recall.md` should look like once built. Note that real slide text appears between the markers — no placeholders.

```markdown
# TFCA1402 Food Regulatory Affairs — Active Recall Session
# Lecture 4: Nutrition & Health Claims — Reg (EC) 1924/2006

> **How to use:** Copy the entire content of this file (from the line below this box
> to the very end) and paste it as your **first message** into a fresh
> ChatGPT or Claude chat. The AI will ask you exam questions one at a time
> and grade your recall against the lecture material.

---

You are an exam-preparation study partner for TFCA1402 Food Regulatory Affairs
(TU Dublin, MSc Culinary Innovation and Food Product Development, lecturer Sheona
Foley). We are practising **active recall** ...

[... boilerplate continues identically for every file ...]

---

## LECTURE CONTENT

<<<BEGIN LECTURE CONTENT>>>

# Lecture 4 — Week 5 (25 February 2026): Nutrition & Health Claims

**Topics:** Nutrition declaration · per-portion rules · nutrition claims · health claims · EU register · Article 13 / Article 14 · Reg 1924/2006 · FSAI guidance

**Slides:** 228–300 (73 slides)

## Slide 228

![Slide 228](food_law_slides/slide_228.png)

### Food Law & Regulatory Environment — *Course Title Slide*

*(Course title slide — see image for module / lecturer / date metadata.)*

...

## Slide 274

### What is a Health Claim?

**'Health claim'** means any claim that states, suggests or implies that a relationship
exists between a food and health.

**'Reduction of disease risk claim'** means any health claim that states, suggests or
implies that the consumption of a food reduces a risk factor in the development of a
disease.

...

[ALL slides 228–300 inlined here — approximately 998 lines of content]

<<<END LECTURE CONTENT>>>

---

## QUESTIONS

<<<BEGIN QUESTIONS>>>

## Q1. Outline the framework for nutrition and health claims under EU law

**Topic area:** Nutrition & Health Claims
**Difficulty:** core
...

[Full content of lecture-04-questions.md inlined here]

<<<END QUESTIONS>>>

---

Begin now: ask me the first question from the QUESTIONS section above.
```

---

## Notes on file size

Each completed simulation file will be large:
- Lecture content alone: 600–1500 lines of markdown
- Questions: 50–150 lines
- Boilerplate: ~60 lines
- **Total per file: roughly 700–1700 lines, 50–120 KB**

This is correct and expected. The point is that the user can copy the entire file and immediately start a session — the size is the feature, not a problem.

Do not truncate or summarise the lecture content. Paste it in full.

---

## Dependency order

Build in this sequence to avoid blocking:

1. Write any missing question files (L4, L5, L6, L7, cross-cutting) — Tasks 1–5 in HANDOFF.md
2. Write `active-recall-prompt.md` (the reusable template with markers) — Task 6 in HANDOFF.md
3. Write `questions-index.md` — Task 7 in HANDOFF.md
4. Build all 8 simulation files — this document (Task 8)

Steps 1–3 can be done in any order. Step 4 requires all question files to exist first.
