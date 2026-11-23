# HD-E RESULT addendum 1: the certified bounds, exact and with inward decimals

*Item BHM-084 (correction). 2026-10-23, the bh-modes lead. Found by the session-R lead's reading of the
D = 7–11 stage report (BHM-085, §1.2). `RESULT.md` (BHM-063) is sealed and unchanged.*
- *This file replaces its decimal quotes of certified lower bounds: E2's "≈" column and E3's last column.*
- *No certificate and no claim changes. Theorem HD uses only positivity.*
- *The decimals were computed from the exact rationals of `runs/record/main/result.json` by floor to four
  significant figures, on host-1.*
- *Sealed.*

## What was wrong

A certified lower bound must be quoted rounded **down**. Rounded up, it claims a bound that was not proved.
- **E3:** `RESULT.md` quotes 4.842 and 3.029 for D = 10 and 11, against 4.8416… and 3.0285….
  - `STAGE_REPORT.md` and REGISTRY row BHM-063 quote 38.6, 7.19 and 3.03 for D = 7, 9 and 11, against 38.572…,
    7.1874… and 3.0285….
  - I repeated those values in my reports to the operator.
- **E2:** 6 of the 13 "≈" values in `RESULT.md` are rounded up: D = 9 ℓ = 5, D = 10 ℓ = 3–5, D = 11 ℓ = 5–6. One
  example is "≈ 136" for 135.959….

## E3: Lemma U(n), m⁻³U₋ ≥ the bound, for every ℓ > ℓ₀ and q ∈ [0, 1]

| D | holds from ℓ = | exact bound | inward decimal |
|---|---|---|---|
| 7 | 11 | 399917/10368 | 38.57 |
| 8 | 11 | 1481614528/62748517 | 23.61 |
| 9 | 12 | 17257/2401 | 7.187 |
| 10 | 14 | 79325/16384 | 4.841 |
| 11 | 15 | 19870/6561 | 3.028 |

## E2: the 13 bands with an onset, U₋ ≥ the bound for q ≤ q_split

The exact rationals are in `runs/record/main/result.json`, field `U_lower_bound`.

| D | ℓ | inward decimal |
|---|---|---|
| 7 | 2 | 345.0 |
| 7 | 3 | 2843 |
| 8 | 3 | 1793 |
| 8 | 4 | 10510 |
| 9 | 3 | 3593 |
| 9 | 4 | 7442 |
| 9 | 5 | 35850 |
| 10 | 3 | 135.9 |
| 10 | 4 | 11670 |
| 10 | 5 | 27160 |
| 11 | 4 | 23140 |
| 11 | 5 | 44350 |
| 11 | 6 | 101800 |

## The rule, going forward

Every decimal quote of a certified bound, or of an interval end, is computed from the exact value by directed
rounding, in a registered script, never typed by hand. BHM-060 was the first instance of this error; this is the
second.
