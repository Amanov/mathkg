# Kyrgyzstan's own state math standard and exam requirements
### The research that §6.1 of `curriculum-framework.md` flagged as the blocking next step, now done — with an honesty note on its limits

The previous document's five-lens review named one gap as blocking: everything in `curriculum-framework.md` was benchmarked against seven *other* countries, but never against what Kyrgyzstan's own Ministry of Education and Science (MoES) actually requires. This document does that check. It changes two of the earlier document's conclusions materially (§4 grade banding, §2's "founder" emphasis) and confirms one thing that should reduce anxiety about the whole approach: the state standard already names functional/applied literacy as a target, so MathKG's Real-Life-Context and Modelling sections are *implementing the official standard*, not working around it.

### A transparency note before anything else

`kao.kg`, `edu.gov.kg`, `unicef.org`, `open.kg`, and `testing.kg` are all blocked by this session's network egress policy — every direct-fetch attempt against the primary-source PDFs returned `EGRESS_BLOCKED`. Everything below therefore comes from web-search-indexed summaries of those documents, not from reading the primary sources line by line. That's good enough to establish structure, direction, and the live policy timeline — it is **not** good enough to hand-author a grade-by-grade content-line table with confidence. Treat the structural claims below as reliable, and treat anything marked *(unconfirmed — verify against the PDF)* as a placeholder that must be checked against the actual document before it drives content production. The primary-source PDF links are listed in full at the end so whoever has normal (non-sandboxed) access can pull the exact text.

---

## 1. The single most important fact: the ground is moving under this right now

Kyrgyzstan is mid-transition from an 11-year to a **12-year school system**, live as of the 2025/2026 academic year. This is not a stable target to design against — it's a multi-year rollout:

- The new **State Educational Standard** was approved by Cabinet of Ministers Resolution **№131 (14 March 2025)**.
- 2025/2026: children turning 5.5–6 start **grade 1 of the new 12-year system**; children who completed the pre-school program move into **grade 2** under the new standards.
- New math textbooks are being procured and distributed for **grades 1, 2, 5, and 8** first (~1.4 million copies, ~200 million som), with further grades' textbooks following in **2026/2027 and 2027/2028**.
- The transition is staged grade-by-grade, not a single cutover — so "the current standard" genuinely means something different depending on which grade you're asking about, for the next two to three years.

**What this changes in the earlier document:** §4's "grades 1–11 (4+5+2)" grade-banding assumed the old 11-year structure. That assumption needs to be replaced with the 12-year structure once the exact new grade-banding is confirmed from the primary source *(unconfirmed — the precise new primary/basic/upper split under the 12-year model needs verification against the Resolution №131 text or a MoES explainer)*. Until that's confirmed, don't finalize a grade-numbered scope-and-sequence — build the strand-and-progression logic (which is more durable) and defer exact grade labels.

**What this means practically for MathKG:** grades 1, 2, 5, and 8 are exactly where new official standards and textbooks are landing *first*. That's the highest-leverage place to start authoring MathKG content — schools and teachers in those specific grades are actively looking for materials aligned to a standard that's brand new to everyone, which is a much easier adoption story than competing with an established, familiar textbook in a grade the transition hasn't reached yet.

---

## 2. The legal/institutional stack that governs math content

| Document | Status | Covers |
|---|---|---|
| State Educational Standard (Cabinet of Ministers Resolution №131, 14 March 2025) | Current, governs the 12-year transition | All subjects, all levels |
| Math subject standard, grades 1–4 | Revised 2021–2022 under the "Okuu Keremet!" project (USAID-funded, implemented by RTI International with MoES), building on the 2014 competence-based State Standard Framework that primary grades had never actually been aligned to until this revision | Primary |
| Math subject standard, grades 5–9 | Approved by Government Resolution **№393 (22 July 2022)** | Basic/lower-secondary |
| Math subject standard, grades 10–11 | Also revised 2022 (Russian-medium version dated 2022 confirmed found; Kyrgyz-medium presumed parallel) | Upper secondary |

Each subject standard document (per its own stated structure, confirmed by search-indexed table-of-contents summaries) contains: general provisions → subject concept (goals/objectives, methodology) → subject competencies and their link to key competencies → **содержательные линии** (content lines/strands) with material distributed across grades → cross-curricular links (межпредметные связи).

**Confirmed content lines for grades 5–9** (direct quote from indexed summary): *"числа и вычисления" (numbers and calculations), "алгебраические отношения и выражения" (algebraic relations and expressions), "геометрические фигуры и их свойства" (geometric figures and their properties), "геометрические величины и их измерения" (geometric magnitudes and their measurement)*, plus others not fully enumerated in what was retrievable *(unconfirmed — the standard almost certainly also has a data/statistics/probability line and a functions line; needs verification against the PDF, since Kyrgyzstan's PISA framework and neighboring countries' standards both include one)*.

**This is directly actionable:** rename MathKG's own strand labels to match these four official content-line names (plus whatever the missing ones turn out to be) rather than the ad hoc "Number & Number Sense / Algebra / Geometry & Measurement" labels used in the earlier scope-and-sequence draft. Matching the state's own vocabulary is what makes a `Topic` legible to a Kyrgyz teacher as "this covers содержательная линия X" instead of a parallel, competing taxonomy they have to mentally translate.

**Confirmed and important:** the standard explicitly frames subject competencies as including **"элементы функциональной грамотности"** (elements of functional literacy) — i.e., PISA-style applied/real-world mathematical literacy is not an add-on MathKG is importing from outside; it is a named goal of Kyrgyzstan's own official standard. This directly validates keeping the Story-Launch/Real-Life-Context/Modelling sections of MathKG's existing template — they are the state standard's own functional-literacy goal, executed well.

---

## 3. The national exam: ОРТ (Общереспубликанское тестирование)

Run by ЦООМО (Center for Assessment in Education and Teaching Methods) via testing.kg; this is the university-entrance test, the thing Kyrgyz students, parents, and teachers actually optimize for in upper-secondary — so it's the strongest real-world pull on what gets taught and practiced in grades 9–11.

- **Main Test** (required of all applicants): four sections — Mathematics, Analogies and sentence completion, Reading and comprehension (native language), Practical grammar (native language). Total time ~3h35m excluding instructions/forms.
- **Mathematics section of the Main Test:** **60 questions, 90 minutes** *(confirmed)*.
- **Subject-specific test in Mathematics** (optional, needed for specialized/STEM-track faculties): a separate, deeper test — offered alongside chemistry, biology, physics, history, Kyrgyz/Russian language & literature, English.
- **A distinctive item format:** questions with two quantities presented in side-by-side boxed columns ("КОЛОНКА А" vs "КОЛОНКА Б"), where the task is to determine the relationship between them — the classic *quantitative-comparison* item type (structurally identical to the old US SAT quantitative-comparison format). This rewards *reasoning about relative magnitude without necessarily computing an exact value* — a distinct skill from "solve for x."

**Actionable additions this justifies, concretely:**
- Add a **quantitative-comparison** activity type to `ACTIVITY_TYPES` (`quant_compare` or similar) — it doesn't exist in the current choice list, it's a named, tested, high-stakes format, and it happens to be an excellent vehicle for exactly the "structure-spotting without brute-force computing" habit the earlier document's founder-skills section already wanted to train — so this isn't a new addition to the pedagogy, it's a new *format* for something already on the roadmap.
- Multiple-choice with 5 options (А–Д) is the Main Test's standard format for math — worth having `answer_grid`-style resources that mirror this exact response format for exam-familiarity practice in grades 9–11, separate from open-response practice used earlier for concept-building.

---

## 4. PISA 2025 — Kyrgyzstan's actual, current outcome data

This updates and supersedes the 2006/2009-only figures in the earlier document — PISA 2025 results were released in the last few weeks (Kyrgyzstan had not participated since 2009; it returned for the 2025 cycle after a 2011–2024 funding gap).

| Metric | Value |
|---|---|
| Kyrgyzstan mathematics score, 2025 | **364** |
| Kyrgyzstan mathematics score, 2006 (last comparable prior participation) | 311 |
| Overall PISA rank, 2025 | 80th of 91 participating countries/systems |
| % of Kyrgyz 15-year-olds below Level 2 in math (2025) | **49%** — roughly half the age cohort is below basic functional numeracy |
| Regional comparison, math 2025 | Kazakhstan 414, Tajikistan 382, **Kyrgyzstan 364** (Uzbekistan's math result excluded from the international comparison table) |
| Global top performers, math 2025 | B-S-J-Z (China) 612, Singapore also top-tier |

There is live public debate in Kyrgyzstan about how to read this (one outlet ran the results as "Success or Self-Deception?"): the score is genuinely up from 2006, but the gain spans nearly two decades and several skipped cycles rather than one policy period, so it's contested whether it reflects real systemic improvement or just the country finally testing again after a long gap with different sampling.

**This is the fact that should most change the earlier document's emphasis, and it does so in the same direction the five-lens review already pushed it.** With **49% of 15-year-olds below basic functional math proficiency**, a curriculum that over-indexes on rich open-ended tasks, TWM-style reasoning, and founder-adjacent modelling for the top of the distribution — while under-investing in scaffolded fluency and functional literacy for the median and below-median student — would optimize for exactly the wrong end of the actual, measured population. The earlier document's §6.6 already flagged the "unicorn founder" framing as a tail-outcome risk; this data makes it concrete: **the highest-leverage grade band for MathKG right now is shoring up basic functional numeracy at scale**, with the founder/TWM/enrichment layer available as a ceiling for students who are ready for it, not as the platform's primary pitch.

---

## 5. What actually changes in `curriculum-framework.md`

1. **§4's grade-banding needs to be re-derived against the 12-year system**, once the exact new primary/basic/upper split is confirmed from the primary source. Don't finalize grade numbers yet; the strand logic (Number → Algebra → Geometry → Data → Founder-adjacent) is more durable than the grade labels attached to it.
2. **Rename strand labels to the official content-line names** ("числа и вычисления," "алгебраические отношения и выражения," "геометрические фигуры и их свойства," "геометрические величины и их измерения," plus the still-unconfirmed remaining lines) instead of the earlier document's invented English-style labels.
3. **Prioritize grades 1, 2, 5, and 8 first** — that's where the new standard and new textbooks are landing in 2025/2026, which is both the area of highest teacher/parent demand for aligned supplementary material and the area where MathKG competes with the least-entrenched incumbent content.
4. **Add a quantitative-comparison activity type**, justified by the ОРТ's actual item format, not just as an import from the earlier TWM-inspired wishlist.
5. **Rebalance the founder-skills framing** (already flagged as a risk in the previous review) using the PISA 49%-below-Level-2 figure as the concrete justification: functional numeracy at scale first, founder/enrichment layer second — not the reverse.
6. **Keep, and now cite by name, the functional-literacy competency already in the state standard** as the legitimizing anchor for the Real-Life-Context/Modelling sections — this is no longer "a good idea borrowed from Finland/USA," it's "implementing МБС's own стандарт."

## 6. What's still genuinely open

- The exact grade-by-grade distribution of content within each content line (what specifically lands in grade 6 vs. grade 7, etc.) — needs the primary-source PDF, not search summaries.
- The full, confirmed list of all content lines for grades 5–9 (data/statistics and functions are likely but unconfirmed) and the equivalent list for grades 1–4 and 10–11.
- The precise new grade-banding under the 12-year system beyond "grades 1, 2, 5, 8 get new material first."
- Whether the субъект standards documents explicitly reference any of the international frameworks this project has been comparing against (Cambridge TWM, UK mastery, Singapore CPA) — none surfaced in this search pass, which suggests MathKG's synthesis is additive to, not already present in, the local standard.

### How to close these

Someone with unrestricted network access (i.e., not this sandboxed session) should pull the primary PDFs directly and either paste the relevant sections back in or add them to the repo under `docs/sources/` so a follow-up pass can build the precise grade-by-grade table with actual citations instead of search-snippet paraphrase:

- Math standard, grades 1–4: `https://kao.kg/wp-content/uploads/2023/01/ПС-Математика-1-4-класс.pdf`
- Math standard, grades 5–11 (Russian-medium): `https://kao.kg/wp-content/uploads/2023/09/ПС-Математика-5-11-кл-русс..pdf`
- Math standard, grades 10–11 (Russian-medium, 2022): `https://kao.kg/wp-content/uploads/2023/04/ПС-Математика-10-11-кл-русс-2022.pdf`
- KAO subject-standards index: `https://kao.kg/предметные-стандарты/` and `https://kao.kg/предметные-стандарты-2/`
- General state standard registry: `https://edu.gov.kg/legislations/30/`
- ОРТ prep guide (main test structure): `https://testing.kg/media/uploads/files/posobie-gotovimsia-ort/study_guide_main_r.pdf`
- ОРТ results/report: `https://testing.kg/media/ORT_Report_Final_ru.pdf`

Once those are in hand, the next research pass should produce an actual grade-by-grade crosswalk table (state content line → MathKG `Topic`/`Subtopic`), not just the structural summary this pass could reach.
