# HD-PILOT, PREREG addendum 1: the horizon control NC-H

*Item BHM-073. 2026-10-23, the bh-modes lead. Registered **after** the VOID attempt at `8c2d6d2` (BHM-072)
and **before** any re-run. `PREREG.md` is sealed and unchanged; this addendum amends its §6 row NC-H and
nothing else. Sealed.*

## Why

- **The attempt at `8c2d6d2` is VOID as registered,** and that verdict stays on the record (BHM-072).
  The gates PG1 and PG2 and the control NC-B held. NC-H did not.
- **What went wrong.** NC-H raised P(0) above the horizon bound by adding a constant c to P, as p3's TD-P2
  did.
  - The constant also raises P(1), from about 3.98 to about 4.10.
  - That puts B(1) = W(1) + P(1) − P(1)² below zero: W(1) = 12 for T1.
  - So σ, which is normalised by B(1), is undefined. The evaluator returned None, not the registered
    σ < 0.
- **Whose defect.** The tampered design was rejected either way; σ undefined counts as failing. The
  defect is the control's design in the registration, not the evaluator.

## The change

**NC-H** becomes the following:
- **The tamper:** T1's pilot design plus c(1 − z), with c = W(0)/f_z(0) − P(0) + 1/10.
- **What it does:** it raises P(0) to 1/10 above the horizon bound W(0)/f_z(0) and leaves P(1) unchanged.
  So B(0) = −f_z(0)/10 < 0 while B(1) keeps its value.
- **The criterion stays σ < 0.**

The only code change is that line of `gates()` in `code/hd/pilot.py`, with its docstring.

## What does not change

Everything else in `PREREG.md`:
- the bands, rungs and samples;
- the design rule, ε and its fallback, the two variables, the degrees and the cap;
- the grid, σ and θ = 10⁻⁴;
- the decision rules;
- PG1, PG2 and NC-B;
- the record and reproduction rule.

## Disclosure, and an added consistency check

**What was seen.** The VOID attempt's band results were seen before this addendum was written:
- every band qualified at every rung with ε = 1/50;
- q_max(D) = 99/100 for every D.

The change touches only NC-H's code path. The bands' designs and decisions never use it, so it cannot
move any decision.

**The added check.** After masking timings and provenance, the re-run must reproduce the VOID attempt
in every field except NC-H's entry and the verdict: every other gate, every band record, the decisions.
If it does not, the difference is reported and the pilot is VOID.

## Nodes

As registered: the record on host-1 and the reproduction on host-2, from a `git archive` of the commit
that holds this file (`kit/hd/run_pilot.sh`).
