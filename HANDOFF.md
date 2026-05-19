# Handoff: TFCA1402 Exam Prep — Resume from here

## What this project is

Converting a 564-slide food law lecture deck into structured exam prep materials for TFCA1402 Food Regulatory Affairs (TU Dublin, MSc Culinary Innovation & Food Product Development). The PDF-to-markdown pipeline is already complete. We are now in the exam prep phase.

---

## Directory layout (what already exists)

```
/home/helinko/Work/fipdes-law-exam-prep/
  00_resources/
    2026 Food Law slides — reflowed.md       ← MASTER SOURCE: all 564 slides as markdown
    exam-prep/
      exam-format-and-themes.md             ← DONE: exam summary (format, topics, regulations)
      questions/
        lecture-01-questions.md             ← DONE (4 questions)
        lecture-02-questions.md             ← DONE (8 questions)
        lecture-03-questions.md             ← DONE (8 questions)
        lecture-04-questions.md             ← NOT YET WRITTEN
        lecture-05-questions.md             ← NOT YET WRITTEN
        lecture-06-questions.md             ← NOT YET WRITTEN
        lecture-07-questions.md             ← NOT YET WRITTEN
        cross-cutting-questions.md          ← NOT YET WRITTEN
      active-recall-prompt.md               ← NOT YET WRITTEN
      questions-index.md                    ← NOT YET WRITTEN
    exam-simulation/                        ← directory does NOT exist yet, must be created
      lecture-01-active-recall.md           ← NOT YET WRITTEN
      lecture-02-active-recall.md           ← NOT YET WRITTEN
      lecture-03-active-recall.md           ← NOT YET WRITTEN
      lecture-04-active-recall.md           ← NOT YET WRITTEN
      lecture-05-active-recall.md           ← NOT YET WRITTEN
      lecture-06-active-recall.md           ← NOT YET WRITTEN
      lecture-07-active-recall.md           ← NOT YET WRITTEN
      cross-cutting-active-recall.md        ← NOT YET WRITTEN
```

---

## Lecture boundaries in the master source file

The master source is `/home/helinko/Work/fipdes-law-exam-prep/00_resources/2026 Food Law slides — reflowed.md`.

To extract a lecture's content for pasting into a simulation file, grep for the heading and read the appropriate line range:

| Lecture | Heading line (approx) | Slides | Key topic |
|---|---|---|---|
| L1 | ~27 | 1–42 | Introduction, EU institutions, history of food law |
| L2 | ~661 | 43–124 | Reg 178/2002 — General Food Law, EFSA, FSAI |
| L3 | ~1852 | 125–227 | FIC Reg 1169/2011 — labelling, allergens, QUID |
| L4 | ~3312 | 228–300 | Nutrition & Health Claims — Reg 1924/2006 |
| L5 | ~4310 | 301–348 | Voluntary Terms (vegan/GF/organic), Food Fraud |
| L6 | ~5026 | 349–424 | Hygiene Package — Reg 852/2004, HACCP |
| L7 | ~6253 | 425–478 | Foods of Animal Origin — Reg 853/2004 |

Revision lectures (L8/L9, slides 479–564) contain exam hints but are NOT used as source content for question files — the exam-format-and-themes.md already captures all that.

---

## Remaining tasks — do them in this order

### TASK 1: Write lecture-04-questions.md (2–3 questions max)

**Topic:** Nutrition & Health Claims (slides 228–300, Reg 1924/2006)

**Key concepts to cover:**
- Distinction: nutrition claim vs health claim (Reg 1924/2006 Annex defines permitted nutrition claims; health claims divided into Art 13.1 general, Art 13.5 newly-developed science, Art 14 reduction-of-disease-risk + children's)
- Mandatory nutrition declaration: 7 nutrients per 100g/ml in order (Energy kJ/kcal, Fat, Saturates, Carbohydrate, Sugars, Protein, Salt) — Reg 1169/2011 Art 30, Annex XIII for Reference Intakes
- "Source of" claim requires ≥15% RI per 100g/100ml (or ≥7.5% per 100ml for beverages); "high in" requires ≥30%
- Art 14 example: calcium reduces risk of osteoporotic fractures (post-menopausal women, ≥400 mg/portion, ≥1200 mg/day from all sources)
- EFSA's role: authorises individual health claims via risk assessment; published EU Register (Reg 432/2012 for the permitted Art 13.1 list)
- Debate angle: do nutrition/health claims help consumers or let unhealthy foods masquerade as healthy? (slide 545, lecturers' explicit debate prompt)

**Format to follow** (same as existing question files):

```markdown
## Q1. {exam-style title}

**Topic area:** Nutrition & Health Claims
**Difficulty:** {core / debate}
**Time budget:** 1 hour

### Question prompt

> {Essay question as it would appear on the exam paper.}

### Answer outline

1. Opening — define/scope, cite controlling regulation
2. Main body — 3–5 bullet points with regulation/article refs
3. Application — concrete examples or cases
4. Conclusion — evaluation / "fit for purpose"

### Key references to score extra marks
- Reg (EC) No 1924/2006, Article X
- Reg (EU) No 1169/2011, Article 30 / Annex XIII
- Reg (EU) No 432/2012 (permitted health claims list)
```

Write 2–3 questions. Good question mix: one explanatory ("Outline the framework for nutrition and health claims under Reg 1924/2006"), one debate ("Debate whether nutrition and health claims are genuinely helpful to consumers"), optionally one applied scenario.

---

### TASK 2: Write lecture-05-questions.md (2–3 questions max)

**Topic:** Voluntary Terms + Food Fraud (slides 301–348)

**Key concepts:**
- Vegan/vegetarian: NO EU legal definition; voluntary use under Art 36(3)(b) of 1169/2011; ISO 23662:2021 is voluntary private standard; V-label is voluntary but requires licence
- Gluten-free: Reg (EU) 828/2014 — "gluten free" ≤20 mg/kg; "very low gluten" 20–100 mg/kg; using "gluten free" on jam is misleading (all jams are naturally GF — violates Art 7 of 1169/2011)
- Organic: Reg (EU) 2018/848 — mandatory EU organic logo; certified by OCBs in Ireland (accredited by DAFM); terms "organic/bio/eco" protected
- PDO/PGI/TSG: Reg 1151/2012 — PDO (strong link to area), PGI (at least one production step), TSG (traditional composition/process, ≥25 yrs domestic use); Irish examples: Imokilly Regato (PDO), Connemara Hill Lamb (PGI), Waterford Blaa (PGI)
- Fairtrade: voluntary certification, not EU regulation; minimum price + premium
- GMO labelling: Reg (EC) 1829/2003 + 1830/2003; must declare "genetically modified" or "produced from genetically modified [ingredient]" in ingredients list
- Food fraud intro: horsemeat scandal 2013 (economic adulteration); RASFF link; Sudan 1 dye
- Farm to Fork Strategy: sustainability labelling context
- Greenwashing debate (slide 545 explicit prompt)

---

### TASK 3: Write lecture-06-questions.md (2–3 questions max)

**Topic:** Hygiene Package & HACCP (slides 349–424, Reg 852/2004)

**Key concepts:**
- Hygiene Package: set of regs from 2004, applicable from 2006 — consolidated scattered EU directives; key acts are 852/2004 (all food), 853/2004 (animal origin), 854/2004 (official controls, later replaced by 2017/625)
- Main principles of 852/2004: Farm-to-Fork; FBOs have primary responsibility; FSMS based on HACCP; traceability; food handler training
- HACCP: Article 5 of 852/2004; 7 Codex principles (hazard ID → CCP ID → critical limits → monitoring → corrective action → verification → documentation); applies to ALL FBOs except primary producers
- HACCP flexibility (Art 5 & Recital 15): Option 1 GHP only; Option 2 recognised guide (I.S. 340 in Ireland); Option 3 full FSMS
- FSAI GN 11: assessment of HACCP compliance
- Food Safety Culture: mandatory since March 2021 under Reg (EU) 2021/382 (amends 852/2004) — covers culture, allergen management, food redistribution/waste
- Registration & approval: Art 6 of 852/2004 — registration with HSE (most FBOs); approval with DAFM (animal origin businesses)
- Annex II of 852/2004: general hygiene requirements (premises, equipment, personal hygiene, water, waste, pest control, temperature control)

---

### TASK 4: Write lecture-07-questions.md (2–3 questions max)

**Topic:** Foods of Animal Origin — Reg 853/2004 (slides 425–478)

**Key concepts:**
- 853/2004 applies ONLY to foods of animal origin and is in ADDITION to 852/2004 (not a replacement)
- Scope: meat, poultry, minced meat, meat preparations, meat products, live bivalve molluscs, fishery products, raw milk, dairy products, eggs and egg products, rendered animal fats, gelatin, collagen
- ID/health marking: Reg 853/2004 Annex II — establishments that produce foods of animal origin must apply an identification mark (oval health mark format); required on packaging or directly on product
- Approval vs registration: businesses handling animal origin foods must be APPROVED (not just registered) — approval from DAFM in Ireland
- Official controls: 854/2004 was the original control regulation; replaced by 2017/625 (Official Controls Regulation) from 14 Dec 2019
- Ante-mortem and post-mortem inspection requirements at slaughter
- Cold chain obligations — temperature control requirements for different product categories
- Flexibility provisions for small establishments (Art 10 of 853/2004)

---

### TASK 5: Write cross-cutting-questions.md (2–3 questions)

**Topic:** Questions that span multiple lectures — drawn directly from the lecturer's explicit debate prompts on slide 545

These are the most exam-likely questions. The lecturer listed these verbatim as revision topics:

1. **"Can plant-based products use terms like 'milk', 'sausage', 'steak'?"** — debate from perspective of meat lobby vs vegetarian/vegan advocates
   - Meat lobby: Reg 1308/2013 (Common Organisation of Agricultural Markets) restricts dairy terms to dairy products (Art 78 + Annex VII Part III); "milk" is legally defined; similar for meat cuts
   - Vegan/vegetarian side: no EU ban on "burger" for plant-based; Art 7 of 1169/2011 (misleading) is the constraint — argue names don't mislead informed consumers; consumer choice; innovation
   - Current EU law: dairy terms ARE protected (CJEU case C-422/16 TofuTown confirmed "soya milk" etc. not permitted); meat terms are less clear-cut
   - Cite: Reg 1308/2013 Art 78 + Annex VII; Reg 1169/2011 Art 7; FSAI guidance; consumer survey data from slide 312

2. **"Is the General Food Law fit for purpose?"** — evaluate Reg 178/2002 in light of BSE, Dioxin, Horsemeat, and other crises
   - Structure: born from crises (BSE 1996 → Green Paper 1997 → White Paper 2000 → Reg 178/2002 enacted 28 Jan 2002); EFSA established; RASFF; traceability Art 18; recall Art 19
   - Arguments FOR: framework has held for 20+ years; RASFF works (Fenugreek E. coli 2011); single market maintained; clear risk analysis framework Art 6/7
   - Arguments AGAINST: horsemeat 2013 showed enforcement gaps; supply chain complexity; glyphosate/Roundup shows assessment vs management tension; COVID exposed weak crisis response; no mandatory country-of-origin for processed foods
   - Conclusion: fundamentally sound but enforcement, scope of traceability, and precautionary principle application need strengthening

3. Optionally: **Greenwashing and sustainability claims** — what is and is not allowed on a label; Farm to Fork Strategy; Reg 1169/2011 Art 36 on voluntary claims

---

### TASK 6: Write active-recall-prompt.md

**Path:** `/home/helinko/Work/fipdes-law-exam-prep/00_resources/exam-prep/active-recall-prompt.md`

This is a **reusable template** — the user copies section "## The Prompt" into a fresh ChatGPT/Claude chat, adds the lecture content and question file between the markers, then sends. The LLM runs the active recall session.

**Required sections:**

1. `## How to use this` — numbered steps: (1) open fresh chat, (2) copy the Prompt section below, (3) paste lecture content between markers, (4) paste questions file between markers, (5) send — LLM will ask Q1 and wait
2. `## The Prompt` — the verbatim text to paste into the LLM, containing:
   - Role definition: "You are an exam-preparation study partner for TFCA1402 Food Regulatory Affairs. We are practising **active recall**..."
   - Instructions for the LLM: ask Q1 → wait for user → compare against lecture content → produce comparison table (Concept | Recall ✓/〜/✗ | Notes) → focused study list → legislation-reference check → ask if user wants to continue
   - Rules: NEVER reveal answer before user attempts; compare only against provided lecture content; use exact regulation citation format (e.g. "Reg (EC) No 178/2002, Article 7"); be encouraging but precise about missing references (extra marks rule); end-of-session summary table
   - Markers: `<<<BEGIN LECTURE CONTENT>>>` ... `<<<END LECTURE CONTENT>>>` and `<<<BEGIN QUESTIONS>>>` ... `<<<END QUESTIONS>>>`
3. `## Example output format` — show the user what a good session looks like:

```
| Concept | Recall | Notes |
|---|---|---|
| Article 7 of Reg 178/2002 — Precautionary Principle | ✓ | Good — cited article number |
| 3 components of Risk Analysis | 〜 Partial | Named assessment + management, missed communication |
| BSE as case example for precautionary principle | ✗ Missed | Slides 47–49 — work this into your answer |
| EFSA does risk assessment NOT risk management | ✗ Missed | Key distinction — slide 82 |

**Focused study list:** Re-read slides 47–49 (BSE) and slide 82 (EFSA three-role split). Practice naming all three components of risk analysis cold.

**Legislation-reference check:** You should have cited Art 7 with the regulation number and year. "Precautionary principle" alone scores partial marks; "Art 7 of Reg (EC) 178/2002" scores full marks.
```

4. `## Variant: whole-deck session` — brief note on using the complete reflowed.md instead of one lecture file

---

### TASK 7: Write questions-index.md

**Path:** `/home/helinko/Work/fipdes-law-exam-prep/00_resources/exam-prep/questions-index.md`

A one-page index linking every file. Include:
- The 8 question files (L1–L7 + cross-cutting) with a one-line summary of each
- The active-recall-prompt.md with a one-line usage note
- The exam-format-and-themes.md with a one-line description
- A table mapping the 8 indicative exam topics (from slide 547) to the question file and question numbers that cover each

---

### TASK 8: Build exam-simulation files (8 files)

**Directory:** `/home/helinko/Work/fipdes-law-exam-prep/00_resources/exam-simulation/` (create it first)

Each file is a **complete, self-contained prompt** — user opens the file, copies all content, pastes into ChatGPT/Claude, and the active recall session starts immediately. No assembly required.

**Structure of each file** (e.g. `lecture-04-active-recall.md`):

```
# Active Recall Session — Lecture 4: Nutrition & Health Claims
# TFCA1402 Food Regulatory Affairs

## Instructions for use
Copy EVERYTHING below this line and paste it as your first message into a fresh ChatGPT or Claude chat.

---

You are an exam-preparation study partner for TFCA1402 Food Regulatory Affairs (TU Dublin). We are practising **active recall**: you will ask exam questions one at a time, and I will write what I remember from memory — without looking at any notes. After I answer, compare my recall against the lecture content provided and produce a structured assessment.

### Your instructions
1. Read the LECTURE CONTENT and QUESTIONS sections below.
2. Ask me the **first** question. Do not reveal the answer outline.
3. Wait for me to type my free-recall answer.
4. When I respond, produce:
   a. A **comparison table** — Concept | Recall (✓/〜/✗) | Notes — covering the key concepts expected for this question.
   b. A **focused study list** — specific slides, articles, or cases I missed.
   c. A **legislation-reference check** — any regulations or article numbers I should have cited (these earn extra marks in this exam).
5. Ask me whether to continue to the next question or revisit this one.
6. After all questions, produce a summary table: Topic Area | Strength (Strong/OK/Needs Work).

### Rules
- **Never reveal the answer before I attempt recall.** If I ask, remind me to try first.
- Compare strictly against the LECTURE CONTENT below — do not add external facts.
- Use exact regulation citation format: e.g. "Reg (EC) No 178/2002, Article 7".
- Be encouraging but precise about missing references — the lecturer marks down for "KNOWLEDGE AND REFERENCES MISSING".

### LECTURE CONTENT

<<<BEGIN LECTURE CONTENT>>>
{paste full content of lessons/lecture-04 or the relevant section of the reflowed.md here}
<<<END LECTURE CONTENT>>>

### QUESTIONS

<<<BEGIN QUESTIONS>>>
{paste full content of questions/lecture-04-questions.md here}
<<<END QUESTIONS>>>

Begin by asking me the first question.
```

**How to build each file:** Read the appropriate line range from the master source (`2026 Food Law slides — reflowed.md`) and the matching question file, then write the combined file. The lecture content sections are large (30–80 KB each) — that is expected and correct.

**Files to create:**
- `lecture-01-active-recall.md` — L1 content (lines ~27–660 of reflowed.md) + lecture-01-questions.md
- `lecture-02-active-recall.md` — L2 content (lines ~661–1851) + lecture-02-questions.md
- `lecture-03-active-recall.md` — L3 content (lines ~1852–3311) + lecture-03-questions.md
- `lecture-04-active-recall.md` — L4 content (lines ~3312–4309) + lecture-04-questions.md
- `lecture-05-active-recall.md` — L5 content (lines ~4310–5025) + lecture-05-questions.md
- `lecture-06-active-recall.md` — L6 content (lines ~5026–6252) + lecture-06-questions.md
- `lecture-07-active-recall.md` — L7 content (lines ~6253–7078) + lecture-07-questions.md
- `cross-cutting-active-recall.md` — Revision lecture content (lines ~7079–end) + cross-cutting-questions.md

---

## Style constraints for question files

- **2–3 questions max** per lecture (user's explicit instruction — earlier files at L1/L2/L3 have more questions, that's fine, don't change them, just follow the limit for new files)
- Each question must follow the exact markdown structure used in lecture-01/02/03-questions.md (read one of those files to see the format)
- Every answer outline must cite at least one specific regulation + article number
- Include at least one debate-style question per file where the topic supports it
- Do NOT add comments, explanatory notes, or headers beyond the standard template

## Important files to read before writing

Before writing any question file, read:
1. `/home/helinko/Work/fipdes-law-exam-prep/00_resources/exam-prep/exam-format-and-themes.md` — exam context and what gets marks
2. `/home/helinko/Work/fipdes-law-exam-prep/00_resources/exam-prep/questions/lecture-03-questions.md` — use as the style template
3. The relevant section of the master source for the lecture you're writing questions for

## Do NOT touch

- `/home/helinko/Work/fipdes-law-exam-prep/00_resources/exam-prep/exam-format-and-themes.md` — complete, do not modify
- `/home/helinko/Work/fipdes-law-exam-prep/00_resources/exam-prep/questions/lecture-01-questions.md` — complete
- `/home/helinko/Work/fipdes-law-exam-prep/00_resources/exam-prep/questions/lecture-02-questions.md` — complete
- `/home/helinko/Work/fipdes-law-exam-prep/00_resources/exam-prep/questions/lecture-03-questions.md` — complete
- Any file under `_build/slides_md/` — raw slide data, do not modify
- The master reflowed.md — read-only source
