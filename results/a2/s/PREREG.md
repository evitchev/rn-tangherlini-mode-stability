# PREREG — A2-S: the singular S-certificate for ℓ = 2 through extremality (stage A2, step 3)

*Item BHM-100. 2026-10-24, the bh-modes lead. Step 3 of `TARGET_A2_ADDENDUM_1.md` §4 (BHM-092). The design is
A2-PILOT's (BHM-095). Registered before any run on S5's potential; the development tests (§6) used synthetic inputs only.
Code: `code/a2/scert.py`, `kit/a2/run_s.sh`, at the commit that holds this file. Sealed; any change before the run is a
dated addendum.*

## 1. The claim

> **A2-S.** For D = 6, ℓ = 2 and every q ∈ [q(1/8), 1], with q(1/8)² = 1 − w(1/8)² ≤ (99/100)²:
> N(z, μ) > 0 for all z ∈ (0, 1). N is METHOD's S-deformed potential for the design P below. Hence A_{2,q} ≥ 0.

- **With A1,** whose ℓ = 2 range reaches 99/100 (and T3 is certified on [0.97277, 0.99020]), A2-E and Lemma U, this
  completes Theorem A2. Theorem A2 then reads, for D = 6: A_{ℓ,q} ≥ 0 for every ℓ ≥ 2 and every 0 < q ≤ 1.
- **The reduction** (`TARGET_A2_ADDENDUM_1.md` §3). Proposition 3 for P that is C¹ on (0, 1) is machine-checked
  (`prop3_Ioo`, `prop3_Dn`, BHM-090/091). The tortoise map at q = 1 is pencil (`METHOD_ADDENDUM_1.md` §1).
- **The label after a pass:** *certified* (exact); reduction machine-checked (Lean), with R's existence proved
  (pencil; audited 0×).

## 2. The design and the exact polynomial

- **The design.** P = a(1 + ε)/(z + ε) + p₀(z), with a = −2/5 and ε = w/(3(1 + w)) = ε_n/ε_d = 7μ/(3(6 + 7μ + μ²)).
- **p₀** is the degree-12 Chebyshev series of the sealed pilot record, `results/a2/pilot/runs/record/main/result.json`.
  Its SHA-256 is checked against `SEALED.sha256` (gate DESIGN). The coefficients are its `float.hex` values,
  converted exactly to monomials in z.
- **With S = ε_d·z + ε_n and Π = a(ε_d + ε_n) + p₀S,** P = Π/S, and

  NL := N·S²·L = Un·Hd²·fd·S² − 64Hn²·Ud·[(1 − z)fzn·Π·S + fn(−ΠS + (1 − z)(Π_z S − ε_d Π) + Π²)].

  This is a polynomial in (z, μ). Un/Ud, Hn/Hd, fn/fd and fzn/fd are `hd.scert`'s exact parts at n = 4, and
  L = Ud·Hd²·fd.
- **NL vanishes at the corner (z, μ) = (0, 0)**, where S = 0, so no strict bound on a (z, μ) box can contain it.
  Four charts cover [0, 1] × [0, 1/8]:

  | Chart | Variables | Box | Polynomial |
  |---|---|---|---|
  | O | (z, μ) | [1/4, 1] × [0, 1/8] | NL |
  | O′ | (z, μ) | [0, 1/4] × [1/32, 1/8] | NL |
  | T | z = μζ | (ζ, μ) ∈ [0, 8] × [0, 1/32] | T = NL(μζ, μ)/μ² |
  | C | μ = zσ | (z, σ) ∈ [0, 1/4] × [0, 1/8] | C = NL(z, zσ)/z² |

- **Coverage** (pencil, with the inequalities checked exactly: gate COVER). Take z < 1/4 and μ < 1/32. If z ≤ 8μ, then
  (z/μ, μ) lies in T. Otherwise μ < z/8 = σ₁z, so (z, μ/z) lies in C. The rest is in O or O′. The checks are
  Z_T·σ₁ ≥ 1, Z_T·μ_T ≤ z₁, z₁·σ₁ ≤ μ₁, 0 < μ_T < μ₁ and 0 < z₁ < 1.
- **Hence N > 0.** For every (z, μ) ∈ (0, 1) × [0, 1/8], some chart gives NL(z, μ) > 0. There S > 0 and L > 0 (gates
  S, L), so N > 0.

## 3. Gates (each must hold for VERIFIED)

- **KAT:** the verifier's known-answer tests (A1's).
- **E0:** `TARGET.md`'s U₋, H₋ equal S5's (5.62b), (5.63b) at n = 4.
- **H:** every coefficient of H₋ is > 0.
- **PARAM:**
  - s² = 1 + 4mq²/25;
  - q(0) = 1;
  - q(1/8)² ≤ (99/100)²;
  - w increasing on [0, 1], by exact Bernstein on w′'s numerator and denominator.
- **DESIGN:** the pilot record's seal, a = −2/5 and b = 1/2.
- **G-RES** (BHM-085 §3 (ii), symbolic in ℓ, a, b₀, b₁). At q = 1 and P = a/z + b₀ + b₁z, N is a polynomial in z with
  N(0) = 576H₋(2)²(ℓ(ℓ − 3)/9 − a(a + 1)).
- **COVER:** as in §2.
- **L:** L > 0 on [0, 1/8]. **S:** ε_n = 7μ ≥ 0, zero only at μ = 0, and ε_d > 0 on [0, 1/8].
- **DIV-T, DIV-C:** the exact divisions by μ² and z².
- **POS-O, POS-O′, POS-T, POS-C:** each chart polynomial > 0 on its closed box, by exact Bernstein bisection
  (`onset.bernstein.prove_sign`, depth ≤ 40). The record gives the least accepted Bernstein coefficient.

**Information, not a gate: THROAT.** The pencil throat limit (`TARGET_A2_ADDENDUM_1.md` §3) predicts
T(ζ, 0) = 576H₋(2)²L(0)[(c − a − a²)(18ζ + 7)² + 49(a² − a)], with c = −2/9 and H₋(2) = 30. The record gives the
difference. A non-zero difference would be reported; the certificate does not use it.

## 4. Controls (same kit; each must give its registered verdict)

| Control | Registered verdict | Why it must |
|---|---|---|
| nc-a2: U₋ − 2H₋²x⁴, which makes the extremal throat coefficient c′ = −1/4 − 1/36 (design-free, BHM-085 §3 item 6) | REJECT, by a POS chart | At q = 1, N(0) = 576H₋(2)²(c′ − a(a + 1)) < 0 for every a, so the corner limit is negative |
| nc-zm: U₋ − H₋²x⁴ (c′ = −1/4) with a = −1/2 | REJECT, by a POS chart | N(0) = 0 at q = 1: the zero margin, which a strict certificate refuses |
| nc-res: a = −7/10 | REJECT, by a POS chart | Outside the window (−2/3, −1/3): N(0) < 0 at q = 1 |
| nc-bound: a planted bound state W − Kb at q = 1, b = ((z − 1/20)(1/5 − z))², K = ⌈2I₁/I₂⌉ | REJECT: nc-bound (b) | (a) the trial energy Q[b] < 0, certified in Arb, so no N ≥ 0 can exist (Proposition 3); (b) the certificate is refused on the bump |
| td-coeff: U₋'s 7680 → 7681 | REJECT, with E0 among the reasons | The transcription gate |
| td-verifier: the verifier's threshold lowered to −1 | REJECT: KAT | The KATs |
| td-chart: the throat chart without the division by μ² | REJECT: POS-T | T(ζ, 0) ≡ 0: the blow-up is needed. A control on the singular branch |
| td-cover: σ₁ = 1/16, so Z_T·σ₁ = 1/2 | REJECT: COVER | A gap between the charts |

"By a POS chart" means the verdict lists only POS-O, POS-O′, POS-T or POS-C (one or more) and no other check.

## 5. Runs, hosts

- **One command:** `kit/a2/run_s.sh`. The record runs on host-1, from a `git archive` of the commit that holds this file,
  under `nice -n 19` in `[venv]`. The reproduction runs on host-2 with `BHM_REF`; identical after masking.
- **The records** carry the UTC start (masked) and the archive's SHA-256.
- **Timeout:** 12 h per job.
- **The kill criteria** are those of `TARGET_A2_ADDENDUM_1.md` §5.
  - A POS failure on the main run is not a refutation. It is a failed certificate, reported as it stands; K4 applies
    at the end of the time box.
  - Only a certified negative trial value (K1) refutes.

## 6. Development tests (synthetic only; `code/a2/devtest_scert.py`)

W = 12 − 7x (U = 64m²(12 − 7x), H = m) replaces S5's potential, with its own design from `a2.pilot`'s functions (the same
rule). E0, G-RES and THROAT are not run there. **Results, 10/10 as expected** (at `57039e7` on host-2, 1 s per job):
- the main run is VERIFIED;
- nc-a2 REJECTs by POS-T and POS-C (negative corners), and nc-zm by POS-C with the corner value exactly 0;
- nc-res REJECTs by POS-T and POS-C;
- nc-bound REJECTs as `REJECT: nc-bound (b)`, with (a) certified;
- td-verifier REJECTs by KAT, td-chart by POS-T and td-cover by COVER;
- td-coeff is VERIFIED there, as expected without E0;
- two records of the main run are identical after masking.
