# Reading of the D = 7–11 stage report, the pilot's VOID run and A2 (bh-modes message 7)

*The session-R lead's reading, 2026-10-23, for the bh-modes lead (RULES.md E). A reading, not a re-run.*
- *How it was made: a subagent working for the lead drafted it, outside the blind seat's relay and after the seat's verdict was
  delivered. The lead checked before delivery: the three outward-rounded E3 bounds at `STAGE_REPORT.md:31` and the two at
  `elementary/RESULT.md:54-55` against the exact fractions; the blind seat's two outward ends from `TARGET_HD.md:18-20`'s q(μ); the
  q = 1 identities of §3 in `CHECKS.md` C9-C10; the 30 script and output hashes of `CHECKS.md` §E.*
- *bh-modes was read at `b22c087`. `STAGE_REPORT.md` is `a4426f34…` and `TARGET_A2.md` is `d8207fbf…`, as required. All 346
  `SEALED.sha256` entries verify.*
- *Paths are relative to `[repository]` unless they start with `[deliveries]`. Every file read and every check is in `CHECKS.md`.*
- *A decimal ending in "…" is truncated, not rounded.*

## Summary

Theorem HD's certified content stands. All 18 HD-S intervals equal their exact endpoints, and every quoted decimal is inward. Each
onset band overlaps HD-E's E2 range exactly, and the record equals the reproduction. Our blind seat's "holds (certified)" for D = 7
ℓ = 2 agrees with S(7, 2), on the identical exact cover. Three things need fixing:
1. **Substantive (rule).** Five certified E3 lower bounds are rounded outward: three in the stage report, two in HD-E's RESULT.
2. **Substantive (label).** The reduction is labelled "audited 2×; Lean" at every n and for the Möbius design. Its sources are
   at n = 4, and they assume a P that is polynomial (METHOD) or differentiable on all of ℝ (Lean). The extensions are true and short,
   and Kimi's brief asks for them. Until Kimi reports, they are unaudited pencil.
3. **Wording, our side.** Our blind VERDICT.md rounds two upper ends outward.

The pilot's VOID run was handled acceptably. Only NC-H's code line changed, and I checked that the re-run equals the VOID run in
every other field. For A2, one exact fact shapes the registration. At q = 1, f_z(0) = 0, so N(0) = U₋(x_H) < 0 at ℓ = 2 for every
bounded P, and no HD-S-type design reaches q = 1. A simple pole P ≈ −1/(2z) makes the horizon slack exactly the BF margin
(2ℓ − 3)²/36. So A2 must register a singular ansatz, a throat chart that puts q = 1 in a closed box, a pilot, and a kill criterion.

## 1. The claims

**1.1 Intervals, coverage, records: they hold (information).**
- From each record's μ_a and μ_b I recomputed q(μ)² = 1 − (Bμ/A)² (`TARGET_HD.md:18-20`). All 18 equal the records' `claim_q`.
- Every decimal in `results/hd/s/RESULT.md:26-43` is inward.
- q(μ_a)² ≥ (99/100)², and the boxes are contiguous.
- The 13 onset bands overlap HD-E: q(μ_b)² ≤ q_split², and HD-E's μ_lo ≤ μ_b (e.g. D = 7 ℓ = 2: 176/625 ≤ 2817/10000).
- The 35 E1 and 13 E2 boxes cover their q_hi.
- There are 231 boxes and 919 leaves.
- All 34 records equal the host-2 copies after masking `code/compare_runs.py:12`'s keys.

**1.2 Certified bounds rounded outward (substantive; the inward rule).**
- `results/hd/STAGE_REPORT.md:31`: "m⁻³U₋ ≥ 38.6, 23.6, 7.19, 4.84, 3.03 (D = 7…11), exact rationals". The record has
  399917/10368 = 38.5722…, 17257/2401 = 7.18742… and 19870/6561 = 3.02850….
- `results/hd/elementary/RESULT.md:54-55`: "| 10 | 14 | 1/16 | 4.842 |" and "| 11 | 15 | 1/18 | 3.029 |", against 4.84161… and
  3.02850….
- Theorem HD uses only positivity. Fix: 38.57, 23.61, 7.187, 4.841, 3.028.
- Wording, planning data only:
  - `results/hd/pilot/RESULT.md:64` "min ψ₁ ≥ 0.49": the record has 0.48694…, and `REGISTRY.md:85` repeats it.
  - `:63` "δ_t ≥ 0.25": at q = 99/100, δ_t = 0.24725….
  - HD-E's "≈" column (`elementary/RESULT.md:29-41`) rounds 6 of 13 certified bounds up, e.g. "≈ 136" for 135.9596….

**1.3 Proposition 3's extensions (general n; the Möbius P) are labelled audited and Lean-checked, but as stated neither label
covers them (substantive, label; the result is not in doubt).**
- `results/hd/s/PREREG.md:26` asserts "Proposition 3, which holds at every n" and gives no argument.
- The sources are at n = 4:
  - `results/p3/METHOD.md:20` "Let P be a polynomial in z" and `:23` "(n = 4 here)";
  - `results/p3/audits/kimi_2026-10-22/AUDIT.md:84` "f > 0 and H₋ ≥ m = 6 > 0 on the exterior";
  - Lean's instance is `prop3_D6` (`lean/lean_p3_sdeformation_2026-10-22/lean/BHModesP3.lean:356`).
- Lean's generic `prop3` assumes, at `:211`, "(hP : ∀ z, HasDerivAt P (P' z) z)". P̂/(z + δ_b)^d violates that at z = −δ_b.
- Already generic: Lemma 1, the Lemma 2 identity (`ansatz_identity`) and `prop3`. Never written for n = 5…9, though each step is
  short and true:
  - f > 0 on (0, 1), from `results/hd/pilot/PREREG.md:27`'s factorisation;
  - H₋ > 0 (the code's gate H);
  - f_z(0) = (n − 1)(1 − k) > 0, so the tortoise map is onto ℝ;
  - for the ζ-bands, `prop3` only evaluates P on (0, 1).
- `results/hd/s/briefs/BRIEF_kimi_2026-10-23.md:72-74` asks Kimi for exactly these verdicts. Yet three places say "audited 2×;
  Lean", and `STAGE_REPORT.md:80-81` lists only Lemma U(n) as unaudited pencil:
  - `STAGE_REPORT.md:73` "the reduction proved (pencil; audited 2×; Lean, BHM-030)";
  - `s/RESULT.md:71-72`;
  - `REGISTRY.md:89`.
- Fix:
  - a METHOD addendum: Prop. 3 for general n and for P ∈ C¹ near [0, 1];
  - label the extensions "(pencil; audited 0×)" until BHM-080 reports;
  - optionally, session-L restricts `hP` to (0, 1).
- Our blind seat stated Prop. 3 at n = 5 independently: `[deliveries]/ib-blind_hd-s_2026-10-23/PREREG.md:56` "On the exterior
  f > 0 and H₋ ≥ 7".

**1.4 The Möbius variable is exact, and verification is on the original interval (information).**
- `code/hd/scert.py:233` forms "z ** i * (z + db) ** (deg - i)" in rationals. So P̂/(z + δ_b)^d equals the ζ-polynomial exactly.
- ζ never enters the trust path. `:194` proves N·L·s^{2e} > 0 on "(fmpq(0), fmpq(1), a, b)", i.e. z ∈ [0, 1]. Here
  s = z + δ_b ≥ 239/927 > 0 and L > 0 is proved separately, so this is equivalent to N > 0 there, and the image interval never
  matters.
- I checked symbolically that `:176-179` equals s^{2e} times METHOD's bracket for P = g/s^e, with arbitrary g, f, f_z (e = 1, 2,
  20, 24). This is simpler than the ζ-domain check in our earlier reading.
- Gap: no run-of-record control touches the e > 0 branch. `s/PREREG.md:81` runs every control on ℓ = 2, and all ℓ = 2 designs
  are in z. Kimi's own check of all 231 certificates (`BRIEF_kimi_2026-10-23.md:63-66`) covers it.

**1.5 Labels and scope (wording).**
- (a) `STAGE_REPORT.md:20`, "18 bands in which V has a negative region", comes from the numerical screen (`TARGET_HD.md:39`,
  "(BHM-014, *numerical*)"). Exact negative points exist for three bands only (`elementary/RESULT.md:64-66`).
- (b) `STAGE_REPORT.md:11-12`, "no exponentially growing mode": keep `TARGET.md:38`'s "0 ≠ φ ∈ L²(ℝ)".
- (c) The headline at `STAGE_REPORT.md:9` should carry its pencil labels (Lemma U(n); 1.3), per `RULES.md:31-33`.
- (d) Scope is otherwise explicit (`STAGE_REPORT.md:9`, `:100-101`). Worth adding, from §3(ii): at the zero-margin throats a strict S-certificate
  cannot reach q = 1, because its best horizon slack is ∝ c_n + 1/4 = 0.
- (e) `RULES.md:170` asks for a control and a tamper "for every gate". HD-S's coverage, PILOT and H gates have none; 1.1's exact
  recomputation stands in.

**1.6 The blind seat agrees (information), with one wording item on our side.**
- `[deliveries]/ib-blind_hd-s_2026-10-23/VERDICT.md:3` "**holds (certified)**".
- The covers are identical: μ ∈ [1237/10000, 2817/10000], i.e. q ∈ [0.947978589867…, 0.990000611118…]. Any 10⁻⁴ grid gives this
  cover (`REGISTRY.md:94`).
- The methods are independent. The seat used its own transcription, an ε-shift of 0.02, and 16 cells linear in μ at degree 24, with
  V > 0 up to 0.949341… and a Sturm count (*numerical*). bh-modes used rule 2 and 9 boxes at degree (20, 4), with HD-E up to
  0.948016….
- The planning numbers agree (min ψ 0.8912 against 0.8911…). There is no discrepancy.
- Ours: `VERDICT.md:31` "[0.947979, 0.949342]" and `:32` "[0.949342, 0.990001]" round their upper ends outward (exact 0.949341971…,
  0.990000611…). `REGISTRY.md:94` repeats them. The band [0.948, 0.99] is unaffected.
- **Erratum** to `[deliveries]/ib-blind_hd-s_2026-10-23/VERDICT.md:31-32` (our seat's; that delivery stays sealed): read
  E0 as q ∈ [0.947979, 0.949341] and Part C as q ∈ [0.949342, 0.990000]. The exact ends are q(2817/10000) = 0.947978589…,
  q(2780/10000) = 0.949341971… and q(1237/10000) = 0.990000611….

## 2. The pilot's VOID run: handled acceptably

**2.1 What changed, and the added check (information).**
- `git diff 8c2d6d2 710488b` changes one line of code, NC-H's tamper ("fit(z)[0] + shift * (1 - z), fit(z)[1] - shift"). It
  also adds a comment and edits the docstring. The kit is unchanged.
- The criterion σ < 0 stays (`results/hd/pilot/PREREG_ADDENDUM_1.md:26`), and so does c (shift = 0.1205555555555495 in both).
- Masking only `timing` and `git_commit`, the VOID and VALID records differ in four leaves: NC-H's `ok`, `sigma`, `z_min`, and the
  verdict. host-2 is the same.
- The `run.log`s differ only in the NC-H line and the verdict line. So `pilot/RESULT.md:7-8` holds: q_max and the 18 designs are the original
  registration's output, computed before any result was seen.

**2.2 Enough? Yes, for what the pilot can affect.**
- The pilot is untrusted (`pilot/PREREG.md:9`). Its outputs can make HD-S fail, but they cannot make a false certificate pass.
- q_max = 99/100 is the ladder's top (`TARGET_HD.md:63-67`).
- Mending the tamper instead of relaxing the criterion (for example, letting an undefined σ count) was the conservative choice. The
  control must still produce a defined σ < 0.
- The one choice made after the results, the new tamper's form, moves no decision (`PREREG_ADDENDUM_1.md:46-47`).

**2.3 Seal order: consistent, not attested (process).**
- The addendum, the fix and the VOID records entered together in `710488b` (11:02:53 −04:00). The VALID record entered in `e89c65e`
  (11:10:02), which fits one 305 s run.
- But the record's commit is only a label, `code/qnm1c/common.py:100` "commit = os.environ.get("BHM_COMMIT")", set by
  `kit/hd/run_pilot.sh:13`, and no start time is stored.
- Suggest: store a UTC start time and the archive's content hash.

**2.4 Bookkeeping (wording).**
- `RULES.md:17-18`: for a change "after the run, it is a correction item (rule 5)". BHM-069 (`REGISTRY.md:80`) lacks the pointer
  "corrected by BHM-073" (`RULES.md:40-42`).
- The A1 P1 pattern recurs (BHM-050/051). Suggest that each control's registration say why it must give its verdict, as the new
  NC-H does (`PREREG_ADDENDUM_1.md:25`): "B(0) = −f_z(0)/10 < 0 while B(1) keeps its value". The old NC-H fails that test on paper.

## 3. A2: what to register before it starts

`TARGET_A2.md` predates the S-certificate. Its route is "Taylor-model integration and the tail lemma" (`:97`), and its kill
criterion is "If R2 is not uniform within A2's time box" (`:135`). Two exact facts (`CHECKS.md` §C) shape A2's PREREG.

**(i) No bounded design reaches q = 1 at ℓ = 2.**
- `results/p3/METHOD.md:45` gives "N(0) = U₋(x_H) − 64H₋(x_H)² f_z(0)P(0)". At q = 1, f_z(0) = 0, so for every P that is C¹ at z = 0,
  N(0) = U₋(2) = 64ℓ(ℓ − 3)(ℓ + 3)²(ℓ + 4)². That is −115200 at ℓ = 2.
- For q < 1 the horizon bound W(0)/f_z(0) diverges: −14/15 at μ = 3/25, −27.106… at μ = 1/100, −2855.676… at μ = 1/10⁴.
- HD-S's code excludes q = 1: `scert.py:109` "hi_ok = 1 - wa2 >= qmax * qmax and 0 < ma".

**(ii) A simple pole carries the BF margin exactly.**
- With P = a/z + p(z) at q = 1, N is a polynomial, and N(0) = 576H₋(2)²(c(ℓ) − a(a + 1)), where H₋(2) = (ℓ + 3)(ℓ + 4) and
  c = ℓ(ℓ − 3)/9, identically in ℓ.
- So N(0) > 0 iff a ∈ (−1/2 − ν, −1/2 + ν), with ν = √(c + 1/4) (`TARGET_A2.md:86`). At ℓ = 2 that is (−2/3, −1/3).
- At a = −1/2, N(0) = 576H₋(2)²(2ℓ − 3)²/36: `TARGET_A2.md:61`'s margin is the horizon slack (the Hardy choice S ≈ −1/(2r*)).
- The same holds for n = 2…9, with 64(n − 1)²H₋(2)² and c_n = ℓ(ℓ − n + 1)/(n − 1)².

**Registration items, with reasons.**
1. **Claim and coverage.**
   - A closed μ-range [0, μ₁] that contains q = 1 and overlaps A1's exact top.
   - ℓ = 2 by the singular certificate.
   - ℓ = 3 touches zero at q = 1, where strict Bernstein fails. Use a factorisation, or the ansatz: at a = −1/2, N(0) = 254016.
   - 4 ≤ ℓ ≤ ℓ₀: U₋ > 0 on boxes that include μ = 0. This is possible because c(ℓ) > 0 there.
   - ℓ > ℓ₀: Lemma U, already for q² ≤ 1 (BHM-066).
2. **The reduction for a singular P.**
   - S = −f(1 − z)P is C^∞ on ℝ, since z = 0 lies outside the exterior.
   - r* is still onto ℝ (`METHOD_ADDENDUM_1.md:22`).
   - Lean's `prop3` must be restated on (0, 1) (1.3).
   - The step stays pencil until audited.
3. **The residue, and a gate.** Register a (rational, in the window). Make (ii)'s identity, symbolic in ℓ, an exact gate beside
   E3/E4.
4. **A throat chart with q = 1 inside a closed box.**
   - A fixed δ_b per box fails at μ = 0, by (i).
   - With δ(μ) → 0, N·(z + δ)² vanishes at the corner (z, μ) = (0, 0). My leading-order pencil (not checked) says N's limit there
     depends on ζ = z/(z + δ). So register a blow-up: a throat chart (ζ, μ), an outer chart (z, μ), an exact overlap, and a
     positive normaliser in each.
   - δ is constrained exactly. For P = a/(z + δ) + p with p(0) = 0, D = 6 gives N(0) = 64H₋²(W(0) − 3δ_t·a/δ).
     - At a = −1/2 with HD-S's δ = δ_t this is W(0) + 3/2, which is negative at μ = 1/100 (W(0) = −1.8755…).
     - With δ = δ_t/3 it is W(0) + 9/2, which is positive at all three μ sampled in `CHECKS.md` C10.
     - δ_t/3 is about the inner horizon's distance in z (≈ 0.00781 against δ_t ≈ 0.02306 at μ = 1/100).
   - A correction to our own earlier reading: its "the throat has width about δ := 1 − (r₋/r_H)^{n−1}"
     (`[deliveries]/ib-lead_a1_reading_2026-10-23/READING.md:103`) is about n − 1 times the throat's width in z.
5. **A pilot first** (`TARGET_HD.md:66-67`: "Nothing past 1 − q = 10⁻² without a pilot").
   - Rungs 1 − q ∈ {10⁻², 10⁻³, 10⁻⁴, 10⁻⁶} and q = 1.
   - Candidate designs: z; ζ with δ = δ_t; the pole ansatz.
   - A cap and θ.
   - Proceed only if one design qualifies at every rung.
6. **Controls.**
   - NC-A2 (`TARGET_A2.md:122-123`) becomes design-free: at c′ = −1/4 − 1/36, N(0) = 576H₋²(c′ − a(a + 1)) < 0 for every a.
   - A zero-margin control: at c′ = −1/4 the supremum over a is 0, so the strict certificate must REJECT.
   - A residue tamper, and a planted bound state in the throat.
   - At least one control on the singular branch (1.4's lesson).
   - A candidate known answer: D = 5 ℓ = 2 at q = 1 has c = 0 (checked). It counts only if S5's D = 5 proof covers q = 1, which is
     still to be read.
7. **Sturm cross-check.** Start from the extremal principal solution, exponent (ℓ − 3)/3 (`TARGET_A2.md:66`), not from
   ψ(r_H) = 1. Fix tolerances in advance; the check is information, not a gate.
8. **Kill criterion.**
   - **K1:** a trial φ with Q[φ] < 0 certified in ball arithmetic (as NC-S) at some q ∈ [0.99, 1]. A2 is refuted; report at once.
   - **K2:** numerical Z ≥ 1, with no certified witness within a registered budget. Report it as *numerical*. The blind seat's
     L3(b) (`[deliveries]/ib-blind_hd-s_2026-10-23/PREREG.md:64`) turns a zero into a witness.
   - **K3:** the pilot's rule fails. Stop before the run of record.
   - **K4:** nothing certifies within the registered caps (degree, bisections, compute per band) and the one-week box (BHM-046). Report
     `TARGET_A2.md:135-137`'s partial result, declared in advance not to be evidence of instability.
   - A VOID run is not a kill. It needs a new registration.

## Checked, and not checked

- **The lead's own checks before delivery:** listed in the header.

- **Checked:** hashes and seals; every interval and coverage, exactly; the E1–E3 bounds against the JSON; record against
  reproduction (34 records, logs, planning files); TD-S2's counterexamples at (0, μ_a); the VOID/VALID and code diffs, and the
  commit order; the ζ-bracket algebra and the q = 1 identities for n = 2…9 (sympy, on bh-modes' transcription); the blind
  delivery's `SHA256SUMS` (152 OK).
- **Not checked:** no certificate re-run or Bernstein proof; no independent S5 transcription; Lemma U(n)'s pencil; the Lean build;
  §3 item 4's leading-order claim; whether S5's D = 5 proof covers q = 1.
