# Reading of the stage-3 report (BHM-149): HD-X-2, the composition of Theorem HD-X, [another line of this project] (c-i), the screen

*The session-R lead's reading, 2026-10-26, for the bh-modes lead (RULES.md E). It is a reading, not a re-run.
It was drafted with a subagent's help. Before delivery the lead checked findings 2a, 4c, 3a, 4a and 5a against the cited lines
(the gate list `code/hdx/critical.py:87-88` against the controls of PREREG :126-141 and `STAGE_REPORT.md:109`; DET at
`[a record of another line of this project]:23` against its control table).*
- *bh-modes was read at `013c174`, which contains `b056f61`. `results/stage3/STAGE_REPORT.md` is `1307b1f2…` with 195
  lines, as required. All 1854 `SEALED.sha256` entries verify (`sha256sum -c`), the 262 under `results/hdx/critical/`
  and `results/stage3/` included.*
- *Paths are relative to `[repository]`. **[V]** marks what I verified, by reading or by my own short derivation.
  **[S]** marks what I report as stated without checking it. Everything not checked is listed at the end.*
- *Nothing of the project was run. I used `sha256sum`, read-only `git log` and `grep`, and a JSON reader to print fields
  of HD-X-2's records (`python3 -I -c 'json.load…'` on host-0; read-only, no project code imported). `RULES.md` B3 asks
  agents not to run Python on host-0, so that use is disclosed here. All arithmetic below is by hand.*

## Summary

Theorem HD-X's certified content stands, as far as a reading can check it. No finding is ERROR or GAP-MAJOR.
1. **Q1, HD-X-2's divisions and cover: sound, no finding.**
   - Each new divisor is ≥ 0 on its closed box: μ on O and O′, and the extra σ on C.
   - A divisor vanishes only at points that map to μ = 0. The claim excludes μ = 0, since q = 1 is Z's.
   - Everywhere else the divisor is > 0, so a positive quotient gives NL > 0 at every (z, μ) ∈ (0, 1) × (0, MU1].
   - The cover is complete. I checked it by derivation and in the code.
2. **Q2, the controls.**
   - No control is weaker than registered, and none passes vacuously. VOID handling hides nothing.
   - But six gates (PARAM, H, S, R, L, XN) have no control or tamper, against the project's own commitment of 10-23
     (gap-minor).
   - Two wording items: d0-corner's stated reason does not describe its record, and "two changes" conflicts with the
     PREREG's "one change".
3. **Q3, the composition: complete for every D = 7–11, ℓ ≥ 2 and q ∈ (0, 1].** Two wording items:
   - the report does not name the HD-E E1 sliver (99/100, q(μ_lo)) that HD-X-E's MEET relies on, as A2's addendum did;
   - the headline drops the L² form and the pencil labels that BHM-087 adopted.
4. **[another line of this project] (c-i): the split between certified and pencil is right.**
   - The report uses M₀ for two different matrices in one sentence.
   - Two provisos are missing: the tested cyclic order was found numerically, and Fable's B3 holds under named
     conventions.
   - DET has no control.
5. **The D = 12–20 screen is information only and is used in no theorem.** One scope wording item.

## Q1. HD-X-2's design, its divisions and its cover

**1.1 The four divisions [V].** Sources: `results/hdx/critical/PREREG.md:57-67`; `code/hdx/critical.py:149-165` (the
divisions) and `:471-474` (the boxes).

| Chart and box | Divisor | Sign on the closed box | Zero set | Maps to |
|---|---|---|---|---|
| O, (z, μ) ∈ [1/4, 1] × [0, MU1] | μ | ≥ 0 | μ = 0 | q = 1, outside the claim |
| O′, (z, μ) ∈ [0, 1/4] × [1/32, MU1] | μ | ≥ 1/32 > 0 | none | — |
| T, (ζ, μ) ∈ [0, 8] × [0, 1/32] | μ², as in HD-X-S | ≥ 0 | μ = 0 | (z, μ) = (0, 0) |
| C, (z, σ) ∈ [0, 1/4] × [0, 1/8] | z²σ | ≥ 0 | z = 0 or σ = 0 | μ = zσ = 0 |

- **Where a divisor is 0.** Every such point of a box maps to μ = 0. HD-X-2 claims only μ ∈ (0, MU1], i.e.
  q ∈ [q(MU1), 1), and q = 1 is Z's, so nothing is lost there. On a closed box, positivity at μ = 0 is a limit statement
  (∂_μNL > 0). It is stronger than the claim needs, Bernstein needs it, and it holds.
- **Everywhere else** the divisor is > 0, so quotient > 0 ⇔ NL > 0.
- **The divisions are exact.**
  - DIV-O tests that every monomial of NL has μ-degree ≥ 1 (`:153`).
  - DIV-T tests that every monomial has total degree ≥ 2 (`:160`).
  - DIV-C tests total degree ≥ 2 and μ-degree ≥ 1 (`:161`).
  - The exponent bookkeeping is right: z^iμ^j → ζ^iμ^{i+j} for T, and → z^{i+j}σ^j for C.
  - With M = NL/μ, the divisions need M(0, 0) = 0, which FIRST also checks (`:214-217`).
- **Structure.** T = M(μζ, μ)/μ and K = M(z, zσ)/z. So HD-X-2 is HD-X-S's construction applied to M. M vanishes to
  first order at the corner, where HD-X-S's NL vanished to second order.

**1.2 The cover [V].** Take (z, μ) ∈ (0, 1) × (0, MU1].
- If z ≥ 1/4, the point is in O.
- If z < 1/4 and μ ≥ 1/32, it is in O′.
- If z < 1/4, μ < 1/32 and z ≤ 8μ, it is in T, with ζ = z/μ ∈ (0, 8].
- Otherwise σ = μ/z < 1/8, and it is in C.

This is PREREG :66-67, and Fable's A3 case split (`results/stage3/audits/fable_2026-10-26/AUDIT.md:118-126`) restricted
to μ > 0.
- COVER's code also checks 0 < MUT < MU1 and 0 < Z1 < 1 (`critical.py:428`). Fable found these two range checks missing
  from HD-X-S's COVER (`AUDIT.md:128-130`).
- In all 9 `none` records, the boxes are as registered.

**1.3 The reduction's other inputs [V, except where marked].**
- **S > 0 for μ > 0.** In all 9 `none` records ε_n = c·μ with c > 0. Each ε in PREREG :106-114 is a positive multiple of μ over a
  quadratic in μ with positive coefficients; I read all nine.
- **R ≥ 1 on [0, 1].** R = (1 − (1 − z)^k)/z = Σ_{j<k}(1 − z)^j (derivation).
- **NL = N·S²R²L is an algebraic identity.** I derived it from PREREG :50-55, using P = Π/D, D = S·R·Hn and
  L = Ud·Hd²·fd. The derivation needs Ud, Hd and fd to depend on μ only; that premise is [S].
- **q(MU1)² ≤ (99/100)² in all nine bands.** I checked it by hand from PREREG :106-114; the PARAM gate also checks it in
  each record.
  - D = 7 ℓ = 2: ε and q(MU1)² come from one w = 8μ/(7 + μ²), with q² = 1 − w². This gives 197505/201601 at μ = 1/8.
  - D = 11 ℓ = 3: likewise with w = 7μ/(μ² + 6), which gives 2961/3025.
- **D = 7 ℓ = 2's row is internally consistent** (by hand).
  - Take the constants from `results/hdx/critical/dev/DEV.md:48`: H(2) = 42, L(0) = 49, R(0) = 4, ε_d(0) = 7,
    w′(0) = 8/7.
  - THROAT's formula (PREREG :93) then gives 14869757952ζ + 5310627840, and C₀ = 387072.
  - K(0, 0) = C₀ε_d(0)²R(0)²L(0) = 14869757952 = T₁, as CORNER requires.
- **Proposition 3 applies as written for μ > 0** (`results/p3/METHOD_ADDENDUM_3.md:41`).
  - w increasing gives q decreasing.
  - By the intermediate value theorem, each q ∈ [q(MU1), 1) is q(μ) for some μ ∈ (0, MU1].
- **Every chart is one leaf** (`bernstein_leaves` = 1 for each POS chart in all 9 `none` records), as RESULT :15
  says.

**Findings.**
- **1a (none).** I found no gap in the divisions or the cover.
- **1b (none; information).** `results/hdx/critical/RESULT.md:66-67` calls these "the same steps as HD-X-S's". They are
  not quite: there are the extra divisions, and the claim stops short of μ = 0. The report's status row
  (`STAGE_REPORT.md:130`) says it correctly.
- **1c (none; process note).** The label "HD-X-2's own form not audited" (`:130`) may outlive Kimi's audit.
  - Kimi's brief lets Kimi use its own cover (`results/stage3/briefs/BRIEF_kimi_2026-10-26.md:134-135`).
  - Its pencil task asks about the reduction (`:146-148`), not about PREREG §2's charts as written.
  - My 1.1–1.2 is a check by reading, not an audit. The bh-modes lead could ask Kimi for a verdict on the charts as
    written, or cite this reading.

## Q2. Is any HD-X-2 control weaker than registered?

**2.1 What I verified [V].**
- **The forms are the registered ones.**
  - The kit's table (`kit/hdx/run_critical.sh:18-33`) equals PREREG §4's (`:128-141`) character for character, up to
    Markdown's `\|`.
  - `code/hdx/kitcheck.py:16-39` implements PREREG :121's `+A,B|C`. The verdict must be a REJECT that is not an
    exception or an unwritten record, with required ⊆ failed ⊆ required ∪ allowed.
- **There are ten `+` forms, not nine.** They are nc-ehat-low, d0-corner, nc-ehat-high, d0-throat, nc-Q0, nc-Qneg,
  td-nu, d6, td-coeff and td-div. The four `=` forms are none, nc-bound, td-verifier and td-cover.
- **Every "may also fail" set holds only POS charts,** so every non-POS failure is predicted exactly, as PREREG :122-123
  says.
- **35 of 35** `kitcheck.txt` files in `runs/record/` read "match", and RESULT :35-47 equals the records.
- **No required failure can be met vacuously.** Each is absent from the `none` job, which is VERIFIED, and each is forced
  by an exact property of the change:
  - K(0, 0) < 0 for nc-ehat-low, and K(0, 0) = 0 for d0-corner;
  - T(0, 0) < 0 for nc-ehat-high, and T(0, 0) = 0 for d0-throat;
  - M(1, μ) ≡ 0 for nc-Q0 and < 0 for nc-Qneg, on O's edge z = 1. There INF fails by its clause "c > 0"
    (`critical.py:229`);
  - NL(z, 0) ≠ 0 for td-nu and td-coeff;
  - T(2, MU_C) < 0, by construction, for d6;
  - the divisions themselves, for td-div;
  - for nc-bound, the refusal on the support that a certified Q[b] < 0 forces.
- **The POS failures are exact counterexamples.** Every required POS failure in the records is an exact value ≤ 0 at an
  exact point, never "undecided at depth" (`code/onset/bernstein.py:84-89`). A chart that was "not run" meets a required
  failure only where its DIV failure is also in the form, i.e. for td-nu, td-coeff and td-div (e.g. td-coeff: POS-O,
  POS-O′ and POS-C read "not run: the chart's division failed").
- **nc-bound is not vacuous.**
  - Its `=` form needs part (a) certified. An uncertified (a), or an exception, adds "nc-bound (a)" to the verdict and
    breaks the form (`critical.py:485-495`).
  - The planted NL is NL − 64Hn²Ud·fd·K·b·S²R² (`:349-351`). I re-derived it from U − 64H²Kb.
  - The supports and K in the records equal PREREG :152-153's.
- **VOID handling hides nothing.**
  - The VOID rule is not in the kit. `run_critical.sh:46-60` prints KIT FAIL on any mismatch, a band's `none` job
    included. So a VOID kit band is always an uncertified band and a failed kit.
  - Both kit bands were VERIFIED, so no VOID arose.
  - The rule was sealed in `6cedd44` (21:51:29 EDT), before the record ran (21:52:14 EDT, RESULT :7-8).
  - It is HD-X-S's rule (`results/hdx/s/PREREG.md:89-90`).

**Findings.**
- **2a (gap-minor, process).** Six gates have no planted control or tamper: PARAM, H, S, R, L and XN. No control in
  PREREG :126-141 targets them, and none of them fails in any record.
  - This is against `RULES.md:170` and against the commitment the project made after our reading of 10-23
    (`results/hd/STAGE_REPORT_ADDENDUM_1.md:33-35`): "From A2 on, each gate's registration carries a control."
  - HD-X-S's td-H, td-param, td-L and td-S (`results/hdx/s/PREREG.md:69-74`) tamper HD-X-S's own gate code
    (`code/hdx/scert.py:207, :215, :246, :260`). HD-X-2's gates are new code (`critical.py:382-420`), and no control
    reaches them.
  - `STAGE_REPORT.md:109` does not say so.
  - S matters for the reduction: it keeps the pole off [0, 1] and makes S² > 0 in the step from NL to N.
  - What stands in: 1.3's readings of S and R, of PARAM's q(MU1) bound, and of XN's identity. I did not check H or L.
  - Fix: a dated addendum adding td-param, td-H, td-S (ε_n → −ε_n, as in HD-X-S), td-R, td-L and a td-XN (one term of
    NL's assembly perturbed), run on the two kit bands. At the least, name these gates in E.4 together with what stands
    in, as BHM-087 item 5 did for HD-S.
- **2b (wording).** d0-corner's registered reason, "K(0, 0) = 0 exactly: only strictness refuses it" (PREREG :130),
  does not describe its record.
  - At ε̂ = 1/k, POS-O, POS-O′ and POS-T also fail, with negative values, at both bands (RESULT :36). For example, in
    `runs/record/D7l2/d0-corner/result.json` POS-O is < 0 at (1/4, 0), POS-O′ at (1/4, 1/32) and POS-T at (8, 1/32).
    So that job would be refused even without strictness.
  - POS-C's own refusal is at (0, 0) with value exactly 0. That is the first corner `prove_sign` tests
    (`bernstein.py:84-87`), so the strict test did fire at the registered point.
  - d0-throat is clean: POS-T alone, at (0, 0), value 0, at both bands. nc-Q0's POS-O is refused at (1, 0) with value 0.
  - Strictness is also tested in every job by KAT3, "t(1-t)+mu (zero at a corner) rejected" (`code/a1/p1.py:88`).
  - The forms record no point or value. HD-X-S's d0 and d6 rules did (`results/hdx/s/PREREG.md:63-64`), and HD-X-2's
    records meet those stronger rules.
  - Fix: one sentence in the report giving each zero-margin control's refusal point and value. For later
    registrations, add a detail field to the form; Kimi's brief already asks Kimi for this
    (`BRIEF_kimi_2026-10-26.md:153-154`).
- **2c (wording).** The report and the PREREG disagree on the number of changes.
  - `STAGE_REPORT.md:167-169` says the registration took "the fork's code with two changes by the lead".
  - PREREG :18 says "The lead's one change before registration: `nice -n 19`".
  - The VOID rule is registration text (PREREG :143-146, :212-217), not code.
  - Fix: "one code change (`nice`) and one registration rule (VOID)".

## Q3. The composition of Theorem HD-X

**3.1 The cover [V, from the cited records' statements].** D = 7–11 means n = 5…9, with ℓ₀ = 10, 10, 11, 13, 14.

| ℓ | q ∈ (0, 99/100] | q ∈ (99/100, 1) | q = 1 |
|---|---|---|---|
| ℓ > ℓ₀ | Lemma U(n), for every q ≤ 1 (`results/hd/STAGE_REPORT.md:31`) | the same | the same, and Z |
| n − 1 ≤ ℓ ≤ ℓ₀ (33) | HD-E's E1 on [0, q(μ_lo)], with q(μ_lo) ≥ 99/100 (`results/hdx/elementary/PREREG.md:21-22`) | E1 up to q(μ_lo), then HD-X-E on [q(μ_lo), 1] (MEET, `:39-41`) | HD-X-E and Z |
| 2ℓ > n − 1 and ℓ ≤ n − 2 (11) | Theorem HD | HD-X-S on [q(1/8), 1], with q(1/8) ≤ 99/100 | HD-X-S and Z |
| 2ℓ ≤ n − 1, i.e. 𝒦 (9) | Theorem HD | HD-X-2 on [q(MU1), 1), with q(MU1) ≤ 99/100 | Z only |

- **The ℓ ranges.**
  - The three ranges partition ℓ ≥ 2, since n − 2 < n − 1 ≤ ℓ₀.
  - The counts check: 33 = 7+6+6+7+7, 20 = 2+3+4+5+6 and 9 = 1+1+2+2+3.
  - 𝒦 lies inside the bands, because (n − 1)/2 ≤ n − 2 for n ≥ 3.
  - The code's MU1 table and the kit's band list are exactly 𝒦 (`critical.py:80-81`, `run_critical.sh:34`).
  - 𝒦 is where u₀ is throat-principal (`results/extremal/RESULT.md:62-64`).
- **Endpoints.** Every junction is closed on at least one side.
  - q(MU1) and q(1/8) lie at or below 99/100.
  - q(μ_lo) is closed on both sides.
  - q = 1 is Z's, and also HD-X-S's, HD-X-E's and Lemma U's.
- **Overlaps.** None matters, since each part proves A ≥ 0 on its own.
- **Each part's hypotheses are met where it is used.**
  - HD-X-E: V ≥ 0 suffices, since V_S− = fU₋/(64r²H₋²) (`results/screen12/PREREG.md:19`).
  - HD-X-S at μ = 0 needs Proposition 3's (0, 1) form, which `results/p3/METHOD_ADDENDUM_3.md:18-22` states. HD-X-2
    needs it only at μ > 0 (`:41`).
  - Z rests on Lemma 1 and `tortoise_q1`, both machine-checked [S].
  - Z's "every D ≥ 4" was registered through the symbolic-n job (`results/extremal/PREREG.md:55, :138`).

**Findings.**
- **3a (wording).** The report does not name the E1 sliver that HD-X-E's range relies on.
  - The composition reads as "Theorem HD for q ≤ 99/100, then HD-X-E on (99/100, 1)" (`STAGE_REPORT.md:55, :57-59`).
    Line `:62` says "Each range meets Theorem HD's".
  - But HD-X-E starts at q(μ_lo) ≥ 99/100. So for the 33 (D, ℓ), the sliver (99/100, q(μ_lo)) rests on HD-E's E1 box,
    which lies above Theorem HD's stated range (q ≤ 99/100, `results/hd/STAGE_REPORT.md:9`).
  - The cover is still complete. MEET checks the meeting exactly (`:63`), and HD-X-E's own RESULT says it right
    (`results/hdx/elementary/RESULT.md:33`).
  - A2 named its analogue: "A1's P1 Part I on [99/100, q(μ_lo(ℓ))]" (`results/a2/STAGE_REPORT_ADDENDUM_1.md:19-20`,
    BHM-106).
  - Kimi's brief has the same compressed form (`BRIEF_kimi_2026-10-26.md:70-78`), but its task 4 checks the meeting
    (`:144`).
  - Fix at `:59`: "HD-X-E on [q(μ_lo), 1], and HD-E's E1 on [99/100, q(μ_lo)] (q(μ_lo) ≥ 99/100; gate MEET)". At `:62`:
    "meets Theorem HD's (for HD-X-E, HD-E's E1 box)".
- **3b (wording; label).** The headline (`STAGE_REPORT.md:12-14`, also `results/hdx/critical/RESULT.md:74-76`) drops two
  corrections that bh-modes adopted after our reading of 10-23 (REGISTRY BHM-087;
  `results/hd/STAGE_REPORT_ADDENDUM_1.md:8-12`).
  - **The L² statement.** It was "no κ > 0 and no 0 ≠ φ ∈ L²(ℝ) with A_{ℓ,q}φ = −κ²φ". The headline now says "no
    exponentially growing mode, up to and including extremality". At q = 1 the L² form matters most: the theorem is
    spectral and says nothing about non-modal behaviour at the degenerate horizon. Aretakis-type horizon instabilities
    are an example; that is my remark, not from a fetched source.
  - **The pencil steps beside "(certified)"** (`RULES.md:31-33`). The status table has them row by row (`:121-136`),
    and `:133` says "resting on the rows above", but the headline carries only the one label.
  - Fix: BHM-087's wording, plus "Rests on, beyond exact computation:
    - HD-X-2's reduction and cover (pencil; its own form audited 0×);
    - HD-X-S's (audited 1×);
    - the tortoise map for 0 < q < 1 (audited 1×);
    - Lemma U(n), steps (a)–(d) (audited 2×);
    - Proposition 3 (Lean, with the tortoise map as a hypothesis)."

## 4. [another line of this project] (c-i)

**4.1 The split [V].**
- **Certified, at 36 cases** (18 (D, ℓ) pairs × 2 ω). Arb enclosures of M0, ROT, DET, CYCLIC and TRINV each contain 0
  with relative radius ≤ 10⁻³⁰, and FROB is exact. That is a certified test, not a proof
  (`[a record of another line of this project]` §4; `RESULT_ADDENDUM_1.md:23-34`).
- **Pencil:** the relations, the TQ system and the quantum Wronskian. Fable's B3 found them "SOUND as pencil statements"
  (`results/stage3/audits/fable_2026-10-26/AUDIT.md:20`).
- **The report matches this split** (`STAGE_REPORT.md:30-36, :52, :134`). It says "The tests are not a proof", and that
  a second party for the tests is pending.
- **One harmless understatement.** Because FROB is exact, M₀ = (−1)ⁿI holds exactly at those cases for every ω. That is
  a little more than "tested".

**Findings.**
- **4a (wording).** M₀ names two different matrices in one sentence (`STAGE_REPORT.md:31-32`).
  - In "M₀ = (−1)ⁿI" it is the monodromy around r = 0.
  - In "(−1)ⁿM₀M₁···M_{k−1} = M_∞" it is the monodromy around horizon h₀. The code's product runs over the horizon
    matrices `Mc[j]` (`[code of another line of this project]:30, :33, :774-780`).
  - Read literally, the two statements give M₁···M_{k−1} = M_∞, which is a different relation.
  - The sealed PREREG has the same collision (`[a record of another line of this project]:20, :24`).
  - Fix: write the product as the note does, M_∞ = (−1)ⁿM(ω)M(ζ^{−1}ω)···M(ζ^{−(k−1)}ω)
    (`[a note of another line of this project]:30-31`), or rename the r = 0 matrix.
- **4b (wording).** The report says "The relations themselves … are proved (pencil; audited 1×: Fable's B3, SOUND)"
  (`:33-34`). It leaves out two provisos on what the tests test.
  - B3 holds under named conventions. The product order is "a convention" (`AUDIT.md:217-218, :239`), and one
    subsidiary sentence was not checked (`:236`).
  - The tested CYCLIC order "is the one the planning found numerically … its derivation from the fundamental-group
    relation is pencil, not done" (`[a record of another line of this project]:24-26`).
  - The loops' homotopy classes rest on a pencil distance argument (`:33-34`).
  - So nobody has written down that the code's order is the traversal order of the code's loops. The wrong-order
    control shows only that the order matters.
  - Fix: add both provisos at `:31-34` or in the status row `:134`.
- **4c (gap-minor, process; no theorem rests on it).** DET has no control.
  - The "tamper" control expects DET to pass (`[a record of another line of this project]:47`), and no other control targets
    it.
  - `STAGE_REPORT.md:110` does not say so.
  - Fix: in the next addendum, a tamper that must fail DET, e.g. one horizon matrix scaled by 1 + 10⁻²⁰ before the
    judge. Otherwise, name the gap in E.4.

## 5. The D = 12–20 screen

- **[V] It is labelled information wherever it appears:** `STAGE_REPORT.md:37-38, :79, :96, :111, :117-118, :136,
  :172-173, :195`; `results/screen12/PREREG.md:8-9`; `results/screen12/RESULT.md:4-5`.
  - It is absent from "How the parts compose" (`:54-67`) and from Theorem HD-X.
  - Z's claim for D ≥ 4 rests on Z's own symbolic-n job, not on the screen.
  - At `:117-118`, Z checks the screen, not the reverse.
- **5a (wording).** `:37-38` says "The bands of V_S− are exactly ℓ = 2, …, n − 2 at every D". That drops the screen's
  own scope (`results/screen12/RESULT.md:177-180`): ℓ ≤ 6n, and q no closer to 1 than 1 − 10⁻¹⁰, beyond the exact q = 1
  data.
  - That every ℓ ≤ n − 2 has a band is exact, since U₋(x_H) < 0 at q = 1.
  - That no ℓ above n − 2 has one is numerical, and only for ℓ ≤ 6n.
  - Fix: "(numerical, ℓ ≤ 6n)".

## What I read

- **The report:** `results/stage3/STAGE_REPORT.md`, in full.
- **HD-X-2:**
  - `results/hdx/critical/PREREG.md` (`7d96a6c7…`) and `RESULT.md` (`f178311e…`), in full; `dev/DEV.md`.
  - From `runs/record/`: the verdict, checks and details of all 35 jobs, and every `kitcheck.txt`.
  - `code/hdx/critical.py` (`8a7b041e19c906fd`, equal to `6cedd44`'s), in full.
  - `code/hdx/kitcheck.py` and `kit/hdx/run_critical.sh`, in full.
  - `code/onset/bernstein.py:69-100` (`prove_sign`); `code/a1/p1.py:51-88` (the tamper and the KATs, by their labels).
  - `code/hdx/scert.py`, by grep only.
- **HD-X-S and HD-X-E:** `results/hdx/s/PREREG.md` and `RESULT.md`; `results/hdx/elementary/PREREG.md`, `RESULT.md` and
  `inward_2026-10-26/inward_hdxe.host-1.log`.
- **The frame:** `TARGET_HD_ADDENDUM_2.md`, `TARGET_HD_ADDENDUM_3.md` and `results/p3/METHOD_ADDENDUM_3.md`.
- **Earlier stages:**
  - `results/hd/STAGE_REPORT.md:1-40` and `STAGE_REPORT_ADDENDUM_1.md:1-40`;
  - `results/a2/STAGE_REPORT.md` (its statements) and `STAGE_REPORT_ADDENDUM_1.md:15-26`;
  - `results/extremal/RESULT.md`, and `results/extremal/PREREG.md` by grep.
- **[another line of this project]:** `[a record of another line of this project]`, `RESULT.md` and `RESULT_ADDENDUM_1.md`;
  `[a note of another line of this project]:10-35`; `[code of another line of this project]` (its docstring and `:766-781`).
- **Audits and briefs:** `results/stage3/audits/fable_2026-10-26/AUDIT.md:1-32, :91-141, :186-240`;
  `results/stage3/briefs/BRIEF_kimi_2026-10-26.md:55-90, :126-160`.
- **The screen:** `results/screen12/PREREG.md:1-30`; `results/screen12/RESULT.md:1-12, :33-45, :160-206`.
- **Rules and registry:** `RULES.md`; `CHARTER.md` §5; the `REGISTRY.md` rows for BHM-087, BHM-103 to 106 and BHM-133
  to 150.
- **For format:** our `[deliveries]/ib-lead_hd_reading_2026-10-23/READING.md`.

## What I did not check

- I ran no certificate, kit or Bernstein proof, and re-derived no chart polynomial.
- `hd.scert.exact_parts`, i.e. how Un, Ud, Hn, Hd, fn, fzn and fd are formed. In particular, I did not check that Ud, Hd
  and fd depend on μ only, which NL = N·S²R²L needs.
- `param_n` and the PARAM identities, beyond q(MU1)². The content of gates H and L.
- `Poly2.bernstein` (the box substitution), and the KATs beyond their labels.
- S5's transcription (E0n) and Kimi's.
- The Lean statements `prop3_Dn`, `tortoise_q1` and Lemma 1.
- Theorem HD's parts, Lemma U(n), and HD-E's E1 boxes and μ_lo values, which I took from stage 2 and our earlier
  reading. I also did not compute the size of the (99/100, q(μ_lo)) slivers.
- HD-X-E, HD-X-S and HD-X-PILOT beyond their claims and controls.
- (c-i)'s rigorous step and Gronwall bound, its records' radii, and `DEV.md` and `DEV_ADDENDUM_1.md`.
- The screen's numbers.
- Z's partner, B1, Lemma R, and A1 and A2 beyond their statements. That includes the headline's D = 6–11 sentence
  (`:23`), which I read against `results/a2/STAGE_REPORT.md:10, :14` only.
- The process slips (`STAGE_REPORT.md:174-182`).
