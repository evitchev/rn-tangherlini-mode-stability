# Development runs for the public snapshot (pubkit), before its registration

*bh-modes lead, 2026-11-23 (EST). Unregistered runs of `paper/stability/snapshot/assemble.sh` and of the reproduction
package on development snapshots, made to find faults before `PREREG.md` is registered, as for the paper kit
(`results/paperkit/DEV.md`). None is a run of record.*

| Run | Commit | Where | What | Outcome |
|---|---|---|---|---|
| A1 | `6e0a83b` | host-0 | `assemble.sh` | stopped at step 2: a loop's last command was a failing test, under `set -e` |
| A2 | `6e0a83b` | host-0 | `assemble.sh`, step 2 fixed | stopped at step 4: a `grep` count with no match, under `pipefail` |
| A3 | `6e0a83b` | host-0 | `assemble.sh`, counts fixed | ran: 7,203 files, 76 MB; 130 redacted, 2 renamed, 33 manifests; no target left; **one quiet-list word**, in `paper/stability/audits/fable_v04_delta_2026-11-18/LEAD_CHECK.md` (the note that a brief named a label) |
| A4 | `3737d4c` | host-0 | `assemble.sh`, with the quiet-list labels redacted and counted | ran: the same counts; no target, no quiet-list word, no file over 50 MB; `SHA256SUMS` verifies; v4's `SOURCES.tsv` matches its redacted source |
| K1dev | `3737d4c` (snapshot `261cd49`) | host-1 | fresh venv from the lock; `run.sh all` | **`all: KIT PASS`, exit 0**, ended 2026-11-23T04:33:31Z. Every part's canonical comparison passes: the 54 cited records equal. Tests: 366 of 370 equal; the four that differ are A2-S's nc-a2, nc-res, nc-zm and td-chart, exactly the four the first trial's PREREG expected (`results/paperkit/RESULT.md` l.55–56). p3's run.log files differ by their timings, as information. (The wrapper's own exit 1 came from its final `tail`, run in the wrong directory, not from the kit.) |
| K3dev | `3737d4c` (snapshot `261cd49`) | host-2 | `run_lean.sh`, with `BHM_LEAN_TOOLCHAIN` and `BHM_LEAN_PATH_FILE` | **`lean: KIT PASS`, exit 0**, 04:22:00Z–04:47:07Z: each of the nine developments, `lean_a1` included, ends "ALL CHECKS AS REQUIRED (as archived)", through the HOME shim. Each whole log differs after masking times, as information (all nine have redacted sources or build scripts, so their logged hashes differ). (The wrapper's exit 1, again its final `tail` in the wrong directory.) |
