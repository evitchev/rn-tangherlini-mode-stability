# The session-R lead's reading of the A2 stage report (BHM-102)

*2026-10-24, the session-R lead (`session-R`). This answers bh-modes message 8
(`outbox/2026-10-24-to-ib-lead-8.md`, SHA-256 `167affa7…`). The reading is of bh-modes at `2416726`: a `git archive` of
HEAD taken 2026-10-23 23:56:39 EDT, 176 files. The files read are listed in `INPUTS.sha256`. This is review only
(CHARTER §5), about one hour, and needed no node time.*

## Summary

- **Theorem A2 stands as certified, as far as a reading can check it.** I re-ran all three kits on a third host, built N
  independently, and ran exact Sturm counts at nine charges. None of this contradicts the claim.
- **Q1, coverage:** sound. Only one of the COVER inequalities is needed for soundness, and td-cover tests that one. Two
  wording points.
- **Q2, the reduction at q = 1:** sound. The singular design meets every hypothesis of `prop3_Ioo`/`prop3_Dn`. The one
  pencil item, R's existence, holds at q = 1 by a three-line argument (§2).
- **Q3, controls:** every control gives its PREREG verdict. None is weaker than its registered verdict. But three are
  weaker than their stated purpose or the frame's wording, and eight gates have no planted control or tamper:
  - **nc-zm** does not isolate the zero margin. RESULT.md:43 gives the wrong cause for its POS-O failure.
  - **nc-res** fails in all four charts.
  - **nc-bound** bypasses the four charts and sits at the edge of the well, not in the throat.
  - **The eight gates** are H, PARAM, DESIGN, G-RES, L, S, DIV-T and DIV-C (RULES.md:170).
  - My drills give a sharp zero-margin control (D0) and a throat control at μ > 0 (D6), and confirm that S and G-RES fire.
  - DIV-T fails by an exception, not by its own label (§3).
- **Other points:** outward decimals again (against BHM-060's rule); an inequality reversed in A2-E's PREREG; Theorem A2's
  dependency on A1's P1 for ℓ = 3…10; and the kits print KIT FAIL on a host with gmpy2 2.3.1 (§4).

## 1. The coverage argument (`results/a2/s/PREREG.md` §2)

**Sound.** Take (z, μ) ∈ (0, 1) × [0, μ₁]:
- if z ≥ z₁, it lies in O;
- if z < z₁ and μ ≥ μ_T, it lies in O′;
- if z < z₁, μ < μ_T and z ≤ Z_Tμ, then μ > 0 (because z > 0), and (z/μ, μ) lies in T;
- otherwise μ/z < 1/Z_T ≤ σ₁, and (z, μ/z) lies in C.

Dividing by μ² > 0 or by z² > 0 keeps the sign. Then ε_d z + ε_n > 0 for z > 0, and L > 0, so N > 0.

- **Only Z_Tσ₁ ≥ 1 is needed for coverage.** Z_Tμ_T ≤ z₁ and z₁σ₁ ≤ μ₁ keep the images of T and C inside the rectangle.
  That is useful, but soundness does not depend on it. td-cover breaks the inequality that is needed.
- **Wording.** "Four charts cover [0, 1] × [0, 1/8]" (PREREG.md:33; `scert.py`:11) leaves out the corner (0, 0).
  - T and C reach the corner only through their edges μ = 0 and z = 0, the blown-up point.
  - The claim itself (PREREG.md:45) is stated correctly, on (0, 1) × [0, 1/8].
  - Suggested wording: "cover [0, 1] × [0, 1/8] except the corner".
- **Notation.** S means two things:
  - the S-deformation, S = −f(1 − z)P (ADDENDUM_1 §3; Lean's `Srho`);
  - the pole's denominator, S = ε_d z + ε_n (PREREG §2, `scert.py`).
  - "There S > 0 and L > 0 (gates S, L)" means the denominator. A different letter would help in later text.

## 2. The reduction for the singular P at q = 1 (`TARGET_A2_ADDENDUM_1.md` §3)

**Sound.** I read it against `lean/lean_p3_sdeformation_v3_2026-10-23/lean/BHModesP3.lean` (`prop3_Ioo` l.403,
`prop3_Dn` l.638).
- **P.** `hP`/`hP'` need P′ to exist and be continuous on (0, 1) only.
  - P = a(1 + ε)/(z + ε) + p₀ with ε ≥ 0 is C^∞ there, also at q = 1: ε = 0 puts the pole at z = 0, the boundary.
  - My drill D1 (§3) shows that gate S catches a pole moved inside the exterior.
- **The parameters.** q² ≤ 1. m = 6 > 0. δ = (s − 1)/12 ≥ 0 on [0, 1/8], because s = 7(6 − μ²)/(5(6 + μ²)) ≥ 1 exactly
  when μ ≤ 1.
- **N.** Lean's `Nz` (l.173) is the expression in `scert.py`:9/100, U − 64H²[(1 − z)f_zP + f(−P + (1 − z)P_z + P²)].
- **What stays pencil: R's existence.** That is what the report says. `prop3` needs some R : ℝ → (1, ∞) with
  dR/dr* = f(R). It does not need R to be onto.
  - At q = 1, f(ρ) = (1 − ρ⁻³)² is smooth and > 0 on (1, ∞), with f(1) = f′(1) = 0.
  - The solution with R(0) = 2 never reaches 1, because ρ = 1 is an equilibrium and f is locally Lipschitz.
  - It grows at most linearly, because f ≤ 1, so it exists on all of ℝ.
  - Nothing here uses a non-degenerate horizon. Onto ℝ (TARGET.md §1) is needed only to identify the operator.
- **Headline wording.** STAGE_REPORT.md:14–15 ends "no exponentially growing mode, through extremality". Two lines later
  (l.21) it says "Not claimed: … anything at q = 1 beyond the quadratic form".
  - `TARGET_A2.md` §2's Reading is the precise form: "no mode e^{κt}φ(r*) with κ > 0 and φ ∈ L²".
  - I suggest quoting that Reading in the headline.

## 3. The controls: is any weaker than registered?

All nine A2-S jobs give their registered verdicts (my re-run, §5). Checked against their stated reasons and against the frame
(`TARGET_A2_ADDENDUM_1.md`:89–90):

- **nc-a2: as registered, and discriminating.** Only POS-T and POS-C fail, both on the exceptional edges:
  C(0, 0) = −49340399616 and T(8, 0) = −3361641689088. POS-O and POS-O′ pass.
- **nc-zm: verdict as registered, but not discriminating, and RESULT.md:43 gives the wrong cause.**
  - POS-O fails at (19/64, 0). The cause is a = −1/2, not the lowering of U.
  - My check, `zm_mechanism.log`, gives N(19/64, 0) as follows:

    | Case | N(19/64, 0) |
    |---|---|
    | main (U, a = −2/5) | 2068.6 |
    | U − H₋²x⁴ with a = −2/5 (the lowering alone) | 2020.5 |
    | U unchanged with a = −1/2 (the residue change alone) | −21.9 |
    | both (nc-zm) | −70.0 |

  - So a verifier that accepted the zero margin would still REJECT nc-zm through POS-O, and the kit's `pos_only` would pass.
    Only the record's detail shows the zero margin being refused (POS-C: exactly 0 at (0, 0)).
  - RESULT.md:43 says "U₋ − H₋²x⁴ also lowers the outer region, so POS-O fails too". That needs a correction.
  - **A sharp version, drill D0.** Keep a = −2/5 and lower U by (16/25)H₋²x⁴. Then c′ = −2/9 − 4/225 = −6/25 = a(a + 1)
    exactly. The verdict is `REJECT: POS-C` alone, with C(0, 0) = 0 exactly; O, O′ and T pass.
  - I suggest adding D0 as an addendum control, with the verdict as an exact string and the corner value 0 checked.
- **nc-res: verdict as registered, but not specific.**
  - It fails in all four charts: at the corner (C(0, 0) = −73903104) and elsewhere, so it does not isolate the residue.
  - It is fine as a gross tamper. A residue-specific tamper (optional) would confine the change of the pole to near z = 0,
    e.g. by the factor (1 − z)^k for large k.
- **nc-bound: (a) is sound; (b) is weaker than "the certificate is refused" read plainly.**
  - (a): Q[b] < 0, certified in Arb, is a valid witness.
  - (b) is an exact Bernstein check of the planted NL on the bump box [1/20, 1/5] × {0}. The four charts run on the
    unplanted potential: POS-O, POS-O′, POS-T and POS-C all pass in the nc-bound record.
  - **Where the bump sits.** At q = 1, ℓ = 2, U₋ < 0 only for z < 0.0866846… (one sign change, exact count). So most of
    [1/20, 1/5], including its midpoint 1/8 where (b) refused, lies outside the well. The frame asks for a bound state
    "in the throat".
  - **Drill D5** runs nc-bound's planted potential through all four charts: all four REJECT. But POS-T and POS-C fail at
    the corner, because b(0) = 10⁻⁴ lowers W at the horizon by Kb(0) ≈ 340. That also breaks the throat's margin, so the
    rejection says nothing specific about the bump.
- **td-chart: as registered.**
  - It shows that the blow-up is needed: without the division by μ², T(ζ, 0) ≡ 0.
  - It is a verifier tamper, not a planted failure on the singular branch. No registered control puts a negative region
    inside T's box away from μ = 0.
  - **Drill D6:** NL − Kμ(z − μ)(3μ − z), with K = 128·T(2, 1/64) ≈ 1.25·10¹¹. The defect is zero at μ = 0, so T(ζ, 0) is
    unchanged. POS-T REJECTs with a counterexample at (ζ, μ) = (2, 1/32). So the T chart does detect negativity at μ > 0.
  - Suggestion for any later singular certificate: register a control of this kind, a planted throat defect that vanishes
    on the exceptional edge.
- **td-cover, td-coeff, td-verifier: as registered.**
- **Gates with no planted control and no tamper.** RULES.md:170 asks for "a planted control and a tamper for every gate".
  H, PARAM, DESIGN, G-RES, L, S, DIV-T and DIV-C have neither in STAGE_REPORT §E.4. My drills:
  - **D1** (the pole moved inside the exterior, ε_n → −ε_n): S FAILs, and so do all four POS charts.
  - **D3** (G-RES's comparison run on U + x⁴): FAIL, difference 16. The gate is not vacuous.
  - **D2** (the throat chart divided by μ³): REJECT, but as "exception PolynomialError", not as DIV-T.
    - The cause: `scert.py`:255 builds `Tp` from T even after DIV-T has failed.
    - The run stays fail-closed, but the DIV-T label can never appear. Stopping before `Tp` when `tdiv` or `cdiv` is
      false would fix this.
  - **Not drilled:** H, PARAM, DESIGN and L.

## 4. Other points

1. **Decimals, against your own BHM-060 rule ("quoted exactly or inward").**
   - STAGE_REPORT.md:33 has "A1's T3 ([0.97277, 0.99020]) overlaps A2-S ([0.98936, 1])". Both endpoints are outward.
     - Exact: T3 = [√(21576/22801), √(31416/32041)] = [0.9727663…, 0.9901988…], and q(1/8) = √(2961/3025) = 0.9893649….
     - Inward: [0.97277, 0.99019] and [0.98937, 1].
   - The same 0.99020 appears in TARGET_A2_ADDENDUM_1.md:27 and in s/PREREG.md:13.
   - ADDENDUM_1:27 writes "q(1/8) = 0.98937…", a rounding written as if it were a truncation. The digits are 0.98936….
   - BHM-060 and `results/p3/RESULT_ADDENDUM_1.md`:16 write √(31416/32041) as "0.9901987…". The digits are
     0.99019883….
   - The overlap holds exactly either way.
2. **`results/a2/elementary/PREREG.md`:13 has an inequality reversed.**
   - It reads "w(k/1000)² ≤ 1 − (99/100)². So q(μ_lo(ℓ)) ≤ 99/100". The first inequality gives q(μ_lo) ≥ 99/100, as
     l.26 and the RESULT say.
   - My values for q(μ_lo(ℓ)), ℓ = 3…10, run from 0.9900005 (ℓ = 4) to 0.9901675 (ℓ = 9).
   - **Consequence for the stated dependencies.** For ℓ = 3…10, Theorem A2's range [99/100, 1] is A2-E's [q(μ_lo), 1]
     plus A1's P1 on [99/100, q(μ_lo)), slivers of up to 1.7·10⁻⁴. The composition bullet says this. The status row
     (STAGE_REPORT.md:80, "resting on the rows above and on Lemma U") should add A1's P1.
3. **The kits and the environment.**
   - My host: Python 3.12.8, python-flint 0.9.0 / FLINT 3.6.0, sympy 1.14.0, but gmpy2 2.3.1.
   - There all three kits print KIT FAIL with `BHM_REF` set. The only difference is `/provenance/gmpy2` (2.3.2 against
     2.3.1). Every verdict, every other field and every `run.log` matches.
   - The kits check the flint and sympy versions only. Either check gmpy2 too (exit 2, "environment mismatch"), or mask
     the provenance field and compare it separately. Otherwise a correct third-party reproduction prints KIT FAIL.
4. **[another line of this project] (`[a record of another line of this project]`, for information).**
   - I read it and found no issue at the level of a reading.
   - Your "monodromy-free conditions" b₋₁ = b₁ = 0 at b₋₂ = 2 are, as I recall them, the Duistermaat–Grünbaum
     trivial-monodromy conditions for ℓ(ℓ + 1) = 2. That is from memory; check the source before citing it.
   - The second parties are the operator's routing. My CHARTER §5 role is review only.

## 5. Checked, and not checked

**Checked (the lead's own work; all files are in this folder):**
- **The snapshot.** bh-modes at `2416726` (`git archive`); `INPUTS.sha256` lists the files read.
- **Re-runs on host-0.** They ran from `git archive`s of the commits of record. The archive hashes match the RESULTs:
  `a565ef2b…` (`25c796e`), `69712348…` (`e422d74`) and `a87c1d71…` (`5497819`).
  - Verdicts as registered: A2-S 9/9, A2-E 6/6, pilot 1/1.
  - All 16 `run.log`s are byte-identical to the records.
  - Every `result.json` is identical after masking, apart from the gmpy2 provenance field.
  - Caps: soft `ulimit -v` 4 GB, `timeout` 900 s. A2-S took 7 s; each of the other two took seconds.
- **An independent N (`lead_checks/lead_indep_a2s.py`).** Built from TARGET.md §1 as printed, PREREG §2's design and the
  pilot record's Chebyshev coefficients.
  - It equals bh-modes' NL/(S²L) exactly, as polynomials in z at μ = 0, 1/64 and 1/8. It also matches at 30 rational
    points, 9 of them throat points z = μζ.
  - **Exact Sturm counts:** N·(z + ε)² has no root on the closed interval [0, 1] and is positive, at μ = 0, 10⁻⁶, 10⁻⁴,
    10⁻³, 10⁻², 1/32, 1/16, 1/10 and 1/8. That is q² from 1 down to 2961/3025.
  - This is a second positivity method at nine charges, not a certificate for every μ.
- **By reading:** the coverage logic; the Lean hypotheses (`prop3_Ioo`, `prop3_Dn`); and the parametrisation.
  - param_n(4, 2) gives w = 7μ/(6 + μ²) and s = 7(6 − μ²)/(5(6 + μ²)). (1 + 2mδ)² = 1 + 4mq²/25 holds (by hand), and
    δ(0) = 1/30, which is g_res's d at ℓ = 2.
- **The nc-zm mechanism, and six drills.** D0–D3, D5 and D6, in `lead_checks/drills/`. They are driven from my own
  script; nothing in the bh-modes tree was edited.

**Not checked:**
- No independent transcription of S5. E0 compares with bh-modes' own S5 forms, and my N starts from TARGET.md as printed.
- The Bernstein prover itself. It rests on A1's KATs and was blind-replicated at D = 7.
- The Lean build. I read the statements only.
- The pilot's design rule, and A2-E beyond its re-run.
- No second-party role.

**Disclosure.**
- At 00:13:46 EDT one of my commands ran a job with [repository] as its working directory. It created an untracked
  file there, `kit_pilot_lead.log`: 85 bytes, "No such file or directory", exit 127, no run started.
- I moved it out at 00:13:52. It is kept in `rerun/stray/` with its hash.
- `git status` was clean before and after. Nothing else was written in the bh-modes tree.
