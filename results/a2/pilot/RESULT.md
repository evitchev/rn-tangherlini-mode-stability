# A2-PILOT RESULT: VALID, the design qualifies at degree 12 (BHM-095)

*2026-10-24, the bh-modes lead. Registration: `PREREG.md` (BHM-093, SHA-256 `dba6c8815b3e8a7d…`), sealed before the
run. The record ran on host-1 and the reproduction on host-2, from a `git archive` of `5497819` (archive SHA-256
`a87c1d71bf873c4b…`) with `kit/a2/run_pilot.sh`. UTC start 03:29:02; 13 s.*
- *Both kits print KIT PASS. The reproduction is identical to the record after masking, and the `run.log`s are
  byte-identical.*
- *Untrusted: double precision, no claim (`PREREG.md` §1).*

## The outcome

**`VALID: qualifies at degree 12`.** The ℓ = 2 design of `TARGET_A2_ADDENDUM_1.md` §3 meets the rule at the least
registered degree:

  P(z, μ) = −(2/5)(1 + ε)/(z + ε) + p₀(z),  ε = δ_t/6,  p₀ of degree 12,

with σ ≥ θ = 10⁻⁴ and B(1) > 0 at all 26 samples. The minimum over samples is **σ = 0.7546**, at q = 1 (μ = 0).

| Sample | q | σ at degree 12 (16, 24) |
|---|---|---|
| μ = 0 | 1 | 0.755 (0.880, 0.894) |
| 1 − q = 10⁻⁶ | 0.999999 | 0.766 (0.885, 0.901) |
| 1 − q = 10⁻⁴ | 0.9999 | 0.859 (0.904, 0.909) |
| 1 − q = 10⁻³ | 0.999 | 0.935 (0.971, 0.963) |
| 1 − q = 10⁻² | 0.99 | 0.923 (0.981, 0.977) |
| μ = 1/8 | 0.98936… | 0.923 (0.981, 0.977) |

All samples are in `runs/record/main/run.log` and `result.json`. Every sample in between, down to μ = 1/8·2⁻¹²
(1 − q ≈ 6·10⁻¹⁰), has σ > 0.75. The selected design's 13 Chebyshev coefficients are in the record as `float.hex`.

## Gates (all as registered)

| Gate | Registered | Observed |
|---|---|---|
| PG-T3: T3's recorded certificate, first box [3/25, 13/100], at μ = 1/8 | σ > 0 | σ = 0.109 (minimum at z = 0) |
| NC-H: the residue moved to −7/10, at q = 1 | σ < 0 | σ = −0.283 (minimum at z = 0.289); B(1) = 2.156 > 0, so σ is defined |
| NC-B: planted bound state at q = 1, K = 137261, I₁ = 9.1·10⁻⁷ > 0 | design σ < 0; no rebuilt design qualifies | design σ = −433; the lowered solution breaks down at every degree (z ≈ 0.455) |

**Information.** c = W(0)/9 = −0.22222222222222196 (−2/9) and β₀ = 0.16000000000000228 (4/25).
- **The Sturm cross-check.** ψ₁ has no breakdown at any sample. Its minimum, with ψ₁(r_H) = 1, falls from 0.973 at
  μ = 1/8 to 0.086 at μ = 1/8·2⁻¹². That is the throat's ψ ~ z^{−1/3} profile setting in. At q = 1 the principal
  solution has no breakdown either.
- **So no node:** A_{2,q} ≥ 0 *numerically* on the whole range. K2 does not apply.

## Status and what follows

- The pilot passes its rule; K3 does not apply.
- **A2-S registers this design** at degree 12. Its exact coefficients are the binary values of the recorded floats,
  converted to the monomial basis, and A2-S's exact verification is the trust base.
- **Theorem A2:** *conjecture*, unchanged.

## Hashes (SHA-256, first 16 hex)

- Code at `5497819`: `code/a2/pilot.py` `077c956f76a53a6e`; `kit/a2/run_pilot.sh` `fc1b5df468bad51a`.
- Record: `runs/record/main/result.json` `26501fe6f55dfd46`, `run.log` `93f6dfa39393bc95`.
- Reproduction: `runs/repro-host-2/main/result.json` `17828b4150ab7f65`, `run.log` `93f6dfa39393bc95`.
