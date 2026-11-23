# Stage report — A1: D = 6, all ℓ ≥ 2, 0 < q ≤ 99/100 (stage 2, step 1)

*2026-10-23, the bh-modes lead. The format is `RULES.md` E. The operator's time box (BHM-046) was
about three days from 2026-10-23; the step started and ended the same day. A report follows each
step (BHM-046). Item BHM-055.*

## The result

> **Theorem A1 (certified).** For every integer ℓ ≥ 2 and every q ∈ (0, 99/100], the quadratic
> form ∫(|φ′|² + V_{ℓ,q}|φ|²)dr* of the D = 6 Reissner–Nordström–Tangherlini scalar-type
> gravitational potential V_S− (Kodama–Ishibashi's Φ₋, `TARGET.md` §1) is ≥ 0 on C₀^∞(ℝ). So the
> master equation has no exponentially growing mode.

**Why this is new.** Kodama–Ishibashi left charged D ≥ 6 open ("d ≥ 6?", S5, *cited*). The certified
range contains a band, ℓ = 2 and q ∈ (q_*, 0.99], where V has a negative region and no published
S-deformation applies (BHM-017, O3 and O4). That meets the charter's primary-success condition
(CHARTER e4), once P1's second-party check is back. This is relative to the sources read (`results/screen/PREREG.md` §1.5); it is not a
completeness claim.

## The certificates, each with the exact quantity it bounds (`RULES.md` E.1)

| Part | Quantity bounded | Certified bound | Item |
|---|---|---|---|
| ℓ = 2, q ≤ q_* | U₋(x; q) on {0 ≤ x ≤ x_H(q), 0 ≤ q ≤ q_*}; q_*² is the real root of 3025Y³ − 31521Y² + 99792Y − 68796 | U₋ ≥ 0, with equality only at (q_*, x_H(q_*)). Exact Bernstein on three regions and a corner lemma | BHM-017 (O2) |
| ℓ = 2, q ∈ [0.97277, 0.99020] | N(z, μ) = U₋ − 64H₋²[(1 − z)f_zP + f(−P + (1 − z)P_z + P²)] for the eight stored P (T3) | N > 0 on [0, 1] × each μ-box, closed: exact Bernstein, degree (68, 16), 3 boxes each | BHM-023 (T3) |
| ℓ = 3…10, q ≤ 99/100 | U₋(x; q) on the exterior, as F(t, μ)/Den(μ) | U₋ ≥ 1.95·10⁴ (ℓ = 3), rising to ≥ 1.38·10⁷ (ℓ = 10); exact values in `RESULT.md` | BHM-052 (P1, Part I) |
| ℓ ≥ 11, q ≤ 1 | m⁻³U₋ = P(ε, κ, x) = Pos − Neg on [0, 1/12] × [0, 1/5] × [0, 2] | m⁻³U₋ ≥ 64 − Neg(1/12, 1/5, 2) = 959747/17496 ≈ 54.86 | BHM-052 (Lemma U) |

**How the parts compose.** V ≥ 0 gives A ≥ 0 directly, and N ≥ 0 gives A ≥ 0 through
`results/p3/METHOD.md` Proposition 3. The overlap [0.97277, q_*] is covered twice.

## Code and logs of record (`RULES.md` E.2)

| Part | Code (commit) | Record | Reproduction |
|---|---|---|---|
| O2 | `code/onset/` at `180824b` | host-1, `results/onset/RESULT.md` | host-2, identical |
| T3 | `code/p3/scert.py` at `782fc56` | host-1, `results/p3/RESULT.md` (T3 `f893d820aa0f289f`) | host-2, identical |
| P1 | `code/a1/p1.py` `7e5fac94a3a51087` at `3625bf0` | host-1, `results/a1/runs/record/main/result.json` `58b9850b6cd76077`, log `4c086d6acd9d9e3b` | host-2, identical; logs byte-identical |

The full hash lists are in each `RESULT.md` and in `SEALED.sha256`.

## One-command re-runs (`RULES.md` E.3)

From a fresh clone, at the commit named above, with `BHM_PYTHON` set to the `ENVIRONMENT.md`
interpreter: `kit/onset/run.sh`, `kit/p3/run.sh` and `kit/a1/run.sh`. Each prints KIT PASS or
KIT FAIL and compares itself with the run of record. `kit/p3/run.sh` prints KIT FAIL by design: its
registered gate G1 fails under design rule 1. Design rule 2 is `kit/p3/run_rule2.sh` (KIT PASS).

## Controls and tampers for every gate (`RULES.md` E.4)

| Part | Planted control (observed) | Tamper (observed) |
|---|---|---|
| O2 | NC-O2, positivity claimed past the onset: REJECT, exact counterexample | TD-O1, coefficient: REJECT; TD-O2, the corner lemma inverted: REJECT |
| T3 | NC-P1, a planted bound state: REJECT, the certificate refused with a certified trial function | TD-P1, coefficient: REJECT; TD-P2, P(0) above the horizon bound: REJECT, exact counterexample |
| P1 | NC-A1a, ℓ = 2's real negative region: REJECT at (1, 121/1000); NC-A1b, a planted bump: REJECT at (1/2, 11/100); NC-A1c, coverage: REJECT; NC-A1d, the uniform bound below its range: REJECT | TD-A1a, coefficient: REJECT at E0; TD-A1b, a dropped monomial: REJECT; TD-A1c, a tampered verifier: REJECT at the KATs |

**Gate G1**, Q = 0 at D = 10 for ℓ = 2, a known answer with a negative region, passed with design
rule 2 (BHM-025).

## Status, and what is pencil-only (`RULES.md` E.5)

| Claim | Label | Second party |
|---|---|---|
| O2 | *certified* (exact); corner argument re-derived independently | Kimi (BHM-037); Lean (BHM-030) |
| T3 | *certified* (exact) | Kimi (BHM-036, re-run BHM-040); session-L's run in progress (BHM-044, BHM-046) |
| S-deformation reduction (p3 METHOD) | proved (pencil; audited 2×); Lemmas 1–2 and Prop. 3 machine-checked (Lean) | Kimi, Fable (BHM-036, BHM-042); Lean (BHM-030) |
| P1 and Lemma U | *certified* (exact); pencil steps (a)–(d) proved (pencil; audited 0×) | **pending**: a sealed Kimi brief, its runs of record on host-1/005 |
| Theorem A1 | *certified*, resting on the four rows above | complete when P1's second party is back |

**Cited, not reproved.** S5's reduction of the perturbation equations to the master equations, and
S5's results for the other sectors (tensor and vector types, Φ₊), are *cited*. They make Theorem
A1 a statement about no growing linear gravito-electromagnetic modes (`TARGET.md` §2).

**Unaudited pencil.** Lemma U's steps (a)–(d) (`results/a1/PREREG.md` §3). They are short: one
algebraic identity, two inequalities, and a monotonicity argument.

## What changed during the step

- **A failed first attempt** (BHM-050). It was a defect in writing the record, not in the
  certificate. It was fixed by a registered addendum (BHM-051) before the re-run, and it stays on
  the record.
- **Fable's wording fixes** to both METHODs are in, as addenda (BHM-054), with one correction item
  (BHM-053). The correction is to the 1c PREREG's recursion formula; the code was right.

## Next (the operator's order)

1. **Second party for P1:** a Kimi brief, sealed with this report.
2. **D = 7–11 at q ≤ 99/100**, about two weeks, with a per-D q_max registered in advance.
   - The exact extremal margins are now certified for every D: c_n + 1/4 = (2ℓ − n + 1)²/(4(n − 1)²)
     (BHM-049). That puts the zero-margin cases exactly at D = 2ℓ + 3.
   - The blind slot is kept for the first result of this step (BHM-046).
3. **A2**, one week. Lemma U already covers ℓ ≥ 11 up to q = 1.
