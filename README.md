# Mode stability of Reissner–Nordström–Tangherlini black holes in the scalar gravitational sector, for D = 6–11 and every charge up to extremality

This repository accompanies the paper of that title by Evgueniy Vitchev. It holds the code of every computation the
proof uses, the records of those computations, a reproduction package, and the Lean developments that the paper cites.

## What the paper proves

For D = 6, …, 11, every multipole ℓ ≥ 2 and every charge 0 < |Q| ≤ M, extremality included, the operator
−d²/dr*² + V_S− of Kodama and Ishibashi's scalar-type master equation for Φ₋ is non-negative, so that equation has no
exponentially growing mode (Theorem 1). At extremality the paper gives, for every D ≥ 4, a positive zero-energy solution
that decays at infinity (Theorem 2). The proof is computer-assisted: its computations verify polynomial inequalities,
and a few exact identities, in exact rational arithmetic.

## Layout

| Path | Contents |
|---|---|
| `code/` | The Python code of the computations (python-flint with FLINT 3.6.0, and sympy). |
| `kit/stability/` | The reproduction package: one command per part of Theorem 1, and the Lean part. |
| `kit/<piece>/` | The runners of the single pieces, which the package calls. |
| `results/<piece>/` | For each piece of the proof: its specification, written before it ran (`PREREG.md` and addenda); its result file (`RESULT.md`); the JSON records of its runs (`runs/record/`) and of their reproductions on a second computer (`runs/repro-…/`); and the independent checks (`audits/`, `reviews/`). |
| `results/paperkit/` | The specification and result of the reproduction package's first trial run. |
| `results/stage3/` | Independent checks made of several pieces at once. |
| `lean/` | Nine Lean developments, each with its build script, its build log, its source hashes and its tests. |
| `paper/stability/` | Independent checks of the paper's assembly and text. |
| `literature/` | The reports and ledgers of the two citation checks (their copies of the cited papers are not published). |
| `AUDITS.md` | Every independent check, with its record. |
| `REDACTIONS.md` | What this public copy changes in the project's records; `REDACTIONS.tsv` lists the changed files. |
| `requirements.lock` | The pinned Python packages, with their hashes. |

## Reproducing the computations

You need Linux on x86-64 and CPython 3.12 (3.12.8 was used), and bash with coreutils. Then, from the top of this
repository:

```
python3.12 -m venv venv
venv/bin/python -m pip install --require-hashes -r requirements.lock
export BHM_PYTHON=$PWD/venv/bin/python
kit/stability/run.sh all /some/new/directory
```

This re-runs every certificate of Theorem 1, the package's own tests, and each piece's tests on false inputs and on
deliberately corrupted code. It ends with `all: KIT PASS` only if each new record equals the recorded one in the
canonical form of `kit/stability/canon.py` (which drops only timing, host, version and archive fields; the expected
hashes are in `kit/stability/expected.tsv`) and every test ends as specified. It takes about 45 CPU minutes, or 11
minutes with the default 8 parallel processes (`BHM_JOBS`). The parts can also be run one at a time:
`selftest`, `A1`, `A2`, `HD`, `HDX` and `Z`. `kit/stability/README.md` gives the details.

## Reproducing the Lean developments

You need Lean 4.24.0 and Mathlib v4.24.0 (commit `f897ebcf72cd16f89ab4577d0c826cd14afaafc7`, with the dependencies its
`lake-manifest.json` pins), built, and `python3` for the mutation tests:

```
elan toolchain install leanprover/lean4:v4.24.0
git clone https://github.com/leanprover-community/mathlib4 && cd mathlib4 && git checkout f897ebcf72cd16f89ab4577d0c826cd14afaafc7
lake exe cache get && lake build
```

Write Mathlib's `LEAN_PATH` (the `.lake/build/lib/lean` directories of Mathlib and of each package under
`.lake/packages/`, and the toolchain's `lib/lean`, separated by colons) into a file, and run:

```
export BHM_LEAN_TOOLCHAIN=$HOME/.elan/toolchains/leanprover--lean4---v4.24.0
export BHM_LEAN_PATH_FILE=/path/to/that/file
kit/stability/run_lean.sh /some/new/directory
```

Each of the nine developments is rebuilt by its own `build.sh`: its source hash, the compilation (no `sorry`, no new
axiom), its tests that must fail, and its mutation tests. The run ends with `lean: KIT PASS` only if every build ends
with its archived verdict. It takes about 25 minutes.

## About the records

The records were written while the work was done, in the project's working vocabulary. The paper explains every result
in standard terms. In the records:
- `BHM-` numbers refer to the project's registry, which is not published;
- "certified" means verified by exact computation, "pencil" proved by hand, "second party" an independent check, and
  "gate" a check inside the code;
- "Kimi", "Fable", "session-L" and "session-R" are the AI agents that made the independent checks (`AUDITS.md`);
- `host-1` is the computer on which the records were computed, and `host-2` the second, separate computer of the
  reproductions (the paper's §6); `host-0` is the one on which files were edited. Paths outside this repository are
  shortened to bracketed names, such as `[repository]` and `[run-folder]` (`REDACTIONS.md`).

The project's own repository, with its registry and full history, is private; this is a curated copy. Some passages of
its records mention unrelated unpublished work, the author's other projects, a private working account, or the
computers and folders the work was done in. Here they are replaced by neutral words, and `REDACTIONS.tsv` lists each
changed file with the SHA-256 of its original. No computed number, verdict or result changes.

The reproduction package was run on this copy itself (`results/pubkit2/`). `results/pubkit/` records an earlier run, on a copy that still had the local names.

## Licenses

The code is under the MIT license (`LICENSE`). The records, data and documents are under CC BY 4.0
(`LICENSE-DATA.md`).
