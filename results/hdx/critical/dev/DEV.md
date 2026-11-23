# HD-X-2: development notes for the registration (not registered)

*2026-10-26, a fork of the bh-modes lead, for the lead's PREREG of HD-X-2 (`results/hdx/critical/PREREG.md`, to be
written). Branch `hdx-2` from `fd25e00`, in a local clone; the patches are in `[workdir]/hdx2-dev/patches/`. The final code is at `ca28c8b`. The design
rule comes from the planning pilot (`[workdir]/hdx2-pilot/NOTE.md`, not registered).*

## The files

- **`code/hdx/critical.py`**, the certificate: one job per band (`--band D,L`), with `--control`. It is fail-closed and
  writes a record per RULES.md D.
  - **The design**, fixed by rule: P = −ν − ℓy/((z + ε)R) − (1 − z)H_z/H + cμ. Here ε = ε̂w/(1 + w), ε̂ is the midpoint of
    (1/k, 2/(k − ℓ)), and c = 1/4.
  - **NL** = N·S²R²L, built from hd.scert.exact_parts. It is checked on four charts after exact divisions: O and O′
    (M = NL/μ), T (NL(μζ, μ)/μ²) and C (NL(z, zσ)/(z²σ)).
  - **Gates, in the record's order:** KAT, E0n, PARAM, H, S, R, L, COVER, Z0, DIV-O, DIV-T, DIV-C, THROAT, CORNER,
    FIRST, INF, XN, then POS-O, POS-O′, POS-T and POS-C. The nc-bound control adds (a) and (b).
  - **`gates()`** runs everything before the POS charts. `run()` calls it, and the development tests call it on S5's
    potential.
- **`code/hdx/kitcheck.py`**, the kit's verdict matcher. It accepts three forms: `=exact`, `^prefix`, and
  `+required|allowed` (a REJECT that is not an exception, whose failed checks include the required ones and lie within
  required ∪ allowed).
- **`code/hdx/devtest_critical.py`**, the development tests (§3).
- **`kit/hdx/run_critical.sh`**, the one-command re-run, in kit/hdx/run_elementary.sh's style.
  - It checks the environment (flint 0.9.0, FLINT 3.6.0, sympy 1.14.0, gmpy2 2.3.2).
  - It honours BHM_ARCHIVE, BHM_COMMIT and BHM_REF (compare_runs per job). BHM_JOBS sets the parallelism (default 8).
  - It runs 35 jobs: the 9 bands with control none, and the 13 controls on D = 7 ℓ = 2 and on D = 11 ℓ = 4.
  - Its table of registered forms is read back by the devtest, and must equal the devtest's SPECS.

## 1. Per-band constants (for the PREREG)

Common to every band: c = 1/4; Z1 = 1/4, ZT = 8, SIG1 = 1/8, MUT = 1/32; MU_C = 1/64, the charge point of nc-bound and
d6; MAX_DEPTH = 40; XN uses 24 seeded points (seed 1000n + ℓ) plus (1/4, 1/32), (1/1000, 1/1000) and (999/1000, MU1).

| D, l | k | nu | a = -l/k | window (1/k, 2/(k - l)) | ehat | eps = eps_n/eps_d | MU1 | q(MU1)^2 | deg NL, M, T, K |
|---|---|---|---|---|---|---|---|---|---|
| 7, 2 | 4 | 7/2 | -1/2 | (1/4, 1) | 5/8 | (5*mu)/(mu**2 + 8*mu + 7) | 1/8 | 197505/201601 | (24, 14), (24, 13), (24, 36), (36, 13) |
| 8, 2 | 5 | 4 | -2/5 | (1/5, 2/3) | 13/30 | (39*mu)/(10*mu**2 + 90*mu + 80) | 13/100 | 698908729/714118729 | (30, 14), (30, 13), (30, 42), (42, 13) |
| 9, 2 | 6 | 9/2 | -1/3 | (1/6, 1/2) | 1/3 | (10*mu)/(3*mu**2 + 30*mu + 27) | 13/100 | 7961448561/8130448561 | (36, 14), (36, 13), (36, 48), (48, 13) |
| 9, 3 | 6 | 11/2 | -1/2 | (1/6, 2/3) | 5/12 | (5*mu)/(2*mu**2 + 12*mu + 10) | 3/25 | 2404864/2455489 | (36, 14), (36, 13), (36, 48), (48, 13) |
| 10, 2 | 7 | 5 | -2/7 | (1/7, 2/5) | 19/70 | (209*mu)/(70*mu**2 + 770*mu + 700) | 13/100 | 9829338561/10033828561 | (42, 14), (42, 13), (42, 54), (54, 13) |
| 10, 3 | 7 | 6 | -3/7 | (1/7, 1/2) | 9/28 | (117*mu)/(56*mu**2 + 364*mu + 308) | 3/25 | 46562824/47513449 | (42, 14), (42, 13), (42, 54), (54, 13) |
| 11, 2 | 8 | 11/2 | -1/4 | (1/8, 1/3) | 11/48 | (11*mu)/(4*mu**2 + 48*mu + 44) | 13/100 | 1321538729/1348578729 | (48, 14), (48, 13), (48, 60), (60, 13) |
| 11, 3 | 8 | 13/2 | -3/8 | (1/8, 2/5) | 21/80 | (147*mu)/(80*mu**2 + 560*mu + 480) | 1/8 | 2961/3025 | (48, 14), (48, 13), (48, 60), (60, 13) |
| 11, 4 | 8 | 15/2 | -1/2 | (1/8, 1/2) | 5/16 | (5*mu)/(3*mu**2 + 16*mu + 13) | 3/25 | 1015861/1038361 | (48, 14), (48, 13), (48, 60), (60, 13) |

| D, l | H(2) | L(0) | R(0) | eps_d(0) | w'(0) | C0 | T(zeta, 0) = K(0, 0) zeta + T(0, 0) |
|---|---|---|---|---|---|---|---|
| 7, 2 | 42 | 49 | 4 | 7 | 8/7 | 387072 | 14869757952*zeta + 5310627840 |
| 8, 2 | 56 | 64 | 5 | 80 | 9/8 | 2107392/5 | 4315938816000*zeta + 1578015129600 |
| 9, 2 | 72 | 81 | 6 | 27 | 10/9 | 491520 | 1044855521280*zeta + 386983526400 |
| 9, 3 | 90 | 25 | 6 | 10 | 6/5 | 2799360 | 251942400000*zeta + 62985600000 |
| 10, 2 | 90 | 100 | 7 | 700 | 11/10 | 4105728/7 | 1408264704000000*zeta + 525584505600000 |
| 10, 3 | 110 | 121 | 7 | 308 | 13/11 | 20592000/7 | 1654563246336000*zeta + 419012770176000 |
| 11, 2 | 110 | 121 | 8 | 44 | 12/11 | 704000 | 10554638336000*zeta + 3957989376000 |
| 11, 3 | 132 | 36 | 8 | 480 | 7/6 | 16099776/5 | 1709286170296320*zeta + 436224074711040 |
| 11, 4 | 156 | 169 | 8 | 13 | 16/13 | 11501568 | 21023762153472*zeta + 4043031183360 |

The second table is what THROAT, CORNER and FIRST check (`gates()` on S5's potential, at `9f88f7b`, host-2). T(ζ, 0) is
linear, and K(0, σ) = T₁ + T₀σ.

## 2. The controls: registered forms, and why each can fail

| control | change | registered form (kit) | why it can fail, i.e. what a wrong verifier would let through |
|---|---|---|---|
| none | — | `=VERIFIED` | — |
| nc-ehat-low | ε̂ = 1/k − 1/20 | `+POS-C\|POS-O,POS-O',POS-T` | K(0, 0) = C₀(…) < 0 exactly. A verifier that never tests the C chart's corner would pass |
| d0-corner | ε̂ = 1/k | `+POS-C\|…` | K(0, 0) = 0 exactly. Only the strictness of the check refuses it |
| nc-ehat-high | ε̂ = 2/(k − ℓ) + 1/8 | `+POS-T\|POS-O,POS-O',POS-C` | T(0, 0) < 0 exactly, at the T chart's corner |
| d0-throat | ε̂ = 2/(k − ℓ) | `+POS-T\|…` | T(0, 0) = 0 exactly. Strictness only |
| nc-Q0 | c = 0 | `+INF,POS-O\|POS-O',POS-T,POS-C` | N(1, μ) ≡ 0. INF's positivity clause and POS-O's edge z = 1 must refuse it |
| nc-Qneg | c = −1/4 | `+INF,POS-O\|…` | N(1, μ) < 0 for μ > 0 |
| td-nu | ν + 1/100 in P | `+Z0,DIV-O,DIV-C,CORNER,FIRST,INF,POS-O,POS-O',POS-C\|POS-T` | NL(z, 0) ≠ 0. DIV-T still holds (S² carries μ²), so POS-T may run |
| d6 | NL − K6μ²(z − μ)(3μ − z)(1 − z) | `+POS-T\|POS-O,POS-O',POS-C` | It keeps Z0, every division, THROAT, CORNER, FIRST and INF (it vanishes at μ = 0 and at z = 1), and XN, which is computed before the defect. Only the POS charts at μ > 0 can catch it, and T(2, MU_C) < 0 by construction |
| nc-bound | W − Kb at μ = MU_C, with b inside U₋ < 0 | `=REJECT: nc-bound (b)` | (a) needs the support inside the U₋ < 0 region near the horizon (exact) and Q[b] < 0 (Arb). (b) must refuse the planted NL on the support; a design that ignored the potential would pass |
| td-coeff | U₋ + 16nm² | `+E0n,Z0,DIV-O,DIV-C,THROAT,CORNER,FIRST,INF,POS-O,POS-O',POS-C\|POS-T` | the transcription gate E0n. XN passes, because both of its routes use the tampered U |
| td-verifier | acceptance lo > −1 | `=REJECT: KAT` | the KATs alone. Every positivity gate passes under the lenient verifier |
| td-cover | SIG1 = 1/16 | `=REJECT: COVER` | ZT·SIG1 = 1/2 < 1. POS-C on the smaller box passes |
| td-div | T by μ³, C by z³σ | `+DIV-T,DIV-C,THROAT,CORNER,FIRST,POS-T,POS-C\|POS-O,POS-O'` | the divisions. THROAT, CORNER and FIRST have no chart to read |

**Why some forms use `+`.** The POS charts are never run on S5's potential before registration. So a control's
complete failure set is registered as its required checks, plus the POS charts it may also fail. The non-POS failures
are predicted exactly. The devtest checks them on S5's potential at both kit bands, through gates(), and on the
synthetic potential through main().

## 3. The development tests

- **Log:** `host-1:[run-folder]/hdx2-dev/devtest-<commit>.log`, run from a `git archive` of the commit, under
  `nice -n 19`. The run of the final commit, `ca28c8b`, gave 144/144 and DEVTEST PASS in 74 s (host-1, 21:06 EDT): `devtest-ca28c8b.log`, beside this file (SHA-256 `0054fd791672023045561eaac77f9bb25be7c8ababc00b8311380218dcf4ecad`). The
  earlier run at `9f88f7b` (109/118) failed only on the devtest's own expectation of the record's key order (the JSON is
  written with sorted keys); `00d17ca` fixed that test.
- **The synthetic potential.** H_syn = m + (1 + mδ)x, and U_syn(x) is built so that the band's design is exact at μ = 0,
  so Z0 holds by construction. The synthetic UH accepts only int n and ℓ (the BHM-124 lesson).
  - main() runs end to end on it, POS charts included, at D = 7 ℓ = 2, D = 9 ℓ = 2 and D = 11 ℓ = 4: VERIFIED.
  - Every control runs at D = 7 ℓ = 2 and D = 11 ℓ = 4, judged by the kit's matcher, with its non-POS failures exact.
- **S5's potential,** through gates() and with no POS chart:
  - every gate passes for all 9 bands with control none;
  - at both kit bands, every control fails exactly its predicted non-POS gates;
  - nc-bound's part (a), the support and the certified Q[b] < 0, runs at both kit bands.
  - POS-O, POS-O′, POS-T, POS-C and nc-bound's part (b) never run on S5's potential.
- **Also tested:** the record writer and compare_runs (IDENTICAL after masking); parse_band; the typed UH; the KATs and
  their tamper; kitcheck.
- **The kit's control flow**, with a stub interpreter (`[workdir]/hdx2-dev/kitstub/fakepy`, host-1). The stub fakes
  hdx.critical's records with verdicts in each registered form and passes everything else to the venv's Python.
  - `bash -n` passes.
  - All 35 jobs give KIT PASS.
  - With BHM_REF set to that output: compare_runs is IDENTICAL, and KIT PASS.
  - With one wrong verdict (d6 at D = 11 ℓ = 4 as "REJECT: POS-O"): KIT FAIL, and kitcheck prints NO MATCH.
  - The kit itself has not run on S5's potential: that would run the POS charts.

## 4. Open questions for the registration

1. **The tortoise map onto ℝ at q = 1, at general n.** It is pencil, and so far audited only at n = 4 (BHM-116). The
   PREREG has to write it out at general n. Here it is needed only at q = 1, which is Z's part.
2. **The reduction for μ > 0.** P is C^∞ on [0, 1]: its poles are at z = −ε, at R's zeros (|1 − z| = 1, z ≠ 0) and at
   H's zeros, all off [0, 1]. Proposition 3 (prop3_Dn) then applies for each μ ∈ (0, MU1]. The PREREG should state this.
3. **The claim's range** is q ∈ [q(MU1), 1). With Z it extends to q = 1, and with Theorem HD to (0, 1]. There is
   no known answer, as for A2. The synthetic potential is a planted exact case, not a known answer.
4. **The planning saw these designs' chart values on grids and their μ → 0 edges exactly** (the pilot's NOTE). The
   PREREG should say so, as A2-PILOT's did.
5. **Runtime.** On the synthetic potential each job takes seconds. On S5's potential the POS charts have degrees up to
   (48, 60) (T) and (60, 13) (K) at D = 11. The kit's wall time is unknown until the run of record; it is expected to
   be minutes.
6. **nc-bound's support and K** come from a rule (the first root of U₋ at MU_C, the support (z_U/5, 4z_U/5) rounded
   inward to 1/10000, and K = ceil(2I₁/I₂)), not from registered numbers. On S5's potential, part (a) gives:

   | band | support | K | I₁ (float) | Q[b] (Arb) |
   |---|---|---|---|---|
   | D = 7, ℓ = 2 | [21/1000, 837/10000] | 301062550 | 2.901·10⁻¹² | [−2.900610727e-12 ± 1.90e-23] |
   | D = 11, ℓ = 4 | [257/10000, 41/400] | 346269974 | 4.661·10⁻¹¹ | [−4.660852684e-11 ± 8.10e-22] |

   I₁ > 0 in both, as it must be if the claim holds: I₁ is the unplanted trial energy, and I₁ ≤ 0 would be a K1 event.
7. **The verdict string** follows the registered order (C.ORDER), and the kit's `^`/`=` forms rely on it. The record's
   JSON, though, is written with sorted keys.
8. **This file, the draft PREREG and the devtest log** are in `results/hdx/critical/dev/`, in the last patch, for the lead to keep or drop. *(The lead kept them; at registration, BHM-143, the draft became `results/hdx/critical/PREREG.md`, with the lead's changes.)*
