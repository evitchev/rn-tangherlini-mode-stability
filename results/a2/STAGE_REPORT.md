# Stage report — A2: D = 6 through extremality (stage 2, step 3)

*The bh-modes lead. Format: `RULES.md` E. Item BHM-102.*
- *The operator's go came on 2026-10-23 at about 22:40 EDT. The box ran one week, to 2026-10-30 (BHM-092). The stage
  finished the same evening: the last run of record started at 03:50 UTC on 2026-10-24, i.e. 23:50 EDT on 2026-10-23.*
- *The item dates from BHM-092 on are UTC (2026-10-24). Local EDT was still 2026-10-23.*

## The result

> **Theorem A2 (certified).** For every integer ℓ ≥ 2 and every q ∈ [99/100, 1], the quadratic form
> ∫(|φ′|² + V_{ℓ,q}|φ|²)dr* of the D = 6 Reissner–Nordström–Tangherlini scalar-type gravitational potential V_S−
> (Kodama–Ishibashi's Φ₋, `TARGET.md` §1) is ≥ 0 on C₀^∞(ℝ). That includes the extremal case, q = 1.
>
> **With Theorem A1** (0 < q ≤ 99/100): for D = 6, A_{ℓ,q} ≥ 0 for every ℓ ≥ 2 and every 0 < q ≤ 1. So the master
> equation for Φ₋ has no exponentially growing mode, through extremality.

- **What is new, relative to the sources read.** Kodama–Ishibashi left charged D ≥ 6 open (S5, *cited*). They also note
  that a horizon-regular S-deformation cannot remove V_S−'s negative region near extremality (S5 l.1884–1888). A2's
  S-deformation is singular at the inner horizon's side of the throat: a pole at z = −δ_t/6, outside the exterior. That
  is how it reaches q = 1. No completeness claim is made (`RULES.md` A7).
- **Not claimed** (`TARGET_A2.md` §2): decay; anything at q = 1 beyond the quadratic form; other sectors.

## The certificates, each with the exact quantity bounded (`RULES.md` E.1)

| Part | Quantity bounded | Certified bound | Item |
|---|---|---|---|
| ℓ = 2, q ∈ [q(1/8), 1], q(1/8)² = 2961/3025 | N(z, μ) for P = −(2/5)(1 + ε)/(z + ε) + p₀(z), ε = w/(3(1 + w)), on four charts covering (0, 1) × [0, 1/8] | NL > 0 on O, O′; NL(μζ, μ)/μ² > 0 on T (least Bernstein coefficient 528353280); NL(z, zσ)/z² > 0 on C. Each in one exact Bernstein box | BHM-101 (A2-S) |
| ℓ = 3, q ∈ [q(11/100), 1] | U₋ = F/Den on the closed exterior, F(1 − s, μ) = μK(μ) + sG(s, μ) | K ≥ 12192768 and G ≥ 275106444444/390625 (min Bernstein); F = 0 only at the extremal horizon | BHM-097 (A2-E) |
| ℓ = 4…10, q ∈ [q(μ_lo(ℓ)), 1] | U₋ on the closed exterior | from U₋ ≥ 917504000000000000/1592858715949 (> 5.7·10⁵, ℓ = 4) to > 9.9·10⁷ (ℓ = 10) | BHM-097 (A2-E) |
| ℓ ≥ 11, q ≤ 1 | m⁻³U₋ | ≥ 959747/17496 | BHM-052 (Lemma U, A1) |

**How the parts compose.**
- **ℓ = 2:** A1's T3 ([0.97277, 0.99020]) overlaps A2-S ([0.98936, 1]).
- **ℓ = 3…10:** A1's P1 covers [0, q(μ_lo)] and A2-E covers [q(μ_lo), 1], with q(μ_lo)² ≥ (99/100)².
- **ℓ ≥ 11:** Lemma U covers every q ≤ 1.
- **How each part gives A ≥ 0:** V ≥ 0 gives A ≥ 0 directly (A2-E, Lemma U). N ≥ 0 gives A ≥ 0 through Proposition 3
  for P that is C¹ on (0, 1) (A2-S).

## Code and logs of record (`RULES.md` E.2)

| Part | Code (commit) | Record (host-1) | Reproduction (host-2) |
|---|---|---|---|
| A2-PILOT (untrusted) | `code/a2/pilot.py` `077c956f76a53a6e` at `5497819` | `results/a2/pilot/runs/record/main/result.json` `26501fe6f55dfd46`, log `93f6dfa39393bc95` | identical after masking; log byte-identical |
| A2-E | `code/a2/elementary.py` `710f91c027e3cf60` at `e422d74` | `results/a2/elementary/runs/record/none/result.json` `ad59836dff7d3362`, log `f8db875b4ba6a236` | 6/6 identical; logs byte-identical |
| A2-S | `code/a2/scert.py` `779fa2acbbdce7d0` at `25c796e` | `results/a2/s/runs/record/none/result.json` `82cdb25c3d8bc005`, log `d640cbb56a42a918` | 9/9 identical; logs byte-identical |

- Every record carries its UTC start time and its archive's SHA-256, as the session-R lead suggested.
- The full hash lists are in each `RESULT.md` and in `SEALED.sha256`.

## One-command re-runs (`RULES.md` E.3)

From a fresh clone at the commit named above, with `BHM_PYTHON` set to the `ENVIRONMENT.md` interpreter:
- `kit/a2/run_pilot.sh`;
- `kit/a2/run_elementary.sh`;
- `kit/a2/run_s.sh`.

Each prints KIT PASS or KIT FAIL. With `BHM_REF` set to the record, each compares itself with it.

## Controls and tampers for every gate (`RULES.md` E.4)

| Part | Planted controls (observed) | Tampers (observed) |
|---|---|---|
| A2-PILOT | NC-H (residue −7/10): σ = −0.283; NC-B (planted bound state): σ = −433, and the lowered solution breaks down at every degree | PG-T3, the evaluator against T3's recorded certificate: σ = 0.109 > 0 |
| A2-E | nc-ell2: REJECT, counterexample −691200 at the corner; nc-strict: REJECT, 0 at ℓ = 3's touching corner; nc-bump: REJECT | td-coeff: REJECT at E0; td-verifier: REJECT at the KATs |
| A2-S | nc-a2 (c′ = −1/4 − 1/36, design-free) and nc-res: REJECT, negative at the blown-up corner; nc-zm: REJECT, exactly 0 there (zero margin); nc-bound: Q[b] < 0 certified in Arb, certificate refused | td-coeff: E0; td-verifier: KAT; td-chart (the blow-up omitted): POS-T; td-cover (a gap): COVER |

**Known answer: not available.** No published case has a negative region reaching a degenerate horizon (the D = 6–11
screen), and D = 5 ℓ = 2 is elementary near extremality (planning data). As `TARGET_A2.md` §5 foresaw, A1's gates G1
and G2, the pilot's PG-T3, and the exact identities G-RES and THROAT stand in. This gap is reported.

## Status, and what is pencil-only (`RULES.md` E.5)

| Claim | Label | Second party |
|---|---|---|
| A2-S | *certified* (exact) | **pending** |
| A2-E | *certified* (exact) | **pending** |
| G-RES, the residue identity (symbolic in ℓ, a) | *certified* (exact), as a gate of A2-S | pending; a Lean candidate |
| The reduction: Proposition 3 for P C¹ on (0, 1) | *machine-checked* (Lean, BHM-090/091) | complete |
| The tortoise map onto ℝ at q = 1, and R's existence | proved (pencil; audited 0×) | **pending** |
| Theorem A2 | *certified*, resting on the rows above and on Lemma U | complete when A2-S's and A2-E's second parties are back |

**Cited, not reproved.** S5's reduction to the master equations, as for A1.

## What changed during the stage

- **The design came from planning data** (numerical; not registered, not results; `results/planning/a2_design*`).
  - The first round showed that the residue-shifted q = 1 solution fails at mid-radius.
  - The second round found the lowered-potential design. Its slack at q = 1 is β₀ = 4/25 by construction, and it has
    σ ≈ 0.8–0.99 at every rung. It already covers 1 − q = 10⁻², so no ordinary rule-2 boxes were needed.
  - The pilot then fixed the degree under registration (BHM-093/095). Its PREREG says it was not blind to the design's
    performance at the rungs.
- **One defect was found by a devtest before registration.** The pilot's extremal Sturm check started below the
  integration's first point (BHM-093).
- **No run of record failed.** No VOID, no kill criterion triggered.
- **Changes from the session-R lead's advice** (BHM-085 §3), each marked in `TARGET_A2_ADDENDUM_1.md`:
  - one design family for the whole range, rather than ordinary boxes plus a singular corner;
  - the pole at δ_t/6 rather than δ_t/3;
  - no known answer.
