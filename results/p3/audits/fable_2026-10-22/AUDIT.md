# AUDIT: the p3 S-certificate method (bh-modes BHM-022, `results/p3/METHOD.md`), a pencil audit with a code and a Lean reading

Seat: Fable (session-R secondary), audit seat in gaps, on the session-R lead's queue message of
2026-10-22. Brief: `results/p3/briefs/BRIEF_fable_2026-10-22.md`, sha256
`5f59fdbe52950e43fd368834907298d702cf892d515c1e10ac5fbf6a4b366293` (verified against bh-modes' `SEALED.sha256`, as were
TARGET.md, TARGET_ADDENDUM_1.md, results/onset/PREREG.md, results/p3/PREREG.md, results/p3/PREREG_ADDENDUM_1.md and
results/p3/METHOD.md). Started 2026-10-22 20:02 EDT (AUDIT_START.txt), filed about 20:20 EDT, in a gap of a B3-CONV run;
well inside the 2-3 h box. Workspace `[fable-folder]/bhm-p3-audit/`; nothing written under `[repository]`.

**Read:** the six artifacts; `code/p3/scert.py` in full, `code/onset/bernstein.py` in full, `code/ki/potentials.py` in full,
`onset.param` in `code/onset/onset.py` (commit 094591c as the brief names); for task 3 only, after tasks 1 and 2:
`lean/lean_p3_sdeformation_2026-10-22/README.md`, `lean/BHModesP3.lean` in full, and the summary lines of its
`lean/BUILD_LOG.txt`. **Not read (anti-anchoring, as instructed):** results/p3/RESULT.md, RULE2_RESULT.md,
diagnosis_G1.*, runs/, rule2/, REGISTRY rows BHM-023 onward, outbox/, anything under `[deliveries]/` other than my own
1c delivery folder, `[kimi-folder]/`, `[session-R-folder]/bh-modes_2026-10-22/`. S5 itself (Kodama-Ishibashi) was not
opened; its transcription is a trust-base item (sec. 6).

**Machine spot checks of the hand work** (`spotchecks_p3.py`, `spotchecks_p3b.py` with logs; nothing from `code/` imported):
Lemma 2's identity for generic f(rho), P(z) (symbolic); the factorisation f = (1 - x/x_H)(1 - x/x_-), kappa^3 = x_H/x_- =
(1 - w)/(1 + w), f_z(0) = 3(1 - kappa^3); the mu-parametrisation identity s^2 = 1 + 4 m q^2/25 for general l and its
monotonicity at l = 2; N(1) and the -3 < P(1) < 4 window; the epsilon identity of the remark; N_times_L's algebra with and
without the `extra` term; the Bernstein conversion formula after the affine map, in one and two variables (reconstruction,
enclosure, corners). All pass. `spotchecks_p3.log` shows one FAIL that is my own test constant (84 written for 168 in the
derivative of s(mu)); `spotchecks_p3b.py` re-runs that item with the derivative printed, PASS. The parametrisation was never in
doubt.

## Overall verdict

**SOUND.** Lemma 1, Lemma 2 and Proposition 3 are correct as written and prove what the certificates need: N >= 0 on [0, 1]
(for each mu in a box) implies the quadratic form of A_{l,q} >= 0 on C_0^infty(R). The code's trust base (`parts`,
`N_times_L`, `verify`, `prove_sign`) proves N > 0 on the closed box for exactly METHOD's N, and the Bernstein enclosure is a
valid proof of strict positivity on a closed box, edges and bisection included. The Lean theorems `prop3` and `prop3_D6` say
what Proposition 3 needs, and none of the README's exclusions is a real gap. No ERROR, no GAP-MAJOR. GAP-MINOR items, all
wording or hygiene: (1) Lemma 2's diffeomorphism claim is asserted without its one-line reason (sec. 2); (2) the "why such P
exist" remark's positivity sentence is not a theorem and is false for G1, as PREREG_ADDENDUM_1 already records (sec. 4);
(3) `onset.bernstein.Q` would convert a float through its decimal string (not exercised in the trust path) (sec. 5);
(4) E0 compares two transcriptions by the same hand (sec. 6); (5) a README wording nit (sec. 7).

## 1. Lemma 1 (S-deformation identity) and the Corollary: SOUND

- For S real and C^1, |phi' + S phi|^2 = |phi'|^2 + S (|phi|^2)' + S^2 |phi|^2 (the cross term is S (phi' conj(phi) + phi
  conj(phi')) = S (|phi|^2)'). Integrating S (|phi|^2)' by parts over R gives -int S' |phi|^2 with no boundary terms because phi
  has compact support; S' is continuous, so every integrand is continuous with compact support and integrable. Rearranging
  gives the identity. Correct.
- Corollary: V + S' - S^2 >= 0 pointwise on R makes both right-hand integrals >= 0, so the form is >= 0 on C_0^infty(R). "So A >= 0"
  is TARGET.md section 2's reading of A as the self-adjoint operator determined by the form on C_0^infty: a form that is >= 0
  on a form core has a >= 0 closure, so the operator it determines is >= 0 and has no negative eigenvalue. For V bounded and
  continuous (TARGET.md section 1) there is no ambiguity about which operator this is: -d^2/dr*^2 + V is essentially
  self-adjoint on C_0^infty(R) and its closure is the form operator. Correct.

## 2. Lemma 2 (the ansatz): SOUND, one wording item

- **The diffeomorphism r* -> rho (the brief's first question).** f > 0 on (1, infinity) for every q in [0, 1] (f = (1 -
  x/x_H)(1 - x/x_-) with 0 < x < x_H <= x_-; spot check 2), so r*(rho) = int drho/f is C^infty and strictly increasing with a
  C^infty inverse (inverse function theorem, derivative f > 0). It is onto R: at the horizon f has a simple zero for q < 1
  (f_z(0) = 3(1 - kappa^3) > 0, kappa^3 = (1 - w)/(1 + w) < 1 iff w > 0 iff q < 1), so r* diverges like log(rho - 1) to
  -infinity; for q = 1 the zero is double and r* diverges like -1/(rho - 1), still to -infinity; at infinity f -> 1 and r* ->
  +infinity. So the claim holds for every q in [0, 1), near the horizon included, and in fact at q = 1 too. METHOD states it
  in one clause without the reason. GAP-MINOR (wording): add "f > 0 on (1, infinity), f(1) = 0 and f -> 1, so r* is strictly
  increasing and diverges at both ends".
- **S is C^1 on R (the second question).** S = -f(rho) P(1 - 1/rho)/rho is a polynomial in 1/rho (f = 1 - x_H rho^-3 + q^2
  x_H^2 rho^-6/4), so it is C^infty on (1, infinity); composed with the C^infty map r* -> rho it is C^infty on R, hence C^1, which
  is all Lemma 1 uses. The integration by parts has no boundary terms because phi has compact support in R; the behaviour of S
  at r* -> +-infinity (it tends to 0 at both ends) is not even needed. Correct.
- **First form and change of variable (the third question).** With d/dr* = f d/drho: S_{r*} = -f(f' beta + f beta'), so V-tilde
  = f [W - f' beta - f(beta' + beta^2)], W = U/(64 rho^2 H^2). With z = 1 - 1/rho, dz/drho = (1 - z)^2, f' = (1 - z)^2 f_z,
  beta = (1 - z) P, beta' = (1 - z)^2 (-P + (1 - z) P_z), and rho (1 - z) = 1: rho^2 f' beta = (1 - z) f_z P, rho^2 f beta' =
  f(-P + (1 - z) P_z), rho^2 f beta^2 = f P^2, rho^2 W = U/(64 H^2). Hence rho^2 V-tilde/f = N/(64 H^2), i.e. V-tilde = f N/(64
  rho^2 H^2) with METHOD's N. Verified symbolically for generic f and P (spot check 1). Correct. x = x_H (1 - z)^3 is
  x = 2M/r^3 with x = x_H at r = r_H = 1. Correct.
- **Endpoints.** z = 1: f = 1, (1 - z) f_z -> 0, P_z finite, U(0) = 64 m^3 + 384 m^2, H(0) = m, so N(1) = 64 m^2 (m + 6 - P(1)^2 +
  P(1)), positive for m = 6 iff -3 < P(1) < 4 (spot check 4). z = 0: f(0) = 0, so N(0) = U(x_H) - 64 H(x_H)^2 f_z(0) P(0).
  Correct. Because the identity is pointwise and phi has compact support, no tail lemma is needed: N >= 0 on the open (0, 1)
  already suffices, and the certificate's closed [0, 1] is more.

## 3. Proposition 3: SOUND

On the exterior (0 < z < 1) f > 0, rho > 0 and H_- = m + 10(1 + m delta) x >= m > 0 (delta >= 0, x > 0), so N >= 0 gives
V-tilde >= 0 on all of R, and the Corollary applies with the C^1 S of Lemma 2. Correct. The "every mu in the box" version
(Remark, sec. 4) is this proposition applied at each mu.

## 4. The Remarks

- **Endpoints included:** SOUND (sec. 2).
- **Why such P exist:** the identity is correct, N(P_true - eps) = 64 H^2 eps [(1 - z) f_z + f(2 P_true - 1 - eps)] when
  N(P_true) = 0, and rho f' = (1 - z) f_z (spot check 5). The sentence "which is > 0 for small eps where psi_1 > 0" is not a
  consequence of the identity: the bracket (1 - z) f_z + f(2 P_true - 1) can be negative where psi_1 decreases (P_true < 0),
  and PREREG_ADDENDUM_1 records that it reaches -1.288 for G1 while staying >= 0.992 for T1. GAP-MINOR (wording, no effect
  on any certificate since the design is untrusted): restate as "positive where that bracket is, which the planning data show
  for the D = 6 band and the addendum's diagnosis refutes for G1; design rule 2 removes the dependence".
- **Parameter boxes (the fourth question):** SOUND. For a fixed mu, N(., mu) >= 0 on [0, 1] iff N(., mu) Den(mu) >= 0 when
  Den(mu) > 0, so Proposition 3 holds at q(mu) for every mu in the box, provided that the setting at mu (x_H(mu), delta(mu),
  kappa^3(mu)) is the physical one at q(mu). It is: onset/PREREG.md section 1's parametrisation gives s^2 = 1 + 4 m q^2/25
  identically in (l, mu) (spot check 3), w increases from 0 to 1 on [0, 1] (q decreases from 1 to 0), s decreases from 7/5 to
  1 at l = 2 (delta >= 0), and kappa^3 = x_H/x_- = (1 - w)/(1 + w) (spot check 2). In the code the positive factor is L =
  Ud Hd^2 fd and L > 0 is itself proved by Bernstein on the box (sec. 5), so Den > 0 is not assumed.

## 5. The trust base in code (task 2): SOUND, one hygiene item

- **`setting`.** U = U_TARGET and H = H_TARGET from `ki/potentials.py` are TARGET.md section 1's U_- and H_- term by term (I
  compared all five coefficients of U and both of H). E0 raises unless `U_minus(4)` (the general-n transcription of S5
  (5.63b)) equals U_TARGET exactly; I also checked by hand that U_minus(4) reproduces TARGET's five coefficients and that
  H_minus(4) = m + 10(1 + m delta) x. For D6, `param(2)` gives A, w, s, m, delta = (s - 1)/(2m), x_H = 2/(1 + w) and q^2 = 1 -
  w^2 exactly as onset/PREREG.md section 1; kappa^3 = (1 - w)/(1 + w); x = x_H (1 - z)^3; f = (1 - (1 - z)^3)(1 - kappa^3 (1 -
  z)^3), which equals TARGET's 1 - x + q^2 x^2/4 (spot check 2). For G1: n = 8, m = (l - 1)(l + n) = 10 = l(l + n - 1) - n,
  x = (1 - z)^7, f = 1 - x, delta = 0, as PREREG section 2 registers.
- **`parts`.** Splits U, H, f into numerator and denominator after `cancel(together(.))` and refuses a denominator that
  depends on z; so f_z = fn_z/fd exactly. Correct.
- **`N_times_L`.** Returns (Un Hd^2 fd - 64 Hn^2 Ud [(1 - z) fn_z P + fn(-P + (1 - z) P_z + P^2)], Ud Hd^2 fd). With U = Un/Ud,
  H = Hn/Hd, f = fn/fd this is exactly N L with L = Ud Hd^2 fd, and with `extra` it is (N - 64 H^2 extra) L (spot check 6).
  For NC-P1 (b), V + W with W = -K_p f b/rho^2 has V-tilde_W = f (N - 64 H^2 K_p b)/(64 rho^2 H^2), so `extra = K_p b` is the right
  modification. Correct.
- **`verify`.** Proves L > 0 on the mu-box and N L > 0 on [0, 1] x [a, b] (both strict, by `prove_sign`), hence N > 0 on the
  closed box, which is stronger than Proposition 3's N >= 0. At a point, mu is substituted exactly before `parts`. For G1 the
  mu-interval is degenerate, harmless (the affine map to a point gives constant Bernstein rows). Correct.
- **`prove_sign` (bernstein.py).** On each closed subbox the polynomial is the convex combination of its Bernstein coefficients
  (the basis functions are >= 0 and sum to 1), so all coefficients > 0 proves p > 0 on the closed subbox, edges and corners
  included (the corner values ARE the corner coefficients). The subboxes are closed and cover the parent; bisection is
  depth-limited and an undecided leaf raises (REJECT, fail-closed); a corner with sign p <= 0 raises with an exact
  counterexample. The conversion power basis -> Bernstein after the affine map, b_k = sum_{i <= k} C(k, i)/C(d, i) a_i, and
  its tensor-product form in (t, mu) are the standard formulas; I re-implemented them in Fractions and checked reconstruction,
  the enclosure property and the corner values on random polynomials (spot check 7). The arithmetic is python-flint `fmpq`,
  exact. Valid.
- **GAP-MINOR (hygiene).** `Q(v)` converts anything that is not a Fraction through `Fraction(str(v))`; for a float this is the
  decimal repr, not the binary value. The trust path never passes a float (box endpoints are Fractions or ints, P's
  coefficients are converted exactly by `Fraction(float)` in `cheb_to_monomial`, sympy Rationals print exactly), so nothing is
  affected; make `Q` reject floats so that this stays true.
- **Not checked here:** the design step (untrusted by registration); the recorded certificates and their re-verification
  (Kimi's brief); the `pieces` logic beyond reading it; `qnm1c.common` and `onset.onset.build`.

## 6. Trust base: GAP-MINOR, one addition

E0 compares TARGET.md's U_- with `U_minus(4)`, the same author's transcription of S5's general-n formula. It catches a
discrepancy between the two (TD-P1 shows it does) but not a common transcription error; the known-answer gate G1 (S6: Q = 0
stable, where the certificate has to pass through a negative region of V) is the empirical guard against that, and the
S-certificate's result also inherits S5's reduction to the master equation (TARGET.md's "physical reading"). State it once:
"the trust base includes S5 (5.59)-(5.63) as transcribed in `ki/potentials.py` and TARGET.md section 1". The rest (python-flint
exact rationals, sympy's exact `cancel`/`Poly`, the code's correctness, fail-closed verdicts) is as PREREG section 1 states.

## 7. Statement fidelity of the Lean layer (task 3): FAITHFUL; no exclusion is a real gap

- `sdef_identity` is Lemma 1 for complex phi in C^1 with compact support (C_0^infty is a special case), V continuous, S real
  with continuous derivative S' everywhere: exactly the identity, with the first integral bracketed (the README's caught slip).
  `form_nonneg_of_sdef` is the Corollary (V + S' - S^2 >= 0 everywhere gives the form >= 0).
- `ansatz_identity` is Lemma 2's computation at a point rho != 0 with H(z) != 0: V + f(dS/drho) - S^2 = f Nz/(64 rho^2 H^2) with
  f' = (1 - z)^2 F', beta = (1 - z) P, beta' = (1 - z)^2 (-P + (1 - z) P'); `Nz` is METHOD's N verbatim; `zc_hasDerivAt`,
  `f_hasDerivAt`, `beta_hasDerivAt`, `Srho_hasDerivAt` are the derivative facts of Lemma 2's proof; `rho_fprime` is rho f' =
  (1 - z) f_z.
- `prop3`: hypotheses F, P in C^1 (everywhere), U, H continuous, R : R -> R with dR/dt = F(zc(R t)) and R t > 1 for all t, F >= 0
  and H != 0 on (0, 1), Nz >= 0 on (0, 1); conclusion 0 <= int (|phi'|^2 + Vrho(R t) |phi|^2) for every C^1 compactly supported
  complex phi, with Vrho = F U/(64 rho^2 H^2) at z = zc(rho). This is Proposition 3 for the operator in r* (the variable t),
  with N >= 0 needed only on the open interval (weaker hypothesis, stronger theorem). Its proof is METHOD's: S(t) = Srho(R t),
  the chain rule through dR/dt = F, Lemma 1, the ansatz identity, and the signs.
- `prop3_D6`: with `Hm`, `Um` TARGET.md's H_- and U_- (checked term by term against TARGET.md section 1), `xH q` = 2/(1 +
  sqrt(1 - q^2)), `x6` = x_H (1 - z)^3, `F6` = 1 - x + q^2 x^2/4, `F6'` its z-derivative (checked), it discharges F6's derivative
  and continuity, U6, H6 continuity, F6 > 0 on (0, 1) for q^2 <= 1 (`F6_pos`), H6 > 0 for m > 0, delta >= 0 (`H6_pos`), leaving
  as hypotheses: q^2 <= 1, m > 0, delta >= 0, P in C^1, the map R, and Nz >= 0 on (0, 1). `Vrho_D6` and `F6_zc_TARGET` identify
  its V and f with TARGET.md's in units r_H = 1. For a certificate at q = q(mu): m = 6 > 0, delta(mu) >= 0 (sec. 4), P is a
  polynomial, and the code's N equals this Nz because the factorised f equals F6 and f_z equals F6' (spot check 2), with
  delta(mu) and x_H(mu) exact. So `prop3_D6`'s hypotheses and conclusion say what Proposition 3 needs for item (c).
- **The exclusions, one by one.** (i) Existence of the inverse tortoise map R: standard and shown in sec. 2 (f > 0 on (1,
  infinity), divergence at both ends); `prop3` holds for every such R, and the physical statement needs one R, which exists. Not
  a gap. (ii) C^infty: Lemma 1 needs C^1 only; METHOD's C^infty is more than used. Not a gap. (iii) Scaling from r_H = 1: under
  r = r_H rho, r* = r_H rho*, the form scales by r_H^-1 and V by r_H^-2 with x dimensionless, so positivity is invariant. Not a
  gap. (iv) "That the form determines A": TARGET.md section 2's definition, as in sec. 1 above; for bounded continuous V it is
  the unique self-adjoint realisation. Not a gap. (v) N >= 0 for a concrete P: item (c), the certificates. Not a gap of the
  method. The Remarks `N_at_horizon(_D6)`, `N_at_infinity_D6`, `N_at_infinity_ell2`, `N_eps_shift` match sec. 2 and sec. 4.
- **GAP-MINOR (README wording).** "prop3_D6 discharges every hypothesis except R and N >= 0" leaves out q^2 <= 1, m > 0, delta
  >= 0 and P in C^1, which remain hypotheses (all trivially met by the physical data). Say so.
- **Not re-done here:** the build. The folder's own `lean/BUILD_LOG.txt` reports Lean 4.24.0, exit 0, 0 errors, 0 warnings, 0
  sorry, and 27/27 theorems on {propext, Classical.choice, Quot.sound}; I read those lines and did not re-run the build or the
  mutations (statement fidelity was the task).

## 8. Hypotheses this audit had to assume

1. S5's (5.59)-(5.63) are transcribed correctly in `ki/potentials.py` and TARGET.md section 1 (S5 not opened); the
   physical reading (S5's reduction to master equations) is TARGET.md's and outside the method.
2. python-flint's `fmpq`/`fmpq_poly` and sympy's `cancel`, `fraction`, `Poly`, `expand` are exact and correct.
3. The code as read at commit 094591c is the code that produced the records (Kimi's object), and the design step is
   untrusted by registration, so its correctness is irrelevant to the certificates.
4. The Lean build log's claims (compile, axioms, mutations) hold as recorded; not re-run.
5. q in (0, 1) for the simple horizon zero (only the diffeomorphism's divergence uses it, and q = 1 diverges too); m > 0 and
   delta >= 0 for the physical data (verified for the l = 2 parametrisation, sec. 4).
6. The definition of A_{l,q} as the form operator (TARGET.md section 2).

## 9. Files

AUDIT.md (this file); spotchecks_p3.py, spotchecks_p3.log (exit 1: my test constant, sec. "Machine spot checks");
spotchecks_p3b.py, spotchecks_p3b.log (exit 0); AUDIT_START.txt. Hashes in SHA256SUMS (which does not list itself).
