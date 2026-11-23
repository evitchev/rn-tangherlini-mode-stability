# PREREG — prototype certificate for target A1, ℓ = 2 (S-deformation, exact positivity)

*Item BHM-022. 2026-10-22, the bh-modes lead. The operator's next-work list (`CHARTER.md`
changelog, fourth entry; TODO) includes "a first prototype certificate for ℓ = 2 under its own
registration". This file registers it before any design computation or run. Sealed; changes
before the run are dated addenda.*

## 1. Method (replaces `FEASIBILITY.md` draft 1, P3's Frobenius + Taylor-model plan)

**The reduction** (`results/p3/METHOD.md`, *proved (pencil; audited 0×)*).

- **The identity.** For any S ∈ C¹(ℝ) and φ ∈ C₀^∞(ℝ):
  ∫(|φ′|² + V|φ|²) dr* = ∫|φ′ + Sφ|² dr* + ∫Ṽ|φ|² dr*, where Ṽ = V + dS/dr* − S².
  So Ṽ ≥ 0 implies A_{ℓ,q} ≥ 0. No boundary condition is needed.
- **The ansatz.** Units r_H = 1, ρ = r/r_H, z = 1 − 1/ρ ∈ [0, 1), and S = −f(ρ)(1 − z)P(z) with
  P a polynomial. Then Ṽ = f·N/(64ρ²H₋²), where
  N := U₋ − 64H₋²[(1 − z)f_z P + f(−P + (1 − z)P_z + P²)].
  Here x = x_H(1 − z)³ and f = (1 − (1 − z)³)(1 − κ³(1 − z)³), with κ³ = x_H/x₋.
- **The certificate.** N is a polynomial in z and finite at z = 1 (spatial infinity). So
  **N ≥ 0 on [0, 1] ⇒ A_{ℓ,q} ≥ 0**, a single exact positivity check with no tail lemma.
- **Parameter boxes.** q enters through the rational parametrisation μ of BHM-016. On a
  μ-box, P = P(z, μ) and N is a polynomial in (z, μ), up to a positive factor Den(μ).

**Design (untrusted).** P is chosen numerically and is not part of the trust base:
- the Riccati equation (1 − z)P_z = P − P² + [U₋/(64H₋²) − (1 − z)f_z P]/f is integrated in
  τ = log(z/(1 − z)) in double precision;
- P is set to the regular solution minus ε = 1/50, interpolated at Chebyshev–Lobatto nodes in
  z (and in μ for boxes), with coefficients rounded to rationals.

**Verification (the trust base).**
- N is built exactly (sympy 1.14.0) from `TARGET.md`'s U₋ and H₋, with E0 against S5 (5.63b).
- N > 0 is proved by exact Bernstein enclosures (`code/onset/bernstein.py`, python-flint
  `fmpq`), with Den > 0 checked the same way.
- Fail-closed: VERIFIED only if every check holds.

## 2. Claims and tiers (D = 6, ℓ = 2 unless stated)

| Tier | Claim | Registered status |
|---|---|---|
| **T1** | A_{2,q} ≥ 0 at μ = 1/6, i.e. q = √(45325/47089) ≈ 0.981091 (inside (q_*, 0.99]) | **must pass** |
| T2 | A_{2,q} ≥ 0 for μ ∈ [1/6 − 1/200, 1/6 + 1/200], i.e. q ∈ [≈0.97994, ≈0.98221] | reported either way |
| T3 | A_{2,q} ≥ 0 for μ ∈ [3/25, 1/5], i.e. q ∈ [0.97277, 0.99020], covered by μ-boxes of width ≤ 1/100 | stretch; reported either way |
| **G1** | Known answer (S6, proved): A ≥ 0 for D = 10, ℓ = 2, Q = 0, where V has a negative region (BHM-014, K1). The same construction (x = (1 − z)⁷, f = 1 − x) must verify | **must pass** |

If T3 passes, then with BHM-017 (O2: V ≥ 0 for q ≤ q_*) the ℓ = 2 part of A1 (q ∈ (0, 0.99])
is certified. A1's own PREREG will then register P1 (ℓ ≥ 3) and cite T3. This prototype makes
no claim for ℓ ≥ 3.

## 3. Controls and drills (same session)

| Name | What | Expected |
|---|---|---|
| **NC-P1** (`TARGET.md` §5's planted bound state) | V → V + W, W = −K_p f b/ρ² with b = (z − 3/10)²(3/5 − z)² on [3/10, 3/5], else 0; K_p chosen so that a trial function certifies a bound state | (a) an explicit trial φ₀ = b on the same support gives Q[φ₀] < 0, by Arb's rigorous integration; (b) the T1 certificate (the same P) checked against V + W must REJECT |
| **TD-P1** | U₋'s coefficient 7680 → 7681 | REJECT (E0) |
| **TD-P2** | P(0) raised by 1/10 above the horizon bound P(0) < U₋(x_H)/(64H₋²f_z(0)) | REJECT, with an exact counterexample at z = 0 |

## 4. Pass criterion and what is recorded

- **Pass.** T1 and G1 VERIFIED; NC-P1 (a) certified and (b) REJECT; TD-P1 and TD-P2 REJECT.
- **Reported either way.** T2 and T3.
- **Recorded.** P's rational coefficients, which are the certificate, so anyone can re-verify
  without the design step. Also the degrees, the Bernstein box counts, and the wall time of
  design and of verification separately. The prototype's purpose includes the compute
  estimate (`FEASIBILITY.md` §3).
- **Nodes.** Record on host-1, reproduction on host-2 (`kit/p3/run.sh`).
