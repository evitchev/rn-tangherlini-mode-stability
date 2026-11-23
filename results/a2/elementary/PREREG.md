# PREREG — A2-E: ℓ = 3…10 near extremality, by U₋ ≥ 0 (stage A2, step 2)

*Item BHM-096. 2026-10-24, the bh-modes lead. Step 2 of `TARGET_A2_ADDENDUM_1.md` §4 (BHM-092). Registered before any
run on S5's potential; the development tests (§5) used synthetic inputs only. Code: `code/a2/elementary.py`,
`kit/a2/run_elementary.sh`, at the commit that holds this file. Sealed; any change before the run is a dated addendum.*

## 1. The claim

> **A2-E.** For D = 6, every ℓ ∈ {3, …, 10} and every q ∈ [q(μ_lo(ℓ)), 1], U₋ ≥ 0 on the closed exterior
> 0 ≤ x ≤ x_H. For ℓ = 4…10 the inequality is strict. For ℓ = 3 its only zero is at the extremal horizon (x = x_H = 2,
> q = 1). Hence V_S− ≥ 0 on the exterior, and A_{ℓ,q} ≥ 0.

- **μ_lo(ℓ)** is A1's P1 lower end (BHM-052): the largest k/1000 with w(k/1000)² ≤ 1 − (99/100)². So q(μ_lo(ℓ)) ≤ 99/100.
  Together with P1 Part I, on [μ_lo, 1], every q ∈ [0, 1] is covered for these ℓ.
- **With A1 and Lemma U,** this leaves only ℓ = 2 for Theorem A2 (A2-S).

## 2. Method (exact; `onset.onset`'s parametrisation, μ = 0 at q = 1)

- **The setup.** With x = t·x_H, U₋ = F(t, μ)/Den(μ) in lowest terms, from `TARGET.md` §1's U₋.
- **Gates:**
  - KAT, the verifier's known-answer tests;
  - E0, `TARGET.md`'s U₋ and H₋ equal S5's (5.62b), (5.63b) at n = 4;
  - H, every coefficient of H₋ is > 0;
  - the parametrisation identities: s² = 1 + 4mq²/25, and q(0) = 1;
  - w increasing on [0, 1];
  - q(μ_lo)² ≥ (99/100)².
- **ℓ = 4…10.** Den > 0 on [0, μ_lo], and F > 0 on [0, 1] × [0, μ_lo], by exact Bernstein bisection
  (`onset.bernstein.prove_sign`, depth ≤ 40). The record gives the certified lower bound min F / max Den.
- **ℓ = 3.** F(1, 0) = 0, because U₋(x_H) = 64ℓ(ℓ − 3)(ℓ + 3)²(ℓ + 4)² at q = 1 (BHM-085 C9). So no strict bound holds at
  that corner. With s = 1 − t:
  - F(1 − s, μ) = μK(μ) + sG(s, μ), where K = F(1, μ)/μ and G = (F(1 − s, μ) − F(1, μ))/s are exact polynomial
    divisions. Both remainders must be 0, and the identity is checked.
  - K > 0 on [0, μ_lo] and G > 0 on [0, 1] × [0, μ_lo], by exact Bernstein.
  - Then F ≥ 0, with F = 0 only at s = μ = 0.

**Verdict.** VERIFIED if every check holds, otherwise `REJECT: <checks>`, fail-closed.

## 3. Controls (same kit; each must give its registered verdict)

| Control | Registered verdict | Why |
|---|---|---|
| nc-ell2: ℓ = 2 on [0, μ_lo(2)] | REJECT: E l=2 | U₋(x_H) = −115200 < 0 at q = 1: a counterexample corner |
| nc-strict: ℓ = 3 with a strict bound on F itself | REJECT: E l=3 | F(1, 0) = 0 at a corner of the box |
| nc-bump: ℓ = 4 with F − 10⁷·64t³(1 − t)³Den | REJECT: E l=4 | Negative at t = 1/2 |
| td-coeff: U₋'s 7680 → 7681 | REJECT, beginning with E0 | The transcription gate |
| td-verifier: the verifier's threshold lowered to −1 | REJECT: KAT | The known-answer tests catch it |

## 4. Runs, hosts

- **One command:** `kit/a2/run_elementary.sh`.
- **The record** runs on host-1, from a `git archive` of the commit that holds this file, under `nice -n 19` in
  `[venv]`. **The reproduction** runs on host-2 with `BHM_REF`; every JSON must be identical after masking.
- **The records** carry the UTC start time (masked) and the archive's SHA-256.

## 5. Development tests (synthetic only; `code/a2/devtest_elementary.py`)

The test used U = 64m³(2 − x)(1 + x) and U + 64m³ in place of S5's U₋. U vanishes at x = 2 like ℓ = 3's U₋, and is
otherwise unrelated. Results, 9/9 as expected, at `a2d325c` on host-2:
- the ℓ = 3 splitting proves F ≥ 0;
- the strict bound refuses the touching corner;
- the strict bound proves ℓ = 4;
- the bump and a negative U are refused with exact counterexamples;
- the tampered verifier fails the KATs;
- the record writer runs (with E0 failing by construction), and two records are identical after masking.
