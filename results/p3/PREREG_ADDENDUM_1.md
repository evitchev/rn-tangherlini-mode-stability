# p3 PREREG addendum 1 — a design rule with slack everywhere

*Item BHM-024. 2026-10-22, the bh-modes lead. Registered **after** the run of record (BHM-023)
and **before** any re-run.*
- **Why.** The run of record failed the registered must-pass gate G1.
- **The failure stands** (BHM-023).
- **What this does.** It registers a second design rule and the re-runs it must pass.
- **Why a design change is admissible.** The verification, which is the trust base, is
  unchanged, so a design change cannot turn a false claim true (RULES.md A1). Sealed.

## Diagnosis (post-hoc, numerical; `results/p3/diagnosis_G1.{py,log}`)

- **The defect.** METHOD.md's remark gives, for the registered design P = P_true − ε:
  ρ²(Ṽ/f) = ε[ρf′ + f(2P_true − 1 − ε)].
- **Where it fails.** For G1 (D = 10, ℓ = 2, Q = 0), where ψ₁ falls through the deep negative
  region of V, that bracket has minimum −1.288 at z ≈ 0.29 (P_true ≈ −0.56). For T1 its
  minimum is +0.992.
- **Consequence.** The registered design direction cannot work in deep ditches, however
  accurate the fit. T1, T2 and T3 (D = 6, a shallow ditch) are not affected.

## Design rule 2

> P = P_true − ε₁(ρ − 1)/(f ψ₁²) − ε₂ z^6,  ε₁ = ε₂ = 1/50,

fitted exactly as before (Chebyshev–Lobatto in z of degree 28; in μ of degree 4 for boxes).
log ψ₁ is integrated with the Riccati equation, d log ψ₁/dτ = zP.

**Why it has slack everywhere** (pencil, the same identity as METHOD.md's remark). Write
β = P/ρ = β_true − η, with η = η₁ + η₂, η₁ = ε₁z/(fψ₁²) and η₂ = ε₂z⁶/ρ. Then
ρ²Ṽ/f = ρ²[(fψ₁²η)′/ψ₁² − fη²], and:
- **The η₁ term contributes exactly ε₁/ψ₁²**, which is > 0 everywhere, the horizon included
  (ψ₁(r_H) = 1).
- **The η₂ term contributes** ε₂z⁵[z(ρf′ + f(2P_true − 1)) + 6f(1 − z)]. This tends to
  ε₂(2P_true(1) − 1) > 0 at infinity, where η₁'s contribution decays like 1/ψ₁².
- **The quadratic terms** are O(ε²).

## Re-runs and criteria

| Name | What | Expected |
|---|---|---|
| G1 (rule 2) | D = 10, ℓ = 2, Q = 0 | **VERIFIED (must pass)** |
| T1 (rule 2) | μ = 1/6 | **VERIFIED (must pass)** |
| TD-P2 (rule 2) | P(0) raised by 1/10 above the horizon bound | **REJECT (must)** |
| T2 (rule 2) | the T2 box | reported either way |

- **Nodes.** Record on host-1, reproduction on host-2 (`kit/p3/run_rule2.sh`).
- **The A1 certificate.** Rule 2 becomes the design rule A1's own PREREG will use, unless that
  PREREG says otherwise. The T1, T2 and T3 certificates of BHM-023 stand as verified; a
  certificate's validity does not depend on how P was designed.
