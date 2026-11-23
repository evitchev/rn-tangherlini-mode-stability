# Lean layer, item (b): the exact onset for D = 6, ℓ = 2 (bh-modes): session-L, 2026-10-22

This answers §3 item (b) of the bh-modes lead's second message (`outbox/2026-10-22-to-session-L-2.md`): "the onset: the
minimal polynomials 10μ³ − 11μ² + 228μ − 45 and 3025Y³ − 31521Y² + 99792Y − 68796. The positivity of U₋ for q ≤ q_*
comes from three Bernstein boxes (`results/onset/`)". The claims are O1–O5 of `results/onset/PREREG.md` (BHM-016),
verified in `RESULT.md` (BHM-017).

| file | content |
|---|---|
| `lean/BHModesOnset.lean` | 54 theorems, namespace `BHModes.Onset` |
| `lean/build.sh`, `lean/BUILD_LOG.txt` | the audited build (A1 format): compile, axioms, two negative controls, ten mutations |
| `lean/SOURCES.tsv`, `lean/mutations.json`, `lean/vendor/` | the source hash, the specs, the vendored judge (byte copy) |
| `review/ONSET_MUTATION_REGISTRATION.md`, `review/REGISTRATION_TIME.txt` | predictions, written and hashed before the first run |
| `oracle/gen_onset.py` and `.out` | prints the file's section "Generated": F, Q, the cofactor K, the Bernstein forms |
| `oracle/check_onset.py` and `.out` | independent sympy checks, and a cross-check against the bh-modes record |
| `SHA256SUMS` | every file except itself |

## A finding for the lead: F reduces to degree (4, 4)

In the record, U₋(t·x_H) = F(t, μ)/Den(μ) with F of degree (4, 104) (`runs/record/main/result.json`, `F_degrees`).
Those factors cancel. With δ = (1 − μ²)/(5(6 + μ²)) and x_H = 2(6 + μ²)/((μ + 1)(μ + 6)):

    U₋ = F(t, μ)/((μ + 1)³(μ + 6)),   F of degree (4, 4) with 24 terms   (Lean: param_U)
    F(1, μ) = 1024 (μ + 15)(10μ³ − 11μ² + 228μ − 45)                   (Lean: g_factor)

`oracle/check_onset.py` confirms that the record's degree-104 g is exactly this g times a degree-100 polynomial with no
root in [0, 1].

So the O2 positivity needs only three single Bernstein boxes of a degree-(4, 4) polynomial, with simple endpoints:
- **Box 1:** F > 0 on [0, 7/8] × [1/6, 1]. The minimum Bernstein coefficient is 731962/9.
- **Box 2:** F > 0 on [7/8, 1] × [1/4, 1]. The minimum is 179096.
- **Box 3:** Q < 0 on [7/8, 1] × [1/6, 1/4], where F(t, μ) = F(1, μ) + (t − 1)Q(t, μ). This replaces the record's
  derivative sign test with an exact factorisation.

Since μ_* ≈ 0.1989 lies in (1/6, 1/4), these three facts and g ≥ 0 for μ ≥ μ_* give O2.

## What is proved

| PREREG claim | Lean theorem(s) | statement |
|---|---|---|
| O5 | `O5_s_sq`, `O5_s_pos`, `O5_delta_nonneg`, `w_strictMonoOn`, `w_zero`, `w_one`, `O5_sqrt`, `O5_xH`, `param_of_q`, `delta_of_q`, `param_U` | s² = 1 + 4mq²/25 with s > 0 and δ ≥ 0 on [0, 1]; w = √(1 − q²) is strictly increasing from 0 to 1, so every q ∈ [0, 1] is some q(μ); TARGET.md's δ is δ(μ); U₋ = F/Den |
| O1 | `g_factor`, `p_strictMono`, `p_root_exists`, `p_root_bounds`, `p_root_unique`, `C_relation`, `q2_root`, `C_root_unique`, `qstar_sq_bounds`, `qstar_bounds`, `p_irreducible`, `C_irreducible` | g = 1024(μ + 15)p; p has exactly one real root μ_*, in (0.19893240974, 0.19893240975); (6 + μ²)⁶C(q(μ)²) = p(μ)K(μ), so C(q_*²) = 0; C has exactly one real root; q_* ∈ (0.9730564367, 0.9730564368), the registered prediction; both cubics are irreducible over ℚ, so they are the minimal polynomials up to their leading coefficients |
| O2 | `O2` (in q), `O2_mu` (in t, μ) | for 0 ≤ q with q² ≤ q_*², TARGET.md's δ and 0 ≤ x ≤ x_H(q): U₋(x) ≥ 0. In (t, μ): F ≥ 0 on [0, 1] × [μ_*, 1], with equality only at (1, μ_*) |
| O3 | `O3`, `O3_mu` | for q ≤ 1 with q² > q_*²: U₋(x_H(q)) < 0 |
| O4 | `O4_bracket`, `O4_threshold`, `O4` | KI (6.24)'s bracket at the horizon is 4(4μ − 3)/(μ + 1): > 0 for q < 3/5, = 0 at q = 3/5, < 0 for q > 3/5 |

- `O2` and `O3` are stated in TARGET.md's own terms: q, δ with δ ≥ 0 and (1 + 2mδ)² = 1 + 4mq²/25, and
  x_H = 2/(1 + √(1 − q²)). The parametrisation is only a tool inside the proofs.
- μ_* enters as "any root of p". Since `p_root_unique` holds, that is the root.
- **Not proved here:** E0 (it is in the A1 and extremal layers), and the record's Arb root isolation and its 45-digit
  interval. Here the interval is 10⁻¹¹ wide, enough for the registered prediction.

## Checks

- **Oracle.** `oracle/check_onset.py RECORD_JSON` passes all 15 checks:
  - TARGET.md's U₋ equals F/Den at 20 rational points;
  - the factorisation, irreducibility and root counts (sympy);
  - the record's minimal-polynomial strings, μ_* interval, q_* decimal and degree-104 g (cofactor without roots in
    [0, 1]);
  - the O4 bracket;
  - a sanity grid.
  - One bug in my oracle was fixed before the run of record: a Python float at μ = 1. Debugging showed agreement at a
    rational test point.
- **Build.** `lean/BUILD_LOG.txt`: "BHModesOnset: ALL CHECKS AS REQUIRED".
  - Compile: exit 0, 0 errors, 0 warnings, 0 sorry, 52 s.
  - `#print axioms`: 54/54 theorems use only propext, Classical.choice and Quot.sound.
  - Both checker negative controls are rejected.
  - The judge passes all ten mutations.
- **The registration against the run: 9 of 10 agree in full, and one prediction of mine was wrong.**
  - `review/ONSET_MUTATION_REGISTRATION.md` (sha256 `905cdc96…`) was logged at 19:21:43Z and again by the build at
    19:22:55Z, before the first run.
  - For ONM1–ONM8 and ONM10, the first failure, the exact failing set and the registered error texts all agree.
  - **ONM9** (F's constant term 165888 → 165889): the first failure (`param_U`) is as predicted. The failing set is
    {`param_U`, `g_factor`, `box1`, `box2`}, without the `F_split` I predicted. A change in F's t-independent part
    cancels in F(t, μ) − F(1, μ), so `F_split` is not sensitive to it. The judge's `pass` is still true, because it
    checks only membership. The miss is in my prediction, not in the file, and under the reading rule it stands as
    recorded.

**Files.** `SHA256SUMS` covers every file except itself. The build outputs are kept outside the folder;
`lean/build.sh` regenerates them.
