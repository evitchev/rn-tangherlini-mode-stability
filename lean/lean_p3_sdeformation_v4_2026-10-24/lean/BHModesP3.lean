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

/-! ### v2 (2026-10-23): Proposition 3 with P needed only on (0, 1)

The bh-modes lead's optional item of 2026-10-23, from the session-R lead's reading (BHM-085 §1.3), with the
statement of bh-modes results/p3/METHOD_ADDENDUM_2.md (BHM-086). `prop3` above asks P to have the derivative P′ at
every z and P′ to be continuous on ℝ. HD-S's ζ-designs have P = P̂/(z + δ_b)^d, with a pole at z = −δ_b < 0, which
`pole_not_differentiable` shows that hypothesis excludes. `prop3_Ioo` asks for P′ only at the points of (0, 1), and
for P′ to be continuous only on (0, 1). Its other hypotheses are `prop3`'s, unchanged. Lines 1–392 of this file are
the first build's, byte for byte. -/

/-- Proposition 3 with P C¹ on (0, 1) only: nothing is assumed about P or P′ outside (0, 1). -/
theorem prop3_Ioo (U H F F' P P' R : ℝ → ℝ)
    (hF : ∀ z, HasDerivAt F (F' z) z) (hP : ∀ z, 0 < z → z < 1 → HasDerivAt P (P' z) z)
    (hF' : Continuous F') (hP' : ContinuousOn P' (Set.Ioo 0 1)) (hU : Continuous U) (hHc : Continuous H)
    (hR : ∀ t, HasDerivAt R (F (zc (R t))) t) (hR1 : ∀ t, 1 < R t) (hf : ∀ z, 0 < z → z < 1 → 0 ≤ F z)
    (hH : ∀ z, 0 < z → z < 1 → H z ≠ 0)
    (hN : ∀ z, 0 < z → z < 1 → 0 ≤ Nz U H F F' P P' z)
    (φ φ' : ℝ → ℂ) (hφ : ∀ x, HasDerivAt φ (φ' x) x) (hφ' : Continuous φ')
    (hc : HasCompactSupport φ) :
    0 ≤ ∫ t, (‖φ' t‖ ^ 2 + Vrho U H F (R t) * ‖φ t‖ ^ 2) := by
  have hRc : Continuous R := continuous_iff_continuousAt.2 fun t => (hR t).continuousAt
  have hFc : Continuous F := continuous_iff_continuousAt.2 fun z => (hF z).continuousAt
  have hRne : ∀ t, R t ≠ 0 := fun t => by linarith [hR1 t]
  have hzc : Continuous fun t => zc (R t) := by
    unfold zc; exact continuous_const.sub (hRc.inv₀ hRne)
  -- P and P′ enter only along t ↦ zc (R t), which stays in (0, 1).
  have hzm : ∀ t, zc (R t) ∈ Set.Ioo (0 : ℝ) 1 := fun t => zc_mem _ (hR1 t)
  have hPz : Continuous fun t => P (zc (R t)) :=
    ContinuousOn.comp_continuous (fun z hz => (hP z hz.1 hz.2).continuousAt.continuousWithinAt) hzc hzm
  have hP'z : Continuous fun t => P' (zc (R t)) := hP'.comp_continuous hzc hzm
  have hHne : ∀ t, H (zc (R t)) ≠ 0 := fun t => hH _ (hzm t).1 (hzm t).2
  have hV : Continuous fun t => Vrho U H F (R t) := by
    unfold Vrho
    refine Continuous.div (by fun_prop) (by fun_prop) fun t => ?_
    have := hRne t; have := hHne t; positivity
  have hS : ∀ t, HasDerivAt (fun t => Srho F P (R t))
      (dSrho F F' P P' (R t) * F (zc (R t))) t := fun t =>
    (Srho_hasDerivAt F F' P P' (R t) (hRne t) (hF _) (hP _ (hzm t).1 (hzm t).2)).comp t (hR t)
  have hS' : Continuous fun t => dSrho F F' P P' (R t) * F (zc (R t)) := by
    have hFz : Continuous fun t => F (zc (R t)) := hFc.comp hzc
    have hF'z : Continuous fun t => F' (zc (R t)) := hF'.comp hzc
    have h1z : Continuous fun t => 1 - zc (R t) := continuous_const.sub hzc
    unfold dSrho
    exact ((((h1z.pow 2).mul hF'z).mul (h1z.mul hPz)).add
      (hFz.mul ((h1z.pow 2).mul (hPz.neg.add (h1z.mul hP'z))))).neg.mul hFz
  refine form_nonneg_of_sdef (fun t => Vrho U H F (R t)) (fun t => Srho F P (R t))
    (fun t => dSrho F F' P P' (R t) * F (zc (R t))) φ φ' hV hS hS' hφ hφ' hc fun t => ?_
  have hm := hzm t
  have key := ansatz_identity U H F F' P P' (R t) (hRne t) (hHne t)
  have e : Vrho U H F (R t) + dSrho F F' P P' (R t) * F (zc (R t)) - Srho F P (R t) ^ 2
      = F (zc (R t)) * Nz U H F F' P P' (zc (R t)) / (64 * R t ^ 2 * H (zc (R t)) ^ 2) := by
    rw [← key]; unfold Vrho dSrho Srho; ring
  rw [e]
  have := hRne t; have := hHne t
  exact div_nonneg (mul_nonneg (hf _ hm.1 hm.2) (hN _ hm.1 hm.2)) (by positivity)

/-- METHOD_ADDENDUM_2's form: P C¹ on an open interval (a, b) containing [0, 1]. -/
theorem prop3_near (U H F F' P P' R : ℝ → ℝ) (a b : ℝ) (ha : a < 0) (hb : 1 < b)
    (hF : ∀ z, HasDerivAt F (F' z) z) (hP : ∀ z, a < z → z < b → HasDerivAt P (P' z) z)
    (hF' : Continuous F') (hP' : ContinuousOn P' (Set.Ioo a b)) (hU : Continuous U) (hHc : Continuous H)
    (hR : ∀ t, HasDerivAt R (F (zc (R t))) t) (hR1 : ∀ t, 1 < R t) (hf : ∀ z, 0 < z → z < 1 → 0 ≤ F z)
    (hH : ∀ z, 0 < z → z < 1 → H z ≠ 0)
    (hN : ∀ z, 0 < z → z < 1 → 0 ≤ Nz U H F F' P P' z)
    (φ φ' : ℝ → ℂ) (hφ : ∀ x, HasDerivAt φ (φ' x) x) (hφ' : Continuous φ')
    (hc : HasCompactSupport φ) :
    0 ≤ ∫ t, (‖φ' t‖ ^ 2 + Vrho U H F (R t) * ‖φ t‖ ^ 2) :=
  prop3_Ioo U H F F' P P' R hF (fun z h0 h1 => hP z (by linarith) (by linarith)) hF'
    (hP'.mono (Set.Ioo_subset_Ioo (by linarith) (by linarith))) hU hHc hR hR1 hf hH hN φ φ' hφ hφ' hc

/-- A ζ-design: P = P̂/(z + δ)^d. HD-S's P̂ is a polynomial in z for each μ in a box, and δ = δ_b > 0. -/
noncomputable def Pzeta (Ph : ℝ → ℝ) (δ : ℝ) (d : ℕ) (z : ℝ) : ℝ := Ph z / (z + δ) ^ d

/-- Its derivative, (P̂′(z + δ) − dP̂)/(z + δ)^(d+1), with Ph' = P̂′. -/
noncomputable def Pzeta' (Ph Ph' : ℝ → ℝ) (δ : ℝ) (d : ℕ) (z : ℝ) : ℝ :=
  (Ph' z * (z + δ) - d * Ph z) / (z + δ) ^ (d + 1)

theorem Pzeta_hasDerivAt (Ph Ph' : ℝ → ℝ) (δ : ℝ) (d : ℕ) (z : ℝ) (hPh : HasDerivAt Ph (Ph' z) z)
    (hz : 0 < z + δ) : HasDerivAt (Pzeta Ph δ d) (Pzeta' Ph Ph' δ d z) z := by
  have hs : HasDerivAt (fun w => (w + δ) ^ d) ((d : ℝ) * (z + δ) ^ (d - 1)) z := by
    simpa using ((hasDerivAt_id z).add_const δ).pow d
  have hz0 : z + δ ≠ 0 := hz.ne'
  have hne : (z + δ) ^ d ≠ 0 := pow_ne_zero _ hz0
  refine (hPh.div hs hne).congr_deriv ?_
  unfold Pzeta'
  rcases Nat.eq_zero_or_pos d with rfl | hd
  · simp; field_simp
  · obtain ⟨k, rfl⟩ : ∃ k, d = k + 1 := ⟨d - 1, by omega⟩
    simp only [Nat.add_sub_cancel]
    field_simp
    push_cast
    ring

theorem Pzeta'_continuousOn (Ph Ph' : ℝ → ℝ) (δ : ℝ) (hδ : 0 ≤ δ) (d : ℕ) (hPh : Continuous Ph)
    (hPh' : Continuous Ph') : ContinuousOn (Pzeta' Ph Ph' δ d) (Set.Ioo 0 1) := by
  unfold Pzeta'
  refine ContinuousOn.div (by fun_prop) (by fun_prop) fun z hz => ?_
  have : 0 < z + δ := by linarith [hz.1]
  positivity

/-- `prop3_Ioo` for a ζ-design with δ ≥ 0: the pole z = −δ lies outside (0, 1). -/
theorem prop3_zeta (U H F F' Ph Ph' R : ℝ → ℝ) (δ : ℝ) (d : ℕ) (hδ : 0 ≤ δ)
    (hF : ∀ z, HasDerivAt F (F' z) z) (hPh : ∀ z, HasDerivAt Ph (Ph' z) z)
    (hF' : Continuous F') (hPh' : Continuous Ph') (hU : Continuous U) (hHc : Continuous H)
    (hR : ∀ t, HasDerivAt R (F (zc (R t))) t) (hR1 : ∀ t, 1 < R t) (hf : ∀ z, 0 < z → z < 1 → 0 ≤ F z)
    (hH : ∀ z, 0 < z → z < 1 → H z ≠ 0)
    (hN : ∀ z, 0 < z → z < 1 → 0 ≤ Nz U H F F' (Pzeta Ph δ d) (Pzeta' Ph Ph' δ d) z)
    (φ φ' : ℝ → ℂ) (hφ : ∀ x, HasDerivAt φ (φ' x) x) (hφ' : Continuous φ')
    (hc : HasCompactSupport φ) :
    0 ≤ ∫ t, (‖φ' t‖ ^ 2 + Vrho U H F (R t) * ‖φ t‖ ^ 2) :=
  prop3_Ioo U H F F' (Pzeta Ph δ d) (Pzeta' Ph Ph' δ d) R hF
    (fun z h0 _ => Pzeta_hasDerivAt Ph Ph' δ d z (hPh z) (by linarith)) hF'
    (Pzeta'_continuousOn Ph Ph' δ hδ d (continuous_iff_continuousAt.2 fun z => (hPh z).continuousAt) hPh')
    hU hHc hR hR1 hf hH hN φ φ' hφ hφ' hc

/-- Why `prop3_Ioo` is needed: the ζ-design P = 1/(z + δ) (P̂ = 1, d = 1) has no P′ with HasDerivAt P (P′ z) z at every
z, as `prop3` asks, since P is not continuous at its pole z = −δ. -/
theorem pole_not_differentiable (δ : ℝ) (P' : ℝ → ℝ) : ¬ ∀ z, HasDerivAt (Pzeta (fun _ => 1) δ 1) (P' z) z := by
  have e : Pzeta (fun _ => 1) δ 1 = fun z => (z + δ)⁻¹ := by
    funext z; simp [Pzeta]
  rw [e]
  intro h
  have hc : ContinuousAt (fun z : ℝ => (z + δ)⁻¹) (-δ) := (h (-δ)).continuousAt
  have h1 : Filter.Tendsto (fun z : ℝ => z + δ) (nhdsWithin (-δ) (Set.Ioi (-δ))) (nhdsWithin 0 (Set.Ioi 0)) := by
    refine tendsto_nhdsWithin_iff.2 ⟨?_, eventually_nhdsWithin_of_forall fun z hz => ?_⟩
    · exact ((continuous_id.add continuous_const).tendsto' (-δ) 0 (by simp)).mono_left nhdsWithin_le_nhds
    · simp only [Set.mem_Ioi] at hz ⊢; linarith
  exact not_tendsto_nhds_of_tendsto_atTop h1.inv_tendsto_nhdsGT_zero _
    (hc.tendsto.mono_left nhdsWithin_le_nhds)

/-! ### v3 (2026-10-23): Proposition 3 at general n (D = n + 2), K = 1, Λ = 0

The bh-modes lead's request of 2026-10-23 (BHM-090): the general-n instance of `prop3_Ioo`, as `prop3_D6` is the
n = 4 instance of `prop3`. `HmN` and `UmN` are S5 (5.62b) and (5.63b) at general n, session-L's transcription from the
c_n layer (`BHModes.Cn.Hm` and `BHModes.Cn.Um`, bodies copied byte for byte), taken at K = 1 and y = 0. In units
r_H = 1, x = x_H(1 − z)^(n−1) and f = 1 − x + q²x²/4 (bh-modes TARGET_HD.md §1). Lines 1–520 of this file are the v2
build's, byte for byte. -/

/-- S5 (5.62b) at general n (the c_n layer's `Hm`). -/
noncomputable def HmN (n m δ x : ℝ) : ℝ := m + n * (n + 1) / 2 * (1 + m * δ) * x

/-- S5 (5.63b) at general n, with the horizon curvature K and the cosmological term y (the c_n layer's `Um`). -/
noncomputable def UmN (n K m δ x y : ℝ) : ℝ :=
  (-4 * n ^ 3 * (n + 2) * (n + 1) ^ 2 * (1 + m * δ) ^ 2 * x ^ 2 + 48 * n ^ 2 * (n + 1) * (n - 2) * m * (1 + m * δ) * x
      - 16 * (n - 2) * (n - 4) * m ^ 2) * y
    - n ^ 3 * (3 * n - 2) * (n + 1) ^ 4 * δ * (1 + m * δ) ^ 3 * x ^ 4
    - 4 * n ^ 2 * (n + 1) ^ 2 * (1 + m * δ) ^ 2 * ((n + 1) * (3 * n - 2) * m * δ - n ^ 2) * x ^ 3
    + 4 * (n + 1) * (1 + m * δ) * (m * (n - 2) * (n - 4) * (n + 1) * (m + n ^ 2 * K) * δ
        + 4 * n * (2 * n ^ 2 - 3 * n + 4) * m + n ^ 2 * (n - 2) * (n - 4) * (n + 1) * K) * x ^ 2
    - 16 * m * ((n + 1) * m * (-4 * m + 3 * n ^ 2 * (n - 2) * K) * δ + 3 * n * (n - 4) * m
        + 3 * n ^ 2 * (n + 1) * (n - 2) * K) * x
    + 64 * m ^ 3 + 16 * n * (n + 2) * m ^ 2 * K

/-- x = x_H(1 − z)^(n−1). -/
noncomputable def xn (n : ℕ) (q z : ℝ) : ℝ := xH q * (1 - z) ^ (n - 1)

/-- f = 1 − x + q²x²/4, as a function of z. -/
noncomputable def Fn (n : ℕ) (q z : ℝ) : ℝ := 1 - xn n q z + q ^ 2 * xn n q z ^ 2 / 4

/-- f_z = (n − 1)x_H(1 − z)^(n−2)(1 − q²x/2). -/
noncomputable def Fn' (n : ℕ) (q z : ℝ) : ℝ := (n - 1) * xH q * (1 - z) ^ (n - 2) * (1 - q ^ 2 * xn n q z / 2)

noncomputable def Hn (n : ℕ) (q m δ z : ℝ) : ℝ := HmN n m δ (xn n q z)

noncomputable def Un (n : ℕ) (q m δ z : ℝ) : ℝ := UmN n 1 m δ (xn n q z) 0

/-- At n = 4, H₋ is TARGET.md's `Hm`. -/
theorem HmN_four (m δ x : ℝ) : HmN 4 m δ x = Hm m δ x := by
  unfold HmN Hm; ring

/-- At n = 4, K = 1 and y = 0, U₋ is TARGET.md's `Um`. -/
theorem UmN_four (m δ x : ℝ) : UmN 4 1 m δ x 0 = Um m δ x := by
  unfold UmN Um; ring

/-- At n = 4 the data are `prop3_D6`'s: f, f_z, H₋ and U₋ are F6, F6', H6 and U6. -/
theorem Dn_four (q m δ : ℝ) :
    Fn 4 q = F6 q ∧ Fn' 4 q = F6' q ∧ Hn 4 q m δ = H6 q m δ ∧ Un 4 q m δ = U6 q m δ := by
  have hx : xn 4 q = x6 q := funext fun z => by unfold xn x6; norm_num
  refine ⟨funext fun z => ?_, funext fun z => ?_, funext fun z => ?_, funext fun z => ?_⟩
  · unfold Fn F6; rw [hx]
  · unfold Fn' F6'; rw [hx]; norm_num
  · unfold Hn H6; rw [hx]; push_cast; exact HmN_four m δ (x6 q z)
  · unfold Un U6; rw [hx]; push_cast; exact UmN_four m δ (x6 q z)

theorem xn_zc (n : ℕ) (q ρ : ℝ) : xn n q (zc ρ) = xH q / ρ ^ (n - 1) := by
  unfold xn; rw [one_sub_zc, inv_pow, div_eq_mul_inv]

/-- Fn at z = 1 − 1/ρ is TARGET_HD.md's f = 1 − 2M/ρ^(n−1) + (qM)²/ρ^(2(n−1)). -/
theorem Fn_zc_TARGET (n : ℕ) (q M ρ : ℝ) (hM : M * (1 + Real.sqrt (1 - q ^ 2)) = 1) :
    Fn n q (zc ρ) = 1 - 2 * M / ρ ^ (n - 1) + (q * M) ^ 2 / (ρ ^ (n - 1)) ^ 2 := by
  unfold Fn; rw [xn_zc, xH_eq_twoM q M hM]; ring

/-- Vrho with the general-n data is TARGET_HD.md's V = f U₋/(64 r² H₋²) at r = ρ, x = x_H/ρ^(n−1). -/
theorem Vrho_Dn (n : ℕ) (q m δ ρ : ℝ) :
    Vrho (Un n q m δ) (Hn n q m δ) (Fn n q) ρ
      = (1 - xH q / ρ ^ (n - 1) + q ^ 2 * (xH q / ρ ^ (n - 1)) ^ 2 / 4) * UmN n 1 m δ (xH q / ρ ^ (n - 1)) 0
          / (64 * ρ ^ 2 * HmN n m δ (xH q / ρ ^ (n - 1)) ^ 2) := by
  unfold Vrho Un Hn Fn; rw [xn_zc]

theorem Fn_hasDerivAt (n : ℕ) (hn : 1 ≤ n) (q z : ℝ) : HasDerivAt (Fn n q) (Fn' n q z) z := by
  have hx : HasDerivAt (fun w => xn n q w) (xH q * (((n - 1 : ℕ) : ℝ) * (1 - z) ^ (n - 1 - 1) * (0 - 1))) z := by
    unfold xn
    exact (((hasDerivAt_const z (1 : ℝ)).sub (hasDerivAt_id z)).pow (n - 1)).const_mul (xH q)
  have h := (hx.const_sub 1).add ((hx.pow 2).const_mul (q ^ 2) |>.div_const 4)
  refine h.congr_deriv ?_
  have e1 : n - 1 - 1 = n - 2 := by omega
  have e2 : ((n - 1 : ℕ) : ℝ) = n - 1 := by rw [Nat.cast_sub hn, Nat.cast_one]
  unfold Fn' xn
  rw [e1, e2]
  norm_num
  ring

/-- The horizon: f(z = 0) = 0, at every n. -/
theorem Fn_zero (n : ℕ) (q : ℝ) (hq : q ^ 2 ≤ 1) : Fn n q 0 = 0 := by
  have h := F6_zero q hq
  unfold F6 x6 at h
  unfold Fn xn
  simpa using h

/-- f > 0 on the exterior, 0 < z < 1, for n ≥ 2 (as `F6_pos`). -/
theorem Fn_pos (n : ℕ) (hn : 2 ≤ n) (q z : ℝ) (hq : q ^ 2 ≤ 1) (hz0 : 0 < z) (hz1 : z < 1) : 0 < Fn n q z := by
  have hxH := xH_pos q
  have h1z : 0 < 1 - z := by linarith
  have hw1 : (1 - z) ^ (n - 1) < 1 := pow_lt_one₀ h1z.le (by linarith) (by omega)
  set x := xn n q z with hxdef
  have hx0 : 0 ≤ x := by rw [hxdef]; unfold xn; positivity
  have hx : x < 2 / (1 + Real.sqrt (1 - q ^ 2)) := by
    rw [hxdef]; unfold xn
    have : xH q * (1 - z) ^ (n - 1) < xH q * 1 := by gcongr
    unfold xH at this ⊢; linarith
  unfold Fn; rw [← hxdef]
  set s := Real.sqrt (1 - q ^ 2) with hs_def
  have hs : s ^ 2 = 1 - q ^ 2 := Real.sq_sqrt (by linarith)
  have hs0 : 0 ≤ s := Real.sqrt_nonneg _
  have hpos : 0 < 1 + s := by linarith
  have hx' : x * (1 + s) < 2 := by rwa [lt_div_iff₀ hpos] at hx
  have h1 : 0 < 2 - x * (1 + s) := by linarith
  have h2 : 0 < 2 - x * (1 - s) := by nlinarith
  nlinarith [mul_pos h1 h2]

theorem Hn_pos (n : ℕ) (q m δ z : ℝ) (hm : 0 < m) (hδ : 0 ≤ δ) (hz1 : z ≤ 1) : 0 < Hn n q m δ z := by
  have hxH := xH_pos q
  have h0 : 0 ≤ 1 - z := by linarith
  unfold Hn HmN xn; positivity

/-- Proposition 3 at general n ≥ 2 (D = n + 2), K = 1, Λ = 0: for q² ≤ 1, m > 0, δ ≥ 0, any P that is C¹ on (0, 1),
and any R with dR/dr* = f(R) and R > 1. -/
theorem prop3_Dn (n : ℕ) (hn : 2 ≤ n) (q m δ : ℝ) (hq : q ^ 2 ≤ 1) (hm : 0 < m) (hδ : 0 ≤ δ) (P P' R : ℝ → ℝ)
    (hP : ∀ z ∈ Set.Ioo (0 : ℝ) 1, HasDerivAt P (P' z) z) (hP' : ContinuousOn P' (Set.Ioo (0 : ℝ) 1))
    (hR : ∀ t, HasDerivAt R (Fn n q (zc (R t))) t) (hR1 : ∀ t, 1 < R t)
    (hN : ∀ z, 0 < z → z < 1 → 0 ≤ Nz (Un n q m δ) (Hn n q m δ) (Fn n q) (Fn' n q) P P' z)
    (φ φ' : ℝ → ℂ) (hφ : ∀ x, HasDerivAt φ (φ' x) x) (hφ' : Continuous φ')
    (hc : HasCompactSupport φ) :
    0 ≤ ∫ t, (‖φ' t‖ ^ 2 + Vrho (Un n q m δ) (Hn n q m δ) (Fn n q) (R t) * ‖φ t‖ ^ 2) := by
  refine prop3_Ioo (Un n q m δ) (Hn n q m δ) (Fn n q) (Fn' n q) P P' R (Fn_hasDerivAt n (by omega) q)
    (fun z h0 h1 => hP z ⟨h0, h1⟩) ?_ hP' ?_ ?_ hR hR1
    (fun z hz0 hz1 => (Fn_pos n hn q z hq hz0 hz1).le)
    (fun z _ hz1 => (Hn_pos n q m δ z hm hδ hz1.le).ne') hN φ φ' hφ hφ' hc
  · unfold Fn' xn; fun_prop
  · unfold Un UmN xn; fun_prop
  · unfold Hn HmN xn; fun_prop

/-- `prop3_Dn` for a ζ-design P = P̂/(z + δ_b)^d with δ_b ≥ 0 (written δb; δ is S5's). -/
theorem prop3_Dn_zeta (n : ℕ) (hn : 2 ≤ n) (q m δ : ℝ) (hq : q ^ 2 ≤ 1) (hm : 0 < m) (hδ : 0 ≤ δ)
    (Ph Ph' R : ℝ → ℝ) (δb : ℝ) (d : ℕ) (hδb : 0 ≤ δb)
    (hPh : ∀ z, HasDerivAt Ph (Ph' z) z) (hPh' : Continuous Ph')
    (hR : ∀ t, HasDerivAt R (Fn n q (zc (R t))) t) (hR1 : ∀ t, 1 < R t)
    (hN : ∀ z, 0 < z → z < 1 →
      0 ≤ Nz (Un n q m δ) (Hn n q m δ) (Fn n q) (Fn' n q) (Pzeta Ph δb d) (Pzeta' Ph Ph' δb d) z)
    (φ φ' : ℝ → ℂ) (hφ : ∀ x, HasDerivAt φ (φ' x) x) (hφ' : Continuous φ')
    (hc : HasCompactSupport φ) :
    0 ≤ ∫ t, (‖φ' t‖ ^ 2 + Vrho (Un n q m δ) (Hn n q m δ) (Fn n q) (R t) * ‖φ t‖ ^ 2) :=
  prop3_Dn n hn q m δ hq hm hδ (Pzeta Ph δb d) (Pzeta' Ph Ph' δb d) R
    (fun z hz => Pzeta_hasDerivAt Ph Ph' δb d z (hPh z) (by linarith [hz.1]))
    (Pzeta'_continuousOn Ph Ph' δb hδb d (continuous_iff_continuousAt.2 fun z => (hPh z).continuousAt) hPh')
    hR hR1 hN φ φ' hφ hφ' hc

/-- The Remark at z = 0 (the horizon), general n. -/
theorem N_at_horizon_Dn (n : ℕ) (q m δ : ℝ) (hq : q ^ 2 ≤ 1) (P P' : ℝ → ℝ) :
    Nz (Un n q m δ) (Hn n q m δ) (Fn n q) (Fn' n q) P P' 0
      = Un n q m δ 0 - 64 * Hn n q m δ 0 ^ 2 * Fn' n q 0 * P 0 :=
  N_at_horizon _ _ _ _ _ _ (Fn_zero n q hq)

/-- The Remark at z = 1 (spatial infinity), general n ≥ 2: N(1) = 64m²(m + n(n + 2)/4 − P(1)² + P(1)). -/
theorem N_at_infinity_Dn (n : ℕ) (hn : 2 ≤ n) (q m δ : ℝ) (P P' : ℝ → ℝ) :
    Nz (Un n q m δ) (Hn n q m δ) (Fn n q) (Fn' n q) P P' 1 = 64 * m ^ 2 * (m + n * (n + 2) / 4 - P 1 ^ 2 + P 1) := by
  have h0 : (1 - 1 : ℝ) ^ (n - 1) = 0 := by rw [sub_self]; exact zero_pow (by omega)
  unfold Nz Un Hn Fn Fn' UmN HmN xn
  rw [h0]
  ring

/-! ### v4 (2026-10-24): A2-S's gate G-RES, and the D = 4 Darboux identities of the [another line of this project] job `chandrasekhar`

The bh-modes lead's message 7 of 2026-10-24, §3, items (a) and (b). Lines 1–681 of this file are the v3 build's, byte
for byte. -/

/-! #### (a) G-RES (bh-modes code/a2/scert.py, `g_res`; results/a2/s/PREREG.md §3)

At q = 1 and D = 6 (n = 4), with m and δ those of ℓ, and P = a/z + b₀ + b₁z: N is a polynomial in z with
N(0) = 576H₋(2)²(ℓ(ℓ − 3)/9 − a(a + 1)), identically in ℓ, a, b₀ and b₁. N is `Nz` with `prop3_D6`'s data at q = 1,
and H₋(2) is `Hm` at x = 2, the value of x at the horizon when q = 1 (`D6_extremal`). P is not defined at z = 0. So
`g_res` says that N agrees with a polynomial p at every z ≠ 0 and gives p(0), and `g_res_tendsto` says that N(z) → p(0)
as z → 0. -/

/-- m = ℓ(ℓ + n − 1) − n at n = 4. -/
def mEll (ℓ : ℝ) : ℝ := (ℓ - 1) * (ℓ + 4)

/-- δ at n = 4 and q = 1: the root of S5 (5.58) with 1 + 2mδ = (2ℓ + 3)/5 (`mEll_dEll_S5`). -/
noncomputable def dEll (ℓ : ℝ) : ℝ := 1 / (5 * (ℓ + 4))

/-- m and δ are S5's at n = 4 and q = 1: m = ℓ(ℓ + 3) − 4, 1 + 2mδ = (2ℓ + 3)/5, and (5.58),
(1 + 2mδ)² = 1 + 4mq²/(n + 1)². -/
theorem mEll_dEll_S5 (ℓ : ℝ) (hℓ : ℓ + 4 ≠ 0) :
    mEll ℓ = ℓ * (ℓ + 3) - 4 ∧ 1 + 2 * mEll ℓ * dEll ℓ = (2 * ℓ + 3) / 5
      ∧ (1 + 2 * mEll ℓ * dEll ℓ) ^ 2 = 1 + 4 * mEll ℓ * 1 ^ 2 / (4 + 1) ^ 2 := by
  have e1 : mEll ℓ = ℓ * (ℓ + 3) - 4 := by unfold mEll; ring
  have e2 : 1 + 2 * mEll ℓ * dEll ℓ = (2 * ℓ + 3) / 5 := by unfold mEll dEll; field_simp; ring
  refine ⟨e1, e2, ?_⟩
  rw [e2, e1]; ring

/-- q = 1: x_H = 2, so x = 2(1 − z)³, f = (1 − (1 − z)³)² and f_z = 6(1 − z)²(1 − (1 − z)³). These are scert.py's
x = 2y, f = (1 − y)² and f_z, with y = (1 − z)³. -/
theorem D6_extremal (z : ℝ) :
    x6 1 z = 2 * (1 - z) ^ 3 ∧ F6 1 z = (1 - (1 - z) ^ 3) ^ 2 ∧ F6' 1 z = 6 * (1 - z) ^ 2 * (1 - (1 - z) ^ 3) := by
  have hx : xH 1 = 2 := by unfold xH; norm_num
  unfold F6 F6' x6
  rw [hx]
  exact ⟨rfl, by ring, by ring⟩

/-- The pole ansatz P = a/z + b₀ + b₁z. -/
noncomputable def Pres (a b0 b1 z : ℝ) : ℝ := a / z + b0 + b1 * z

/-- P_z = −a/z² + b₁ (`Pres_hasDerivAt`). -/
noncomputable def Pres' (a b1 z : ℝ) : ℝ := -a / z ^ 2 + b1

theorem Pres_hasDerivAt (a b0 b1 z : ℝ) (hz : z ≠ 0) : HasDerivAt (Pres a b0 b1) (Pres' a b1 z) z := by
  have h := (((hasDerivAt_inv hz).const_mul a).add_const b0).add ((hasDerivAt_id' z).const_mul b1)
  have e : Pres a b0 b1 = fun w => a * w⁻¹ + b0 + b1 * w := by
    funext w; unfold Pres; rw [div_eq_mul_inv]
  rw [e]
  refine h.congr_deriv ?_
  unfold Pres'
  field_simp

/-- H₋(2) = (ℓ + 3)(ℓ + 4), as the A2-S record gives it. -/
theorem H2_ell (ℓ : ℝ) (hℓ : ℓ + 4 ≠ 0) : Hm (mEll ℓ) (dEll ℓ) 2 = (ℓ + 3) * (ℓ + 4) := by
  unfold Hm mEll dEll; field_simp; ring

/-- U₋(2) = 576H₋(2)²·ℓ(ℓ − 3)/9: the c_n layer's C1 at n = 4, where c₄ = ℓ(ℓ − 3)/9. -/
theorem U2_ell (ℓ : ℝ) (hℓ : ℓ + 4 ≠ 0) :
    Um (mEll ℓ) (dEll ℓ) 2 = 576 * Hm (mEll ℓ) (dEll ℓ) 2 ^ 2 * (ℓ * (ℓ - 3) / 9) := by
  rw [H2_ell ℓ hℓ]; unfold Um mEll dEll; field_simp; ring

/-- G-RES: N agrees with a polynomial p at every z ≠ 0, and p(0) = 576H₋(2)²(ℓ(ℓ − 3)/9 − a(a + 1)), for every ℓ ≠ −4
and every a, b₀ and b₁. -/
theorem g_res (ℓ a b0 b1 : ℝ) (hℓ : ℓ + 4 ≠ 0) :
    ∃ p : Polynomial ℝ,
      (∀ z, z ≠ 0 → Nz (U6 1 (mEll ℓ) (dEll ℓ)) (H6 1 (mEll ℓ) (dEll ℓ)) (F6 1) (F6' 1) (Pres a b0 b1) (Pres' a b1) z
        = p.eval z)
      ∧ p.eval 0 = 576 * Hm (mEll ℓ) (dEll ℓ) 2 ^ 2 * (ℓ * (ℓ - 3) / 9 - a * (a + 1)) := by
  -- With g = 3 − 3z + z² and Q = a + b₀z + b₁z², f = z²g² and zP = Q, so the bracket of N is B, free of 1/z.
  let B : ℝ → ℝ := fun z => 6 * (1 - z) ^ 3 * (3 - 3 * z + z ^ 2) * (a + b0 * z + b1 * z ^ 2)
    + (3 - 3 * z + z ^ 2) ^ 2 * (-(z * (a + b0 * z + b1 * z ^ 2)) + (1 - z) * (-a + b1 * z ^ 2)
      + (a + b0 * z + b1 * z ^ 2) ^ 2)
  let X : Polynomial ℝ := Polynomial.X
  let C : ℝ → Polynomial ℝ := Polynomial.C
  let xP : Polynomial ℝ := C 2 * (1 - X) ^ 3
  let gP : Polynomial ℝ := C 3 - C 3 * X + X ^ 2
  let QP : Polynomial ℝ := C a + C b0 * X + C b1 * X ^ 2
  let BP : Polynomial ℝ :=
    C 6 * (1 - X) ^ 3 * gP * QP + gP ^ 2 * (-(X * QP) + (1 - X) * (C (-a) + C b1 * X ^ 2) + QP ^ 2)
  let UP : Polynomial ℝ :=
    C (-400000 * dEll ℓ * (1 + mEll ℓ * dEll ℓ) ^ 3) * xP ^ 4
      - C (1600 * (1 + mEll ℓ * dEll ℓ) ^ 2 * (50 * mEll ℓ * dEll ℓ - 16)) * xP ^ 3
      + C (7680 * mEll ℓ * (1 + mEll ℓ * dEll ℓ)) * xP ^ 2
      - C (16 * mEll ℓ * (5 * mEll ℓ * (96 - 4 * mEll ℓ) * dEll ℓ + 480)) * xP
      + C (64 * mEll ℓ ^ 3 + 384 * mEll ℓ ^ 2)
  let HP : Polynomial ℝ := C (mEll ℓ) + C (10 * (1 + mEll ℓ * dEll ℓ)) * xP
  let p : Polynomial ℝ := UP - C 64 * HP ^ 2 * BP
  have hev : ∀ z, p.eval z
      = Um (mEll ℓ) (dEll ℓ) (2 * (1 - z) ^ 3) - 64 * Hm (mEll ℓ) (dEll ℓ) (2 * (1 - z) ^ 3) ^ 2 * B z := by
    intro z
    simp only [p, UP, HP, BP, QP, gP, xP, C, X, B, Polynomial.eval_add, Polynomial.eval_sub, Polynomial.eval_mul,
      Polynomial.eval_pow, Polynomial.eval_C, Polynomial.eval_X, Polynomial.eval_one, Polynomial.eval_neg]
    unfold Um Hm
    ring
  refine ⟨p, fun z hz => ?_, ?_⟩
  · obtain ⟨hx, hf, hf'⟩ := D6_extremal z
    rw [hev z]
    unfold Nz U6 H6
    rw [hx, hf, hf']
    unfold Pres Pres'
    simp only [B]
    field_simp
    ring
  · rw [hev 0]
    have e2 : (2 : ℝ) * (1 - 0) ^ 3 = 2 := by norm_num
    rw [e2, U2_ell ℓ hℓ]
    simp only [B]
    ring

/-- G-RES as a limit: N(z) → 576H₋(2)²(ℓ(ℓ − 3)/9 − a(a + 1)) as z → 0 with z ≠ 0. -/
theorem g_res_tendsto (ℓ a b0 b1 : ℝ) (hℓ : ℓ + 4 ≠ 0) :
    Filter.Tendsto
      (fun z => Nz (U6 1 (mEll ℓ) (dEll ℓ)) (H6 1 (mEll ℓ) (dEll ℓ)) (F6 1) (F6' 1) (Pres a b0 b1) (Pres' a b1) z)
      (nhdsWithin 0 {0}ᶜ) (nhds (576 * Hm (mEll ℓ) (dEll ℓ) 2 ^ 2 * (ℓ * (ℓ - 3) / 9 - a * (a + 1)))) := by
  obtain ⟨p, hp, h0⟩ := g_res ℓ a b0 b1 hℓ
  rw [← h0]
  have hc : Continuous fun z => p.eval z := by
    simp only [Polynomial.eval_eq_sum_range]
    fun_prop
  refine ((hc.tendsto 0).mono_left nhdsWithin_le_nhds).congr' ?_
  filter_upwards [self_mem_nhdsWithin] with z hz
  exact (hp z hz).symm

/-! #### (b) D = 4, q = 0: the Darboux identities of the [another line of this project] job `chandrasekhar` (bh-modes [code of another line of this project],
`chandrasekhar`; [a record of another line of this project] §3)

n = 2 and δ = 0, in the job's variables r and M: f = 1 − 2M/r and x = 2M/r. With F = f/(r(mr + 6M)), β = 6M,
κ = m(m + 2), 𝒲 = βF + κ/(2β) and 𝒲_* = f·d𝒲/dr, at every r with r ≠ 0 and mr + 6M ≠ 0:
𝒲² + 𝒲_* − κ²/(4β²) is our V_S− (`darboux_KI`), and 𝒲² − 𝒲_* − κ²/(4β²) is Regge–Wheeler's f((m + 2)/r² − 6M/r³)
(`darboux_RW`). For r ≠ 0, H₋ = m + 3x vanishes exactly where mr + 6M = 0 (`H_zero_iff`), so at r₀ = −6M/m. The
Regge–Wheeler potential is analytic at r₀, and 𝒲² − 𝒲_* − κ²/(4β²) agrees with it near r₀, off r₀
(`RW_regular_at_r0`). -/

/-- f = 1 − 2M/r. -/
noncomputable def f4 (M r : ℝ) : ℝ := 1 - 2 * M / r

/-- Our V_S− at n = 2 and δ = 0: f U₋/(64r²H₋²), with U₋ = `UmN` 2 1 m 0 x 0 and H₋ = `HmN` 2 m 0 x at x = 2M/r. -/
noncomputable def VKI4 (m M r : ℝ) : ℝ :=
  f4 M r * UmN 2 1 m 0 (2 * M / r) 0 / (64 * r ^ 2 * HmN 2 m 0 (2 * M / r) ^ 2)

/-- Regge–Wheeler's potential f((m + 2)/r² − 6M/r³). -/
noncomputable def VRW4 (m M r : ℝ) : ℝ := f4 M r * ((m + 2) / r ^ 2 - 6 * M / r ^ 3)

/-- The superpotential 𝒲 = βF + κ/(2β), with F = f/(r(mr + 6M)), β = 6M and κ = m(m + 2). -/
noncomputable def W4 (m M r : ℝ) : ℝ := 6 * M * (f4 M r / (r * (m * r + 6 * M))) + m * (m + 2) / (2 * (6 * M))

/-- d𝒲/dr by the quotient rule, where r ≠ 0 and mr + 6M ≠ 0. -/
theorem W4_deriv (m M r : ℝ) (hr : r ≠ 0) (hH : m * r + 6 * M ≠ 0) :
    deriv (W4 m M) r
      = 6 * M * ((2 * M / r ^ 2 * (r * (m * r + 6 * M)) - f4 M r * (m * r + 6 * M + r * m))
          / (r * (m * r + 6 * M)) ^ 2) := by
  have hf : HasDerivAt (fun y => f4 M y) (2 * M / r ^ 2) r := by
    have h := ((hasDerivAt_inv hr).const_mul (2 * M)).const_sub 1
    have e : (fun y => f4 M y) = fun y => 1 - 2 * M * y⁻¹ := by
      funext y; unfold f4; rw [div_eq_mul_inv]
    rw [e]
    refine h.congr_deriv ?_
    field_simp
  have hD : HasDerivAt (fun y => y * (m * y + 6 * M)) (1 * (m * r + 6 * M) + r * (m * 1)) r :=
    (hasDerivAt_id' r).mul (((hasDerivAt_id' r).const_mul m).add_const (6 * M))
  have h : HasDerivAt (W4 m M)
      (6 * M * ((2 * M / r ^ 2 * (r * (m * r + 6 * M)) - f4 M r * (1 * (m * r + 6 * M) + r * (m * 1)))
        / (r * (m * r + 6 * M)) ^ 2)) r := by
    unfold W4
    exact ((hf.div hD (mul_ne_zero hr hH)).const_mul (6 * M)).add_const _
  rw [h.deriv]
  ring

/-- 𝒲² + 𝒲_* − κ²/(4β²) is our V_S− (n = 2, δ = 0), wherever r ≠ 0 and H₋ ≠ 0; M ≠ 0. -/
theorem darboux_KI (m M r : ℝ) (hM : M ≠ 0) (hr : r ≠ 0) (hH : m * r + 6 * M ≠ 0) :
    W4 m M r ^ 2 + f4 M r * deriv (W4 m M) r - (m * (m + 2)) ^ 2 / (4 * (6 * M) ^ 2) = VKI4 m M r := by
  have eH : HmN 2 m 0 (2 * M / r) = (m * r + 6 * M) / r := by unfold HmN; field_simp; ring
  rw [W4_deriv m M r hr hH]
  unfold VKI4
  rw [eH]
  unfold W4 f4 UmN
  set s := m * r + 6 * M with hs
  field_simp
  rw [hs]
  ring

/-- 𝒲² − 𝒲_* − κ²/(4β²) is Regge–Wheeler's potential, wherever r ≠ 0 and H₋ ≠ 0; M ≠ 0. -/
theorem darboux_RW (m M r : ℝ) (hM : M ≠ 0) (hr : r ≠ 0) (hH : m * r + 6 * M ≠ 0) :
    W4 m M r ^ 2 - f4 M r * deriv (W4 m M) r - (m * (m + 2)) ^ 2 / (4 * (6 * M) ^ 2) = VRW4 m M r := by
  rw [W4_deriv m M r hr hH]
  unfold VRW4 W4 f4
  set s := m * r + 6 * M with hs
  field_simp
  rw [hs]
  ring

/-- For r ≠ 0, H₋ = m + 3x (n = 2, δ = 0) at x = 2M/r vanishes exactly when mr + 6M = 0. -/
theorem H_zero_iff (m M r : ℝ) (hr : r ≠ 0) : HmN 2 m 0 (2 * M / r) = 0 ↔ m * r + 6 * M = 0 := by
  have e : HmN 2 m 0 (2 * M / r) = (m * r + 6 * M) / r := by unfold HmN; field_simp; ring
  rw [e, div_eq_zero_iff, or_iff_left hr]

/-- r₀ = −6M/m is a zero of H₋; the Regge–Wheeler potential is analytic there; and 𝒲² − 𝒲_* − κ²/(4β²) agrees with
it near r₀, off r₀. -/
theorem RW_regular_at_r0 (m M : ℝ) (hm : m ≠ 0) (hM : M ≠ 0) :
    HmN 2 m 0 (2 * M / (-6 * M / m)) = 0 ∧ AnalyticAt ℝ (VRW4 m M) (-6 * M / m) ∧
      ∀ᶠ r in nhdsWithin (-6 * M / m) {-6 * M / m}ᶜ,
        W4 m M r ^ 2 - f4 M r * deriv (W4 m M) r - (m * (m + 2)) ^ 2 / (4 * (6 * M) ^ 2) = VRW4 m M r := by
  have hr0 : -6 * M / m ≠ 0 := div_ne_zero (by intro h; apply hM; linarith) hm
  refine ⟨(H_zero_iff m M _ hr0).2 (by field_simp; ring), ?_, ?_⟩
  · unfold VRW4 f4
    generalize -6 * M / m = r0 at hr0 ⊢
    fun_prop (disch := simp [hr0])
  · filter_upwards [self_mem_nhdsWithin, nhdsWithin_le_nhds ((isOpen_ne (x := (0 : ℝ))).mem_nhds hr0)]
      with r hr hr'
    have hH : m * r + 6 * M ≠ 0 := by
      intro h
      apply hr
      show r = -6 * M / m
      field_simp
      linarith
    exact darboux_RW m M r hM hr' hH

end BHModes.P3
