/-
  bh-modes, target A1, Lemma U (bh-modes BHM-052, results/a1/RESULT.md Part II), as second party for exact
  identities (operator ruling of 2026-10-23). Session-L, 2026-10-23.

  For m ≥ 150 (so every ℓ ≥ 11), q² ≤ 1, TARGET.md's δ ≥ 0 with (1 + 2mδ)² = 1 + 4mq²/25, and 0 ≤ x ≤ 2:
      U₋(m, δ, x) ≥ m³ · 959747/17496 > 0.
  The proof is the record's: with m = ε⁻² and δ = κε, ε⁶U₋ = Pos − Neg, both with nonnegative coefficients;
  κ² = q²/25 − δ (S5 (5.58)) gives κ ≤ 1/5; m ≥ 150 gives ε ≤ 1/12; so Pos ≥ 64 and Neg ≤ Neg(1/12, 1/5, 2).
  U₋ is TARGET.md's (S5 (5.63b) at n = 4); its E0 check against S5 is in the A1 and extremal layers.
-/
import Mathlib.Data.Real.Sqrt
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.GCongr
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith

set_option autoImplicit false
set_option relaxedAutoImplicit false

noncomputable section

namespace BHModes.LemmaU

/-- TARGET.md's U₋ (S5 (5.63b), n = 4). -/
def Um (m δ x : ℝ) : ℝ :=
  -400000 * δ * (1 + m * δ) ^ 3 * x ^ 4 - 1600 * (1 + m * δ) ^ 2 * (50 * m * δ - 16) * x ^ 3
    + 7680 * m * (1 + m * δ) * x ^ 2 - 16 * m * (5 * m * (96 - 4 * m) * δ + 480) * x + 64 * m ^ 3 + 384 * m ^ 2

/-- The positive part of ε⁶U₋(x; ε⁻², κε). -/
def Pos (ε κ x : ℝ) : ℝ :=
  64 + 384 * ε ^ 2 + 320 * ε * κ * x + 7680 * ε ^ 4 * x ^ 2 + 7680 * ε ^ 3 * κ * x ^ 2 + 25600 * ε ^ 6 * x ^ 3

/-- The negative part: RESULT.md's nine monomials. -/
def Neg (ε κ x : ℝ) : ℝ :=
  7680 * ε ^ 3 * κ * x + 7680 * ε ^ 4 * x + 80000 * ε ^ 3 * κ ^ 3 * x ^ 3 + 134400 * ε ^ 4 * κ ^ 2 * x ^ 3
    + 28800 * ε ^ 5 * κ * x ^ 3 + 400000 * ε ^ 4 * κ ^ 4 * x ^ 4 + 1200000 * ε ^ 5 * κ ^ 3 * x ^ 4
    + 1200000 * ε ^ 6 * κ ^ 2 * x ^ 4 + 400000 * ε ^ 7 * κ * x ^ 4

/-- The split: ε⁶ U₋(x; m = ε⁻², δ = κε) = Pos − Neg. -/
theorem split (ε κ x : ℝ) (hε : ε ≠ 0) : ε ^ 6 * Um (1 / ε ^ 2) (κ * ε) x = Pos ε κ x - Neg ε κ x := by
  unfold Um Pos Neg
  field_simp
  ring

theorem Pos_zero : Pos 0 0 0 = 64 := by
  unfold Pos; norm_num

/-- S5 (5.58) in these variables: TARGET.md's (1 + 2mδ)² = 1 + 4mq²/25 gives κ² = q²/25 − δ for κ = δ√m. -/
theorem kappa_identity (m δ q : ℝ) (hm : 0 < m) (h : (1 + 2 * m * δ) ^ 2 = 1 + 4 * m * q ^ 2 / 25) :
    (δ * Real.sqrt m) ^ 2 = q ^ 2 / 25 - δ := by
  rw [mul_pow, Real.sq_sqrt hm.le]
  have h4 : 4 * m * (δ + m * δ ^ 2 - q ^ 2 / 25) = 0 := by linear_combination h
  have hm4 : 4 * m ≠ 0 := by positivity
  have := (mul_eq_zero.mp h4).resolve_left hm4
  linarith

theorem Pos_ge (ε κ x : ℝ) (hε : 0 ≤ ε) (hκ : 0 ≤ κ) (hx : 0 ≤ x) : 64 ≤ Pos ε κ x := by
  unfold Pos
  have : 0 ≤ 384 * ε ^ 2 + 320 * ε * κ * x + 7680 * ε ^ 4 * x ^ 2 + 7680 * ε ^ 3 * κ * x ^ 2
      + 25600 * ε ^ 6 * x ^ 3 := by positivity
  linarith

/-- Monotonicity: Neg has nonnegative coefficients, so it is largest at the corner of the box. -/
theorem Neg_mono (ε κ x : ℝ) (hε0 : 0 ≤ ε) (hε : ε ≤ 1 / 12) (hκ0 : 0 ≤ κ) (hκ : κ ≤ 1 / 5) (hx0 : 0 ≤ x)
    (hx : x ≤ 2) : Neg ε κ x ≤ Neg (1 / 12) (1 / 5) 2 := by
  unfold Neg
  gcongr

theorem corner : Neg (1 / 12) (1 / 5) 2 = 159997 / 17496 := by
  unfold Neg; norm_num

theorem corner_margin : 64 - Neg (1 / 12) (1 / 5) 2 = 959747 / 17496 := by
  rw [corner]; norm_num

/-- Lemma U. -/
theorem lemmaU (m q δ x : ℝ) (hm : 150 ≤ m) (hq : q ^ 2 ≤ 1) (hδ : 0 ≤ δ)
    (hdef : (1 + 2 * m * δ) ^ 2 = 1 + 4 * m * q ^ 2 / 25) (hx0 : 0 ≤ x) (hx2 : x ≤ 2) :
    m ^ 3 * (959747 / 17496) ≤ Um m δ x := by
  have hm0 : 0 < m := by linarith
  have hs : 0 < Real.sqrt m := Real.sqrt_pos.mpr hm0
  have hss : Real.sqrt m ^ 2 = m := Real.sq_sqrt hm0.le
  set ε := (Real.sqrt m)⁻¹ with hε
  set κ := δ * Real.sqrt m with hκ
  have hε0 : 0 < ε := inv_pos.mpr hs
  have hεm : 1 / ε ^ 2 = m := by rw [hε, inv_pow, hss]; field_simp
  have hκε : κ * ε = δ := by rw [hκ, hε]; field_simp
  have hs12 : 12 ≤ Real.sqrt m := by
    have h144 : Real.sqrt 144 = 12 := by
      rw [show (144 : ℝ) = 12 ^ 2 by norm_num]; exact Real.sqrt_sq (by norm_num)
    rw [← h144]; exact Real.sqrt_le_sqrt (by linarith)
  have hε12 : ε ≤ 1 / 12 := by
    rw [hε, inv_eq_one_div]; exact one_div_le_one_div_of_le (by norm_num) hs12
  have hκ0 : 0 ≤ κ := by positivity
  have hκsq : κ ^ 2 = q ^ 2 / 25 - δ := kappa_identity m δ q hm0 hdef
  have hκ5 : κ ≤ 1 / 5 := by nlinarith
  have hsplit := split ε κ x hε0.ne'
  rw [hεm, hκε] at hsplit
  have hP := Pos_ge ε κ x hε0.le hκ0 hx0
  have hN := Neg_mono ε κ x hε0.le hε12 hκ0 hκ5 hx0 hx2
  have hc := corner_margin
  have hlow : 959747 / 17496 ≤ ε ^ 6 * Um m δ x := by linarith
  have hεm3 : m ^ 3 * ε ^ 6 = 1 := by
    have h6 : ε ^ 6 = (m ^ 3)⁻¹ := by
      rw [hε, inv_pow, show Real.sqrt m ^ 6 = (Real.sqrt m ^ 2) ^ 3 by ring, hss]
    rw [h6, mul_inv_cancel₀ (by positivity)]
  calc m ^ 3 * (959747 / 17496) ≤ m ^ 3 * (ε ^ 6 * Um m δ x) := by gcongr
    _ = Um m δ x := by rw [← mul_assoc, hεm3, one_mul]

/-- Lemma U for every ℓ ≥ 11, with m = (ℓ − 1)(ℓ + 4). -/
theorem lemmaU_ell (ℓ : ℕ) (hℓ : 11 ≤ ℓ) (q δ x : ℝ) (hq : q ^ 2 ≤ 1) (hδ : 0 ≤ δ)
    (hdef : (1 + 2 * (((ℓ : ℝ) - 1) * ((ℓ : ℝ) + 4)) * δ) ^ 2
      = 1 + 4 * (((ℓ : ℝ) - 1) * ((ℓ : ℝ) + 4)) * q ^ 2 / 25) (hx0 : 0 ≤ x) (hx2 : x ≤ 2) :
    0 < Um (((ℓ : ℝ) - 1) * ((ℓ : ℝ) + 4)) δ x := by
  have h11 : (11 : ℝ) ≤ ℓ := by exact_mod_cast hℓ
  have hm : (150 : ℝ) ≤ ((ℓ : ℝ) - 1) * ((ℓ : ℝ) + 4) := by nlinarith
  have hU := lemmaU _ q δ x (by linarith) hq hδ hdef hx0 (by linarith)
  have hpos : 0 < (((ℓ : ℝ) - 1) * ((ℓ : ℝ) + 4)) ^ 3 * (959747 / 17496) := by
    have : 0 < ((ℓ : ℝ) - 1) * ((ℓ : ℝ) + 4) := by linarith
    positivity
  linarith

/-- TARGET.md's horizon x_H = 2/(1 + √(1 − q²)) is at most 2, so Lemma U covers the whole exterior 0 ≤ x ≤ x_H. -/
theorem xH_le_two (q : ℝ) : 2 / (1 + Real.sqrt (1 - q ^ 2)) ≤ 2 := by
  have h0 : 0 ≤ Real.sqrt (1 - q ^ 2) := Real.sqrt_nonneg _
  rw [div_le_iff₀ (by positivity)]
  nlinarith

end BHModes.LemmaU
