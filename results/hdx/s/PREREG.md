# PREREG — HD-X-S: the singular S-certificates for the 11 non-critical bands of D = 7–11 through extremality (HD-X-1, step 3)

*Item BHM-131. 2026-10-26, the bh-modes lead. Step 3 of `TARGET_HD_ADDENDUM_2.md` §4 (BHM-121), after HD-X-PILOT
(BHM-129, BHM-130).*
- *Registered before `hdx.scert` has run on any HD-X band's design. The development tests (§6) used synthetic inputs,
  plus the gate band D = 6 ℓ = 2, whose record is a known answer.*
- *The code was written by a fork of the lead (BHM-120) and read by the lead: `code/hdx/scert.py`, `code/hdx/bands.py`,
  `code/hdx/verdicts.py`, `code/hdx/gate.py` and `kit/hdx/run_s.sh`, at the commit that holds this file. Sealed; any
  change before the run is a dated addendum.*

## 1. The claim

> **HD-X-S.** For each of the 11 bands (D, ℓ) with 2ℓ > n − 1 (D = 7 ℓ = 3; D = 8 ℓ = 3, 4; D = 9 ℓ = 4, 5; D = 10
> ℓ = 4, 5, 6; D = 11 ℓ = 5, 6, 7), and every q ∈ [q(1/8), 1] with q(1/8)² ≤ (99/100)², A_{ℓ,q} ≥ 0 on C₀^∞(ℝ).

- **With Theorem HD** (q ≤ 99/100), **HD-X-E** (BHM-128) and **Lemma U(n)**, this completes Theorem HD-X outside the
  critical set 𝒦: D = 7–11, every ℓ with (D, ℓ) ∉ 𝒦, every q ∈ (0, 1].
- **Not claimed:** the 9 bands of 𝒦 (HD-X-2), whose q = 1 endpoint is Z's (BHM-126).

## 2. Method (A2-S at general n; `code/hdx/scert.py`)

- **The design** is HD-X-PILOT's sealed record for the band (BHM-130): `results/hdx/pilot/runs/record/main/result.json`,
  SHA-256 `a95b583b883bc62545ed3fbfeb2595700c365db414e2441c6375c897fabfaa80`, with every band at the degree it selected.
  P = a(1 + ε)/(z + ε) + p₀(z), with a from `hdx.bands`, ε = w/((n − 1)(1 + w)) = ε_n/ε_d, and p₀ the recorded
  Chebyshev series converted exactly to monomials.
- **The polynomial.** With S = ε_d z + ε_n and Π = a(ε_d + ε_n) + p₀S, so that P = Π/S,

    NL := N·S²·L = U_n H_d² f_d S² − 64H_n² U_d [(1 − z)f_zn Π S + f_n(−Π S + (1 − z)(Π_z S − ε_d Π) + Π²)],

  a polynomial in (z, μ), with L = U_d H_d² f_d > 0.
- **The charts** (A2-S's constants: Z1 = 1/4, ZT = 8, SIG1 = 1/8, MUT = 1/32, μ₁ = 1/8):
  - O: (z, μ) ∈ [Z1, 1] × [0, μ₁], NL > 0;
  - O′: [0, Z1] × [MUT, μ₁], NL > 0;
  - T: z = μζ, (ζ, μ) ∈ [0, ZT] × [0, MUT], T = NL(μζ, μ)/μ² > 0;
  - C: μ = zσ, (z, σ) ∈ [0, Z1] × [0, SIG1], C = NL(z, zσ)/z² > 0.

  Each is checked by exact Bernstein bisection (`onset.bernstein.prove_sign`, depth ≤ 40). DIV-T and DIV-C check the
  divisions exactly, and COVER checks ZT·SIG1 ≥ 1, ZT·MUT ≤ Z1 and Z1·SIG1 ≤ μ₁.
- **The reduction.** In every point of (0, 1) × [0, μ₁] some chart gives NL > 0, and S > 0, L > 0 there, so N > 0.
  - Then A_{ℓ,q} ≥ 0 by Proposition 3 for P that is C¹ on (0, 1) (*machine-checked*, `prop3_Ioo`/`prop3_Dn`,
    BHM-090/091, every n ≥ 2). P's pole z = −ε lies outside [0, 1].
  - The tortoise map onto ℝ at q = 1, at general n: Z's PREREG §2 (pencil; audited 0×).
- **Gates:**
  - KAT;
  - E0n (S5's U₋ and H₋ against Kimi's transcription, n = 2…12);
  - H;
  - PARAM (the parametrisation identities, q(0) = 1, q(1/8)² ≤ (99/100)², w increasing);
  - DESIGN (the pilot record's SHA-256 as sealed, and the band's registered a, B_POLE and μ₁);
  - G-RES (at q = 1, N(0) = 64(n − 1)²H(2)²(c − a(a + 1)) for P = a/z + b₀ + b₁z, symbolic in ℓ, a, b₀, b₁);
  - COVER, L, S, DIV-T, DIV-C, and the four charts.
- **THROAT,** information: T(ζ, 0) against 64(n − 1)²H(2)²L(0)[(c − a − a²)(ε_d(0)ζ + ε_n′(0))² + (a² − a)ε_n′(0)²].
- **The gate band** `--band 6,2` runs A2-S's design (A2-PILOT's sealed record) with A2-S's constants. Its record must
  equal A2-S's (BHM-101) in every field A2-S's certificate determines, including every chart's least Bernstein
  coefficient (`hdx.gate`; `kit/hdx/run_s.sh --gate`).

## 3. Controls, per band (registered verdict rules: `code/hdx/verdicts.py`)

| Control | Registered verdict | Why it could fail, and why it must |
|---|---|---|
| nc-a2: U − k_a2H²x⁴, k_a2 = (2ℓ − n + 1)² + 1 | REJECT, every reason a POS chart | c′ = −1/4 − 1/(4(n − 1)²) is below the BF bound, so N(0) < 0 at q = 1 for every a (design-free) |
| nc-res: a = a_nc, outside the window | REJECT, every reason a POS chart | c − a(a + 1) < 0 at the corner |
| nc-well: a planted bound state at q = 1 on WELL's support, inside U₋ < 0 | REJECT: nc-well (b), with (a) certified | (a) Q[b] < 0 in Arb at 256 bits, with K = ⌈2I₁/I₂⌉. (b) NL of the planted potential at μ = 0 is refused on [z_a, z_b], where z_a > 0. Unplanted, that NL is C(z, 0)·z² > 0 there whenever POS-C holds, so the refusal comes from the well and not from a zero of the check (unlike the A2 audit's (e)(ii), BHM-116) |
| d0: U − 4β₀H²x⁴, so c′ = a(a + 1) | REJECT, POS-C among the reasons, every reason a POS chart, POS-C's detail at (0, 0) with the value 0 | The sharp zero margin at the blown-up corner. POS-C alone is not registered: the lowering also eats slack away from the corner, and in the tight bands O or O′ may fail too |
| d6: NL − Kμ(z − μ)(3μ − z), K = (4/MUT)·T(2, MUT/2) | REJECT, POS-T among the reasons, every reason a POS chart, POS-T's point at μ ≠ 0 | A planted throat defect that vanishes at μ = 0, so T(ζ, 0) is unchanged |
| td-coeff: U₋ + 16nm² | REJECT, E0n among the reasons | The transcription gate. The tamper also enters the certificate, so POS failures may come too |
| td-verifier | REJECT: KAT | |
| td-chart: the throat chart without the division by μ² | REJECT: POS-T | T(ζ, 0) ≡ 0 undivided |
| td-cover: SIG1 halved | REJECT: COVER | ZT·SIG1 < 1 |
| td-H: the H gate on H₋ − n(n + 1)x | REJECT: H | |
| td-param: param_n's tamper | REJECT: PARAM | |
| td-design: a changed hash | REJECT: DESIGN | |
| td-gres: G-RES on U₋ + x⁴ | REJECT: G-RES | |
| td-L: the L gate on −L | REJECT: L | |
| td-S: ε_n → −ε_n, the pole inside the exterior | REJECT, with S first and every later reason a POS chart | |
| td-divT: the throat chart divided by μ³ | REJECT: DIV-T, POS-T | |
| td-divC: the corner chart divided by z³ | REJECT: DIV-C, POS-C | |

## 4. Runs, hosts

- **Two commands:** `kit/hdx/run_s.sh` runs 11 bands × 18 jobs, at `BHM_JOBS` (default 8) at a time, and
  `kit/hdx/run_s.sh --gate` runs the gate
  band against A2-S's record.
- **Hosts:**
  - the record on host-1, from a `git archive` of the commit that holds this file, under `nice -n 19` in
    `[venv]`;
  - the reproduction on host-2, with `BHM_REF`: every JSON identical after masking.
- **The records** carry the UTC start time (masked) and the archive's SHA-256.
- **Timeout:** the kit's per job. A timeout is VOID for that job.
- **The kill criteria** are the frame's K1–K4, per band (`TARGET_HD_ADDENDUM_2.md` §6). A band whose `none` job rejects
  is reported as it stands. It is not refuted, since the reduction runs one way only. Its controls are then VOID.

## 5. What each outcome means (registered now)

- **A band VERIFIED** (its `none` job VERIFIED, and its 17 controls as registered): A_{ℓ,q} ≥ 0 for every
  q ∈ [q(1/8), 1]. That is *certified*; the reduction is Proposition 3 (*machine-checked*), and the tortoise map at
  general n is proved (pencil; audited 0×).
- **All 11 VERIFIED:** with Theorem HD, HD-X-E and Lemma U(n), Theorem HD-X holds outside 𝒦.
- A second party is pending (RULES.md A4): Kimi, by a brief, at HD-X's stage report.

## 6. Development tests

- **`code/hdx/devtest_scert.py`** uses a synthetic potential with each band's exact throat coefficient (D = 7 ℓ = 3 and
  D = 11 ℓ = 7).
  - Each of the 18 jobs ended as its rule requires, and two main runs were identical.
  - Direct tests: DESIGN on A2-PILOT's sealed record; td-design's changed hash; a design outside the family; a missing
    HD-X record (DESIGN fails under its own label); a critical band, refused; G-RES at n = 5; and td-gres failing with
    difference 16.
- **The gate band**, `hdx.scert --band 6,2`: VERIFIED, and identical to A2-S's record (BHM-101), including every chart's
  least Bernstein coefficient.
- **Results:** 46/46 at `bb23ba2`, in the fork's clone, on host-2. The rerun at `c4b6d3e`, in this repository, on host-1:
  46/46 as expected, DEVTEST PASS (`[run-folder]/dev-hdxs-c4b6d3e/devtest_scert.log`).
