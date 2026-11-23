# RESULT — HD-X-PILOT: the design pilot for the 11 non-critical bands

*Item BHM-130. 2026-10-26, the bh-modes lead. Registration: `PREREG.md` (BHM-129). Untrusted, and no claim. Sealed.*

## Verdict: VALID; every band qualifies; KIT PASS

- **The record:** host-1 at `38a3ce0`, from its `git archive` (SHA-256 `ce303c1adbc19c52…`), 18:19:52–18:22:24 UTC.
- **The reproduction:** host-2, with `BHM_REF`. `main` and `gate-a2` are IDENTICAL after masking.
- **gate-a2:** VALID, qualifying at degree 12, and IDENTICAL to A2-PILOT's record of record (BHM-095).
- **In every band** C-EXACT, NC-H and NC-B hold as registered, and PG-HDS holds in the 9 bands that have an HD-S record.
  There is no Sturm breakdown at any sample.

| D, ℓ | a | β₀ | least degree g | min σ at g (float, truncated) |
|---|---|---|---|---|
| 7, 3 | −7/20 | 16/25 | 12 | 0.9335 |
| 8, 3 | −11/25 | 4/25 | 16 | 0.6832 |
| 8, 4 | −8/25 | 36/25 | 12 | 0.9507 |
| 9, 4 | −2/5 | 16/25 | 12 | 0.4211 |
| 9, 5 | −3/10 | 64/25 | 12 | 0.9552 |
| 10, 4 | −16/35 | 4/25 | 20 | 0.1172 |
| 10, 5 | −13/35 | 36/25 | 12 | 0.5958 |
| 10, 6 | −2/7 | 4 | 12 | 0.9474 |
| 11, 5 | −17/40 | 16/25 | 16 | 0.5424 |
| 11, 6 | −7/20 | 64/25 | 12 | 0.7823 |
| 11, 7 | −11/40 | 144/25 | 12 | 0.9652 |

These equal the fork's development run with the same code, as the PREREG disclosed (§1).

## What follows

HD-X-S (BHM-131) registers each band's design from this record. The coefficients are the binary values of the recorded
floats (`float.hex`), converted exactly to the monomial basis. Its gate DESIGN reads
`runs/record/main/result.json` by the SHA-256 sealed under BHM-130.

## Records

- `runs/record/` (host-1) and `runs/repro-host-2/`: `main/` and `gate-a2/`, each with `result.json` and `run.log`;
  `gate-a2/gate.txt`; and, for the reproduction, `compare.txt`.
- The kit logs and hosts are in `logs/`.
