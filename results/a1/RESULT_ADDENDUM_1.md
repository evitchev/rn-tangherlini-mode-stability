# A1 RESULT addendum 1: Lemma U's bound, exact and with inward decimals

*Item BHM-119 (correction). 2026-10-25, the bh-modes lead. Found while drafting the stage-2 close-out report.
`RESULT.md` (BHM-052), `STAGE_REPORT.md` (BHM-055) and `TARGET_A2_ADDENDUM_1.md` (BHM-092) are sealed and unchanged.*
- *This file replaces their decimal quotes of Lemma U's bound.*
- *No certificate and no claim changes. Theorems A1 and A2 use only m⁻³U₋ > 0.*
- *The decimals were computed on host-1 by floor, in exact integer arithmetic, from the rational `part2.bound` of
  `runs/record/main/result.json` (`58b9850b6cd76077`). Script `inward_2026-10-25/inward.py`, log
  `inward_2026-10-25/inward.host-1.log`.*
- *Sealed.*

## What was wrong

A certified lower bound must be quoted rounded **down** (BHM-084). Lemma U's bound is 959747/17496 = 54.8552…, and
five places quote it as 54.86:
- `RESULT.md` l.39 and `STAGE_REPORT.md` l.27: "≈ 54.86".
- REGISTRY rows BHM-052 and BHM-065: "≈ 54.86".
- `TARGET_A2_ADDENDUM_1.md` l.24: "m⁻³U₋ ≥ 54.86". The certificate does not give this, since 54.86 > 959747/17496.
  It was written after BHM-084's rule, which it breaks.

Kimi's AUDIT.md (BHM-065) also writes "≈ 54.86". That is Kimi's record; its l.87 gives 54.8552….

## Lemma U: m⁻³U₋ ≥ the bound, for every ℓ ≥ 11 and q ∈ [0, 1]

| exact bound | inward, 4 significant figures | inward, 5 significant figures |
|---|---|---|
| 959747/17496 | 54.85 | 54.855 |
