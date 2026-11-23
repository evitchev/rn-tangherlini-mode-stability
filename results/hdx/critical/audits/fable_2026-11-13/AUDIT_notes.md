# Working notes: every derivation behind AUDIT.md (Fable, 2026-11-13; written before AUDIT.md)

Notation. k = n − 1; ρ = r (units r_H = 1); z = 1 − 1/ρ ∈ (0, 1) on the exterior; y = (1 − z)^k = ρ^{−k};
x = x_H y; w = √(1 − q²) = Bμ/A with A = (ℓ + n) + (ℓ − 1)μ², B = 2ℓ + n − 1 (param_n); x_H = 2/(1 + w);
k_r := x_H/x₋ = (1 − w)/(1 + w); (1 − z) d/dz = ρ d/dρ. ν = ℓ + n/2 − 1; a = −ℓ/k; ε̂ = (1/k + 2/(k − ℓ))/2;
ε = ε̂w/(1 + w) = ε_n/ε_d; c = 1/4; S = ε_d z + ε_n; R = (1 − y)/z; H = H₋(x_H y) = Hn/Hd; U = Un/Ud; f = fn/fd.
w₁ := w′(0) = B/(ℓ + n); ε₁ := ε̂ w₁ (so ε = ε₁μ + O(μ²)).

## N0. The design at μ = 0 is Z's zero mode (why Z0 holds; a pencil check of the design's statement)
u₀ = ρ^{−ν}(1 − y)^{−ℓ/k}/h, h = (ℓ − 1) + ny.
(1 − z)(log u₀)_z = ρ (log u₀)_ρ:
- ρ d/dρ (−ν log ρ) = −ν.
- ρ d/dρ (−(ℓ/k) log(1 − y)) = −(ℓ/k)(−ρ y_ρ)/(1 − y) = −(ℓ/k)(k y)/(1 − y) = −ℓy/(1 − y) = −ℓy/(zR)  (ρ y_ρ = −k y; zR = 1 − y).
- −ρ (log h)_ρ = −(1 − z) h_z/h.
At μ = 0: w = 0, x_H = 2, δ(0) = 1/((ℓ + n)(n + 1)), 1 + mδ = (ℓ + n)/(n + 1), so
H = m + n(n + 1)(1 + mδ)x/2 = (ℓ − 1)(ℓ + n) + n(ℓ + n)y = (ℓ + n) h.  Hence H_z/H = h_z/h and
P(z, 0) = −ν − ℓy/(zR) − (1 − z)H_z/H = (1 − z)(log u₀)_z = g (A3's notation), the design's μ = 0 value (ε = 0, cμ = 0).
Then β = (1 − z)P = u₀,ρ/u₀, S = −fβ = −(log u₀)_{r*}, and Ṽ = V + S′ − S² = V − u₀″/u₀ = 0 for a zero mode,
i.e. N(z, 0) ≡ 0. (Z0 is the exact gate for this; the pencil reason is as above.)

## N1. Item 1: P is C^∞ (indeed analytic) on a neighbourhood of [0, 1] for each fixed μ ∈ (0, MU1]
P(z, μ) = −ν − ℓ y/((z + ε) R) − (1 − z) H_z/H + cμ is a rational function of z (y, R, H, H_z polynomials in z).
Poles:
- z = −ε. Gate S: ε_n(0) = 0, ε_n/μ > 0 and ε_d > 0 on [0, MU1]; so for μ > 0, ε = ε_n/ε_d > 0 and −ε < 0 ∉ [0, 1].
- Zeros of R(z) = (1 − (1 − z)^k)/z. R(z) = Σ_{j=0}^{k−1} (1 − z)^j (geometric sum), so R ≥ 1 on [0, 1] and R(0) = k.
  Its complex zeros are 1 − z = e^{2πij/k}, j = 1..k − 1: |1 − z| = 1, z ≠ 0 (real only z = 2 for even k). None in [0, 1].
  (Gate R certifies R > 0 on [0, 1] exactly; the geometric sum proves it by pencil.)
- Zeros of H = m + (n(n + 1)/2)(1 + mδ) x_H y. m = (ℓ − 1)(ℓ + n) > 0 (ℓ ≥ 2); δ(μ) > 0 on [0, MU1] (gate H; pencil:
  δ > 0 iff s > 1 iff (B − n − 1)(ℓ + n) > (B + n + 1)(ℓ − 1)μ² iff 2(ℓ − 1)(ℓ + n)(1 − μ²) > 0 iff μ² < 1);
  x_H = 2/(1 + w) > 0 (w ≥ 0); y ≥ 0 for z ≤ 1. So H ≥ m > 0 on [0, 1]. Its zero is at y = −m/α < 0 (α > 0):
  for odd k a real z > 1, for even k none real.
So P is analytic on an open set containing [0, 1]; in particular C¹ on (0, 1) (Proposition 3's hypothesis) and C^∞ on
[0, 1] as the PREREG says. (At μ = 0 the pole −ε sits at z = 0: excluded by μ > 0; q = 1 is Z's.)

The identity NL = N S² R² L (PREREG §2 displays NL as a polynomial and defines it as N S² R² L; the equality):
With D := S R Hn and Π := P D. Since (z + ε) = S/ε_d and H_z/H = Hn_z/Hn (Hd is μ-only),
  Π = (−ν + cμ) S R Hn − ℓ ε_d y Hn − (1 − z) Hn_z S R      — a polynomial (= critical.py l.159–160's Pi).
P = Π/D, P_z = (Π_z D − Π D_z)/D². The bracket in N:
  (1 − z)(fzn/fd)(Π/D) + (fn/fd)(−Π/D + (1 − z)(Π_z D − Π D_z)/D² + Π²/D²) = B/(fd D²),
  B := (1 − z) fzn Π D + fn(−Π D + (1 − z)(Π_z D − Π D_z) + Π²).
N = Un/Ud − 64 (Hn²/Hd²) B/(fd D²). Multiply by Ud Hd² fd D² and use D² = S² R² Hn²:
  N · Ud Hd² fd S² R² Hn² = Un Hd² fd S² R² Hn² − 64 Ud Hn² B;  divide by Hn² (≠ 0 on [0, 1] × [0, MU1]):
  N · (Ud Hd² fd) S² R² = Un Hd² fd S² R² − 64 Ud B = the displayed NL.   ∎
Valid wherever N is defined (D ≠ 0 and Ud, Hd, fd ≠ 0), i.e. on [0, 1] × (0, MU1] given gates S, R, H, L.
Sign: for μ ∈ (0, MU1] and z ∈ [0, 1]: S = ε_d z + ε_n > 0 (both coefficients > 0 for μ > 0), R ≥ 1, L > 0 (gate L;
L depends on μ only). So S² R² L > 0 and sign N = sign NL. Only S ≠ 0, R ≠ 0, L > 0 are needed; the gates give more.
(The factored f of exact_parts equals the unfactored one: (1 − y)(1 − k_r y) = 1 − (1 + k_r)y + k_r y² with
1 + k_r = 2/(1 + w) = x_H and k_r = (1 − w²)x_H²/4 = q² x_H²/4, so = 1 − x_H y + q² x_H² y²/4 = 1 − x + q²x²/4.)

## N2. Item 2: the divisions and the edges
Write NL = Σ c_{ij} z^i μ^j.
- M := NL/μ exists iff every monomial has j ≥ 1 iff NL(z, 0) ≡ 0 (Z0 ⟺ DIV-O). Then NL = μ M identically.
- T := NL(μζ, μ)/μ²: NL(μζ, μ) = Σ c_{ij} ζ^i μ^{i+j}; the map (i, j) ↦ (i, i + j) is injective, so no cancellation
  (critical.py l.175 accumulates exactly one term per key). Exact iff every monomial has i + j ≥ 2 (DIV-T, l.179).
  Then T(ζ, μ) = Σ c_{ij} ζ^i μ^{i+j−2} and μ² T(z/μ, μ) = NL(z, μ) for μ ≠ 0.
- K := NL(z, zσ)/(z²σ): NL(z, zσ) = Σ c_{ij} z^{i+j} σ^j; (i, j) ↦ (i + j, j) injective. Exact iff i + j ≥ 2 and
  j ≥ 1 for every monomial (DIV-C, l.180) — so DIV-C ⟺ DIV-O ∧ DIV-T. Then z²σ K(z, μ/z) = NL(z, μ) for z ≠ 0.
  Given Z0, DIV-T and DIV-C reduce to c_{01} = 0, i.e. M(0, 0) = 0 (FIRST's "M(z, 0) = O(z)").
What positivity on the closed box gives:
- O, O′ (M > 0 on [1/4, 1] × [0, MU1], [0, 1/4] × [1/32, MU1]): NL = μM > 0 at every point with μ > 0.
  Edge μ = 0 (O): NL = 0 there; M(z, 0) = ∂_μ NL(z, 0) > 0 says NL > 0 for small μ > 0 — not needed for the claim.
  Edge z = 0 (O′): NL(0, μ) = μ M(0, μ) > 0, i.e. N(0, μ) > 0 at the horizon for μ ∈ [1/32, MU1] — not needed
  (Proposition 3 uses (0, 1) only). Edge z = 1 (O): spatial infinity, not in (0, 1) — not needed; consistent with INF.
- T (T > 0 on [0, 8] × [0, 1/32]): for (z, μ) with μ > 0 and ζ = z/μ ∈ [0, 8], NL = μ² T(ζ, μ) > 0.
  Edge ζ = 0: z = 0, the horizon — not needed. Edge μ = 0: T(ζ, 0) = T₁ζ + T₀, the second-order jet of NL at the
  corner along z = ζμ; it is where the design window enters (N7) — a necessary condition for the closed-box certificate
  to exist, not a point of the claim (q = 1 is Z's).
- C (K > 0 on [0, 1/4] × [0, 1/8]): for (z, μ) with z > 0, σ = μ/z ∈ (0, 1/8], NL = z²σ K(z, σ) > 0 (μ > 0 forces
  z > 0 in this chart). Edge z = 0: the blown-up corner, K(0, σ) = c_{11} + c_{02}σ = T₁ + T₀σ (CORNER) — not needed.
  Edge σ = 0: μ = 0, K(z, 0) = M(z, 0)/z (NL(z, zσ) = zσ M(z, zσ) so K = M(z, zσ)/z) — not needed; at z → 0 it is
  K(0, 0) = M_z(0, 0) = c_{11} = T₁ (FIRST).
So: no point with z = 0, μ = 0 (in any chart: ζ = 0, σ = 0, z = 0 of C) or z = 1 is needed for the claim. The
boundaries between charts (z = 1/4; μ = 1/32; z = 8μ, i.e. ζ = 8 ⟺ σ = 1/8) are points of (0, 1) × (0, MU1] and are
covered because the boxes are closed (either neighbouring chart serves). The claim uses NL > 0 on the open set
(0, 1) × (0, MU1] only; the certificates prove it on [0, 1] × [0, MU1] with the blow-ups at (0, 0) and the μ = 0 edge.
Bookkeeping identities (pure exponent algebra, given the divisions): T(ζ, 0) = c_{02} + c_{11}ζ (T₀ = c_{02},
T₁ = c_{11}); M(z, 0) = c_{11} z + c_{21} z² + …, so M(0, 0) = c_{01} = 0 and M_z(0, 0) = c_{11}; K(0, σ) = c_{11} + c_{02}σ.
These are CORNER and the structural half of FIRST; only the values of T₀, T₁ carry content (N7).

## N3. Item 3: COVER
Constants: Z1 = 1/4, ZT = 8, SIG1 = 1/8, MUT = 1/32; MU1 ∈ {1/8, 13/100, 3/25}. ZT·SIG1 = 1; ZT·MUT = 1/4 = Z1;
Z1·SIG1 = 1/32 = MUT ≤ MU1 (3/25 = 0.12 is the least MU1). Also 0 < Z1 < 1 and 0 < MUT < MU1.
Case split for (z, μ) ∈ (0, 1) × (0, MU1]:
1. z ≥ Z1: (z, μ) ∈ [Z1, 1] × [0, MU1] = O.  (uses Z1 < 1)
2. z < Z1 and μ ≥ MUT: (z, μ) ∈ [0, Z1] × [MUT, MU1] = O′.  (uses MUT ≤ MU1, which is Z1·SIG1 ≤ MU1 when ZT·SIG1 = 1)
3. z < Z1, μ < MUT, z ≤ ZT μ: ζ := z/μ ∈ (0, ZT] (μ > 0), so (ζ, μ) ∈ [0, ZT] × [0, MUT] = T. (ZT·MUT ≤ Z1 makes
   T's image lie in z ≤ Z1, so the split's "z ≤ 8μ < 1/4" is consistent and no positivity is asked beyond z = 1/4.)
4. z < Z1, μ < MUT, z > ZT μ: σ := μ/z ∈ (0, 1/ZT) ⊂ (0, SIG1] since ZT·SIG1 ≥ 1; (z, σ) ∈ [0, Z1] × [0, SIG1] = C.
   (μ < MUT is automatic here: μ < z/ZT < Z1/ZT = MUT. Z1·SIG1 ≤ MU1 keeps C's image inside μ ≤ MU1.)
Exhaustive: (1) or not; if not, (2) or μ < MUT; then (3) or (4). Each lands in a closed box. The one inequality the
split itself needs beyond the ranges is ZT·SIG1 ≥ 1; the other two products bound the images of T and C inside
[0, Z1] × [0, MUT] ⊂ [0, 1] × [0, MU1] (so the certificates ask for positivity only where N is defined and claimed) and,
through MUT = Z1·SIG1 ≤ MU1, make O′ reach μ = MU1. critical.py l.452 checks the three products and the two ranges.
Union of the images: O ∪ O′ ∪ T-image {0 ≤ z ≤ 8μ ≤ 1/4} ∪ C-image {0 ≤ μ ≤ z/8, z ≤ 1/4} = [0, 1] × [0, MU1].

## N4. Item 4: Proposition 3 (prop3_Dn) and q(μ)
prop3_Dn (BHModesP3.lean l.638–644) hypotheses, matched at each fixed μ ∈ (0, MU1]:
- n ≥ 2 ✓ (n = 5..9). q² ≤ 1 ✓ (q = q(μ) ∈ [q(MU1), 1)). m > 0 ✓ (m = (ℓ − 1)(ℓ + n)). δ ≥ 0 ✓ (gate H: δ(μ) > 0;
  pencil N1; and the branch s = 1 + 2mδ > 0 is param_n's s = B((ℓ + n) − (ℓ − 1)μ²)/((n + 1)A) ≥ B(n + 1)/((n + 1)A) > 0,
  so δ is S5's δ ≥ 0 with (1 + 2mδ)² = 1 + 4mq²/(n + 1)², PARAM's identity).
- hP: P has derivative P′ on (0, 1); hP′: P′ continuous on (0, 1) ✓ (N1: P analytic near [0, 1]).
- hR, hR1: a function R : ℝ → (1, ∞) with R′(t) = Fn(zc(R t)) = f(ρ = R(t)), i.e. dρ/dr* = f: the inverse tortoise
  map. For 0 < q < 1: f = (1 − y)(1 − k_r y) > 0 on (1, ∞) (0 < k_r < 1), simple zero at ρ = 1 (f_z(0) = k(1 − k_r) > 0),
  f → 1 at ∞; r* = ∫dρ/f is a C^∞ strictly increasing bijection (1, ∞) → ℝ and R = (r*)^{−1} has R′ = f(R)
  (my A2, 2026-10-26, re-derived there). Needs q < 1: q(μ) < 1 for μ > 0 (w = Bμ/A > 0). q(μ) > 0 as well
  (q(MU1)² ≥ 0.978 in §3's table), though Lean needs only q² ≤ 1.
- hN: N(z, μ) ≥ 0 on (0, 1): N > 0 by N1–N3 given the certified charts. Lean's Nz (l.173–174) is METHOD.md's N with
  U = Un n q m δ = UmN n 1 m δ (x_H(q)(1 − z)^{n−1}) 0 (S5 (5.63b), K = 1, y = 0), H = HmN (5.62b), F = Fn = 1 − x + q²x²/4
  (the unfactored f; equal to exact_parts' factored one, N1), F′ = Fn′. The paper's N at μ is this function at
  q = q(μ), δ = δ(μ), x_H = 2/(1 + w(μ)) = 2/(1 + √(1 − q²)) (w ≥ 0 is the right branch).
- Conclusion: 0 ≤ ∫(‖φ′‖² + V(R(t))‖φ‖²) for C¹ compactly supported φ, V = Vrho = F U/(64ρ²H²) = fU₋/(64ρ²H₋²)
  (TARGET_HD §1): A_{ℓ,q(μ)} ≥ 0 on C₀^∞(ℝ).
q(μ): q2 = 1 − w², w = Bμ/A, A ≥ ℓ + n > 0 for all real μ, so w is C^∞ on [0, 1]; w(0) = 0, w(1) = 1, and
w′ = B((ℓ + n) − (ℓ − 1)μ²)/A² ≥ B(n + 1)/A² > 0 on [0, 1], so 0 ≤ w < 1 on [0, 1) and q(μ) = √(1 − w²) is
continuous on [0, 1], strictly decreasing, q(0) = 1, q(μ) < 1 for μ > 0. By the intermediate value theorem on
[0, MU1], every q ∈ [q(MU1), 1] is q(μ) for some μ ∈ [0, MU1]; q < 1 forces μ ≠ 0, so every q ∈ [q(MU1), 1) comes
from some μ ∈ (0, MU1] (monotonicity makes it unique but is not needed). Continuity, q(0) = 1 and q(MU1) < 1 suffice.
The PREREG's sentence "the image of [0, MU1] under the continuous q(μ), with q(0) = 1, contains [q(MU1), 1]" is this.

## N5. Item 5: the composition
HD-X-2 gives A_{ℓ,q} ≥ 0 for q ∈ [q(MU1), 1); Z gives q = 1 (Lean A_nonneg, every n ≥ 2, ℓ ≥ 2); Theorem HD gives
q ∈ (0, 99/100] (every ℓ ≥ 2, D = 7–11; q_max(D) = 99/100 for every D per code/hd/scert.py l.51 citing
TARGET_HD_ADDENDUM_1, and TARGET_HD_ADDENDUM_2 l.5–6). Union = (0, 1] iff q(MU1) ≤ 99/100: then q ∈ (0, 1) is either
≤ 99/100 or > 99/100 ≥ q(MU1). PARAM checks q(MU1)² ≤ (99/100)² = 0.9801 exactly; §3's table (information): the
largest is 46562824/47513449 (D = 10, ℓ = 3): 47513449 × 0.9801 = 46,567,931.4 > 46,562,824, so ≤ 0.9801 ✓; the
others are smaller. Spot check of a table value: D = 7 ℓ = 2, MU1 = 1/8: w = 8(1/8)/(7 + 1/64) = 64/449,
q² = 1 − 4096/201601 = 197505/201601 ✓ (table).
The partition of ℓ ≥ 2 per D (remark, §1 bullet 3): 𝒦 = {2ℓ ≤ n − 1}; HD-X-S = the 11 bands with 2ℓ > n − 1 and
ℓ ≤ n − 2; HD-X-E: n − 1 ≤ ℓ ≤ ℓ₀(D); Lemma U(n): ℓ > ℓ₀. D = 7: 2 | 3 | 4–10 | >10; D = 8: 2 | 3, 4 | 5–10 | >10;
D = 9: 2, 3 | 4, 5 | 6–11 | >11; D = 10: 2, 3 | 4, 5, 6 | 7–13 | >13; D = 11: 2, 3, 4 | 5, 6, 7 | 8–14 | >14. Complete.

## N6. INF at z = 1, from the definitions (information; consistency of the design with ν)
At z = 1: y = 0, R(1) = 1, f = 1, f_z(1) = 0 (y_z = −k(1 − z)^{k−1} = 0 for k ≥ 2), H = m, H_z(1) = 0, so
P(1, μ) = −ν + cμ and P_z(1, μ) = 0. N(1, μ) = U₋(x = 0) − 64m²(P² − P). From Lean's UmN at K = 1, y = 0 (l.542),
U₋(0) = 64m³ + 16n(n + 2)m² = 64m²(m + n(n + 2)/4), and m + n(n + 2)/4 = ν(ν + 1):
ν(ν + 1) = ℓ² + (n − 1)ℓ + n²/4 − n/2, m = ℓ² + (n − 1)ℓ − n, difference n(n + 2)/4 ✓. So
N(1, μ) = 64m²[ν(ν + 1) − (−ν + cμ)² + (−ν + cμ)] = 64m²[(2ν + 1)cμ − c²μ²], and NL(1, μ) = N S(1, μ)² R(1)² L =
64m²((2ν + 1)cμ − c²μ²) S(1, μ)² L(μ): the INF identity (PREREG §3; critical.py l.246). Positive for μ ∈ (0, MU1]
iff c > 0 and 2ν + 1 > c MU1 (2ν + 1 = 2ℓ + n − 1 ≥ 8 ≫ 13/400). N(1, 0) = 0 is u₀ ~ ρ^{−ν}: −ν is a root of
P² − P = ν(ν + 1) (the other is ν + 1). This uses U₋'s constant term from Lean's transcription, not re-checked
against S5 here.

## N7. THROAT re-derived (information; not among items 1–5, but the window the charts rest on)
Along z = μζ, μ → 0⁺. 1 − y = kμζ + O(μ²); 1 − k_r = 2w/(1 + w) = 2w₁μ + O(μ²); so
1 − k_r y = (1 − k_r) + k_r(1 − y) = μ(2w₁ + kζ) + O(μ²); f = (1 − y)(1 − k_r y) = kμ²ζ(kζ + 2w₁) + O(μ³);
f_z = (−y_z)[(1 − k_r y) + k_r(1 − y)] = 2kμ(kζ + w₁) + O(μ²) (y_z → −k).
P = −ℓy/((z + ε)R) + O(1) = −ℓ/(kμ(ζ + ε₁)) + O(1) (y, R/k → 1; ε = ε₁μ + O(μ²)); P_z = ℓ/(kμ²(ζ + ε₁)²) + O(1/μ).
In N = U − 64H²[(1 − z)f_z P + f(−P + (1 − z)P_z + P²)] the O(1) pieces as μ → 0 are
f_z P → −2ℓ(kζ + w₁)/(ζ + ε₁); f P_z → ℓζ(kζ + 2w₁)/(ζ + ε₁)²; f P² → ℓ²ζ(kζ + 2w₁)/(k(ζ + ε₁)²); f P → 0 and the
cross terms are O(μ). With U → U₋(2) = 64ℓ(ℓ − k)H(2)² (TARGET_HD_ADDENDUM_2 §3, G-RES) and H → H(2):
N₀(ζ) (ζ + ε₁)² / (64 H(2)² ℓ) = (ℓ − k)(ζ + ε₁)² + 2(kζ + w₁)(ζ + ε₁) − ζ(kζ + 2w₁)(k + ℓ)/k.
ζ²: (ℓ − k) + 2k − (k + ℓ) = 0 — T(ζ, 0) is linear in ζ, as THROAT and CORNER assume (gate_corner l.220 refuses
degree > 1). ζ¹: 2ε₁(ℓ − k) + 2(kε₁ + w₁) − 2w₁(k + ℓ)/k = 2ℓ(ε₁ − w₁/k) = 2ℓw₁(ε̂ − 1/k).
ζ⁰: ε₁[(ℓ − k)ε₁ + 2w₁] = ε̂w₁²[2 − (k − ℓ)ε̂].
S = ε_d(0) μ (ζ + ε₁) + O(μ²), R → k, L → L(0), so T(ζ, 0) = lim NL/μ² = N₀(ζ) ε_d(0)² (ζ + ε₁)² k² L(0):
  T(ζ, 0) = 64 k² H(2)² L(0) ε_d(0)² ℓ [2ℓ w₁ (ε̂ − 1/k) ζ + ε̂ w₁² (2 − (k − ℓ) ε̂)].
THROAT's form: 64k²H(2)²L(0)R(0)²ε_d(0)²w₁² β(ζ/w₁) with β(s) = 2a²(ε̂ − 1/k)s + aε̂((a + 1)ε̂ − 2/k), a = −ℓ/k:
R(0)² w₁² β(ζ/w₁) = k² w₁² [2(ℓ²/k²)(ε̂ − 1/k)ζ/w₁ + (ℓε̂/k²)(2 − (k − ℓ)ε̂)] = ℓ[2ℓw₁(ε̂ − 1/k)ζ + ε̂w₁²(2 − (k − ℓ)ε̂)]. ✓
Identical. So T₁ = 128 ℓ² k² H(2)² L(0) ε_d(0)² w₁ (ε̂ − 1/k) > 0 iff ε̂ > 1/k, and T₀ > 0 iff ε̂ < 2/(k − ℓ) (a + 1 =
(k − ℓ)/k > 0 since 2ℓ ≤ k on 𝒦). FIRST's K(0, 0) = C₀ ε_d(0)² R(0)² L(0), C₀ = 128H(2)²ℓ²w′(0)(ε̂ − 1/k), equals this T₁ ✓.
N₀(0) = 64H(2)²ℓ[2/ε̂ − (k − ℓ)] is the horizon value N(0, 0⁺) (f_z(0)P(0) → −2ℓ/ε̂), the same window's upper end.
The window (1/k, 2/(k − ℓ)) is non-empty for every ℓ, and ε̂ is its midpoint; table values 5/8, 13/30, 1/3, 5/12,
19/70, 9/28, 11/48, 21/80, 5/16 all re-computed ✓ (e.g. D = 8 ℓ = 2, k = 5: (1/5 + 2/3)/2 = 13/30).
Also checked: ν = 7/2 at D = 7 ℓ = 2; a = −1/2; ε = (5/8)·8μ/(7 + μ² + 8μ) = 5μ/(μ² + 8μ + 7) ✓ (table).
