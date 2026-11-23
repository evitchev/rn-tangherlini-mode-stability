# PREREG — HD-S: S-certificates on the 18 bands of D = 7–11 (stage 2, step 2)

*Item BHM-076. 2026-10-23, the bh-modes lead. Part HD-S of `TARGET_HD.md` (BHM-061), with q_max(D) = 99/100 and
the designs of `TARGET_HD_ADDENDUM_1.md` (BHM-075). The gates follow `TARGET_HD.md` §5 and the
session-R lead's advice (BHM-058 §2). Sealed; any change before the run is a dated addendum.*

## 1. Claims (exact)

**S(D, ℓ),** for each of the 18 bands of `TARGET_HD.md` §3: A_{ℓ,q} ≥ 0 for every q ∈ [q(μ_b), q(μ_a)]. This is
an exact interval containing [q_lo, 99/100].
- q_lo = q_split for the 13 bands with an onset (HD-E, BHM-062 §2).
- q_lo = 0 for the 5 bands from 0⁺ (D = 8–11 ℓ = 2, D = 11 ℓ = 3).
- The interval's ends are given exactly, as square roots of rationals, and quoted with inward decimals
  (BHM-060).

**What follows with HD-E (BHM-063): Theorem HD** (`TARGET_HD_ADDENDUM_1.md` §1), for D = 7–11, every ℓ ≥ 2 and
every q ∈ (0, 99/100]:
- every ℓ < ℓ_el(D) is one of the 18 bands; every ℓ ≥ ℓ_el(D) is covered by HD-E's E1 and E3;
- a band with an onset is covered by HD-E's E2 for q ≤ q_split, and by S(D, ℓ) from q(μ_b) ≤ q_split up to
  q(μ_a) ≥ 99/100. For the interior band (D = 10 ℓ = 3) this is the exact check, which `TARGET_HD.md` §5
  requires, that the first box starts below the onset;
- a band from 0⁺ is covered by S(D, ℓ) alone, from q = 0 (μ_b = 1).

## 2. Method (`code/hd/scert.py`)

**The reduction.** It is `results/p3/METHOD.md`'s Proposition 3, which holds at every n: N ≥ 0 on [0, 1] proves
A_{ℓ,q} ≥ 0.
- METHOD.md is proved in pencil and audited twice (Kimi, Fable); its Lemmas 1–2 and Proposition 3 are
  machine-checked in Lean (BHM-030).
- METHOD.md's remark on parameter boxes extends this to μ-boxes.

**The coverage, exact.**
- **The μ-boxes.** μ_a = ⌊10⁴ μ(99/100)⌋/10⁴, and μ_{i+1} = min(⌈10⁴ · (11/10) μ_i⌉/10⁴, μ_b).
  - μ_b = 1 for a band from 0⁺.
  - Otherwise μ_b = ⌈10⁴ μ(q_lo)⌉/10⁴.
- **The checks:** q(μ_a)² ≥ (99/100)²; q(μ_b)² ≤ q_lo² for a band with an onset; the boxes are contiguous.
- **w increases on [0, 1]** (pencil): w′ = B((ℓ + n) − (ℓ − 1)μ²)/A², and (ℓ + n) − (ℓ − 1)μ² ≥ n + 1 > 0.

**The design (untrusted),** per box.
- Rule 2 (BHM-024) with the band's ε, variable and degree from `TARGET_HD_ADDENDUM_1.md` §2.
- P_d is computed with `hd.pilot`'s floats at the Chebyshev–Lobatto nodes in μ (degree 4) and in the variable.
  - The variable is z on [0, 1], or ζ = z/(z + δ_b) on [0, 1/(1 + δ_b)].
  - δ_b is the rational of denominator ≤ 1000 nearest to δ_t at the box's mid-point (`Fraction.limit_denominator`).
- The coefficients are the floats' exact binary values. For a ζ-design, P = P̂/(z + δ_b)^d with P̂ a polynomial
  in (z, μ).

**The planning record (untrusted; BHM-058 §2.5).** At each μ-node of a box it holds q, the minimum of ψ₁, the
exact design's σ and the one-dimensional fit's σ. It is written to `planning.jsonl` before that box's
verification.

**The verification (the trust base).**
- N·L·s^{2e} is built exactly as a polynomial in (z, μ). L = U_den·H_den²·f_den, and s = z + δ_b, e = d for a
  ζ-design (s = 1, e = 0 for z).
- L > 0 and N·L·s^{2e} > 0 on [0, 1] × box are proved by exact Bernstein bisection
  (`onset.bernstein.prove_sign`; depth ≤ 30 for L and ≤ 40 for N).
- Fail-closed.

**The fallback (registered).**
- A box that does not verify is redesigned at the next two degrees of {16, 20, 24, 28, 32, 40, 48}, capped at 48.
- If it still fails, it is bisected at its μ-midpoint and the whole procedure is applied to each half, at most
  three times.
- The band is REJECT if a piece fails after the last step.
- Every attempt is recorded.

**Compute.** The bands run as separate processes, at most 8 at a time per node, under `nice -n 19`, each with a
12-hour cap. A band that reaches the cap is reported as not complete.

## 3. Gates, per band

| Name | What | Must |
|---|---|---|
| KAT | the verifier's KATs (`a1.p1`) | hold |
| E0n | `ki.potentials`' U₋, H₋ equal Kimi's independent transcription for n = 2…12 (HD-E's gate) | hold |
| PILOT | the code's design table equals the designs at q_max of the VALID pilot record (`results/hd/pilot/runs/record/main/result.json`) | hold |
| H | H₋ has positive coefficients, so H₋ ≥ m > 0 | hold |
| coverage | §2's exact checks | hold |
| G-S6 | for a band from 0⁺, the box ending at μ = 1 (q = 0) verifies: S6's known answer (proved), the band's must-pass gate. At D = 10 it was passed as a point (G1, BHM-025) | hold |

## 4. Controls and drills

Each runs on the first band of each D (ℓ = 2), and td-verifier runs once. Each must end with exactly its
registered verdict.

| Name | What | Registered verdict |
|---|---|---|
| NC-S(D), `nc-bound` | A planted bound state, scaled to that D's own potential. At the first box's mid-point μ_c: W − Kb on [3/10, 3/5], with b = ((z − 3/10)(3/5 − z))² and K = ⌈2I₁/I₂⌉ from floats. (a) The trial function b's energy is certified < 0 by Arb's rigorous integration; (b) the first box's certificate, at μ_c, is checked against the planted potential | `REJECT: nc-bound (b)`, with (a) holding |
| TD-S1(D), `td-coeff` | U₋ + 16nm² | `REJECT: E0n` |
| TD-S2(D), `td-horizon` | The first box's certificate plus c(1 − z)s^e, where c = W(0)/f_z(0) − P(0) + 1/10 at μ_a, so P(0) is 1/10 above the horizon bound there | `REJECT: td-horizon` |
| TD-S3, `td-verifier` (D = 7 ℓ = 2) | the verifier's acceptance threshold lowered to −1 | `REJECT: KAT` |

## 5. S14's Table I: consistency information, not a gate

- **What S14 reports** (SOURCES.md, *cited*, *numerical*): the ℓ = 2 scalar-type modes of V₋ are damped for
  D = 6–11 at Λ = 0.
- **Its range:** its rows reach q_S14 = 0.98 for D ≤ 8 and 0.9 for D ≥ 9. In our q = 2q_S14/(1 + q_S14²), that is
  ≈ 0.9998 and ≈ 0.9945.
- **The comparison is of verdicts.** A VERIFIED S(D, 2) agrees with it. So no numerical tolerance is needed.
- A REJECT would be a failure of the certificate, not evidence against S14.

## 6. The blind replication (the operator's ruling, BHM-064)

- **The first band, D = 7 ℓ = 2** (q ∈ [0.948, 0.99]), is the blind slot.
- **The brief:** `results/hd/s/briefs/BRIEF_ib-blind_2026-10-23.md`, sealed with this file. It goes to the
  session-R lead before HD-S runs, and the seat's runs of record go to host-1/005.
- **The comparison:** the seat's verdict is compared with S(7, 2). A disagreement is reported and investigated,
  never averaged away.

## 7. Pass criterion, and what follows

- **A band is VERIFIED** if its gates hold and every box verifies, fallback pieces included.
- **HD-S is VERIFIED** if all 18 bands are VERIFIED and every control and drill ends with its registered verdict.
  The record runs on host-1 and the reproduction on host-2, from a `git archive` of this commit
  (`kit/hd/run_s.sh`), and they must be identical after masking.
- **Status on VERIFIED:**
  - each S(D, ℓ) is *certified* (exact); the reduction is proved (pencil; audited 2×; Lean);
  - with HD-E, **Theorem HD is certified for D = 7–11 at q ≤ 99/100**;
  - second parties: the blind replication of D = 7 ℓ = 2, and a Kimi brief afterwards.
- **On a band's REJECT:**
  - it is reported as it stands, with its counterexamples, and nothing more is tried under this registration;
  - each D's certified q-range is reported, the deliverable of `TARGET_HD.md` §6.

## 8. What ran before this registration

- **Development, on host-1,** from a `git archive` of `e9f59ab`:
  - syntax checks;
  - `python -m hd.devtest_s`, synthetic inputs only: U = 64m³ + 400x² + x⁴ and H = m + 15x at (n, ℓ) = (5, 4);
  - one box, μ ∈ [1/2, 11/20], in z and in ζ at degree 16: design, verification (VERIFIED) and a tampered
    certificate (REJECT);
  - the partition rule for (5, 4) (24 boxes); the inward decimals; w at μ = 1.
- **Not run:** S5's U₋ and H₋ were evaluated for no band, and no gate, control or band was run.
- **HD-PILOT ran before this** (BHM-072 to BHM-074), as `TARGET_HD.md` §4 requires: untrusted, floats only.

## 9. Artifacts

- `code/hd/scert.py` and `kit/hd/run_s.sh`.
- `code/hd/pilot.py` (the floats of the design) and `code/hd/elementary.py` (`BANDS`, `param_n`, `gate_E0n`).
- `code/a1/p1.py`, `code/onset/bernstein.py`, `code/onset/onset.py`, `code/p3/scert.py` and `code/ki/potentials.py`.
- `results/hd/pilot/runs/record/main/result.json` (PILOT) and `results/p3/audits/kimi_2026-10-22/own/build.py` (E0n).

All are at the commit that holds this file.
