# p3 METHOD addendum 2: Proposition 3 at general n, and for a P that is C¹ near [0, 1]

*Item BHM-086. 2026-10-23, the bh-modes lead.*
- *It answers the session-R lead's reading of the D = 7–11 stage report, §1.3 (BHM-085). The reading
  observes that HD-S uses Proposition 3 at n = 5…9 and for P = P̂/(z + δ_b)^d, while `METHOD.md`, its two audits
  and the Lean instance `prop3_D6` are at n = 4, with P a polynomial (Lean's generic `prop3` assumes P
  differentiable on all of ℝ).*
- *`METHOD.md` is sealed and unchanged.*
- *Status: the extension below is proved (pencil; audited 0×). Kimi's HD-S brief asks for exactly these two verdicts
  (BHM-080). The n = 4 polynomial case keeps its status: proved (pencil; audited 2×), and machine-checked in Lean.
  Sealed.*

## The statement

Let D = n + 2 with n ≥ 2, K = 1, Λ = 0, and 0 ≤ q < 1. Work in units r_H = 1, with ρ ∈ (1, ∞) and z = 1 − 1/ρ ∈ (0, 1).
Then:
- x = x_H(1 − z)^{n−1}, and f = (1 − y)(1 − ky) with y = (1 − z)^{n−1} and k = x_H/x₋ = (1 − w)/(1 + w) ∈ [0, 1).

Let P be C¹ on an open interval containing [0, 1], and put β = (1 − z)P and S(r*) = −f(ρ)β(ρ). Define
N = U₋ − 64H₋²[(1 − z)f_zP + f(−P + (1 − z)P_z + P²)]. **If N ≥ 0 on (0, 1), then A_{ℓ,q} ≥ 0.**

## Proof (each step as in `METHOD.md` and `METHOD_ADDENDUM_1.md`; only what depends on n or on P is new)

1. **f > 0 on the exterior.** For z ∈ (0, 1), 0 < y < 1 and 0 ≤ k < 1, so both factors are positive.
2. **The tortoise map is a C^∞ diffeomorphism ℝ → (1, ∞).**
   - At the horizon, f_z(0) = (n − 1)(1 − k) > 0 for q < 1. So the zero of f at ρ = 1 is simple, and r* → −∞
     logarithmically.
   - At infinity, f → 1, so r* → +∞.
   - The rest is `METHOD_ADDENDUM_1.md` §1, word for word.
3. **S ∈ C¹(ℝ).** z(ρ) = 1 − 1/ρ maps (1, ∞) into (0, 1), where P is C¹. So β, f and S are C¹ in ρ, hence in r*.
4. **The identity Ṽ = f·N/(64ρ²H₋²)** is Lemma 2's computation, and it does not use n. It uses only:
   - dz/dρ = (1 − z)²;
   - f′ = (1 − z)²f_z and β′ = (1 − z)²(−P + (1 − z)P_z);
   - ρ²W = U₋/(64H₋²).

   Lean's `ansatz_identity` is this identity, with f, f_z and P generic.
5. **The sign.** H₋ = m + n(n + 1)(1 + mδ)x/2 ≥ m > 0, since x > 0 and δ ≥ 0 (HD-S's gate H). With f > 0 and ρ > 0,
   N ≥ 0 on (0, 1) gives Ṽ ≥ 0 on ℝ. Lemma 1 and its Corollary, which are general, give A_{ℓ,q} ≥ 0.

## Where the hypotheses are met

**HD-S's z-designs:** P is a polynomial in (z, μ), so it is C^∞ in z for each μ.

**HD-S's ζ-designs:** P = P̂/(z + δ_b)^d with δ_b > 0 a fixed rational per box.
- This is C^∞ on (−δ_b, ∞) ⊃ [0, 1], so the hypothesis holds. The pole at z = −δ_b is outside, and only (0, 1) is
  used.
- The certificate proves N·L·(z + δ_b)^{2d} > 0 on [0, 1] × box, with L > 0 proved separately. Since
  (z + δ_b)^{2d} > 0 there, this gives N > 0 on [0, 1].

**What Lean does not cover here.** Its generic `prop3` asks P to be differentiable on all of ℝ. A ζ-design does not
meet that literally: it has a pole at z = −δ_b. But only P's values on (0, 1) enter the identity and the
quadratic form, so the restriction to (0, 1) is all that is used. Restating `prop3` with that hypothesis is offered to
session-L (BHM-085, §1.3).
