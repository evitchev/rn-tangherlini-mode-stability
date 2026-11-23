# bh-modes pencil audit: HD-X-2's reduction and its chart cover (second audit; session-R secondary Fable)

*2026-11-13. Brief: `results/hdx/critical/briefs/BRIEF_fable_2026-11-13.md` (bh-modes repository), sha256
`243c712fae560056ffe5a007dbf2c131785bd6b66d5ce97ca0325b2bb66b9b14`, computed here with `sha256sum` at 11:30:59 EST and
equal to the hash in the session-R lead's cover message; `SEALED.sha256` not opened. A copy of the brief is
beside this file. Pencil audit: no computation was run anywhere (nothing on host-1 or host-2; on host-0 only reading,
`sha256sum` and writing in this folder). Nothing outside the brief's allow-list was opened: no `RESULT*.md`, no
`PREREG_ADDENDUM_*.md`, no `runs/`, `logs/`, `dev/` or `audits/` folder other than my own A3 folder, no `REGISTRY.md`,
`TODO.md`, `README.md`, `outbox/`, `paper/`, `SEALED.sha256`, nothing under `[deliveries]/` except this folder, no
`[kimi-folder]/`. Kimi's audit of this step was not seen. Seat time: 11:30:59 to the time in §10 (EST, from `date`).
Every derivation is in `AUDIT_notes.md` (N0–N7), written before this file.*

## 0. Verdicts

| Item | Object (PREREG §2 unless said) | Verdict |
|---|---|---|
| 1 | Smoothness of P for fixed μ ∈ (0, MU1]; sign of N from NL | **SOUND** |
| 2 | The three exact divisions; what closed-box positivity gives at each edge | **SOUND** |
| 3 | COVER: the case split from ZT·SIG1 = 1, ZT·MUT = Z1, Z1·SIG1 ≤ MU1 | **SOUND** |
| 4 | N > 0 ⟹ A_{ℓ,q(μ)} ≥ 0 by `prop3_Dn`; what the step needs of q(μ) | **SOUND** |
| 5 | The composition in §1: Z at q = 1, Theorem HD on (0, 99/100], q(MU1) ≤ 99/100 | **SOUND** |

Nothing is GAP-MINOR, GAP-MAJOR or ERROR. No fix is required; §7 lists five remarks at the level of one clause each,
none of which changes a claim. The verdicts are about the logic that turns the certified gates into the claim; they
are conditional on those gates (§8), whose outcomes are in files barred to me.

Beyond the five items, two consistency checks were done by pencil from the definitions (information, §6): the INF
identity at z = 1, and the THROAT limit T(ζ, 0), which comes out exactly as registered, including its linearity in ζ
and the two ends of the window on ε̂.

Notation: k = n − 1; ρ = r, units r_H = 1; z = 1 − 1/ρ; y = (1 − z)^k; x = x_H y; w = Bμ/A (param_n), x_H = 2/(1 + w),
k_r = (1 − w)/(1 + w); w₁ = w′(0), ε₁ = ε̂w₁. S, R, L, Π, D, NL as in PREREG §2.

## 1. Item 1 — smoothness and sign: SOUND

**P is analytic on a neighbourhood of [0, 1] for each fixed μ ∈ (0, MU1]** (so C^∞ on [0, 1] as §2 says, and C¹ on
(0, 1) as Proposition 3 needs). P(z, μ) = −ν − ℓy/((z + ε)R) − (1 − z)H_z/H + cμ is a rational function of z; its
poles (N1):
- z = −ε: gate S gives ε_n(0) = 0, ε_n/μ > 0 and ε_d > 0 on [0, MU1], so ε = ε_n/ε_d > 0 for μ > 0 and the pole is
  at −ε < 0. (At μ = 0 it sits at z = 0; the claim excludes μ = 0.)
- the zeros of R = (1 − (1 − z)^k)/z: these are 1 − z = e^{2πij/k}, j = 1, …, k − 1, so |1 − z| = 1 with z ≠ 0, as
  the PREREG says; none lies in [0, 1]. By pencil R = Σ_{j=0}^{k−1}(1 − z)^j ≥ 1 on [0, 1] (gate R certifies R > 0).
- the zeros of H = m + (n(n + 1)/2)(1 + mδ)x_H y: m = (ℓ − 1)(ℓ + n) > 0, δ(μ) > 0 on [0, MU1] (gate H; by pencil
  δ > 0 ⟺ μ² < 1), x_H > 0, y ≥ 0 on [0, 1], so H ≥ m > 0 on [0, 1]; the zero is at y < 0, i.e. real z > 1 or complex.

**The identity NL = N S² R² L** (defined in §2 and displayed as a polynomial; the equality is not written out in the
PREREG, so it was derived, N1): with D = S R Hn and Π = P D a polynomial (the code's `Pi`, `critical.py` l.159–160,
is exactly (−ν + cμ)SRHn − ℓε_d y Hn − (1 − z)Hn_z S R), P = Π/D, P_z = (Π_z D − Π D_z)/D², the bracket of N equals
B/(fd D²) with B = (1 − z)fzn Π D + fn(−Π D + (1 − z)(Π_z D − Π D_z) + Π²), and
N·Ud Hd² fd D² = Un Hd² fd D² − 64 Ud Hn² B. Since D² = S² R² Hn², dividing by Hn² gives N·L·S²R² = Un Hd² fd S²R² −
64 Ud B, the displayed NL, with L = Ud Hd² fd. The identity holds wherever N is defined, i.e. on [0, 1] × (0, MU1]
given gates S, R, H (poles) and L (Ud, Hd, fd ≠ 0). The factored f of `exact_parts` equals S5's 1 − x + q²x²/4 (N1).

**Sign.** For μ ∈ (0, MU1] and z ∈ [0, 1]: S = ε_d z + ε_n > 0 (both coefficients positive for μ > 0), R ≥ 1, L > 0
(gate L; L depends on μ only). So S²R²L > 0 and N has the sign of NL; in particular NL > 0 on (0, 1) gives N > 0
there. Only S ≠ 0, R ≠ 0 and L > 0 enter; the gates give more. SOUND.

## 2. Item 2 — the divisions: SOUND

Write NL = Σ c_{ij} z^i μ^j (N2).
- **M = NL/μ** exists iff every monomial has j ≥ 1 iff NL(z, 0) ≡ 0: DIV-O is Z0. Then NL = μM identically.
- **T = NL(μζ, μ)/μ²**: NL(μζ, μ) = Σ c_{ij} ζ^i μ^{i+j}, and (i, j) ↦ (i, i + j) is injective, so the code's
  accumulation (`charts`, l.175) has one term per key and no cancellation; the division is exact iff every monomial has
  i + j ≥ 2 (l.179). Then μ² T(z/μ, μ) = NL(z, μ) for μ ≠ 0.
- **K = NL(z, zσ)/(z²σ)**: (i, j) ↦ (i + j, j) is injective; exact iff i + j ≥ 2 and j ≥ 1 (l.180), so DIV-C ⟺
  DIV-O ∧ DIV-T. Then z²σ K(z, μ/z) = NL(z, μ) for z ≠ 0. Given Z0, both DIV-T and DIV-C say c_{01} = 0, i.e.
  M(0, 0) = 0, FIRST's first part.

**What positivity on the closed box gives.** With M > 0 on O = [1/4, 1] × [0, MU1] and on O′ = [0, 1/4] ×
[1/32, MU1], NL = μM > 0 at every point with μ > 0. With T > 0 on [0, 8] × [0, 1/32], NL = μ²T(z/μ, μ) > 0 at every
(z, μ) with μ > 0 and z/μ ∈ [0, 8]. With K > 0 on [0, 1/4] × [0, 1/8], NL = z²σK > 0 at every (z, μ) with z > 0 and
μ/z ∈ (0, 1/8]; in that chart μ > 0 forces z > 0. So the brief's sentence holds as stated: positivity of M, T or K on
its closed box gives NL > 0 at every point of the chart with μ > 0.

**The edges** (N2), none of which the claim needs:
| edge | what the certificate says there | needed? |
|---|---|---|
| μ = 0 in O | NL ≡ 0; M(z, 0) = ∂_μNL(z, 0) > 0, i.e. NL > 0 for small μ > 0 | no (q = 1 is Z's) |
| z = 0 in O′; ζ = 0 in T | NL(0, μ) = μM(0, μ) = μ²T(0, μ) > 0: N(0, μ) > 0 at the horizon | no (Proposition 3 uses (0, 1)) |
| μ = 0 in T | T(ζ, 0) = T₁ζ + T₀, the second-order jet of NL at the corner along z = ζμ | no for the claim; a necessary condition for a strict certificate on the closed box: the design window (§6) |
| z = 0 in C | K(0, σ) = c_{11} + c_{02}σ = T₁ + T₀σ, the blown-up corner (CORNER) | no |
| σ = 0 in C | K(z, 0) = M(z, 0)/z (since NL(z, zσ) = zσ M(z, zσ)); K(0, 0) = M_z(0, 0) = c_{11} = T₁ (FIRST) | no |
| z = 1 in O | spatial infinity; M(1, μ) = 64m²c(2ν + 1 − cμ)S(1, μ)²L(μ) > 0 (INF, §6) | no |

The boundaries between charts (z = 1/4; μ = 1/32; z = 8μ, which is ζ = 8 in T and σ = 1/8 in C) are points of
(0, 1) × (0, MU1] and are covered because the boxes are closed; either neighbouring chart serves. The claim uses NL > 0
on the open set (0, 1) × (0, MU1] only; the certificates prove it on the closed rectangle [0, 1] × [0, MU1], with the
corner (0, 0) blown up and the μ = 0 edge divided out. The identities T(ζ, 0) = c_{02} + c_{11}ζ, M_z(0, 0) = c_{11}
and K(0, σ) = c_{11} + c_{02}σ are exponent bookkeeping once the divisions are exact; CORNER and the structural half of
FIRST test the implementation, and only the values T₀, T₁ carry content (§6). SOUND.

## 3. Item 3 — COVER: SOUND

Z1 = 1/4, ZT = 8, SIG1 = 1/8, MUT = 1/32 (`critical.py` l.99), MU1 ∈ {1/8, 13/100, 3/25} (l.96–97). ZT·SIG1 = 1;
ZT·MUT = 1/4 = Z1; Z1·SIG1 = 1/32 = MUT ≤ MU1 (the least MU1 is 3/25). The case split (N3), for
(z, μ) ∈ (0, 1) × (0, MU1]:
1. z ≥ 1/4 → O (needs Z1 < 1).
2. z < 1/4, μ ≥ 1/32 → O′ (needs MUT ≤ MU1; this is Z1·SIG1 ≤ MU1, since Z1·SIG1 = MUT when ZT·SIG1 = 1).
3. z < 1/4, μ < 1/32, z ≤ 8μ → ζ = z/μ ∈ (0, 8], (ζ, μ) ∈ T's box. ZT·MUT ≤ Z1 keeps T's image inside z ≤ 1/4, so
   the PREREG's "z ≤ 8μ < 1/4" is consistent and the T certificate asks nothing beyond z = 1/4.
4. z < 1/4, μ < 1/32, z > 8μ → σ = μ/z < 1/8, (z, σ) ∈ C's box; this is the one place ZT·SIG1 ≥ 1 is used. Here
   μ < 1/32 is automatic (μ < z/8 < 1/32). Z1·SIG1 ≤ MU1 keeps C's image inside μ ≤ MU1.
The four cases are exhaustive and each lands in a closed box where the corresponding polynomial is certified positive,
so NL > 0 at every point of (0, 1) × (0, MU1]. The images of the four boxes are O, O′, {0 ≤ z ≤ 8μ, μ ≤ 1/32} and
{0 ≤ μ ≤ z/8, z ≤ 1/4}, whose union is [0, 1] × [0, MU1], as the code's docstring says (l.17). The code's COVER
(l.452) checks the three products and the two ranges 0 < MUT < MU1 and 0 < Z1 < 1; the PREREG's text lists the
products (remark R1). SOUND.

## 4. Item 4 — from N > 0 to the claim: SOUND

`prop3_Dn` (`lean/lean_p3_sdeformation_v5_2026-10-24/lean/BHModesP3.lean` l.638–644; read as a statement, proof not
re-checked) has the hypotheses n ≥ 2; q² ≤ 1; m > 0; δ ≥ 0; P with derivative P′ on (0, 1) and P′ continuous on (0, 1);
R : ℝ → ℝ with R′(t) = Fn n q (zc (R t)) and R(t) > 1 for every t; N ≥ 0 on (0, 1), with N = `Nz` (l.173–174, METHOD.md's
N) built from `Un` = S5's U₋ (`UmN` at K = 1, y = 0, l.533–542, 555), `Hn` = H₋ (`HmN`, l.530, 553), `Fn` = 1 − x +
q²x²/4 and `Fn′` (l.548–551) at x = x_H(q)(1 − z)^{n−1}, x_H = 2/(1 + √(1 − q²)) (l.273). Its conclusion is the
quadratic form with V = `Vrho` = fU₋/(64ρ²H₋²) composed with R (TARGET_HD §1's V_{ℓ,q} in r*), nonnegative on C¹
compactly supported φ, hence on C₀^∞(ℝ): A_{ℓ,q} ≥ 0. At each fixed μ ∈ (0, MU1] (N4):
- q = q(μ) with q² = 1 − w² ∈ (0, 1) ✓; m = (ℓ − 1)(ℓ + n) > 0 ✓; δ = δ(μ) > 0 (gate H; pencil in N1), and it is S5's
  δ: PARAM's identity s² = 1 + 4mq²/(n + 1)² with s = 1 + 2mδ, on the branch s > 0 (param_n's s is manifestly > 0 on
  [0, 1]) ✓; x_H(μ) = 2/(1 + w) with w = √(1 − q²) ≥ 0, the branch Lean takes ✓. So Lean's N at (q(μ), m, δ(μ)) is the
  paper's N(·, μ), with Lean's unfactored f equal to `exact_parts`' factored one (N1).
- P(·, μ) is analytic near [0, 1] (item 1): hP and hP′ hold.
- hR, hR1: R is the inverse tortoise map ρ(r*), with dρ/dr* = f(ρ) and ρ > 1. For 0 < q < 1, f = (1 − y)(1 − k_r y) > 0
  on (1, ∞) with 0 < k_r < 1, f has a simple zero at ρ = 1 (f_z(0) = k(1 − k_r) > 0) and f → 1 at infinity, so
  r* = ∫dρ/f is a C^∞ increasing bijection (1, ∞) → ℝ and R = (r*)^{−1} satisfies both hypotheses (pencil; my A2 of
  2026-10-26, re-derived there). This is the step that needs q < 1, and q(μ) < 1 holds for every μ > 0 because
  w = Bμ/A > 0 there. (At q = 1 the zero of f is double; `tortoise_q1` covers it, but HD-X-2 never uses q = 1.)
- hN: N(z, μ) > 0 on (0, 1) by items 1–3, given the certified charts.
So A_{ℓ,q(μ)} ≥ 0 for every μ ∈ (0, MU1].

**q(μ).** w = Bμ/A is C^∞ on [0, 1] (A ≥ ℓ + n > 0), w(0) = 0, w(1) = 1, w′ = B((ℓ + n) − (ℓ − 1)μ²)/A² > 0 on [0, 1]
(PARAM certifies w increasing), so 0 ≤ w < 1 on [0, 1) and q(μ) = √(1 − w²) is continuous and strictly decreasing on
[0, 1] with q(0) = 1 and q(μ) < 1 for μ > 0. By the intermediate value theorem on [0, MU1], the image of [0, MU1]
contains [q(MU1), 1], as §2 says; a q < 1 cannot come from μ = 0, so every q ∈ [q(MU1), 1) is q(μ) for some
μ ∈ (0, MU1] (uniquely, by monotonicity, though only continuity, q(0) = 1 and q(MU1) < 1 are needed). The step therefore
needs of q(μ): continuity on [0, MU1] (from 0 ≤ w < 1 there); q(0) = 1 (w(0) = 0); q(μ) < 1 for μ > 0 (w > 0) where
the q < 1 tortoise map is invoked; and nothing else. All hold. SOUND.

## 5. Item 5 — the composition in §1: SOUND

For a band of 𝒦: HD-X-2 gives A_{ℓ,q} ≥ 0 on [q(MU1), 1); Z gives q = 1 (`A_nonneg`, `lean_z_d_2026-10-26`, every
n ≥ 2 and ℓ ≥ 2); Theorem HD gives (0, 99/100] for every ℓ ≥ 2 and D = 7–11 (q_max(D) = 99/100 for every D:
`code/hd/scert.py` l.51 citing TARGET_HD_ADDENDUM_1, and TARGET_HD_ADDENDUM_2 l.5–6, "Theorem HD stays as stated, for
q ≤ 99/100"). The union is (0, 1] iff q(MU1) ≤ 99/100: any q ∈ (0, 1) is either ≤ 99/100 or > 99/100 ≥ q(MU1). PARAM
checks q(MU1)² ≤ (99/100)² exactly (`critical.py` l.410, 418). §3's table (information): the largest value,
46562824/47513449 at D = 10 ℓ = 3, is below 0.9801 (47513449 × 0.9801 = 46,567,931.4 > 46,562,824); the entry for
D = 7 ℓ = 2 re-computed from MU1 = 1/8: w = 64/449, q² = 197505/201601 ✓. Each of the three pieces is a statement about
the same operator A_{ℓ,q} = −d²/dr*² + fU₋/(64r²H₋²) on C₀^∞(ℝ) (TARGET_HD §1; Lean's `Vrho` and `Vr_S5`). So every
q ∈ (0, 1] is covered for each band of 𝒦. Remark: §1's third bullet (HD-X outside 𝒦) partitions ℓ ≥ 2 completely at
each D (N5): 𝒦 | the 11 HD-X-S bands | HD-X-E's n − 1 ≤ ℓ ≤ ℓ₀(D) | Lemma U(n). SOUND, with Theorem HD, Z, HD-X-E,
HD-X-S and Lemma U(n) taken as hypotheses (§8).

## 6. Two cross-checks from the definitions (information)

- **INF** (N6). At z = 1: y = 0, R(1) = 1, f = 1, f_z = 0, H = m, H_z = 0, P(1, μ) = −ν + cμ, P_z(1, μ) = 0. From Lean's
  `UmN` at K = 1, y = 0, U₋(x = 0) = 64m³ + 16n(n + 2)m² = 64m²ν(ν + 1) (the algebra m + n(n + 2)/4 = ν(ν + 1) holds
  identically in ℓ, n). So N(1, μ) = 64m²[(2ν + 1)cμ − c²μ²] and NL(1, μ) = 64m²((2ν + 1)cμ − c²μ²)S(1, μ)²L(μ),
  the registered identity; positive on (0, MU1] iff c > 0 and 2ν + 1 > c·MU1. N(1, 0) = 0 says −ν is a root of
  P² − P = ν(ν + 1), i.e. u₀ ~ ρ^{−ν} is the decaying solution at infinity, as the design intends.
- **THROAT** (N7). Along z = μζ, μ → 0⁺: f = kμ²ζ(kζ + 2w₁) + O(μ³), f_z = 2kμ(kζ + w₁) + O(μ²), P = −ℓ/(kμ(ζ + ε₁)) +
  O(1), P_z = ℓ/(kμ²(ζ + ε₁)²) + O(1/μ). The O(1) part of N along the ray, N₀(ζ), times (ζ + ε₁)², is
  64H(2)²ℓ[(ℓ − k)(ζ + ε₁)² + 2(kζ + w₁)(ζ + ε₁) − ζ(kζ + 2w₁)(k + ℓ)/k], using U₋(2) = 64ℓ(ℓ − k)H(2)² at q = 1
  (TARGET_HD_ADDENDUM_2 §3). The ζ² coefficient is (ℓ − k) + 2k − (k + ℓ) = 0, so T(ζ, 0) is linear in ζ, as THROAT
  and CORNER assume (`gate_corner` refuses degree > 1). With S = ε_d(0)μ(ζ + ε₁) + O(μ²), R(0) = k, L(0):
  T(ζ, 0) = 64k²H(2)²L(0)ε_d(0)²ℓ[2ℓw₁(ε̂ − 1/k)ζ + ε̂w₁²(2 − (k − ℓ)ε̂)], which is exactly the registered
  64k²H(2)²L(0)R(0)²ε_d(0)²w′(0)²β(ζ/w′(0)) with β(s) = 2a²(ε̂ − 1/k)s + aε̂((a + 1)ε̂ − 2/k), a = −ℓ/k. Hence T₁ > 0 iff
  ε̂ > 1/k and T₀ > 0 iff ε̂ < 2/(k − ℓ) (a + 1 = (k − ℓ)/k > 0 on 𝒦), PREREG l.100; T₁ equals FIRST's
  C₀ε_d(0)²R(0)²L(0) with C₀ = 128H(2)²ℓ²w′(0)(ε̂ − 1/k); and T₀ is N(0, 0⁺)·ε_n′(0)²R(0)²L(0) with
  N(0, 0⁺) = 64H(2)²ℓ[2/ε̂ − (k − ℓ)]. The nine ε̂ values of §3's table are the midpoints of the windows (re-computed).

Neither check is among items 1–5; they confirm that the pencil statements the gates test are the right ones.

## 7. Remarks (no change to any claim; each is one clause if adopted)

- **R1 (§2, COVER).** The text derives the cover from the three products; the split also uses 0 < Z1 < 1 and
  MUT ≤ MU1 (the latter is the third product, since Z1·SIG1 = MUT when ZT·SIG1 = 1). The code checks both ranges
  (`critical.py` l.452). The only inequality beyond the ranges that the split needs is ZT·SIG1 ≥ 1; ZT·MUT ≤ Z1 and
  Z1·SIG1 ≤ MU1 bound the images of T and C inside the rectangle (so the certificates ask for positivity only where N is
  defined and claimed). As in my A3 remark on HD-X-S.
- **R2 (§2, the reduction).** "The continuous q(μ)" rests on 0 ≤ w < 1 on [0, MU1] (w increasing, w(1) = 1, PARAM),
  and "q(μ) < 1" on w > 0 for μ > 0. Both are immediate from w = Bμ/A; a clause would make the sentence self-contained.
- **R3 (§2, NL).** NL is defined as N S²R²L and displayed as a polynomial; the equality is two lines of algebra (§1),
  not written in the PREREG or in HD-X-S's. The XN gate tests it at 27 rational points, a spot check; the identity could
  also be certified exactly per band with one symbolic cancellation (degrees ≤ (60, 14)), at small cost. The pencil
  identity above is what the reduction rests on.
- **R4 (§2, the sign).** "S, R and L are > 0" is more than the sign needs (S ≠ 0, R ≠ 0, L > 0); harmless.
- **R5 (§2, smoothness).** P is analytic on a neighbourhood of [0, 1]; "C^∞ on [0, 1]" is correct and Proposition 3
  needs only C¹ on (0, 1). Harmless.

## 8. Hypotheses assumed

1. **The certified gates and charts of HD-X-2 ran and passed** on each band: KAT, E0n, PARAM, H, S, R, L, COVER, Z0,
   DIV-O/T/C, THROAT, CORNER, FIRST, INF, XN, POS-O/O′/T/C (`critical.py` as read, at the commit of the PREREG). The
   brief excludes re-running them; their outcomes are in barred `RESULT*.md` files. The verdicts above are about the
   logic that turns them into the claim, and hold for every band whose `none` job is VERIFIED.
2. **S5's transcription.** `Un`/`Hn` in Lean (`UmN`, `HmN`) and `U_minus`/`H_minus` in `code/ki/potentials.py` (not on
   this allow-list) are S5's (5.63b), (5.62b); E0n and the Lean oracle checks are the evidence, not re-done here. Used
   in items 4–5 (the Lean N is the paper's N) and in §6 (the constant term of U₋; U₋(2) = 64ℓ(ℓ − n + 1)H₋(2)² at q = 1,
   TARGET_HD_ADDENDUM_2 §3, G-RES).
3. **Lean statements as read, proofs not re-checked, builds not re-run:** `prop3_Dn`, `prop3_Ioo`, `Nz`, `Vrho`
   (BHModesP3.lean), `tortoise_q1`, `A_nonneg` (BHModesZd.lean, via its README).
4. **The tortoise map for 0 < q < 1** at general n: pencil (my A2, 2026-10-26), restated in §4.
5. **For item 5:** Theorem HD on (0, 99/100] for every ℓ ≥ 2 and D = 7–11, with q_max(D) = 99/100 for every D
   (TARGET_HD_ADDENDUM_1 is not on the allow-list; `code/hd/scert.py` l.51 and TARGET_HD_ADDENDUM_2 l.5–6 record it);
   Z at q = 1 (BHM-126, `A_nonneg`); HD-X-E, HD-X-S and Lemma U(n) for the bands outside 𝒦.
6. The brief's description of the item matches the files read (it does).

## 9. Files and line ranges read, per item (bh-modes repository paths)

- **Item 1:** `results/hdx/critical/PREREG.md` l.1–33 (header, claim), 34–56 (design, NL), 69–77 (reduction), 79–98
  (gates); `code/hdx/critical.py` l.1–67 (docstring), 87–105 (constants), 127–165 (`design`, `build`), 253–279
  (`direct_N`, `gate_xn`), 404–450 (gates PARAM, H, S, R, L); `code/hd/scert.py` l.131–183 (`ratpoly`, `exact_parts`,
  `Exact.NL`); `code/hd/elementary.py` l.70–78 (`param_n`); `results/p3/METHOD.md` l.19–38; `METHOD_ADDENDUM_2.md`
  l.13–53; `METHOD_ADDENDUM_3.md` l.9–49.
- **Item 2:** `PREREG.md` l.57–67 (charts), 91–100 (Z0, DIV, THROAT, CORNER, FIRST, INF, the window), 104–117
  (table); `critical.py` l.168–192 (`charts`, `edge`), 195–251 (`throat_data`, `gate_throat`, `gate_corner`,
  `gate_first`, `gate_inf`), 458–488 (Z0, DIV, degrees), 495–508 (the four boxes).
- **Item 3:** `PREREG.md` l.59–67, 116–117; `critical.py` l.17–22, 94–101, 451–453; my A3 audit
  `results/stage3/audits/fable_2026-10-26/AUDIT.md` l.118–137 (§A3 (ii)).
- **Item 4:** `PREREG.md` l.69–77, 85; `lean/lean_p3_sdeformation_v5_2026-10-24/lean/BHModesP3.lean` l.173–200 (`Nz`,
  `ansatz_identity`, `Vrho`, `Srho`), 403–411 (`prop3_Ioo`), 528–555 (`HmN`, `UmN`, `xn`, `Fn`, `Fn′`, `Hn`, `Un`),
  636–666 (`prop3_Dn`, `prop3_Dn_zeta`), and the list of `theorem`/`def` lines; `lean/lean_p3_sdeformation_v5_2026-10-24/
  README.md` (all); `lean/lean_z_d_2026-10-26/README.md` (all; `tortoise_q1` l.42–51, `A_nonneg` l.80–89);
  `code/hd/elementary.py` l.70–78, 106–141; `critical.py` l.404–420; `TARGET_HD.md` l.9–23; `METHOD_ADDENDUM_2.md`
  l.24–38; my A3 audit l.60–89 (§A2).
- **Item 5:** `PREREG.md` l.22–32, 85, 102–117, 203–219 (§7); `TARGET_HD.md` l.25–31, 61–75; `TARGET_HD_ADDENDUM_2.md`
  l.1–22, 24–48; `results/hdx/s/PREREG.md` l.11–18, 39–42; `code/hd/scert.py` l.51; `critical.py` l.94–97;
  `lean/lean_z_d_2026-10-26/README.md` l.80–99.
- **Context:** `results/hdx/critical/PREREG.md` all 219 lines; `results/hdx/s/PREREG.md` all; `TARGET.md` all;
  `TARGET_HD.md` all; `TARGET_HD_ADDENDUM_2.md` all; `CHARTER.md` §5 (l.101–122); `RULES.md` §B (l.76–120);
  `results/p3/METHOD.md` and addenda 1–3 all; `code/hd/elementary.py`, `code/hd/scert.py`, `code/hdx/critical.py`
  all; my A3 audit all.

## 10. Process and time

- Start 11:30:59 EST (brief hash computed); the derivation notes finished 11:46:41 EST; this file written next. End
  time: see `STATE_LOG.md`'s last entry and the delivery message (from `date`). Inside the two-hour box; no stop
  condition was reached.
- No process run on any host; no external contact; nothing written outside this folder; no git.
- Files here: `AUDIT.md` (this), `AUDIT_notes.md` (N0–N7, written first), `BRIEF_fable_2026-11-13.md` (a 0444 copy
  of the brief, same sha256), `STATE.md`, `STATE_LOG.md`, `MESSAGES.md` (the last three evolve and are excluded from
  `SHA256SUMS`, which lists every other file).
