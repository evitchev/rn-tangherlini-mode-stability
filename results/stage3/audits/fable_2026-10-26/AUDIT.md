# bh-modes stage-2/3 pencil audit (second party: session-R secondary Fable)

*2026-10-26. Brief: `results/stage3/briefs/BRIEF_fable_2026-10-26.md`, sha256
`e45fdde0881d702a239ade57ee48bc649f9b7c0dcac35216630f87c245b73c34` (quoted from the lead's message; `SEALED.sha256` not
opened). Pencil audit; no process was run anywhere (nothing on host-0, host-1 or host-2); no file outside the brief's
allow-list was opened (no RESULT*.md, runs/, logs/, audits/, REGISTRY.md, TODO.md, README.md, outbox/, SEALED.sha256,
[deliveries]/ other than this folder, [kimi-folder]/). Lean files were read for their theorem statements only.
Seat time about one hour (about 21:20 to 22:25 EDT), inside the six-hour box; Part A first, then Part B. Working notes
with every derivation: `AUDIT_notes_A1.md`, `AUDIT_notes_A2_A3.md`, `AUDIT_notes_B.md` (written before this file).*

## 0. Verdicts

| Item | Object | Verdict |
|---|---|---|
| A1 | Lemma U(n), `results/hd/elementary/PREREG.md` §3 Part II (a)-(d) | **SOUND** |
| A2 | Proposition 3 at general n; R for 0 < q < 1; the ζ-design branch (`results/p3/METHOD.md`, addenda 1 §1 and 2) | **SOUND** |
| A3 | The singular-design reduction and the four charts (`TARGET_A2_ADDENDUM_1.md` §3, `results/a2/s/PREREG.md`; `TARGET_HD_ADDENDUM_2.md` §3, `results/hdx/s/PREREG.md`) | **SOUND** (cover and reduction); **GAP-MINOR** (wording at μ = 0, fix in §A3) |
| B1 | The Darboux intertwiner at q = 1 (`results/extremal/PREREG.md` §2) | **GAP-MINOR** (the sector statement at the extremal horizon is not argued; fix in §B1) |
| B2 | Lemma R (`[a note of another line of this project]` §2) | **SOUND** |
| B3 | The functional relations at q = 1 (`[a note of another line of this project]`; `results/planning/kimaster_fr_2026-10-26/NOTE.md` §§1-3) | **SOUND** as pencil statements, conventions named in §B3 |

**Part A overall: SOUND.** Every step re-derived by hand closes; the one gap is a wording gap (the pencil form of
Proposition 3 cited for the singular design needs the hypothesis "P ∈ C¹(0, 1)", which Lean's `prop3_Ioo`/`prop3_Dn`
already have and the pencil proof supports unchanged). No claim changes.

**Part B overall: SOUND with one GAP-MINOR.** B1's written argument shows w → 0 along the real axis only, while the
quasinormal-mode condition at the extremal horizon for Im ω < 0 is a recessiveness condition in a complex sector; the
missing sentence (w is analytic at ρ = 1 with a simple zero) is supplied below and closes it, together with the
Wronskian identity W[Lψ₁, Lψ₂] = ω²W[ψ₁, ψ₂], which gives D_Ṽ ≡ D_V. No claim changes. Nothing is ERROR or GAP-MAJOR.

Notation below: k = n − 1; units r_H = 1; ρ = r; z = 1 − 1/ρ; Y = ρ^{−k}; x = 2Y at q = 1; ′ = d/dr* unless said.

## Part A

### A1. Lemma U(n), general n (D = 7-11): SOUND

What was checked, from `results/hd/elementary/PREREG.md` §2 E3 and §3 Part II, with U₋(n) of `code/ki/potentials.py`
(S5 (5.63b), y = 0).

- **The scaling.** With m = ε⁻², δ = κε, a monomial m^a δ^b x^c of U₋ becomes ε^{b−2a} κ^b x^c, and ε⁶ times it is
  ε^{6−2a+b}. The highest power of m in U₋ is m³, in the constant term 64m³ and in the terms m³δ^b (b = 1, …, 4, one per
  power of x). So every exponent of ε is ≥ 0: ε⁶U₋ is a polynomial in (ε, κ, x), and its ε⁰ part is exactly the
  constant 64. Hence Pos_n(0) = 64 means "at ε = 0 for every (κ, x)", which the degree count justifies; the text could
  say so in one clause. The split by the sign of each coefficient is unique, so Pos_n and Neg_n have nonnegative
  coefficients by construction.
- **(a)** (1 + 2mδ)² = 1 + 4mq²/(n + 1)² gives δ + mδ² = q²/(n + 1)² on the branch δ ≥ 0, so κ² = mδ² ≤ δ + mδ² ≤
  1/(n + 1)² for q ∈ [0, 1], including q = 1: κ ≤ 1/(n + 1).
- **(b)** x ∈ [0, x_H] with x_H = 2/(1 + √(1 − q²)) ≤ 2; the lemma is stated on [0, 2] directly.
- **(c)** m(ℓ) = (ℓ − 1)(ℓ + n) increases for ℓ ≥ 1, so ℓ > ℓ₀ gives m ≥ m(ℓ₀ + 1) and ε = m^{−1/2} ≤ 1/√m(ℓ₀ + 1) ≤
  1/isqrt(m(ℓ₀ + 1)) = ε̄ (rational, uniform in q and x).
- **(d)** A polynomial with nonnegative coefficients is nondecreasing in each variable on [0, ∞), so Neg_n(ε, κ, x) ≤
  Neg_n(ε̄, 1/(n + 1), 2), the corner value, and Pos_n ≥ Pos_n(0, κ, x) ≥ 64.
- **The chain.** U₋ = m³ε⁶U₋ = m³(Pos_n − Neg_n) ≥ m³(64 − Neg_n(ε̄, 1/(n + 1), 2)); the lemma holds wherever that number
  is > 0, which is what the machine certifies at the found ℓ₀(n). With f > 0 on the exterior and H₋ = m +
  n(n + 1)(1 + mδ)x/2 ≥ m > 0, V_S− has the sign of U₋.

Hypotheses assumed: the certified corner value > 0 at ℓ₀(n) (machine; not re-run); the transcription gate E0n; ℓ₀(n) is a
bound found by search, not a sharp threshold (the text says so).

### A2. Proposition 3 at general n; R for 0 < q < 1; the ζ-design branch: SOUND

- **Lemma 1** re-derived: |φ′ + Sφ|² = |φ′|² + S(|φ|²)′ + S²|φ|² for S real, and ∫S(|φ|²)′ = −∫S′|φ|² with no boundary
  term. It needs only S ∈ C¹(ℝ) real and V continuous.
- **Lemma 2** re-derived: dz/dρ = (1 − z)², d/dr* = f d/dρ, S = −fβ, so Ṽ = f[W − f_ρβ − f(β_ρ + β²)]; with β = (1 − z)P,
  f_ρ = (1 − z)²f_z, β_ρ = (1 − z)²(−P + (1 − z)P_z) and ρ²(1 − z)² = 1, the four products are (1 − z)f_zP,
  f(−P + (1 − z)P_z), fP² and U₋/(64H₋²). Ṽ = fN/(64ρ²H₋²) with N as written; no step uses n. The endpoint remark
  N(1) = 64m²(m + 6 − P(1)² + P(1)) at n = 4 and the window −3 < P(1) < 4 at ℓ = 2 (m = 6) check.
- **R for 0 < q < 1 at general n.** f = 1 − x + q²x²/4 = (1 − x/x_H)(1 − x/x₋) with x_{H,∓} = 2/(1 ∓ w), w = √(1 − q²),
  and x = x_H(1 − z)^k in units r_H = 1, so f = (1 − y)(1 − ky), y = ρ^{−k} ∈ (0, 1), k_ratio = x_H/x₋ = (1 − w)/(1 + w)
  ∈ [0, 1). f > 0 and C^∞ on (1, ∞); r*(ρ) = ∫dρ/f is C^∞ and strictly increasing with derivative 1/f > 0, so its inverse
  R is C^∞ (inverse function theorem, f(R) ≠ 0). Onto ℝ: 1/f → 1 at infinity (divergent integral); at the horizon
  f = (n − 1)(1 − k_ratio)(ρ − 1) + O((ρ − 1)²), a simple zero (f_z(0) = (n − 1)(1 − k_ratio) > 0 checked), so the
  integral diverges logarithmically. At q = 1 the zero is double, f ~ (n − 1)²(ρ − 1)², divergence like 1/(ρ − 1)
  (coefficient 1/9 at n = 4: TARGET_A2's E2). Addendum 2's steps 1, 2 are correct at every n ≥ 2.
- **Steps 3-5 of addendum 2.** S ∈ C¹(ℝ) because z∘R maps ℝ smoothly into (0, 1), where P is C¹: the proof uses P on
  (0, 1) only, so the hypothesis "C¹ on an open interval containing [0, 1]" is stronger than needed (see A3). H₋ ≥ m > 0
  needs δ ≥ 0, which the branch 1 + 2mδ > 0 gives. Lean's `prop3_Dn` (read: hypotheses `hP : ∀ z ∈ Ioo 0 1, HasDerivAt
  P (P' z) z`, `hR : ∀ t, HasDerivAt R (Fn n q (zc (R t))) t`, `hR1 : ∀ t, 1 < R t`) takes exactly R's existence as a
  hypothesis, which the pencil above supplies for 0 < q < 1 and `tortoise_q1` supplies at q = 1.
- **The ζ-design (Möbius) branch.** P = P̂/(z + δ_b)^d, δ_b > 0: C^∞ on (−δ_b, ∞) ⊃ [0, 1]; the pole is outside. N contains
  P, P_z, P² with denominators (z + δ_b)^d, (z + δ_b)^{d+1}, (z + δ_b)^{2d}; since 2d ≥ d + 1 for d ≥ 1, (z + δ_b)^{2d}N
  is a polynomial (the addendum does not say why; one clause). The certificate's N·L·(z + δ_b)^{2d} > 0 with L > 0 gives
  N > 0 on [0, 1], more than Proposition 3 needs. Lean's `prop3_Dn_zeta` has δ_b ≥ 0 and derives the (0, 1)
  differentiability from z > 0, consistent.
- Notation: addendum 2's w = √(1 − q²) equals TARGET_HD §1's w = Bμ/A by PARAM; its k = x_H/x₋ is METHOD_ADDENDUM_1's
  κ³ at n = 4; the brief's n − 1 is called k in B3's sources. No conflict, but three symbols for two ratios.

Hypotheses assumed: S5's reduction and transcription (the trust base of addendum 1 §3; Kimi's and session-L's checks
are in barred folders and were not opened); Lean statements read, proofs not re-checked.

### A3. The singular-design reduction and the four charts: SOUND; GAP-MINOR (wording at μ = 0)

- **The pole ansatz at general n, q = 1** (gate G-RES), re-derived: f = (1 − (1 − z)^k)² = k²z² + O(z³),
  f_z = 2k²z + O(z²); with P = a/z + p, p ∈ C¹ at 0, the bracket (1 − z)f_zP + f(−P + (1 − z)P_z + P²) at z = 0 is
  2k²a − k²a + k²a² = k²a(a + 1). So N(0) = U₋(2) − 64k²H₋(2)²a(a + 1) = 64k²H₋(2)²(c − a(a + 1)) with
  c = U₋(2)/(64k²H₋(2)²), E3's c at n = 4 (576 = 64·9). Window: c − a(a + 1) > 0 iff a ∈ (−1/2 − ν, −1/2 + ν),
  ν = √(c + 1/4) = |2ℓ − n + 1|/(2k) for c = ℓ(ℓ − n + 1)/k²; for 2ℓ > n − 1 this is (−ℓ/k, (ℓ − n + 1)/k); at n = 4,
  ℓ = 2: (−2/3, −1/3). Throat slack k²(c − a(a + 1)) = θ(1 − θ)(2ℓ − n + 1)² for a = a_pr + θ(a_ot − a_pr); a = −2/5 is
  θ = 1/5, slack 4/25 = β₀. All as in the files.
- **The pole position.** ε = w/(k(1 + w)) = Bμ/(k(A + Bμ)) (TARGET_HD §1); at n = 4, ℓ = 2 this is 7μ/(3(6 + 7μ + μ²)) =
  A2-S's ε_n/ε_d. ε_n = Bμ ≥ 0 with a zero only at μ = 0, ε_d = k(A + Bμ) > 0 for μ ≥ 0. The inner horizon is at
  z₋ = 1 − k_ratio^{−1/k} ≈ −δ_t/k with δ_t = 1 − k_ratio = 2w/(1 + w), and ε = δ_t/(2k): the throat's centre, as stated.
- **(i) S is C^∞ on the exterior and Proposition 3 applies at each μ.** For μ > 0 the pole z = −ε < 0 lies outside
  [0, 1]; P is C^∞ on (−ε, ∞) and addendum 2's Proposition applies as written. For μ = 0 (q = 1) ε = 0 and the pole is
  at z = 0, the horizon: outside the open exterior (0, 1), not outside [0, 1]. The brief's and
  `TARGET_A2_ADDENDUM_1.md` §3's phrase "outside [0, 1]" is wrong at this one point; the same file's "z = −ε ≤ 0 lies
  outside (0, 1)" is the correct statement. At μ = 0 the pencil Proposition of `METHOD_ADDENDUM_2.md` (P C¹ on an open
  interval containing [0, 1]) does not apply as written; the files cite Lean's `prop3_Ioo`/`prop3_Dn` (P C¹ on (0, 1))
  for exactly this, and that statement does apply (read; its hypotheses are met: f ≥ 0 and H ≠ 0 on (0, 1), R, and
  N ≥ 0 on (0, 1), which the charts give). The pencil proof goes through unchanged under the weaker hypothesis: step 3
  uses only z(ρ) ∈ (0, 1), and Lemma 1 needs S ∈ C¹(ℝ), which holds because z∘R lands in (0, 1). Addendum 2's last
  paragraph says this in words for the ζ-design; it is not stated as a Proposition.
  - **GAP-MINOR, fix:** add to `METHOD_ADDENDUM_2.md` (as an addendum 3, since it is sealed) the statement "Let P be C¹
    on (0, 1). If N ≥ 0 on (0, 1), then A_{ℓ,q} ≥ 0," with the one-line proof "step 3 uses z(ρ) ∈ (0, 1) only; the
    rest is unchanged," and replace "outside [0, 1]" by "outside (0, 1)" wherever the singular design at μ = 0 is
    meant. No claim changes: the reduction is sound at every μ ∈ [0, μ₁], and the certificates prove more (NL > 0 on
    the closed boxes).
- **(ii) The cover.** Rectangle (0, 1) × [0, μ₁]; charts O = [z₁, 1] × [0, μ₁], O′ = [0, z₁] × [μ_T, μ₁],
  T: z = μζ with (ζ, μ) ∈ [0, Z_T] × [0, μ_T], C: μ = zσ with (z, σ) ∈ [0, z₁] × [0, σ₁]; z₁ = 1/4, Z_T = 8,
  μ_T = 1/32, σ₁ = 1/8, μ₁ = 1/8 (both PREREGs). Case split, re-derived: z ≥ z₁ → O (needs z₁ ≤ 1); z < z₁ and
  μ ≥ μ_T → O′ (needs μ_T ≤ μ₁); z < z₁, μ < μ_T and z ≤ Z_Tμ → μ ≥ z/Z_T > 0, ζ = z/μ ∈ (0, Z_T], the point is in T's
  box and NL(z, μ) = μ²T(ζ, μ) > 0 by DIV-T and POS-T; else z > Z_Tμ → σ = μ/z < 1/Z_T ≤ σ₁ (this is Z_Tσ₁ ≥ 1), the
  point is in C's box and NL = z²C(z, σ) > 0 by DIV-C and POS-C, μ = 0 included (σ = 0). So every point of
  (0, 1) × [0, μ₁] has a chart with NL > 0, and with S = ε_dz + ε_n > 0 for z > 0 and L > 0 (gates S, L),
  N = NL/(S²L) > 0. SOUND.
  - COVER's Z_Tμ_T ≤ z₁ and z₁σ₁ ≤ μ₁ are not needed for coverage; they keep the images of T and C inside the
    rectangle, so that no positivity is demanded outside the exterior. The one coverage inequality beyond the trivial
    ones is Z_Tσ₁ ≥ 1. A2-S lists 0 < μ_T < μ₁ and 0 < z₁ < 1 (needed, for O and O′); HD-X-S's COVER lists only the
    three products, with the same fixed constants, so nothing is lost there; a run with other constants would want the
    two range checks. Remark, no gap.
  - `TARGET_A2_ADDENDUM_1.md` §3 says the charts cover [0, 1] × [0, μ₁]; the certificates' closed boxes do include
    z = 0, where NL is defined but N is not when μ = 0 (S = 0). Proposition 3 needs (0, 1) only, and both PREREGs
    state (0, 1). Consistent.
  - The exactness of the divisions (every monomial of NL of total degree ≥ 2, i.e. NL and both first partials vanish at
    (0, 0)) is the gates DIV-T/DIV-C's content; the pencil files assert only NL(0, 0) = 0, the gate carries the rest.
    The THROAT limit (information) re-derived: T(ζ, 0) = 64k²H(2)²L(0)[(c − a − a²)(ε_d(0)ζ + ε_n′(0))² +
    (a² − a)ε_n′(0)²], at n = 4 (18ζ + 7)² and 49; matches both PREREGs.

Hypotheses assumed: the Lean statements `prop3_Ioo`, `prop3_Dn` as read (not re-checked); the gates DIV, POS, S, L,
PARAM, G-RES as exact machine checks (not re-run); the pilot's design as sealed.

## Part B

### B1. The Darboux intertwiner at q = 1: GAP-MINOR (fix supplied; no claim changes)

Source: `results/extremal/PREREG.md` §2, "The partner" and "The intertwiner". Re-derived:
- w = (log u₀)_{r*} = fg/ρ with g = ρu₀,ρ/u₀ = −ν − ℓY/(1 − Y) + n(n − 1)Y/h (from u₀ = ρ^{−ν}(1 − Y)^{−α}/h); V = w² + w′
  from −u₀″ + Vu₀ = 0. L = ∂ − w, L† = −∂ − w (w real): L†L = −∂² + w′ + w² = A, LL† = −∂² + w² − w′ = Ã. So
  LA = LL†L = ÃL and L(A − ω²) = (Ã − ω²)L for every ω. Lψ = 0 iff ψ = Cu₀, which solves Aψ = ω²ψ only at ω = 0; so for
  ω ≠ 0, L is injective on the 2-dimensional solution space, hence bijective, with inverse L†/ω².
- Ũ: with ρd/dρ = −kYd/dY and ρf_ρ = 2kY(1 − Y), V = (f/ρ²)[(1 − Y)²(g² − g − kYg_Y) + 2kY(1 − Y)g] (Z-id's W) and
  Ṽ = w² − w′ = (f/ρ²)[(1 − Y)²(g² + g + kYg_Y) − 2kY(1 − Y)g]. Both as written.
- w at the ends: g → −ν and f → 1 at infinity, w ~ −ν/ρ; at the throat g ~ −ℓ/(1 − Y), f = (1 − Y)², w ~ −ℓ(1 − Y), and
  with s = −r* ~ 1/(k²(ρ − 1)), 1 − Y ~ k(ρ − 1) ~ 1/(ks): w ~ −ℓ/(ks) = −α/s. Both as written.
- For a solution ψ ~ e^{±iωr*}(1 + o(1)) whose o(1) is an asymptotic series in (ρ − 1) or 1/ρ, (o(1))′ = f·d/dρ of it is
  O((ρ − 1)²) or O(1/ρ²), so Lψ ~ (±iω − w)e^{±iωr*}(1 + o(1)) ~ ±iωe^{±iωr*}(1 + o(1)). As written.
- Wronskians: for ψ ∈ Sol_A(ω), (Lψ)′ = −wLψ − ω²ψ, so W[Lψ₁, Lψ₂] = ω²W[ψ₁, ψ₂] (NOTE.md §2's identity).

**The gap.** The PREREG says the quasinormal-mode conditions at the extremal horizon "are set at an irregular singular
point; that is the part to audit". For Im ω < 0 the ingoing solution e^{−iωr*} is dominant on the real axis as
r* → −∞ (|e^{−iωr*}| = e^{Im ω·r*}), so "ingoing" means the solution recessive in a sector of the complex (ρ − 1)-plane:
arg(ρ − 1) ∈ (arg ω − π, arg ω) (NOTE.md §1; re-derived from |e^{−iωr*}| = exp(−(|ω|/(k²|ρ − 1|))sin(arg ω − arg(ρ − 1)))
with r* ≈ −1/(k²(ρ − 1))). The PREREG's limits w → 0 are stated along the real axis only.

**The fix (two sentences).** fg = (1 − Y)²g is analytic at Y = 1 (the simple pole of g is cancelled by the double zero
of f) and vanishes there to first order, and the zeros of h sit at Y = −(ℓ − 1)/n, away from ρ = 1; so w = fg/ρ is
analytic at ρ = 1 with a simple zero, w = O(ρ − 1) in every direction. With the standard fact that the asymptotic
expansion of a recessive solution at a rank-1 irregular point holds with its derivatives in its sector, LH has the
asymptotics −iωe^{−iωr*}(1 + o(1)) in H's sector, so LH = −iωH̃ with H̃ the recessive solution of Ã normalised the same
way; likewise Lψ_∞ = iωψ̃_∞ at infinity (w = O(1/ρ) there). Then D_Ṿ := W[H̃, ψ̃_∞] = W[LH, Lψ_∞]/ω² = W[H, ψ_∞] = D_V for
ω ≠ 0, with the same r* (same f) on both sides. So V and Ṽ share their quasinormal-mode conditions at q = 1 for ω ≠ 0,
as claimed. At ω = 0 the map degenerates (Lu₀ = 0), which the claim excludes.

Hypotheses assumed: the standard asymptotic theory at rank-1 irregular singular points (expansions of recessive
solutions valid, with derivatives, in sectors; not re-proved here); u₀ > 0 on (1, ∞) (Z-pos), so w is real and C^∞ on ℝ.

### B2. Lemma R: SOUND

Source: `[a note of another line of this project]` §2. Re-derived: x(ζr) = 2M/(ζ^{n−1}r^{n−1}) = x(r), so f(ζr) = f(r) and
V(ζr) = g(x)/(ζr)² = ζ⁻²V(r); (f∂_r)[ψ(ζr)] = ζ[(f∂_r)ψ](ζr) and (f∂_r)²[ψ(ζr)] = ζ²[(f∂_r)²ψ](ζr) =
ζ²[(V − ω²)ψ](ζr) = [V(r) − ζ²ω²]ψ(ζr). So φ(r) = ψ(ζr) solves the equation at ζω (the equation depends on ω² only), on
the rotated domain. The hypothesis V = g(x)/r² holds for V_S± = fU±/(64r²H±²), U± and H± being polynomials in x with
(n, m, δ) coefficients (`code/ki/potentials.py`). The remarks check: Z_{n−1} = Z_{D−3} (trivial at D = 4, ω → −ω at D = 5,
Z₃ at D = 6, Z₈ at D = 11); in y = r^{n−1}, ∂_r = (n − 1)y^{(n−2)/(n−1)}∂_y, and dividing by (n − 1)²y^{2(n−2)/(n−1)} leaves
every coefficient rational in y except ω²y^{2/(n−1)−2}/(n − 1)² (NOTE.md §1's form, with k = n − 1); the zeros of H₋ are
at x = −2m/(n(n + 1)(1 + mδ)) < 0, none on the positive axis; 2(n − 1) zeros of f; ∞ irregular of rank 1 for ω ≠ 0.

Hypotheses assumed: none beyond the form of V (the vector and tensor types are excluded by the note).

### B3. The functional relations at q = 1: SOUND as pencil statements

Sources: `[a note of another line of this project]`; `results/planning/kimaster_fr_2026-10-26/NOTE.md` §§1-3. The planning
numerics were not used as evidence. Local structure re-derived first (q = 1, k = n − 1, f = ρ^{−2k}(ρ^k − 1)²):
- **r = 0.** With F = (ρ^k − 1)², the equation times ρ^{4k+2}/F² is ρ²ψ″ + ρ(−2k + ρF_ρ/F)ψ′ + (−W̃/F + ω²ρ^{4k+2}/F²)ψ = 0,
  W̃ analytic with W̃(0) = 16u₄/(64(ℓ + n)²n²), u₄ = U₋'s x⁴ coefficient = −n³(3n − 2)(n + 1)⁴δ(1 + mδ)³ = −n³(3n − 2)(ℓ + n)²
  at q = 1 (δ = 1/((ℓ + n)(n + 1)), 1 + mδ = (ℓ + n)/(n + 1)); so W̃(0) = −n(3n − 2)/4 and the indicial roots are n/2 and
  (3n − 2)/2 (sum 2k + 1, product n(3n − 2)/4). Their difference k is a resonance; ω² enters at relative order ρ^{4k+2} > ρ^k,
  so the no-log condition is ω-independent, and at ω = 0 the exponent-n/2 solution is u₀ = const·ρ^{n/2}·(power series in
  ρ^k), log-free (re-derived from u₀'s closed form). Hence M₀ = (−1)ⁿI. As in the note (exact there for n = 2…9).
- **Horizons.** 1/f = 1/(k²(ρ − 1)²) + (k + 1)/(k²(ρ − 1)) + O(1), so r* = −1/(k²(ρ − 1)) + ((k + 1)/k²)log(ρ − 1) +
  analytic: rank 1, and one turn around the horizon multiplies e^{−iωr*} by λ := e^{2πω(k+1)/k²}. W(1) = ℓ(ℓ − n + 1) from
  U₋(2) = 64ℓ(ℓ − n + 1)H₋(2)². **Infinity.** 1/f = 1 + 2ρ^{−k} + …, residue 0 for k ≥ 2: no log. As in the note.

The five relations:
- **(a) Lemma R's action.** At infinity, with r* normalised by r* − r → 0, r*(ζr) = ζr*(r) exactly along rotated rays
  (1/f − 1 = O(r^{−k})), and ωr is invariant; so ψ_∞(ζr; ζ⁻¹ω) solves at ω with the asymptotics e^{iωr*}(1 + O(1/r)) in the
  same sector arg(ωr) ∈ (0, π), where it is recessive: it equals ψ_∞(r; ω). At r = 0 the Frobenius series contain
  r^{β± + jk + i(4k+2)}ω^{2i}; under r → ζr, ω² → ζ⁻²ω² each term is invariant (ζ^{jk} = 1, ζ^{i(4k+2)−2i} = ζ^{4ik} = 1),
  so φ±(ζr; ζ⁻¹ω) = ζ^{β±}φ±(r; ω) with ζ^{β₊} = ζ^{β₋}ζ^k = ζ^{β₋}: one scalar ζ^{n/2}, given a rotation-invariant
  convention for φ₋'s resonant coefficient (e.g. zero). H(ζ^jr; ζ^{−j}ω) solves at ω and is recessive at h_j = ζ^{−j};
  R1 follows by the change of variable in the Wronskian (a factor ζ^j from ∂_r, a phase from the r*-branch constant).
  Stokes sectors at infinity are set by arg(ωr), which is invariant: no sector is rotated. SOUND.
- **(b) The cyclic monodromy product.** In the Frobenius frame Φ, Φ(ζ^jr; ζ^{−j}ω) = ζ^{jn/2}Φ(r; ω); continuing along the
  rotated loop around h_j is continuing Φ(·; ζ^{−j}ω) along the loop around h₀, so Φ → ΦM(ζ^{−j}ω) and the scalar cancels:
  M_j(ω) = M(ζ^{−j}ω), no conjugation. det M = 1 since W_{r*} = fW_r is single-valued and f has a double zero. M is entire
  in ω² (the Frobenius solutions are; the loop is fixed). The big loop is the ordered product of the loops around 0, the k
  horizons and the k apparent points (trivial), so M_∞ = (−1)ⁿ∏_j M(ζ^{−j}ω) in the traversal order; the written order is
  a convention, as the addendum says. tr M_∞(ζω) = tr M_∞(ω) because ζ^{−(k−1)} = ζ cyclically permutes the factors. SOUND.
- **(c) The TQ system with λ.** y_s := H(·; e^{θ+iπs}) solves at ω and is recessive in S_s = (arg ω + π(s − 1), arg ω + πs).
  Recessive expansions hold in the adjacent sectors, so W[y_s, y_{s+1}] = 2iω_s = 2iω(−1)^s. y_{s−1} = τ_sy_s + cy_{s+1}
  with c = 1 by the Wronskian against y_s. One turn around h₀, in the direction in which arg ω grows, shifts r* by
  2πi(k + 1)/k², and the recessive solution on the next sheet is y_{s+2} = λ_s·(y_s continued), λ_s = e^{2π(−1)^sω(k+1)/k²}
  (the note's M_loc⁻¹: an orientation convention). Wronskians are continuation-invariant and λ_{s±1} = λ_s⁻¹, so
  τ_{s+2} = λ_s⁻²τ_s: τ(θ + 2πi) = λ⁻²τ(θ). Trace: y₂ = y₀ − τ₁y₁, y₃ = −τ₂y₀ + (1 + τ₁τ₂)y₁, and the turn sends
  y₀ → λ⁻¹y₂, y₁ → λy₃, so tr = λ⁻¹ + λ(1 + τ₁τ₂) = λ + λ⁻¹ + λτ₁τ₂ with det 1; tr M⁻¹ = tr M for det 1, so the trace
  formula is orientation-free. The first version without λ would need the log term of r* to vanish, and (k + 1)/k² ≠ 0.
  SOUND.
- **(d) The quantum Wronskian.** W[φ₋, φ₊] = k (f·r^{β₋+β₊−1}(β₊ − β₋) → ρ^{−2k}ρ^{2n−2}k = k). Writing H = (Q₊φ₋ − Q₋φ₊)/k
  with Q± = W[H, φ±], and using that φ± depend on ω² only, τ(θ)y₀ = y₋₁ − y₁ against φ± gives τQ±(θ) = Q±(θ − iπ) −
  Q±(θ + iπ), and W[y₀, y₁] = 2iω gives Q₋(θ)Q₊(θ + iπ) − Q₊(θ)Q₋(θ + iπ) = 2ikω. SOUND, given fixed continuation paths
  from the horizon to r = 0 (the apparent points have trivial monodromy and r = 0 a scalar one, so only the side of the
  other horizons matters; the note's Q± presuppose one).
- **(e) D = (Q₋E₊ − Q₊E₋)/k.** From H = (Q₊φ₋ − Q₋φ₊)/k and E± = W[ψ_∞, φ±]: D = W[H, ψ_∞] = (Q₋E₊ − Q₊E₋)/k. SOUND, same
  path proviso.

Not checked in detail: the subsidiary sentence "Lemma R relates the E± at ω and ζ⁻¹ω through M(ω)" (path bookkeeping);
it is not among the five relations. Hypotheses assumed: the standard asymptotic theory at rank-1 irregular points; the
no-log condition at r = 0 (exact in the note for n = 2…9, and re-derived by pencil above for every n ≥ 2); the
conventions named (product order, loop orientation, continuation paths, φ₋'s resonant coefficient).

## Hypotheses assumed throughout

1. S5's reduction to the master equation and its (5.59)-(5.63), as transcribed in `code/ki/potentials.py` (the trust base
   of `METHOD_ADDENDUM_1.md` §3). The independent transcription checks sit in barred folders and were not opened.
2. Every exact machine gate named in the PREREGs (E0/E0n, H, PARAM, DESIGN, G-RES, COVER, L, S, DIV-T, DIV-C, the POS
   charts, Lemma U's corner values, Z's checks) as a check that ran and passed: not re-run here.
3. The Lean theorems `prop3`, `prop3_Ioo`, `prop3_Dn`, `prop3_Dn_zeta` and `tortoise_q1`: statements read, proofs not
   re-checked.
4. Standard asymptotic theory at rank-1 irregular singular points (B1, B3).
5. The brief's descriptions of the items, which match the files read.

## Process

- Files read, all on the allow-list: `CHARTER.md` §5, `RULES.md` B3, `TARGET.md`, `TARGET_A2.md`, `TARGET_HD.md`,
  `TARGET_A2_ADDENDUM_1.md`, `TARGET_HD_ADDENDUM_2.md`, `code/ki/potentials.py`, `results/hd/elementary/PREREG.md`,
  `results/p3/METHOD.md`, `METHOD_ADDENDUM_1.md`, `METHOD_ADDENDUM_2.md`, `results/a2/s/PREREG.md`,
  `results/hdx/s/PREREG.md`, `results/extremal/PREREG.md`, `[a note of another line of this project]`,
  `[a note of another line of this project]`, `results/planning/kimaster_fr_2026-10-26/NOTE.md`, and the theorem statements in
  `lean/lean_p3_sdeformation_v5_2026-10-24/lean/BHModesP3.lean` and `lean/lean_z_d_2026-10-26/lean/BHModesZd.lean`
  (grep of the `theorem` lines only).
- No process run; no external contact; nothing written outside this folder; no git.
- Files here: `AUDIT.md` (this), `AUDIT_notes_A1.md`, `AUDIT_notes_A2_A3.md`, `AUDIT_notes_B.md`, the brief's copy
  `BRIEF_fable_2026-10-26.md`, `STATE.md`, `STATE_LOG.md`, `MESSAGES.md` (the last three evolve and are excluded from
  `SHA256SUMS`, which lists every other file).
