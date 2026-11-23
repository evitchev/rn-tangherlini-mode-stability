/-
  bh-modes BHM-126, item (d) of the lead's message 8, as asked in message 9 (2026-10-26): the tortoise map at q = 1,
  the chain-rule step, Lemma 1 with S = −(log u₀)_{r*}, and A_{ℓ,1} ≥ 0. Session-L, 2026-10-26.

  This file has three parts:
  - lines 36-174 are lean_z_2026-10-26's BHModesZ.lean lines 25-163, byte for byte: the definitions and the
    theorems (a)-(c) of BHM-134;
  - lines 180-239 are lean_p3_sdeformation_v5's BHModesP3.lean lines 86-145, byte for byte: Lemma 1
    (`sdef_identity`) and its Corollary (`form_nonneg_of_sdef`);
  - from line 241 on, the new section (d).
  Units r_H = 1 at q = 1: S5's x = 2M/r^(n−1) with M = 1, so x = 2Y, Y = ρ^(−(n−1)) and f = (1 − Y)². n is an
  integer ≥ 2 in section (d).
-/
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Inv
import Mathlib.Analysis.Calculus.Deriv.Inverse
import Mathlib.Analysis.Calculus.Deriv.Support
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Analysis.Complex.Basic
import Mathlib.Analysis.SpecialFunctions.ExpDeriv
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.MeasureTheory.Function.LocallyIntegrable
import Mathlib.MeasureTheory.Integral.IntegralEqImproper
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.Topology.Order.IntermediateValue
import Mathlib.Topology.Order.MonotoneContinuity
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.FunProp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

set_option autoImplicit false
set_option relaxedAutoImplicit false

noncomputable section

namespace BHModes.Z

/-! ### The c_n layer's definitions (lean_cn_2026-10-23, lines 24-43, byte for byte) -/

/-- S5 (5.62b) at general n. -/
def Hm (n m δ x : ℝ) : ℝ := m + n * (n + 1) / 2 * (1 + m * δ) * x

/-- S5 (5.63b) at general n, with the horizon curvature K and the cosmological term y. -/
def Um (n K m δ x y : ℝ) : ℝ :=
  (-4 * n ^ 3 * (n + 2) * (n + 1) ^ 2 * (1 + m * δ) ^ 2 * x ^ 2 + 48 * n ^ 2 * (n + 1) * (n - 2) * m * (1 + m * δ) * x
      - 16 * (n - 2) * (n - 4) * m ^ 2) * y
    - n ^ 3 * (3 * n - 2) * (n + 1) ^ 4 * δ * (1 + m * δ) ^ 3 * x ^ 4
    - 4 * n ^ 2 * (n + 1) ^ 2 * (1 + m * δ) ^ 2 * ((n + 1) * (3 * n - 2) * m * δ - n ^ 2) * x ^ 3
    + 4 * (n + 1) * (1 + m * δ) * (m * (n - 2) * (n - 4) * (n + 1) * (m + n ^ 2 * K) * δ
        + 4 * n * (2 * n ^ 2 - 3 * n + 4) * m + n ^ 2 * (n - 2) * (n - 4) * (n + 1) * K) * x ^ 2
    - 16 * m * ((n + 1) * m * (-4 * m + 3 * n ^ 2 * (n - 2) * K) * δ + 3 * n * (n - 4) * m
        + 3 * n ^ 2 * (n + 1) * (n - 2) * K) * x
    + 64 * m ^ 3 + 16 * n * (n + 2) * m ^ 2 * K

/-- m = (ℓ − 1)(ℓ + n). -/
def mm (n ℓ : ℝ) : ℝ := (ℓ - 1) * (ℓ + n)

/-- δ₁, the q = 1 value of δ. -/
def δ1 (n ℓ : ℝ) : ℝ := 1 / ((n + 1) * (ℓ + n))

/-! ### The zero mode -/

/-- ν = ℓ + n/2 − 1. -/
def nu (n ℓ : ℝ) : ℝ := ℓ + n / 2 - 1

/-- g = −ν − ℓY/(1 − Y) + n(n − 1)Y/((ℓ − 1) + nY): ρ ∂_ρ log u₀ for u₀ = ρ^(−ν)(1 − Y)^(−ℓ/(n−1))/((ℓ − 1) + nY),
    with Y = ρ^(−(n−1)). -/
def g (n ℓ Y : ℝ) : ℝ := -nu n ℓ - ℓ * Y / (1 - Y) + n * (n - 1) * Y / ((ℓ - 1) + n * Y)

/-- W = U₋/(64 H₋²) at x = 2Y, m = (ℓ − 1)(ℓ + n), δ = δ₁, K = 1 and y = 0. -/
def W (n ℓ Y : ℝ) : ℝ := Um n 1 (mm n ℓ) (δ1 n ℓ) (2 * Y) 0 / (64 * Hm n (mm n ℓ) (δ1 n ℓ) (2 * Y) ^ 2)

/-- The partner's quadratic Ũ (RESULT.md, n symbolic). -/
def Ut (n ℓ Y : ℝ) : ℝ :=
  (5 * n ^ 2 / 4 - n / 2) * Y ^ 2 + (-3 * n ^ 2 / 2 + 2 * n + 2 * ℓ - 2) * Y
    + (n ^ 2 / 4 + n * ℓ - 3 * n / 2 + ℓ ^ 2 - 3 * ℓ + 2)

/-! ### (b) The gates -/

/-- Gate q1: δ₁ is the extremal point of S5 (5.58), (n + 1)²δ(1 + mδ) = q² at q = 1. -/
theorem gate_q1 (n ℓ : ℝ) (h1 : n + 1 ≠ 0) (h2 : ℓ + n ≠ 0) :
    (n + 1) ^ 2 * δ1 n ℓ * (1 + mm n ℓ * δ1 n ℓ) = 1 := by
  unfold mm δ1; field_simp; ring

/-- Gate H: H₋(2Y) = (ℓ + n)((ℓ − 1) + nY) at q = 1. -/
theorem gate_H (n ℓ Y : ℝ) (h1 : n + 1 ≠ 0) (h2 : ℓ + n ≠ 0) :
    Hm n (mm n ℓ) (δ1 n ℓ) (2 * Y) = (ℓ + n) * ((ℓ - 1) + n * Y) := by
  unfold Hm mm δ1; field_simp; ring

/-! ### ∂_Y g -/

/-- ∂_Y g = −ℓ/(1 − Y)² + n(n − 1)(ℓ − 1)/((ℓ − 1) + nY)². -/
theorem g_hasDerivAt (n ℓ Y : ℝ) (hY : 1 - Y ≠ 0) (hP : (ℓ - 1) + n * Y ≠ 0) :
    HasDerivAt (g n ℓ) (-ℓ / (1 - Y) ^ 2 + n * (n - 1) * (ℓ - 1) / ((ℓ - 1) + n * Y) ^ 2) Y := by
  have hA : HasDerivAt (fun y : ℝ => ℓ * y / (1 - y)) ((ℓ * 1 * (1 - Y) - ℓ * Y * (0 - 1)) / (1 - Y) ^ 2) Y :=
    ((hasDerivAt_id' Y).const_mul ℓ).div ((hasDerivAt_const Y (1 : ℝ)).sub (hasDerivAt_id' Y)) hY
  have hB : HasDerivAt (fun y : ℝ => n * (n - 1) * y / ((ℓ - 1) + n * y))
      ((n * (n - 1) * 1 * ((ℓ - 1) + n * Y) - n * (n - 1) * Y * (0 + n * 1)) / ((ℓ - 1) + n * Y) ^ 2) Y :=
    ((hasDerivAt_id' Y).const_mul (n * (n - 1))).div
      ((hasDerivAt_const Y (ℓ - 1)).add ((hasDerivAt_id' Y).const_mul n)) hP
  have hC := ((hasDerivAt_const Y (-nu n ℓ)).sub hA).add hB
  have hg : g n ℓ = fun y : ℝ => -nu n ℓ - ℓ * y / (1 - y) + n * (n - 1) * y / ((ℓ - 1) + n * y) := by
    funext y; rfl
  rw [hg]
  convert hC using 1
  field_simp
  ring

theorem deriv_g (n ℓ Y : ℝ) (hY : 1 - Y ≠ 0) (hP : (ℓ - 1) + n * Y ≠ 0) :
    deriv (g n ℓ) Y = -ℓ / (1 - Y) ^ 2 + n * (n - 1) * (ℓ - 1) / ((ℓ - 1) + n * Y) ^ 2 :=
  (g_hasDerivAt n ℓ Y hY hP).deriv

/-! ### (a) Z-id -/

/-- (a) Z-id: 2(n − 1)Y(1 − Y)g + (1 − Y)²(g² − g − (n − 1)Y ∂_Y g) = U₋/(64H₋²) at x = 2Y. -/
theorem z_id (n ℓ Y : ℝ) (h1 : n + 1 ≠ 0) (h2 : ℓ + n ≠ 0) (hY : 1 - Y ≠ 0) (hP : (ℓ - 1) + n * Y ≠ 0) :
    2 * (n - 1) * Y * (1 - Y) * g n ℓ Y
      + (1 - Y) ^ 2 * (g n ℓ Y ^ 2 - g n ℓ Y - (n - 1) * Y * deriv (g n ℓ) Y) = W n ℓ Y := by
  rw [deriv_g n ℓ Y hY hP, W, gate_H n ℓ Y h1 h2]
  unfold g nu Um mm δ1
  set P := (ℓ - 1) + n * Y with hPdef
  set Q := 1 - Y with hQdef
  field_simp
  rw [hPdef, hQdef]
  ring

/-! ### (c) The partner -/

/-- (c) Ũ := (1 − Y)²(g² + g + (n − 1)Y ∂_Y g) − 2(n − 1)Y(1 − Y)g is the quadratic `Ut`. -/
theorem partner (n ℓ Y : ℝ) (hY : 1 - Y ≠ 0) (hP : (ℓ - 1) + n * Y ≠ 0) :
    (1 - Y) ^ 2 * (g n ℓ Y ^ 2 + g n ℓ Y + (n - 1) * Y * deriv (g n ℓ) Y) - 2 * (n - 1) * Y * (1 - Y) * g n ℓ Y
      = Ut n ℓ Y := by
  rw [deriv_g n ℓ Y hY hP]
  unfold g nu Ut
  set P := (ℓ - 1) + n * Y with hPdef
  set Q := 1 - Y with hQdef
  field_simp
  rw [hPdef, hQdef]
  ring

/-- At n = 4, Ũ = 18Y² + (2ℓ − 18)Y + ℓ² + ℓ (RESULT.md). -/
theorem partner_n4 (ℓ Y : ℝ) : Ut 4 ℓ Y = 18 * Y ^ 2 + (2 * ℓ - 18) * Y + ℓ ^ 2 + ℓ := by
  unfold Ut; ring

/-- P-asym: Ũ(0) = ν(ν − 1) and Ũ(1) = ℓ(ℓ + n − 1). -/
theorem partner_ends (n ℓ : ℝ) : Ut n ℓ 0 = nu n ℓ * (nu n ℓ - 1) ∧ Ut n ℓ 1 = ℓ * (ℓ + n - 1) := by
  unfold Ut nu; constructor <;> ring

/-- P-reg: the partner has no pole at the zero Y₀ = (1 − ℓ)/n of H₋. For n ≠ 0 and every Y₀ ≠ 1, that zero included,
    the expression of (c) tends to Ũ(Y₀) as Y → Y₀ with Y ≠ Y₀. -/
theorem partner_no_pole (n ℓ Y₀ : ℝ) (hn : n ≠ 0) (hY : 1 - Y₀ ≠ 0) :
    Filter.Tendsto (fun Y => (1 - Y) ^ 2 * (g n ℓ Y ^ 2 + g n ℓ Y + (n - 1) * Y * deriv (g n ℓ) Y)
        - 2 * (n - 1) * Y * (1 - Y) * g n ℓ Y) (nhdsWithin Y₀ {Y₀}ᶜ) (nhds (Ut n ℓ Y₀)) := by
  have hc : Continuous (fun Y : ℝ => Ut n ℓ Y) := by unfold Ut; fun_prop
  have hc1 : Continuous (fun Y : ℝ => 1 - Y) := by fun_prop
  have h1 : ∀ᶠ Y in nhdsWithin Y₀ {Y₀}ᶜ, 1 - Y ≠ 0 :=
    Filter.Eventually.filter_mono nhdsWithin_le_nhds (hc1.continuousAt.eventually_ne hY)
  have h2 : ∀ᶠ Y in nhdsWithin Y₀ {Y₀}ᶜ, (ℓ - 1) + n * Y ≠ 0 := by
    by_cases h0 : (ℓ - 1) + n * Y₀ = 0
    · filter_upwards [self_mem_nhdsWithin] with Y hYne hz
      apply hYne
      have h3 : n * (Y - Y₀) = 0 := by linear_combination hz - h0
      have h4 : Y - Y₀ = 0 := (mul_eq_zero.mp h3).resolve_left hn
      exact Set.mem_singleton_iff.mpr (by linarith)
    · have hc2 : Continuous (fun Y : ℝ => (ℓ - 1) + n * Y) := by fun_prop
      exact Filter.Eventually.filter_mono nhdsWithin_le_nhds (hc2.continuousAt.eventually_ne h0)
  refine (hc.continuousAt.tendsto.mono_left nhdsWithin_le_nhds).congr' ?_
  filter_upwards [h1, h2] with Y hY1 hY2
  exact (partner n ℓ Y hY1 hY2).symm

/-! ### Lemma 1 and its Corollary (lean_p3_sdeformation_v5, BHModesP3.lean lines 86-145, byte for byte) -/

open MeasureTheory

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

/-! ### (d) The tortoise map at q = 1, the zero mode in r*, and A_{ℓ,1} ≥ 0

The bh-modes lead's message 9 (2026-10-26), item 3. Units r_H = 1 at q = 1: S5's x = 2M/r^(n−1) with M = 1, so
x = 2Y with Y = ρ^(−(n−1)), and f = 1 − x + x²/4 = (1 − Y)². Here n is a natural number, n ≥ 2. -/

/-- Y = ρ^(−(n−1)), written (1/ρ)^(n−1). -/
def Yr (n : ℕ) (ρ : ℝ) : ℝ := ρ⁻¹ ^ (n - 1)

/-- f at q = 1, in units r_H = 1. -/
def fr (n : ℕ) (ρ : ℝ) : ℝ := (1 - Yr n ρ) ^ 2

/-- f is S5's 1 − x + q²x²/4 at q = 1 and x = 2Y. -/
theorem fr_S5 (n : ℕ) (ρ : ℝ) : fr n ρ = 1 - 2 * Yr n ρ + 1 ^ 2 * (2 * Yr n ρ) ^ 2 / 4 := by
  unfold fr; ring

theorem Yr_mem (n : ℕ) (hn : 2 ≤ n) (ρ : ℝ) (hρ : 1 < ρ) : 0 < Yr n ρ ∧ Yr n ρ < 1 := by
  have h0 : 0 < ρ⁻¹ := inv_pos.mpr (by linarith)
  have h1 : ρ⁻¹ < 1 := inv_lt_one_of_one_lt₀ hρ
  exact ⟨pow_pos h0 _, pow_lt_one₀ h0.le h1 (by omega)⟩

theorem fr_pos (n : ℕ) (hn : 2 ≤ n) (ρ : ℝ) (hρ : 1 < ρ) : 0 < fr n ρ := by
  have h := Yr_mem n hn ρ hρ
  exact pow_pos (by linarith [h.2]) 2

theorem fr_le_one (n : ℕ) (hn : 2 ≤ n) (ρ : ℝ) (hρ : 1 < ρ) : fr n ρ ≤ 1 := by
  have h := Yr_mem n hn ρ hρ
  unfold fr; nlinarith [h.1, h.2]

/-- 1 − Y ≤ (n − 1)(ρ − 1) for ρ > 1, by Bernoulli's inequality. -/
theorem one_sub_Yr_le (n : ℕ) (hn : 2 ≤ n) (ρ : ℝ) (hρ : 1 < ρ) : 1 - Yr n ρ ≤ ((n : ℝ) - 1) * (ρ - 1) := by
  have hρ0 : ρ ≠ 0 := by linarith
  have hi : 0 < ρ⁻¹ := inv_pos.mpr (by linarith)
  have hb := one_add_mul_le_pow (a := ρ⁻¹ - 1) (by linarith) (n - 1)
  rw [show (1 : ℝ) + (ρ⁻¹ - 1) = ρ⁻¹ by ring] at hb
  have hc : ((n - 1 : ℕ) : ℝ) = (n : ℝ) - 1 := by rw [Nat.cast_sub (by omega)]; simp
  rw [hc] at hb
  have h2 : 1 - ρ⁻¹ ≤ ρ - 1 := by
    have e : 1 - ρ⁻¹ = (ρ - 1) / ρ := by field_simp
    rw [e]; exact div_le_self (by linarith) hρ.le
  have hn1 : (0 : ℝ) ≤ (n : ℝ) - 1 := by
    have : (2 : ℝ) ≤ n := by exact_mod_cast hn
    linarith
  unfold Yr
  nlinarith [mul_le_mul_of_nonneg_left h2 hn1]

/-- f ≤ (n − 1)²(ρ − 1)² for ρ > 1: near the extremal horizon, f vanishes at least to second order. -/
theorem fr_le_sq (n : ℕ) (hn : 2 ≤ n) (ρ : ℝ) (hρ : 1 < ρ) : fr n ρ ≤ (((n : ℝ) - 1) * (ρ - 1)) ^ 2 := by
  have h0 : 0 ≤ 1 - Yr n ρ := by linarith [(Yr_mem n hn ρ hρ).2]
  exact pow_le_pow_left₀ h0 (one_sub_Yr_le n hn ρ hρ) 2

/-- dY/dρ = −(n − 1)Y/ρ. -/
theorem Yr_hasDerivAt (n : ℕ) (hn : 2 ≤ n) (ρ : ℝ) (hρ : ρ ≠ 0) :
    HasDerivAt (Yr n) (-((n : ℝ) - 1) * Yr n ρ / ρ) ρ := by
  obtain ⟨k, rfl⟩ := Nat.exists_eq_add_of_le hn
  have h := (hasDerivAt_inv hρ).pow (k + 1)
  have e : Yr (2 + k) = (fun y : ℝ => y⁻¹) ^ (k + 1) := by
    funext y; simp only [Yr, Pi.pow_apply]; congr 1; omega
  rw [e]
  convert h using 1
  simp only [Pi.pow_apply, Nat.add_sub_cancel]
  push_cast
  ring

/-- df/dρ = 2(1 − Y)(n − 1)Y/ρ. -/
theorem fr_hasDerivAt (n : ℕ) (hn : 2 ≤ n) (ρ : ℝ) (hρ : ρ ≠ 0) :
    HasDerivAt (fr n) (2 * (1 - Yr n ρ) * (((n : ℝ) - 1) * Yr n ρ / ρ)) ρ := by
  have h := ((hasDerivAt_const ρ (1 : ℝ)).sub (Yr_hasDerivAt n hn ρ hρ)).pow 2
  have e : fr n = (fun y => 1 - Yr n y) ^ 2 := by funext y; simp only [fr, Pi.pow_apply]
  rw [e]
  convert h using 1
  norm_num
  ring

/-! #### The tortoise map r*(ρ) = ∫₂^ρ ds/f(s) -/

/-- The tortoise coordinate at q = 1, r*(ρ) = ∫₂^ρ ds/f(s) (base point ρ = 2). -/
def tort (n : ℕ) (ρ : ℝ) : ℝ := ∫ s in (2 : ℝ)..ρ, 1 / fr n s

theorem invfr_continuousOn (n : ℕ) (hn : 2 ≤ n) : ContinuousOn (fun s => 1 / fr n s) (Set.Ioi 1) := by
  intro s hs
  have hs1 : 1 < s := hs
  have hs0 : s ≠ 0 := by linarith
  apply ContinuousAt.continuousWithinAt
  exact continuousAt_const.div (fr_hasDerivAt n hn s hs0).continuousAt (fr_pos n hn s hs1).ne'

/-- dr*/dρ = 1/f on (1, ∞). -/
theorem tort_hasDerivAt (n : ℕ) (hn : 2 ≤ n) (ρ : ℝ) (hρ : 1 < ρ) :
    HasDerivAt (tort n) (1 / fr n ρ) ρ := by
  have hc := invfr_continuousOn n hn
  have hsub : Set.uIcc (2 : ℝ) ρ ⊆ Set.Ioi 1 := by
    intro x hx
    rw [Set.mem_uIcc] at hx
    show 1 < x
    rcases hx with ⟨h, _⟩ | ⟨h, _⟩ <;> linarith
  exact intervalIntegral.integral_hasDerivAt_right ((hc.mono hsub).intervalIntegrable)
    (hc.stronglyMeasurableAtFilter isOpen_Ioi ρ hρ) (hc.continuousAt (isOpen_Ioi.mem_nhds hρ))

theorem tort_strictMonoOn (n : ℕ) (hn : 2 ≤ n) : StrictMonoOn (tort n) (Set.Ioi 1) := by
  apply strictMonoOn_of_deriv_pos (convex_Ioi 1)
  · intro x hx
    exact (tort_hasDerivAt n hn x hx).continuousAt.continuousWithinAt
  · intro x hx
    rw [interior_Ioi] at hx
    rw [(tort_hasDerivAt n hn x hx).deriv]
    exact one_div_pos.mpr (fr_pos n hn x hx)

/-- r*(ρ) ≥ ρ − 2 for ρ ≥ 2. -/
theorem tort_ge (n : ℕ) (hn : 2 ≤ n) (ρ : ℝ) (hρ : 2 ≤ ρ) : ρ - 2 ≤ tort n ρ := by
  have hd : ∀ x, 1 < x → HasDerivAt (fun y => tort n y - y) (1 / fr n x - 1) x :=
    fun x hx => (tort_hasDerivAt n hn x hx).sub (hasDerivAt_id' x)
  have hm : MonotoneOn (fun y => tort n y - y) (Set.Ici 2) := by
    apply monotoneOn_of_deriv_nonneg (convex_Ici 2)
    · intro x hx
      have hx1 : 1 < x := by have : (2 : ℝ) ≤ x := hx; linarith
      exact (hd x hx1).continuousAt.continuousWithinAt
    · intro x hx
      rw [interior_Ici] at hx
      have hx1 : 1 < x := by have : (2 : ℝ) < x := hx; linarith
      exact (hd x hx1).differentiableAt.differentiableWithinAt
    · intro x hx
      rw [interior_Ici] at hx
      have hx1 : 1 < x := by have : (2 : ℝ) < x := hx; linarith
      rw [(hd x hx1).deriv]
      have h1 := fr_pos n hn x hx1
      have h2 := fr_le_one n hn x hx1
      rw [sub_nonneg, le_div_iff₀ h1]
      linarith
  have h := hm (Set.mem_Ici.mpr le_rfl) (Set.mem_Ici.mpr hρ) hρ
  have h2 : tort n 2 = 0 := intervalIntegral.integral_same
  simp only [h2] at h
  linarith

/-- r*(ρ) ≤ (1 − 1/(ρ − 1))/(n − 1)² for 1 < ρ ≤ 2. -/
theorem tort_le (n : ℕ) (hn : 2 ≤ n) (ρ : ℝ) (hρ1 : 1 < ρ) (hρ2 : ρ ≤ 2) :
    tort n ρ ≤ (1 - 1 / (ρ - 1)) / ((n : ℝ) - 1) ^ 2 := by
  have hc0 : 0 < ((n : ℝ) - 1) ^ 2 := by
    have : (2 : ℝ) ≤ n := by exact_mod_cast hn
    have : (0 : ℝ) < (n : ℝ) - 1 := by linarith
    positivity
  set c := ((n : ℝ) - 1) ^ 2 with hc
  have hG : ∀ x, 1 < x → HasDerivAt (fun y => -(c * (y - 1))⁻¹) (1 / (c * (x - 1) ^ 2)) x := by
    intro x hx
    have hne : c * (x - 1) ≠ 0 := mul_ne_zero hc0.ne' (by linarith)
    have h := (((hasDerivAt_id' x).sub_const 1).const_mul c).inv hne
    convert h.neg using 1
    field_simp
  have hd : ∀ x, 1 < x → HasDerivAt (fun y => tort n y - -(c * (y - 1))⁻¹) (1 / fr n x - 1 / (c * (x - 1) ^ 2)) x :=
    fun x hx => (tort_hasDerivAt n hn x hx).sub (hG x hx)
  have hm : MonotoneOn (fun y => tort n y - -(c * (y - 1))⁻¹) (Set.Ioc 1 2) := by
    apply monotoneOn_of_deriv_nonneg (convex_Ioc 1 2)
    · intro x hx
      exact (hd x hx.1).continuousAt.continuousWithinAt
    · intro x hx
      rw [interior_Ioc] at hx
      exact (hd x hx.1).differentiableAt.differentiableWithinAt
    · intro x hx
      rw [interior_Ioc] at hx
      rw [(hd x hx.1).deriv]
      have h1 := fr_pos n hn x hx.1
      have h2 := fr_le_sq n hn x hx.1
      have h3 : 0 < c * (x - 1) ^ 2 := mul_pos hc0 (pow_pos (by linarith [hx.1]) 2)
      rw [sub_nonneg, div_le_div_iff₀ h3 h1]
      rw [hc]; nlinarith [h2]
  have h := hm ⟨hρ1, hρ2⟩ ⟨by norm_num, le_rfl⟩ hρ2
  have h2 : tort n 2 = 0 := intervalIntegral.integral_same
  simp only [h2] at h
  have e1 : (c * ((2 : ℝ) - 1))⁻¹ = 1 / c := by norm_num
  rw [e1] at h
  have e2 : (1 - 1 / (ρ - 1)) / c = 1 / c - (c * (ρ - 1))⁻¹ := by
    field_simp
  rw [e2]
  linarith

theorem tort_surjOn (n : ℕ) (hn : 2 ≤ n) : Set.SurjOn (tort n) (Set.Ioi 1) Set.univ := by
  intro y _
  have hc0 : 0 < ((n : ℝ) - 1) ^ 2 := by
    have : (2 : ℝ) ≤ n := by exact_mod_cast hn
    have : (0 : ℝ) < (n : ℝ) - 1 := by linarith
    positivity
  set c := ((n : ℝ) - 1) ^ 2 with hc
  -- the lower point ρ₁ = 1 + 1/(c K), K = |y| + 1/c + 1
  set K := |y| + 1 / c + 1 with hK
  have hK1 : 1 ≤ c * K := by
    have : 0 ≤ c * |y| := mul_nonneg hc0.le (abs_nonneg y)
    have e : c * K = c * |y| + 1 + c := by rw [hK]; field_simp
    rw [e]; linarith
  have hKpos : 0 < c * K := by linarith
  set ρ₁ := 1 + 1 / (c * K) with hρ₁
  have hρ₁1 : 1 < ρ₁ := by rw [hρ₁]; have := one_div_pos.mpr hKpos; linarith
  have hρ₁2 : ρ₁ ≤ 2 := by
    rw [hρ₁]; have : 1 / (c * K) ≤ 1 := by rw [div_le_one hKpos]; exact hK1
    linarith
  have hlow : tort n ρ₁ < y := by
    have h := tort_le n hn ρ₁ hρ₁1 hρ₁2
    have e : (1 - 1 / (ρ₁ - 1)) / c = 1 / c - K := by
      rw [hρ₁, add_sub_cancel_left, one_div_one_div]
      field_simp
    rw [e] at h
    have : y ≥ -|y| := neg_abs_le y
    have : 0 < 1 / c := one_div_pos.mpr hc0
    rw [hK] at h
    linarith
  -- the upper point ρ₂ = |y| + 3
  set ρ₂ := |y| + 3 with hρ₂
  have hρ₂2 : 2 ≤ ρ₂ := by rw [hρ₂]; have := abs_nonneg y; linarith
  have hup : y < tort n ρ₂ := by
    have h := tort_ge n hn ρ₂ hρ₂2
    have : y ≤ |y| := le_abs_self y
    rw [hρ₂] at h
    linarith
  have h12 : ρ₁ ≤ ρ₂ := by linarith
  have hcont : ContinuousOn (tort n) (Set.Icc ρ₁ ρ₂) := by
    intro x hx
    exact (tort_hasDerivAt n hn x (by linarith [hx.1])).continuousAt.continuousWithinAt
  obtain ⟨x, hx, hxy⟩ := intermediate_value_Icc h12 hcont ⟨hlow.le, hup.le⟩
  exact ⟨x, show 1 < x by linarith [hx.1], hxy⟩

theorem tort_bijOn (n : ℕ) (hn : 2 ≤ n) : Set.BijOn (tort n) (Set.Ioi 1) Set.univ :=
  ⟨Set.mapsTo_univ _ _, (tort_strictMonoOn n hn).injOn, tort_surjOn n hn⟩

/-- (d), first part: at q = 1 and every integer n ≥ 2, the tortoise map is an increasing bijection (1, ∞) → ℝ,
    with dr*/dρ = 1/f. -/
theorem tortoise_q1 (n : ℕ) (hn : 2 ≤ n) :
    StrictMonoOn (tort n) (Set.Ioi 1) ∧ Set.BijOn (tort n) (Set.Ioi 1) Set.univ ∧
      ∀ ρ, 1 < ρ → HasDerivAt (tort n) (1 / fr n ρ) ρ :=
  ⟨tort_strictMonoOn n hn, tort_bijOn n hn, tort_hasDerivAt n hn⟩

/-! #### The inverse map R : ℝ → (1, ∞), with dR/dr* = f(R) -/

/-- R = (r*)⁻¹ on (1, ∞). -/
def Rt (n : ℕ) : ℝ → ℝ := Function.invFunOn (tort n) (Set.Ioi 1)

theorem Rt_spec (n : ℕ) (hn : 2 ≤ n) (t : ℝ) : 1 < Rt n t ∧ tort n (Rt n t) = t := by
  have h : ∃ a ∈ Set.Ioi (1 : ℝ), tort n a = t := tort_surjOn n hn (Set.mem_univ t)
  exact ⟨Function.invFunOn_mem h, Function.invFunOn_eq h⟩

theorem Rt_tort (n : ℕ) (hn : 2 ≤ n) (ρ : ℝ) (hρ : 1 < ρ) : Rt n (tort n ρ) = ρ :=
  (tort_strictMonoOn n hn).injOn (Rt_spec n hn _).1 hρ (Rt_spec n hn _).2

theorem Rt_strictMono (n : ℕ) (hn : 2 ≤ n) : StrictMono (Rt n) := by
  intro a b hab
  have ha := Rt_spec n hn a
  have hb := Rt_spec n hn b
  by_contra h
  push_neg at h
  have := (tort_strictMonoOn n hn).monotoneOn hb.1 ha.1 h
  rw [ha.2, hb.2] at this
  linarith

theorem Rt_continuous (n : ℕ) (hn : 2 ≤ n) : Continuous (Rt n) := by
  rw [continuous_iff_continuousAt]
  intro t
  apply continuousAt_of_monotoneOn_of_image_mem_nhds ((Rt_strictMono n hn).monotone.monotoneOn Set.univ) Filter.univ_mem
  have e : Rt n '' Set.univ = Set.Ioi 1 := by
    ext ρ
    constructor
    · rintro ⟨s, _, rfl⟩
      exact (Rt_spec n hn s).1
    · intro hρ
      exact ⟨tort n ρ, Set.mem_univ _, Rt_tort n hn ρ hρ⟩
  rw [e]
  exact isOpen_Ioi.mem_nhds (Rt_spec n hn t).1

/-- dR/dr* = f(R). -/
theorem Rt_hasDerivAt (n : ℕ) (hn : 2 ≤ n) (t : ℝ) : HasDerivAt (Rt n) (fr n (Rt n t)) t := by
  have hR := Rt_spec n hn t
  have h := HasDerivAt.of_local_left_inverse (Rt_continuous n hn).continuousAt
    (tort_hasDerivAt n hn (Rt n t) hR.1) (one_div_pos.mpr (fr_pos n hn (Rt n t) hR.1)).ne'
    (Filter.Eventually.of_forall fun y => (Rt_spec n hn y).2)
  simpa using h

/-! #### The chain-rule step: w = f g/ρ and V = w² + w′ -/

/-- ∂_Y g, as stated in `g_hasDerivAt`. -/
def dg (n ℓ Y : ℝ) : ℝ := -ℓ / (1 - Y) ^ 2 + n * (n - 1) * (ℓ - 1) / ((ℓ - 1) + n * Y) ^ 2

/-- w = f g/ρ as a function of ρ: (log u₀)_{r*} at r* = r*(ρ). -/
def wr (n : ℕ) (ℓ ρ : ℝ) : ℝ := fr n ρ * g n ℓ (Yr n ρ) / ρ

/-- dw/dρ. -/
def dwr (n : ℕ) (ℓ ρ : ℝ) : ℝ :=
  ((2 * (1 - Yr n ρ) * (((n : ℝ) - 1) * Yr n ρ / ρ) * g n ℓ (Yr n ρ)
      + fr n ρ * (dg n ℓ (Yr n ρ) * (-((n : ℝ) - 1) * Yr n ρ / ρ))) * ρ
    - fr n ρ * g n ℓ (Yr n ρ) * 1) / ρ ^ 2

/-- V_S− at q = 1 as a function of ρ: f W/ρ² = f U₋/(64ρ²H₋²) at x = 2Y. -/
def Vr (n : ℕ) (ℓ ρ : ℝ) : ℝ := fr n ρ * W n ℓ (Yr n ρ) / ρ ^ 2

/-- The partner potential Ṽ = f Ũ/ρ² as a function of ρ. -/
def Vtr (n : ℕ) (ℓ ρ : ℝ) : ℝ := fr n ρ * Ut n ℓ (Yr n ρ) / ρ ^ 2

/-- Vr is S5's V_S− = f U₋/(64 r² H₋²) at q = 1, K = 1, y = 0, x = 2Y and r = ρ. -/
theorem Vr_S5 (n : ℕ) (ℓ ρ : ℝ) :
    Vr n ℓ ρ = (1 - 2 * Yr n ρ + 1 ^ 2 * (2 * Yr n ρ) ^ 2 / 4) * Um n 1 (mm n ℓ) (δ1 n ℓ) (2 * Yr n ρ) 0
      / (64 * ρ ^ 2 * Hm n (mm n ℓ) (δ1 n ℓ) (2 * Yr n ρ) ^ 2) := by
  unfold Vr W fr; ring

theorem wr_hasDerivAt (n : ℕ) (hn : 2 ≤ n) (ℓ : ℝ) (hℓ : 1 ≤ ℓ) (ρ : ℝ) (hρ : 1 < ρ) :
    HasDerivAt (wr n ℓ) (dwr n ℓ ρ) ρ := by
  have hρ0 : ρ ≠ 0 := by linarith
  have hY := Yr_mem n hn ρ hρ
  have h1 : 1 - Yr n ρ ≠ 0 := by linarith [hY.2]
  have hP : (ℓ - 1) + (n : ℝ) * Yr n ρ ≠ 0 := by
    have : (0 : ℝ) < (n : ℝ) * Yr n ρ := mul_pos (by exact_mod_cast (by omega : 0 < n)) hY.1
    linarith
  have hg := (g_hasDerivAt (n : ℝ) ℓ (Yr n ρ) h1 hP).comp ρ (Yr_hasDerivAt n hn ρ hρ0)
  have h := ((fr_hasDerivAt n hn ρ hρ0).mul hg).div (hasDerivAt_id' ρ) hρ0
  convert h using 1

-- The chain-rule step (+): with w′ = dw/dr* = f dw/dρ, ρ²(w² + w′)/f is (a)'s left side at Y = ρ^(−(n−1)).
-- (A line comment, not a doc comment: a heartbeat timeout is then placed on this theorem's own line.)
theorem riccati_plus (n : ℕ) (hn : 2 ≤ n) (ℓ : ℝ) (hℓ : 1 ≤ ℓ) (ρ : ℝ) (hρ : 1 < ρ) :
    ρ ^ 2 * (wr n ℓ ρ ^ 2 + fr n ρ * deriv (wr n ℓ) ρ) / fr n ρ
      = 2 * ((n : ℝ) - 1) * Yr n ρ * (1 - Yr n ρ) * g n ℓ (Yr n ρ)
        + (1 - Yr n ρ) ^ 2 * (g n ℓ (Yr n ρ) ^ 2 - g n ℓ (Yr n ρ)
          - ((n : ℝ) - 1) * Yr n ρ * deriv (g n ℓ) (Yr n ρ)) := by
  have hρ0 : ρ ≠ 0 := by linarith
  have hY := Yr_mem n hn ρ hρ
  have h1 : 1 - Yr n ρ ≠ 0 := by linarith [hY.2]
  have hP : (ℓ - 1) + (n : ℝ) * Yr n ρ ≠ 0 := by
    have : (0 : ℝ) < (n : ℝ) * Yr n ρ := mul_pos (by exact_mod_cast (by omega : 0 < n)) hY.1
    linarith
  rw [(wr_hasDerivAt n hn ℓ hℓ ρ hρ).deriv, deriv_g (n : ℝ) ℓ (Yr n ρ) h1 hP]
  unfold wr dwr dg fr
  set Y := Yr n ρ with hYdef
  set G := g (n : ℝ) ℓ Y with hGdef
  set Q := 1 - Y with hQdef
  set P := (ℓ - 1) + (n : ℝ) * Y with hPdef
  field_simp
  rw [hQdef, hPdef]
  ring

-- The chain-rule step (−): ρ²(w² − w′)/f is (c)'s left side at Y = ρ^(−(n−1)).
theorem riccati_minus (n : ℕ) (hn : 2 ≤ n) (ℓ : ℝ) (hℓ : 1 ≤ ℓ) (ρ : ℝ) (hρ : 1 < ρ) :
    ρ ^ 2 * (wr n ℓ ρ ^ 2 - fr n ρ * deriv (wr n ℓ) ρ) / fr n ρ
      = (1 - Yr n ρ) ^ 2 * (g n ℓ (Yr n ρ) ^ 2 + g n ℓ (Yr n ρ) + ((n : ℝ) - 1) * Yr n ρ * deriv (g n ℓ) (Yr n ρ))
        - 2 * ((n : ℝ) - 1) * Yr n ρ * (1 - Yr n ρ) * g n ℓ (Yr n ρ) := by
  have hρ0 : ρ ≠ 0 := by linarith
  have hY := Yr_mem n hn ρ hρ
  have h1 : 1 - Yr n ρ ≠ 0 := by linarith [hY.2]
  have hP : (ℓ - 1) + (n : ℝ) * Yr n ρ ≠ 0 := by
    have : (0 : ℝ) < (n : ℝ) * Yr n ρ := mul_pos (by exact_mod_cast (by omega : 0 < n)) hY.1
    linarith
  rw [(wr_hasDerivAt n hn ℓ hℓ ρ hρ).deriv, deriv_g (n : ℝ) ℓ (Yr n ρ) h1 hP]
  unfold wr dwr dg fr
  set Y := Yr n ρ with hYdef
  set G := g (n : ℝ) ℓ Y with hGdef
  set Q := 1 - Y with hQdef
  set P := (ℓ - 1) + (n : ℝ) * Y with hPdef
  field_simp
  rw [hQdef, hPdef]
  ring

/-- V = w² + w′ on (1, ∞): `riccati_plus` with (a). -/
theorem V_eq (n : ℕ) (hn : 2 ≤ n) (ℓ : ℝ) (hℓ : 2 ≤ ℓ) (ρ : ℝ) (hρ : 1 < ρ) :
    Vr n ℓ ρ = wr n ℓ ρ ^ 2 + fr n ρ * deriv (wr n ℓ) ρ := by
  have hρ0 : ρ ≠ 0 := by linarith
  have hY := Yr_mem n hn ρ hρ
  have h1 : 1 - Yr n ρ ≠ 0 := by linarith [hY.2]
  have hP : (ℓ - 1) + (n : ℝ) * Yr n ρ ≠ 0 := by
    have : (0 : ℝ) < (n : ℝ) * Yr n ρ := mul_pos (by exact_mod_cast (by omega : 0 < n)) hY.1
    linarith
  have hn1 : (n : ℝ) + 1 ≠ 0 := by positivity
  have hln : ℓ + (n : ℝ) ≠ 0 := by have : (0 : ℝ) ≤ n := Nat.cast_nonneg n; linarith
  have hf := fr_pos n hn ρ hρ
  have hr := riccati_plus n hn ℓ (by linarith) ρ hρ
  rw [z_id (n : ℝ) ℓ (Yr n ρ) hn1 hln h1 hP, div_eq_iff hf.ne'] at hr
  unfold Vr
  rw [div_eq_iff (pow_ne_zero 2 hρ0)]
  linear_combination -hr

/-- Ṽ = w² − w′ on (1, ∞): `riccati_minus` with (c). -/
theorem Vt_eq (n : ℕ) (hn : 2 ≤ n) (ℓ : ℝ) (hℓ : 1 ≤ ℓ) (ρ : ℝ) (hρ : 1 < ρ) :
    Vtr n ℓ ρ = wr n ℓ ρ ^ 2 - fr n ρ * deriv (wr n ℓ) ρ := by
  have hρ0 : ρ ≠ 0 := by linarith
  have hY := Yr_mem n hn ρ hρ
  have h1 : 1 - Yr n ρ ≠ 0 := by linarith [hY.2]
  have hP : (ℓ - 1) + (n : ℝ) * Yr n ρ ≠ 0 := by
    have : (0 : ℝ) < (n : ℝ) * Yr n ρ := mul_pos (by exact_mod_cast (by omega : 0 < n)) hY.1
    linarith
  have hf := fr_pos n hn ρ hρ
  have hr := riccati_minus n hn ℓ hℓ ρ hρ
  rw [partner (n : ℝ) ℓ (Yr n ρ) h1 hP, div_eq_iff hf.ne'] at hr
  unfold Vtr
  rw [div_eq_iff (pow_ne_zero 2 hρ0)]
  linear_combination -hr

/-! #### The zero mode u₀, and S = −(log u₀)_{r*} -/

/-- u₀ = ρ^(−ν)(1 − Y)^(−ℓ/(n−1))/((ℓ − 1) + nY) (RESULT.md), with real powers. -/
def u0 (n : ℕ) (ℓ ρ : ℝ) : ℝ :=
  ρ ^ (-nu n ℓ) * (1 - Yr n ρ) ^ (-(ℓ / ((n : ℝ) - 1))) / ((ℓ - 1) + n * Yr n ρ)

theorem u0_pos (n : ℕ) (hn : 2 ≤ n) (ℓ : ℝ) (hℓ : 1 ≤ ℓ) (ρ : ℝ) (hρ : 1 < ρ) : 0 < u0 n ℓ ρ := by
  have hY := Yr_mem n hn ρ hρ
  have hP : 0 < (ℓ - 1) + (n : ℝ) * Yr n ρ := by
    have : (0 : ℝ) < (n : ℝ) * Yr n ρ := mul_pos (by exact_mod_cast (by omega : 0 < n)) hY.1
    linarith
  unfold u0
  exact div_pos (mul_pos (Real.rpow_pos_of_pos (by linarith) _) (Real.rpow_pos_of_pos (by linarith [hY.2]) _)) hP

/-- d(log u₀)/dρ = g/ρ on (1, ∞). -/
theorem log_u0_hasDerivAt (n : ℕ) (hn : 2 ≤ n) (ℓ : ℝ) (hℓ : 1 ≤ ℓ) (ρ : ℝ) (hρ : 1 < ρ) :
    HasDerivAt (fun x => Real.log (u0 n ℓ x)) (g n ℓ (Yr n ρ) / ρ) ρ := by
  have hρ0 : ρ ≠ 0 := by linarith
  have hY := Yr_mem n hn ρ hρ
  have hQ : 0 < 1 - Yr n ρ := by linarith [hY.2]
  have hP : 0 < (ℓ - 1) + (n : ℝ) * Yr n ρ := by
    have : (0 : ℝ) < (n : ℝ) * Yr n ρ := mul_pos (by exact_mod_cast (by omega : 0 < n)) hY.1
    linarith
  have hn1 : (n : ℝ) - 1 ≠ 0 := by
    have : (2 : ℝ) ≤ n := by exact_mod_cast hn
    linarith
  have hYd := Yr_hasDerivAt n hn ρ hρ0
  have a1 := (Real.hasDerivAt_log hρ0).const_mul (-nu n ℓ)
  have a2 := ((hYd.const_sub 1).log hQ.ne').const_mul (ℓ / ((n : ℝ) - 1))
  have a3 := ((hYd.const_mul (n : ℝ)).const_add (ℓ - 1)).log hP.ne'
  have hL := (a1.sub a2).sub a3
  have hL' : HasDerivAt (fun x => -nu n ℓ * Real.log x - ℓ / ((n : ℝ) - 1) * Real.log (1 - Yr n x)
      - Real.log ((ℓ - 1) + n * Yr n x)) (g n ℓ (Yr n ρ) / ρ) ρ := by
    convert hL using 1
    unfold g nu
    set Y := Yr n ρ with hYdef
    set Q := 1 - Y with hQdef
    set P := (ℓ - 1) + (n : ℝ) * Y with hPdef
    field_simp
    rw [hQdef, hPdef]
    ring
  apply hL'.congr_of_eventuallyEq
  filter_upwards [Ioi_mem_nhds hρ] with x hx
  have hYx := Yr_mem n hn x hx
  have hQx : 0 < 1 - Yr n x := by linarith [hYx.2]
  have hPx : 0 < (ℓ - 1) + (n : ℝ) * Yr n x := by
    have : (0 : ℝ) < (n : ℝ) * Yr n x := mul_pos (by exact_mod_cast (by omega : 0 < n)) hYx.1
    linarith
  have hx0 : 0 < x := by linarith [show (1 : ℝ) < x from hx]
  unfold u0
  rw [Real.log_div (mul_pos (Real.rpow_pos_of_pos hx0 _) (Real.rpow_pos_of_pos hQx _)).ne' hPx.ne',
    Real.log_mul (Real.rpow_pos_of_pos hx0 _).ne' (Real.rpow_pos_of_pos hQx _).ne',
    Real.log_rpow hx0, Real.log_rpow hQx]
  ring

/-- w = (log u₀)_{r*}: the r*-derivative of log u₀(R(r*)) is w(R(r*)). -/
theorem w_log_deriv (n : ℕ) (hn : 2 ≤ n) (ℓ : ℝ) (hℓ : 1 ≤ ℓ) (t : ℝ) :
    HasDerivAt (fun s => Real.log (u0 n ℓ (Rt n s))) (wr n ℓ (Rt n t)) t := by
  have hR := Rt_spec n hn t
  have h := (log_u0_hasDerivAt n hn ℓ hℓ (Rt n t) hR.1).comp t (Rt_hasDerivAt n hn t)
  convert h using 1
  unfold wr
  ring

/-- S = −(log u₀)_{r*} = −w(R). -/
theorem S_eq (n : ℕ) (hn : 2 ≤ n) (ℓ : ℝ) (hℓ : 1 ≤ ℓ) (t : ℝ) :
    -wr n ℓ (Rt n t) = -deriv (fun s => Real.log (u0 n ℓ (Rt n s))) t := by
  rw [(w_log_deriv n hn ℓ hℓ t).deriv]

/-! #### Continuity, the zero-energy equation in r*, and A_{ℓ,1} ≥ 0 -/

theorem W_continuousAt (n ℓ Y : ℝ) (h1 : n + 1 ≠ 0) (h2 : ℓ + n ≠ 0) (hP : (ℓ - 1) + n * Y ≠ 0) :
    ContinuousAt (W n ℓ) Y := by
  have hH : Hm n (mm n ℓ) (δ1 n ℓ) (2 * Y) ≠ 0 := by
    rw [gate_H n ℓ Y h1 h2]; exact mul_ne_zero h2 hP
  show ContinuousAt (fun Y => Um n 1 (mm n ℓ) (δ1 n ℓ) (2 * Y) 0 / (64 * Hm n (mm n ℓ) (δ1 n ℓ) (2 * Y) ^ 2)) Y
  apply ContinuousAt.div
  · unfold Um; fun_prop
  · unfold Hm; fun_prop
  · exact mul_ne_zero (by norm_num) (pow_ne_zero 2 hH)

theorem Vr_continuousAt (n : ℕ) (hn : 2 ≤ n) (ℓ : ℝ) (hℓ : 2 ≤ ℓ) (ρ : ℝ) (hρ : 1 < ρ) :
    ContinuousAt (Vr n ℓ) ρ := by
  have hρ0 : ρ ≠ 0 := by linarith
  have hY := Yr_mem n hn ρ hρ
  have hP : (ℓ - 1) + (n : ℝ) * Yr n ρ ≠ 0 := by
    have : (0 : ℝ) < (n : ℝ) * Yr n ρ := mul_pos (by exact_mod_cast (by omega : 0 < n)) hY.1
    linarith
  have hn1 : (n : ℝ) + 1 ≠ 0 := by positivity
  have hln : ℓ + (n : ℝ) ≠ 0 := by have : (0 : ℝ) ≤ n := Nat.cast_nonneg n; linarith
  have cY := (Yr_hasDerivAt n hn ρ hρ0).continuousAt
  have cf := (fr_hasDerivAt n hn ρ hρ0).continuousAt
  have cW := (W_continuousAt (n : ℝ) ℓ (Yr n ρ) hn1 hln hP).comp cY
  exact (cf.mul cW).div (continuousAt_id.pow 2) (pow_ne_zero 2 hρ0)

/-- V_S− at q = 1 as a function of r*. -/
def Vstar (n : ℕ) (ℓ t : ℝ) : ℝ := Vr n ℓ (Rt n t)

/-- The zero mode in r*: U = u₀ ∘ R has U′ = w(R)U and U″ = V U, the q = 1 zero-energy master equation. -/
theorem zero_mode (n : ℕ) (hn : 2 ≤ n) (ℓ : ℝ) (hℓ : 2 ≤ ℓ) (t : ℝ) :
    HasDerivAt (fun s => u0 n ℓ (Rt n s)) (wr n ℓ (Rt n t) * u0 n ℓ (Rt n t)) t ∧
      HasDerivAt (fun s => wr n ℓ (Rt n s) * u0 n ℓ (Rt n s)) (Vstar n ℓ t * u0 n ℓ (Rt n t)) t := by
  have hU : ∀ s, HasDerivAt (fun s => u0 n ℓ (Rt n s)) (wr n ℓ (Rt n s) * u0 n ℓ (Rt n s)) s := by
    intro s
    have hpos : ∀ x, 0 < u0 n ℓ (Rt n x) := fun x => u0_pos n hn ℓ (by linarith) (Rt n x) (Rt_spec n hn x).1
    have h := (w_log_deriv n hn ℓ (by linarith) s).exp
    have e : (fun x => Real.exp (Real.log (u0 n ℓ (Rt n x)))) = fun x => u0 n ℓ (Rt n x) := by
      funext x; exact Real.exp_log (hpos x)
    rw [e, Real.exp_log (hpos s)] at h
    convert h using 1
    ring
  refine ⟨hU t, ?_⟩
  have hR := Rt_spec n hn t
  have hw := (wr_hasDerivAt n hn ℓ (by linarith) (Rt n t) hR.1).comp t (Rt_hasDerivAt n hn t)
  have h := hw.mul (hU t)
  convert h using 1
  unfold Vstar
  rw [V_eq n hn ℓ hℓ (Rt n t) hR.1, (wr_hasDerivAt n hn ℓ (by linarith) (Rt n t) hR.1).deriv]
  simp only [Function.comp_apply]
  ring

/-- (d): A_{ℓ,1} ≥ 0. For every integer n ≥ 2 and ℓ ≥ 2, the quadratic form of −d²/dr*² + V_S− at q = 1 is
    nonnegative on C¹ functions with compact support (C₀^∞ included): Lemma 1 with S = −(log u₀)_{r*}. -/
theorem A_nonneg (n : ℕ) (hn : 2 ≤ n) (ℓ : ℝ) (hℓ : 2 ≤ ℓ) (φ φ' : ℝ → ℂ)
    (hφ : ∀ x, HasDerivAt φ (φ' x) x) (hφ' : Continuous φ') (hc : HasCompactSupport φ) :
    0 ≤ ∫ x, (‖φ' x‖ ^ 2 + Vstar n ℓ x * ‖φ x‖ ^ 2) := by
  have hR := fun t => Rt_spec n hn t
  have cR := Rt_continuous n hn
  have cV : ∀ t, ContinuousAt (fun s => Vr n ℓ (Rt n s)) t :=
    fun t => (Vr_continuousAt n hn ℓ hℓ (Rt n t) (hR t).1).comp cR.continuousAt
  have cw : ∀ t, ContinuousAt (fun s => wr n ℓ (Rt n s)) t :=
    fun t => (wr_hasDerivAt n hn ℓ (by linarith) (Rt n t) (hR t).1).continuousAt.comp cR.continuousAt
  have hV : Continuous (Vstar n ℓ) := continuous_iff_continuousAt.2 cV
  have hS : ∀ t, HasDerivAt (fun s => -wr n ℓ (Rt n s)) (-(Vr n ℓ (Rt n t) - wr n ℓ (Rt n t) ^ 2)) t := by
    intro t
    have h := ((wr_hasDerivAt n hn ℓ (by linarith) (Rt n t) (hR t).1).comp t (Rt_hasDerivAt n hn t)).neg
    convert h using 1
    rw [V_eq n hn ℓ hℓ (Rt n t) (hR t).1, (wr_hasDerivAt n hn ℓ (by linarith) (Rt n t) (hR t).1).deriv]
    ring
  have hS' : Continuous (fun t => -(Vr n ℓ (Rt n t) - wr n ℓ (Rt n t) ^ 2)) :=
    continuous_iff_continuousAt.2 fun t => ((cV t).sub ((cw t).pow 2)).neg
  exact form_nonneg_of_sdef (Vstar n ℓ) (fun s => -wr n ℓ (Rt n s))
    (fun t => -(Vr n ℓ (Rt n t) - wr n ℓ (Rt n t) ^ 2)) φ φ' hV hS hS' hφ hφ' hc
    (fun x => le_of_eq (by simp only [Vstar]; ring))

end BHModes.Z
