# p3 method: the S-certificate, in pencil

*Item BHM-022 (with `PREREG.md`). **Status: proved (pencil; audited 0×).** Why N ≥ 0 on [0, 1]
implies A_{ℓ,q} ≥ 0. `TARGET.md` §1 owns the formulas. Here f, U₋, H₋ are S5's (cited, CHARTER
e7), and ′ = d/dρ.*

**Lemma 1 (S-deformation identity).** Let V be continuous on ℝ, let S ∈ C¹(ℝ) be real, and let
φ ∈ C₀^∞(ℝ). Then
  ∫(|φ′|² + V|φ|²) = ∫|φ′ + Sφ|² + ∫(V + S′ − S²)|φ|²   (′ = d/dr* here).

*Proof.*
- Expand: |φ′ + Sφ|² = |φ′|² + S(|φ|²)′ + S²|φ|², using S real.
- Integrate by parts: ∫S(|φ|²)′ = −∫S′|φ|². There are no boundary terms, since φ has compact
  support. ∎

**Corollary.** If Ṽ := V + S′ − S² ≥ 0 on ℝ, the quadratic form of A = −d²/dr*² + V is ≥ 0 on
C₀^∞(ℝ), so A ≥ 0 (`TARGET.md` §2).

**Lemma 2 (the ansatz).** Work in units r_H = 1, with ρ = r ∈ (1, ∞) and z = 1 − 1/ρ ∈ (0, 1),
so that dz/dρ = (1 − z)². Let P be a polynomial in z and β := (1 − z)P = P/ρ. Put
S(r*) := −f(ρ)β(ρ). Then S is C^∞ on ℝ, and
  Ṽ = f·N/(64ρ²H₋²),  N := U₋ − 64H₋²[(1 − z)f_z P + f(−P + (1 − z)P_z + P²)],
with x = x_H(1 − z)^{n−1} (n = 4 here).

*Proof.*
- **Smoothness.** r* ↦ ρ is a C^∞ diffeomorphism ℝ → (1, ∞), and f and β are smooth in ρ.
- **First form.** V = fW with W := U₋/(64ρ²H₋²), and d/dr* = f d/dρ. So
  Ṽ = fW − f(f′β + fβ′) − f²β² = f[W − f′β − f(β′ + β²)].
- **Change of variable.** With f′ = (1 − z)²f_z and β′ = (1 − z)²(−P + (1 − z)P_z):
  - ρ²f′β = (1 − z)f_z P;
  - ρ²fβ′ = f(−P + (1 − z)P_z);
  - ρ²fβ² = fP²;
  - ρ²W = U₋/(64H₋²).

  Multiplying by ρ² gives Ṽ = (f/ρ²)·N/(64H₋²). ∎

**Proposition 3.** If N(z) ≥ 0 for all z ∈ [0, 1], then A_{ℓ,q} ≥ 0.
*Proof.* On the exterior f > 0, ρ > 0 and H₋ ≥ m > 0, so Ṽ ≥ 0 on ℝ. Apply the Corollary. ∎

**Remarks.**
- **The endpoints are included.**
  - z = 1 is spatial infinity. There f = 1, (1 − z)f_z → 0 and P_z is finite, so
    N(1) = 64m²(m + 6 − P(1)² + P(1)) for D = 6. The check at z = 1 replaces the Riccati
    tail lemma of `FEASIBILITY.md` draft 1, and needs −3 < P(1) < 4 for ℓ = 2.
  - z = 0 is the horizon: N(0) = U₋(x_H) − 64H₋(x_H)² f_z(0)P(0).
- **Why such P exist.** For the exact zero-energy solution ψ₁, P_true := ρψ₁′/ψ₁ gives
  N ≡ 0. With P = P_true − ε one finds
  ρ²(Ṽ/f) = ε[ρf′ + f(2P_true − 1 − ε)], which is > 0 for small ε where ψ₁ > 0 (planning data,
  `results/planning/`). So the design target has slack O(ε). The polynomial fit only needs an
  error small against it.
- **Parameter boxes.** If P = P(z, μ) and N(z, μ)·Den(μ) ≥ 0 on [0, 1] × [μ_a, μ_b] with
  Den > 0, the Proposition holds for every μ in the box, i.e. for every q in its image.
