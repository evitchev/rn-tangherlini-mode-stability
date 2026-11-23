# PREREG: the reproduction package on the public snapshot (pubkit)

*Item BHM-209. Registered 2026-11-23 (EST) by the bh-modes lead, before any run. Under the operator's rulings BHM-191
(item 3: the kit's repository), BHM-195, BHM-196 and BHM-206 (the redactions and licenses).*

## What is run

**The snapshot.** `paper/stability/snapshot/assemble.sh C OUT`, where C is the commit that registers this file. Every
input comes from C: the paths of `MANIFEST.txt`, minus `EXCLUDE.txt`; `SEALED.sha256` cut to the files present; the
helper package `[code of another line of this project]` moved to `code/kimaster`; `redact.sed` applied line for line (BHM-206); the Lean
`SOURCES.tsv` and the `SHA256SUMS` files brought up to date; the files of `root/`; `REDACTIONS.md` and the top-level
`SHA256SUMS`. The snapshot becomes a new git repository with one commit, by "Evgueniy Vitchev"
`<[withheld-address]>` (BHM-196), and is cloned fresh on each node from a git bundle.

**Before the runs, on the clone:** `sha256sum -c SHA256SUMS` must pass, and assemble.sh's own scans must report no
redaction target left and no quiet-list word.

**The runs**, from the fresh clone, under `nice -n 19`:
- **K1, host-1:** a fresh venv (`[python]/bin/python3.12 -m venv`, then `pip install --require-hashes -r
  requirements.lock`), then `kit/stability/run.sh all OUT/all`.
- **K2, host-2:** the node's `[venv]` (built from the same lock, `ENVIRONMENT.md`), then
  `kit/stability/run.sh all OUT/all`.
- **K3, host-2:** `kit/stability/run_lean.sh OUT/lean`, with `BHM_LEAN_TOOLCHAIN` and `BHM_LEAN_PATH_FILE` set
  explicitly, to the node's Lean 4.24.0 toolchain and to a copy of its Mathlib `lean_path.txt` outside the default
  path, so that the new path handling of `run_lean.sh` is used.

## Pass

- **K1 and K2:** exit 0, and the last line `all: KIT PASS`. This requires that every cited record of the 54 equals its
  record in the canonical form, every test ends as specified, and the package's selftest passes. The redactions
  touch no record, so any difference is a failure of the snapshot.
- **K3:** exit 0, the last line `lean: KIT PASS`, and each of the nine developments' line "as archived" (its new
  verdict line equals its archived one).
- Anything else is **FAIL**. A failure is reported in `RESULT.md` as it happened, with its cause if found. There is no
  re-run under this registration; a fix needs a new item.

## Information, not criteria

- Each Lean build's whole log after masking times. For the developments whose sources were redacted, the logged source
  hash differs from the archived log's, as `REDACTIONS.md` predicts.
- Timings, and the byte comparison of `run.log` files (p3's print timings).
- The canonical comparison of the 370 tests. Expected: 366 equal, and A2-S's nc-a2, nc-res, nc-zm and td-chart
  differing in their detail strings, as in the first trial (`results/paperkit/RESULT.md` l.55–56) and in the
  development run K1dev (`DEV.md`). Their verdicts are checked by A2-S's own runner, which the pass line requires.

## Afterwards

The run's logs and summaries go to `results/pubkit/runs/`, and the verdict to `results/pubkit/RESULT.md`. Then the
session-R lead's scan of the snapshot with its own list, counts only (message 23's item 2). Nothing is pushed
to `[first-private-location]` before both are done.
