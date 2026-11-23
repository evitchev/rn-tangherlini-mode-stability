# RESULT: the reproduction package on the public copy without local names (pubkit2)

*Item BHM-220, under the registration BHM-219 (`PREREG.md`, sealed at `53d2c82`). bh-modes lead, 2026-11-23 (EST).*

**Verdict: PASS.** Every criterion of `PREREG.md` holds.

## The copy

- **Assembled** by `paper/stability/snapshot/assemble3.sh 53d2c82`, with the tools as sealed: 7,232 files, 77 MB.
  2,456 files changed, 77 paths renamed, 42 manifests brought up to date, and the two code constants set.
- **Its scans:**
  - no redaction target left, in contents or in paths;
  - neither catch-all name used;
  - no quiet-list word and no file over 50 MB;
  - `SEALED.sha256`: 1,723 files, every line verifying.
- **Its `SHA256SUMS`:** 7,231 lines, hashing to `22fced88…`, and it verifies.
- **Against the last development build** (from `ce1002b`, `DEV.md`), `diff -rq` finds only three files:
  `REDACTIONS.md` (its commit), `SEALED.sha256` (the line of the sealed `PREREG.md`) and `SHA256SUMS`.
- **As a repository:** one commit, C1 = `8d9e971`, "The paper's code, records, reproduction package and Lean
  developments", with "Evgueniy Vitchev <evgueniy.vitchev@rutgers.edu>" as author and committer (BHM-217).
  - **The bundle:** `64d91f39…`, holding `HEAD` and `main`, cloned fresh for each run.
  - **Each clone:** `HEAD` was C1, and `sha256sum -c SHA256SUMS` passed before the run.

## The runs, from the fresh clones, under `nice -n 19`

| Run | Node | Environment | Outcome |
|---|---|---|---|
| K1 | host-1 | a fresh venv from `requirements.lock`: python-flint 0.9.0, gmpy2 2.3.2, mpmath 1.3.0, sympy 1.14.0 | `all: KIT PASS`, exit 0, 17:42:39Z–17:54:06Z |
| K2 | host-2 | `[venv]` (the same versions) | `all: KIT PASS`, exit 0, 17:42:39Z–17:55:12Z |
| K3 | host-2 | Lean 4.24.0 and Mathlib v4.24.0, through `BHM_LEAN_TOOLCHAIN` and `BHM_LEAN_PATH_FILE` (a copy of the node's path file) | `lean: KIT PASS`, exit 0, 17:42:39Z–18:09:05Z |

- **K1 and K2:** the selftest passes (KC1–KC6 and KC6b). Each of A1, A2, HD, HDX and Z ends `KIT PASS`, with its
  canonical comparison of the cited records: A1 3/3, A2 2/2, HD 19/19, HDX 21/21 and Z 9/9. So all 54 cited records
  equal their records. The six records that the package checks byte for byte pass those checks, against this copy's
  `SEALED.sha256` and its two constants.
- **K3:** each of the nine developments, `lean_a1_2026-10-22` included, ends "build.sh exit 0; ALL CHECKS AS REQUIRED
  (as archived)". So the renamed Lean setup folder works in all nine build scripts.

## Information, as `PREREG.md` expected

- **The tests:** 334 of 370 equal in canonical form on each node, and the same 36 differ on both.
  - **Four** are A2-S's nc-a2, nc-res, nc-zm and td-chart, as in BHM-210.
  - **The other 32** quote the SHA-256 of a record changed in this copy: the 20 HD-S check runs and the 12
    design-tamper tests. Each was compared field by field with its stored record, on each node. Apart from the masked
    fields, only that hash differs.

  The verdict of every test is checked by its piece's runner, which the pass lines require.
- **The `run.log` files**, byte for byte: A1 17/21, A2 22/27, HD 69/69, HDX 277/288 and Z 19/19 identical, on each
  node. Against BHM-210 (A2 23/27, HDX 288/288), the twelve more that differ are exactly the design-tamper tests,
  whose message quotes the changed hash.
- **The Lean logs:** every build's whole log differs from its archived log after masking times, since each
  development has a changed source or build script.
- **Timings:** K1 about 11.5 minutes (with its venv), K2 about 12.5, K3 about 26.5.

## Records

- `runs/k1-host-1/` and `runs/k2-host-2/`: each run's log and launch script, the five parts' `*.canon.txt`, and
  `selftest.txt`.
- `runs/k3-host-2/`: the run's log and launch script, and each development's new `BUILD_LOG.txt`.
- `runs/SHA256SUMS` lists all 27 files.

## Next

1. The second commit, C2, adds these records (`PREREG.md`, "Afterwards").
2. The session-R lead scans C1 and C2.
3. Both are pushed to `evitchev/rn-tangherlini-mode-stability`, private until posting day.
