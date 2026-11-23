# Item (c), option B: independent exact re-run of T3 (bh-modes, ℓ = 2), run of record: session-L, 2026-10-23

> **For second-party seats** (Kimi, the session-R lead's blind subagent): please do not read this folder
> before your own check.

**Result: C-B is VERIFIED on all eight boxes, and every registered requirement and prediction holds** (`out/record.out`
ends "ALL AS REGISTERED").

- **Registration.** `../p3_T3_rerun_registration_2026-10-22/REGISTRATION.md` (sha256 `1224713c…`, archived by the lead
  as BHM-044). It was written before any run, and this folder follows it without deviation.
- **Ruling.** The operator ruled that this run counts as CHARTER e5's second party (`OPERATOR_RULING.txt`).
- **Code.** `code/p3rerun.py`, sha256 `9edeb8b1…`.
  - It was frozen at 04:38:40Z (`FREEZE.txt`), after a development run on the known-answer gates and a synthetic P
    only (`out/dev.out`).
  - The run of record is its first execution on T3's data. It took 82.7 s.

## What is certified

For each k = 0, …, 7 and every (z, μ) ∈ [0, 1] × [a_k, b_k], with exact integer Bernstein arithmetic:

    N_k(z, μ) > 0,   N_k = Ñ_k/((μ + 1)³(μ + 6)).

- **X1.** Ñ_k/((μ + 1)³(μ + 6)) equals item (a)'s `Nz (U6 q 6 δ) (H6 q 6 δ) (F6 q) (F6' q) P_k(·, μ) ∂_zP_k(·, μ)`
  exactly, with q = q(μ), δ = δ(μ). This is checked by sympy, not in Lean.
- **D3.** The eight boxes tile [3/25, 1/5].
- **With the Lean bridge.** By item (a)'s `prop3_D6`, the quadratic form is ≥ 0 for every μ ∈ [3/25, 1/5], that is
  q ∈ [0.97277, 0.99020], and every inverse tortoise map R.
- **So the record's T3 (BHM-023) is confirmed** by a second party, from the same certificate data and with
  independently written code.

## Per box

Every box is certified by one bisection in z at z = 1/2, giving 2 leaves at depth 1 (3 nodes). "Min ratio" is the
smallest Bernstein coefficient over the largest in modulus, on the worse leaf.

| k | box | min ratio | X1 | X2 | X3 (z = 1, z = 0) | NP-A: c_k, outcome | NP-B: outcome | time |
|---|---|---|---|---|---|---|---|---|
| 0 | [3/25, 13/100] | 0.2174 | ✓ | 40/40 | ✓ ✓ | 1/32, REJECT at (1/4, 3/25), N ≈ −362.6 | REJECT at (1, 3/25), N = −18432 | 10.5 s |
| 1 | [13/100, 7/50] | 0.2155 | ✓ | 40/40 | ✓ ✓ | 1/32, REJECT at (1/4, 13/100), N ≈ −361.7 | REJECT at (1, 13/100), N = −18432 | 10.1 s |
| 2 | [7/50, 3/20] | 0.2134 | ✓ | 40/40 | ✓ ✓ | 1/32, REJECT at (1/4, 7/50), N ≈ −360.7 | REJECT at (1, 7/50), N = −18432 | 10.4 s |
| 3 | [3/20, 4/25] | 0.2113 | ✓ | 40/40 | ✓ ✓ | 1/32, REJECT at (1/4, 3/20), N ≈ −359.6 | REJECT at (1, 3/20), N = −18432 | 10.1 s |
| 4 | [4/25, 17/100] | 0.2092 | ✓ | 40/40 | ✓ ✓ | 1/32, REJECT at (1/4, 4/25), N ≈ −358.5 | REJECT at (1, 4/25), N = −18432 | 10.3 s |
| 5 | [17/100, 9/50] | 0.2069 | ✓ | 40/40 | ✓ ✓ | 1/32, REJECT at (1/4, 17/100), N ≈ −357.3 | REJECT at (1, 17/100), N = −18432 | 10.4 s |
| 6 | [9/50, 19/100] | 0.2047 | ✓ | 40/40 | ✓ ✓ | 1/32, REJECT at (1/4, 9/50), N ≈ −356.0 | REJECT at (1, 9/50), N = −18432 | 10.4 s |
| 7 | [19/100, 1/5] | 0.2024 | ✓ | 40/40 | ✓ ✓ | 1/32, REJECT at (1/4, 19/100), N ≈ −354.7 | REJECT at (1, 19/100), N = −18432 | 10.5 s |

- **Data checks.** D1 (the T3 file's sha256 starts `f893d820aa0f289f`), D2 (the record and the reproduction have
  identical boxes and P) and D3 all hold.
- **Counterexamples.** Every reported counterexample was recomputed at the same point by route P. The exact values
  agree.
- **NP-A's witnesses.** At (1/3, μ0_k), N ≈ −150 on every box. Route R's closed forms, route R's expanded polynomial and
  route P give the same exact value.

## The registered predictions against the run

| registered | outcome |
|---|---|
| KA1–KA4 hold: B1 and B2 coefficient sets equal the Lean file's (minima 731962/9 and 179096); KA3 REJECT; KA4 VERIFIED | as registered |
| X1–X3 hold on every box | as registered |
| C-B VERIFIED on all eight boxes | as registered |
| NP-A not VERIFIED on any box (must); REJECT with an exact counterexample on all eight (predicted) | as registered |
| NP-B REJECT on all eight (must), at depth 0 at (1, a_k) with N = −18432 (predicted) | as registered |
| DR1: the corner-only checker VERIFIES NP-A wherever P_k is VERIFIED | as registered: it VERIFIES NP-A on all eight boxes, which the real checker REJECTS |
| DR2: with F's constant at 165889, X1 fails and X2 fails at all 40 points | as registered, on every box |

## Notes

- **Against the record.**
  - The record used 3 Bernstein boxes per μ-box at degree (68, 16).
  - Here, in item (b)'s reduced form, N has degree (68, 12) and needs 2 boxes per μ-box.
  - The certificate data are the same. The code was written independently of the record's: none of it is shared, and
    sympy appears only in the cross-checks.
- **The size of the margin.**
  - On every box, (1/32)·β(z) added to P_k makes N negative at (1/3, μ0_k), while (1/64)·β(z) does not.
  - So a perturbation of P of a size close to the design's ε = 1/50 can break the certificate in the interior, and
    the checker catches it.
- **Outside Lean.** The Bernstein positivity (my Python) and the identification X1 (sympy) are outside Lean, as
  option B intends. Lean covers the reduction (`prop3_D6`, item (a)) and U₋ = F/Den (`param_U`, item (b)).
- **Not blind.** I knew the record's verdict before the run. This is stated in the registration, §5.
- **Environment.** The run was on the editing node of the bh-modes environment, as were the Kimi and Fable spot
  checks. Whether seats must compute on the compute nodes is the operator's call. The run is deterministic and needs
  no network, so a reproduction elsewhere is the one command below. It should give the same `out/record.json` except
  for the timings.

## Reproduce

    cd code
    [python-2]/bin/python3 -I -B p3rerun.py record LEAN_ONSET T3_RECORD T3_REPRO ../out/record.json

- `LEAN_ONSET` is `lean_onset_2026-10-22/lean/BHModesOnset.lean`, used for `Fp`, `B1` and `B2`.
- `T3_RECORD` and `T3_REPRO` are bh-modes `results/p3/runs/record/T3/result.json` and
  `results/p3/runs/repro-*/T3/result.json`.
- The environment is Python 3.12 and sympy 1.14.0. sympy is used only in X1 and in X3 at z = 0.

## Files

| file | content |
|---|---|
| `code/p3rerun.py` | the frozen code: route R, routes L and P, the Bernstein search, the planted certificates, the drills |
| `FREEZE.txt` | the code's sha256 and freeze time, written before the run of record |
| `OPERATOR_RULING.txt` | the operator's ruling on second-party status |
| `out/dev.out` | the development run: helper self-tests, KA1–KA4, every code path on a synthetic P (not T3 data) |
| `out/record.out`, `out/record.json` | the run of record: printed summary, and every value (exact rationals as strings) |
| `SHA256SUMS` | every file except itself |
