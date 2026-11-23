# RESULT: the reproduction package on the public snapshot (pubkit)

*Item BHM-210, under the registration BHM-209 (`PREREG.md`, sealed at `7820337`). bh-modes lead, 2026-11-23 (EST).*

**Verdict: PASS.** Every criterion of `PREREG.md` holds.

## The snapshot

- **Assembled** by `paper/stability/snapshot/assemble.sh 7820337`, with the tools as sealed (`assemble.sh` `6801c3e0…`):
  7,203 files, 76 MB; 130 files redacted, 2 paths renamed, 33 manifests brought up to date. Its scans: no redaction
  target left, no quiet-list word, no file over 50 MB. Its `SHA256SUMS` hashes to `293e1915…` and verifies.
- **Against the development build** (`3737d4c`, scanned by the session-R lead in BHM-208), `diff -rq` finds only
  `REDACTIONS.md`, `SEALED.sha256`, `SHA256SUMS`, `results/pubkit/DEV.md` and `results/pubkit/PREREG.md`.
- **As a repository:** one commit, `49b12d0`, by "Evgueniy Vitchev" `<[withheld-address]>` as author
  and committer (BHM-196). Its bundle (`b614fbde…`) was cloned fresh on each node, and `sha256sum -c SHA256SUMS` passed
  there before any run.

## The runs, from the fresh clones, under `nice -n 19`

| Run | Node | Environment | Outcome |
|---|---|---|---|
| K1 | host-1 | a fresh venv from `requirements.lock`: python-flint 0.9.0, gmpy2 2.3.2, mpmath 1.3.0, sympy 1.14.0 | `all: KIT PASS`, exit 0, ended 2026-11-23T05:01:11Z |
| K2 | host-2 | `[venv]` (the same versions) | `all: KIT PASS`, exit 0, ended 05:02:20Z |
| K3 | host-2 | Lean 4.24.0 and Mathlib v4.24.0, through `BHM_LEAN_TOOLCHAIN` and `BHM_LEAN_PATH_FILE` (a copy of the path file outside its default place) | `lean: KIT PASS`, exit 0, 04:49:46Z–05:16:20Z |

- **K1 and K2:** the selftest passes (KC1–KC6), and each of A1, A2, HD, HDX and Z ends `KIT PASS` with its canonical
  comparison `PASS`: all 54 cited records equal their records.
- **K3:** each of the nine developments, `lean_a1_2026-10-22` included, ends "ALL CHECKS AS REQUIRED (as archived)",
  with `build.sh` exit 0. So the source hashes, compilation, axiom audits, negative controls and mutation tests hold on
  the redacted copies, whose `SOURCES.tsv` entries `assemble.sh` brought up to date.

## Information, as `PREREG.md` expected

- **The tests:** 366 of 370 equal in canonical form on each node. The four that differ are A2-S's nc-a2, nc-res, nc-zm and
  td-chart, as in the first trial and in K1dev; their verdicts are checked by A2-S's runner.
- **Logs:** p3's `run.log` files differ by their timings. Each Lean build's whole log differs from its archived log after
  masking times, since every one of the nine has a redacted source or build script, so its logged hashes differ.
- **Timings:** K1 and K2 about 12 minutes each, K3 about 26.5 minutes.

## Records

`runs/k1-host-1/` and `runs/k2-host-2/`: each run's log, the five parts' `*.canon.txt` and `selftest.txt`.
`runs/k3-host-2/`: the run's log and each development's new `BUILD_LOG.txt`. `runs/SHA256SUMS` lists all 24 files.

## Next

The session-R lead's second scan, of the snapshot with this result in it. Then the push to
`[first-private-location]`, private until posting day.
