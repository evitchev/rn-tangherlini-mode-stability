# PREREG — blind determination, HD-S band 1: D = 7, ℓ = 2, q ∈ [948/1000, 99/100]

*ib-blind seat (Claude agent working for the session-R lead). Written and sealed 2026-10-23, before any
computation of the determination. It is sealed by `chmod 0444`; its sha256 is in `PREREG.sha256`. Changes can only
come as dated, separately sealed `PREREG_AMEND_<k>_<date>.md` files, each written before the runs it affects.*

## 0. Anchors

**The brief.** `[repository]/results/hd/s/briefs/BRIEF_ib-blind_2026-10-23.md`,
sha256 **`1339b7fbd0c0761e055e375501bbb857485fc728c40c5c2b2bf2e0e19a8703dd`** (checked 2026-10-23T15:16Z).

**My transcription.** `TRANSCRIPTION.md`, sha256 `23f926e19f289b371346de2428faac68920a9d00ebbfa5b1d720ca6557c0ee80`.
- The formulas are coded in `code/ki_s5.py` (sha256 `b2585fb00ba70a3bbe50e55ce1ca22dc8811799252d521b5fbebfc934b6d311b`).
- The checks are `code/check_transcription.py` (sha256 `30333817d35e4bea9a6f548e09624c62679d34f7fa8bac42947d87738c587cd4`).
- All ten checks pass, and four tampers are each caught (TRANSCRIPTION.md §5).

**Source.** S5 = hep-th/0308128 **v4**, PDF sha256 `317219dcee4b2195b0a4c06c9d984daeb5f594f403235b653c6771a5beedcaf6`,
read with pdftotext 0.86.1 only.

**Phase 1 computed only:**
- the transcription checks C1–C10;
- the extremal κ(n, ℓ) at q = 1;
- the exact band edges in µ_T;
- environment probes.

Nothing integrated the zero-energy equation, and nothing tested any certificate.

For q in the band, the only evaluation of V was check C8a: the sign of U₋ at the horizon x = x_H, as a function
of q. It has a single sign change, at q = 0.949691…, which the brief gives as background. Nothing tested the sign
of V on the rest of the exterior.

I hold no result for this band, and I have not seen bh-modes' result.

## 1. The question

**Claim (brief).** For n = 5, ℓ = 2 (m = 7) and every q ∈ B = [948/1000, 99/100], the operator
A_q = −d²/dr*² + V_q on C₀^∞(ℝ) is non-negative.

**Notation.**
- V_q = f U₋/(64 r² H₋²), with f = 1 − x + q²x²/4, x = x_H ρ^{−4}, H₋ = 7 + 15(1+7δ)x, and U₋ as in
  TRANSCRIPTION.md §4.
- Units: r_H = 1, so ρ = r ∈ (1, ∞). Positivity does not depend on the scale, since V scales as r_H^{−2}.
- z = 1 − 1/ρ ∈ (0, 1), and dr*/dρ = 1/f. W := V/f = U₋/(64ρ²H₋²).
- Charges are parametrised by µ_T ∈ [0, 1] (TRANSCRIPTION.md §4). Everything is then rational in (z, µ_T).
- **The cover.** C = [µ_lo, µ_hi] = [1237/10000, 2817/10000]. Exactly, q(µ_lo) ≥ 99/100 and q(µ_hi) ≤ 948/1000, and
  q is strictly decreasing in µ_T. So C ⊇ B. Covering slightly more than B is allowed: it only strengthens a
  "holds".

## 2. Mathematical basis (fixed now)

**L1 (S-deformation; METHOD.md Lemma 1, re-derived).** For real S ∈ C¹(ℝ) and φ ∈ C₀^∞(ℝ),
∫(|φ′|² + V|φ|²) = ∫|φ′ + Sφ|² + ∫(V + S′ − S²)|φ|². So V + S′ − S² ≥ 0 on ℝ implies A ≥ 0.

**L2 (METHOD.md Lemma 2; checked as C9).** Put S = −f P(z)/ρ. Then V + S′ − S² = f N/(64ρ²H₋²), with
N := U₋ − 64H₋²[(1−z)f_z P + f(−P + (1−z)P_z + P²)].
- On the exterior f > 0 and H₋ ≥ 7 (since δ ≥ 0 and x > 0). So **N ≥ 0 on [0, 1] implies A ≥ 0.**
- The endpoints are N(1) = −784(2P(1)−9)(2P(1)+7), which needs −7/2 < P(1) < 9/2, and
  N(0) = U₋(x_H) − 64H₋(x_H)² f_z(0) P(0).

**L3 (zero-energy criterion).** ρ = 1 is a regular singular point of (fψ_ρ)_ρ = Wψ, with double exponent 0. Let
ψ₀ be the analytic solution there with ψ₀(1) = 1 (so ψ₀ → 1 as r* → −∞). Let Z(q) be the number of zeros of ψ₀ on
(1, ∞).
- **(a) Z = 0 implies A ≥ 0.** Apply L1 with S = −(dψ₀/dr*)/ψ₀; then V + S′ − S² ≡ 0.
- **(b) Z ≥ 1 implies that A has a negative eigenvalue.**
  - Let r*₁ be the first zero. Put u = ψ₀ on (−∞, r*₁] and u = 0 after it. Let χ_L equal 1 on [−L, ∞) and fall
    linearly to 0 on [−2L, −L].
  - Then Q[χ_L u] = ∫χ_L′² u² = O(1/L). The boundary terms [χ²uu′] vanish, and −u″ + Vu = 0 on the support.
  - Adding εh, with h ∈ C₀^∞ near r*₁ and h(r*₁) ≠ 0, changes Q by −2εψ₀′(r*₁)h(r*₁) + O(ε²), and ψ₀′(r*₁) ≠ 0.
    So Q < 0 for suitable ε and large L.
  - V → 0 at both ends, so σ_ess = [0, ∞) and the negative spectrum consists of eigenvalues.

**L4 (tail).** Suppose U₋(x) ≥ 0 for 0 < x ≤ x_H ρ₁^{−4} (so V ≥ 0 on [ρ₁, ∞)), ψ₀(ρ₁) > 0 and ψ₀_ρ(ρ₁) ≥ 0.
Then ψ₀ > 0 on [ρ₁, ∞), because ψ₀ is convex in r* wherever it is positive.

**L5 (zeros enter only through the outer end).**
- Zeros of ψ₀ are simple, ψ₀ is jointly continuous in (ρ, q), and ψ₀ = 1 + O(ρ−1) uniformly for q in compact sets.
- So on a q-cell, the number of zeros in (1, ρ₁] stays constant unless ψ₀(ρ₁; q) = 0 somewhere in the cell.

## 3. Method

The verdict combines three parts. Each result is labelled **certified** or **numerical**.

### Part E — exact checks (label: certified)

**Method.** All checks are positivity checks of polynomials in Q[z or t, µ_T], after multiplying by an explicit
denominator that is positive on [0, 1]. Each is done in exact rational arithmetic (python-flint fmpq, fmpq_poly,
fmpq_mat) by tensor Bernstein expansion with exact de Casteljau subdivision. The criterion is that **every Bernstein
coefficient on every leaf is > 0**. The cap is 4096 leaves per check.

- **E0 (V ≥ 0 at low charge).**
  - Check D_E·U₋(x_H(µ)(1−z)⁴; µ) > 0 on [0, 1]_z × [µ_a, µ_hi], with **µ_a = 2780/10000**. This is safely past the
    horizon sign change at µ_T = 0.2770435, so q(µ_a) < 0.94969.
  - A pass gives A ≥ 0 there, by L2 with P ≡ 0. It also checks the brief's background statement at q = 948/1000.
  - If E0 fails, [µ_a, µ_hi] goes to Part C.
- **E1 (tail).**
  - For the ρ₁* chosen in Part N, check U₋(t·x_H(µ)ρ₁*^{−4}; µ) > 0 on [0, 1]_t × C.
  - The x⁰ term is 49392 > 0.
- **E2 (cover).** The exact inequalities q(µ_lo)² ≥ (99/100)² and q(µ_hi)² ≤ (948/1000)², and positivity of
  D_E and D_C (the cell denominators) on C, by factor lists.

### Part N — Sturm count (label: numerical)

**Grid.** q_i = 948/1000 + i/2000, for i = 0, …, 84. That is 85 points, with both ends of B included exactly.

**ψ₀ at each q_i.**
- **Start.** Frobenius series at ρ = 1, from the exact recurrence
  a_N = [Σ_{k<N} a_k W_{N−1−k} − N Σ_{1≤k<N} k a_k g_{N−k}]/(N² g₀), where f = (ρ−1)g. The Taylor data of g and W
  come from truncated power-series arithmetic in mpmath, at working precision.
  - Order K = 60. Evaluate at ρ₀ = 1 + t₀, with t₀ = min(R/4, 1/50) and R = 1 − ((1−w)/(1+w))^{1/4} (the distance
    to the inner horizon).
- **Integrator I.** mpmath `odefun` (Taylor method) on the system ψ_ρ = χ/f, χ_ρ = Wψ (χ = dψ/dr*), at
  **mp.dps = 30**, from ρ₀ to ρ₁*.
- **Integrator II (independent).** Fixed-step classical RK4 in Python floats, in u = log(ρ−1), with 2×10⁴ and
  4×10⁴ steps and a Richardson error estimate. It starts from a separately computed order-30 series at t₀/2.

**Zero count Z(q_i).**
- Count sign changes of ψ at ≥ 4000 nodes, log-spaced in ρ−1.
- Cross-check with the unwrapped Prüfer angle θ = atan2(ψ, χ). θ increases through every multiple of π, so
  Z = ⌊θ_end/π⌋. The two counts must agree.
- Integrators I and II must agree on Z, and on ψ₀(ρ₁*) and ψ₀_ρ(ρ₁*) to relative 10⁻⁸.

**Tail.**
- **ρ₁*** is the first value in (1.5, 2, 3, 5, 10, 30, 100) for which (i) E1 passes and (ii) ψ₀(ρ₁*; q_i) > 0 and
  ψ₀_ρ(ρ₁*; q_i) > 0 at every grid point. L4 then excludes zeros beyond ρ₁*.
- If no listed value works, every q_i where (ii) fails is undetermined in Part N, and this is reported.
- As a sanity check (not part of the logic), integrate on to ρ = 100. There Z must be unchanged and ρψ₀_ρ/ψ₀ must
  approach 9/2.

**Precision check.** At every 4th grid point, rerun integrator I with mp.dps = 45 and K = 90. ψ₀(ρ₁*) must agree to
≥ 20 significant digits.

**Gap argument between grid points (L5 + L4; numerical).**
- The count can change inside a cell only if a(q) := ψ₀(ρ₁*; q) vanishes. The tail lemma needs b(q) := ψ₀_ρ(ρ₁*; q) ≥ 0.
- For g = a and g = b, with h the local grid spacing (1/2000 before any bisection) and second differences
  D2_i = (g_{i+1} − 2g_i + g_{i−1})/h², require on every cell [q_i, q_{i+1}]:
  min(g_i, g_{i+1}) > 2 · (h²/8) · max(|D2_i|, |D2_{i+1}|).
  This is the linear-interpolation error bound with a safety factor of 2. At the ends of B, use the one-sided D2.
- A cell that fails is bisected (new grid points added, the same tests run) up to 6 levels.
- **"holds (numerical)"** needs Z(q_i) = 0 at all points, and every cell to pass.

### Part C — S-deformation certificate (label: certified)

**Region.** [µ_lo, µ_a], plus [µ_a, µ_hi] if E0 fails. It starts as **16 equal cells** in µ_T.

**The certificate.**
- On each cell [µ_l, µ_r], P(z, µ) = (1−s)P_l(z) + sP_r(z), with s = (µ−µ_l)/(µ_r−µ_l). P_l and P_r are polynomials
  of degree ≤ 40 in z with rational coefficients (denominator 2⁴⁸).
- **How P is found is free and is not evidence.** The default is a least-squares fit to P_true − ε₁ − ε₂g(z), where
  P_true = ρψ₀_ρ/ψ₀ is numerical, ε₁ ∈ (0, 1) and g is a positive profile. Only the exact check below counts.

**Exact check.**
- Form D_C(µ)·N(z, µ(s)) ∈ Q[z, s] exactly from `ki_s5.py`. D_C is an explicit product of positive factors on
  [0, 1]: powers of 2, 3, (7+µ²), (1+µ) and (7+µ).
- **The cell is certified** if every tensor-Bernstein coefficient on [0, 1]² is > 0, possibly after subdivision.
  The subdivision caps are depth 10 in z, depth 6 in s, and 4096 leaves.
- A leaf with a negative exact corner value is a definite failure for that P.

**On failure.** Make up to 4 new attempts with changed P (degree, ε₁, g). Then bisect the cell, down to depth 6
(width (µ_a − µ_lo)/1024).

**Independent cross-evaluation.** In every certified cell, at 50 rational points (fixed seed 20261023), the verifier's
polynomial must **equal exactly** N evaluated by a separate sympy substitution into the L2 formula.

**Scope.** "Certified" means: exact, relative to my transcription of S5, assuming python-flint's exact arithmetic
is correct. Part C passes when every cell of its region is certified.

## 4. Controls and tampers (each must behave as stated; otherwise see §6, S3)

- **NEG1, planted well (must find negative spectrum).**
  - **Setup.** At q = 97/100, replace W by W − A b(ρ), where b = 16(ρ−1)²(2−ρ)² on [1, 2] and 0 elsewhere (C¹).
    The test function is φ = (ρ−1)(2−ρ) on [1, 2] and 0 elsewhere; it is in H¹(dr*).
  - **Integrals.** I₁ = ∫fφ_ρ² dρ, I₂ = ∫Wφ² dρ, I₃ = ∫φ²/f dρ (= ‖φ‖²) and I₄ = ∫bφ² dρ, all rigorously
    enclosed with `acb.integral` at 128 bits.
  - **Amplitude.** A := max(1, ⌈(I₁ + I₂ + 0.1·I₃)/I₄⌉ + 1). Then Q[φ] = I₁ + I₂ − A·I₄ ≤ −0.1‖φ‖² − I₄ < 0 is
    certified: the ground truth is negative spectrum.
  - If I₁ + I₂ < 0 already, without the well, that is itself a witness for the unperturbed operator at q = 0.97.
    It falls under S1 and is reported at once.
  - **Requirements.** Part N must report Z ≥ 1 there with both integrators. Part C must *not* certify the cell
    containing q = 0.97 with the well, after the same 4 attempts; a certification would be a verifier bug.
- **POS0, sanity check (not a gate on the verdict).**
  - At q = 0 (µ_T = 1), stability is known: Ishibashi–Kodama 2003 for Schwarzschild–Tangherlini. Part N must give Z = 0.
  - Any disagreement is reported.
- **TP1, verifier tamper (must be caught).**
  - Take the first certified cell. Replace P by P + Δ, with Δ = (max over the cell's two corner µ of
    P_true(0) − P(0)) + 1/10, rationalised. This forces N(0, µ) < 0 at a corner.
  - Separately, use P − 20, which forces N(1) < 0.
  - The exact verifier must reject both and print the negative corner values.
- **TP2, transcription guard (must be caught).**
  - Every Part N, C and E run of record first runs C1–C10 on the `ki_s5` it imports, and aborts on any FAIL.
  - Drill: one run with the T1-tampered U₋ (selected by an environment flag) must abort before computing anything.
    Its log is kept.
- **Run order.** The controls and drills run **before** the band runs of record, on the same code (hashes recorded).

## 5. Precision, grids, caps

**Precision.**
- mpmath: dps 30 for the main runs and dps 45 for the checks; Frobenius orders 60 and 90.
- Integrator II uses floats.
- Parts C and E are exact (python-flint fmpq). The rigorous integrals in NEG1 use 128-bit acb.

**Grids.**
- Part N: 85 points, step 1/2000, with adaptive bisection of up to 6 levels per cell.
- Part C: 16 µ-cells, with bisection down to depth 6.
- Part E: subdivision up to 4096 leaves.

**Caps for every Python run.**
- `ulimit -v 8000000` (8 GB per process, inherited by workers) and `timeout`: 1800 s for controls and drills,
  3600 s for a Part N sweep, 7200 s for a Part C invocation, 1800 s for Part E.
- At most 8 worker processes, under `nice -n 19`.

**Total node budget for phase 2.** At most 5 h wall, of which Part C may use at most 3 h.

## 6. Stopping rules

- **S1.** Suppose some q_i has Z ≥ 1 with both integrators agreeing. Then stop the band runs and build a witness:
  ψ₀ truncated at its first zero, with a cutoff at the horizon end and a smoothed corner, its form value rigorously
  enclosed (< 0) with acb.integral. Report the q and the witness to the lead at once, as the brief requires.
- **S2.** If the integrators disagree on Z at some q, rerun with dps 60 and K 120. If they still disagree, that q is
  undetermined and is reported.
- **S3.** If a control or tamper does not behave as in §4, stop the runs of record and report. The verdict can be at
  most "undetermined" until a fix is made, by a sealed amendment, and re-drilled.
- **S4.** When a budget in §5 is used up, stop that part and report what exists: certified sub-intervals and numerical
  results.

## 7. Verdict rules (one verdict in VERDICT.md)

- **holds (certified).**
  - E2 passes; E0 covers its sub-band or Part C covers it; Part C covers [µ_lo, µ_a]; all controls behave.
  - Part N, run as a cross-check, must also give Z = 0 everywhere. A contradiction between a complete certificate
    and Part N is treated as a bug, and the verdict is "undetermined" until it is resolved.
- **holds (numerical).**
  - Part N passes in full: Z = 0 on the grid, integrators and precision agreeing, tail and gap tests passing.
  - All controls behave, but the certificate is incomplete. Certified sub-intervals are listed separately, each
    labelled certified.
- **fails.** A q in B with a witness of rigorously negative form value.
- **undetermined.** Anything else, with reasons.

VERDICT.md will also state how sure I am, and why.

## 8. Host plan

**Nodes.**
- Runs of record go to **host-2**, with **host-1** as the fallback (if host-2 is unreachable or its 1-min load is
  > 12), **under `nice -n 19`**.
- The interpreter is `[venv]/bin/python3 -I`, used **as is, with no installs**: Python 3.12.8,
  python-flint 0.9.0, sympy 1.14.0, mpmath 1.3.0 with the gmpy backend (probed 2026-10-23).
- The workspace copy is `<node>:[session-R-runs]/hds_2026-10-23/`. It goes there by `scp`/`ssh -o BatchMode=yes`, and
  outputs come back to `host-0:[session-R-runs]/hds_2026-10-23/`, with sha256 compared after each copy.

**Each run.**
- The command prints `date -u` and `hostname` at its start and end, inside the same command.
- Its full output is `tee`d into `logs/` (never filtered before the tee).
- `runs.json` gets one record per run: id, purpose, record or spot check, host, command, start and end UTC, exit
  code, code and input sha256s, output and log sha256s.

**Blindness on the nodes.**
- I never access `[run-folder]/` or other processes' outputs.
- I check only my own jobs, by PID (`ps -o pid,etime,rss -p <PID>`), and list no other processes.
- In bh-modes I open nothing beyond the brief, TARGET_HD.md §1 and results/p3/METHOD.md.

**Phase-1 spot checks**, not of record, were run on host-2 (logs in `logs/`).

## 9. Deliverables (phase 2, after the lead's go)

- `VERDICT.md`.
- Code, logs and evidence under `SHA256SUMS`.
- `runs.json`, with the host of every run.
- Delivery to `[deliveries]/ib-blind_hd-s_2026-10-23/`, plus a one-line pointer to the session-R lead.
- Nothing is sent anywhere else.

## 10. Time estimate for phase 2

About **6 h of seat time**:
- about 3 h to write and drill the code: Part N about 1 h, Part C/E verifier about 1.5 h, controls and tampers
  about 0.5 h;
- about 2 h of runs, mostly overlapping the coding;
- about 1 h for the write-up and delivery.

Node compute stays within the 5 h wall budget of §5.
