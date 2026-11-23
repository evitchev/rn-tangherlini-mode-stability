# Stage report — D = 7–11: all ℓ ≥ 2, 0 < q ≤ 99/100 (stage 2, step 2)

*2026-10-23, the bh-modes lead. Item BHM-079. The format is `RULES.md` E. The operator's time box (BHM-046) was
about two weeks from 2026-10-23, to 2026-11-06; the step started and ended the same day. A report follows each
step (BHM-046).*

## The result

> **Theorem HD (certified).** For D = 7, 8, 9, 10, 11, every integer ℓ ≥ 2 and every q ∈ (0, 99/100], the quadratic
> form ∫(|φ′|² + V_{ℓ,q}|φ|²)dr* of the D-dimensional Reissner–Nordström–Tangherlini scalar-type gravitational
> potential V_S− (Kodama–Ishibashi's Φ₋, `TARGET_HD.md` §1) is ≥ 0 on C₀^∞(ℝ). So the master equation has no
> exponentially growing mode.

**With Theorem A1 (D = 6), every D = 6–11 is certified at q ≤ 99/100, for all ℓ.** That completes BHM-027's
fallback deliverable: D = 6–11 for q ≤ 99/100, the exact D = 6 onset (BHM-017) and the extremal margins
(BHM-049). A2 is the step that remains.

**Why it is new.**
- Kodama and Ishibashi left the charged case open for D ≥ 6 ("d ≥ 6?", S5, *cited*).
- The certified range contains 18 bands in which V has a negative region, so positivity of V does not settle it:
  - 13 open at an onset q_on > 0, one of them in the interior (D = 10 ℓ = 3, from q ≈ 0.49);
  - 5 are negative from q = 0⁺. S6's S-deformation covers those only at Q = 0.
- This is relative to the sources read (`results/screen/PREREG.md` §1.5). It is not a completeness claim.

## The certificates, each with the exact quantity it bounds (`RULES.md` E.1)

| Part | Quantity bounded | Certified bound | Item |
|---|---|---|---|
| HD-E, E1 | U₋(x; q) on {0 ≤ x ≤ x_H(q), q ≤ 99/100}, as F(t, μ)/Den(μ), for ℓ_el(D) ≤ ℓ ≤ ℓ₀(D); ℓ_el = 4, 5, 6, 6, 7 and ℓ₀ = 10, 10, 11, 13, 14 | U₋ > 0, at the first Bernstein node; the lower bounds are in HD-E's `result.json` | BHM-063 |
| HD-E, E2 | the same, on the 13 bands with an onset, for q ≤ q_split | U₋ > 0, with lower bounds from ≈ 136 (D = 10 ℓ = 3) to ≈ 10⁵ | BHM-063 |
| HD-E, E3 | m⁻³U₋ = Pos_n − Neg_n on [0, ε̄] × [0, 1/(n + 1)] × [0, 2], for ℓ > ℓ₀(D) and q ≤ 1 | m⁻³U₋ ≥ 38.6, 23.6, 7.19, 4.84, 3.03 (D = 7…11), exact rationals | BHM-063 |
| HD-S | N(z, μ)·L(μ)·s^{2e} for the 231 stored P̂ (P = P̂/s^e), on [0, 1] × each μ-box, together with L > 0 | > 0 on every box, closed; exact Bernstein, 919 leaves; degree ≤ (96, 16) | BHM-078 |

**How the parts compose.**
- V ≥ 0 gives A ≥ 0 directly. N ≥ 0 gives A ≥ 0 through `results/p3/METHOD.md`'s Proposition 3, on each μ-box.
- Every ℓ < ℓ_el(D) is one of the 18 bands.
- For a band with an onset, HD-S's exact interval starts at q(μ_b) ≤ q_split, below the top of HD-E's E2 range.

## Code and logs of record (`RULES.md` E.2)

| Part | Code (commit) | Record | Reproduction |
|---|---|---|---|
| HD-E | `code/hd/elementary.py` `b77e92151ca9d7f6` at `6fe9689` | host-1, `results/hd/elementary/runs/record/main/result.json` `bb06c9023b0f7ad0`, log `d9454332450335d9` | host-2, identical; logs byte-identical |
| HD-PILOT (untrusted) | `code/hd/pilot.py` `27f7bac39f0d36a7` at `710488b` | host-1, `results/hd/pilot/runs/record/main/result.json` `10e04bf69e70c579` | host-2, identical |
| HD-S | `code/hd/scert.py` `8a67a9e6d381a6a2` at `0aa2673` | host-1, `results/hd/s/runs/record/` (34 records) | host-2, identical; logs byte-identical |

The full hash lists are in each `RESULT.md` and in `SEALED.sha256`.

## One-command re-runs (`RULES.md` E.3)

From a fresh clone at the commit named above, with `BHM_PYTHON` set to the `ENVIRONMENT.md` interpreter, run
`kit/hd/run_elementary.sh`, `kit/hd/run_pilot.sh` and `kit/hd/run_s.sh`. Each prints KIT PASS or KIT FAIL and
compares itself with the run of record. `kit/hd/run_s.sh` runs 8 jobs at a time, and the whole of HD-S takes about
three minutes on one node.

## Controls and tampers for every gate (`RULES.md` E.4)

| Part | Planted control (observed) | Tamper (observed) |
|---|---|---|
| HD-E | REJECT, each with an exact counterexample or failed check:<br>• NC-E1, past a horizon onset: at the horizon corner;<br>• NC-E2, past the interior onset: at an interior node;<br>• NC-E3, a band from 0⁺ at small q;<br>• NC-E4, coverage;<br>• NC-E5, the uniform bound below its range | TD-E1, a coefficient: REJECT at E0n; TD-E2, the parametrisation: REJECT in every job; TD-E3, the verifier: REJECT at the KATs |
| HD-PILOT | NC-B, a planted bound state: qualifies nowhere, σ = −679; PG1/PG2, the certified designs have σ > 0 | NC-H, the horizon bound: σ = −0.996 (after addendum 1) |
| HD-S, per D | NC-S, a planted bound state scaled to that D's potential: Q[b] certified < 0 (−1.16·10⁻⁶ to −2.02·10⁻⁶) and the certificate REJECTed on it | TD-S1, a coefficient: REJECT at E0n; TD-S2, P(0) above the horizon bound: REJECT, with an exact counterexample at z = 0; TD-S3, the verifier (once): REJECT at the KATs |

**Known answers.** G-S6: for the five bands from 0⁺, the box containing Q = 0 verified, which reproduces S6's
theorem at those parameters. S14's Table I is consistent with the result (ℓ = 2 modes damped; *cited*, *numerical*).

## Status, and what is pencil-only (`RULES.md` E.5)

| Claim | Label | Second party |
|---|---|---|
| HD-E E1, E2 | *certified* (exact) | Kimi: a sealed brief, to be relayed (BHM-068) |
| HD-E E3, Lemma U(n) | *certified* (exact); steps (a)–(d) proved (pencil; audited 0×) | Kimi (the same brief); Lean offered to session-L |
| HD-S, all 18 bands | *certified* (exact); the reduction proved (pencil; audited 2×; Lean, BHM-030) | the blind replication of D = 7 ℓ = 2 (the session-R lead's seat, BHM-077); Kimi: a sealed brief, to be relayed (BHM-080) |
| Theorem HD | *certified*, resting on the rows above | complete when these are back |

**Cited, not reproved.** As for A1: S5's reduction of the perturbation equations to the master equations, and S5's
results for the other sectors. They make Theorem HD a statement about no growing linear gravito-electromagnetic
modes.

**Unaudited pencil.** Lemma U(n)'s steps (a)–(d) at general n (`results/hd/elementary/PREREG.md` §3). They are the
same four steps Kimi audited at n = 4.

## What changed during the step

- **HD-PILOT's first run was VOID** (BHM-072), on a defect in the registration's horizon control. That control
  shifted P by a constant, which also moved P at infinity and left the scaled slack undefined. A registered
  addendum fixed it before the re-run (BHM-073), and the re-run was VALID (BHM-074). The VOID run stays on the
  record. The re-run reproduced it in every other field.
- **q_max(D) = 99/100 for every D** (BHM-075), the top rung of the registered ladder. The zero-margin throats
  needed nothing special at q ≤ 0.99.
- **The blind slot** went to this step's first S-certificate band, by the operator's ruling (BHM-064).

## Next (the operator's order, BHM-027)

1. **Second parties:**
   - Kimi's briefs for HD-E and HD-S (to be relayed by the operator);
   - the blind replication;
   - the session-R lead's one-hour reading of this report (`RULES.md` E).
2. **A2** (D = 6, q ∈ [99/100, 1]): one week, with a kill criterion registered in advance.
3. **Not in the order:** D = 7–11 beyond q = 0.99. `TARGET_HD.md` §4.1 caps q_max at 0.99, so going further needs
   the operator's ruling and a pilot past 1 − q = 10⁻².
