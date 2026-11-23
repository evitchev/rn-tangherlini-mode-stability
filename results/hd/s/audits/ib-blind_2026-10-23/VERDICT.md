# VERDICT — HD-S band 1: D = 7, ℓ = 2, q ∈ [948/1000, 99/100] (ib-blind seat, 2026-10-23)

## Verdict: **holds (certified)**

For every q ∈ [948/1000, 99/100], A_{2,q} = −d²/dr*² + V_q on C₀^∞(ℝ) is non-negative: it has no negative spectrum.
- This is **certified** in exact rational arithmetic, relative to my transcription of S5 (TRANSCRIPTION.md).
- Two exact pieces cover the band:
  - exact positivity of V on the exterior over the low-charge end (E0);
  - an S-deformation certificate over the rest (Part C).
- Separately, the pre-registered Sturm count (Part N) gives **holds (numerical)** on its own. It agrees with the
  certificate.

**Anchors.**
- Brief: sha256 `1339b7fbd0c0761e055e375501bbb857485fc728c40c5c2b2bf2e0e19a8703dd`.
- `PREREG.md`: `7addc5911fdda10724a222558d26421dc05e8b016b12eb650e9d9f38ddfb1b87`, approved.
- `PREREG_AMEND_1_2026-10-23.md`: `7787687075b214c2c8d96752c7b745ad53493829ed734c8542c1192ea7966c30`.
- `TRANSCRIPTION.md`: `23f926e19f289b371346de2428faac68920a9d00ebbfa5b1d720ca6557c0ee80`.
- Record code is frozen in `code/rec/*_v1.py` (hashes in `logs/code_rec_v1_sha256.txt` and `runs.json`).
- All runs of record were on **host-2** under `nice -n 19` with `[venv]` (Python 3.12.8, python-flint 0.9.0,
  sympy 1.14.0, mpmath 1.3.0), as it is.

## 1. Results by part

### Certified (exact)

The band is covered in the rational parameter µ_T (TARGET_HD §1, checked in TRANSCRIPTION.md).

| Part | Statement | Run |
|---|---|---|
| E2 | The cover µ_T ∈ [1237/10000, 2817/10000] is exactly q ∈ [0.94797859, 0.99000061] ⊇ [0.948, 0.99]. The denominator 1296(1+µ)⁴(7+µ)⁴ > 0 on it. | RR-07 |
| E0 | U₋ > 0 on [0,1]_z × [2780/10000, 2817/10000] (Bernstein, 3 leaves). So **V > 0 on the whole exterior** and A ≥ 0 for q ∈ [0.947979, 0.949342]. This includes the brief's background statement at q = 0.948. | RR-07 |
| C | **16/16 cells certified** on µ_T ∈ [1237/10000, 2780/10000], i.e. q ∈ [0.949342, 0.990001]. In each cell N(z, µ) > 0 on [0,1] × cell, exactly, which makes V + S′ − S² ≥ 0 (PREREG L2), so A ≥ 0 (L1). | RR-10 |

**The Part C certificate in detail.**
- S = −f P/ρ, with P(z, µ) linear in µ across each cell. Its endpoint polynomials have degree 24 in z, with
  coefficients in 2⁻⁴⁸ℤ. They are fits to P_true − 0.02, where P_true = ρψ₀′/ψ₀.
- Every cell certified on the first attempt, with 2 Bernstein leaves.
- In every cell, the exact polynomial agrees with an independent sympy evaluation of N at **50/50** random rational
  points.
- At the horizon, P(0) = P_true(0) − 0.02 at the corners. At infinity, P(1) = 4.480, inside the window (−7/2, 9/2).

### Numerical (Part N, cross-check; it passes by itself)

**Grid.** q_i = 948/1000 + i/2000, for i = 0…84 (RR-08).

**Zero counts.** Every point gives Z = 0:
- integrator I (mpmath Taylor, 30 digits), by sign changes and by Prüfer angle;
- integrator II (float RK4 in log(ρ−1), at N and 2N steps);
- the 45-digit rerun at 22 points.

**Agreement.**
- Integrators I vs II: ≤ 8.3e-13 relative in ψ₀, ≤ 4.6e-11 in ψ₀′.
- Richardson error: ≤ 1.2e-13.
- 45-digit vs 30-digit: ≤ 4.8e-25.

**Size of the zero-energy solution.** min ψ₀ falls from 1.0014 (q = 0.948) to **0.8912** (q = 0.99, at ρ ≈ 1.475).

**Tail.** ρ₁* = 1.5: E1 (exact) shows V > 0 for ρ ≥ 1.5 across the band, and ψ₀(1.5), ψ₀′(1.5) > 0 at all points.

**Gap argument** (RR-09). All 84 cells pass for ψ₀(1.5; q) (worst margin 12,463× the interpolation bound) and for
ψ₀′(1.5; q) (worst cell [0.9895, 0.99]: 0.00812 against a bound of 2.97e-5, i.e. 273×). No bisection was needed.

## 2. Controls and tampers (all behaved as pre-registered)

| Control | Required | Observed | Run |
|---|---|---|---|
| TP2, transcription guard | a T1-tampered U₋ aborts before computing | guard FAIL (C1–C4, C8, C10), EXIT 3 | RR-01 |
| NEG1, ground truth | rigorous negative form value with the planted well | q = 0.97: unperturbed I₁+I₂ = +0.19999… (A3 not triggered); A = 10; Q[φ] = −0.053972 certified; Rayleigh quotient ≤ −0.9735 | RR-02 |
| NEG1, Sturm | Z ≥ 1 in both integrators | Z = 1 in I, II (N and 2N) and the 45-digit rerun | RR-03 |
| NEG1, certifier (X3a) | refuse at the 4 retry settings | 4/4 refused | RR-06 |
| NEG1, certifier (X3b) | the band cell's own P is refused once the well is added | refused (negative exact corner at z = 1/4) | RR-11 |
| POS0, q = 0 | Z = 0 | Z = 0 | RR-04 |
| TP1, verifier tamper (out-of-band cell) | P + Δ and P − 20 rejected | both rejected | RR-05 |
| TP1, verifier tamper (first band cell) | same | both rejected (Δ = 3/25) | RR-10 |

The Bernstein self-test (corner property, enclosure, a known pass and a known fail) passed at the start of every
certificate run.

## 3. How sure I am, and why

**Very sure, relative to S5's potential as I transcribed it.**

**The certificate is exact.**
- It rests on two elementary identities: L1, which is integration by parts, and L2, which was checked
  symbolically (C9).
- The rest is polynomial positivity in rational arithmetic: Bernstein coefficients that are all strictly positive.
- The margins are not thin: every cell needed only 2 leaves, with a uniform shift ε = 0.02.

**The numerics agree independently.**
- ψ₀ stays at or above 0.89 everywhere on the band, so it is far from having a zero.
- Two integrators, of different methods and arithmetic, agree to about 1e-12.

**Residual risks.**
- *A transcription error in S5, or in my reading of it.* This is reduced by:
  - the Q = 0 limit (Paper I, general n);
  - n = 2 against Zerilli and Chandrasekhar's charged polar RN potentials;
  - the U₊ ↔ U₋ involution;
  - the extremal structure: κ(n,ℓ) + 1/4 is a perfect square for all n, ℓ;
  - exact agreement with the brief's two background numbers: the horizon sign change at q = 0.949691… and κ = −1/4
    at q = 1.
- *A software defect.* This is reduced by the controls above, the exact cross-evaluation in every cell, and both
  tamper drills.
- *python-flint's exact arithmetic.* I trust it as a standard library and did not audit it.

## 4. Observations (data, not interpretation)

- P_true(0) = W(1)/f′(1) runs from +0.005 (µ_T = 0.278) to −1.910 (q = 0.99). The dip of ψ₀ below 1 deepens toward
  q = 0.99 but stays shallow.
- At extremality the inverse-square coefficient is κ(n,ℓ) = ℓ(ℓ−n+1)/(n−1)² (TRANSCRIPTION.md, C10). D = 7, ℓ = 2 is
  exactly critical (κ = −1/4), as the brief says. The band stops at q = 0.99, where the margins above are still
  comfortable.

## 5. Process notes

- **A1.** Every run of record logged `date -u; hostname; uptime; nproc; free -g`, then the Python gate:
  - w = 1–8, load1 ≤ 1.5, MemAvailable ≈ 121 GB, all within the rule;
  - RR-01 aborted at the guard, by design, before the Python gate.
- **A2.**
  - `code/rec/*_v1.py` was frozen read-only before RR-01 and never edited.
  - The only difference from the development versions is the import lines (module names).
- **A3.** Not triggered: I₁ + I₂ > 0 at q = 0.97, and no q_i gave Z ≥ 1.
- **Development runs** (8; only out-of-band parameters; recorded in `runs.json`) found and fixed two bugs before the
  freeze:
  - mpmath odefun took about 1e5 steps to reach ρ = 5·10⁴ and hit the 8 GB cap (abort, exit 134). Fixed by
    integrating ρ > 100 in log ρ.
  - The Chebyshev nodes were mirrored. The exact verifier correctly refused the resulting P.
- **Phase 1.** The phase-1 slips were disclosed in the phase-1 report and accepted.
- **Monitoring and copies.**
  - My own jobs were checked only by PID, from a pidfile.
  - Every run-of-record log and output was copied back and matches the node copy byte for byte
    (`node_mirror_host-2/`).
- **Blindness.** It held throughout. In bh-modes I opened only the brief, TARGET_HD.md §1 and
  `results/p3/METHOD.md`. On host-2 I used only my own folder and the venv; on host-1, one environment probe. I listed
  no processes and never touched `[run-folder]/`. I have not seen bh-modes' result for this band.

## 6. Where things are (in this delivery)

- **Documents:** `VERDICT.md`, `PREREG.md` (+ `.sha256`), `PREREG_AMEND_1_2026-10-23.md` (+ `.sha256`),
  `TRANSCRIPTION.md`.
- **Records:** `runs.json` (every run, with host, gate, code hashes and log hashes);
  `records/runs_phase1_3ea47ab2.json`; `PHASE1_SHA256SUMS`.
- **Code:**
  - `code/ki_s5.py` (the transcription), `code/check_transcription.py`;
  - `code/rec/` (record code), `code/dev/` (development), `code/tools/` (bookkeeping only);
  - `code/archive/`.
- **Outputs:** `logs/` (full logs), `out/` (JSON outputs), `node_mirror_host-2/`.
- **Sources:** `lit/` (S5 v1–v4 and Paper I PDFs, with the pdftotext extracts used).
- **Checksums:** `SHA256SUMS` covers every file in this folder except itself.
