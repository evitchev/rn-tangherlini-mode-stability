/-
  BHModesA1: the algebraic identities behind the bh-modes stage-1 target A1 (session-L, 2026-10-22).
  Private under the bh-modes quiet rule. The request is the bh-modes lead's of 2026-10-22, item 3(a).
  Sources:
  - Kodama–Ishibashi hep-th/0308128 (S5), read from the rendered pages 5, 21, 24 and 25 of the coordinator's own fetch,
    byte-identical to the screen's copy: (2.19), (5.39), (5.40), (5.58), (5.60), (5.62b), (5.63b), (5.65);
  - bh-modes TARGET.md §1 and §3.
  Named inputs: the transcriptions of (5.62b) and (5.63b) (`KI_Hm`, `KI_Um`) and TARGET.md's H₋ and U₋ (`Hm`, `Um`).
  `oracle/check_identities.py` checks every identity here symbolically.
  Not proved here: the asymptotics V ≈ c/r*² near the degenerate horizon. Only its algebraic content is proved:
  κ r_H² = 9, from the second derivative of f, and the value of c.
-/
import Mathlib.Data.Real.Sqrt
import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Pow
import Mathlib.Analysis.Calculus.Deriv.Inv
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith

set_option autoImplicit false
set_option relaxedAutoImplicit false

namespace BHModes

noncomputable section

/-! ### Kodama–Ishibashi, general n, and the D = 6 specialisation of TARGET.md -/

/-- Kodama–Ishibashi (5.62b): `H₋ = m + n(n+1)/2 (1 + mδ) x`. -/
def KI_Hm (n m δ x : ℝ) : ℝ := m + n * (n + 1) / 2 * (1 + m * δ) * x

/-- Kodama–Ishibashi (5.63b): `U₋` for general `n` and `K`, with `y = λ r²`. -/
def KI_Um (n K m δ x y : ℝ) : ℝ :=
  (-4 * n ^ 3 * (n + 2) * (n + 1) ^ 2 * (1 + m * δ) ^ 2 * x ^ 2
      + 48 * n ^ 2 * (n + 1) * (n - 2) * m * (1 + m * δ) * x - 16 * (n - 2) * (n - 4) * m ^ 2) * y
    - n ^ 3 * (3 * n - 2) * (n + 1) ^ 4 * δ * (1 + m * δ) ^ 3 * x ^ 4
    - 4 * n ^ 2 * (n + 1) ^ 2 * (1 + m * δ) ^ 2 * ((n + 1) * (3 * n - 2) * m * δ - n ^ 2) * x ^ 3
    + 4 * (n + 1) * (1 + m * δ) * (m * (n - 2) * (n - 4) * (n + 1) * (m + n ^ 2 * K) * δ
        + 4 * n * (2 * n ^ 2 - 3 * n + 4) * m + n ^ 2 * (n - 2) * (n - 4) * (n + 1) * K) * x ^ 2
    - 16 * m * ((n + 1) * m * (-4 * m + 3 * n ^ 2 * (n - 2) * K) * δ + 3 * n * (n - 4) * m
        + 3 * n ^ 2 * (n + 1) * (n - 2) * K) * x
    + 64 * m ^ 3 + 16 * n * (n + 2) * m ^ 2 * K

/-- TARGET.md §1: `H₋` at `n = 4`, `K = 1`, `λ = 0`. -/
def Hm (m δ x : ℝ) : ℝ := m + 10 * (1 + m * δ) * x

/-- TARGET.md §1: `U₋` at `n = 4`, `K = 1`, `λ = 0`. -/
def Um (m δ x : ℝ) : ℝ :=
  -400000 * δ * (1 + m * δ) ^ 3 * x ^ 4 - 1600 * (1 + m * δ) ^ 2 * (50 * m * δ - 16) * x ^ 3
    + 7680 * m * (1 + m * δ) * x ^ 2 - 16 * m * (5 * m * (96 - 4 * m) * δ + 480) * x + 64 * m ^ 3 + 384 * m ^ 2

/-- (5.62b) at `n = 4` is TARGET.md's `H₋`. -/
theorem KI_Hm_n4 (m δ x : ℝ) : KI_Hm 4 m δ x = Hm m δ x := by
  unfold KI_Hm Hm; ring

/-- (5.63b) at `n = 4`, `K = 1`, `y = 0` is TARGET.md's `U₋`. -/
theorem KI_Um_n4 (m δ x : ℝ) : KI_Um 4 1 m δ x 0 = Um m δ x := by
  unfold KI_Um Um; ring

/-- (5.39) at `n = 4`, `K = 1`, with the S⁴ eigenvalue `k² = ℓ(ℓ + 3)`: `m = (ℓ − 1)(ℓ + 4)`. -/
theorem m_of_ell (ℓ : ℝ) : ℓ * (ℓ + 3) - 4 * 1 = (ℓ - 1) * (ℓ + 4) := by ring

/-! ### The metric function and its outer horizon -/

/-- (2.19) and (5.40) at `n = 4`, `K = 1`, `λ = 0`: `f = 1 − x + q²x²/4` with `x = 2M/r³` and `q = Q/M`. -/
theorem f_in_x (M Q r : ℝ) (hM : M ≠ 0) (hr : r ≠ 0) :
    1 - 2 * M / r ^ 3 + Q ^ 2 / r ^ 6 = 1 - 2 * M / r ^ 3 + (Q / M) ^ 2 * (2 * M / r ^ 3) ^ 2 / 4 := by
  field_simp; ring

/-- The outer horizon `x_H = 2/(1 + √(1 − q²))` is a zero of `f`, for `q² ≤ 1`. -/
theorem f_horizon (q : ℝ) (hq : q ^ 2 ≤ 1) :
    1 - 2 / (1 + Real.sqrt (1 - q ^ 2)) + q ^ 2 * (2 / (1 + Real.sqrt (1 - q ^ 2))) ^ 2 / 4 = 0 := by
  have hs : Real.sqrt (1 - q ^ 2) ^ 2 = 1 - q ^ 2 := Real.sq_sqrt (by linarith)
  have hpos : 0 < 1 + Real.sqrt (1 - q ^ 2) := by positivity
  field_simp
  linear_combination 4 * hs

/-- `f > 0` on the exterior: `0 ≤ x < x_H` gives `1 − x + q²x²/4 > 0`, for `q² ≤ 1`. -/
theorem f_pos_exterior (q x : ℝ) (hq : q ^ 2 ≤ 1) (hx0 : 0 ≤ x) (hx : x < 2 / (1 + Real.sqrt (1 - q ^ 2))) :
    0 < 1 - x + q ^ 2 * x ^ 2 / 4 := by
  set s := Real.sqrt (1 - q ^ 2) with hs_def
  have hs : s ^ 2 = 1 - q ^ 2 := Real.sq_sqrt (by linarith)
  have hs0 : 0 ≤ s := Real.sqrt_nonneg _
  have hpos : 0 < 1 + s := by linarith
  have hx' : x * (1 + s) < 2 := by rwa [lt_div_iff₀ hpos] at hx
  -- 4 f = (2 − x(1 + s))(2 − x(1 − s)), and both factors are positive
  have h1 : 0 < 2 - x * (1 + s) := by linarith
  have h2 : 0 < 2 - x * (1 - s) := by nlinarith
  nlinarith [mul_pos h1 h2]

/-! ### The parameter δ -/

/-- (5.58) and (5.60) at `n = 4` give the defining relation of δ: `(1 + 2mδ)² = 1 + 4m(Q/M)²/25`. -/
theorem delta_relation (M Q m δ μ : ℝ) (hM : M ≠ 0)
    (h58 : μ ^ 2 = M ^ 2 + 4 * m * Q ^ 2 / (4 + 1) ^ 2) (h60 : μ = (1 + 2 * m * δ) * M) :
    (1 + 2 * m * δ) ^ 2 = 1 + 4 * m * (Q / M) ^ 2 / 25 := by
  subst h60
  field_simp
  linear_combination 25 * h58

/-- For `m ≠ 0`, the relation is equivalent to (5.65) at `n = 4`: `Q² = 25 M² δ (1 + mδ)`. -/
theorem delta_relation_iff (M Q m δ : ℝ) (hM : M ≠ 0) (hm : m ≠ 0) :
    (1 + 2 * m * δ) ^ 2 = 1 + 4 * m * (Q / M) ^ 2 / 25 ↔ Q ^ 2 = (4 + 1) ^ 2 * M ^ 2 * δ * (1 + m * δ) := by
  have key : (1 + 2 * m * δ) ^ 2 - (1 + 4 * m * (Q / M) ^ 2 / 25)
      = 4 * m / (25 * M ^ 2) * ((4 + 1) ^ 2 * M ^ 2 * δ * (1 + m * δ) - Q ^ 2) := by
    field_simp; ring
  have hc : 4 * m / (25 * M ^ 2) ≠ 0 := by positivity
  constructor
  · intro h
    have h0 : 4 * m / (25 * M ^ 2) * ((4 + 1) ^ 2 * M ^ 2 * δ * (1 + m * δ) - Q ^ 2) = 0 := by
      rw [← key, h, sub_self]
    have := (mul_eq_zero.mp h0).resolve_left hc
    linarith
  · intro h
    have h0 : (1 + 2 * m * δ) ^ 2 - (1 + 4 * m * (Q / M) ^ 2 / 25) = 0 := by rw [key, h, sub_self, mul_zero]
    linarith

/-- The parametrisation `s = 1 + 2mδ = √(1 + 4mq²/25)`, for `m ≥ 0` and `δ ≥ 0`. -/
theorem s_param (m δ q : ℝ) (hm : 0 ≤ m) (hδ : 0 ≤ δ) (h : (1 + 2 * m * δ) ^ 2 = 1 + 4 * m * q ^ 2 / 25) :
    1 + 2 * m * δ = Real.sqrt (1 + 4 * m * q ^ 2 / 25) := by
  rw [← h, Real.sqrt_sq]
  positivity

/-! ### The extremal limit q = 1 (information for A2) -/

/-- At `q = 1`, with `m = (ℓ − 1)(ℓ + 4)`, `ℓ ≥ 2` and `δ ≥ 0`: `δ = 1/(5(ℓ + 4))`. -/
theorem delta_extremal (ℓ δ : ℝ) (hℓ : 2 ≤ ℓ) (hδ : 0 ≤ δ)
    (h : (1 + 2 * ((ℓ - 1) * (ℓ + 4)) * δ) ^ 2 = 1 + 4 * ((ℓ - 1) * (ℓ + 4)) * 1 ^ 2 / 25) :
    δ = 1 / (5 * (ℓ + 4)) := by
  have hm : 0 < (ℓ - 1) * (ℓ + 4) := by nlinarith
  have h1 : 1 + 4 * ((ℓ - 1) * (ℓ + 4)) * 1 ^ 2 / 25 = ((2 * ℓ + 3) / 5) ^ 2 := by ring
  rw [h1] at h
  have hA : 0 ≤ 1 + 2 * ((ℓ - 1) * (ℓ + 4)) * δ := by positivity
  have hB : 0 ≤ (2 * ℓ + 3) / 5 := by linarith
  have h2 : 1 + 2 * ((ℓ - 1) * (ℓ + 4)) * δ = (2 * ℓ + 3) / 5 := (sq_eq_sq₀ hA hB).mp h
  have h4 : ℓ + 4 ≠ 0 := by linarith
  have hl1 : ℓ - 1 ≠ 0 := by linarith
  field_simp
  have h3 : 2 * ((ℓ - 1) * (ℓ + 4)) * δ = 2 * (ℓ - 1) / 5 := by linarith
  have h5 : (ℓ - 1) * (2 * ((ℓ + 4) * δ * 5) - 2) = 0 := by linear_combination 5 * h3
  have h6 := (mul_eq_zero.mp h5).resolve_left hl1
  linarith

/-- At `q = 1`, `f(r) = (1 − M/r³)²`. -/
theorem f_extremal (M r : ℝ) (hr : r ≠ 0) : 1 - 2 * M / r ^ 3 + M ^ 2 / r ^ 6 = (1 - M / r ^ 3) ^ 2 := by
  field_simp; ring

/-- The first derivative of `f(r) = 1 − 2M/r³ + M²/r⁶` at `r ≠ 0`. -/
theorem f_hasDerivAt (M r : ℝ) (hr : r ≠ 0) :
    HasDerivAt (fun r : ℝ => 1 - 2 * M / r ^ 3 + M ^ 2 / r ^ 6) (6 * M / r ^ 4 - 6 * M ^ 2 / r ^ 7) r := by
  have h3 : HasDerivAt (fun r : ℝ => r ^ 3) (3 * r ^ 2) r := by simpa using hasDerivAt_pow 3 r
  have h6 : HasDerivAt (fun r : ℝ => r ^ 6) (6 * r ^ 5) r := by simpa using hasDerivAt_pow 6 r
  have hr3 : r ^ 3 ≠ 0 := pow_ne_zero 3 hr
  have hr6 : r ^ 6 ≠ 0 := pow_ne_zero 6 hr
  have hA : HasDerivAt (fun r : ℝ => 2 * M / r ^ 3) ((0 * r ^ 3 - 2 * M * (3 * r ^ 2)) / (r ^ 3) ^ 2) r :=
    HasDerivAt.div (hasDerivAt_const r (2 * M)) h3 hr3
  have hB : HasDerivAt (fun r : ℝ => M ^ 2 / r ^ 6) ((0 * r ^ 6 - M ^ 2 * (6 * r ^ 5)) / (r ^ 6) ^ 2) r :=
    HasDerivAt.div (hasDerivAt_const r (M ^ 2)) h6 hr6
  have hC := HasDerivAt.add (HasDerivAt.sub (hasDerivAt_const r (1 : ℝ)) hA) hB
  refine HasDerivAt.congr_deriv hC ?_
  field_simp
  ring

/-- The second derivative of `f` at `r ≠ 0`. -/
theorem f'_hasDerivAt (M r : ℝ) (hr : r ≠ 0) :
    HasDerivAt (fun r : ℝ => 6 * M / r ^ 4 - 6 * M ^ 2 / r ^ 7) (-24 * M / r ^ 5 + 42 * M ^ 2 / r ^ 8) r := by
  have h4 : HasDerivAt (fun r : ℝ => r ^ 4) (4 * r ^ 3) r := by simpa using hasDerivAt_pow 4 r
  have h7 : HasDerivAt (fun r : ℝ => r ^ 7) (7 * r ^ 6) r := by simpa using hasDerivAt_pow 7 r
  have hr4 : r ^ 4 ≠ 0 := pow_ne_zero 4 hr
  have hr7 : r ^ 7 ≠ 0 := pow_ne_zero 7 hr
  have hA : HasDerivAt (fun r : ℝ => 6 * M / r ^ 4) ((0 * r ^ 4 - 6 * M * (4 * r ^ 3)) / (r ^ 4) ^ 2) r :=
    HasDerivAt.div (hasDerivAt_const r (6 * M)) h4 hr4
  have hB : HasDerivAt (fun r : ℝ => 6 * M ^ 2 / r ^ 7) ((0 * r ^ 7 - 6 * M ^ 2 * (7 * r ^ 6)) / (r ^ 7) ^ 2) r :=
    HasDerivAt.div (hasDerivAt_const r (6 * M ^ 2)) h7 hr7
  have hC := HasDerivAt.sub hA hB
  refine HasDerivAt.congr_deriv hC ?_
  field_simp
  ring

/-- `κ r_H² = 9` at the degenerate horizon `r_H³ = M`, where `κ = f''(r_H)/2`. -/
theorem kappa_extremal (M r : ℝ) (hr : r ≠ 0) (hM : r ^ 3 = M) :
    (-24 * M / r ^ 5 + 42 * M ^ 2 / r ^ 8) / 2 * r ^ 2 = 9 := by
  subst hM
  field_simp
  ring

/-- The near-horizon coefficient at `q = 1`. With `x_H = 2`, `δ = 1/(5(ℓ + 4))` and `κ r_H² = 9`,
`c = U₋(x_H)/(64 κ r_H² H₋(x_H)²)` equals `ℓ(ℓ − 3)/9`. -/
theorem c_extremal (ℓ : ℝ) (hℓ : 2 ≤ ℓ) :
    Um ((ℓ - 1) * (ℓ + 4)) (1 / (5 * (ℓ + 4))) 2
        / (64 * 9 * Hm ((ℓ - 1) * (ℓ + 4)) (1 / (5 * (ℓ + 4))) 2 ^ 2) = ℓ * (ℓ - 3) / 9 := by
  have h4 : 0 < ℓ + 4 := by linarith
  have hm : 0 < (ℓ - 1) * (ℓ + 4) := by nlinarith
  have hH : Hm ((ℓ - 1) * (ℓ + 4)) (1 / (5 * (ℓ + 4))) 2 ≠ 0 := by
    unfold Hm; positivity
  rw [div_eq_iff (by positivity)]
  unfold Um Hm
  field_simp
  ring

/-- The Breitenlöhner–Freedman margin: `c + 1/4 = (2ℓ − 3)²/36`. -/
theorem BF_margin (ℓ : ℝ) : ℓ * (ℓ - 3) / 9 + 1 / 4 = (2 * ℓ - 3) ^ 2 / 36 := by ring

/-- Non-vacuity: at `ℓ = 2` the coefficient is `−2/9`, and the margin is `1/36` (TARGET.md §3). -/
theorem nonvacuity_ell_two : (2 : ℝ) * (2 - 3) / 9 = -2 / 9 ∧ (2 * (2 : ℝ) - 3) ^ 2 / 36 = 1 / 36 := by
  constructor <;> norm_num

end

end BHModes
