# A2 stage report, addendum 2: second parties complete

*Item BHM-117. 2026-10-25, the bh-modes lead. `STAGE_REPORT.md` (BHM-102) and `STAGE_REPORT_ADDENDUM_1.md` (BHM-106)
are sealed and unchanged. This addendum replaces the report's status table with today's second parties. No certificate
and no claim changes. Sealed.*

Theorem A2 reads as in the report, with addendum 1 §1's reading: for D = 6, every integer ℓ ≥ 2 and every
q ∈ [99/100, 1], q = 1 included, A_{ℓ,q} ≥ 0. With Theorem A1, for every 0 < q ≤ 1 the master equation for Φ₋ has no
mode e^{κt}φ(r*) with κ > 0 and φ ∈ L²(ℝ, dr*).

## Status (replaces `STAGE_REPORT.md`, "Status, and what is pencil-only")

| Claim | Label | Second party |
|---|---|---|
| A2-S, ℓ = 2 on [q(1/8), 1] | *certified* (exact) | Kimi: its own NL from its own transcription and the stored design, its own verifier on the four charts, the cover's inequalities exact, and the kit's reproduction (BHM-116) |
| A2-E, ℓ = 3…10 on [q(μ_lo(ℓ)), 1] | *certified* (exact) | Kimi: its own exact route, ℓ = 3's splitting included, with its own μ_lo(ℓ), exact coverage, and the kit's reproduction (BHM-116) |
| G-RES, the residue identity | *certified* (exact), as a gate of A2-S | machine-checked (Lean, BHM-107); Kimi re-derived it symbolically in (ℓ, a, b₀, b₁) (BHM-116) |
| The reduction: Proposition 3 for P C¹ on (0, 1) | *machine-checked* (Lean, BHM-090/091) | complete. Kimi's pencil verdict on its use for the singular design: SOUND (BHM-116) |
| The tortoise map onto ℝ at q = 1, and R's existence | proved (pencil; audited 1×) | Kimi: SOUND (BHM-116), the first audit. The reading's argument for R (addendum 1 §7) agrees |
| P1 Part I (ℓ = 3…10 on [99/100, q(μ_lo(ℓ))]) and Lemma U (ℓ ≥ 11) | *certified* (exact) | Kimi (BHM-065); Lemma U also in Lean (BHM-066) |
| Theorem A2 | *certified*, resting on the rows above | **complete**: every row has its second party. Kimi's pencil verdict on the composition, with the range ends compared exactly: SOUND (BHM-116) |

**What is still pencil only.** R's existence at q = 1 (`results/p3/METHOD_ADDENDUM_1.md` §1), now audited once. Lean takes
R as a hypothesis (BHM-091).

**Cited, not reproved,** as in the report: S5's reduction of the perturbation equations to the master equations.

## Notes from the second party

- **Its route.** Kimi's code is its own: its transcription (BHM-036), exact QQ(μ) arithmetic, and its fixed Bernstein
  verifier (BHM-111), with coefficient-level KATs on boxes of width ≠ 1. The mathematics follows the registered methods,
  as the brief allowed: A2-E's ℓ = 3 splitting, and A2-S's four charts and cover.
- **Its controls all reject.** Two differ from ours:
  - **(d) is its own zero-margin control.** The residue moves to the window's edge, a = −1/3, and p₀ drops by 1/10. Then
    N(0) = 0 exactly at q = 1 and N/z > 0 on [0, 1] there, and the strict check refuses. This isolates the zero margin,
    which our nc-zm did not (addendum 1 §5).
  - **(e) is nc-bound's construction:** the same bump and the same rule for K. Its Q[b] < 0 is right: it integrates over
    the whole support with the form's weights, and C = (3/20)¹³/12012 exactly. But it shares nc-bound's limit
    (addendum 1 §5): the support reaches past U₋'s zero at z = 0.0866846…. And (e)(ii) checks z²N′ on [0, 1], which is 0
    at z = 0, so a strict check refuses it with or without the well. Its printed refusal is a genuine negative value, at
    z = 1/2. Our throat-specific control is d6 (BHM-105).
- **Hosts.** Kimi's own checks ran on host-1 and the kits on host-2. The delivered logs are byte-identical to the copies
  on those nodes. Short development checks ran where Kimi's session lives, as the brief allowed.
- **Reproduction.** Both kits gave KIT PASS. Kimi's 15 `run.log`s are byte-identical to the records. Its 15 records
  equal ours after masking, except `archive_sha256` ("unknown", since `BHM_ARCHIVE` was unset; README, "Re-running").

## Next

Stage 2's three steps are done, each with its second parties: A1 (BHM-067), D = 7–11 (BHM-112) and A2 (this addendum).
What follows is the operator's decision. The lead's close-out report for it comes next.
