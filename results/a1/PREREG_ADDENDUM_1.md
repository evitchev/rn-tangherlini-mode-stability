# PREREG addendum 1 — A1 for ℓ ≥ 3 (P1): a defect in writing the record, and the re-run

*Item BHM-051. 2026-10-23, the bh-modes lead. Registered before the re-run. `PREREG.md`
(BHM-047) is unchanged; this addendum changes code only.*

## 1. What happened at `e60de7f` (BHM-050)

`kit/a1/run.sh` ran on host-1 (record) and host-2 (reproduction), from a `git archive` of
`e60de7f`. Both gave **KIT FAIL**, identically (the two `kit.log`s are byte-identical).
- **`none` (the main run), `nc-uniform`, `td-coeff`, `td-split`** crashed while writing their record:
  `TypeError: Object of type BooleanTrue is not JSON serializable`.
  - The cause is Part II's check "ε̄ ≥ m₀^{−1/2}", left as a sympy Boolean.
  - The crash came after each verdict was computed and before it was printed. **No verdict of the
    main run was printed**, and its partial `result.json` is archived unread.
- **`td-verifier`** rejected through `KeyError: 'F'`, because the tampered verifier did not fill
  `minrec`. That is a REJECT, but not by the registered route, the KATs.
- **`nc-ell2`, `nc-bump`, `nc-coverage`** rejected exactly as predicted:
  - an exact counterexample at (t, μ) = (1, 121/1000);
  - an exact counterexample at (t, μ) = (1/2, 11/100);
  - [μ_lo, 1] reaching only q < 99/100.

## 2. The fix (`code/a1/p1.py`, commit `a74fc6b`)

- The check "ε̄ ≥ m₀^{−1/2}" is a Python bool.
- The tampered verifier records `minrec` as `prove_sign` does; the acceptance threshold remains its
  only difference.
- The record is converted to plain JSON types before it is written, and a record that cannot be
  written is a REJECT (fail-closed).

**What does not change:** the claim, the boxes, the criteria, the controls, the drills, the
predictions and the implementation parameters.

**Tested.** The synthetic development tests ran again on host-1, from a `git archive` of
`a74fc6b`:
- a record assembled from synthetic Part I and Part II serializes;
- the tampered verifier fills `minrec`.

Nothing of U₋ was evaluated.

## 3. The re-run

- **The run of record of P1** is `kit/a1/run.sh` at the commit that holds this addendum, on host-1,
  reproduced on host-2.
- **The attempt at `e60de7f`** stays on the record (BHM-050), including the three control outcomes
  that completed there. The kit runs those controls again, as registered.
