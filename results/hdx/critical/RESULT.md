# RESULT — HD-X-2: the critical bands of D = 7–11 through extremality

*Item BHM-144. 2026-10-26, the bh-modes lead. Registration: `PREREG.md` (BHM-143). Sealed.*

## Verdict: VERIFIED as registered, KIT PASS

- **The record:** host-1 at `6cedd44`, from its `git archive` (SHA-256 `249b819a0b15ec1a…`), 01:52:14–01:52:52 UTC
  (21:52–21:53 EDT on 2026-10-26).
  - BHM_JOBS = 4, since host-1 was also running the D ≥ 12 screen's record and the [another line of this project] fork's jobs. The
    parallelism changes no result.
- **The reproduction:** host-2, with `BHM_REF` set to the record, 01:53:40–01:53:52 UTC. KIT PASS, and all 35 jobs are
  IDENTICAL after masking.
- **All 9 bands are VERIFIED.** Every gate holds in every band: KAT, E0n, PARAM, H, S, R, L, COVER, Z0, DIV-O, DIV-T,
  DIV-C, THROAT, CORNER, FIRST, INF, XN, POS-O, POS-O′, POS-T and POS-C.
- **Every chart is positive at the first Bernstein node** in every band: one leaf per chart, with no bisection. The exact
  least Bernstein coefficients are in each record's `min_bernstein`.

| D, ℓ | MU1 | q(MU1)², each ≤ (99/100)² | deg NL (z, μ) | `none` | time |
|---|---|---|---|---|---|
| 7, 2 | 1/8 | 197505/201601 | (24, 14) | VERIFIED | 1.9 s |
| 8, 2 | 13/100 | 698908729/714118729 | (30, 14) | VERIFIED | 2.7 s |
| 9, 2 | 13/100 | 7961448561/8130448561 | (36, 14) | VERIFIED | 2.8 s |
| 9, 3 | 3/25 | 2404864/2455489 | (36, 14) | VERIFIED | 2.2 s |
| 10, 2 | 13/100 | 9829338561/10033828561 | (42, 14) | VERIFIED | 2.9 s |
| 10, 3 | 3/25 | 46562824/47513449 | (42, 14) | VERIFIED | 2.9 s |
| 11, 2 | 13/100 | 1321538729/1348578729 | (48, 14) | VERIFIED | 3.6 s |
| 11, 3 | 1/8 | 2961/3025 | (48, 14) | VERIFIED | 2.8 s |
| 11, 4 | 3/25 | 1015861/1038361 | (48, 14) | VERIFIED | 3.0 s |

**The controls,** on D = 7 ℓ = 2 and D = 11 ℓ = 4. Each ends in its registered form (PREREG §4), as `hdx.kitcheck` found
in both runs.

| Control | D = 7 ℓ = 2 | D = 11 ℓ = 4 | Registered form |
|---|---|---|---|
| nc-ehat-low | REJECT: POS-O, POS-O′, POS-T, POS-C | the same | `+POS-C\|POS-O,POS-O',POS-T` |
| d0-corner | REJECT: POS-O, POS-O′, POS-T, POS-C | the same | `+POS-C\|POS-O,POS-O',POS-T` |
| nc-ehat-high | REJECT: POS-T | REJECT: POS-O′, POS-T | `+POS-T\|POS-O,POS-O',POS-C` |
| d0-throat | REJECT: POS-T | REJECT: POS-T | `+POS-T\|POS-O,POS-O',POS-C` |
| nc-Q0 | REJECT: INF, POS-O | REJECT: INF, POS-O | `+INF,POS-O\|POS-O',POS-T,POS-C` |
| nc-Qneg | REJECT: INF, POS-O | REJECT: INF, POS-O, POS-O′, POS-T, POS-C | `+INF,POS-O\|POS-O',POS-T,POS-C` |
| td-nu | REJECT: Z0, DIV-O, DIV-C, CORNER, FIRST, INF, POS-O, POS-O′, POS-C | the same | `+Z0,DIV-O,DIV-C,CORNER,FIRST,INF,POS-O,POS-O',POS-C\|POS-T` |
| d6 | REJECT: POS-O, POS-O′, POS-T | the same | `+POS-T\|POS-O,POS-O',POS-C` |
| nc-bound | REJECT: nc-bound (b) | the same | `=REJECT: nc-bound (b)` |
| td-coeff | REJECT: E0n, Z0, DIV-O, DIV-C, THROAT, CORNER, FIRST, INF, POS-O, POS-O′, POS-C | the same | `+E0n,Z0,DIV-O,DIV-C,THROAT,CORNER,FIRST,INF,POS-O,POS-O',POS-C\|POS-T` |
| td-verifier | REJECT: KAT | the same | `=REJECT: KAT` |
| td-cover | REJECT: COVER | the same | `=REJECT: COVER` |
| td-div | REJECT: DIV-T, DIV-C, THROAT, CORNER, FIRST, POS-T, POS-C | the same | `+DIV-T,DIV-C,THROAT,CORNER,FIRST,POS-T,POS-C\|POS-O,POS-O'` |

- **nc-bound.** The support and K equal the development values, as §4 requires:
  - D = 7 ℓ = 2: [21/1000, 837/10000], K = 301062550;
  - D = 11 ℓ = 4: [257/10000, 41/400], K = 346269974.

  At both, Q[b] < 0 is certified in Arb. The printed enclosures are [−2.900610727·10⁻¹² ± 1.90·10⁻²³] and
  [−4.660852684·10⁻¹¹ ± 8.10·10⁻²²]. The planted NL is refused on the support. The unplanted trial energy I₁ is > 0 at
  both (floats), so no K1 event occurred.
- **d6.** The design's T(2, MU_C) is > 0 at both kit bands, so K6 > 0 and the planted T(2, MU_C) is < 0. POS-T refused
  it at both, and POS-O and POS-O′ did too. Every identity gate passed under it.

## What is certified

> **HD-X-2 (certified).** For each of the 9 bands of 𝒦 (D = 7–11 with 2ℓ ≤ n − 1) and every q ∈ [q(MU1), 1), with
> q(MU1)² ≤ (99/100)² checked exactly, A_{ℓ,q} ≥ 0 on C₀^∞(ℝ).

What it rests on:
- Proposition 3 for P that is C¹ on (0, 1): *machine-checked* (`prop3_Dn`, BHM-091).
- P's smoothness for μ > 0, and the cover of (0, 1) × (0, MU1] by the four charts: proved (pencil; audited 0× at
  general n). These are the same steps as HD-X-S's, and item A3 of Fable's audit (BHM-141).
- The tortoise map onto ℝ for 0 < q < 1: proved (pencil). This is item A2 of the same audit.
- S5's transcription, checked by gate E0n against Kimi's independent one, as in HD-E.

**With Z at q = 1** (BHM-126; machine-checked, BHM-134/135), **Theorem HD** for q ≤ 99/100 (BHM-079), **HD-X-E**
(BHM-128), **HD-X-S** (BHM-132) and **Lemma U(n)** (BHM-063):

> **Theorem HD-X (certified).** For D = 7, 8, 9, 10, 11, every integer ℓ ≥ 2 and every q ∈ (0, 1], the quadratic form
> A_{ℓ,q} of the scalar-type gravitational potential V_S− (Kodama–Ishibashi's Φ₋) is ≥ 0 on C₀^∞(ℝ). So the master
> equation has no exponentially growing mode, up to and including extremality.

With Theorems A1 and A2 (D = 6), every D = 6–11 is now certified for all ℓ ≥ 2 and all q ∈ (0, 1]. The physical
reading rests on S5's reduction (*cited*), as for A1. This is relative to the sources read, and it makes no novelty
claim (RULES.md A7); session-L's literature check is pending (BHM-140, item 4).

**Second parties: pending** (RULES.md A4).
- Kimi, by a sealed brief, at the stage-3 report (BHM-140, item 2).
- Fable's pencil audit of the reduction's steps (BHM-141, Part A).

## Records

- `runs/record/` (host-1) and `runs/repro-host-2/`: one directory per job (`D<D>l<ℓ>/<control>/`), each with
  `result.json`, `run.log` and `kitcheck.txt`, and in the reproduction `compare.txt`.
- The kit logs and hosts, with UTC times, are in `logs/`. The two kit logs are byte-identical.
- Every copy in the repo was hashed against its node copy (host-1, host-2): all match.
- The SHA-256 of every record and log are in `SEALED.sha256` under BHM-144.
