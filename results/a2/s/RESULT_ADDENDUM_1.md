# A2-S RESULT addendum 1: every gate has a control, the reading's drills pass, and the main path is unchanged (BHM-105)

*2026-10-24, the bh-modes lead. Registration: `PREREG_ADDENDUM_1.md` (BHM-104), sealed before these checks ran. The
record ran on host-1 and the reproduction on host-2, from a `git archive` of `669e774` (archive SHA-256
`74c7259c0f4ba107…`) with `kit/a2/run_s_check.sh`.*
- *Both kits print KIT PASS.*
- *All 12 records are identical after masking, and the `run.log`s are byte-identical.*
- *`RESULT.md` (BHM-101) is sealed and unchanged.*

**VERIFIED as registered.**

## The new controls (all as registered)

| Control | Verdict | Detail |
|---|---|---|
| td-H | REJECT: H | |
| td-param | REJECT: PARAM | |
| td-design | REJECT: DESIGN | the pilot record's SHA-256 `26501fe6…` is not the changed sealed hash |
| td-gres | REJECT: G-RES | difference 16 |
| td-L | REJECT: L | |
| td-S | REJECT: S, POS-O, POS-O′, POS-T, POS-C | the pole inside the exterior |
| td-divT | REJECT: DIV-T, POS-T | DIV-T fails under its own label; POS-T is "not run" |
| td-divC | REJECT: DIV-C, POS-C | the same for C |
| **d0** (sharp zero margin) | **REJECT: POS-C** | `at (0, 0); POS-C: sign*p = 0 <= 0`; O, O′ and T pass. The strict bound fails exactly at the blown-up corner, and only there |
| **d6** (planted throat defect, zero at μ = 0) | REJECT: POS-O, POS-O′, POS-T | POS-T fails at (ζ, μ) = (2, 1/32), so the throat chart detects negativity at μ > 0. C passes |

With BHM-100's controls, every gate of A2-S now has a planted control or a tamper (RULES.md E.4).

## X0: inward decimals of the certified range ends (exact integer square roots)

| Quantity | Exact | Decimal |
|---|---|---|
| A2-S's lower end q(1/8) | √(2961/3025) | **0.98937** (rounded up) |
| T3, μ ∈ [3/25, 1/5] | [√(21576/22801), √(31416/32041)] | **[0.97277, 0.99019]** (inward) |
| T3's upper end, 8 decimals truncated | √(31416/32041) | **0.99019883** |
| q(μ_lo(ℓ)), ℓ = 3…10 (A2-E's lower end, rounded up; P1's upper end, rounded down) | `check-runs/record/scheck/result.json` | from 0.9900006 / 0.9900005 (ℓ = 4) to 0.9901675 / 0.9901674 (ℓ = 9) |

All three registered values are reproduced.

## X1: the main path is unchanged

The `none` job reran A2-S's certificate with the addendum's code. Its record equals BHM-101's sealed record after removing
timing, provenance and the archive hash (no differing key). So the code changes of `PREREG_ADDENDUM_1.md` §1 left the
certificate exactly as it was.

## Status

- **A2-S:** *certified* (exact), unchanged. Its gates now all have controls.
- The corrections that the reading asks for are BHM-106 (`results/a2/STAGE_REPORT_ADDENDUM_1.md`).

## Hashes

- Code at `669e774`: `code/a2/scert.py`, `code/a2/scheck.py`, `kit/a2/run_s_check.sh`, as in BHM-104.
- Records under `check-runs/record/` and `check-runs/repro-host-2/`. All are listed in `SEALED.sha256`.
