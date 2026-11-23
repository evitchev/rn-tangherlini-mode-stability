# PREREG: the reproduction package on the public copy without local names (pubkit2)

*Item BHM-219. Registered 2026-11-23 (EST) by the bh-modes lead, before any run of record. Under the operator's rulings
BHM-206 (the redactions and licenses) and BHM-217 (the repository's new home, the Rutgers address, the private
account's four lines blanked out, every local machine and folder name removed), and BHM-216 (the repository
created).*

## Why

BHM-217 changes the public copy far more than BHM-206 did: about 2,450 files change and 77 paths are renamed. Some of
them are files the package itself uses:
- the Lean setup folder, in `kit/stability/run_lean.sh` and the nine Lean build scripts;
- six records that the package checks byte for byte;
- the values of `SEALED.sha256`;
- two constants of `code/hdx/elementary.py`.

`DEV.md` gives the details. The run of record BHM-210 (`results/pubkit/`) was made on a copy that still had the local
names. The paper's §6 says that a second run, on the public repository itself, gave the same on both computers. This
run is made on the new copy, so that this statement holds for it.

## What is run

**The snapshot.** `paper/stability/snapshot/assemble3.sh C OUT`, where C is the commit that registers this file. Every
input comes from C:
- the paths of `MANIFEST2.txt` (`MANIFEST.txt` with `results/pubkit2`), minus `EXCLUDE.txt`;
- the helper package `[code of another line of this project]`, moved to `code/kimaster`;
- `redact2.sed`, applied line for line;
- the code constants of `hashconst.tsv`, set to the SHA-256 here of the records they name;
- the Lean `SOURCES.tsv` and `SHA256SUMS` files, brought up to date;
- `SEALED.sha256`, with each registered file's SHA-256 here;
- the files of `root/`;
- `REDACTIONS.md`, `REDACTIONS.tsv` and the top-level `SHA256SUMS`.

The snapshot becomes a new git repository with one commit, C1, with "Evgueniy Vitchev <evgueniy.vitchev@rutgers.edu>"
as author and committer (BHM-217). It is cloned fresh on each node from a git bundle that holds `HEAD` and `main`.

**Before the runs.** assemble3.sh's scans must report all of these:
- no redaction target left, in contents or in paths;
- no use of the two catch-all names, for a home path or a user's name that no rule names;
- no quiet-list word;
- no file over 50 MB;
- no failure in `SEALED.sha256`.

On each clone, `sha256sum -c SHA256SUMS` must pass, and `HEAD` must be C1.

**The runs**, from the fresh clones, under `nice -n 19`:
- **K1, host-1:** a fresh venv (`[python]/bin/python3.12 -m venv`, then `pip install --require-hashes -r
  requirements.lock`), then `kit/stability/run.sh all OUT/all`.
- **K2, host-2:** the node's `[venv]` (built from the same lock, `ENVIRONMENT.md`), then
  `kit/stability/run.sh all OUT/all`.
- **K3, host-2:** `kit/stability/run_lean.sh OUT/lean`, with `BHM_LEAN_TOOLCHAIN` and `BHM_LEAN_PATH_FILE` set
  explicitly, to the node's Lean 4.24.0 toolchain and to a copy of its Mathlib `lean_path.txt`. This uses the renamed
  Lean setup folder of the copy.

Each run's launch script is kept with its log.

## Pass

- **K1 and K2:** exit 0, and the last line `all: KIT PASS`. This requires three things: every one of the 54 cited
  records equals its record in the canonical form, every test ends as specified, and the package's selftest passes.
  The canonical form drops the `host` field, the only place where a registered record names a computer, so any
  difference is a failure of the copy.
- **K3:** exit 0, the last line `lean: KIT PASS`, and each of the nine developments' line "as archived" (its new
  verdict line equals its archived one).
- Anything else is **FAIL**. A failure is reported in `RESULT.md` as it happened, with its cause if found. There is no
  re-run under this registration; a fix needs a new item.

## Information, not criteria

- Each Lean build's whole log after masking times. Every development's logged source hashes differ from its archived
  log's, since every one has a changed source or build script (`REDACTIONS.tsv`).
- Timings, and the byte comparison of `run.log` files (p3's print timings).
- The canonical comparison of the 370 tests. The expected result is 334 equal, as in K1dev (`DEV.md`, D2). The 36 that
  should differ are these:
  - A2-S's nc-a2, nc-res, nc-zm and td-chart, in their detail strings, as in BHM-210;
  - 32 records that quote the SHA-256 of a record changed in this copy: the 20 HD-S check runs (`scheck-…`, field
    `record_sha256`) and the 12 design-tamper tests (HD-X-S's 11 `…-td-design` and A2-S-check's `td-design`, in the
    message). Each should differ from its stored record in that hash alone, apart from the masked fields.

  The verdicts of all 370 are checked by their pieces' own runners, which the pass line requires.

## Afterwards

1. The run's logs and summaries go to `results/pubkit2/runs/`, and the verdict to `results/pubkit2/RESULT.md`.
2. A second build is made, by assemble3.sh at the commit that adds them. Its files must equal C1's except for these:
   - `results/pubkit2/RESULT.md` and `results/pubkit2/runs/`, which are new;
   - `README.md` and `REDACTIONS.md`, whose sentence on this run changes from "is run" to "was run";
   - `REDACTIONS.tsv` and `SHA256SUMS`.

   This build becomes the repository's second commit, C2, by the same author.
3. The session-R lead scans the trees of C1 and C2 with its own list, counts only.
4. Nothing is pushed to `evitchev/rn-tangherlini-mode-stability` before the runs and that scan are done. Then C1 and C2
   are pushed, and a fresh clone from GitHub must equal C2's tree.
