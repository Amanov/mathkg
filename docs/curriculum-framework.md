# MathKG Curriculum Framework
### Comparative curriculum research + a Kyrgyz-language thinking-skills design for a "founder-grade" math education

This document answers three questions for the MathKG content team:

1. What do the strongest school-maths systems (Cambridge, Singapore, China, USA, UK, Finland, Estonia) actually do differently, and what should MathKG take from each?
2. What "ways of thinking" — not just topics — need to be trained deliberately so a student who grows up on MathKG has the reasoning habits of a founder, not just exam skills?
3. What is true about the **Kyrgyz language** that should shape how we write lessons and word problems, so the language itself works *for* mathematical thinking instead of against it?

It also maps every recommendation onto the data model that already exists in this repo (`Topic → Subtopic → SubSubtopic → Resource`, `LEARNING_GOALS`, `ACTIVITY_TYPES`), because the lesson template already in `apps/resources/data/*.py` (Story Launch → Curiosity Question → Real Life Context → CPA Activity → Number Sense → Visual Models → Practice → Fluency → Challenge → Think & Reason → Reflect → Assess) is already, whether intentionally or not, a synthesis of several of these systems. This doc validates that structure, closes its gaps, and gives it a topic scope-and-sequence.

---

## 1. What each system actually contributes (not the folk version)

| System | What it's actually good at | The one mechanism worth copying |
|---|---|---|
| **Singapore** | Concrete→Pictorial→Abstract (CPA) sequencing; number bonds; the **bar model** for turning word problems into diagrams before algebra exists | Never introduce an abstract symbol before the concept has lived as an object and a picture. Every new concept gets a CPA triplet. |
| **China (mainland curriculum + "teaching with variation")** | "Two Basics" (扎实的基础知识, 基本技能) — deep procedural fluency as the substrate reasoning runs on; **变式教学 (bianshi) / variation theory**: deliberately varying one feature of a problem at a time (conceptual variation = same concept, different representations; procedural variation = same procedure, systematically changing what's given/unknown) so the invariant structure becomes visible by contrast | Fluency practice should never be "20 random problems." It should be a *sequence* where each problem changes exactly one thing from the last, so the student's attention is pulled to what matters. |
| **Cambridge (Primary/Lower Secondary Maths + "Thinking and Working Mathematically")** | An explicit, examinable taxonomy of mathematical *behaviour*, not just content — the **TWM framework**: 4 pairs of characteristics — Specialising & Generalising, Conjecturing & Convincing, Characterising & Classifying, Critiquing & Improving | Every rich task should be tagged by which TWM pair it trains, the same way MathKG already tags `learning_goal`. This is the single biggest structural gap in the current model (see §3). |
| **UK (National Curriculum + NCETM/White Rose "Teaching for Mastery")** | The "5 Big Ideas": Coherence (small, connected steps), Representation & Structure, Mathematical Thinking, Fluency, **Variation** (procedural + conceptual — the UK imported this directly from China); also NRICH's rich-task culture ("Convince Me", "Always/Sometimes/Never", "Odd One Out") | Whole-class-together small steps beat tracked/streamed fast-forward. Depth before breadth: "keep together, go deeper," not "move the fast kids ahead." |
| **USA (Common Core's 8 Standards for Mathematical Practice)** | Not content standards but **process** standards, cross-cutting every grade: (1) make sense of problems & persevere, (2) reason abstractly & quantitatively, (3) construct viable arguments & critique reasoning, (4) model with mathematics, (5) use tools strategically, (6) attend to precision, (7) look for and make use of structure, (8) look for and express regularity in repeated reasoning | These 8 are a checklist you can literally run against every `Resource` you author: "which of the 8 practices does this activity actually exercise?" (4) *model with mathematics* is the direct academic ancestor of "turn a business problem into an equation," i.e. founder-thinking. |
| **Finland** | Delayed formal instruction (no formal reading/arithmetic pressure before ~age 7), **phenomenon-based learning** (start from a real, messy, cross-subject question, not from a topic label), low-stakes formative assessment, deep trust in teacher judgement, "less but deeper" | Every unit should open with a real phenomenon/question the child cares about *before* naming the maths topic. MathKG's "Story Launch / Curiosity Question / Real Life Context" block already does exactly this — keep it, and make sure it's never skipped for the sake of covering more content. |
| **Estonia** (#1 in Europe on PISA maths; ~13% top performers vs 9% OECD average, and unusually *equitable* — outcome depends less on family background than almost anywhere else) | A coherent, tightly spiralled curriculum + genuinely subject-specialist, master's-level teachers; **computational thinking and digital/algorithmic literacy taught as a core strand from primary school**, not bolted on; strong formative feedback culture | Treat "compute/estimate/verify with a tool" and basic algorithmic thinking (sequences, conditionals, debugging one's own reasoning) as a *maths* strand from an early grade, not something deferred to a separate "informatics" class. This is also the most direct on-ramp to "build a startup" later. |

**Net takeaway:** the countries with the best outcomes agree that *content coverage is not the bottleneck — thinking habits are*. Singapore/China supply the fluency and representational machinery; UK/Cambridge/USA supply an explicit vocabulary for the reasoning itself; Finland/Estonia supply the motivational and equity conditions that let the other two actually stick. MathKG needs all three layers, not just a topic list.

---

## 2. The "founder" argument, made concrete

"Kids who graduate can build a unicorn for Kyrgyzstan" is not a slogan you get from covering more topics faster. It comes from specific, trainable habits that show up in the research above and that a founder uses daily:

- **Fermi estimation / quantitative sense-making** — "roughly how big is this market/cost/risk?" before any precise calculation. (USA Practice 2 + 4; Singapore number sense.)
- **Modelling under uncertainty** — turning a fuzzy real situation into a formal structure (equation, graph, table), checking it against reality, and revising it. (USA Practice 4; Finland's phenomenon-based framing.)
- **Conjecture → test → revise, without fear of being wrong** — a founder's entire job is proposing something unproven and updating on evidence. This is *literally* Cambridge TWM's Conjecturing/Convincing pair and NRICH's "Always/Sometimes/Never."
- **Critiquing and improving a plan/argument** — spotting the flaw in your own or someone else's reasoning before the market does. (TWM Critiquing/Improving; USA Practice 3; the existing "Explain the Mistake" activity.)
- **Structure-spotting across superficially different problems** — recognising that a pricing problem and a physics-rate problem are "the same shape." (USA Practice 7–8; China's variation theory trains exactly this by contrast.)
- **Computational/algorithmic fluency** — comfortable formalising a process into steps a machine (or a spreadsheet, or an employee) can follow. (Estonia's strand.)
- **Data and statistical literacy** — reading evidence, spotting a misleading chart, understanding risk and probability. (Increasingly central in UK/Cambridge upper-secondary and USA; currently the weakest strand in most Kyrgyz-region curricula and worth over-investing in.)

None of this argues for *less* arithmetic fluency — the opposite. Estimation, modelling and structure-spotting are cheap illusions without real number sense and procedural fluency underneath (China's "Two Basics" point). The recommendation is: keep the fluency machinery MathKG already has, and make sure every unit also produces at least one artifact in each of the categories above by upper-primary/lower-secondary.

> **Caveat, stated plainly:** this whole section is a bet on *far transfer* — that classroom habits (conjecturing, critiquing, structure-spotting) carry over to real-world entrepreneurial judgement. Near-transfer within mathematics is well evidenced; transfer to an unrelated domain like founding a company is one of the more contested claims in the learning sciences. Treat §2 as the hypothesis the curriculum is testing, not a proven causal chain — and don't let "unicorn founder" become the only north star. Optimising the whole system for a tail outcome (a handful of future founders) at the expense of the median outcome (a numerate population) is a real failure mode; founder-relevant skills should sit as a layer on top of broad numeracy, not replace it as the goal every lesson is justified against.

---

## 3. Gap analysis against the existing MathKG data model

The lesson template already implemented in `apps/resources/data/koshuu_1_digit_data.py` is unusually well aligned with the research above:

| Existing section | Maps to |
|---|---|
| 📖 Сабак (Story Launch, Curiosity Question, Real Life Context) | Finland phenomenon-based launch |
| 🧠 Conceptual Understanding (CPA Activity, Number Sense, Visual Models, Manipulatives) | Singapore CPA + bar model |
| ✍ Practice (Guided/Independent/Interactive) | Standard gradual-release pedagogy (all systems) |
| ⚡ Fluency (Daily 5, Speed Practice, Number Bonds, Fact Fluency) | Singapore/China procedural fluency ("Two Basics") |
| 🧩 Challenge (NRICH Investigation, Open Problems, Math Puzzles) | Cambridge/NRICH rich tasks |
| 💭 Think & Reason (Convince Me, Explain the Mistake, Always/Sometimes/Never, Odd One Out, Which One Doesn't Belong) | Cambridge TWM (partially — see gap below) + USA Practice 3 |
| 🎯 Reflect (Planning, Monitoring, Evaluating) | Metacognition / self-regulated learning (Finland, Estonia formative-assessment culture) |
| 📊 Assess (Exit Ticket, Quiz, Mastery Check, Diagnostic) | Mastery learning / Bloom |

**What's missing, concretely:**

1. **Variation is not a first-class tag.** `LEARNING_GOALS` has `patterns`, `fluency`, `discovery`, etc., but nothing that captures "this sequence of problems varies one feature at a time on purpose." Without it, item-writers will keep generating i.i.d. random problems (which the `data/*.py` generator files currently suggest they do), losing the single most distinctive Chinese/UK-mastery technique. **Recommend adding a `variation` learning goal** ("Вариациялоо" / systematic variation sets) and, at the `Resource` authoring level, a convention that a `worksheet` resource tagged `variation` documents *what one thing changes between each item*.
2. **TWM's "Specialising & Generalising" pair has no home.** "Odd One Out"/"Which One Doesn't Belong" covers Characterising/Classifying; "Convince Me"/"Always-Sometimes-Never" covers Conjecturing/Convincing; "Explain the Mistake" covers Critiquing/Improving — but there is no activity type for *try a few small cases, then state the general rule*, which is the most important habit for a future founder (pattern → hypothesis → generalised rule is literally the scientific-startup loop). **Recommend adding a `specialise_generalise` learning goal** and pairing it with the existing `four_in_row`/`create_question`/`digit_puzzle` activity types, or a new lightweight activity type like `pattern_hunt`.
3. **No explicit "Model / Estimate" tag.** `modelling` exists in `LEARNING_GOALS` (good — it's already there), but nothing in the current section layout (`koshuu_1_digit_data.py`) surfaces it as its own block the way "Fluency" and "Challenge" are surfaced. Recommend a **🧮 Model & Estimate** section (Fermi Question, Data Story, Spreadsheet/Tool Check) added to the per-topic template from upper-primary onward.
4. **No computational-thinking strand.** Nothing in `ACTIVITY_TYPES`/`LEARNING_GOALS` corresponds to Estonia's algorithmic-literacy strand. This doesn't need to be "coding" — at primary level it can be unplugged (sequences, loops-as-repeated-patterns, debugging a wrong recipe); by lower-secondary it can use a simple visual tool. Recommend it live as its own `Topic` ("Эсептөө ыкмалары" / Computational thinking) threaded across grades, tagged with a new `algorithmic` learning goal.
5. **Statistics/data literacy is underweighted relative to its founder-relevance.** Worth its own `Topic` with a dedicated subtopic per grade band from grade 3 up (see scope-and-sequence below), not just a chapter near the end of a school year the way many regional programmes currently treat it.

None of this requires touching the existing schema's shape — `LEARNING_GOALS` and `ACTIVITY_TYPES` are just choice lists, and `Topic/Subtopic/SubSubtopic` already supports arbitrary depth — it's additive.

> **Tension to resolve, not ignore:** §1 credits Finland with "less but deeper," and this section then proposes four *additional* strands on top of a template that already has 8 sections per subtopic. Adding without cutting anything contradicts the principle being cited. Before building all of this out, name what a given grade band will teach *less* of (fewer topics per year, not just more tags per topic) so depth is actually gained rather than the surface area of the curriculum silently growing. Also note: adding a `variation`/`specialise_generalise` tag to the database is bookkeeping, not an intervention — nothing improves until the resources behind those tags are actually authored well.

---

## 4. Scope-and-sequence skeleton (grades 1–11, Kyrgyz system: 4 + 5 + 2)

Five strands run through every grade band; what changes is depth and the dominant technique borrowed from each system.

| Grade band | Number & Number Sense | Algebra / Patterns | Geometry & Measurement | Data & Probability | Founder-adjacent strand |
|---|---|---|---|---|---|
| **1–2** (age 7–8) | Number bonds to 10/20, place value via CPA; **delay formal written algorithms** (Finland) until concepts are solid | Pattern-spotting with objects, no symbols yet | Shape, direct comparison of length/mass/capacity | Simple pictograms/tally from real classroom data | Unplugged sequencing ("first, then, finally"); Story-Launch-first for every unit |
| **3–4** | Place value to 10,000+, all 4 operations fluent (China-style variation drills for fluency), fractions as CPA | Bar-model algebra (Singapore): unknowns as boxes, not letters yet | Perimeter/area by counting → formula; angle intro | Bar charts, mean as "fair share," simple probability language | First "Specialise & Generalise" tasks: find the rule from 3–4 worked examples |
| **5–6** | Fractions/decimals/percent unified via bar model + number line; ratio intro | Letters as unknowns introduced only after bar-model fluency; simple equations | Coordinate plane; area/volume formulas derived, not memorised | Data collection projects; mean/median/mode meaningfully distinguished | First Fermi-estimation tasks; first "Explain the Mistake" peer-critique routine formalised |
| **7–8** | Directed numbers, indices, standard form | Linear equations/graphs, sequences (explicit + recursive — natural bridge to algorithmic thinking) | Similarity, Pythagoras, transformations | Probability with sample spaces; misleading-graph critique tasks (USA Practice 3 applied to media literacy) | Simple spreadsheet/tool-based modelling; intro "build vs. buy" style resource-allocation problems |
| **9** | Surds, exponential growth (loans/inflation — directly relevant to a founder) | Quadratics, simultaneous equations | Trigonometry, circle theorems | Correlation vs. causation; basic statistical inference | Business-maths capstone unit: unit economics, break-even, simple interest vs. compound |
| **10–11** (Cambridge-IGCSE-rigor territory) | Complex/rational functions as needed for chosen track | Functions, calculus intro | Vectors, 3D geometry | Regression, expected value, decision trees under uncertainty | Full open-ended modelling capstone (a real local problem: e.g. optimise a small business's pricing/logistics), presented and defended — TWM Conjecturing/Convincing/Critiquing all exercised at once |

This is a skeleton, not a finished syllabus — the actual `Topic`/`Subtopic` rows should be authored to it incrementally, reusing the existing `order` field for sequencing.

---

## 5. Kyrgyz linguistics: what actually helps or hurts mathematical thinking

This is where language-specific decisions have measurable effect, and where most regional textbooks (often literal translations from Russian) quietly sabotage understanding.

### 5.1 The numeral system is an asset — use it explicitly

**Correction to the earlier draft of this section:** the claim needs to be narrower than "Kyrgyz numerals are transparent like Vietnamese/Chinese." That's only true for the teens. "Он бир" = ten-one = 11, "он эки" = ten-two = 12 ... "он тогуз" = 19 — this part *is* cleanly compositional, exactly like Vietnamese "mười một." But the decade words themselves — жыйырма (20), отуз (30), кырк (40), элүү (50), алтымыш (60), жетимиш (70), сексен (80), токсон (90) — are **not** synchronically parseable by a child as "digit × ten" the way Vietnamese "hai mươi" (two-ten) or Mandarin 二十 (two-ten) are at *every* level. They're closer to Turkish's yirmi/otuz/kırk: distinct lexical items a learner must memorise, historically related to number roots but not transparently so today. So Kyrgyz gets the teens-transparency advantage cleanly, but not the full decades-transparency that Vietnamese/Mandarin get — the earlier framing overstated the parallel.

This structural property (teens only) is the same one that Miura/Fuson-style research credits — with real but *limited*, not magical, effect sizes; the Vietnamese/French study found the advantage is real but modest and fades if instruction doesn't deliberately exploit it — for giving some East and Southeast Asian children an early edge in place-value understanding, versus English's fully opaque "eleven/twelve" or French's "quatre-vingt-dix" (four-twenty-ten = 90). No study of Kyrgyz specifically was found in this research pass — this is an inference from the general mechanism, not a Kyrgyz-specific finding, and should be treated (and tested) as a hypothesis rather than cited as established.

**Actionable rule for MathKG:** don't just rely on the numeral system doing the work passively — *teach place value by making the numeral's own morphology visible*. E.g. when introducing tens/ones with base-10 blocks, explicitly say the number's parts out loud in the order they're built ("он" + "бир" → 1 ten block + 1 ones block) rather than just naming the whole numeral. This is a near-zero-cost win that many literal-translation textbooks throw away by treating number names as opaque vocabulary to memorise rather than as a place-value diagram already built into the language.

### 5.2 Agglutination + case marking: an asset for relational/algebraic language, a risk for translated word problems

Kyrgyz is agglutinative with an explicit case system (nominative, genitive, dative -га/-ге, accusative -ны/-ни, locative -да/-де, ablative -дан/-ден, etc.) and SOV (subject–object–verb) word order, unlike Russian/English SVO.

- **Asset (framed as a pedagogical analogy, not a proven mechanism):** case suffixes make part-whole and directional relationships grammatically explicit in a way English prepositions don't always. "Асандан 3 алма арт" (roughly "from Asan, take away 3 apples") marks the *source* of a decrease directly with the ablative case, which is *worth trying* as a scaffold toward signed numbers and part-whole bar models. Calling the case suffix "a mini bar-model" is a teaching metaphor, not an established cognitive-linguistic finding — pilot it and check whether it actually helps before treating it as a settled design principle. Overclaiming a language-thinking link here (soft linguistic determinism) is an easy way to lose credibility with a reviewer who knows the literature.
- **Risk:** because Kyrgyz is verb-final, a word problem translated word-for-word from a Russian or English original often buries the operation (the verb) at the very end of a long sentence, after all the numeric information — this is harder to parse for a child than the source language, where verbs often appear earlier. **Actionable rule: author word problems natively in Kyrgyz idiom, not as translations.** Put the question and the operative relationship early or repeat it, and keep clause structure short; don't just calque an English/Russian problem sentence-by-sentence.
- Comparative structures ("көбүрөөк" / more, "азыраак" / less, "X, Y-ден N чоң" / X is N more than Y) should be taught as a small, fixed set of sentence *frames*, drilled explicitly before they're needed in fluency work — comparison-language confusion (not knowing whether "more than" means add or which quantity is bigger) is one of the most common word-problem failure modes cross-linguistically, and it's a translation/register issue, not a maths issue.

### 5.3 Academic register consistency (BICS vs. CALP)

Kyrgyz math vocabulary is a mix of native Kyrgyz coinages, Russian loanwords/calques (e.g. many geometry/algebra terms historically came through Russian-medium instruction), and some Arabic-origin roots. Cummins' distinction between everyday conversational language (BICS) and formal academic language (CALP) matters a lot here: a child can be fluent in spoken Kyrgyz and still lack the *academic register* needed to read a formally worded maths problem, if the curriculum doesn't teach that register deliberately and consistently.

**Actionable rules:**
- Maintain **one canonical glossary** of Kyrgyz math terms per concept (this repo should have a single source-of-truth term list, versioned like code) so a child who learns "бүтүн сан" for integer in grade 4 never meets a different word for the same concept in grade 7 because a different author wrote that unit.
- Where a Russian-loan term is already the de facto standard in Kyrgyz schools, don't fight it by inventing a purist neologism nobody uses outside this platform — consistency with what a child's teacher/textbook already uses beats etymological purity.
- No grammatical gender in Kyrgyz removes one class of translation bugs common in Russian-authored materials — but plural/case agreement on generated numbers-in-context (the worksheet generators in `apps/resources/data/`) still needs to be handled correctly by whatever templating produces problem text, not just interpolated blindly (e.g. numeral + counted noun agreement rules).

### 5.4 Net effect

None of this requires reinventing Kyrgyz-language pedagogy from scratch — it requires (a) exploiting the numeral system's transparency on purpose instead of by accident, (b) authoring word problems natively instead of translating, and (c) treating the academic-register glossary as a maintained artifact, not an afterthought.

---

## 6. Known limitations and open questions (five-lens review)

This framework was reviewed against five perspectives — learning science, Kyrgyz classroom implementation, applied linguistics, equity/access, and assessment/policy alignment — before further work proceeds. What follows are the gaps that review surfaced, ranked by how much they should block next steps.

1. **Blocking: the Kyrgyz Republic's own state standard has not been checked.** This document compares seven *other* countries' curricula but never checked Kyrgyzstan's own Мамлекеттик билим берүү стандарты or the exams students actually sit. That should have been research step zero. Without it, there's no way to know which parts of §4's scope-and-sequence reinforce what's graded versus compete with it for classroom time — and competing with the graded curriculum is how a well-designed supplementary resource gets deprioritised by teachers and parents regardless of its quality. **Recommended immediate next step, before authoring more content:** obtain and map the current state standard (by grade/strand) against §4, and mark each cell as *aligned*, *extends beyond*, or *diverges from* the official standard, with a reason for any divergence.
2. **Equity risk: open-ended "rich tasks" can widen gaps if unscaffolded.** §4's upper-secondary capstone ("open-ended modelling problem, presented and defended") and much of the Think & Reason section follow a minimally-guided, discovery-style model. That style is well documented to advantage students who already have more prior knowledge or home academic support unless it's heavily scaffolded — the opposite of Estonia's equity result, which this document holds up as the benchmark to beat. No scaffolding plan is proposed yet; one is needed before these activity types are built out at scale.
3. **Access assumption: computational/tool-based modelling assumes device and connectivity access this document didn't verify.** The Estonia-inspired computational-thinking strand (§3.4) and the "spreadsheet/tool check" step (§4, grades 7–9) were borrowed without their infrastructure precondition. Needs an explicit low-connectivity/no-device fallback path, not just an unplugged *option* at primary level.
4. **Capacity gap: teacher facilitation skill, not resource count, is the likely bottleneck.** A Curiosity-Question slide deck or a Think & Reason activity card does not by itself produce inquiry-based teaching; the UK and Shanghai-exchange experience with mastery-style teaching required sustained paid CPD to move practice, with contested effect sizes even then. This document has no teacher-training or facilitator-guide component yet, and the volume implied by multiplying §4's scope-and-sequence against the existing ~12-section template is a real production-capacity risk that hasn't been sized.
5. **No falsifiable checkpoint.** There is currently no proposed way to know, a year or two in, whether any of this actually changed student reasoning versus just existing as tags in the database. A small measurable pilot (one grade band, one strand, a pre/post task on e.g. specialise-and-generalise reasoning) should precede a full rollout.
6. **Framing risk: "unicorn founder" as the headline goal.** Useful as a north star for prioritising founder-relevant strands (§2), but risks reading as narrow or imported Silicon Valley language to Kyrgyz teachers and parents, and risks optimising the system for a tail outcome at the expense of the median student's broad numeracy. Recommend keeping the founder-skills framing internal (as a design lens for content authors) rather than as the platform's public-facing pitch to families.

None of this invalidates the direction in §1–§5 — the comparative research and the gap analysis against the existing data model hold up. It means: check the state standard before writing more scope-and-sequence, build a scaffolding plan alongside any open-ended task, and pilot small with a measurable checkpoint before scaling the production effort.

---

## 7. Summary checklist for content authors

- [ ] Every new unit opens with a real Story/Curiosity/Real-life hook before naming the topic (Finland).
- [ ] Every new concept gets a Concrete → Pictorial → Abstract triplet before symbols appear (Singapore).
- [ ] Every fluency worksheet is a **variation sequence** (one thing changes per item), not i.i.d. random items (China / UK mastery).
- [ ] Every topic has at least one task tagged for each TWM pair by the end of the unit: Specialise/Generalise, Conjecture/Convince, Characterise/Classify, Critique/Improve (Cambridge) — add the two missing `LEARNING_GOALS` (`variation`, `specialise_generalise`) to close the gap described in §3.
- [ ] From grade 3 up, every topic produces at least one artifact in each of: estimate/model, structure-spot-across-problems, data/critique-a-claim (USA 8 Practices as a checklist).
- [ ] From primary onward, an algorithmic-thinking thread runs in parallel (Estonia) — unplugged at first, tool-based later.
- [ ] Word problems are authored natively in Kyrgyz, using a single maintained glossary, and deliberately use the numeral system's own base-10 transparency and case-marking as teaching aids rather than incidental facts.

---

### Sources consulted
- [Thinking and Working Mathematically: definitions & examples — Cambridge](https://www.cambridge.org/education/blog/2021/01/26/thinking-and-working-mathematically-part-1-definitions-and-examples/)
- [Developing learners' Thinking and Working Mathematically skills — Cambridge](https://www.cambridge.org/gb/education/blog/2022/04/07/developing-learners-thinking-and-working-mathematically-skills/)
- [Cambridge Primary Mathematics Curriculum Framework (0096)](https://static1.squarespace.com/static/59edc421bff200ece07aaea0/t/60dad862f37caa053cab5d23/1624954979966/Cambridge+Primary+Mathematics+Curriculum+Framework+0096_tcm142-592530.pdf)
- ['Bianshi' and the Variation Theory of Learning — Springer](https://link.springer.com/chapter/10.1007/978-94-6300-782-5_3)
- [Teaching with variation: an effective way of mathematics teaching in China — ResearchGate](https://www.researchgate.net/publication/291569306_Teaching_with_variation_An_effective_way_of_mathematics_teaching_in_China)
- [PISA 2022 Results — Estonia country note (OECD)](https://www.oecd.org/en/publications/pisa-2022-results-volume-i-and-ii-country-notes_ed6fbcc5-en/estonia_dafed886-en.html)
- [What makes Estonia's education system successful? — VisitEDUestonia](https://visiteduestonia.com/what-makes-estonias-education-system-successful/)
- [How has digital learning improved Estonia's PISA results? — VisitEDUestonia](https://visiteduestonia.com/how-has-digital-learning-improved-estonias-pisa-results/)
- [Transparent number-naming system gives only limited advantage for preschoolers' numerical development (Vietnamese vs. French) — PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0243472)
- [Ethnolinguistic and Cognitive Aspects of Sacred Numbers in the Turkic Worldview (Kazakh, Kyrgyz, Uzbek)](https://www.ijscl.com/article_735124.html)
