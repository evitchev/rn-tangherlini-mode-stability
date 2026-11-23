# Check of the stability paper's new appendices against their sources

*2026-11-22 (EST). Registry BHM-203 (with BHM-202). Written by the session that received the brief
`outbox/2026-11-22-to-bh-modes-4e-2.md` (SHA-256 `55820db6b1ba43f0ba3c82d40ecff0ea66daba36c731967f3854b4c7f3594c8c`,
checked) from the lead session. This is the session that wrote the cold read (BHM-199), so it is not independent of
that list; it had not seen the sources below before this check.*

## 0. What was read, and how

- **The paper, frozen:** `stability_2026-11-22b.pdf` (SHA-256 `4148f78d…9f7e`, checked) and
  `stability_2026-11-22b.tex` (SHA-256 `966637a5…8c8a`, checked), both in this folder. The source was read in
  full. PDF pages 6–8 and 14–17 were viewed as rendered pages; on them the PDF says what the source says
  (§3–§4.6, and Appendices A–C).
- **The sources:** only the files the brief lists.
  - [1]: PDF pages 24–25 as rendered pages (the formulae of item 1 were compared there), and passages of the
    `.txt`.
  - [4], [5], [6]: passages of the `.txt` files.
  - `code/ki/potentials.py` and the eleven files under `results/`, each read in full.
- **No other file was opened, no web, no code was run.** Commands: `sha256sum`, `ls`, `wc`, `date`, and
  `cat -n`, `sed -n`, `grep -n` and one-line `awk` to print passages with their line and page numbers (the page
  of a line is 1 plus the number of form feeds before it, as the brief says; a line that begins with a form feed
  is on the new page).
- **All arithmetic below is by hand.** Where it is exact I say so; otherwise it is decimal arithmetic good to
  about six significant figures.
- **Reader:** Claude Fable 5.2 at effort `xhigh`, by the operator's `/model` and `/effort` commands in this
  session's transcript.
- Reference numbers such as [1] are the PDF's.

## 1. Verdicts

| # | What | Verdict |
|---|---|---|
| 1 | Appendix A's U₋ against [1, eq. (5.63b)] at λ = 0, K = 1, on the rendered page | **MATCHES** |
| 1 | Appendix A's U₋ against `U_minus` in `code/ki/potentials.py` | **MATCHES** |
| 2 | Appendix B.1 against `results/p3/METHOD.md` l.19–36 | **MATCHES**; the algebra is correct |
| 3 | Appendix B.2 against `results/p3/METHOD_ADDENDUM_1.md` l.15–25 | **MATCHES**; the argument is sound |
| 4 | Appendix B.3 against `results/a1/PREREG.md` l.50–66 and `results/hd/elementary/PREREG.md` l.50–56 | **MATCHES** |
| 4 | §4.3: the statement, ℓ₀ = 10, 10, 10, 11, 13, 14, and the six exact bounds | **MATCHES**; all six reproduced by hand |
| 5 | Appendix B.4, the proof | correct |
| 5 | §4.5–§4.6: the chart domains and the constants | **MATCHES** |
| 5 | §4.6: the five conditions | three **MATCH**; for two, "the code checks" is **CANNOT TELL** |
| 6 | §4.1: ε → 0 as q → 1 for the singular designs | **MATCHES** |
| 6 | §4.1: Proposition 3 follows from Lemmas 1–2 | **MATCHES** (one sentence of the source is missing, §3 note N1) |
| 7 | §4.6: c = 1/4 | **MATCHES** |
| 7 | §5.3: each μ_lo equals E1's lower end, and the code checks it | **MATCHES** |
| 8 | §6: the description of the test G1 | **MATCHES** |
| 9 | The new citations of §1–§2, eleven anchors | **MATCH**; one caveat on [6] |

No item DIFFERS. I found no error in the mathematics of Appendices A and B. Section 3 lists six notes; N1 to N5
each carry a suggestion.

## 2. The items

### 1. Appendix A: U₋

**Against [1].** [1, eq. (5.63b)], read on the rendered page 25:

    U₋ = [−4n³(n+2)(n+1)²(1+mδ)²x² + 48n²(n+1)(n−2)m(1+mδ)x − 16(n−2)(n−4)m²] y
         − n³(3n−2)(n+1)⁴ δ(1+mδ)³ x⁴
         − 4n²(n+1)²(1+mδ)² {(n+1)(3n−2)mδ − n²} x³
         + 4(n+1)(1+mδ) {m(n−2)(n−4)(n+1)(m+n²K)δ + 4n(2n²−3n+4)m + n²(n−2)(n−4)(n+1)K} x²
         − 16m {(n+1)m(−4m + 3n²(n−2)K)δ + 3n(n−4)m + 3n²(n+1)(n−2)K} x
         + 64m³ + 16n(n+2)m²K.

Here x = 2M/r^{n−1}, y = λr² and z = Q²/r^{2n−2} [1, eq. (5.40), p. 21], so λ = 0 removes the first bracket.
With K = 1, term by term:

| Power | [1] at y = 0, K = 1 | Appendix A | |
|---|---|---|---|
| x⁴ | −n³(3n−2)(n+1)⁴ δ(1+mδ)³ | −n³(3n−2)(n+1)⁴ δ(1+mδ)³ | same |
| x³ | −4n²(n+1)²(1+mδ)²{(n+1)(3n−2)mδ − n²} | −4n²(n+1)²(1+mδ)²[(n+1)(3n−2)mδ − n²] | same |
| x² | +4(n+1)(1+mδ){m(n−2)(n−4)(n+1)(m+n²)δ + 4n(2n²−3n+4)m + n²(n−2)(n−4)(n+1)} | the same three terms | same |
| x¹ | −16m{(n+1)m(−4m + 3n²(n−2))δ + 3n(n−4)m + 3n²(n+1)(n−2)} | −16m[(n+1)m(3n²(n−2) − 4m)δ + …] | same; one sum reordered |
| x⁰ | +64m³ + 16n(n+2)m² | +64m³ + 16n(n+2)m² | same |

H₋ = m + n(n+1)(1+mδ)x/2 is [1, eq. (5.62b)], and V_{S±} = fU±/(64r²H±²) is [1, eq. (5.61)], as §2 has them.
[1, p. 25] also says that Φ₋ and Φ₊ "represent the gravitational mode and the electromagnetic mode,
respectively", which is the abstract's new wording.

**Against the code.** `U_minus(n, K=1)` (`code/ki/potentials.py` l.33–42) has the same five terms with K kept as
a parameter, and drops the y bracket ("at y = 0"). Its n = 4 form `U_TARGET` (l.57–61) agrees with Appendix A at
n = 4 by hand: −400000δ(1+mδ)³x⁴ − 1600(1+mδ)²(50mδ − 16)x³ + 7680m(1+mδ)x² − 16m(5m(96 − 4m)δ + 480)x + 64m³ +
384m².

**Two further checks, mine.**
- Item 4 below reproduces the six bounds of Lemma U from Appendix A's formula. That tests its x¹, x³ and x⁴
  coefficients at n = 4, …, 9 against the records' numbers.
- At δ = 0, Appendix A gives U₋ = 4[n⁴(n+1)²x³ + n(n+1)(4(2n²−3n+4)m + n(n−2)(n−4)(n+1))x² − 12nm((n−4)m +
  n(n+1)(n−2))x + 16m³ + 4n(n+2)m²], which is four times the neutral numerator as I remember it from the
  literature. This is from memory, not from a file.

**The last sentence of Appendix A,** "Its transcription from [1] was checked in the Lean formalisation and by
two independent transcriptions": see note N3.

### 2. Appendix B.1 (Lemma 2)

**MATCHES** `results/p3/METHOD.md` l.19–35, step for step: β := (1 − z)P = P/ρ and S = −fβ; V = fW with
W := U₋/(64ρ²H₋²); d/dr* = f d/dρ; the first form Ṽ = f[W − f_ρβ − f(β_ρ + β²)]; the four products with ρ²; the
conclusion. The paper writes f_ρ, β_ρ where the source writes f′, β′ with ′ = d/dρ, which is right, since in the
paper a prime is d/dr*.

**The algebra,** checked by hand:
- S′ = f dS/dρ = −f(f_ρβ + fβ_ρ), so Ṽ = fW − f(f_ρβ + fβ_ρ) − f²β² = f[W − f_ρβ − f(β_ρ + β²)].
- z = 1 − 1/ρ gives dz/dρ = 1/ρ² = (1 − z)², so f_ρ = (1 − z)²f_z and
  β_ρ = (1 − z)²·d/dz[(1 − z)P] = (1 − z)²(−P + (1 − z)P_z).
- With ρ(1 − z) = 1: ρ²f_ρβ = (1 − z)f_zP; ρ²fβ_ρ = f(−P + (1 − z)P_z); ρ²fβ² = fP²; ρ²W = U₋/(64H₋²).
- So ρ²·[bracket] = [U₋ − 64H₋²((1 − z)f_zP + f(−P + (1 − z)P_z + P²))]/(64H₋²) = N/(64H₋²), and
  Ṽ = fN/(64ρ²H₋²).

**Differences from the source,** none an error:
- The source takes P a polynomial in z, at n = 4 ("n = 4 here"). The paper takes P a C¹ function on (0, 1) and
  general n. The computation uses neither restriction.
- The source's bullet "Smoothness" (l.21, l.26: S is C^∞ on ℝ) is not in the paper: note N1.

### 3. Appendix B.2 (the tortoise coordinate)

**MATCHES** `results/p3/METHOD_ADDENDUM_1.md` l.17–24: f > 0 on the exterior region; r* = ∫dr/f is C^∞ and
strictly increasing, with a C^∞ inverse; a simple zero of f at the horizon for q < 1 and a double zero at q = 1,
so r* → −∞ like log(r − r_H) and like −1/(r − r_H); f → 1 and r* → +∞ at infinity; every q ∈ [0, 1].

**The argument is sound.** As a function of x, f = 1 − x + q²x²/4 has the roots (2/q²)(1 ∓ √(1 − q²)) for
q > 0; the smaller is x_H = 2/(1 + √(1 − q²)), and f(0) = 1 > 0, so f > 0 on 0 < x < x_H, which is the exterior
region since x decreases in r. The roots are distinct for q < 1 and equal (x = 2) at q = 1. At q = 0, f = 1 − x.

**Differences from the source,** none an error:
- The source proves f > 0 from the factorisation f = (1 − x/x_H)(1 − x/x₋) with x_H ≤ x₋. The paper uses the
  smallest positive root. The paper's form also covers q = 0, where there is no x₋.
- The source's "f_z(0) = 3(1 − κ³) > 0" (l.21) is the n = 4 value. The paper states the simple zero for general
  n, which is right.

### 4. Appendix B.3 and §4.3 (Lemma U)

**Appendix B.3 MATCHES** `results/a1/PREREG.md` l.52–65 (n = 4) and `results/hd/elementary/PREREG.md` l.52–56
(general n): the polynomial ε⁶U₋(x; m = ε⁻², δ = κε) = Pos − Neg with Pos(0) = 64, and the steps (a)–(d).
- (a) Expanding (1 + 2mδ)² = 1 + 4mq²/(n + 1)² gives 4mδ + 4m²δ² = 4mq²/(n + 1)², so mδ² + δ = q²/(n + 1)², and
  κ² = mδ² = q²/(n + 1)² − δ ≤ 1/(n + 1)². Correct. The source's 1/25 and 1/5 are the n = 4 values.
- (b) Correct: x_H ≤ 2, with equality at q = 1.
- (c) At ℓ = ℓ₀ + 1, m = ℓ₀(ℓ₀ + n + 1), which is the source's m(ℓ₀ + 1). At n = 4: 10·15 = 150, and
  150·(1/12)² = 150/144 ≥ 1. The sources fix ε̄ = 1/isqrt(m₀) (`a1/PREREG.md` l.61, `hd/elementary/PREREG.md`
  l.32); the paper says only "a rational ε̄ with m₀ε̄² ≥ 1", which is what the proof needs.
- (d) Correct.
- The substitution gives a polynomial: every term of U₋ has at most six powers of 1/ε after it (I checked each of
  the five terms), and the constant term comes from 64m³ alone.

**§4.3 MATCHES** `results/a1/RESULT.md` l.33–41 and `results/hd/elementary/RESULT_ADDENDUM_1.md` l.23–29:

| n (D) | the files: "holds from ℓ =" | paper's ℓ₀ | the files' exact bound | paper | my value by hand |
|---|---|---|---|---|---|
| 4 (6) | 11 | 10 | 959747/17496 | same | 959747/17496, exact |
| 5 (7) | 11 | 10 | 399917/10368 = 38.57224… | same | 38.57224 |
| 6 (8) | 11 | 10 | 1481614528/62748517 = 23.61194… | same | 23.61194 |
| 7 (9) | 12 | 11 | 17257/2401 = 7.18742… | same | 7.18742 |
| 8 (10) | 14 | 13 | 79325/16384 = 4.84161… | same | 4.84161 |
| 9 (11) | 15 | 14 | 19870/6561 = 3.02850… | same | 3.02850 |

**How I reproduced the bounds.** From Appendix A, with c := (n + 1)(3n − 2),

    Neg_n = 16[3n²(n−2)(n+1) ε³κ + 3n(n−4) ε² + 3n²(n+1)(n−2) ε⁴] x
          + 4n²(n+1)² ε³ [(c − 2n²) ε²κ + (2c − n²) εκ² + c κ³] x³
          + n³(3n−2)(n+1)⁴ κ ε⁴ (ε + κ)³ x⁴,

and every other monomial, among them the whole x² term and the constant 64, has a non-negative coefficient for
n ≥ 4 and belongs to Pos. At n = 4 this is the nine monomials of `results/a1/RESULT.md` l.36–37, with the
same coefficients (7680, 7680, 80000, 134400, 28800, 400000, 1200000, 1200000, 400000). For n ≥ 5 it has ten
monomials (the ε²x term is new), as Table 1 says. At the corner (ε̄, 1/(n + 1), 2):
- n = 4, ε̄ = 1/12: the nine terms are 16/9, 20/27, 80/27, 56/27, 5/27, 40/81, 50/81, 125/486 and 625/17496. Their
  sum is 159997/17496, as `RESULT.md` l.38 has it, and 64 − 159997/17496 = 959747/17496. Exact.
- n = 5, …, 9, with ε̄ = 1/12, 1/13, 1/14, 1/16, 1/18 (m₀ = 160, 170, 209, 286, 336): Neg = 25.42776, 40.38806,
  56.81258, 59.15839, 60.97150, and 64 − Neg is the last column above.

**One remark on a decimal:** note N2.

### 5. Appendix B.4, and the charts of §4.5–§4.6

**The proof of B.4 is correct.** Take 0 < z < 1 and 0 ≤ μ ≤ μ₁.
- z ≥ z₁: the point is in O = [z₁, 1] × [0, μ₁].
- z < z₁ and μ ≥ μ₀: it is in O′ = [0, z₁] × [μ₀, μ₁].
- z < z₁, μ < μ₀ and z ≤ ζ₁μ: then μ > 0 because z > 0, and (ζ, μ) = (z/μ, μ) lies in [0, ζ₁] × [0, μ₀].
- z < z₁, μ < μ₀ and z > ζ₁μ: then σ = μ/z < 1/ζ₁ ≤ σ₁, which is where ζ₁σ₁ ≥ 1 is used, and (z, σ) lies in
  [0, z₁] × [0, σ₁]. This case includes μ = 0, with σ = 0.
- The second claim: μ ≤ μ₀ ≤ μ₁ and z = μζ ≤ μ₀ζ₁ ≤ z₁ on T's image; z ≤ z₁ and μ = zσ ≤ z₁σ₁ ≤ μ₁ on C's.

It is the case split of `results/hdx/critical/PREREG.md` l.66–67. B.4 proves the cover of (0, 1) × [0, μ₁]; §4.6
states it for (0, 1) × (0, μ₁], which is contained in it. The two uses in §4.5 are consistent with it: for A2-S
and HD-X-S the polynomials are positive down to μ = 0, and at μ = 0 the charts O and C (σ = 0) give NL > 0 for
every z ∈ (0, 1); for the critical bands N_O = NL/μ and N_C = NL(z, zσ)/(z²σ) give NL > 0 only for μ > 0.

**The chart domains and constants MATCH:**

| Paper (§4.5, §4.6) | `hdx/s/PREREG.md` l.31–38 | `a2/s/RESULT.md` l.17–24 | `hdx/critical/PREREG.md` l.59–64, l.116 |
|---|---|---|---|
| O = [z₁, 1] × [0, μ₁] | [Z1, 1] × [0, μ₁] | [1/4, 1] × [0, 1/8] | [1/4, 1] × [0, MU1] |
| O′ = [0, z₁] × [μ₀, μ₁] | [0, Z1] × [MUT, μ₁] | [0, 1/4] × [1/32, 1/8] | [0, 1/4] × [1/32, MU1] |
| T: z = μζ, [0, ζ₁] × [0, μ₀] | [0, ZT] × [0, MUT] | [0, 8] × [0, 1/32] | [0, 8] × [0, 1/32] |
| C: μ = zσ, [0, z₁] × [0, σ₁] | [0, Z1] × [0, SIG1] | [0, 1/4] × [0, 1/8] | [0, 1/4] × [0, 1/8] |
| z₁ = 1/4, ζ₁ = 8, σ₁ = 1/8, μ₀ = 1/32 | Z1, ZT, SIG1, MUT: the same | the same | l.116: the same |
| μ₁ = 1/8 (A2-S, HD-X-S) | μ₁ = 1/8 | 1/8 | — |
| μ₁ ∈ {1/8, 13/100, 3/25} (critical) | — | — | the MU1 column, l.106–114: exactly these three |
| N_O = NL, N_T = NL(μζ, μ)/μ², N_C = NL(z, zσ)/z² | the same (l.32–35) | the same | — |
| critical: N_O = NL/μ, N_T = NL(μζ, μ)/μ², N_C = NL(z, zσ)/(z²σ) | — | — | M, T, K: the same |

Also matching: NL := N·S_ε²·L with L = Ud·Hd²·fd and P = Π/S_ε (`hdx/s/PREREG.md` l.26–30); in the critical
bands NL = N·S_ε²R²L with 𝒟 = S_ε·R·Hn and R = (1 − (1 − z)^{n−1})/z (`hdx/critical/PREREG.md` l.42, l.50–54);
A2-S's degrees (38, 12), (38, 48), (48, 12) and "no chart needed a bisection"; HD-X-2's degrees in Table 1
against the table at l.106–114; the nine critical bands (l.25); and "the largest is q(μ₁)² = 46562824/47513449,
at D = 10, ℓ = 3" (l.111; I compared the nine values by hand). Two values recomputed by hand from §2's w(μ):
q(1/8)² = 2961/3025 at D = 6, ℓ = 2, and 197505/201601 at D = 7, ℓ = 2. Both agree. R ≥ 1 on [0, 1] is right:
R = 1 + (1 − z) + … + (1 − z)^{n−2}.

**The five conditions.** As §4.6 states them: 0 < z₁ < 1, 0 < μ₀ ≤ μ₁, ζ₁σ₁ ≥ 1 (for the cover), and ζ₁μ₀ ≤ z₁,
z₁σ₁ ≤ μ₁ (for the images).
- The constants satisfy all five: 0 < 1/4 < 1; 0 < 1/32 ≤ 3/25, the least μ₁; 8·(1/8) = 1; 8·(1/32) = 1/4;
  (1/4)(1/8) = 1/32 ≤ μ₁.
- The files say that the gate COVER checks the last three: `hdx/s/PREREG.md` l.38 ("COVER checks ZT·SIG1 ≥ 1,
  ZT·MUT ≤ Z1 and Z1·SIG1 ≤ μ₁") and `hdx/critical/PREREG.md` l.66. **MATCHES** for these three.
- "HD-X-2's code checks all five": for 0 < z₁ < 1 and 0 < μ₀ ≤ μ₁ this is **CANNOT TELL**. No listed file says
  that the code checks them, and `code/hdx/critical.py` is not on the list. Note N4.

### 6. §4.1

**ε → 0 as q → 1: MATCHES.**
- A2-S: ε = w/(3(1 + w)) (`a2/s/RESULT.md` l.12; 3 = n − 1 at n = 4).
- HD-X-S: ε = w/((n − 1)(1 + w)) = ε_n/ε_d (`hdx/s/PREREG.md` l.24).
- HD-X-2: ε = ε̂w/(1 + w) = ε_n/ε_d (`hdx/critical/PREREG.md` l.44), with the gate S: "ε_n(0) = 0; ε_n/μ > 0 and
  ε_d > 0 on [0, MU1]" (l.87).

In each, ε is a positive multiple of w/(1 + w), and w(μ) of §2 is 0 at μ = 0 (q = 1) and positive for μ > 0. So
ε > 0 for q < 1 and ε → 0 as q → 1, as the paper says, and at q = 1 the pole is at z = 0: P = a/z + p₀(z)
there, as the gate G-RES of `a2/s/RESULT.md` l.30 has it. The paper is more exact here than
`hdx/s/PREREG.md` l.41 ("P's pole z = −ε lies outside [0, 1]"), which does not hold at μ = 0.

**Proposition 3 follows from Lemmas 1–2: MATCHES** `results/p3/METHOD.md` l.37–38 ("On the exterior f > 0, ρ > 0
and H₋ ≥ m > 0, so Ṽ ≥ 0 on ℝ. Apply the Corollary").
- The paper's hypothesis is weaker than the source's: P is C¹ on the open interval and N ≥ 0 there, against a
  polynomial P with N ≥ 0 on [0, 1]. The argument covers it: Ṽ = fN/(64ρ²H₋²) ≥ 0 on the exterior region is
  exactly N ≥ 0 on z ∈ (0, 1), and Lemma 1 needs only S ∈ C¹(ℝ). The files name this version too: "Proposition 3
  for P C¹ on (0, 1)" (`a2/s/RESULT.md` l.13, l.54; `hdx/s/PREREG.md` l.40).
- That S ∈ C¹(ℝ) is not said in the paper: note N1.
- "Formally verified in Lean for every n" and "at q = 1 it is also formally verified": the listed files say so
  (`hdx/s/PREREG.md` l.40–41, "every n ≥ 2"; `hdx/critical/PREREG.md` l.77, `tortoise_q1`). I did not see the
  Lean files.

### 7. §4.6 and §5.3

**c = 1/4: MATCHES** `results/hdx/critical/PREREG.md` l.46 ("c = 1/4") and l.116 ("The constants common to every
band: c = 1/4, …"). The design the paper describes is the file's (l.40): I checked by hand that at ε = 0 and
μ = 0, −ν − ℓy/(zR) − (1 − z)H_z/H equals (1 − z)(log u₀)_z for the u₀ of Theorem 2, using
H₋ = (ℓ + n)((ℓ − 1) + nY) at q = 1. That identity also confirms the remark after Theorem 2 that
1/((ℓ − 1) + nY) is 1/H₋ at q = 1 up to a constant.

**Each μ_lo equals E1's lower end: MATCHES** `results/hdx/elementary/RESULT.md` l.12 ("MEET means every μ_lo
equals HD-E's sealed E1 lower end, and the hand-off ℓ₀ = 10, 10, 11, 13, 14 matches"), with l.10 ("Every gate
holds: … MEET"). The file also supports §5.3's two sub-bullets (l.26–29), the count of 33 cases (l.13), and by my
count from ℓ_el and ℓ₀ the 35 pairs of E1.

### 8. §6: the test G1

**MATCHES** `results/p3/PREREG.md` l.43: "Known answer (S6, proved): A ≥ 0 for D = 10, ℓ = 2, Q = 0, where V has
a negative region (BHM-014, K1). The same construction (x = (1 − z)⁷, f = 1 − x) must verify | must pass".
- The paper: "the same method of choosing designs, applied to a case whose answer is known (D = 10, ℓ = 2,
  Q = 0, stable by [3] although V has a negative region there), had to give a verified design". The case, the
  reason the answer is known ([3] is the file's S6) and the requirement are the file's.
- "Counts as failed, as specified in advance" agrees with l.59: "Pass. T1 and G1 VERIFIED; …". T3 is "stretch;
  reported either way" (l.42).
- "and did not": line 43 registers the test; the outcome is in `results/p3/RESULT.md`, which is not on my list.
  Two listed files agree with it indirectly: `METHOD_ADDENDUM_1.md` l.35–37 and `a1/PREREG.md` l.75 ("G1 passed
  at D = 10 with rule 2").
- T3's range ends, recomputed by hand from §2's w(μ) at n = 4, ℓ = 2: μ = 1/5 gives q² = 21576/22801 and
  μ = 3/25 gives q² = 31416/32041, as §5.1 has them.

### 9. The new citations of §1–§2

| Anchor | The paper says | The source, at that place | |
|---|---|---|---|
| [1, p. 3] | the horizon's spatial section; K = 1 for the round Sⁿ | p. 3: "the space Kⁿ describes the structure of a spatial section of its horizon … K denotes its sectional curvature … we normalise K so that K = 0, ±1" | MATCHES |
| [1, eqs. (2.12), (2.14)] | λ := 2Λ/(n(n + 1)) | p. 4: (2.12) is the Einstein equation with Λ; (2.14): "λ := 2Λ/(n(n + 1))" | MATCHES |
| [1, eq. (2.18)] | ds² = −f dt² + f⁻¹dr² + r²dσ_n² | p. 5: "ds² = −f(r)dt² + dr²/f(r) + r²dσ_n²" | MATCHES |
| [1, eq. (2.19)] | f = K − λr² − 2M/r^{n−1} + Q²/r^{2(n−1)} | p. 5: "f(r) = K − λr² − 2M/r^{n−1} + Q²/r^{2n−2}" | MATCHES |
| [1, p. 15] | the modes with ℓ = 0 change the parameters of the background | p. 15: "the lowest eigenvalue is k² = 0 … A perturbation corresponding to such a constant mode represents a variation of the parameters λ, M, and Q of the background" | MATCHES |
| [1, p. 32] | "the S-deformation cannot remove this negative region if S is a regular function at the horizon" | p. 32, word for word, after "V_S₋ has a negative region around the horizon for the extremal and near extremal cases" | MATCHES |
| [1, p. 42] | at ℓ = 1, Φ₋ is not gauge-invariant, while Φ₊ is | p. 42: "For k² = n and K = 1 … we find that Φ₊ is gauge-invariant. In contrast, … Φ₋ is not gauge-invariant" | MATCHES |
| [4, p. 13], first | "becomes negative near the horizon in general" | p. 13: "However, for n > 2, Ṽ_S₋ becomes negative near the horizon in general (See Fig.3)" | MATCHES |
| [4, p. 13], second | "except for some special cases" | p. 13: "We have not been able to prove the stability for n > 2 by this method, except for some special cases" | MATCHES |
| [5, p. 40] | D = 4, and D = 5 for a spherical horizon with Λ ≥ 0; D = 5 is one of the special cases | p. 40: "For n = 2, this is positive definite for m > 0. When K = 1, λ ≥ 0 and n = 3 … we can show that Ṽ_S₋ > 0" | MATCHES |
| [6] | the charge q "in units of the extremal charge"; up to 0.98, and 0.9 for D = 9–11 | p. 2: "the charge normalized by its extremal quantity q = Q/Q_ext < 1"; Table I (p. 3): rows q = 0 to 0.98, with no entry at 0.98 for D = 9, 10, 11 | MATCHES; note N5 |

Also seen at their anchors and matching, though not new: [5, p. 40] ("for scalar type perturbation, we were not
able to prove even the stability …"), [5, p. 43] ("there does not seem to be a systematic method …"), [4,
Table 1] ("D ≥ 6 ?"), [4, eqs. (76)–(77)], [1, eqs. (5.39), (5.58), (5.60), (5.62b)], and x_H = 2/(1 + √(1 − q²))
with extremality at |Q| = M, from (2.19).

## 3. Notes

**N1. One sentence of the source did not come over: that S is C¹ on ℝ.** `results/p3/METHOD.md` l.21 and l.26
say that S is smooth on ℝ because r* ↦ ρ is a diffeomorphism. Lemma 1 asks for S ∈ C¹(ℝ), and neither Lemma 2,
nor Appendix B.1, nor the sentence after Proposition 3 says that S = −f(1 − z)P has it. It does: P is C¹ on
(0, 1), and z is a smooth function of r* ∈ ℝ by Appendix B.2. *Suggest* adding to Lemma 2 or to B.1: "S is C¹ on
ℝ, since P is C¹ on (0, 1) and r ↦ r* is a diffeomorphism (Appendix B.2)."

**N2. "≈ 54.86" is rounded up.** 959747/17496 = 54.8552…, so §4.3's "m⁻³U₋ ≥ 959747/17496 ≈ 54.86" quotes a
lower bound above its value. It is copied faithfully from `results/a1/RESULT.md` l.39 ("≈ 54.86 m³"), but the
project's own rule is the other way: "A certified lower bound must be quoted rounded **down**"
(`results/hd/elementary/RESULT_ADDENDUM_1.md` l.13). The version I read cold had "(rounded down: 54.85)". The
exact fraction is in the text, so no claim is wrong. *Suggest* 54.85.

**N3. The last sentence of Appendix A is only partly supported by the listed files.** They show one independent
transcription of (5.62b) and (5.63b), Kimi's (`METHOD_ADDENDUM_1.md` l.49; the gate E0n of
`hd/elementary/PREREG.md` l.65, for n = 2, …, 12), and a comparison with the potential printed in another paper
(`METHOD_ADDENDUM_1.md` l.50), which is not a transcription of [1]. For the second transcription (the blind
replication of §6, I suppose) and for "checked in the Lean formalisation" my verdict is CANNOT TELL: nothing on
my list shows them. Item 1 above is one more comparison with the rendered page.

**N4. "HD-X-2's code checks all five."** The listed files show three conditions in the gate COVER (item 5).
Either point me to the lines of the code that check 0 < z₁ < 1 and 0 < μ₀ ≤ μ₁, or write "HD-X-2's code checks
the last three; the first two hold for the constants above".

**N5. Which extremal charge does [6] mean?** The paper's wording now follows [6] exactly, and [6] does not say
whether Q_ext is taken at fixed mass or at fixed horizon radius. It matters, because the sentence keeps the
letter q, which §2 defines as |Q|/M.
- [6] uses the same f as [1] and units r₊ = 1, in which "2M = 1 + Q² − …" (p. 2). At Λ = 0 the horizons are then
  at r^{n−1} = 1 and r^{n−1} = Q², so at fixed r₊ the extremal charge is Q_ext = 1.
- If that is [6]'s Q_ext, then q_[6] = Q and |Q|/M = 2q_[6]/(1 + q_[6]²): their 0.98 is 0.99980 in the paper's q,
  and their 0.9 is 0.99448. If Q_ext is taken at fixed M, the two q agree.
- CANNOT TELL from the text which it is. *Suggest* dropping the letter ("up to 0.98 of the extremal charge, in
  their normalisation"), or settling it from their Table I, as the comparison with [8] must already have done.

**N6. Three small things outside the nine items.**
- **§4.6, the remark on the critical bands.** "u₀ is the principal solution … at the degenerate horizon … Then
  no design can give N > 0 at q = 1." The conclusion needs u₀ to be principal at infinity as well. It is, since
  u₀ decays there and the other solution grows; with both ends the operator is critical and has no positive
  strict supersolution, which N > 0 would supply. The remark is marked as not used in the proof; it wants the
  four words "and at infinity".
- **§1, after the quotation of [1, p. 32].** "The deformations we use near q = 1 are regular at the horizon for
  each q < 1, but not uniformly." By my computation the function S itself vanishes at the horizon for every q,
  q = 1 included: there f ≈ (n − 1)²z² and P ≈ a/z, so S = −f(1 − z)P ≈ −(n − 1)²az. What has the pole at q = 1 is
  P, that is S/f, as §4.1 says ("P, and so S/f, is not regular"). A referee who holds the paper to the quoted
  sentence will ask which of the two is meant. *Suggest* S/f in §1 too.
- **Letters.** Appendix B.1's W := U₋/(64ρ²H₋²) is not the W := (log u₀)_{r*} of §4.6; Appendix B.3's P_n stands
  beside the design P; and B.3 uses ε and κ again without §4.3's "in this subsection only". In B.3 (a),
  "Dividing … by 4m" skips "after subtracting 1", as the source does.

## 4. What this check does not cover

- The records (JSON) and the result files that are not on the brief's list: Table 1's counts and degrees beyond
  the rows compared above, Appendix C's line ranges, and the outcome of G1.
- The Lean developments, and every statement that something is formally verified.
- The code, apart from the 62 lines of `code/ki/potentials.py`.
- The correctness of [1]'s eq. (5.63b) itself, of the exact computations, and of Theorems 1 and 2.
