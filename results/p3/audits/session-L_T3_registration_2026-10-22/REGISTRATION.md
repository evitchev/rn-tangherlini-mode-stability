# Item (c), option B: registration of an independent exact re-run of T3 (bh-modes, ℓ = 2): session-L, 2026-10-22, before any run

> **For second-party seats** (Kimi, the session-R lead's blind subagent): please do not read this folder
> before your own check.

**Status: registered, not started.**
- The bh-modes lead's third message (`outbox/2026-10-22-to-session-L-3.md`, §4) asks the operator whether this
  re-implementation counts as CHARTER e5's second party, and asks for this registration before any start.
- The run waits for the operator's ruling.
- Nothing has been computed on T3's certificates except what §6 lists.

## 1. The claim (C-B)

**Data.**
- `result.boxes_mu[k].{mu, P}`, k = 0, …, 7, of bh-modes `results/p3/runs/record/T3/result.json`. Its sha256 is
  `f893d820aa0f289f…`, as in `results/p3/RESULT.md`.
- The key "(i, j)" of P_k is the coefficient of z^i μ^j, with μ the global parameter of BHM-016. This was settled on P
  values alone (§6).

**The claim.** For every k and every (z, μ) ∈ [0, 1] × [a_k, b_k]:

    N_k(z, μ) > 0,

where N_k is METHOD.md Lemma 2's N, exactly as the item (a) Lean file defines it:

    N_k(z, μ) = Nz (U6 q 6 δ) (H6 q 6 δ) (F6 q) (F6' q) P_k(·, μ) ∂_zP_k(·, μ) z.

- m = 6, and q = q(μ), δ = δ(μ) come from item (b): w = 7μ/(6 + μ²) = √(1 − q²) and δ = (1 − μ²)/(5(6 + μ²))
  (`param_of_q`, `delta_of_q`, `O5_sqrt`).
- The eight boxes are contiguous, cover [3/25, 1/5], and each is at most 1/100 wide.
- The claim is strict on the closed box, so it includes the horizon (z = 0) and spatial infinity (z = 1).

**What it gives, with the Lean layer.**
- For each μ ∈ [3/25, 1/5], C-B supplies hypothesis hN of item (a)'s `prop3_D6`, at q = q(μ), δ = δ(μ), m = 6,
  P = P_k(·, μ) and P' = ∂_zP_k(·, μ).
- The other hypotheses hold: q² = 1 − w² ≤ 1, m > 0, δ(μ) ≥ 0 for μ ≤ 1, and P_k is a polynomial in z.
- So the quadratic form is ≥ 0 for every inverse tortoise map R. That is the record's T3 conclusion, A_{2,q} ≥ 0 for
  q ∈ [0.97277, 0.99020].
- **Outside Lean:** the identification of the re-run's polynomial with Nz is checked exactly by sympy (X1 below), not
  proved in Lean.

## 2. The boxes

| k | [a_k, b_k] | q range (rounded) |
|---|---|---|
| 0 | [3/25, 13/100] | [0.98850, 0.99020] |
| 1 | [13/100, 7/50] | [0.98666, 0.98850] |
| 2 | [7/50, 3/20] | [0.98468, 0.98666] |
| 3 | [3/20, 4/25] | [0.98257, 0.98468] |
| 4 | [4/25, 17/100] | [0.98033, 0.98257] |
| 5 | [17/100, 9/50] | [0.97794, 0.98033] |
| 6 | [9/50, 19/100] | [0.97542, 0.97794] |
| 7 | [19/100, 1/5] | [0.97277, 0.97542] |

Box 7 contains μ_* ≈ 0.198932 (q_* ≈ 0.973056). There U₋(x_H) changes sign (item (b), O1–O3).

## 3. The method

**Construction (route R, the trust base).** It uses my own exact integer arithmetic: Python 3.12 integers, with no
python-flint and no sympy.

    Ñ_k(z, μ) = F(t, μ) − 64 Ĥ² [(1 − z) f̂_z P_k + f̂ (−P_k + (1 − z) ∂_zP_k + P_k²)],   t = (1 − z)³

- F is item (b)'s `Fp`, with U₋ = F/((μ + 1)³(μ + 6)) (Lean `param_U`).
- f̂ = (1 + μ)(6 + μ) − 2(6 + μ²)t + (1 − μ)(6 − μ)t² = (1 + μ)(6 + μ)·f.
- Ĥ = 6(1 + μ) + 4(6 − μ)t = (1 + μ)·H₋.
- So N_k = Ñ_k/Den with Den = (μ + 1)³(μ + 6) > 0. Ñ_k has degree (68, 12) in (z, μ).

**Cross-checks of the construction.** If one fails, the box is void (reported), not REJECT.
- **X1 (route L, exact).** sympy builds Nz from the Lean definitions: U6, H6, F6 and F6', with x_H = 2/(1 + w),
  q² = 1 − w² and δ = δ(μ). After cancelling, it must equal Ñ_k/Den as a rational function.
- **X2 (route P, exact fractions, 40 points per box).** The points (z, μ) are random rationals with denominators
  ≤ 1000 in [0, 1] × [a_k, b_k], from Python's `random.Random(20261022)`. N is computed from:
  - PREREG §1's factored f = (1 − t)(1 − κ³t), with κ³ = x_H/x₋ and x₋ the other root of 1 − x + q²x²/4;
  - f_z by the product rule;
  - TARGET.md's H₋ and U₋;
  - δ taken from q through TARGET.md's (1 + 12δ)² = 1 + 24q²/25 (an exact rational square root), and
    x_H = 2/(1 + √(1 − q²)).

  It must equal Ñ_k/Den at every point.
- **X3 (endpoints, exact in μ).**
  - Ñ_k(1, μ)/Den = 2304(12 − P_k(1, μ)² + P_k(1, μ)) (`N_at_infinity_D6`);
  - Ñ_k(0, μ)/Den = U₋(x_H) − 64H₋(x_H)² f_z(0) P_k(0, μ) (`N_at_horizon_D6`).

**Data checks.**
- **D1:** the file's sha256, as above.
- **D2:** boxes_mu[k].{mu, P} are identical in the record and in the reproduction (`runs/repro-*/T3/result.json`).
  This is reported; the record file is the one used.
- **D3:** the boxes are contiguous, cover the range, and respect the width limit.

**Positivity (the decision).** For each k, let g_k(z, s) = Ñ_k(z, a_k + (b_k − a_k)s) times a positive integer, with
integer coefficients, on the unit square. Its tensor Bernstein coefficients are computed exactly. Then adaptive
bisection:
1. If one of the four corner values is ≤ 0: **REJECT**, with that exact counterexample (z, μ, N).
2. If every Bernstein coefficient is > 0: a certified leaf.
3. Otherwise, bisect the variable with the larger width × degree in the local unit square (ties go to z).
4. The budget is depth ≤ 40 and at most 4096 leaves per box. Once it is exhausted: **UNDECIDED**.

A box is **VERIFIED** when every leaf is certified and D1, D3 and X1–X3 hold. **C-B is VERIFIED when all eight boxes
are.**

**Known-answer gates for the Bernstein code.** They must pass before the run of record.
- **KA1, KA2.** Item (b)'s F on [0, 7/8] × [1/6, 1] and on [7/8, 1] × [1/4, 1]. All 25 Bernstein coefficients must
  equal those of `B1` and `B2` in the item (b) Lean file. Those are kernel-checked through `B1_split`, `B2_split`,
  `box1` and `box2`, with minima 731962/9 and 179096.
- **KA3.** (z − 1/3)² + (s − 1/2)² − 1/100 on the unit square must give REJECT. Its corners are positive; it is
  negative near (1/3, 1/2).
- **KA4.** (z − 1/3)² + (s − 1/2)² + 1/100 must give VERIFIED.

**Freeze.**
- The code is developed and tested only on KA1–KA4 and on a synthetic random P of degree (28, 4), for X1–X3. It never
  touches T3's P_k during development.
- Its sha256 is written into the run folder before the run of record.
- The run of record is the first execution on T3's data. Any later run is labelled as such, and the first stands.

## 4. Planted false certificates (must fail)

**NP-A: the planted false P (interior, near miss).**
- P̃_k = P_k + c_k β(z), with β(z) = (27/4) z (1 − z)².
- β ≥ 0 and β(0) = β(1) = 0, so N is unchanged at z = 0 and at z = 1. β has its maximum β(1/3) = 1 with β′(1/3) = 0,
  so at z = 1/3:

      N_P̃ = N_P − 64H₋² [c((1 − z) f_z + f(2P − 1)) + f c²].

- c_k is fixed at run time, before the checker sees P̃_k. It is the smallest 2^j (j = −20, …, 10) with
  N_P̃(1/3, μ0_k) < 0 by exact evaluation, where μ0_k = a_k + (b_k − a_k)/3. So P̃_k is false, with an exact witness.
- **Must:** not VERIFIED on any box.
- **Predicted:** REJECT, with an exact counterexample, on all eight boxes. UNDECIDED would still be a failure of P̃_k,
  but a miss of this prediction.

**NP-B: the edge z = 1 (false a priori).**
- P̃_k = P_k + (5 − P_k(1, μ)) z²⁸, so P̃_k(1, μ) = 5.
- By `N_at_infinity_D6`, N(1, μ) = 2304(12 − 25 + 5) = −18432 for every μ.
- **Must:** REJECT on all eight boxes.
- **Predicted:** at depth 0, at the corner (1, a_k), with N = −18432.

**DR1: does NP-A discriminate?** A deliberately weakened checker accepts on the four corners alone.
- **Predicted:** it VERIFIES NP-A on every box where the real checker VERIFIES P_k.
- The reason: NP-A leaves z = 0 and z = 1 unchanged.

**DR2: are the cross-checks live?** F's constant term goes from 165888 to 165889 in route R.
- **Predicted:** X1 fails, and X2 fails at all 40 points of every box.
- The reason: the change adds 1/Den to N everywhere.

## 5. Independence

| | this re-run | the record (BHM-023) |
|---|---|---|
| agent | session-L (Claude Opus 5.5) | the bh-modes lead |
| construction of N | route R: item (b)'s reduced form, degree (68, 12), own integer arithmetic | sympy, degree (68, 16) |
| positivity | own Bernstein code in Python integers, with the bisection rule above | `code/onset/bernstein.py`, python-flint `fmpq` |
| shared | the certificate data P_k (by design); TARGET.md and METHOD.md; sympy 1.14.0, used here only in X1 | |

I am not blind to the outcome: I know the record's T3 verdict is VERIFIED. Whether this counts as CHARTER e5's second
party is the operator's ruling.

## 6. What I had seen before registering

**bh-modes files read.**
- `results/p3/{PREREG.md, PREREG_ADDENDUM_1.md, RESULT.md, METHOD.md}`, and CHARTER e5.
- The T1, T2 and T3 `result.json`: their structure, and the P and μ values. I read no `bernstein` field and no log.
- `TARGET.md`. For other items: `code/onset/onset.py` for (b), `code/a2/extremal.py` for (d), and
  `code/qnm1c/{identities,tail}.py` for (e).

**Not read:** `code/p3/scert.py`, `code/onset/bernstein.py`, `kit/p3/`, `results/p3/briefs/`, `diagnosis_G1.*`.

**Computed on T3's data so far.**
- `lean_list_2026-10-22/c_sizing`: degrees, term counts and coefficient sizes of N's numerator for boxes 0 and 7. No
  values and no signs.
- The convention check, on P values only. With the global μ, |P_T3,4(z, 1/6) − P_T1(z)| ≤ 5.1·10⁻⁹ on 21 points.
  Box-local readings give 0.34 (u ∈ [−1, 1]) and 110 (s ∈ [0, 1]).

## 7. Reading rule and delivery

The run of record will go into a new folder, `[deliveries]/p3_T3_rerun_<date>/`. It will cite this file's
sha256, and its result is reported as it stands.
- **Agreement means:** D1, D3, KA1–KA4 and X1–X3 hold; C-B is VERIFIED on all eight boxes; NP-A and NP-B fail as
  registered; DR1 and DR2 come out as predicted.
- **Any difference** is reported as it stands.
- **A REJECT of a real box** is a claim-changing finding. It goes to the lead directly, with its exact counterexample.
