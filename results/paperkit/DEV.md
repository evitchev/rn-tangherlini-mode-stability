# The paper kit's development runs (planning, unregistered)

*2026-11-18, the bh-modes lead. These runs tested the kit before its dry run was registered (`PREREG.md` §5). They are
planning data: no claim rests on them. The PREREG was written after them, and says so. The runs' outputs stay on the
nodes, in `[run-folder]/paperkit-dev-65cbd90*`.*

## 1. What ran

- **The code:** the kit at `65cbd90` ("kit/stability: the paper kit, in development"). The archive's SHA-256, from
  `git archive --format=tar 65cbd90`, is `ef691cfc38ab88d9d81e490b5c65f8bb608e014b053d0e7285b155453a15c11a`. It was
  unpacked on host-1 and host-2.
- **The environment** (host-1): a fresh venv from `[python]/bin/python3.12`, then
  `pip install --require-hashes -r requirements.lock`, with exit 0. It gave Python 3.12.8, python-flint 0.9.0 with
  FLINT 3.6.0, sympy 1.14.0, gmpy2 2.3.2 and mpmath 1.3.0. That is the stranger's install path.
- **Syntax:** `bash -n` on `run.sh` and `run_lean.sh`, on host-1. Both are fine.
- **The expected hashes:** `canon.py build pieces.tsv ROOT` on host-1 gave 424 rows, 54 cited and 370 controls.
  - Cited, by piece: onset 1, p3 1, a1 1, A2-E 1, A2-S 1, HD-E 1, HD-S 18, HD-X-E 1, HD-X-S 11, HD-X-2 9, Z 9.
  - This is the `kit/stability/expected.tsv` that the PREREG names, `ff40e490…`.
- **The selftest** (`run.sh selftest`): KC1–KC6 and KC6b all behaved as required. KC2 changed one digit of an exact
  rational, onset's `mu_c`, and that made it a MISMATCH.
- **The whole kit:** `BHM_JOBS=8 run.sh all`, 17:29:37–17:40:58 UTC, ending `all: KIT PASS` with exit 0.

## 2. The outcome, by part

| Part | Wall time | Cited | Controls | run.log byte-identical |
|---|---|---|---|---|
| A1 | 4 min 6 s | 3/3 | 18/18 | 17/21 |
| A2 | 15 s | 2/2 | 21/25 | 23/27 |
| HD | 4 min 2 s | 19/19 | 50/50 | 69/69 |
| HDX | 2 min 54 s | 21/21 | 267/267 | 288/288 |
| Z | 3 s | 9/9 | 10/10 | 19/19 |

Every sub-kit ended `KIT PASS`, and every p3 tier ended with its record's verdict line.

## 3. What differed, and why

- **Four of A2-S's eight original controls:** nc-a2, nc-res, nc-zm and td-chart.
  - Their records were made at `25c796e`. `a2/scert.py` changed at `669e774` (A2-S's PREREG addendum 1) and they were
    never re-run after that.
  - In each, the only differences are the `detail` strings of the failing checks. Since `669e774` these begin with
    the failing point. For example, nc-a2's POS-C was "POS-C: sign*p = -49340399616 <= 0 at (t, mu) = (0, 0)  (a
    counterexample)" and is now "at (0, 0); POS-C: sign*p = -49340399616 <= 0 at (t, mu) = (0, 0)  (a
    counterexample)".
  - Their verdict lines are the records' ("REJECT: POS-T, POS-C" and so on), and so are the counterexamples' exact
    values. Their run.log files differ in the same strings.
  - The other four, nc-bound, td-coeff, td-verifier and td-cover, are identical.
- **Four p3 run.log files** (T1, T2, T3 and NC-P1) print design and verify times, as known. Their records' canonical
  forms match.
- **Nothing else differed.**

## 4. The second comparator

The outputs were copied back to host-0, outside the repository, and `jq_compare.sh` was run over them:
- cited 54/54 MATCH;
- controls 366/370 MATCH, the same four A2-S controls as `canon.py` found;
- `jq compare: PASS`.

The two comparators agree on every job.

## 5. The Lean part

- **The run:** `run_lean.sh` on host-2, from the same archive, 17:42:12–18:08:57 UTC (26 min 45 s), ending
  `lean: KIT PASS` with exit 0. Lean 4.24.0 (commit `797c613e`), with session-L's Mathlib oleans on that node.
- **The verdicts:** each of the eight builds exited 0 and ended with its archived verdict line.
  - BHModesOnset, BHModesP3 (the build of 2026-10-22, v2, v3 and v4), BHModesLemmaU, BHModesZ and BHModesZd;
  - each line was "ALL CHECKS AS REQUIRED": source hash, compilation, the axiom audit, the negative controls and
    every mutation.
- **The logs:** each differed from the archived one after masking times. The only difference was the time stamp in
  the mutation registration's line ("logged 2026-10-22T19:22:55Z"), which the mask had missed.
  - With that stamp masked too (`run_lean.sh` as registered), all eight logs are identical to the archived ones.
  - The lead checked this on host-2 with the extended mask, over the same eight logs.

## 6. What changed after these runs, before registration

- `kit/stability/expected.tsv` was added, as built above, with `kit/stability/README.md`.
- `run_lean.sh`'s mask now also covers the mutation registration's time stamp (§5).
- The PREREG's expectations follow from these runs: I1, the four A2-S controls; I2, the eight logs; I4, the Lean logs.
