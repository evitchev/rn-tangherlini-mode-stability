# RESULT — HD-E: positivity of U₋ for D = 7–11 where it holds (BHM-063)

*Registered as BHM-062 (`PREREG.md`), part HD-E of `TARGET_HD.md` (BHM-061). The run of record was
on host-1 and the reproduction on host-2, both from a `git archive` of `6fe9689`, in
`[venv]` under `nice -n 19`. They are identical after masking, the main `run.log`s are
byte-identical, and `kit/hd/run_elementary.sh` gives KIT PASS on both nodes. The main run takes
32 s.*

**VERIFIED as registered.** The gates KAT, E0n (our transcription equals Kimi's for n = 2…12),
PARAM4 and H all hold.

## E1: every elementary ℓ up to ℓ₀, q ≤ 99/100

| D | ℓ checked one by one | ℓ₀ |
|---|---|---|
| 7 | 4…10 | 10 |
| 8 | 5…10 | 10 |
| 9 | 6…11 | 11 |
| 10 | 6…13 | 13 |
| 11 | 7…14 | 14 |

Each of these 35 (D, ℓ) is proved at the first Bernstein node, on a μ-box whose coverage of
q ≤ 99/100 is checked exactly. The certified lower bounds of U₋ are in `runs/record/main/result.json`.

## E2: the 13 bands with an onset, up to q_split

| D | ℓ | q ≤ q_split | μ_lo | Bernstein leaves | certified lower bound of U₋ |
|---|---|---|---|---|---|
| 7 | 2 | 0.948 | 176/625 | 7 | ≈ 345 |
| 7 | 3 | 0.977 | 859/5000 | 1 | ≈ 2.84·10³ |
| 8 | 3 | 0.944 | 343/1250 | 1 | ≈ 1.79·10³ |
| 8 | 4 | 0.983 | 71/500 | 1 | ≈ 1.05·10⁴ |
| 9 | 3 | 0.921 | 3317/10000 | 3 | ≈ 3.59·10³ |
| 9 | 4 | 0.952 | 611/2500 | 1 | ≈ 7.44·10³ |
| 9 | 5 | 0.987 | 1211/10000 | 1 | ≈ 3.59·10⁴ |
| 10 | 3 | 0.490 (interior band) | 83/100 | 3 | ≈ 136 |
| 10 | 4 | 0.920 | 201/625 | 1 | ≈ 1.17·10⁴ |
| 10 | 5 | 0.961 | 134/625 | 1 | ≈ 2.72·10⁴ |
| 11 | 4 | 0.897 | 741/2000 | 7 | ≈ 2.31·10⁴ |
| 11 | 5 | 0.929 | 2949/10000 | 1 | ≈ 4.44·10⁴ |
| 11 | 6 | 0.968 | 119/625 | 1 | ≈ 1.02·10⁵ |

- The three zero-margin bands (D = 7 ℓ = 2, D = 9 ℓ = 3, D = 11 ℓ = 4) and the interior band needed
  the most subdivision.
- For each band, the exact q(μ_lo)² ≥ q_split² is in the JSON.

## E3: Lemma U(n), every ℓ > ℓ₀, q ∈ [0, 1], x ∈ [0, 2]

| D | holds from ℓ = | ε̄ | m⁻³U₋ ≥ |
|---|---|---|---|
| 7 | 11 | 1/12 | 38.57 |
| 8 | 11 | 1/13 | 23.61 |
| 9 | 12 | 1/14 | 7.187 |
| 10 | 14 | 1/16 | 4.842 |
| 11 | 15 | 1/18 | 3.029 |

Each bound is an exact rational, in the JSON. The six checks of each lemma pass: polynomiality,
the split, Pos(0) = 64, the κ identity, ε̄, and the sign.

## Controls and drills (all as registered)

| Name | Registered | Observed |
|---|---|---|
| NC-E1, D = 7 ℓ = 2 up to 951/1000 | REJECT at the horizon corner | REJECT: F < 0 at (t, μ) = (1, 1367/5000) |
| NC-E2, D = 10 ℓ = 3 up to 99/200 | REJECT at an interior node | REJECT: F < 0 at (1/2, 1653/2000) |
| NC-E3, D = 8 ℓ = 2 on q ≤ 1/10 | REJECT | REJECT: F < 0 at (1/2, 1987/2000), the corner of the box at its largest charge (q ≈ 0.10) |
| NC-E4, coverage for 98/100 | REJECT | REJECT: coverage |
| NC-E5, Lemma U(9) with ℓ₀ = 2 | REJECT | REJECT: the bound < 0 |
| TD-E1, a coefficient | REJECT at E0n | REJECT: E0n |
| TD-E2, the parametrisation | REJECT in every job | REJECT: the identity fails in every job |
| TD-E3, the verifier | REJECT at the KATs | REJECT: KAT |

## Status, and what follows

- **HD-E:** *certified* (exact). Lemma U(n)'s pencil steps are proved (pencil; audited 0×). An
  independent re-run is pending.
- **Theorem HD now holds** (A_{ℓ,q} ≥ 0, since V > 0):
  - for every ℓ ≥ ℓ_el(D) = 4, 5, 6, 6, 7 and every q ≤ 99/100;
  - for each band with an onset, for q up to its q_split.
- **What remains:** HD-S, on the 18 bands from q_split (or from 0) up to q_max(D), after HD-PILOT.

## Hashes (SHA-256, first 16 hex)

- Code at `6fe9689`:
  - `code/hd/elementary.py` `b77e92151ca9d7f6`
  - `kit/hd/run_elementary.sh` `45243bcf72bdaeb4`
  - `code/a1/p1.py` `7e5fac94a3a51087`
  - `code/onset/bernstein.py` `a0b1ec5c952055ed`
  - `code/onset/onset.py` `9b346258ad0375d1`
  - `code/ki/potentials.py` `7d686b40ad326544`
- The record:
  - `runs/record/main/result.json` `bb06c9023b0f7ad0`
  - `run.log` `d9454332450335d9`
  - `kit.log` `300a3079a6d5493b`
- The reproduction: `runs/repro-host-2/main/result.json` `bce0442384122f20`.
