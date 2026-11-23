# A2-S RESULT: VERIFIED — the singular S-certificate for ℓ = 2 through extremality (BHM-101)

*2026-10-24, the bh-modes lead. Registration: `PREREG.md` (BHM-100), sealed before the run. The record ran on host-1 and
the reproduction on host-2, from a `git archive` of `25c796e` (archive SHA-256 `a565ef2b64d0cd59…`) with
`kit/a2/run_s.sh`. UTC start 03:50:34; 2.8 s.*
- *Both kits print KIT PASS.*
- *All nine records are identical after masking, and the `run.log`s are byte-identical.*

## The result

> **A2-S (certified).** For D = 6, ℓ = 2 and every q ∈ [q(1/8), 1] (q(1/8)² = 2961/3025, so q(1/8) = 0.98936… < 99/100),
> the design P = −(2/5)(1 + ε)/(z + ε) + p₀(z), with ε = w/(3(1 + w)) and p₀ the sealed degree-12 pilot polynomial, gives
> N(z, μ) > 0 for every z ∈ (0, 1). Hence A_{2,q} ≥ 0 (Proposition 3 for P C¹ on (0, 1)).

**The exact polynomials and their proofs:**

| Chart | Polynomial (degrees in its two variables) | Box | Least Bernstein coefficient (exact, in the record) |
|---|---|---|---|
| O | NL (38, 12) | [1/4, 1] × [0, 1/8] | > 0, one box |
| O′ | NL (38, 12) | [0, 1/4] × [1/32, 1/8] | > 0, one box |
| T | NL(μζ, μ)/μ² (38, 48) | [0, 8] × [0, 1/32] | 528353280, one box |
| C | NL(z, zσ)/z² (48, 12) | [0, 1/4] × [0, 1/8] | > 0, one box |

No chart needed a bisection.

**Gates, all passed:**
- **KAT, E0** (S5 (5.62b), (5.63b) at n = 4 equal `TARGET.md`'s forms exactly), and **H**.
- **PARAM:** s² = 1 + 4mq²/25, q(0) = 1, q(1/8)² = 2961/3025 ≤ (99/100)², and w increasing on [0, 1].
- **DESIGN:** the pilot record's SHA-256 is the sealed one; the degree is 12.
- **G-RES:** at q = 1 and P = a/z + b₀ + b₁z, N is a polynomial in z, and N(0) − 576H₋(2)²(ℓ(ℓ − 3)/9 − a(a + 1)) = 0
  identically in ℓ, a, b₀, b₁, with H₋(2) = (ℓ + 3)(ℓ + 4). That is BHM-085 §3 (ii), now certified.
- **COVER, L, S, DIV-T, DIV-C.**
- **The four POS charts.**

**Information, THROAT:** T(ζ, 0) minus the pencil throat limit 576H₋(2)²L(0)[(c − a − a²)(18ζ + 7)² + 49(a² − a)]
is **0 exactly**. So `TARGET_A2_ADDENDUM_1.md` §3's leading-order throat analysis is confirmed exactly at μ = 0.

## Controls (all as registered)

| Control | Verdict | Where |
|---|---|---|
| nc-a2 (c′ = −1/4 − 1/36) | REJECT: POS-T, POS-C | exact negative values at the blown-up corner: C(0, 0) = −49340399616, T(8, 0) = −3361641689088 |
| nc-zm (c′ = −1/4, a = −1/2) | REJECT: POS-O, POS-C | C(0, 0) = 0 exactly: the zero margin. U₋ − H₋²x⁴ also lowers the outer region, so POS-O fails too |
| nc-res (a = −7/10) | REJECT: POS-O, POS-O′, POS-T, POS-C | negative at the corner, and elsewhere |
| nc-bound | REJECT: nc-bound (b) | (a) Q[b] = [−2.757418575·10⁻⁹ ± 3.79·10⁻¹⁹] < 0 in Arb, K = 3403781; (b) refused at (z, μ) = (1/8, 0) with an exact negative value |
| td-coeff | REJECT: E0 | the transcription gate |
| td-verifier | REJECT: KAT | the known-answer tests |
| td-chart | REJECT: POS-T | without the division by μ², T(ζ, 0) ≡ 0: the blow-up is needed |
| td-cover | REJECT: COVER | σ₁ = 1/16 leaves a gap |

## Status

- **A2-S:** *certified* (exact).
- **The reduction:** Proposition 3 for P that is C¹ on (0, 1) is machine-checked (Lean `prop3_Ioo`, `prop3_Dn`;
  BHM-090/091). The tortoise map at q = 1 (`METHOD_ADDENDUM_1.md` §1) and R's existence are proved (pencil; audited 0×).
- **Second party:** pending (RULES.md A4).
- **With A1** (0 < q ≤ 99/100), **A2-E** (ℓ = 3…10) and **Lemma U** (ℓ ≥ 11, q ≤ 1), Theorem A2 holds. The stage
  report gives the composition (BHM-102).

## Hashes (SHA-256, first 16 hex)

- Code at `25c796e`: `code/a2/scert.py`, `kit/a2/run_s.sh` as in BHM-100. The design is the pilot record
  `results/a2/pilot/runs/record/main/result.json` `26501fe6f55dfd46`.
- The records are under `runs/record/<control>/` and `runs/repro-host-2/<control>/`; all are listed in `SEALED.sha256`.
