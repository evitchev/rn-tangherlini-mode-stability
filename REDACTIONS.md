# Redactions of this public copy

This repository is a curated copy of the project's own, made from its commit `53d2c82315c1` by
`paper/stability/snapshot/assemble3.sh` of that commit. Some passages of the project's records mention unrelated
unpublished work of the project, the author's other projects, a private working account, or the computers and
folders the work was done in. Here they are replaced by neutral words:

- **Another line of this project:** its name and its files' paths become "[another line of this project]", "[a
  record of another line of this project]" and the like.
- **The author's other projects:** their names become "session-L", "session-R" and "session-H", the names of
  `AUDITS.md` and the README.
- **Another project's stage labels,** which that project keeps private: "[a stage label of another project]".
- **A private working account,** named in four lines of `results/pubkit/`: "[first-private-location]" and
  "[withheld-address]".
- **The computers:** `host-1` is the computer on which the records were computed, `host-2` the second, separate
  computer of the reproductions (the paper's §6), and `host-0` the computer on which files were edited, where
  nothing was computed. File and folder names change the same way.
- **Local paths** outside this repository: the folder each began in becomes a bracketed name, and the rest of the
  path is kept. `[repository]` is this repository; `[run-folder]` the folder of the runs on host-1 and host-2;
  `[venv]`, `[python]` and `[python-2]` Python installations; `[deliveries]` the folder where the
  independent checkers delivered; `[kimi-folder]`, `[fable-folder]`, `[session-R-folder]` and
  `[session-R-runs]` their working folders; `[projects]`, `[tmp]` and `[workdir]` other local folders. The
  folder that holds Lean's `lean_path.txt` becomes `$HOME/lean-setup`, in the nine Lean developments' build
  scripts and in `kit/stability/run_lean.sh` alike; the README says how to provide that file.

The replacements are made within lines, so no line is added or removed. No computed number, verdict or result
changes. In the code they touch comments, docstrings, computer names and paths outside this repository, with three
further changes:

- one helper module's package is renamed: the original `code/[another line of this project]/master.py` is
  `code/kimaster/master.py` here, and two import lines of `code/extremal/` change with it;
- the Lean setup folder is renamed, as above;
- six records that the reproduction package checks byte for byte name a computer in their `host` field. So
  `SEALED.sha256` gives each registered file's SHA-256 as published here, and the two constants of
  `code/hdx/elementary.py` that hold two of those records' SHA-256 are set to their values here. The canonical
  form that the package compares (`kit/stability/canon.py`) drops the `host` field, so
  `kit/stability/expected.tsv` is unchanged. Thirty-two of the package's test records quote the SHA-256 of a
  record changed here (the HD-S check runs and the design-tamper tests), so a new run's test records differ
  from the stored ones in that hash; the package reports test records as information only.

The reproduction package is run on this copy itself before its release (`results/pubkit2/PREREG.md`).

## Changed files

`REDACTIONS.tsv` lists the 2456 changed files, each with the SHA-256 of its original and of its copy
here, and the number of replacements of each kind. SHA-256 values quoted inside the records themselves, for
example in check notes and audit manifests, are those of the originals.

## Renamed paths

- `results/a1/attempt-e60de7f/repro-host-2`
- `results/a1/audits/kimi_2026-10-23/own/controls.host-1.log`
- `results/a1/audits/kimi_2026-10-23/own/lemmaU.host-1.log`
- `results/a1/audits/kimi_2026-10-23/own/part1.host-1.log`
- `results/a1/audits/kimi_2026-10-23/runs/kit-run-host-2`
- `results/a1/audits/kimi_2026-10-23/runs/own-suite-host-1`
- `results/a1/audits/kimi_2026-10-23/v2/own/controls.host-1v2.log`
- `results/a1/audits/kimi_2026-10-23/v2/own/lemmaU.host-1v2.log`
- `results/a1/audits/kimi_2026-10-23/v2/own/part1.host-1v2.log`
- `results/a1/inward_2026-10-25/inward.host-1.log`
- `results/a1/runs/repro-host-2`
- `results/a2/audits/kimi_2026-10-25/own/a2e.host-1.log`
- `results/a2/audits/kimi_2026-10-25/own/a2s_charts.host-1.log`
- `results/a2/audits/kimi_2026-10-25/own/controls_a2.host-1.log`
- `results/a2/elementary/runs/repro-host-2`
- `results/a2/extremal/runs/repro-host-2`
- `results/a2/pilot/runs/repro-host-2`
- `results/a2/s/check-runs/repro-host-2`
- `results/a2/s/runs/repro-host-2`
- `results/extremal/logs/kit-record-host-1.log`
- `results/extremal/logs/kit-repro-host-2.log`
- `results/extremal/runs/repro-host-2`
- `results/hd/elementary/audits/kimi_2026-10-23/own/run_all.host-1.log`
- `results/hd/elementary/runs/repro-host-2`
- `results/hd/pilot/attempt-8c2d6d2/repro-host-2`
- `results/hd/pilot/runs/repro-host-2`
- `results/hd/s/audits/ib-blind_2026-10-23/logs/band_edges_host-0_20261023T153921Z.log`
- `results/hd/s/audits/ib-blind_2026-10-23/logs/code_rec_v1_sha256_host-2.txt`
- `results/hd/s/audits/ib-blind_2026-10-23/logs/env_probe_host-1_host-2_20261023T154333Z.log`
- `results/hd/s/audits/ib-blind_2026-10-23/logs/flint_probe_host-2_20261023T153520Z.log`
- `results/hd/s/audits/ib-blind_2026-10-23/logs/verdict_numbers_host-0_20261023T162551Z.log`
- `results/hd/s/audits/ib-blind_2026-10-23/node_mirror_host-2`
- `results/hd/s/audits/kimi_2026-10-23/own/controls_s.host-1.log`
- `results/hd/s/audits/kimi_2026-10-23/own/verify_all.host-1.log`
- `results/hd/s/audits/kimi_2026-10-23/runs/kit-run-host-2`
- `results/hd/s/audits/kimi_2026-10-23/v2/own/crosscheck_s.host-1.log`
- `results/hd/s/check-runs/repro-host-2`
- `results/hd/s/runs/repro-host-2`
- `results/hdx/critical/logs/kit-record-a1-host-1.log`
- `results/hdx/critical/logs/kit-record-host-1.log`
- `results/hdx/critical/logs/kit-repro-a1-host-2.log`
- `results/hdx/critical/logs/kit-repro-host-2.log`
- `results/hdx/critical/runs/repro-a1-host-2`
- `results/hdx/critical/runs/repro-host-2`
- `results/hdx/elementary/inward_2026-10-26/inward_hdxe.host-1.log`
- `results/hdx/elementary/logs/kit-record-host-1.log`
- `results/hdx/elementary/logs/kit-repro-host-2.log`
- `results/hdx/elementary/runs/repro-host-2`
- `results/hdx/pilot/logs/kit-record-host-1.log`
- `results/hdx/pilot/logs/kit-repro-host-2.log`
- `results/hdx/pilot/runs/repro-host-2`
- `results/hdx/s/logs/kit-gate-record-host-1.log`
- `results/hdx/s/logs/kit-gate-repro-host-2.log`
- `results/hdx/s/logs/kit-record-host-1.log`
- `results/hdx/s/logs/kit-repro-host-2.log`
- `results/hdx/s/runs/repro-host-2`
- `results/hdx/s/runs/repro-host-2-gate`
- `results/onset/audits/kimi_2026-10-22/v3/own/kat.host-1.log`
- `results/onset/audits/kimi_2026-10-22/v3/own/o2345.host-1.log`
- `results/onset/runs/repro-host-2`
- `results/p3/audits/kimi_2026-10-22/v4/own/controls.host-1.log`
- `results/p3/audits/kimi_2026-10-22/v4/own/kat.host-1.log`
- `results/p3/audits/kimi_2026-10-22/v4/own/verification.host-1.log`
- `results/p3/audits/session-L_T3_registration_2026-10-22`
- `results/p3/audits/session-L_T3_rerun_2026-10-23`
- `results/p3/rule2/repro-host-2`
- `results/p3/runs/repro-host-2`
- `results/paperkit/runs/lean-host-2`
- `results/paperkit/runs/record-host-1`
- `results/paperkit/runs/repro-host-2`
- `results/pubkit/runs/k1-host-1`
- `results/pubkit/runs/k2-host-2`
- `results/pubkit/runs/k3-host-2`
- `results/stage3/audits/kimi_2026-10-27/own/hdx2_check.host-1.log`
- `results/stage3/audits/kimi_2026-10-27/own/hdx_controls.host-1.log`
- `results/stage3/audits/kimi_2026-10-27/own/hdxe.host-1.log`
- `results/stage3/audits/kimi_2026-10-27/own/hdxs.host-1.log`

## Manifests brought up to date

These list the SHA-256 of the files beside them, so their lines for the changed files are updated here. A line for
a file that is not published is left as it was.

- `lean/lean_a1_2026-10-22/lean/SOURCES.tsv`
- `lean/lean_a1_2026-10-22/SHA256SUMS`
- `lean/lean_lemmaU_2026-10-23/lean/SOURCES.tsv`
- `lean/lean_lemmaU_2026-10-23/SHA256SUMS`
- `lean/lean_onset_2026-10-22/lean/SOURCES.tsv`
- `lean/lean_onset_2026-10-22/SHA256SUMS`
- `lean/lean_p3_sdeformation_2026-10-22/lean/SOURCES.tsv`
- `lean/lean_p3_sdeformation_2026-10-22/SHA256SUMS`
- `lean/lean_p3_sdeformation_v2_2026-10-23/lean/SOURCES.tsv`
- `lean/lean_p3_sdeformation_v2_2026-10-23/SHA256SUMS`
- `lean/lean_p3_sdeformation_v3_2026-10-23/lean/SOURCES.tsv`
- `lean/lean_p3_sdeformation_v3_2026-10-23/SHA256SUMS`
- `lean/lean_p3_sdeformation_v4_2026-10-24/lean/SOURCES.tsv`
- `lean/lean_p3_sdeformation_v4_2026-10-24/SHA256SUMS`
- `lean/lean_z_2026-10-26/lean/SOURCES.tsv`
- `lean/lean_z_2026-10-26/SHA256SUMS`
- `lean/lean_z_d_2026-10-26/lean/SOURCES.tsv`
- `lean/lean_z_d_2026-10-26/SHA256SUMS`
- `literature/stability-v04-citecheck-2026-11-18/SHA256SUMS`
- `paper/stability/audits/fable_assembly_2026-11-13/SHA256SUMS`
- `paper/stability/audits/fable_v04_delta_2026-11-18/SHA256SUMS`
- `paper/stability/audits/kimi_assembly_2026-11-21/SHA256SUMS`
- `paper/stability/reviews/ib-lead_reading_2026-11-13/SHA256SUMS`
- `results/a1/audits/kimi_2026-10-23/SHA256SUMS`
- `results/a1/reviews/ib-lead_reading_2026-10-23/SHA256SUMS`
- `results/a2/audits/kimi_2026-10-25/SHA256SUMS`
- `results/a2/extremal/audits/kimi_2026-10-22/SHA256SUMS`
- `results/a2/reviews/ib-lead_reading_2026-10-24/SHA256SUMS`
- `results/hd/elementary/audits/kimi_2026-10-23/SHA256SUMS`
- `results/hd/reviews/ib-lead_reading_2026-10-23/SHA256SUMS`
- `results/hd/s/audits/ib-blind_2026-10-23/SHA256SUMS`
- `results/hd/s/audits/kimi_2026-10-23/SHA256SUMS`
- `results/hdx/critical/audits/fable_2026-11-13/SHA256SUMS`
- `results/onset/audits/kimi_2026-10-22/SHA256SUMS`
- `results/p3/audits/fable_2026-10-22/SHA256SUMS`
- `results/p3/audits/kimi_2026-10-22/SHA256SUMS`
- `results/p3/audits/session-L_T3_registration_2026-10-22/SHA256SUMS`
- `results/p3/audits/session-L_T3_rerun_2026-10-23/SHA256SUMS`
- `results/pubkit/runs/SHA256SUMS`
- `results/stage3/audits/fable_2026-10-26/SHA256SUMS`
- `results/stage3/audits/kimi_2026-10-27/SHA256SUMS`
- `results/stage3/reviews/ib-lead_reading_2026-10-26/SHA256SUMS`

## Not published

- The briefs sent to the independent checkers; `AUDITS.md` says what each check covered.
- The copies of the cited papers made for the citation check.
- The project's registry, charter, rules and history, and the draft versions of the paper.
