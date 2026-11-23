# Working notes, A1 (Lemma U(n)); written before reading anything barred.
Object: results/hd/elementary/PREREG.md §2 E3 and §3 Part II (a)-(d); U_- from code/ki/potentials.py (S5 (5.63b), y = 0).
Derivation checked by pencil:
- Substitution m = eps^-2, delta = kappa eps: a monomial m^a delta^b x^c of U_- becomes eps^(b-2a) kappa^b x^c; times eps^6: eps^(6-2a+b). The largest a is 3, only in 64 m^3 (b = 0, c = 0) and in m^3 delta^b with b >= 1 (x-term: +64(n+1) m^3 delta; x^2: m^3 delta^2; x^3: m^3 delta^3; x^4: m^3 delta^4). So every exponent of eps is >= 0, eps^6 U_- is a polynomial in (eps, kappa, x), and its eps^0 part is exactly 64: Pos_n(0) = 64. The split Pos - Neg by the sign of each coefficient is unique.
- Pos_n(eps, kappa, x) >= 64 for eps, kappa, x >= 0 (nonnegative coefficients), so U_- = m^3 (Pos - Neg) >= m^3 (64 - Neg_n(eps, kappa, x)).
- (a) (1 + 2 m delta)^2 = 1 + 4 m q^2/(n+1)^2 gives delta + m delta^2 = q^2/(n+1)^2 with delta >= 0 (positive root); kappa^2 = m delta^2 <= m delta^2 + delta = q^2/(n+1)^2 <= 1/(n+1)^2 for q in [0, 1]. So kappa <= 1/(n+1), including q = 1.
- (b) x_H = 2/(1 + sqrt(1 - q^2)) <= 2 for q in [0, 1]; the lemma is stated on [0, 2] directly.
- (c) m(l) = (l - 1)(l + n) increases for l >= 1; l > l0 gives m >= m(l0 + 1); eps = m^(-1/2) <= 1/sqrt(m(l0+1)) <= 1/isqrt(m(l0+1)) = eps-bar (isqrt <= sqrt). Rational, uniform in q and x.
- (d) a polynomial with nonnegative coefficients is nondecreasing in each variable on [0, infinity): Neg_n(eps, kappa, x) <= Neg_n(eps-bar, 1/(n+1), 2).
- Chain: U_- >= m^3 (64 - Neg_n(eps-bar, 1/(n+1), 2)); the lemma holds whenever that number is > 0, which is the certified part at the found l0(n). f > 0 on the exterior and H_- = m + n(n+1)(1 + m delta) x/2 >= m > 0 give V the sign of U_-.
Verdict (to be entered): SOUND. Hypotheses assumed: the certified corner value > 0 at l0(n) (machine, not re-run here); the transcription gate E0n; the search rule for l0 (a bound, not a sharp threshold). No fix needed; one wording remark: "Pos_n(0) = 64" means at eps = 0 for every (kappa, x), which the degree count justifies and the text could state.
