# PREREG — exact onset of the negative region of V_S− for D = 6, ℓ = 2

*Item BHM-016. 2026-10-22, the bh-modes lead. Operator's ruling (`CHARTER.md` changelog,
fourth entry): q_max is fixed by a sealed addendum to `TARGET.md` **after the onset near
q ≈ 0.973 is certified exactly**. This file registers that certificate before it runs. It is
also FEASIBILITY P2 (the elementary band of ℓ = 2) and the CHARTER e4 content of A1. Sealed;
changes before the run are dated addenda.*

## 1. Setting

- `TARGET.md` §1 owns the formulas: D = 6, ℓ = 2, m = 6, V_S− = fU₋/(64r²H₋²), x = 2M/r³,
  x_H = 2/(1 + √(1 − q²)), q = |Q|/M ∈ [0, 1].
- The sign of V_S− on the exterior is the sign of U₋(x; q), x ∈ (0, x_H(q)).
- The onset is q_* := inf{q : U₋(·; q) has a zero in (0, x_H(q))} (`TARGET.md` §4).

**Rational parametrisation** (exact; no square roots).
- For μ ∈ [0, 1], put A = (ℓ + 4) + (ℓ − 1)μ². Then:
  - w := √(1 − q²) = (2ℓ + 3)μ/A;
  - s := 1 + 2mδ = (2ℓ + 3)((ℓ + 4) − (ℓ − 1)μ²)/(5A).
- So s² = 1 + 4mq²/25 identically, and q is a monotone bijection: μ = 1 gives q = 0, μ = 0
  gives q = 1.
- With x = t·x_H and t ∈ [0, 1], U₋ = F(t, μ)/Den(μ), where F has integer coefficients and
  Den > 0 on [0, 1].
- g(μ) := F(1, μ) is U₋ at the horizon, up to the positive factor.

## 2. Claims (all exact)

- **O1 (the onset is algebraic).**
  - g has exactly one root μ_* in [0, 1]; it is simple; g(0) < 0 < g(1).
  - Hence q_* = q(μ_*). Prediction (BHM-014, numerical): **q_* ∈ [0.9730564367, 0.9730564368]**.
  - The certificate prints:
    - an isolating interval of width ≤ 10⁻⁴⁵ for μ_* and the induced intervals for q_*² and q_*;
    - the irreducible factor of g that vanishes at μ_*;
    - the minimal polynomial of q_*² (a resultant).
  - An independent Arb root isolation of that factor must agree.
- **O2 (positivity at and below the onset).** For every q ∈ [0, q_*] and x ∈ [0, x_H(q)],
  U₋(x; q) ≥ 0, with equality only at (q, x) = (q_*, x_H(q_*)). So V_S− ≥ 0 on the exterior
  for q ≤ q_*, and > 0 for q < q_*.
- **O3 (negativity above the onset).** For every q ∈ (q_*, 1], U₋(x_H(q); q) < 0. So V_S− < 0
  next to the horizon, and U₋ has a zero in (0, x_H). With O2 this proves q_* is the onset,
  with mechanism "horizon".
- **O4 (range of S5's (6.24) for ℓ = 2).** The bracket at the horizon,
  b = 2m − 10(1 + mδ)x_H, is > 0 for q < 3/5, = 0 at q = 3/5 (μ = 3/4) and < 0 for q > 3/5.
- **O5 (the setting).**
  - S5 (5.63b) at n = 4 equals `TARGET.md`'s U₋ (as E0, BHM-010).
  - The parametrisation identities above hold.
  - Den > 0 on [0, 1], and w is increasing in μ.

**Consequence, once O1–O4 hold** (CHARTER e4): for D = 6, ℓ = 2 the set where neither V ≥ 0
nor S5's (6.24) applies is exactly (q_*, 1]. This is relative to the sources in
`results/screen/PREREG.md` §1.5, and is not a completeness claim. So A1 with q_max = 0.99
contains the non-elementary band (q_*, 0.99].

## 3. Method

- **Arithmetic.** sympy 1.14.0 builds F and g exactly. python-flint 0.9.0 `fmpq` gives the
  Bernstein enclosures on boxes in (t, μ), with adaptive bisection (`code/onset/bernstein.py`).
- **Roots of g.**
  - Sturm root count and exact isolation (`count_roots`, `intervals`).
  - Exact sign evaluations at rational points.
  - Arb root isolation (`fmpz_poly.complex_roots`) as an independent check.
- **O2.** Three regions in (t, μ):
  - F > 0 on [0, 1 − τ] × [μ_lo, 1];
  - F > 0 on [1 − τ, 1] × [μ_c, 1];
  - **corner lemma** ∂F/∂t < 0 on [1 − τ, 1] × [μ_lo, μ_c].

  Here μ_lo is the lower end of μ_*'s interval and μ_c > μ_hi. With O1 this gives
  F(t, μ) > F(1, μ) = g(μ) ≥ 0 in the corner. τ and μ_c are implementation parameters: each
  attempt that succeeds is a proof.
- **Fail-closed.** VERIFIED (exit 0) only if every check holds; anything else is REJECT.
- **Nodes.** Record on host-1, reproduction on host-2, same code (`kit/onset/run.sh`).

## 4. Controls and drills (same session)

| Name | What | Expected |
|---|---|---|
| NC-O1 | False claim: the onset lies in μ ∈ [0.20, 0.21], i.e. q ∈ [0.96997, 0.97277] | REJECT (O1) |
| NC-O2 | False claim: U₋ ≥ 0 on the exterior up to q ≈ 0.975 (μ ≥ 191/1000) | REJECT, with an exact rational counterexample |
| PC-O1 | Positive control: ℓ = 3, U₋ > 0 on the exterior for q ≤ q(μ = 1/30) ≈ 0.99908 | VERIFIED |
| TD-O1 | Tamper: U₋'s coefficient 7680 → 7681 | REJECT (E0) |
| TD-O2 | Tamper: the corner lemma's sign test inverted | REJECT |

**Pass criterion.** Main run VERIFIED with q_* inside the prediction; the five controls and
drills as expected. Then a sealed `TARGET_ADDENDUM_1.md` fixes q_max = 99/100 and records q_*
exactly (`TARGET.md` §4; operator's ruling).
