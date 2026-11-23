# Reproduction package: mode stability of Reissner–Nordström–Tangherlini black holes in the scalar gravitational sector, D = 6–11

*`kit/stability/`. It re-runs the computations of the paper's Theorem 1 (§§4–5) and rebuilds the Lean developments the
paper cites. Its first trial run is specified in `results/paperkit/PREREG.md`, and its run on the public repository in
`results/pubkit/PREREG.md`.*

## What it re-runs

**Theorem 1:** for D = 6–11, every ℓ ≥ 2 and every charge 0 < q ≤ 1, the operator −d²/dr*² + V_S− of Kodama and
Ishibashi's scalar-type master equation is non-negative. Its proof uses the pieces of the paper's Table 1, in five
parts:

| Part | Range | Pieces (record folder) | Cited jobs |
|---|---|---|---|
| A1 | D = 6, q ≤ 99/100 | O1/O2, the onset (`results/onset`); T3 (`results/p3`); P1 with Lemma U(4) (`results/a1`) | 3 |
| A2 | D = 6, q ∈ [99/100, 1] | A2-E (`results/a2/elementary`); A2-S (`results/a2/s`), with its check runs | 2 |
| HD | D = 7–11, q ≤ 99/100 | HD-E: E1, E2 and Lemma U(n) (`results/hd/elementary`); HD-S, 18 bands (`results/hd/s`), with its check runs | 19 |
| HDX | D = 7–11, q ∈ [99/100, 1] | HD-X-E; HD-X-S, 11 bands, and its range check; HD-X-2, 9 bands, and its addendum (`results/hdx/…`) | 21 |
| Z | q = 1, every D ≥ 4 | the extremal zero-energy solution (`results/extremal`) | 9 |

- **The certificates.** The 54 cited jobs are the certificates Theorem 1 uses. Each is a computation in exact rational
  arithmetic that accepts only if every check passes: it then prints `VERIFIED` and exits 0, and otherwise it prints
  `REJECT: <reason>`.
- **The tests.** Each piece also runs its tests on false inputs, which must be rejected, and on deliberately corrupted
  code, which must be caught: 370 jobs in all, each of which must end as specified in advance.
- **The Lean part** (`run_lean.sh`) rebuilds the nine Lean developments the paper cites:
  - the reduction at n = 4, and O2;
  - Lemma U at n = 4;
  - Proposition 3 on (0, 1), and at every n;
  - A2-S's check G-RES;
  - Z, with the tortoise coordinate at q = 1;
  - the transcription of Kodama and Ishibashi's (5.62b)–(5.63b) at n = 4 (the paper's Appendix A).

## What you need

- **Linux on x86_64, and CPython 3.12.** 3.12.8 was used; the gmpy2 wheel in the lock is cp312. Then:

  ```
  python3.12 -m venv venv
  venv/bin/python -m pip install --require-hashes -r requirements.lock
  export BHM_PYTHON=$PWD/venv/bin/python
  ```

  This installs python-flint 0.9.0 (with FLINT 3.6.0), gmpy2 2.3.2, mpmath 1.3.0 and sympy 1.14.0. Each script checks
  these versions and stops if they differ. The results rest on FLINT/Arb, CPython and sympy's exact rationals.
- **Tools:** bash, coreutils (`sha256sum`, `cmp`, `realpath`), `nice`, `timeout` and `xargs`.
- **Time:** about 45 minutes of CPU in all. With the default 8 jobs in parallel (`BHM_JOBS`), `all` took 11 min 21 s on
  a 16-thread computer.
- **Disk:** about 12 MB of outputs.
- **For the Lean part:**
  - Lean 4.24.0, by default at `~/.elan/toolchains/leanprover--lean4---v4.24.0/`, or set `BHM_LEAN_TOOLCHAIN`;
  - Mathlib v4.24.0 (commit `f897ebcf72cd16f89ab4577d0c826cd14afaafc7`), built, with its `LEAN_PATH` written in a file,
    by default `$HOME/lean-setup/lean_path.txt`, or set `BHM_LEAN_PATH_FILE`. The repository's README shows
    how to build it;
  - `python3` (3.8 or later) for the mutation tests.

## One command per part

Run from the top of the repository. OUTDIR must be new and outside the repository.

```
kit/stability/run.sh selftest OUT/selftest   # the package's own tests, KC1-KC6
kit/stability/run.sh A1 OUT/A1               # likewise A2, HD, HDX and Z
kit/stability/run.sh all OUT/all             # the selftest, then the five parts
kit/stability/run_lean.sh OUT/lean           # the Lean part
```

- **The pass line.** Each command ends with `<PART>: KIT PASS` and exits 0 only if all of these hold:
  - every piece's runner ends with `KIT PASS`, by its own rules, specified in advance;
  - every p3 tier ends with the verdict line of its record;
  - every cited job's new record equals its record in the canonical form below.

  Otherwise it ends with `KIT FAIL`.
- **What each part leaves in OUTDIR:**
  - each piece's records and logs in `PART/PIECE/…`;
  - each runner's own log in `PART/PIECE.kit.log`;
  - the comparison in `PART.canon.txt`.
- **Optional variables:** `BHM_COMMIT` and `BHM_ARCHIVE` name the version and the archive's SHA-256 in the new records.

## What "equal" means

`canon.py` turns a record (`result.json`) into a canonical byte string:
- **Dropped:** at every depth, the keys that differ between two runs by construction.
  - `code/compare_runs.py`'s masks: timing, host, platform, version (git commit), and per-box timings;
  - `archive_sha256`, the archive the run came from.
- **Kept:** everything else, every verdict, every exact value, and the tool versions in `provenance`.
- **One exception, for p3's records only:** a top-level `"design_rule": 1` is dropped. p3's code has written that key
  since version `094591c`, after T1–T3's records were made at `782fc56` under the first method of choosing designs.
  (These versions are of the project's own repository, which is private.)
- **The form:** `json.dumps` with sorted keys and no spaces, in UTF-8, plus a newline.

**`expected.tsv`** lists the canonical SHA-256 of each of the 424 records the package compares against: 54 cited and
370 tests.
- `compare` checks first that each record in this repository still has its listed hash, and then that each new record
  has it.
- A cited job that differs fails the part. A test that differs is reported, as information; its verdict is already
  checked by its runner.
- Each job's `run.log` is also compared byte for byte, as information. p3's logs print timings, so they differ.

**`selftest`** shows that the comparison catches what it should, and masks no more than it says:
- **KC1:** an altered expected hash;
- **KC2:** one changed exact value;
- **KC3:** changes to masked fields only, which must still match;
- **KC4:** a missing job;
- **KC5 and KC6:** p3's exception, which applies only to the value 1 and only to p3.

## What a pass shows, and what it does not

- **It shows** that this repository's code, in the pinned environment, reproduces every certificate the theorem cites
  exactly, and that every test ends as specified.
- **It does not show:**
  - the proofs by hand that turn the certificates into Theorem 1: the paper's §4, its Appendix B and the §5 assembly,
    each checked independently (`AUDITS.md`);
  - the transcription of Kodama and Ishibashi's potential, checked separately by Lean and by an independent
    transcription;
  - the soundness of FLINT, CPython or sympy.

## Files read or run at run time, besides `code/`

- **Records of earlier computations,** each checked against `SEALED.sha256` or a hash in the code:
  - the pilot designs (`results/a2/pilot`, `results/hd/pilot`);
  - p3's records under its second method of choosing designs;
  - the records that HD-X-E and A2-S's check runs meet: HD-E, A2-E, A2-S and T3.

  All are in this repository.
- **One independent checker's file is executed.** HD-E's check E0n runs `results/p3/audits/kimi_2026-10-22/own/build.py`,
  Kimi's independent construction of the potential, and compares it with this code's construction for n = 2…12.
  - The check passes only if the file's SHA-256 is
    `399bf7e1c388475409bebdc6116bcacdce7e4d47311855ebfcea350a004c79cc`, the value in the code.
  - The code executes the file before it acts on the hash, so check that hash yourself before you run the HD part.
