# PREREG: the paper kit's dry run, as the reproduction check of every certificate Theorem 1 cites

*2026-11-18, the bh-modes lead. The operator's ruling BHM-182, item 4: "Assemble a stranger-runnable kit from kit/: a
README, one command per theorem part, and the expected hashes. Run it from a clean checkout on host-1/005. Every
certificate the theorem cites should match its registered result byte for byte. Don't publish the kit." Registered
as BHM-186 before the run of record; sealed in `SEALED.sha256`.*

## 1. The object

- **The kit,** `kit/stability/` at the commit C that holds this file:
  - `README.md`;
  - `run.sh`, one command per part (A1, A2, HD, HDX, Z) and `all`;
  - `canon.py`, the canonical comparison;
  - `pieces.tsv`, its fifteen pieces;
  - `expected.tsv`, the expected hashes;
  - `run_lean.sh`, the Lean part.
- **The certificates it re-runs:** every certificate Theorem 1 cites (`paper/stability/versions/DRAFT_v0.4.md` §§4.7
  and 5; `AUDIT_TABLE.md` §4). That is 54 cited jobs, with their registered controls and drills, 370 jobs. The 424
  registered records they are compared with are the records of BHM-017, 023, 052, 063, 078, 089, 097, 101, 105, 128,
  132, 144, 154 and 126. The record folders are listed in `pieces.tsv`.
- **The Lean part** rebuilds eight Lean layers: BHM-030's onset and p3 layers, BHM-066's Lemma U, BHM-090, BHM-091,
  BHM-107, BHM-134 and BHM-135.
- **Not in it:** p3's design rule 2 (BHM-025), which Theorem 1 does not use.

## 2. "Byte for byte"

- **Why whole files cannot match.** Every record carries its run's timing, host, platform, commit and archive hash, so
  two records of the same certificate cannot be identical as files.
- **The canonical form.** The comparison is therefore byte for byte on a canonical form (`canon.py`, its docstring):
  - drop, at every depth, `compare_runs.MASK_KEYS` (the masks of RULES.md D: timing, host, platform, git_commit and the
    per-box timings) and `archive_sha256`;
  - keep everything else: every verdict, every exact value, and the tool versions in `provenance`;
  - write `json.dumps` with sorted keys and no spaces, in UTF-8, plus a newline. The record's canonical hash is the
    SHA-256 of that string.
- **One exception, registered here.** For p3's records only, a top-level `"design_rule"` whose value is the integer 1
  is dropped. p3's code has written that key since `094591c`, and T1–T3's records at `782fc56` predate it.
- **Nothing else is masked.** The selftest's KC3, KC5 and KC6 show the masks to be exactly these.

## 3. The claims

- **K1.** On host-1, from `git archive --format=tar C` unpacked in `[run-folder]/paperkit-C/`, with a fresh venv
  built there from `requirements.lock` (`[python]/bin/python3.12 -m venv`, then `pip install --require-hashes`):
  `BHM_JOBS=8 kit/stability/run.sh all OUT` ends with `all: KIT PASS` and exits 0. OUT lies outside the archive.
- **K2.** On host-2, from the same archive, with `[venv]`: the same command ends with `all: KIT PASS`.
- **K3.** On host-2, from the same archive: `kit/stability/run_lean.sh OUT` ends with `lean: KIT PASS`. Each of the
  eight builds then ends with its archived verdict line.

`all: KIT PASS` holds only if all of these do:
- **(a)** the selftest's controls KC1–KC6 behave as required;
- **(b)** every sub-kit ends with `KIT PASS` by its own registered rules, and every p3 tier ends with its record's
  verdict line (T1, NC-P1, T2 and T3 `VERIFIED`; G1, TD-P1 and TD-P2 their records' `REJECT` lines);
- **(c)** every registered record in `expected.tsv` still has its listed hash;
- **(d)** each of the 54 cited jobs' new record has exactly its registered record's canonical hash.

## 4. Information, reported in the RESULT and not part of the claims

- **(I1) The 370 controls** compared in the same canonical form. All are expected to be identical, with one known
  exception: A2-S's eight original controls. Their records were made at `25c796e`, `a2/scert.py` changed at
  `669e774`, and they had not been re-run since.
  - The development run found four of them differing: nc-a2, nc-res, nc-zm and td-chart.
  - In each, only the `detail` strings of the failing checks differ. Since `669e774` they begin with the failing point,
    as in `"at (8, 0); POS-T: …"`. The verdict lines and the counterexamples' exact values are the same as in the
    records (`DEV.md`).
  - The same four are expected again. Any other difference is reported and explained.
- **(I2) The `run.log` files,** byte for byte. In the development run, 416 of 424 were identical. The other eight are
  expected to differ again:
  - four of p3's, T1, T2, T3 and NC-P1, which print their design and verify times;
  - the four A2-S controls of I1, in the same detail strings.

  Any other difference is reported.
- **(I3) A second comparator.** On host-0, after the outputs are copied back, each new record and its registered
  record go through `jq -S -c` with a `walk` that deletes the same keys (and, for p3, `design_rule` when it is 1). This
  comparison is expected to agree with `canon.py` on every job.
- **(I4) The Lean logs,** compared with the archived ones after masking three things: the start and finish times, the
  mutation registration's "logged" time, and the `seconds=` fields. All eight are expected to be identical, as in the
  development run.
- **(I5)** The wall time of each part, and the archive's SHA-256.

## 5. Not blind

- **The records already exist,** and each was reproduced at its own commit: 428 of 428 identical after masking
  (v0.4 §6, the lead's check of 2026-11-18).
- **Development runs preceded this file:** this kit at `65cbd90`, unregistered planning.
  - On host-1, with a fresh venv: `all: KIT PASS`, the 54 cited jobs MATCH, and the controls 366/370. The second
    comparator agreed on every job.
  - On host-2, the Lean part: `lean: KIT PASS`, each build with its archived verdict line, and all eight logs identical
    to the archived ones once the mutation registration's time stamp is masked too.

  Their outcomes are in `DEV.md` beside this file, and this PREREG was written after them.
- **The expected hashes** were computed by `canon.py build` from the registered records, on host-1, at `65cbd90`:
  `kit/stability/expected.tsv`, SHA-256 `ff40e490c2d26bd792f8bb072c02906134df8ce7e7102641ede311cdb9559c8c`, 424 rows.
  - **Sealed:** all 54 cited records are in `SEALED.sha256` with their current hashes, and so are 347 of the 370
    control records.
  - **Not sealed:** the other 23 are the controls of four early steps, whose main records alone were sealed: onset 5,
    p3 3, a1 7 and HD-E 8. Each is in git, touched by one commit only, the one that added it (`fd689c3`, `094591c`,
    `2ff3cfc` and `d6b6284`).

## 6. If a claim fails

The RESULT reports every difference and explains it; nothing is averaged away (RULES.md D). A fix is a dated addendum
and a re-run, and the failed run stays on the record. If the cause lies outside the kit, in a certificate's own code,
the operator decides before anything is changed. An overrun of the box to 2026-12-05 is a decision point, not an
extension.

## 7. Procedure and hosts

- **The archive.** `git archive --format=tar C` is streamed to both nodes. Its SHA-256 is computed from the same
  stream and passed as `BHM_ARCHIVE`, with `BHM_COMMIT=C`. All computation runs on host-1 and host-2, the top-level
  commands and every job under `nice -n 19` (RULES.md B3).
- **Copied back:** to `results/paperkit/runs/{record-host-1, repro-host-2, lean-host-2}/`, every new `result.json`
  and `run.log`, the sub-kit logs, the `*.canon.txt` files, the selftest's outputs and the top-level log. The Lean part
  copies back its `BUILD_LOG.txt` files and `build.out`.
