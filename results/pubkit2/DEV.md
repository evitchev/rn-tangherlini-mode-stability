# Development runs: the reproduction package on the public copy without local names (pubkit2)

*bh-modes lead, 2026-11-23 (EST). Development work under RULES.md's rule on development runs: documented here, not
runs of record.*

The operator's rulings of 2026-11-23 (BHM-217) change the public copy: the author and committer become
"Evgueniy Vitchev <evgueniy.vitchev@rutgers.edu>", four mentions of a private working account are blanked out, and
every local machine and folder name is removed. The new tools are `paper/stability/snapshot/redact2.sed`,
`assemble3.sh`, `hashconst.tsv` and `MANIFEST2.txt`. Removing the local names changes about 2,400 files and renames
the folders of about 4,300 files. It also changes files the package uses: the Lean setup folder in
`kit/stability/run_lean.sh` and the nine Lean build scripts, six records the package checks byte for byte, the
SHA-256 values of `SEALED.sha256`, and two constants in `code/hdx/elementary.py`. So the package is run on the new
copy, first here as development, then as a registered run of record.

## D1: trial assembly on host-0

`assemble3.sh f38b18c` (the tools as first committed), into the session's scratch folder, in 35 seconds:

- **The copy:** 7,231 files, 77 MB. 2,454 files changed, 77 paths renamed, 42 manifests brought up to date, and the two
  code constants set.
- **Scans:** no redaction target is left, in contents or in paths. The two catch-all names, for a home path or a
  user's name that no rule names, were not used. No quiet-list word, no file over 50 MB. `SEALED.sha256` has 1,722
  files and every line verifies.
- **More scans:** none of the names the rulings remove is left. That covers the private account, its address and its
  numeric ID; the computers' names, in any case; the user's name and the home folder; the local folders' names; the
  network addresses; and every temporary path. The `~/` and `$HOME/` forms left are `$HOME/lean-setup` (13),
  `$HOME/.elan` (12) and `~/.elan` (1), plus three tildes in formulas, such as `V~/f`.
- **Records:** all 2,131 changed JSON files parse (`jq empty`).
- **The kit's own files:** the diffs are as intended. In `kit/stability/run_lean.sh` and the nine Lean `build.sh`
  files, the Lean setup folder became `$HOME/lean-setup`, and the shim's folder changed with it. The two
  constants of `code/hdx/elementary.py` became `679302e9…` (the HD-E record here) and `50eece13…` (the A2-E record
  here). The four lines of `results/pubkit/` now read `[withheld-address]` and `[first-private-location]`.
- **The script's report:** its count of "targets in paths" was wrong: it matched the output folder's own path, which
  holds the user's name. The renaming loop also listed that folder itself, harmlessly here, since its name holds no
  target. Both were fixed before sealing: `-mindepth 1`, and paths taken relative to the copy. The files are unchanged,
  and relative to the copy no path holds a target.

The repository: one commit, `a15dbcc`, with "Evgueniy Vitchev <evgueniy.vitchev@rutgers.edu>" as author and committer.
The first bundle had `main` but no `HEAD`, so the nodes' clones could not check out. Both runs stopped at "EXIT sums"
before anything ran. They were restarted with a bundle that has both (`4a346e98…`).

**The session-R lead's screen of D1** (BHM-218): clean. Its public screen would stop nothing, the quiet list
finds nothing, and its file-by-file comparison with the pushed clone `925c479` matches `REDACTIONS.md`. Two changes
follow from its points for information:
- `redact2.sed` gains a rule for the one regular expression that showed the old names' form, in an archived tool of
  the blind replication. It now matches the new names: `^host-\d+$`. The leftover scan now also looks for the old
  names' prefix, in any case.
- The records of this run name no removed name, not even to say it is gone. A first draft did, and the rules turned
  its sentences into nonsense, so they were rewritten in terms of the kinds of name and the bracketed replacements.
- The README's sentence on this run is now written by `assemble3.sh`, from a marker, like `REDACTIONS.md`'s. It reads
  "is run on this copy itself before its release" until `results/pubkit2/RESULT.md` exists, and "was run" after.

## D2: K1dev on host-1

The trial copy `a15dbcc`, cloned fresh from the bundle (`SHA256SUMS` OK), a fresh venv from `requirements.lock`, then
`kit/stability/run.sh all`, under `nice -n 19`: **`all: KIT PASS`, exit 0**, 17:10:13Z–17:21:32Z.
- **The selftest:** KC1–KC6 and KC6b, all as required.
- **The 54 cited records:** every one matches, A1 3/3, A2 2/2, HD 19/19, HDX 21/21 and Z 9/9. The six records
  that the package checks byte for byte pass those checks, so the new `SEALED.sha256` values and the two constants
  hold.
- **The 370 test records:** 334 equal in canonical form (information). The 36 that differ are these:
  - A2-S's nc-a2, nc-res, nc-zm and td-chart, as in BHM-210;
  - 32 records that quote the SHA-256 of a record changed in this copy, and so differ from the stored ones exactly
    there. These are the 20 HD-S check runs (`scheck-…`), whose field `record_sha256` is the hash of the HD-S record
    they check, and the 12 design-tamper tests (HD-X-S's 11 `…-td-design` and A2-S-check's `td-design`), whose message
    quotes the pilot record's hash. Each was compared field by field with its stored record, and only that hash
    differs, apart from the masked fields.

  Every test still ends as specified, which the pass line requires.

## D3: K3dev on host-2

The same trial copy, cloned fresh from the bundle (`SHA256SUMS` OK), then `kit/stability/run_lean.sh`, with
`BHM_LEAN_TOOLCHAIN` and `BHM_LEAN_PATH_FILE` set to the node's Lean 4.24.0 toolchain and to a copy of its Mathlib
`lean_path.txt`, under `nice -n 19`: **`lean: KIT PASS`, exit 0**, 17:11:06Z–17:36:10Z. Each of the nine developments
ends "build.sh exit 0; ALL CHECKS AS REQUIRED (as archived)", `lean_a1_2026-10-22` included. So the renamed Lean setup
folder works, through the shim of `run_lean.sh`, in all nine build scripts. Every build's whole log differs from its
archived log after masking times (information), as expected, since each has a changed source or build script.

## Outcome

The package passes on the copy without local names: K1dev and K3dev both pass. After D1, the tools changed only in the
ways described there and in D2's note: one more rule, the README's generated sentence, the scans' wording, and
`REDACTIONS.md`'s sentence on the 32 test records. The registered run (BHM-219, `PREREG.md`) follows.
