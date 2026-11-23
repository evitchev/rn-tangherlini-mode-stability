# A2-S, PREREG addendum 1: a control for every gate, the reading's drills, inward decimals, and a consistency check

*Item BHM-104. 2026-10-24, the bh-modes lead. Registered **after** A2-S's run of record (BHM-101) and **before** these
checks run.*
- *It answers the session-R lead's reading of the A2 stage report (BHM-103, `READING.md` §§3–4):*
  - *eight gates have no planted control or tamper, which RULES.md E.4 requires;*
  - *DIV-T can fail only by an exception, not under its own label;*
  - *the decimals of certified range ends are outward.*
- *`PREREG.md` is sealed and unchanged. No certificate is remade. Sealed.*

## 1. The code change, and why the certificate is unaffected

`code/a2/scert.py` at the commit that holds this file differs from `25c796e` in three ways:
- **New control hooks** (§2). Each acts only under its own `--control` name.
- **Failures under their own labels.** A failed DIV-T or DIV-C now skips its chart and marks its POS check
  "not run", where `25c796e` raised an exception. A failed DESIGN now stops the run with `REJECT: DESIGN`.
- **A failed chart's detail starts with its point**, `at (ζ or z, μ or σ)`, before the exact value, which can run to
  hundreds of digits.

None of this touches the main path. **X1** (§4) checks that: the main run's record must equal BHM-101's sealed record,
apart from timing, provenance and the archive hash.

## 2. The new controls (each must give its registered verdict)

| Control | What it changes | Registered verdict | Why it must |
|---|---|---|---|
| td-H | the H gate is applied to H₋ − 20x (its x-coefficient becomes −10) | `REJECT: H` | the gate sees a negative coefficient |
| td-param | PARAM is applied to `param_n`'s `td-param` (B = 2ℓ + n) | `REJECT: PARAM` | s² = 1 + 4mq²/25 fails |
| td-design | DESIGN compares the pilot record with a sealed hash whose first digit is changed | `REJECT: DESIGN` | the hash does not match |
| td-gres | G-RES's comparison runs on U₋ + x⁴ | `REJECT: G-RES` | the residue identity is off by 16 at x = 2 (the reading's D3) |
| td-L | the L gate runs on −L | `REJECT: L` | −L < 0 |
| td-S | ε_n → −ε_n, which moves the pole to z = +ε inside the exterior, on every path (the reading's D1) | REJECT, with S first and only POS charts after it | S sees ε_n < 0; P has a pole in (0, 1) |
| td-divT | the throat chart is divided by μ³ | `REJECT: DIV-T, POS-T` | NL(μζ, μ) has terms of μ-order 2 |
| td-divC | the corner chart is divided by z³ | `REJECT: DIV-C, POS-C` | NL(z, zσ) has terms of z-order 2 |
| d0 | U₋ − (16/25)H₋²x⁴ with a = −2/5, so c′ = −2/9 − 4/225 = −6/25 = a(a + 1) exactly (the reading's sharp zero margin) | `REJECT: POS-C`, and POS-C's detail must begin `at (0, 0); POS-C: sign*p = 0 <= 0` | C(0, 0) ∝ c′ − a(a + 1) = 0, so the strict bound fails exactly at the blown-up corner and nowhere else |
| d6 | NL − Kμ(z − μ)(3μ − z), K = 128·T(2, 1/64) (the reading's D6): a planted defect that vanishes at μ = 0 | REJECT, with POS-T among the reasons and only POS charts; POS-T's point must have μ ≠ 0 | T(ζ, 0) is unchanged, but T(2, 1/32) < 0; the defect also reaches O and O′ at larger μ |

Together with BHM-100's controls, every gate of A2-S now has a planted control or a tamper:
KAT (td-verifier), E0 (td-coeff), H, PARAM, DESIGN, G-RES, COVER (td-cover), L, S, DIV-T, DIV-C, and the four POS charts
(nc-a2, nc-zm, nc-res, d0, d6).

## 3. X0: inward decimals of the certified range ends (`code/a2/scheck.py`)

Decimals are computed by exact integer square roots from the sealed records, so no float enters (BHM-060's rule). Every
record read is checked against `SEALED.sha256` first. Registered values, as the reading computed them:

| Quantity | Exact | Registered decimal |
|---|---|---|
| A2-S's lower end q(1/8), rounded up at 5 decimals | √(2961/3025) | 0.98937 |
| T3's range, from its sealed record's boxes, lower end up and upper end down at 5 decimals | [√(21576/22801), √(31416/32041)] | [0.97277, 0.99019] |
| T3's upper end, truncated at 8 decimals (for BHM-060's digits) | √(31416/32041) | 0.99019883 |

Also recorded, without a registered value: q(μ_lo(ℓ)) for ℓ = 3…10, from A2-E's sealed record. It is rounded up as A2-E's
lower end and down as P1's upper end, at 7 decimals.

## 4. X1: consistency of the main path

The kit's `none` job reruns A2-S's main certificate. `a2.scheck` compares its record with BHM-101's sealed record
(`results/a2/s/runs/record/none/result.json`) after removing timing, provenance and the archive hash. They must be
identical.

## 5. Runs, hosts, development tests

- **One command:** `kit/a2/run_s_check.sh`.
  - It checks the environment first, now including gmpy2 2.3.2, and exits 2 on a mismatch. This answers the reading's §4.3.
  - The record runs on host-1, and the reproduction on host-2 with `BHM_REF`. Both run from a `git archive` of the
    commit that holds this file, under `nice -n 19`.
- **The verdict** of the whole addendum is VERIFIED if every job ends as registered. The kit then prints KIT PASS.
- **Development tests** (`code/a2/devtest_scheck.py`, synthetic W = 12 − 7x with its own design, as in BHM-100):
  **18/18 as expected** at `fdf8765` on host-2.
  - The new controls' verdicts on the synthetic potential.
  - A design outside the family is refused under DESIGN, and td-design's changed hash refuses the sealed pilot record.
  - G-RES on U₋ + x⁴ fails with difference 16.
  - `decimal` on √2 and on an exact square.
  - The record comparison's masking.
  - The kit's shell matching was tested on sample lines and verdicts on host-2.

## 6. What follows

`RESULT_ADDENDUM_1.md` reports these checks. The corrections the reading asks for are separate items, filed with that
result:
- nc-zm's cause (RESULT.md:43);
- nc-bound's wording;
- A2-E's PREREG inequality;
- the outward decimals, including BHM-060's;
- the stage report's status row and headline.
