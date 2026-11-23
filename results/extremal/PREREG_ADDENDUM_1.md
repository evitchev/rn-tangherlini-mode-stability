# PREREG addendum 1 — Z: the run at a188aba was VOID, and the fix

*Item BHM-125. 2026-10-26, the bh-modes lead. `PREREG.md` (BHM-123) is sealed and unchanged. Sealed.*

## The VOID run (BHM-124)

- **The run.** The kit of record ran at `a188aba` on host-1 (archive `1919eb718e2d547c…`), 17:58:10–17:58:12 UTC. It
  printed KIT FAIL.
  - Every integer-n job (claim, information and control) ended in `REJECT: exception TypeError: unsupported operand
    type(s) for ** or pow(): 'str' and 'int'`.
  - The N job ended VERIFIED.
- **The defect.** `main()` passed `--n` on as the string "4", and `ki.potentials.U_minus` needs an int. The development
  test replaced the function that builds the potential, to keep S5's potentials out of it. So it never made that call
  with a string.
- **Its status.** By `PREREG.md` §4 an exception is VOID for its job. The attempt is archived in
  `results/extremal/attempt-a188aba/` (kit log, host and records).
- **What was seen** before the fix: the N job's record. It is VERIFIED; its partner Ũ is a quadratic polynomial in Y,
  and the three comparisons are false. The fix below is mechanical and does not depend on it.

## The fix (at `f6c113d`)

- `main()` converts `--n` to an int (or keeps "N") before anything uses it.
- The development test's synthetic UH now refuses a string n, as S5's functions do. Three new tests run the real
  potential path with it:
  - `main --n 4` ends without an exception;
  - it runs every check;
  - a string n, as at `a188aba`, is refused.
- **Development test:** 47/47 as expected, in 2.8 s, at `f6c113d` on host-1 (`[run-folder]/dev-z-f6c113d/devtest.log`).
- **Nothing else changes.** The claim, the checks, the controls and their registered verdicts, the answer forms, the
  hosts and the timeout are those of `PREREG.md`.

## The re-run

It runs from a `git archive` of the commit that holds this file: the record on host-1 and the reproduction on host-2,
as in `PREREG.md` §4.
