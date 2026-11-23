# RESULT: the paper kit's dry run, as the reproduction check of every certificate Theorem 1 cites

*2026-11-18, the bh-modes lead. Registered in `PREREG.md` (BHM-186, at `0879f27`); this result is BHM-187.*

## Verdict: K1, K2 and K3 hold, as registered

- **K1 (host-1, a fresh venv):** `all: KIT PASS`, exit 0.
- **K2 (host-2, `[venv]`):** `all: KIT PASS`, exit 0.
- **K3 (host-2, the Lean part):** `lean: KIT PASS`, exit 0. Each of the eight builds exited 0 and ended with its
  archived verdict line, "ALL CHECKS AS REQUIRED".

**Every certificate Theorem 1 cites matches its registered record byte for byte**, in the canonical form of PREREG §2:
54 of 54, on each node. Every control and drill ended in its registered form, and every p3 tier ended with its record's
verdict line.

## 1. The runs

- **The archive.** `git archive --format=tar 0879f27`, SHA-256
  `6db58904a6b9b821e67fdf8a43d7d439221af73cdf87b4b3074c9775693bb4f5`. That hash was computed from the stream sent to
  each node and once more on host-0, and all three agree. On both nodes, `expected.tsv` (`ff40e490…`) and the PREREG
  (`46c36039…`) have their registered hashes.
- **K1, host-1.** The archive was unpacked in `[run-folder]/paperkit-0879f27/`.
  - The venv was built there fresh: `[python]/bin/python3.12 -m venv`, then
    `pip install --require-hashes -r requirements.lock`, with exit 0. pip reported "Successfully installed
    gmpy2-2.3.2 mpmath-1.3.0 python-flint-0.9.0 sympy-1.14.0".
  - Then `BHM_JOBS=8 nice -n 19 kit/stability/run.sh all OUT`, 18:11:13–18:22:31 UTC (11 min 18 s).
- **K2, host-2.** The same archive and command, with `[venv]`, 18:11:05–18:22:28 UTC.
- **K3, host-2.** `nice -n 19 kit/stability/run_lean.sh OUT`, 18:22:28–18:46:57 UTC (24 min 29 s), with Lean 4.24.0
  (commit `797c613e`) and the Mathlib oleans the builds read on that node.
- **The outputs** are in `runs/record-host-1/` and `runs/repro-host-2/`: every record and log, the canonical
  comparisons (`*.canon.txt`), the selftest, and the top-level log (`run_all.log`). The Lean logs are in
  `runs/lean-host-2/`.

## 2. The claims' conditions, on each node

| | K1, host-1 | K2, host-2 |
|---|---|---|
| (a) the selftest, KC1–KC6 and KC6b | as required | as required |
| (b) every sub-kit `KIT PASS`; every p3 tier its record's verdict line | yes: 14 sub-kits, and p3's 7 tiers | yes |
| (c) every registered record has its listed hash | 424/424 | 424/424 |
| (d) cited jobs MATCH | 54/54 | 54/54 |

By part (both nodes alike):

| Part | Cited | Controls (information) | run.log identical to the record's (information) |
|---|---|---|---|
| A1 | 3/3 | 18/18 | 17/21 |
| A2 | 2/2 | 21/25 | 23/27 |
| HD | 19/19 | 50/50 | 69/69 |
| HDX | 21/21 | 267/267 | 288/288 |
| Z | 9/9 | 10/10 | 19/19 |

## 3. Information (PREREG §4)

- **I1, the controls:** 366 of 370 identical on each node. The four that differ are exactly those the PREREG expected:
  A2-S's nc-a2, nc-res, nc-zm and td-chart.
  - In each, only failing checks' `detail` strings differ. Since `669e774` they begin with the failing point, as
    `DEV.md` §3 shows.
  - The verdict lines and the counterexamples' values are the records'.
- **I2, the logs:** 416 of 424 identical to the records' on each node. The eight that differ are the expected eight:
  - p3's T1, T2, T3 and NC-P1, which print timings;
  - the four controls of I1.
- **I3, the second comparator.** `jq_compare.sh`, run on host-0 over each node's copied outputs, gives cited 54/54 MATCH
  and controls 366/370 MATCH, the same four. It agrees with `canon.py` on every job.
- **I4, the Lean logs:** all eight are identical to the archived ones after masking the start and finish times, the
  mutation registration's "logged" time, and the `seconds=` fields. Each build's `BUILD_LOG.txt` and `build.out` are in
  `runs/lean-host-2/`.
- **I5:** the times in §1.
- **Beyond the PREREG, the two nodes against each other:** all 424 new records identical in the masked form (jq), and 420
  of 424 `run.log` files byte-identical. The other four are p3's timing logs.

## 4. What this closes

- **The reproduction check of the paper's §6** (the operator's ruling BHM-182, item 4): every certificate Theorem 1
  cites now runs from one clean archive of a single commit. That works with a fresh install from `requirements.lock` on
  one node and with the environment of record on the other. Each matches its registered record exactly in the
  canonical form.
- **A2-S's eight original controls,** never re-run since their code changed, now are: all eight end in their
  registered form. Four have new detail strings.
- **Not shown, as the README says:** the pencil steps, the transcription of S5's potential (checked separately by Lean
  and by independent transcriptions), and the soundness of FLINT, CPython and sympy.

## 5. Process

- Nothing ran on host-0 but `git`, `ssh`, `tar`, `sha256sum`, `cmp` and `jq`.
- The nodes were checked for leftover processes after the runs: none on host-1 or host-2.
- The kit is not published (BHM-182).
