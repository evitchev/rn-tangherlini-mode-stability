# PREREG — A2-PILOT: the design pilot for ℓ = 2 near extremality (stage A2, step 1)

*Item BHM-093. 2026-10-24, the bh-modes lead. Step 1 of `TARGET_A2_ADDENDUM_1.md` §4 (BHM-092). Advice: the
session-R lead's reading (BHM-085, §3, item 5). Sealed; any change before the run is a dated addendum.*

## 1. What the pilot is, and what it is not

- **It is untrusted.** It runs in double precision and makes no claim.
- **Its one output** is the degree g of the ℓ = 2 design that A2-S will register, or the finding that none qualifies.
  The latter is kill criterion K3: stop before any run of record.
- **It cannot certify anything.** A design that qualifies here can still fail A2-S's exact verification. That would be
  reported as it stands.
- **The design was chosen from planning data** (numerical; not registered, not results). They are
  `results/planning/a2_design.{py,log}` at `49f70dd` and `a2_design2.{py,log}` at `8ac29e8`. Those runs scored the
  same family at the four rungs and at q = 1. This pilot is therefore not blind to the design's performance there.
  What it adds:
  - the registered rule;
  - samples between the rungs;
  - the gates;
  - and the record.

## 2. Setting, samples, rungs

- **D = 6 (n = 4), ℓ = 2,** in `hd.pilot`'s `Setting`: units r_H = 1, z = 1 − 1/ρ, `TARGET.md` §1's charge parameter μ,
  q = 1 at μ = 0.
- **The samples.** μ = 0 and μ₁ = 1/8 (q = 0.98937…). The rungs 1 − q ∈ {10⁻², 10⁻³, 10⁻⁴, 10⁻⁶}. Nine
  Chebyshev–Lobatto points on [0, μ₁]. And μ₁·2⁻ᵏ for k = 0…12, which reach 1 − q ≈ 6·10⁻¹¹.
- **The grid** for B: `hd.pilot`'s GRID (logistic in τ = log(z/(1 − z)), and uniform), plus points (δ_t/3)·10^{j/40}
  (j = −200…120) that resolve the throat, plus 10^{−j/20} (j = 1…240) for the extremal horizon. z = 0 is left out at
  μ = 0, where P has its pole.

## 3. The design (`TARGET_A2_ADDENDUM_1.md` §3)

  P(z, μ) = a(1 + ε)/(z + ε) + p₀(z),  a = −2/5,  ε = δ_t/6.

- **p₀** is the degree-g Chebyshev–Lobatto interpolant on [0, 1] of P_β − a/z.
  - P_β is the principal solution (P_β ~ a/z) of (1 − z)P_z = P − P² + [W − β₀ − (1 − z)f_zP]/f at q = 1.
  - β₀ = 9(c − a(a + 1)), with c = W(0)/9 at q = 1 (E3: c = −2/9, so β₀ = 4/25).
  - The integration is RK4 in τ with step 1/500, from τ₀ = −27.6 with P = a/z(τ₀).
  - The node z = 0 takes the value at z = 10⁻⁶. The node z = 1 takes the lowered fixed point
    (1 + √(1 + 4(W(1) − β₀)))/2 − a.
  - p₀ does not depend on μ.
- **The scaled slack** σ = min B/B(1) on the grid, with B = N/(64H₋²) = W − [(1 − z)f_zP + f(−P + (1 − z)P_z + P²)] and
  B(1) = W(1) + P(1) − P(1)². σ is undefined if B(1) ≤ 0 or a value is not finite.
- **The degrees** are g ∈ {12, 16, 20, 24, 32}; 32 is the cap. **θ = 10⁻⁴.**
- **The rule.** The design qualifies at g if σ ≥ θ and B(1) > 0 at every sample. The output is the least such g.

## 4. Gates and controls (the run is VALID only if all three are as registered)

| Gate | What | Registered | Why it must |
|---|---|---|---|
| PG-T3 | T3's recorded certificate (BHM-023), first box [3/25, 13/100], at μ = 1/8, under this evaluator | σ > 0 | N > 0 was proved exactly on [0, 1] × that box; a failure means the evaluator is wrong |
| NC-H | The design at the selected degree (the cap if none qualifies), with a replaced by −7/10, at μ = 0 | σ < 0 | −7/10 is outside the window (−2/3, −1/3). B(0⁺) = 9(c − a(a + 1)) = −0.11 < 0. B(1) stays positive, since P(1) only drops by 3/10, so σ is defined |
| NC-B | A planted bound state at q = 1: W − Kb on [3/10, 3/5], b = ((z − 3/10)(3/5 − z))², K = 2I₁/I₂, as in HD-PILOT's NC-B | The design gives σ < 0, and the design rebuilt on the planted potential qualifies at no degree | The trial function b has energy −I₁ < 0, so no N ≥ 0 can exist (Proposition 3) |

**Information,** not gates:
- **The Sturm cross-check.** ψ₁ > 0 at every sample: the regular solution, ψ₁(r_H) = 1, for q < 1; the principal one at
  q = 1. A breakdown (|P| > 10¹², or a value not finite) is a node. It would be reported under K2 as *numerical*.
- **c and β₀ as computed**, against −2/9 and 4/25.

## 5. Runs, hosts, outcome

- **One command:** `kit/a2/run_pilot.sh`. The record runs on host-1, from a `git archive` of the commit that holds this
  file, under `nice -n 19` in `[venv]`. The reproduction runs on host-2, with `BHM_REF` set to the record:
  identical after masking.
- **The verdict:**
  - `VALID: qualifies at degree g`;
  - `VALID: qualifies nowhere (K3)`;
  - `VOID…` (a gate not as registered, or an exception). A VOID run needs a dated addendum and a re-run; it is not a
    kill.
- **The record** has every sample's σ at every degree, the gates, the selected design's Chebyshev coefficients (as
  `float.hex`), the UTC start (masked) and the archive's SHA-256.
- **What follows:**
  - On a qualifying VALID run, A2-S registers this design at degree g, with exact coefficients equal to the binary
    values of these floats, converted to the monomial basis.
  - On K3, A2 stops before the run of record and reports.

## 6. Development tests (synthetic only)

`code/a2/devtest_pilot.py` runs the whole pilot twice on W = 12 − 7x, in place of S5's potential. That W has the same
values at the extremal horizon and at infinity, and is otherwise unrelated. PG-T3 is skipped there, since it needs S5's
potential. The two records must be identical after masking. The outcome is recorded in the registry item.
