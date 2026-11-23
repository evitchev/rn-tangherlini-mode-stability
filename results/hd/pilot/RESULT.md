# RESULT — HD-PILOT: q_max(D) = 99/100 for D = 7–11 (BHM-074)

*Registered as BHM-069 (`PREREG.md`), with addendum 1 (BHM-073), which was written after the VOID attempt at
`8c2d6d2` (BHM-072). The run of record was on host-1 and the reproduction on host-2, both from a
`git archive` of `710488b`.*
- *They are identical after masking, and the `run.log`s are byte-identical.*
- *The added consistency check holds: the re-run equals the VOID attempt in every field except NC-H's entry
  and the verdict.*
- *The run takes 305 s, and `kit/hd/run_pilot.sh` gives KIT PASS on both nodes.*

**VALID as registered.** The pilot is untrusted. It fixes q_max(D) and the band designs; it certifies
nothing.

## Gates and controls

| Name | Registered | Observed |
|---|---|---|
| PG1 | σ > 0 for the certified rule-2 designs T1 and G1 | T1 σ = 0.06447; G1 σ = 0.02658 |
| PG2 | σ ≥ θ for the pilot's own designs there | T1 σ = 0.06447; G1 σ = 0.02658 (equal to PG1's to six digits: the pilot reproduces p3's design) |
| NC-H | σ < 0 for T1's design plus c(1 − z), c = 0.1206 | σ = −0.996, with the minimum at z = 0.682 (B(0) < 0 as well) |
| NC-B | a planted bound state qualifies nowhere, and G1's design gives σ < 0 on it | the integration breaks down at the planted zero of ψ₁; no qualifying design; σ = −679 |

## The decision

**q_max(D) = 99/100 for D = 7, 8, 9, 10 and 11.** Every band active at every rung qualifies with ε = 1/50,
so the fallback ε = 1/200 was never needed.

## The designs at q_max = 99/100 (adopted by HD-S, `TARGET_HD_ADDENDUM_1.md`)

All use ε = 1/50. "Least degree" is the smallest degree that qualifies in each variable. σ is the scaled
slack, θ = 10⁻⁴.

| D | ℓ | kind, q_lo | design | least degree, z / ζ | min σ of the design over the 9 charges | min ψ₁ | the exact design's own σ |
|---|---|---|---|---|---|---|---|
| 7 | 2 | onset, 0.948 | z, 20 | 20 / 32 | 0.0506 | 0.891 | 0.0719 |
| 7 | 3 | onset, 0.977 | z, 16 | 16 / 24 | 0.00627 | 0.986 | 0.0218 |
| 8 | 2 | from 0⁺ | z, 24 | 24 / 40 | 0.0454 | 0.742 | 0.0449 |
| 8 | 3 | onset, 0.944 | z, 20 | 20 / 24 | 0.0151 | 0.901 | 0.0236 |
| 8 | 4 | onset, 0.983 | z, 20 | 20 / 24 | 0.00303 | 0.996 | 0.0097 |
| 9 | 2 | from 0⁺ | z, 28 | 28 / 40 | 0.0403 | 0.626 | 0.0444 |
| 9 | 3 | onset, 0.921 | z, 24 | 24 / 28 | 0.0180 | 0.799 | 0.0237 |
| 9 | 4 | onset, 0.952 | z, 24 | 24 / 24 | 0.00947 | 0.930 | 0.0101 |
| 9 | 5 | onset, 0.987 | ζ, 20 | 24 / 20 | 0.00152 | 1.000 | 0.00497 |
| 10 | 2 | from 0⁺ | z, 32 | 32 / 48 | 0.0409 | 0.545 | 0.0420 |
| 10 | 3 | onset, 0.490 (interior) | z, 28 | 28 / 32 | 0.0149 | 0.699 | 0.0154 |
| 10 | 4 | onset, 0.920 | z, 24 | 24 / 28 | 0.00281 | 0.847 | 0.00983 |
| 10 | 5 | onset, 0.961 | ζ, 24 | 28 / 24 | 0.00399 | 0.954 | 0.0051 |
| 11 | 2 | from 0⁺ | z, 32 | 32 / 48 | 0.00136 | 0.487 | 0.0387 |
| 11 | 3 | from 0⁺ | z, 32 | 32 / 40 | 0.0133 | 0.618 | 0.0134 |
| 11 | 4 | onset, 0.897 | z, 28 | 28 / 32 | 0.00771 | 0.762 | 0.00941 |
| 11 | 5 | onset, 0.929 | z, 28 | 28 / 28 | 0.00189 | 0.884 | 0.0049 |
| 11 | 6 | onset, 0.968 | ζ, 24 | 32 / 24 | 0.00221 | 0.971 | 0.00285 |

## Observations (planning information, not claims)

- **The zero-margin throats need nothing special at q ≤ 0.99.** D = 7 ℓ = 2, D = 9 ℓ = 3 and D = 11 ℓ = 4 qualify
  in z at degrees 20, 24 and 28. Their least degrees barely change between the rungs 0.97 and 0.99.
- **The Möbius variable ζ wins for three high-ℓ bands:** D = 9 ℓ = 5, D = 10 ℓ = 5 and D = 11 ℓ = 6, by 4 to 8 in
  degree.
- **ζ loses for the bands from 0⁺,** which need degree 40–48 in ζ against 24–32 in z. Their samples run down to
  q = 0, where δ_t = 1 and ζ compresses the far region.
- **The IB lead's conjecture is not tested here.** It says ζ keeps the degree bounded as q → 1. At q ≤ 0.99 the
  throat is still wide (δ_t ≥ 0.25).
- **No sample is near a zero-energy bound state.** min ψ₁ ≥ 0.49 (at D = 11 ℓ = 2), and the exact design's slack is
  ≥ 0.0028 (at D = 11 ℓ = 6).
- **The tightest fit is D = 11 ℓ = 2,** at 0.00136 = 14θ. HD-S's registered fallback (higher degree, then smaller
  μ-boxes) covers it.

## Hashes (SHA-256, first 16 hex)

- Code at `710488b`: `code/hd/pilot.py` `27f7bac39f0d36a7`; `kit/hd/run_pilot.sh` `ab9c97ee203c7e6c`.
- The record: `runs/record/main/result.json` `10e04bf69e70c579`; `run.log` `b59c0ab2ce26562d`; `kit.log` `f6213cd8c6ac37bb`.
- The reproduction: `runs/repro-host-2/main/result.json` `11a86e3c378cf997`.
