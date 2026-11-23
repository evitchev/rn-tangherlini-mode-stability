# A1 stage report, addendum 1: second parties complete

*Item BHM-067. 2026-10-23, the bh-modes lead. `STAGE_REPORT.md` (BHM-055) is sealed and stays as
it is. This addendum replaces its status table with today's second parties. No certificate and no
claim changes.*

## Status (replaces `STAGE_REPORT.md`, "Status, and what is pencil-only")

| Claim | Label | Second party |
|---|---|---|
| O2 | *certified* (exact); corner argument re-derived independently | Kimi (BHM-037); Lean (BHM-030) |
| T3 | *certified* (exact), for q ∈ [√(21576/22801), √(31416/32041)], inward [0.97277, 0.99019] (BHM-060) | Kimi (BHM-036, re-run BHM-040); session-L's independent exact re-run (BHM-056) |
| S-deformation reduction (p3 METHOD) | proved (pencil; audited 2×); Lemmas 1–2 and Prop. 3 machine-checked (Lean) | Kimi, Fable (BHM-036, BHM-042); Lean (BHM-030) |
| P1, ℓ = 3…10 | *certified* (exact) | Kimi, by its own exact route and the kit's reproduction (BHM-065) |
| Lemma U, ℓ ≥ 11 | *certified* (exact); steps (a)–(d) proved (pencil; audited 1×) and the whole lemma machine-checked (Lean) | Kimi (BHM-065); Lean (BHM-066) |
| Theorem A1 | *certified*, resting on the rows above | **complete**: every row has its second party |

**What is still pencil only.** Nothing in A1 beyond what the rows say. Lemma U's steps (a)–(d) were
the report's one unaudited pencil item. Kimi audited them (all SOUND), and session-L's Lean theorem
`lemmaU` proves the lemma from `TARGET.md`'s U₋, whose transcription Lean checks in the A1 layer
(BHM-030).

**Cited, not reproved,** as in the report: S5's reduction to the master equations, and S5's
results for the other sectors.

## The corrected interval

`STAGE_REPORT.md` quotes T3 as [0.97277, 0.99020]. The upper end was rounded outward; the inward
value is 0.99019 (BHM-060). Theorem A1's range, 0 < q ≤ 99/100, is unaffected.
