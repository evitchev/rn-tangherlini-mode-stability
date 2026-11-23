# PREREG — HD-E: positivity of U₋ for D = 7–11 where it holds (stage 2, step 2)

*Item BHM-062. 2026-10-23, the bh-modes lead. Part HD-E of `TARGET_HD.md` (BHM-061). Sealed; any
change before the run is a dated addendum.*

## 1. Setting

`TARGET_HD.md` §1: D = n + 2 with n = 5, …, 9; S5's (5.62b), (5.63b) at general n
(`ki.potentials`); m = (ℓ − 1)(ℓ + n); the parametrisation A = (ℓ + n) + (ℓ − 1)μ², B = 2ℓ + n − 1,
w = Bμ/A, s = 1 + 2mδ = B((ℓ + n) − (ℓ − 1)μ²)/((n + 1)A). On the exterior f > 0 and H₋ ≥ m > 0,
so V has the sign of U₋.

## 2. Claims (all exact)

- **E1.** For every ℓ with ℓ_el(n) ≤ ℓ ≤ ℓ₀(n), every q ∈ [0, 99/100] and every x ∈ [0, x_H(q)]:
  U₋ > 0. The values are ℓ_el = 4, 5, 6, 6, 7 for D = 7, 8, 9, 10, 11; these are the screen's
  elementary ℓ.
- **E2.** For each of the 13 bands with a screen onset q_on > 0, U₋ > 0 for q ∈ [0, q_split],
  x ∈ [0, x_H]. Here q_split = ⌊1000·q_on⌋/1000 − 1/1000:

  | D | ℓ: q_split |
  |---|---|
  | 7 | 2: 0.948; 3: 0.977 |
  | 8 | 3: 0.944; 4: 0.983 |
  | 9 | 3: 0.921; 4: 0.952; 5: 0.987 |
  | 10 | 3: 0.490 (the interior band); 4: 0.920; 5: 0.961 |
  | 11 | 4: 0.897; 5: 0.929; 6: 0.968 |

- **E3, Lemma U(n), for each n.** For every ℓ > ℓ₀(n), every q ∈ [0, 1] and every x ∈ [0, 2]:
  U₋ ≥ m³(64 − Neg_n(ε̄, 1/(n + 1), 2)) > 0.
  - Here ε⁶U₋(x; m = ε⁻², δ = κε) = Pos_n − Neg_n, both with nonnegative coefficients, and
    Pos_n(0) = 64. ε̄ = 1/isqrt(m(ℓ₀ + 1)).
  - ℓ₀(n) is the least ℓ₀ ≥ max(ℓ_el(n), 10), searched up to 400, at which the bound is > 0.
- **What follows.**
  - Theorem HD holds for ℓ ≥ ℓ_el(D) and all q ≤ 99/100.
  - For each band with q_on > 0, it holds for q ≤ q_split. The band's S-certificates (HD-S) must
    start at or below q_split.
  - The five bands from 0⁺ (D = 8–11 ℓ = 2, D = 11 ℓ = 3) have no part here.

## 3. Method (`code/hd/elementary.py`)

**Part I, for each (n, ℓ, q_hi).**
- The code checks exactly that s² = 1 + 4mq²/(n + 1)², q(1) = 0, q(0) = 1 and δ(1) = 0, and that w
  increases on [0, 1] (Bernstein).
- μ_lo = k/10000, with k the largest integer such that w(k/10000)² ≤ 1 − q_hi² (binary search). The
  code checks exactly that q(μ_lo)² ≥ q_hi².
- U₋ = F(t, μ)/Den(μ) in lowest terms, with F/Den = U₋ checked. Den > 0 and F > 0 on
  [0, 1] × [μ_lo, 1] are proved by exact Bernstein bisection (`onset.bernstein.prove_sign`,
  depth ≤ 40).
- A certified lower bound of U₋ is recorded, as in BHM-052.

**Part II.** As BHM-047 §3, with n general. The pencil steps (a)–(d) carry over:
- (a) mδ² + δ = q²/(n + 1)² gives κ ≤ 1/(n + 1);
- (b) x ≤ x_H ≤ 2;
- (c) ε ≤ ε̄ for m ≥ m(ℓ₀ + 1);
- (d) monotonicity of polynomials with nonnegative coefficients.

**Implementation parameters:** the 1/10000 grid, the depth, and the search rule for ℓ₀.

## 4. Gates, controls and drills

| Name | What | Must | Predicted |
|---|---|---|---|
| KAT | the verifier's KATs (BHM-047) | hold | hold |
| E0n | `ki.potentials`' U_minus(n), H_minus(n) equal Kimi's independent transcription (BHM-036; `results/p3/audits/kimi_2026-10-22/own/build.py`, its SHA-256 checked first) for n = 2, …, 12 | hold | hold |
| PARAM4 | param_n(4, ℓ) equals `onset.param`(ℓ) for ℓ = 2…5 | hold | hold |
| H | H₋'s coefficients > 0 for n = 5…9 | hold | hold |
| NC-E1 | `nc-onset-h`: D = 7, ℓ = 2 up to q = 951/1000, past its horizon onset 0.9497 | REJECT | an exact counterexample at the horizon corner, t = 1 |
| NC-E2 | `nc-onset-i`: D = 10, ℓ = 3 up to q = 99/200, past its interior onset 0.4913 | REJECT | an exact counterexample at an interior node, 0 < t < 1 |
| NC-E3 | `nc-zero`: D = 8, ℓ = 2 on q ∈ [0, 1/10], a band from 0⁺ | REJECT | an exact counterexample |
| NC-E4 | `nc-coverage`: D = 7, ℓ = 4 with μ_lo chosen for q = 98/100 | REJECT | the coverage check for 99/100 fails |
| NC-E5 | `nc-uniform`: Lemma U(9) with ℓ₀ = 2 forced | REJECT | the corner bound < 0 |
| TD-E1 | `td-coeff`: U_minus(n) + 16nm² | REJECT | E0n fails |
| TD-E2 | `td-param`: B = 2ℓ + n instead of 2ℓ + n − 1 | REJECT | the identity s² = 1 + 4mq²/(n + 1)² fails in every job |
| TD-E3 | `td-verifier`: acceptance threshold −1 | REJECT | the KATs fail |

## 5. Pass criterion, and what follows

- **VERIFIED** requires all of:
  - the gates;
  - E1 for every n and every ℓ ∈ [ℓ_el(n), ℓ₀(n)];
  - E2 for all 13 bands;
  - E3 for all five n.
- **Record and reproduction.** The record runs on host-1 and the reproduction on host-2, from a
  `git archive` of this commit (`kit/hd/run_elementary.sh`), and they must be identical after
  masking. The kit passes only if every control and drill rejects.
- **Status on VERIFIED:** HD-E *certified* (exact); Lemma U(n)'s pencil steps proved (pencil;
  audited 0×). Theorem HD then holds for every ℓ ≥ ℓ_el(D) and q ≤ 99/100, and for every band with an
  onset, up to its q_split.
- **On a REJECT of the main run:** reported as it stands. The failing (n, ℓ) and its counterexample
  say where the screen's band list was wrong.

## 6. What ran before this registration

- **Development, on host-1,** from a `git archive` of `3593611`:
  - syntax checks;
  - `python -m hd.devtest`, synthetic inputs only:
    - Part I's code path for (n, ℓ) = (5, 4) on U = 64m³ + x²;
    - Lemma U's code path for n = 9 on U = 64m³ − 7680mx;
    - the loading of Kimi's `build.py`, with no comparison made.
- **Not run:** nothing of S5's U₋ for n = 5…9 was evaluated, and no gate, control or drill was run.

## 7. Artifacts

- `code/hd/elementary.py` and `kit/hd/run_elementary.sh`.
- `code/a1/p1.py` (KATs, `positive_mu`, `plain`), `code/onset/bernstein.py`, `code/onset/onset.py`,
  `code/ki/potentials.py`.
- `results/p3/audits/kimi_2026-10-22/own/build.py`, as an oracle.
- `results/screen/runs/record/main/result.json`, the source of the onsets (BHM-014).

All are at the commit that holds this file.
