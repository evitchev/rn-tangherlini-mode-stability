# PREREG — A1 for ℓ ≥ 3 (P1), and the assembly of Theorem A1

*Item BHM-047. 2026-10-23, the bh-modes lead. Stage 2, step 1 of the operator's order (BHM-027),
started on the operator's instruction of 2026-10-23; time box about three days, with a report
at its end (BHM-046). This is A1's own PREREG (`TARGET.md` §5, `FEASIBILITY.md` §1 P1). Sealed;
any change before the run is a dated addendum.*

## 1. Setting

- `TARGET.md` §1 owns the formulas: D = 6; m = (ℓ − 1)(ℓ + 4); δ ≥ 0 with (1 + 2mδ)² = 1 + 4mq²/25;
  H₋ and U₋ of S5 (5.62b), (5.63b) at n = 4; V_{ℓ,q} = fU₋/(64r²H₋²); x = 2M/r³ ∈ [0, x_H(q)] with
  x_H = 2/(1 + √(1 − q²)). `TARGET_ADDENDUM_1.md` fixes q_max = 99/100.
- On the exterior f > 0 and H₋ = m + 10x + 10mδx ≥ m > 0, so V has the sign of U₋.

## 2. Claims

- **P1.** For every integer ℓ ≥ 3, every q ∈ [0, 99/100] and every x ∈ [0, x_H(q)]: **U₋ > 0**.
  Hence V_{ℓ,q} > 0 on the exterior, the form ∫(|φ′|² + V|φ|²) is ≥ 0 on C₀^∞(ℝ), and
  A_{ℓ,q} ≥ 0.
- **Lemma U (part of P1, stated with its full range).** For every ℓ ≥ 11, every q ∈ [0, 1] and
  every x ∈ [0, 2]: U₋ ≥ m³·(64 − Neg(1/12, 1/5, 2)) > 0, with Neg as in §3. The range q ≤ 1 is
  more than A1 needs; it is recorded as an input for A2's R4 (`TARGET_A2.md` §4).
- **Theorem A1, assembled when P1 is VERIFIED.** For every ℓ ≥ 2 and every q ∈ (0, 99/100],
  A_{ℓ,q} ≥ 0:
  - ℓ = 2 and q ≤ q_*: V ≥ 0 (BHM-017, O2);
  - ℓ = 2 and q ∈ [0.97277, 0.99020] ⊇ (q_*, 99/100]: the eight S-certificates T3 (BHM-023),
    through `results/p3/METHOD.md` Proposition 3;
  - ℓ ≥ 3: P1.

## 3. Method (`code/a1/p1.py`)

**Part I, ℓ = 3, …, ℓ₀ with ℓ₀ = 10.**
- The rational parametrisation of the charge from `results/onset/PREREG.md` §1:
  - A = (ℓ + 4) + (ℓ − 1)μ²;
  - w = √(1 − q²) = (2ℓ + 3)μ/A;
  - s = 1 + 2mδ = (2ℓ + 3)((ℓ + 4) − (ℓ − 1)μ²)/(5A).
- Per ℓ, the code checks exactly that:
  - s² = 1 + 4mq²/25, q(1) = 0, q(0) = 1 and δ(1) = 0;
  - w increases on [0, 1] (Bernstein, numerator and denominator of w′).
- **The μ-box.** μ_lo(ℓ) = k/1000, with k the largest integer such that w(k/1000)² ≤ 1 − (99/100)².
  The code checks exactly that q(μ_lo)² ≥ (99/100)². Since w increases, [μ_lo, 1] then covers
  q ∈ [0, 99/100].
- **Positivity.**
  - With x = t·x_H, U₋ = F(t, μ)/Den(μ) in lowest terms (sympy `cancel`), and F/Den = U₋ is
    checked exactly.
  - Den > 0 on [μ_lo, 1], and F > 0 on [0, 1] × [μ_lo, 1], closed, are proved by exact Bernstein
    bisection (`onset.bernstein.prove_sign`, depth ≤ 40).
- **Recorded bound per ℓ.** The least Bernstein coefficient of F over the accepted leaves, divided
  by the largest Bernstein coefficient of Den on [μ_lo, 1], is a certified lower bound for U₋ on
  the region.

**Part II, ℓ ≥ ℓ₀ + 1 = 11 (the uniform lemma).**
- Put ε = m^{−1/2} and κ = m^{1/2}δ. Then P(ε, κ, x) := ε⁶U₋(x; m = ε⁻², δ = κε) is a polynomial.
  The code builds it, and splits it as P = Pos − Neg, where Pos and Neg have nonnegative
  coefficients and Pos has constant term 64.
- **Pencil steps** (proved here, audited 0×):
  - (a) Dividing (5.58) by 4m gives mδ² + δ = q²/25, so κ² = q²/25 − δ ≤ q²/25 and 0 ≤ κ ≤ 1/5
    for q ≤ 1. The code checks the polynomial identity.
  - (b) 0 ≤ x ≤ x_H = 2/(1 + √(1 − q²)) ≤ 2.
  - (c) m = (ℓ − 1)(ℓ + 4) increases with ℓ, so ℓ ≥ 11 gives m ≥ m₀ = 150 and
    0 < ε ≤ ε̄ = 1/isqrt(150) = 1/12. The code checks m₀ε̄² ≥ 1.
  - (d) On [0, ε̄] × [0, 1/5] × [0, 2] a polynomial with nonnegative coefficients is nondecreasing
    in each variable. So Pos ≥ Pos(0, 0, 0) = 64 and Neg ≤ Neg(ε̄, 1/5, 2), which gives
    U₋ = m³P ≥ m³(64 − Neg(1/12, 1/5, 2)).
- **The check.** 64 − Neg(1/12, 1/5, 2) > 0, in exact rationals.

**Implementation parameters** (they cannot turn a false claim true): ℓ₀ = 10, the 1/1000 grid
for μ_lo, the bisection depth. A wrong choice can only make a true claim fail.

## 4. Gates, controls and tamper drills

**Why not TARGET.md §5's G1 and G2.**
- G1 (Q = 0, a negative region) and G2 (charged D = 5) were registered for the certificates of
  the non-elementary band. That band is ℓ = 2's S-certificates and the ODE route, and BHM-023/025
  carry them (G1 passed at D = 10 with rule 2).
- P1 proves positivity of U₋ itself. Its informative known answer is a certified negative region,
  ℓ = 2 above q_* (BHM-017, O3). That is NC-A1a below.
- §5's planted bound state becomes a planted negative region of U₋ (NC-A1b).
- §5's corrupted coefficient is TD-A1a. §5's Frobenius tamper does not apply, since P1 has no
  Frobenius bound; TD-A1b and TD-A1c replace it.

| Name | Control (`--control`) | Must | Predicted |
|---|---|---|---|
| KAT1–KAT5 | in every run | as stated | the verifier rejects −1, (t−½)² + (μ−½)² − 1/100, and t(1−t) + μ (a zero at a corner); it accepts (t−½)² + (μ−½)² + 1/100; `Q` refuses floats |
| E0, H | in every run | hold | S5's (5.63b), (5.62b) at n = 4 equal `TARGET.md`'s U₋, H₋; H₋'s coefficients are > 0 |
| NC-A1a | `nc-ell2`: Part I for ℓ = 2 on q ∈ [0, 99/100] | REJECT | an exact counterexample at the corner (t, μ) = (1, μ_lo(2)), since q(μ_lo(2)) ≥ 0.99 > q_* |
| NC-A1b | `nc-bump`: ℓ = 3 with U₋ − 10⁷·64t³(1 − t)³ | REJECT | an exact counterexample at t = 1/2, found by bisection; the corners are unchanged |
| NC-A1c | `nc-coverage`: μ_lo chosen for q = 98/100 | REJECT | the coverage check for 99/100 fails |
| NC-A1d | `nc-uniform`: Part II with ℓ₀ = 1 (m₀ = 6, ε̄ = 1/2) | REJECT | 64 − Neg(1/2, 1/5, 2) < 0 |
| TD-A1a | `td-coeff`: 7680 → 7681 in U₋ | REJECT | E0 fails |
| TD-A1b | `td-split`: the x⁴ monomials dropped from Neg | REJECT | P ≠ Pos − Neg |
| TD-A1c | `td-verifier`: the verifier accepts when its least Bernstein coefficient is > −1 | REJECT | KAT2 and KAT3 come out accepted |

## 5. Pass criterion, and what follows

- **VERIFIED** requires all of:
  - the KATs, E0 and H;
  - for each ℓ = 3, …, 10: the parametrisation identities, w increasing, the coverage of
    q ≤ 99/100, F/Den = U₋, Den > 0 and F > 0;
  - Part II's six checks.
- **Record and reproduction.** The record runs on host-1 and the reproduction on host-2, both from a
  `git archive` of this commit (`kit/a1/run.sh`), and they must be identical after masking
  (`code/compare_runs.py`). The kit passes only if every control and drill rejects.
- **Status on VERIFIED:**
  - P1 and Lemma U: *certified* (exact); the pencil steps (a)–(d): proved (pencil; audited 0×);
  - Theorem A1: *certified*, resting on BHM-017, BHM-023 and P1, with the reduction of
    `results/p3/METHOD.md` proved (pencil; audited 2×; Lean, BHM-030);
  - an independent re-run of P1 is pending: a sealed Kimi brief whose runs of record go to
    host-1/005 (BHM-046).
- **On a REJECT of the main run:** reported as it stands, with the largest certified range
  (`FEASIBILITY.md` §6). Any new attempt needs a new registration.

## 6. What ran before this registration

- **Development, on host-1** (`[venv]`, `nice -n 19`), from a `git archive` of commit
  `f32db2c`:
  - syntax checks of `code/a1/p1.py`, `code/a1/devtest.py`, `code/cn/identity.py` and
    `code/onset/bernstein.py`;
  - `python -m a1.devtest`, synthetic inputs only:
    - the KATs, with the real verifier (all pass) and with the tampered one (KAT2 and KAT3 fail);
    - Part I's code path for ℓ = 3 on U = 64m³ + 384m² + x²;
    - Part II's code path on U = 64m³ + 384m² − 7680mx.
- **Not run:** nothing of U₋ was evaluated for any ℓ, and no control or drill was run.
- **`code/onset/bernstein.py` changed** in `f32db2c`:
  - `Q` refuses floats (Fable's audit, BHM-042);
  - `prove_sign` takes an optional `minrec` that records the least accepted Bernstein
    coefficient.

  The verdict logic is unchanged. The onset and p3 records are re-run at their own commits, so
  they are unaffected.

## 7. Artifacts

`code/a1/p1.py`, `kit/a1/run.sh`, `code/onset/bernstein.py`, `code/onset/onset.py` (`param`),
`code/ki/potentials.py`, at the commit that holds this file.
