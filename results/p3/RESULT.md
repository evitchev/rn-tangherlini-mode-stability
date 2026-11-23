# ℓ = 2 prototype certificate: run of record (BHM-023)

*2026-10-22, the bh-modes lead. Registration: `results/p3/PREREG.md` and `METHOD.md` (BHM-022,
commit `782fc56`, sealed before any design computation). Run at `782fc56` with
`kit/p3/run.sh`: record on host-1, reproduction on host-2. Every JSON is identical across the
nodes after masking timings.*

## Verdict as registered: FAIL (the must-pass gate G1 failed)

| Tier or control | Registered | Outcome |
|---|---|---|
| **T1** (μ = 1/6, q ≈ 0.981091) | must pass | **VERIFIED.** N has degree 68 in z; 3 Bernstein boxes; design 0.39 s, verification 0.21 s |
| **G1** (D = 10, ℓ = 2, Q = 0) | must pass | **REJECT.** Exact counterexample N(1/4) < 0 |
| **NC-P1** (planted bound state) | must pass | **As registered.** (a) For K_p = 149694 a trial function certifies a bound state: Q[φ₀] = −9.934316448·10⁻⁷ ± 5.6·10⁻¹⁸ (Arb rigorous integration). (b) The T1 certificate is rejected on V + W, with an exact counterexample on the bump |
| TD-P1 (coefficient 7680 → 7681) | must reject | REJECT (E0) |
| TD-P2 (P(0) raised by 1/10) | must reject | REJECT, with an exact counterexample at z = 0 |
| T2 (μ ∈ [97/600, 103/600], q ∈ [0.97994, 0.98221]) | either way | **VERIFIED.** Degree (68, 16); 3 boxes; 4.8 s |
| **T3** (μ ∈ [3/25, 1/5], q ∈ [0.97277, 0.99020]) | stretch | **VERIFIED.** 8 μ-boxes, each of degree (68, 16) with 3 Bernstein boxes; 33 s in all |

## What is certified, and what failed

- **Certified** (exact; the verification is the trust base): A_{2,q} ≥ 0 at T1, on T2, and on
  **all of T3, q ∈ [0.97277, 0.99020]**.
  - Since q_* = 0.973056… > 0.97277 (BHM-017), T3 covers the whole non-elementary band
    (q_*, 0.99]. With BHM-017's O2 (V ≥ 0 for q ≤ q_*), **the ℓ = 2 part of Theorem A1
    (0 < q ≤ 99/100) is certified.**
  - Labels: **certified** (exact). The reduction (`METHOD.md`) is proved (pencil; audited 0×).
    Independent re-run by a second party pending.
  - A1 as a whole still needs ℓ ≥ 3 (FEASIBILITY P1) under A1's own PREREG.
- **G1 failed: the method's known-answer gate.**
  - A REJECT cannot be a false VERIFIED, so this is a completeness failure of the design, not
    a soundness issue.
  - Diagnosis (post-hoc, `diagnosis_G1.{py,log}`, numerical): for the registered design
    P = P_true − ε, METHOD.md's identity gives ρ²Ṽ/f = ε[ρf′ + f(2P_true − 1 − ε)]. For G1 that
    bracket reaches −1.288 at z ≈ 0.29, where ψ₁ falls through the deep negative region of V.
    For T1 its minimum is +0.992.
  - So the registered design direction cannot work in deep ditches. The D = 6 band has a
    shallow ditch, where it does work.
  - A second design rule with slack everywhere is registered in `PREREG_ADDENDUM_1.md`
    (BHM-024), before any re-run. This failure stays on the record.
- **Compute.** About 4 s per μ-box of width 1/100 at degree (68, 16), all exact. This is far
  below `FEASIBILITY.md` §3's estimate for the Frobenius + Taylor-model plan, which this
  method replaces.

## Files

Record, host-1: `runs/record/<tier>/result.json`; the reproduction is in `runs/repro-host-2/`.

| Tier | result.json SHA-256 (16 hex) |
|---|---|
| T1 | `5dbc4bc559be8522` |
| G1 | `818b82898ed895bc` |
| NC-P1 | `279176ea8c45054f` |
| TD-P1 | `9cf032b35e978097` |
| TD-P2 | `dfdebe5ba591bd8e` |
| T2 | `cbaa31267fe3557b` |
| T3 (contains the eight certificates P(z, μ)) | `f893d820aa0f289f` |

- **Code at `782fc56`:** `code/p3/scert.py` `377185b401663186`, `code/onset/bernstein.py`
  `1a67f19164b68a51`, `kit/p3/run.sh` `f626473049409076`.
- **Diagnosis:** `diagnosis_G1.py` `440bcfcd3d94c6e2`, `diagnosis_G1.log` `c9f2c07b0dba2431`.
- **A development run** of T1 alone preceded the kit run on host-1, at the same commit,
  outcome VERIFIED. It is not a record.
