/-
  BHModesP3: the S-deformation identity and the ansatz algebra of bh-modes results/p3/METHOD.md, Lemmas 1–2, with
  Proposition 3 and the Remarks (session-L, 2026-10-22). Private under the bh-modes quiet rule. The request is the
  bh-modes lead's second message of 2026-10-22, §3 item (a).
  Sources: bh-modes results/p3/METHOD.md (Lemmas 1–2, Proposition 3, Remarks) and TARGET.md §1 (f, H₋, U₋, the
  tortoise coordinate). The D = 6 polynomials Hm and Um are TARGET.md's, as in BHModesA1.lean.
  What is proved, exactly:
  - Lemma 1 for complex φ that is C¹ with compact support (C₀^∞ is a special case), V continuous, S real and C¹:
    ∫(‖φ′‖² + V‖φ‖²) = ∫‖φ′ + Sφ‖² + ∫(V + S′ − S²)‖φ‖² (`sdef_identity`); the real case (`sdef_identity_real`);
    the Corollary (`form_nonneg_of_sdef`).
  - Lemma 2 in units r_H = 1, with z = 1 − 1/ρ: dz/dρ = (1 − z)², f′ = (1 − z)² f_z, β′ = (1 − z)²(−P + (1 − z)P_z),
    and V + f·dS/dρ − S² = f·N/(64ρ²H₋²) with METHOD's N (`ansatz_identity`). Here f·dS/dρ is dS/dr*: for any R with
    dR/dr* = f(R), the chain rule gives (S ∘ R)′ = (S′ ∘ R)·(f ∘ R) (used inside `prop3`).
  - Proposition 3: if N ≥ 0 on (0, 1), f ≥ 0 and H₋ ≠ 0 there, then the quadratic form in r* is ≥ 0 for every R with
    dR/dr* = f(R) and R > 1 (`prop3`). Its D = 6 instance discharges f > 0, H₋ > 0, f's derivative and all continuity
    (`prop3_D6`).
  - The Remarks: N at the horizon (`N_at_horizon`, `N_at_horizon_D6`); N(1) = 64m²(m + 6 − P(1)² + P(1)) at D = 6
    (`N_at_infinity_D6`); for ℓ = 2, N(1) > 0 ⟺ −3 < P(1) < 4 (`N_at_infinity_ell2`); the ε-shift (`N_eps_shift`) and
    ρf′ = (1 − z)f_z (`rho_fprime`).
  Not proved here:
  - the existence of the inverse tortoise map R : ℝ → (1, ∞) with dR/dr* = f(R). TARGET.md §1 takes the tortoise
    coordinate as given; `prop3` holds for every such R;
  - C^∞ smoothness. C¹ is all that is used;
  - the scaling from units r_H = 1 to TARGET.md's absolute units;
  - that the quadratic form determines the operator A (TARGET.md's reading);
  - N ≥ 0 for any concrete P. That is item (c).
-/
import Mathlib.MeasureTheory.Integral.IntegralEqImproper
import Mathlib.Analysis.Calculus.Deriv.Support
import Mathlib.Analysis.Calculus.Deriv.Inv
import Mathlib.MeasureTheory.Function.LocallyIntegrable
import Mathlib.Analysis.Complex.Basic
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic.FunProp
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith

set_option autoImplicit false
set_option relaxedAutoImplicit false

open MeasureTheory

namespace BHModes.P3

/-! ### Lemma 1: the S-deformation identity (′ = d/dr*) -/

theorem sdef_identity_real (V S S' φ φ' : ℝ → ℝ)
    (hV : Continuous V) (hS : ∀ x, HasDerivAt S (S' x) x) (hS' : Continuous S')
    (hφ : ∀ x, HasDerivAt φ (φ' x) x) (hφ' : Continuous φ') (hc : HasCompactSupport φ) :
    ∫ x, (φ' x ^ 2 + V x * φ x ^ 2) =
      (∫ x, (φ' x + S x * φ x) ^ 2) + ∫ x, (V x + S' x - S x ^ 2) * φ x ^ 2 := by
  have hφc : Continuous φ := continuous_iff_continuousAt.2 fun x => (hφ x).continuousAt
  have hSc : Continuous S := continuous_iff_continuousAt.2 fun x => (hS x).continuousAt
  have hc' : HasCompactSupport φ' := by
    have h : φ' = deriv φ := funext fun x => (hφ x).deriv.symm
    rw [h]; exact hc.deriv
  have hg : ∀ x, HasDerivAt (fun y => S y * φ y ^ 2)
      (S' x * φ x ^ 2 + S x * (2 * φ x * φ' x)) x := by
    intro x
    have h2 : HasDerivAt (fun y => φ y ^ 2) (2 * φ x * φ' x) x :=
      ((hφ x).pow 2).congr_deriv (by push_cast; ring)
    exact (hS x).mul h2
  have csA : HasCompactSupport (fun x => φ' x + S x * φ x) := hc'.add hc.mul_left
  have i1 : Integrable (fun x => (φ' x + S x * φ x) ^ 2) :=
    (by fun_prop : Continuous fun x => (φ' x + S x * φ x) ^ 2).integrable_of_hasCompactSupport
      (csA.mono fun x hx h0 => hx (by simp [h0]))
  have i2 : Integrable (fun x => (V x + S' x - S x ^ 2) * φ x ^ 2) :=
    (by fun_prop : Continuous fun x => (V x + S' x - S x ^ 2) * φ x ^ 2).integrable_of_hasCompactSupport
      (hc.mono fun x hx h0 => hx (by simp [h0]))
  have ig : Integrable (fun x => S x * φ x ^ 2) :=
    (by fun_prop : Continuous fun x => S x * φ x ^ 2).integrable_of_hasCompactSupport
      (hc.mono fun x hx h0 => hx (by simp [h0]))
  have ig' : Integrable (fun x => S' x * φ x ^ 2 + S x * (2 * φ x * φ' x)) :=
    (by fun_prop : Continuous fun x => S' x * φ x ^ 2 + S x * (2 * φ x * φ' x)).integrable_of_hasCompactSupport
      (hc.mono fun x hx h0 => hx (by simp [h0]))
  have h0 := integral_eq_zero_of_hasDerivAt_of_integrable hg ig' ig
  have hpt : (fun x => φ' x ^ 2 + V x * φ x ^ 2) = fun x =>
      ((φ' x + S x * φ x) ^ 2 + (V x + S' x - S x ^ 2) * φ x ^ 2)
        - (S' x * φ x ^ 2 + S x * (2 * φ x * φ' x)) := by
    funext x; ring
  have i12 : Integrable (fun x => (φ' x + S x * φ x) ^ 2 + (V x + S' x - S x ^ 2) * φ x ^ 2) := i1.add i2
  rw [hpt, integral_sub i12 ig', integral_add i1 i2, h0, sub_zero]

theorem sdef_identity (V S S' : ℝ → ℝ) (φ φ' : ℝ → ℂ)
    (hV : Continuous V) (hS : ∀ x, HasDerivAt S (S' x) x) (hS' : Continuous S')
    (hφ : ∀ x, HasDerivAt φ (φ' x) x) (hφ' : Continuous φ') (hc : HasCompactSupport φ) :
    ∫ x, (‖φ' x‖ ^ 2 + V x * ‖φ x‖ ^ 2) =
      (∫ x, ‖φ' x + (S x : ℂ) * φ x‖ ^ 2) + ∫ x, (V x + S' x - S x ^ 2) * ‖φ x‖ ^ 2 := by
  have hφc : Continuous φ := continuous_iff_continuousAt.2 fun x => (hφ x).continuousAt
  have hSc : Continuous S := continuous_iff_continuousAt.2 fun x => (hS x).continuousAt
  have hc' : HasCompactSupport φ' := by
    have h : φ' = deriv φ := funext fun x => (hφ x).deriv.symm
    rw [h]; exact hc.deriv
  have ha : ∀ x, HasDerivAt (fun y => (φ y).re) (φ' x).re x := fun x => by
    simpa using Complex.reCLM.hasFDerivAt.comp_hasDerivAt x (hφ x)
  have hb : ∀ x, HasDerivAt (fun y => (φ y).im) (φ' x).im x := fun x => by
    simpa using Complex.imCLM.hasFDerivAt.comp_hasDerivAt x (hφ x)
  have hn : ∀ x, HasDerivAt (fun y => ‖φ y‖ ^ 2)
      (2 * ((φ x).re * (φ' x).re + (φ x).im * (φ' x).im)) x := by
    intro x
    have e : (fun y => ‖φ y‖ ^ 2) = fun y => (φ y).re ^ 2 + (φ y).im ^ 2 := by
      funext y; rw [Complex.sq_norm, Complex.normSq_apply]; ring
    rw [e]
    exact (((ha x).pow 2).add ((hb x).pow 2)).congr_deriv (by push_cast; ring)
  have hg : ∀ x, HasDerivAt (fun y => S y * ‖φ y‖ ^ 2)
      (S' x * ‖φ x‖ ^ 2 + S x * (2 * ((φ x).re * (φ' x).re + (φ x).im * (φ' x).im))) x :=
    fun x => (hS x).mul (hn x)
  have csA : HasCompactSupport (fun x => φ' x + (S x : ℂ) * φ x) := hc'.add hc.mul_left
  have i1 : Integrable (fun x => ‖φ' x + (S x : ℂ) * φ x‖ ^ 2) :=
    (by fun_prop : Continuous fun x => ‖φ' x + (S x : ℂ) * φ x‖ ^ 2).integrable_of_hasCompactSupport
      (csA.mono fun x hx h0 => hx (by simp [h0]))
  have i2 : Integrable (fun x => (V x + S' x - S x ^ 2) * ‖φ x‖ ^ 2) :=
    (by fun_prop : Continuous fun x => (V x + S' x - S x ^ 2) * ‖φ x‖ ^ 2).integrable_of_hasCompactSupport
      (hc.mono fun x hx h0 => hx (by simp [h0]))
  have ig : Integrable (fun x => S x * ‖φ x‖ ^ 2) :=
    (by fun_prop : Continuous fun x => S x * ‖φ x‖ ^ 2).integrable_of_hasCompactSupport
      (hc.mono fun x hx h0 => hx (by simp [h0]))
  have ig' : Integrable (fun x =>
      S' x * ‖φ x‖ ^ 2 + S x * (2 * ((φ x).re * (φ' x).re + (φ x).im * (φ' x).im))) :=
    (by fun_prop : Continuous fun x =>
        S' x * ‖φ x‖ ^ 2 + S x * (2 * ((φ x).re * (φ' x).re + (φ x).im * (φ' x).im))).integrable_of_hasCompactSupport
      (hc.mono fun x hx h0 => hx (by simp [h0]))
  have h0 := integral_eq_zero_of_hasDerivAt_of_integrable hg ig' ig
  have hpt : (fun x => ‖φ' x‖ ^ 2 + V x * ‖φ x‖ ^ 2) = fun x =>
      (‖φ' x + (S x : ℂ) * φ x‖ ^ 2 + (V x + S' x - S x ^ 2) * ‖φ x‖ ^ 2)
        - (S' x * ‖φ x‖ ^ 2 + S x * (2 * ((φ x).re * (φ' x).re + (φ x).im * (φ' x).im))) := by
    funext x
    simp only [Complex.sq_norm, Complex.normSq_apply, Complex.add_re, Complex.add_im, Complex.mul_re,
      Complex.mul_im, Complex.ofReal_re, Complex.ofReal_im]
    ring
  have i12 : Integrable (fun x =>
      ‖φ' x + (S x : ℂ) * φ x‖ ^ 2 + (V x + S' x - S x ^ 2) * ‖φ x‖ ^ 2) := i1.add i2
  rw [hpt, integral_sub i12 ig', integral_add i1 i2, h0, sub_zero]

/-- The Corollary of Lemma 1. -/
theorem form_nonneg_of_sdef (V S S' : ℝ → ℝ) (φ φ' : ℝ → ℂ)
    (hV : Continuous V) (hS : ∀ x, HasDerivAt S (S' x) x) (hS' : Continuous S')
    (hφ : ∀ x, HasDerivAt φ (φ' x) x) (hφ' : Continuous φ') (hc : HasCompactSupport φ)
    (hVt : ∀ x, 0 ≤ V x + S' x - S x ^ 2) :
    0 ≤ ∫ x, (‖φ' x‖ ^ 2 + V x * ‖φ x‖ ^ 2) := by
  rw [sdef_identity V S S' φ φ' hV hS hS' hφ hφ' hc]
  exact add_nonneg (integral_nonneg fun x => by positivity)
    (integral_nonneg fun x => mul_nonneg (hVt x) (by positivity))

/-! ### Lemma 2: the ansatz (units r_H = 1, ρ = r, z = 1 − 1/ρ, ′ = d/dρ) -/

noncomputable def zc (ρ : ℝ) : ℝ := 1 - ρ⁻¹

theorem one_sub_zc (ρ : ℝ) : 1 - zc ρ = ρ⁻¹ := by unfold zc; ring

theorem zc_hasDerivAt (ρ : ℝ) (hρ : ρ ≠ 0) : HasDerivAt zc ((1 - zc ρ) ^ 2) ρ := by
  have h := (hasDerivAt_inv hρ).const_sub 1
  refine h.congr_deriv ?_
  rw [one_sub_zc]; field_simp

/-- f(ρ) = F(z): f′ = (1 − z)² f_z. -/
theorem f_hasDerivAt (F F' : ℝ → ℝ) (ρ : ℝ) (hρ : ρ ≠ 0) (hF : HasDerivAt F (F' (zc ρ)) (zc ρ)) :
    HasDerivAt (fun r => F (zc r)) ((1 - zc ρ) ^ 2 * F' (zc ρ)) ρ :=
  (hF.comp ρ (zc_hasDerivAt ρ hρ)).congr_deriv (by ring)

/-- β = (1 − z)P: β′ = (1 − z)²(−P + (1 − z)P_z). -/
theorem beta_hasDerivAt (P P' : ℝ → ℝ) (ρ : ℝ) (hρ : ρ ≠ 0) (hP : HasDerivAt P (P' (zc ρ)) (zc ρ)) :
    HasDerivAt (fun r => (1 - zc r) * P (zc r))
      ((1 - zc ρ) ^ 2 * (-P (zc ρ) + (1 - zc ρ) * P' (zc ρ))) ρ := by
  have hz := zc_hasDerivAt ρ hρ
  have h1 : HasDerivAt (fun r => 1 - zc r) (-(1 - zc ρ) ^ 2) ρ := hz.const_sub 1
  have h2 : HasDerivAt (fun r => P (zc r)) (P' (zc ρ) * (1 - zc ρ) ^ 2) ρ := hP.comp ρ hz
  exact (h1.mul h2).congr_deriv (by ring)

/-- METHOD.md Lemma 2's N, with U = U₋, H = H₋, F = f and F' = f_z as functions of z. -/
noncomputable def Nz (U H F F' P P' : ℝ → ℝ) (z : ℝ) : ℝ :=
  U z - 64 * H z ^ 2 * ((1 - z) * F' z * P z + F z * (-P z + (1 - z) * P' z + P z ^ 2))

/-- Lemma 2: V + f·S′ − S² = f N / (64ρ²H₋²), with S = −fβ, S′ = −(f′β + fβ′) and V = fU₋/(64ρ²H₋²). -/
theorem ansatz_identity (U H F F' P P' : ℝ → ℝ) (ρ : ℝ) (hρ : ρ ≠ 0) (hH : H (zc ρ) ≠ 0) :
    F (zc ρ) * U (zc ρ) / (64 * ρ ^ 2 * H (zc ρ) ^ 2)
      + F (zc ρ) * (-((1 - zc ρ) ^ 2 * F' (zc ρ) * ((1 - zc ρ) * P (zc ρ))
          + F (zc ρ) * ((1 - zc ρ) ^ 2 * (-P (zc ρ) + (1 - zc ρ) * P' (zc ρ)))))
      - (-(F (zc ρ) * ((1 - zc ρ) * P (zc ρ)))) ^ 2
    = F (zc ρ) * Nz U H F F' P P' (zc ρ) / (64 * ρ ^ 2 * H (zc ρ) ^ 2) := by
  simp only [Nz, one_sub_zc]
  field_simp
  ring

noncomputable def Vrho (U H F : ℝ → ℝ) (ρ : ℝ) : ℝ := F (zc ρ) * U (zc ρ) / (64 * ρ ^ 2 * H (zc ρ) ^ 2)

noncomputable def Srho (F P : ℝ → ℝ) (ρ : ℝ) : ℝ := -(F (zc ρ) * ((1 - zc ρ) * P (zc ρ)))

noncomputable def dSrho (F F' P P' : ℝ → ℝ) (ρ : ℝ) : ℝ :=
  -((1 - zc ρ) ^ 2 * F' (zc ρ) * ((1 - zc ρ) * P (zc ρ))
    + F (zc ρ) * ((1 - zc ρ) ^ 2 * (-P (zc ρ) + (1 - zc ρ) * P' (zc ρ))))

theorem Srho_hasDerivAt (F F' P P' : ℝ → ℝ) (ρ : ℝ) (hρ : ρ ≠ 0)
    (hF : HasDerivAt F (F' (zc ρ)) (zc ρ)) (hP : HasDerivAt P (P' (zc ρ)) (zc ρ)) :
    HasDerivAt (Srho F P) (dSrho F F' P P' ρ) ρ :=
  ((f_hasDerivAt F F' ρ hρ hF).mul (beta_hasDerivAt P P' ρ hρ hP)).neg.congr_deriv
    (by unfold dSrho; ring)

/-! ### Proposition 3 -/

theorem zc_mem (ρ : ℝ) (hρ : 1 < ρ) : 0 < zc ρ ∧ zc ρ < 1 := by
  have h0 : 0 < ρ⁻¹ := inv_pos.2 (by linarith)
  have h1 : ρ⁻¹ < 1 := inv_lt_one_of_one_lt₀ hρ
  unfold zc; constructor <;> linarith

/-- Proposition 3: N ≥ 0 on (0, 1) gives a nonnegative quadratic form in r*, for every R with dR/dr* = f(R) and
R > 1 (the inverse tortoise map is one). -/
theorem prop3 (U H F F' P P' R : ℝ → ℝ)
    (hF : ∀ z, HasDerivAt F (F' z) z) (hP : ∀ z, HasDerivAt P (P' z) z)
    (hF' : Continuous F') (hP' : Continuous P') (hU : Continuous U) (hHc : Continuous H)
    (hR : ∀ t, HasDerivAt R (F (zc (R t))) t) (hR1 : ∀ t, 1 < R t)
    (hf : ∀ z, 0 < z → z < 1 → 0 ≤ F z)
    (hH : ∀ z, 0 < z → z < 1 → H z ≠ 0)
    (hN : ∀ z, 0 < z → z < 1 → 0 ≤ Nz U H F F' P P' z)
    (φ φ' : ℝ → ℂ) (hφ : ∀ x, HasDerivAt φ (φ' x) x) (hφ' : Continuous φ')
    (hc : HasCompactSupport φ) :
    0 ≤ ∫ t, (‖φ' t‖ ^ 2 + Vrho U H F (R t) * ‖φ t‖ ^ 2) := by
  have hRc : Continuous R := continuous_iff_continuousAt.2 fun t => (hR t).continuousAt
  have hFc : Continuous F := continuous_iff_continuousAt.2 fun z => (hF z).continuousAt
  have hPc : Continuous P := continuous_iff_continuousAt.2 fun z => (hP z).continuousAt
  have hRne : ∀ t, R t ≠ 0 := fun t => by linarith [hR1 t]
  have hzc : Continuous fun t => zc (R t) := by
    unfold zc; exact continuous_const.sub (hRc.inv₀ hRne)
  have hHne : ∀ t, H (zc (R t)) ≠ 0 := fun t =>
    hH _ (zc_mem _ (hR1 t)).1 (zc_mem _ (hR1 t)).2
  have hV : Continuous fun t => Vrho U H F (R t) := by
    unfold Vrho
    refine Continuous.div (by fun_prop) (by fun_prop) fun t => ?_
    have := hRne t; have := hHne t; positivity
  have hS : ∀ t, HasDerivAt (fun t => Srho F P (R t))
      (dSrho F F' P P' (R t) * F (zc (R t))) t := fun t =>
    (Srho_hasDerivAt F F' P P' (R t) (hRne t) (hF _) (hP _)).comp t (hR t)
  have hS' : Continuous fun t => dSrho F F' P P' (R t) * F (zc (R t)) := by
    unfold dSrho; fun_prop
  refine form_nonneg_of_sdef (fun t => Vrho U H F (R t)) (fun t => Srho F P (R t))
    (fun t => dSrho F F' P P' (R t) * F (zc (R t))) φ φ' hV hS hS' hφ hφ' hc fun t => ?_
  have hm := zc_mem _ (hR1 t)
  have key := ansatz_identity U H F F' P P' (R t) (hRne t) (hHne t)
  have e : Vrho U H F (R t) + dSrho F F' P P' (R t) * F (zc (R t)) - Srho F P (R t) ^ 2
      = F (zc (R t)) * Nz U H F F' P P' (zc (R t)) / (64 * R t ^ 2 * H (zc (R t)) ^ 2) := by
    rw [← key]; unfold Vrho dSrho Srho; ring
  rw [e]
  have := hRne t; have := hHne t
  exact div_nonneg (mul_nonneg (hf _ hm.1 hm.2) (hN _ hm.1 hm.2)) (by positivity)

/-! ### Remarks of METHOD.md (general) -/

theorem N_at_horizon (U H F F' P P' : ℝ → ℝ) (hF0 : F 0 = 0) :
    Nz U H F F' P P' 0 = U 0 - 64 * H 0 ^ 2 * F' 0 * P 0 := by
  unfold Nz; rw [hF0]; ring

/-- With P = P_true − ε: N changes by 64H²ε[(1 − z)f_z + f(2P_true − 1 − ε)]; if N(P_true) = 0 this is METHOD's
ρ²(Ṽ/f)·64H₋², by `rho_fprime`. -/
theorem N_eps_shift (U H F F' P P' : ℝ → ℝ) (ε z : ℝ) :
    Nz U H F F' (fun w => P w - ε) P' z
      = Nz U H F F' P P' z + 64 * H z ^ 2 * ε * ((1 - z) * F' z + F z * (2 * P z - 1 - ε)) := by
  unfold Nz; ring

theorem rho_fprime (F' : ℝ → ℝ) (ρ : ℝ) (hρ : ρ ≠ 0) :
    ρ * ((1 - zc ρ) ^ 2 * F' (zc ρ)) = (1 - zc ρ) * F' (zc ρ) := by
  rw [one_sub_zc]; field_simp

/-! ### D = 6 (TARGET.md §1), in units r_H = 1 -/

def Hm (m δ x : ℝ) : ℝ := m + 10 * (1 + m * δ) * x

def Um (m δ x : ℝ) : ℝ :=
  -400000 * δ * (1 + m * δ) ^ 3 * x ^ 4 - 1600 * (1 + m * δ) ^ 2 * (50 * m * δ - 16) * x ^ 3
    + 7680 * m * (1 + m * δ) * x ^ 2 - 16 * m * (5 * m * (96 - 4 * m) * δ + 480) * x + 64 * m ^ 3 + 384 * m ^ 2

noncomputable def xH (q : ℝ) : ℝ := 2 / (1 + Real.sqrt (1 - q ^ 2))

noncomputable def x6 (q z : ℝ) : ℝ := xH q * (1 - z) ^ 3

noncomputable def F6 (q z : ℝ) : ℝ := 1 - x6 q z + q ^ 2 * x6 q z ^ 2 / 4

noncomputable def F6' (q z : ℝ) : ℝ := 3 * xH q * (1 - z) ^ 2 * (1 - q ^ 2 * x6 q z / 2)

noncomputable def H6 (q m δ z : ℝ) : ℝ := Hm m δ (x6 q z)

noncomputable def U6 (q m δ z : ℝ) : ℝ := Um m δ (x6 q z)

theorem xH_pos (q : ℝ) : 0 < xH q := by unfold xH; positivity

/-- In units r_H = 1, TARGET.md's r_H³ = M(1 + √(1 − q²)) = 1 gives x_H = 2M. -/
theorem xH_eq_twoM (q M : ℝ) (hM : M * (1 + Real.sqrt (1 - q ^ 2)) = 1) : xH q = 2 * M := by
  have hpos : 0 < 1 + Real.sqrt (1 - q ^ 2) := by positivity
  unfold xH; field_simp; linarith

theorem x6_zc (q ρ : ℝ) : x6 q (zc ρ) = xH q / ρ ^ 3 := by
  unfold x6; rw [one_sub_zc]; field_simp

/-- F6 at z = 1 − 1/ρ is TARGET.md's f = 1 − 2M/ρ³ + Q²/ρ⁶ with Q = qM. -/
theorem F6_zc_TARGET (q M ρ : ℝ) (hM : M * (1 + Real.sqrt (1 - q ^ 2)) = 1) :
    F6 q (zc ρ) = 1 - 2 * M / ρ ^ 3 + (q * M) ^ 2 / ρ ^ 6 := by
  unfold F6; rw [x6_zc, xH_eq_twoM q M hM]; ring

/-- Vrho with the D = 6 data is TARGET.md's V = f U₋/(64 r² H₋²) at r = ρ, x = x_H/ρ³. -/
theorem Vrho_D6 (q m δ ρ : ℝ) :
    Vrho (U6 q m δ) (H6 q m δ) (F6 q) ρ
      = (1 - xH q / ρ ^ 3 + q ^ 2 * (xH q / ρ ^ 3) ^ 2 / 4) * Um m δ (xH q / ρ ^ 3)
          / (64 * ρ ^ 2 * Hm m δ (xH q / ρ ^ 3) ^ 2) := by
  unfold Vrho U6 H6 F6; rw [x6_zc]

theorem F6_hasDerivAt (q z : ℝ) : HasDerivAt (F6 q) (F6' q z) z := by
  have h1 : HasDerivAt (fun w : ℝ => (1 - w) ^ 3) (3 * (1 - z) ^ 2 * (-1)) z := by
    simpa using ((hasDerivAt_id z).const_sub 1).pow 3
  have hx : HasDerivAt (fun w => x6 q w) (xH q * (3 * (1 - z) ^ 2 * (-1))) z := by
    unfold x6; exact h1.const_mul (xH q)
  have h := (hx.const_sub 1).add ((hx.pow 2).const_mul (q ^ 2) |>.div_const 4)
  refine (h.congr_deriv ?_)
  unfold F6' x6; push_cast; ring

/-- The horizon: f(z = 0) = 0 (as BHModesA1.f_horizon). -/
theorem F6_zero (q : ℝ) (hq : q ^ 2 ≤ 1) : F6 q 0 = 0 := by
  unfold F6 x6 xH
  have hs : Real.sqrt (1 - q ^ 2) ^ 2 = 1 - q ^ 2 := Real.sq_sqrt (by linarith)
  have hpos : 0 < 1 + Real.sqrt (1 - q ^ 2) := by positivity
  field_simp
  linear_combination 4 * hs

/-- f > 0 on the exterior, 0 < z < 1 (as BHModesA1.f_pos_exterior). -/
theorem F6_pos (q z : ℝ) (hq : q ^ 2 ≤ 1) (hz0 : 0 < z) (hz1 : z < 1) : 0 < F6 q z := by
  have hxH := xH_pos q
  have hw0 : 0 < (1 - z) ^ 3 := by have : 0 < 1 - z := by linarith
                                   positivity
  have hw1 : (1 - z) ^ 3 < 1 := by
    have h0 : 0 ≤ 1 - z := by linarith
    have h1 : 1 - z < 1 := by linarith
    calc (1 - z) ^ 3 < 1 ^ 3 := by gcongr
      _ = 1 := by norm_num
  set x := x6 q z with hxdef
  have hx0 : 0 ≤ x := by rw [hxdef]; unfold x6; positivity
  have hx : x < 2 / (1 + Real.sqrt (1 - q ^ 2)) := by
    rw [hxdef]; unfold x6
    have : xH q * (1 - z) ^ 3 < xH q * 1 := by gcongr
    unfold xH at this ⊢; linarith
  unfold F6; rw [← hxdef]
  set s := Real.sqrt (1 - q ^ 2) with hs_def
  have hs : s ^ 2 = 1 - q ^ 2 := Real.sq_sqrt (by linarith)
  have hs0 : 0 ≤ s := Real.sqrt_nonneg _
  have hpos : 0 < 1 + s := by linarith
  have hx' : x * (1 + s) < 2 := by rwa [lt_div_iff₀ hpos] at hx
  have h1 : 0 < 2 - x * (1 + s) := by linarith
  have h2 : 0 < 2 - x * (1 - s) := by nlinarith
  nlinarith [mul_pos h1 h2]

theorem H6_pos (q m δ z : ℝ) (hm : 0 < m) (hδ : 0 ≤ δ) (hz1 : z ≤ 1) : 0 < H6 q m δ z := by
  have hxH := xH_pos q
  have h0 : 0 ≤ 1 - z := by linarith
  unfold H6 Hm x6; positivity

/-- Proposition 3 at D = 6: for q² ≤ 1, m > 0, δ ≥ 0, any C¹ P, and any R with dR/dr* = f(R) and R > 1. -/
theorem prop3_D6 (q m δ : ℝ) (hq : q ^ 2 ≤ 1) (hm : 0 < m) (hδ : 0 ≤ δ) (P P' R : ℝ → ℝ)
    (hP : ∀ z, HasDerivAt P (P' z) z) (hP' : Continuous P')
    (hR : ∀ t, HasDerivAt R (F6 q (zc (R t))) t) (hR1 : ∀ t, 1 < R t)
    (hN : ∀ z, 0 < z → z < 1 → 0 ≤ Nz (U6 q m δ) (H6 q m δ) (F6 q) (F6' q) P P' z)
    (φ φ' : ℝ → ℂ) (hφ : ∀ x, HasDerivAt φ (φ' x) x) (hφ' : Continuous φ')
    (hc : HasCompactSupport φ) :
    0 ≤ ∫ t, (‖φ' t‖ ^ 2 + Vrho (U6 q m δ) (H6 q m δ) (F6 q) (R t) * ‖φ t‖ ^ 2) := by
  refine prop3 (U6 q m δ) (H6 q m δ) (F6 q) (F6' q) P P' R (F6_hasDerivAt q) hP ?_ hP' ?_ ?_ hR hR1
    (fun z hz0 hz1 => (F6_pos q z hq hz0 hz1).le)
    (fun z _ hz1 => (H6_pos q m δ z hm hδ hz1.le).ne') hN φ φ' hφ hφ' hc
  · unfold F6' x6; fun_prop
  · unfold U6 Um x6; fun_prop
  · unfold H6 Hm x6; fun_prop

/-- The Remark at z = 1 (spatial infinity), D = 6. -/
theorem N_at_infinity_D6 (q m δ : ℝ) (P P' : ℝ → ℝ) :
    Nz (U6 q m δ) (H6 q m δ) (F6 q) (F6' q) P P' 1 = 64 * m ^ 2 * (m + 6 - P 1 ^ 2 + P 1) := by
  unfold Nz U6 H6 F6 F6' Um Hm x6; ring

/-- For ℓ = 2 (m = 6): N(1) > 0 exactly when −3 < P(1) < 4. -/
theorem N_at_infinity_ell2 (q δ : ℝ) (P P' : ℝ → ℝ) :
    0 < Nz (U6 q 6 δ) (H6 q 6 δ) (F6 q) (F6' q) P P' 1 ↔ -3 < P 1 ∧ P 1 < 4 := by
  rw [N_at_infinity_D6]
  constructor
  · intro h
    have h' : 0 < 12 - P 1 ^ 2 + P 1 := by nlinarith
    constructor <;> nlinarith
  · rintro ⟨h1, h2⟩
    have : 0 < (4 - P 1) * (P 1 + 3) := mul_pos (by linarith) (by linarith)
    nlinarith

/-- The Remark at z = 0 (the horizon), D = 6. -/
theorem N_at_horizon_D6 (q m δ : ℝ) (hq : q ^ 2 ≤ 1) (P P' : ℝ → ℝ) :
    Nz (U6 q m δ) (H6 q m δ) (F6 q) (F6' q) P P' 0
      = U6 q m δ 0 - 64 * H6 q m δ 0 ^ 2 * F6' q 0 * P 0 :=
  N_at_horizon _ _ _ _ _ _ (F6_zero q hq)

end BHModes.P3
