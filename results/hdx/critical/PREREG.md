# PREREG — HD-X-2: the critical bands of D = 7–11 through extremality, by route (iii)

*Item BHM-143. 2026-10-26, the bh-modes lead. Step HD-X-2 of `TARGET_HD_ADDENDUM_2.md` (BHM-121, with BHM-122's dates),
under the operator's rulings BHM-120 and BHM-140 (item 1). The planning pilot qualified on 2026-10-26
(`results/planning/hdx2_pilot_2026-10-26/NOTE.md`), so the frame's kill does not apply.*
- *Registered before any POS chart of this code has run on S5's potential at a claimed band.*
- **Not blind,** in three respects:
  - The planning pilot (floats) saw these designs' four charts positive on grids, the rungs positive, and the three
    μ → 0 edges positive exactly. It did so for D = 7 ℓ = 2 and D = 8 ℓ = 2 in detail, and for all 9 bands with the same
    rule.
  - The development tests (§5) ran every gate before the POS charts on S5's potential, at all 9 bands. They also ran
    nc-bound's part (a) at D = 7 ℓ = 2 and D = 11 ℓ = 4.
  - So the values of THROAT, CORNER and FIRST were seen (§3's table).
- *The code was written by a fork of the lead (BHM-140) and read by the lead (the design, NL, the charts and their
  divisions, every gate, the controls, nc-bound and the kit). The files are `code/hdx/critical.py`,
  `code/hdx/kitcheck.py`, `code/hdx/devtest_critical.py` and `kit/hdx/run_critical.sh`, at the commit that holds this
  file.*
- *The lead's one change before registration: `nice -n 19` on the kit's three Python calls that lacked it (the
  environment check, `hdx.kitcheck` and `compare_runs.py`; RULES.md B3). The fork's development notes are in `dev/DEV.md`
  beside this file. Sealed; any change before the run is a dated addendum.*

## 1. The claim

> **HD-X-2.** For each (D, ℓ) in the critical set 𝒦 and every q ∈ [q(MU1), 1), A_{ℓ,q} ≥ 0 on C₀^∞(ℝ). 𝒦 is
> D = 7 ℓ = 2; D = 8 ℓ = 2; D = 9 ℓ = 2, 3; D = 10 ℓ = 2, 3; D = 11 ℓ = 2, 3, 4: the bands with 2ℓ ≤ n − 1.
> - Each band's MU1 has q(MU1) ≤ 99/100, checked exactly.
> - With Z (BHM-126) at q = 1 and Theorem HD for q ≤ 99/100, A_{ℓ,q} ≥ 0 for every q ∈ (0, 1] on these bands.
> - With HD-X outside 𝒦 (HD-X-E, BHM-128; HD-X-S, BHM-132; Lemma U(n)), that completes D = 7–11 for every ℓ ≥ 2 and
>   every q ∈ (0, 1] (Theorem HD-X).

The physical reading is as for A1: S5's reduction (*cited*). There is no known answer, as for A2; the synthetic
potential of §5 is a planted exact case, not a known answer.

## 2. Method (exact; HD-E's parametrisation `hd.elementary.param_n`, μ = 0 at q = 1)

Units r_H = 1, z = 1 − 1/ρ, k = n − 1 and y = (1 − z)^k.

**The design** is fixed by rule, with no fit:

  P(z, μ) = −ν − ℓy/((z + ε)R(z)) − (1 − z)H_z/H + cμ, where
- ν = ℓ + n/2 − 1;
- R = (1 − y)/z, a polynomial;
- H = H₋(x_H y), with param_n's (m, δ);
- ε = ε̂w/(1 + w) = ε_n/ε_d;
- ε̂ = (1/k + 2/(k − ℓ))/2, the midpoint of the throat window (1/k, 2/(k − ℓ));
- c = 1/4.

At μ = 0, P = (1 − z)(log u₀)_z for Z's zero mode u₀ = ρ^{−ν}(1 − y)^{−ℓ/k}/((ℓ − 1) + ny), so N(z, 0) ≡ 0.

**The certificate polynomial.** With S = ε_d z + ε_n, D = S·R·Hn and Π = P·D,

  NL := N S²R²L = Un Hd² fd S²R² − 64 Ud [(1 − z) fzn Π D + fn(−Π D + (1 − z)(Π_z D − Π D_z) + Π²)],

where L = Ud·Hd²·fd and U = Un/Ud, H = Hn/Hd and f = fn/fd (`hd.scert.exact_parts`; Ud, Hd and fd depend on μ only).
N = U − 64H²[(1 − z)f_z P + f(−P + (1 − z)P_z + P²)] is the functional of HD-S and HD-X-S (`hd.scert.Exact.NL`).

**The charts.** Each comes after an exact division:

| chart | variables | box | the polynomial that must be > 0 |
|---|---|---|---|
| O | (z, μ) | [1/4, 1] × [0, MU1] | M = NL/μ |
| O′ | (z, μ) | [0, 1/4] × [1/32, MU1] | M |
| T | z = μζ | [0, 8] × [0, 1/32] | T = NL(μζ, μ)/μ² |
| C | μ = zσ | [0, 1/4] × [0, 1/8] | K = NL(z, zσ)/(z²σ) |

COVER: ZT·SIG1 = 1, ZT·MUT = 1/4 = Z1, and Z1·SIG1 = 1/32 ≤ MU1. So every (z, μ) ∈ (0, 1) × (0, MU1] lies in a chart:
O if z ≥ 1/4; O′ if z < 1/4 and μ ≥ 1/32; T if z ≤ 8μ < 1/4; and C if 8μ < z < 1/4. There NL > 0.

**The reduction** (pencil; the same as HD-X-S's, `TARGET_HD_ADDENDUM_2.md` §3):
- Fix μ ∈ (0, MU1]. P is C^∞ on [0, 1]. Its poles are at z = −ε < 0 (gate S); at R's zeros, where |1 − z| = 1 and
  z ≠ 0, none in [0, 1] (gate R); and at H's zeros, with H > 0 on [0, 1] (gate H).
- S, R and L are > 0 there (gates S, R and L), so NL > 0 gives N > 0 on (0, 1).
- So A_{ℓ,q} ≥ 0 by Proposition 3 for P that is C¹ on (0, 1) (*machine-checked*, `prop3_Dn`, BHM-091, every n ≥ 2).
  It is applied at q = q(μ) < 1. The image of [0, MU1] under the continuous q(μ), with q(0) = 1, contains [q(MU1), 1].
- For 0 < q < 1, the tortoise map onto ℝ is the standard one. f > 0 on the exterior, with a simple zero at the
  horizon, so r* = ∫dr/f is a C^∞ diffeomorphism (1, ∞) → ℝ (pencil; item A2 of Fable's audit, BHM-141).
- q = 1 itself is Z's (BHM-126; its tortoise map is *machine-checked*, `tortoise_q1`, BHM-135).

## 3. Gates (in the record's order)

| gate | what is checked |
|---|---|
| KAT | the verifier's known-answer tests (`a1.p1.kats`) |
| E0n | S5's U₋, H₋ at n = 2…12 equal Kimi's independent transcription (HD-E's gate) |
| PARAM | param_n's identities; q(0)² = 1; x_H(0) = 2; δ(0) = 1/((ℓ + n)(n + 1)); ε_n/ε_d = ε̂w/(1 + w); q(MU1)² ≤ (99/100)²; w increasing on [0, 1] |
| H | every coefficient of H₋ in (x, δ, m) is > 0, and δ > 0 on [0, MU1] |
| S | ε_n(0) = 0; ε_n/μ > 0 and ε_d > 0 on [0, MU1] |
| R | R > 0 on [0, 1] |
| L | L > 0 on [0, MU1] |
| COVER | as in §2 |
| Z0 | NL(z, 0) ≡ 0: the zero-mode identity in this formulation |
| DIV-O, DIV-T, DIV-C | μ \| NL; μ² \| NL(μζ, μ); z²σ \| NL(z, zσ) |
| THROAT | T(ζ, 0) = 64k²H(2)²L(0)R(0)²ε_d(0)²w′(0)²·β(ζ/w′(0)), with β(s) = 2a²(ε̂ − 1/k)s + aε̂((a + 1)ε̂ − 2/k) and a = −ℓ/k |
| CORNER | K(0, σ) = σT(1/σ, 0), i.e. T₁ + T₀σ |
| FIRST | M(z, 0) = O(z), and K(0, 0) = M_z(0, 0) = C₀ε_d(0)²R(0)²L(0), with C₀ = 128H(2)²ℓ²w′(0)(ε̂ − 1/k) |
| INF | NL(1, μ) = 64m²((2ν + 1)cμ − c²μ²)S(1, μ)²L(μ); R(1) = 1; c > 0 and 2ν + 1 > c·MU1 |
| XN | NL/(S²R²L) equals N computed directly (U, H, the unfactored f and P's definition, P_z by sympy), exactly, at 24 seeded points (seed 1000n + ℓ) and (1/4, 1/32), (1/1000, 1/1000), (999/1000, MU1) |
| POS-O, POS-O′, POS-T, POS-C | exact Bernstein bisection (`onset.bernstein.prove_sign`, MAX_DEPTH 40) on the four closed boxes; a chart whose division failed is a failed check, not run |

β's window is the design's: T₁ > 0 iff ε̂ > 1/k, and T₀ > 0 iff ε̂ < 2/(k − ℓ) (with a < 0 and a + 1 > 0).

**The per-band constants,** with the values of THROAT, CORNER and FIRST seen in development (gates() on S5's potential):

| D, ℓ | k | ν | a | ε̂ | ε | MU1 | q(MU1)² | deg NL; M; T; K | T(ζ, 0) = T₁ζ + T₀ |
|---|---|---|---|---|---|---|---|---|---|
| 7, 2 | 4 | 7/2 | −1/2 | 5/8 | 5μ/(μ² + 8μ + 7) | 1/8 | 197505/201601 | (24, 14); (24, 13); (24, 36); (36, 13) | 14869757952ζ + 5310627840 |
| 8, 2 | 5 | 4 | −2/5 | 13/30 | 39μ/(10μ² + 90μ + 80) | 13/100 | 698908729/714118729 | (30, 14); (30, 13); (30, 42); (42, 13) | 4315938816000ζ + 1578015129600 |
| 9, 2 | 6 | 9/2 | −1/3 | 1/3 | 10μ/(3μ² + 30μ + 27) | 13/100 | 7961448561/8130448561 | (36, 14); (36, 13); (36, 48); (48, 13) | 1044855521280ζ + 386983526400 |
| 9, 3 | 6 | 11/2 | −1/2 | 5/12 | 5μ/(2μ² + 12μ + 10) | 3/25 | 2404864/2455489 | (36, 14); (36, 13); (36, 48); (48, 13) | 251942400000ζ + 62985600000 |
| 10, 2 | 7 | 5 | −2/7 | 19/70 | 209μ/(70μ² + 770μ + 700) | 13/100 | 9829338561/10033828561 | (42, 14); (42, 13); (42, 54); (54, 13) | 1408264704000000ζ + 525584505600000 |
| 10, 3 | 7 | 6 | −3/7 | 9/28 | 117μ/(56μ² + 364μ + 308) | 3/25 | 46562824/47513449 | (42, 14); (42, 13); (42, 54); (54, 13) | 1654563246336000ζ + 419012770176000 |
| 11, 2 | 8 | 11/2 | −1/4 | 11/48 | 11μ/(4μ² + 48μ + 44) | 13/100 | 1321538729/1348578729 | (48, 14); (48, 13); (48, 60); (60, 13) | 10554638336000ζ + 3957989376000 |
| 11, 3 | 8 | 13/2 | −3/8 | 21/80 | 147μ/(80μ² + 560μ + 480) | 1/8 | 2961/3025 | (48, 14); (48, 13); (48, 60); (60, 13) | 1709286170296320ζ + 436224074711040 |
| 11, 4 | 8 | 15/2 | −1/2 | 5/16 | 5μ/(3μ² + 16μ + 13) | 3/25 | 1015861/1038361 | (48, 14); (48, 13); (48, 60); (60, 13) | 21023762153472ζ + 4043031183360 |

The constants common to every band: c = 1/4, Z1 = 1/4, ZT = 8, SIG1 = 1/8, MUT = 1/32, and MU_C = 1/64 (nc-bound's
and d6's charge point).

## 4. Controls (run on D = 7 ℓ = 2 and D = 11 ℓ = 4; registered forms as the kit matches them, `code/hdx/kitcheck.py`)

The forms: `=` exact; `^` prefix; `+A,B|C` a REJECT, not an exception, whose failed checks include A and B and lie
within {A, B, C}. The `+` forms are needed because the POS charts have never run on S5's potential before
registration. Each control's non-POS failures are predicted exactly; the development test checked them on S5's
potential at both bands.

| control | change | registered form | why it can fail |
|---|---|---|---|
| none | — | `=VERIFIED` | — |
| nc-ehat-low | ε̂ = 1/k − 1/20 | `+POS-C\|POS-O,POS-O',POS-T` | K(0, 0) < 0 exactly: the C chart's corner must be tested |
| d0-corner | ε̂ = 1/k | `+POS-C\|POS-O,POS-O',POS-T` | K(0, 0) = 0 exactly: only strictness refuses it |
| nc-ehat-high | ε̂ = 2/(k − ℓ) + 1/8 | `+POS-T\|POS-O,POS-O',POS-C` | T(0, 0) < 0 exactly |
| d0-throat | ε̂ = 2/(k − ℓ) | `+POS-T\|POS-O,POS-O',POS-C` | T(0, 0) = 0 exactly: strictness |
| nc-Q0 | c = 0 | `+INF,POS-O\|POS-O',POS-T,POS-C` | N(1, μ) ≡ 0 |
| nc-Qneg | c = −1/4 | `+INF,POS-O\|POS-O',POS-T,POS-C` | N(1, μ) < 0 for μ > 0 |
| td-nu | P's −ν shifted by −1/100 | `+Z0,DIV-O,DIV-C,CORNER,FIRST,INF,POS-O,POS-O',POS-C\|POS-T` | NL(z, 0) ≠ 0 |
| d6 | NL − K6μ²(z − μ)(3μ − z)(1 − z), K6 = 2T(2, MU_C)/(MU_C²(1 − 2MU_C)) | `+POS-T\|POS-O,POS-O',POS-C` | It keeps every identity, and XN is computed before the defect. Only a POS chart at μ > 0 catches it (the planted T(2, MU_C) = −T(2, MU_C) of the design < 0) |
| nc-bound | W − Kb at μ = MU_C, b = ((z − za)(zb − z))² | `=REJECT: nc-bound (b)` | (a) the support lies inside the horizon's U₋ < 0 region (exact; BHM-106 §5), and Q[b] < 0 is certified in Arb. (b) The planted NL must be refused on [za, zb] |
| td-coeff | U₋ + 16nm² | `+E0n,Z0,DIV-O,DIV-C,THROAT,CORNER,FIRST,INF,POS-O,POS-O',POS-C\|POS-T` | the transcription gate (XN passes: both routes are tampered) |
| td-verifier | acceptance lowered to lo > −1 | `=REJECT: KAT` | the KATs alone |
| td-cover | SIG1 = 1/16 | `=REJECT: COVER` | ZT·SIG1 < 1 |
| td-div | T by μ³, C by z³σ | `+DIV-T,DIV-C,THROAT,CORNER,FIRST,POS-T,POS-C\|POS-O,POS-O'` | the divisions |

- **The exact forms of td-verifier, td-cover and nc-bound assume that the band's own POS charts pass.** So the controls
  of a kit band are judged only if that band's `none` job is VERIFIED. If it is not, that band's controls are VOID (as
  in HD-X-S, BHM-131 §4), and the other kit band's controls still stand. The kit itself reports KIT FAIL in that case,
  since a band is not VERIFIED.
- **nc-bound's support and K** come from a rule, not from registered numbers:
  - the support is (z_U/5, 4z_U/5), rounded inward to 1/10000, where z_U is the first root of U₋ at MU_C;
  - K = ⌈2I₁/I₂⌉.
  
  The development test gave these values on S5's potential, as information:
  - D = 7 ℓ = 2: support [21/1000, 837/10000], K = 301062550, Q[b] = −2.90·10⁻¹²;
  - D = 11 ℓ = 4: support [257/10000, 41/400], K = 346269974, Q[b] = −4.66·10⁻¹¹.
  
  I₁, the unplanted trial energy, was > 0 at both (2.90·10⁻¹² and 4.66·10⁻¹¹, floats). The record of the run must show
  the same support and K.

## 5. Development tests (`code/hdx/devtest_critical.py`)

- **The synthetic potential.** H_syn = m + (1 + mδ)x, and U_syn is built so that the design is exact at μ = 0. The
  synthetic UH accepts only int n and ℓ (BHM-124).
  - main() runs end to end: VERIFIED at D = 7 ℓ = 2, D = 9 ℓ = 2 and D = 11 ℓ = 4.
  - Every control runs at D = 7 ℓ = 2 and D = 11 ℓ = 4. Each is matched by the kit's own matcher, with its non-POS
    failures exact and the verdict in the registered order.
- **S5's potential, through gates(), with no POS chart:**
  - every gate passes at all 9 bands;
  - at both kit bands, each control's non-POS failures are exactly §4's;
  - nc-bound's part (a) certifies Q[b] < 0 at both kit bands (§4).
- **Also tested:**
  - the record writer and compare_runs;
  - parse_band;
  - the KATs and their tamper;
  - kitcheck, and that the kit's table of forms equals the devtest's;
  - the kit's control flow, with a stub interpreter: KIT PASS, and KIT FAIL on one wrong verdict.
- **Runs.**
  - The fork: 144/144 at `ca28c8b` (host-1), on the code as registered except the kit's `nice` change. Log:
    `dev/devtest-ca28c8b.log`.
  - The lead's re-run at `d998220`, which holds this file's code with the kit's change (host-2, under `nice -n 19`):
    144/144 as expected in 71 s, DEVTEST PASS. Log: `devtest-d998220.log` beside this file.
  - The lead's re-run of the kit's stub flow test at `d998220` (host-2, the fork's stub `fakepy`, `b51bc895…`):
    - KIT PASS;
    - KIT FAIL with one wrong verdict (d6 at D = 11 ℓ = 4 as `REJECT: POS-O`: NO MATCH);
    - with `BHM_REF` set to the first output, 35 of 35 IDENTICAL, and KIT PASS;
    - `bash -n` passes on host-2.
    
    Logs: `dev/kitstub-d998220-{ok,bad,ref}.log`.

## 6. Runs, hosts, records

- **One command:** `kit/hdx/run_critical.sh`, with 35 jobs: the 9 bands with control none, and the 13 controls on
  D = 7 ℓ = 2 and D = 11 ℓ = 4.
  - KIT PASS only if every band is VERIFIED and every control matches its form.
  - It checks the environment (flint 0.9.0, FLINT 3.6.0, sympy 1.14.0, gmpy2 2.3.2).
  - BHM_JOBS sets the parallelism (default 8). It does not change any result.
- **Hosts.**
  - The record is on host-1, from a `git archive` of the commit that holds this file, under `nice -n 19` in
    `[venv]`.
  - The reproduction is on host-2, with `BHM_REF` set to the record: every job IDENTICAL after masking.
  - The records carry the UTC start and the archive's SHA-256 (BHM_ARCHIVE).
- **Time:** minutes are expected, but this is unmeasured. Synthetic jobs of similar degree take 1–5 s each. On S5's
  potential the POS charts have degree up to (48, 60) for T and (60, 13) for K. Timeout: 6 h per job; a timeout is VOID.

## 7. Outcomes (registered now)

- **Every band VERIFIED, every control in its form, KIT PASS:** HD-X-2 is *certified* (exact) for the 9 bands on
  [q(MU1), 1).
  - The reduction is proved (pencil): P's smoothness and the covering logic, as for HD-X-S. Proposition 3 is
    *machine-checked* (Lean).
  - With Z, Theorem HD, HD-X-E, HD-X-S and Lemma U(n), **Theorem HD-X** follows: for D = 7–11, every ℓ ≥ 2 and every
    q ∈ (0, 1], A_{ℓ,q} ≥ 0.
  - A second party is pending (RULES.md A4): Kimi, by a brief, at the stage-3 report.
- **A band REJECT (in a POS chart or any other gate):** that band is reported as it stands. It is not certified by
  this design and not refuted, since the reduction runs one way only. K4 applies to it (`TARGET_HD_ADDENDUM_2.md` §6),
  and a redesign needs a new registration. If it is a kit band, its controls are VOID (§4). The other bands stand on
  their own jobs.
- **Any exception or timeout, or a control off its form at a kit band whose `none` job is VERIFIED:** VOID. A dated
  addendum and a re-run follow.
- **A certified Q[φ] < 0 for the unplanted potential** (K1) would refute the band. Nothing here computes one:
  nc-bound's I₁ is the unplanted trial energy, and it was > 0 at both kit bands.
