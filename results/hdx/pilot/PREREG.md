# PREREG — HD-X-PILOT: the design pilot for the 11 non-critical bands of D = 7–11 near extremality (HD-X-1, step 1)

*Item BHM-129. 2026-10-26, the bh-modes lead. Step 1 of `TARGET_HD_ADDENDUM_2.md` §4 (BHM-121). The code was written by
a fork of the lead (BHM-120) and read by the lead: `code/hdx/pilot.py`, `code/hdx/bands.py`, `code/hdx/gate.py` and
`kit/hdx/run_pilot.sh`, at the commit that holds this file. Sealed; any change before the run is a dated addendum.*

## 1. What the pilot is, and what it is not

- **It is untrusted.** It runs in double precision and makes no claim.
- **Its one output** is, for each band, the degree g of the design that HD-X-S will register, or the finding that none
  qualifies. The latter is kill criterion K3 for that band: it stops before its run of record.
- **It cannot certify anything.** A design that qualifies here can still fail HD-X-S's exact verification. That would
  be reported as it stands.
- **Not blind.** The scoping (`results/planning/stage3_2026-10-25/hdx/`) and the fork's development runs ran this
  construction on S5's potentials. The development runs were per band at `a007614` and for all bands at `bb23ba2`, in
  the fork's clone, with the same code as here. Every band qualified, at degree 12–20, with the least σ ≈ 0.117 at
  D = 10 ℓ = 4. What this registration adds: the rule fixed in advance, the gates, and the record of record.

## 2. Setting, bands, samples

- **The bands** (`hdx.bands.BANDS`): the 11 bands of D = 7–11 that reach q = 1 with 2ℓ > n − 1. They are D = 7 ℓ = 3;
  D = 8 ℓ = 3, 4; D = 9 ℓ = 4, 5; D = 10 ℓ = 4, 5, 6; and D = 11 ℓ = 5, 6, 7. A critical band (2ℓ ≤ n − 1) is refused.
- **The setting:** `hd.pilot`'s units (r_H = 1, z = 1 − 1/ρ, q = 1 at μ = 0). f and f_z are computed without
  cancellation near the horizon: 1 − (1 − z)^{n−1} = −expm1((n − 1)·log1p(−z)).
  - `hd.pilot.Setting`'s f loses relative accuracy like ε/z there: 1.6·10⁻³ at z = 10⁻¹⁴, against 4.4·10⁻¹⁶ for the
    new form (the fork's devtest).
  - The gate band runs with the old f, as `--legacy-f`.
- **The samples,** per band:
  - q = 1 and μ₁ = 1/8, where PARAM checks q(1/8)² ≤ (99/100)² exactly in HD-X-S;
  - the rungs 1 − q ∈ {10⁻², 10⁻³, 10⁻⁴, 10⁻⁶};
  - nine Chebyshev–Lobatto points on [0, μ₁];
  - μ₁·2⁻ᵏ for k = 0…12.
- **The grid** for B: `hd.pilot`'s GRID, plus points that resolve the throat (scale δ_t/(n − 1)) and the extremal
  horizon, as A2-PILOT's.

## 3. The design (`TARGET_HD_ADDENDUM_2.md` §3)

  P(z, μ) = a(1 + ε)/(z + ε) + p₀(z),  a = a_pr + θ(a_ot − a_pr),  θ = 1/5,  ε = w/((n − 1)(1 + w)).

- a and β₀ = (n − 1)²(c − a(a + 1)) = θ(1 − θ)(2ℓ − n + 1)² are exact, per band (`hdx.bands.residues`), from 4/25 (D = 8
  ℓ = 3, D = 10 ℓ = 4) to 144/25 (D = 11 ℓ = 7).
- **p₀** is the degree-g Chebyshev–Lobatto interpolant on [0, 1] of P_β − a/z.
  - P_β is the principal solution (P_β ~ a/z) of the q = 1 Riccati equation for the lowered potential W − β₀.
  - It is integrated by RK4 in τ from τ₀ = −27.6, with step 0.002, as A2-PILOT does.
  - p₀ does not depend on μ.
- **The scaled slack** σ = min B/B(1) on the grid, with B = N/(64H₋²). σ is undefined if B(1) ≤ 0 or a value is not
  finite.
- **The rule:**
  - the degrees are g ∈ {12, 16, 20, 24, 32}, with 32 the cap, and θ_σ = 10⁻⁴;
  - a band qualifies at g if σ ≥ θ_σ and B(1) > 0 at every sample;
  - the output is the least such g.

## 4. Gates and controls, per band (the run is VALID only if all are as registered)

| Gate | What | Registered | Why it must |
|---|---|---|---|
| C-EXACT | the float c = W(0)/(n − 1)² at q = 1 against `hdx.bands`' exact c | relative difference ≤ 10⁻⁹ | the setting's potential is S5's |
| PG-HDS | HD-S's recorded certificate (BHM-078) on the band's first box, at its lower end μ_a (q(μ_a) ≥ 99/100), under this evaluator | σ > 0 | N > 0 was certified exactly on that box. Not run for D = 10 ℓ = 6 and D = 11 ℓ = 7, which open above q = 0.99 and have no HD-S record; their other gates apply |
| NC-H | the design at the selected degree (the cap if none qualifies), with a replaced by a_nc = a_ot − (a_pr − a_ot)/10, at μ = 0 | σ < 0 | a_nc lies outside the window, so B(0⁺) ∝ c − a(a + 1) < 0, while B(1) stays positive |
| NC-B | a planted bound state at q = 1: W − Kb on WELL's support [z₀/5, 4z₀/5] (rounded inward to 1/1000), inside U₋ < 0, b = ((z − z_a)(z_b − z))², K = 2I₁/I₂ | the design gives σ < 0, and the design rebuilt on the planted potential qualifies at no degree | b has energy −I₁ < 0, so no N ≥ 0 can exist (Proposition 3). The support lies inside U₋ < 0, unlike nc-bound's (BHM-106 §5) |

**The run-level gate, gate-a2.** `hdx.pilot --gate-a2 --legacy-f` runs the gate band (D = 6 ℓ = 2) with A2-PILOT's
constants and gates in this engine. Its record must equal A2-PILOT's record of record (BHM-095) in every field but
claim, provenance, archive and timing (`hdx.gate --kind pilot`).

**Information,** not gates:
- **The Sturm cross-check:** ψ > 0 at every sample. For q < 1 that is the regular solution; at q = 1 it is the
  throat-principal one, started at a_pr. A breakdown is a node, reported under K2 as *numerical*.
- **c and β₀ as computed.**

## 5. Runs, hosts, outcome

- **One command:** `kit/hdx/run_pilot.sh`, with two jobs: `main` (every band) and `gate-a2`.
- **Hosts:**
  - the record on host-1, from a `git archive` of the commit that holds this file, under `nice -n 19` in
    `[venv]`;
  - the reproduction on host-2, with `BHM_REF` set to the record: identical after masking.
- **The verdict of `main`:**
  - `VALID`, with each band qualifying at its g, or K3 for a band that qualifies nowhere;
  - `VOID…` if a gate is not as registered or an exception occurs. A VOID run needs a dated addendum and a re-run; it is
    not a kill.
- **The kit** prints KIT PASS only if `main` is VALID with no K3, and `gate-a2` is VALID and equals A2-PILOT's record.
  A KIT FAIL caused only by a band's K3 is an outcome, not a defect: that band stops (K3).
- **The record** has, per band, every sample's σ at every degree, the gates, and the selected design's Chebyshev
  coefficients (as `float.hex`). It also has the UTC start (masked) and the archive's SHA-256.
- **What follows:**
  - on a VALID run, HD-X-S registers each qualifying band's design, with exact coefficients equal to the binary values
    of these floats, converted to the monomial basis;
  - the record is sealed, and HD-X-S's gate DESIGN reads it by its SHA-256.

## 6. Development tests

`code/hdx/devtest_pilot.py` runs the pilot on a synthetic potential, W_syn = (n − 1)²c·x/2 + (m + n(n + 2)/4)(1 − x/2),
with each band's exact c. That gives the right values at the extremal horizon and at infinity, and is otherwise
unrelated.
- It covers the gate band and two bands, twice each, and the records must be identical.
- It also tests the accuracy of f.
- PG-HDS needs S5's potential and is not run there.

**Results:** 15/15 at `bb23ba2`, in the fork's clone, on host-2. The rerun at `c4b6d3e`, in this repository, on host-1:
15/15 as expected, DEVTEST PASS (`[run-folder]/dev-hdxs-c4b6d3e/devtest_pilot.log`).
