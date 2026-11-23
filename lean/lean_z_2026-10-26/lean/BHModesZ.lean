/-
  bh-modes BHM-126 (results/extremal/RESULT.md): the extremal zero mode Z and its Darboux partner, as second party for
  exact identities (the lead's message 8 of 2026-10-26; operator ruling BHM-120; the rule of BHM-046). Session-L,
  2026-10-26.

  U₋ and H₋ are S5 (5.63b) and (5.62b) at general n, in session-L's transcription. `Hm`, `Um`, `mm` and `δ1` are the
  c_n layer's definitions (`BHModes.Cn`, lean_cn_2026-10-23, lines 24-43), copied byte for byte, at K = 1 and y = 0.
  At q = 1, with Y = ρ^(−(n−1)), x = 2Y and ν = ℓ + n/2 − 1:
      g = −ν − ℓY/(1 − Y) + n(n − 1)Y/((ℓ − 1) + nY)      (ρ ∂_ρ log u₀),
      W = U₋/(64 H₋²)  at  m = (ℓ − 1)(ℓ + n),  δ = δ₁ = 1/((n + 1)(ℓ + n)).
  (a) Z-id:     2(n − 1)Y(1 − Y)g + (1 − Y)²(g² − g − (n − 1)Y ∂_Y g) = W.
  (b) gates:    (n + 1)²δ₁(1 + mδ₁) = 1,   H₋(2Y) = (ℓ + n)((ℓ − 1) + nY).
  (c) partner:  (1 − Y)²(g² + g + (n − 1)Y ∂_Y g) − 2(n − 1)Y(1 − Y)g = Ũ, the quadratic of RESULT.md.
  Every statement is for real n, ℓ and Y wherever the denominators are non-zero, so n is symbolic.
-/
import Mathlib.Data.Real.Basic
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Inv
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.FunProp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.LinearCombination
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

end BHModes.Z
