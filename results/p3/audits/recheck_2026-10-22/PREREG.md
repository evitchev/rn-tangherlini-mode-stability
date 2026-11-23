# PREREG: re-run of Kimi's cross-check of its two routes to N (p3 audit, BHM-036)

*Item BHM-039. Registered 2026-10-22 by the bh-modes lead, before any run.*

## Why

Kimi's p3 audit (BHM-036) builds N in two ways:
- for T1 and G1, from sympy (`own/make_N.py`, which differentiates f symbolically);
- for the box certificates T2 and T3, from its own exact arithmetic in ℚ(μ) (`own/make_boxes.py`,
  `own/rf.py`), with (1 − z)f_z entered by hand.

`own/crosscheck.py` compares the two at μ = 1/6 with T1's stored P. The only log delivered is
`own/crosscheck.log` (20:19:10), which reads `CROSSCHECK FAILED`. It was written before the fix to
`make_boxes.py` (20:21:35) that Kimi records as self-correction 2. `AUDIT.md` says the two routes
agree after the fix, but no delivered log shows it. Kimi's T2 and T3 verdicts rest on the second
route.

## Claim

Kimi's delivered code, unmodified, prints `CROSSCHECK OK`. For T1's stored P at μ = 1/6, the two
routes then give the same N(z), coefficient by coefficient, in exact rational arithmetic.

## Method

- A `git archive` of the commit holding this file and the archived delivery
  (`results/p3/audits/kimi_2026-10-22/`).
- Run on host-1 in `[venv]`, under `nice -n 19`:
  `python -I own/crosscheck.py`. No file of the delivery is changed.

## Pass criterion

The output starts with `CROSSCHECK OK`, and the exit code is 0.

## Control (must fail)

**NC-RC1.** In a scratch copy of `own/`, change one coefficient in `make_boxes.py`: U₂ = 46080(1 + mδ)
becomes 46081(1 + mδ). This alters the hand-entered route only. The cross-check must print
`CROSSCHECK FAILED` and exit 1.

## What follows from the outcome

- **Pass:** the evidence for Kimi's T2 and T3 verdicts is complete.
- **Fail:** Kimi's two routes disagree after the fix. Its T2 and T3 verdicts then do not count as a
  second-party check until Kimi explains the disagreement.

Either way, the status of BHM-023 and BHM-025 rests on their own records and is not changed by this
run.
