# PREREG — HD-PILOT: the design pilot that fixes q_max(D) (stage 2, step 2)

*Item BHM-069. 2026-10-23, the bh-modes lead. Part HD-PILOT of `TARGET_HD.md` (BHM-061), under its §4.
Advice: the session-R lead's reading (BHM-058, §§2–3). Sealed; any change before the run is a
dated addendum.*

## 1. What the pilot is, and what it is not

- **It is untrusted.** It runs in double precision and makes no claim.
- **Its one output is q_max(D)** for D = 7…11, by `TARGET_HD.md` §4's stopping rule, together with the
  design that HD-S will register for each band.
- **It cannot certify anything.** A band that qualifies here can still fail HD-S's exact verification;
  that would be reported as it stands. A rung that does not qualify is not attempted.

## 2. Bands, rungs and samples

- **The 18 bands** of `TARGET_HD.md` §3, each with a lower end q_lo:
  - the 13 with an onset start at HD-E's q_split (BHM-062 §2, certified in BHM-063), so q_lo = q_split;
  - the 5 from 0⁺ (D = 8–11 ℓ = 2, D = 11 ℓ = 3) have q_lo = 0.
- **The rungs** are q_r ∈ {9/10, 97/100, 99/100}. A band is *active* at q_r if q_r > q_lo.
- **The samples.** At each active (band, rung), 9 charges: the Chebyshev–Lobatto points in μ on
  [μ(q_r), μ(q_lo)], with `TARGET_HD.md` §1's parametrisation (μ(0) = 1). They include both ends.

## 3. The design: rule 2 (BHM-024) at general n

- **The setting.** Units r_H = 1 and z = 1 − 1/ρ. Then:
  - x = x_H(1 − z)^{n−1} and f = (1 − (1 − z)^{n−1})(1 − k(1 − z)^{n−1}), with k = x_H/x₋ = (1 − w)/(1 + w);
  - W = U₋/(64H₋²), with `ki.potentials`' U₋ and H₋ at general n (checked against Kimi's transcription
    for n = 2…12 in HD-E's gate E0n).
- **P_true** is the regular solution at the horizon of
  (1 − z)P_z = P − P² + [W − (1 − z)f_zP]/f, with P(0) = W(0)/f_z(0).
  - It is integrated in τ = log(z/(1 − z)) from τ = −27 by RK4 with step 1/500, as in `code/p3/scert.py`.
  - log ψ₁ comes from d log ψ₁/dτ = zP, with ψ₁(r_H) = 1.
  - If |P| exceeds 10¹², or a value is not finite, the integration has broken down (ψ₁ has a zero), and
    the sample fails.
- **The design target:** P_d = P_true − ε(ρ − 1)/(fψ₁²) − εz⁶.
  - ε = 1/50 as in BHM-024.
  - **The fallback** is ε = 1/200, used only for a (band, rung) at which ε = 1/50 qualifies in no
    variable at no degree.
- **The two variables** (`TARGET_HD.md` §4.2). P_d is interpolated at the Chebyshev–Lobatto nodes:
  - in z ∈ [0, 1];
  - or in ζ = z/(z + δ_t) ∈ [0, 1/(1 + δ_t)], where δ_t = 1 − x_H/x₋ = 2w/(1 + w) is the throat width
    (BHM-058 §3).
- **The degrees** are d ∈ {16, 20, 24, 28, 32, 40, 48}. **The cap is 48.**
  - For HD-S, N's degree in z is then at most 4(n − 1) + 2d ≤ 128, in either variable.
  - For a ζ-design, (z + δ_t)^{2d}N is a polynomial in z of that degree.
- **The coefficients** are the double-precision Chebyshev coefficients, as in p3; HD-S uses their exact
  binary values.

## 4. The measurement

- **The bracket.** B = N/(64H₋²) = W − [(1 − z)f_zP + f(−P + (1 − z)P_z + P²)], so N ≥ 0 ⇔ B ≥ 0
  (`results/p3/METHOD.md`, Lemma 2: ρ²Ṽ/f = B).
- **The grid** has 6601 distinct points: z = 0 and z = 1; τ ∈ [−14, 14] in steps of 1/200; and
  z = k/1000 for k = 1…999 (the last two share z = 1/2). B is evaluated there in double precision.
- **The scaled slack** is σ = min_grid B / B(1): the bracket's minimum, scaled by its size at infinity
  (`TARGET_HD.md` §4.2). If B(1) ≤ 0, or a value is not finite, the sample fails.
- **The threshold is θ = 10⁻⁴.**
- **The planning record**, per sample (BHM-058 §2.5):
  - q, μ and δ_t;
  - P_true(0) and P_true(1);
  - the minimum of ψ₁ on the grid, and where it occurs;
  - the exact design's slack, from BHM-024's identity B = ε/ψ₁² + εz⁵[z(ρf′ + f(2P_true − 1)) + 6f(1 − z)]
    − ρ²fη², with no fit;
  - σ, and where it occurs, for every (ε, variable, degree).

## 5. The decision rules (`TARGET_HD.md` §4)

- **Qualifying.** A (band, rung) qualifies if, with ε = 1/50, some variable and some degree ≤ 48 give
  σ ≥ θ at all 9 samples. If ε = 1/50 qualifies nowhere, the same test is made with the fallback
  ε = 1/200.
- **q_max(D)** is the largest rung at which every band of D active there qualifies.
  - A rung with no active band qualifies.
  - If no rung qualifies, D is reported as not attempted at this stage (`TARGET_HD.md` §4.3).
- **The design HD-S registers for each band** at q_max(D): ε, the variable and the least qualifying degree.
  Ties go to z. HD-S's PREREG adopts it, with its own fallback.

## 6. Gates and controls (in the same run)

| Name | What | Must |
|---|---|---|
| PG1 | The recorded rule-2 certificates T1 (D = 6, ℓ = 2, μ = 1/6) and G1 (D = 10, ℓ = 2, Q = 0), for which N > 0 is proved exactly (BHM-025). σ under this evaluator, with P and P_z evaluated exactly at each grid point and then rounded | σ > 0 for both |
| PG2 | The pilot's own design at T1 and at G1, in z at degree 28 with ε = 1/50 (the certified designs' settings) | σ ≥ θ for both |
| NC-H | T1's pilot design with P(0) raised 1/10 above the horizon bound W(0)/f_z(0) (TD-P2's tamper) | σ < 0 |
| NC-B | A planted bound state at G1's setting: W − Kb on [3/10, 3/5], with b = ((z − 3/10)(3/5 − z))² and K = 2I₁/I₂, so that the trial function b has energy −I₁ < 0 (NC-P1's construction; I₁ > 0 required) | (i) no qualifying design, in either variable, at any degree, for either ε; (ii) G1's pilot design against W − Kb has σ < 0 |

## 7. Pass criterion, and what follows

- **VALID** requires PG1, PG2, NC-H and NC-B as registered.
- **Record and reproduction.** The record runs on host-1 and the reproduction on host-2, from a
  `git archive` of this commit (`kit/hd/run_pilot.sh`).
  - They must be identical after masking timings.
  - If they are not, the decisions must agree and every σ must agree to 10⁻⁶ relative; otherwise the
    pilot is VOID.
- **On VALID:** q_max(D) and each band's design are fixed by a sealed `TARGET_HD` addendum before any
  HD-S run, as `TARGET_HD.md` §4.2 requires. HD-S's PREREG follows.
- **On VOID:** nothing is fixed. The failure is reported, and a new registration is needed.

## 8. What ran before this registration

- **Development, on host-1,** from a `git archive` of `486dcbc`:
  - syntax checks;
  - a count of the grid's points;
  - `python -m hd.devtest_pilot`, synthetic inputs only:
    - a Chebyshev fit of exp z;
    - the fit of 1/(z + 1/100) in z and in ζ, with δ_t = 1/25;
    - `exact_eval` on a quadratic;
    - the μ(q) inverse of the parametrisation, as algebra only;
    - `sample()` on a synthetic U = 64m³ + 400x², H = m + 15x;
    - the breakdown path, with a synthetic well of depth 10⁹.
- **Not run:**
  - S5's U₋ was evaluated for no band, and not for T1 or G1;
  - no gate or control was run;
  - θ was fixed before any development run.

## 9. Artifacts

- `code/hd/pilot.py` and `kit/hd/run_pilot.sh`;
- `code/hd/elementary.py` (the band table `BANDS`), `code/p3/scert.py` (`cheb_coeffs`) and
  `code/ki/potentials.py`;
- `results/p3/rule2/record/T1/result.json` and `results/p3/rule2/record/G1/result.json` (PG1).

All are at the commit that holds this file.
