"""Independent checks of the Lemma U Lean layer outside Lean (bh-modes BHM-052; session-L, 2026-10-23).

  [python-2]/bin/python3 -I -B check_lemmaU.py LEAN_FILE

LEAN_FILE is lean/BHModesLemmaU.lean; its definitions Um, Pos and Neg are read and parsed (no paths are printed).
Exact sympy except the sanity grid (8), which compares at 50 digits.
 1. The Lean definitions, parsed: Um is TARGET.md's U_- (n = 4), transcribed independently below.
 2. The split: eps^6 U_-(x; m = eps^-2, delta = kappa eps) = Pos - Neg, as polynomials.
 3. Pos and Neg have positive coefficients; Pos(0, 0, 0) = 64.
 4. Neg is RESULT.md Part II's nine monomials (l. 36-37, transcribed).
 5. kappa: (1 + 2 m delta)^2 - (1 + 4 m q^2/25) = 4m (delta + m delta^2 - q^2/25), so (delta sqrt m)^2 = q^2/25 - delta.
 6. The corner: Neg(1/12, 1/5, 2) = 159997/17496 and 64 - Neg = 959747/17496 (RESULT.md l. 38-39); 1/12 >= 150^(-1/2).
 7. RESULT.md's control NC-A1d: 64 - Neg(1/2, 1/5, 2) = -33488.
 8. Sanity grid: U_- >= m^3 * 959747/17496 for l in {11, 12, 15, 30, 100}, q in {0, 1/2, 9/10, 99/100, 1},
    x in {0, 1/2, 1, 3/2, 2}, with TARGET.md's delta >= 0 from (1 + 2 m delta)^2 = 1 + 4 m q^2/25.
"""

import re
import sys

import sympy as sp

e, k, x, m, d, q = sp.symbols('e k x m d q')
NAMES = {'ε': 'e', 'κ': 'k', 'δ': 'd'}


def lean_def(text, name):
    """The body of `def name (...) : ℝ :=`, up to the next blank line, as a sympy expression."""
    i = text.index(f'def {name} (')
    body = ' '.join(text[i:].split(':=', 1)[1].split('\n\n', 1)[0].split())
    for g, a in NAMES.items():
        body = body.replace(g, a)
    return sp.sympify(body.replace('^', '**'), locals={'e': e, 'k': k, 'x': x, 'm': m, 'd': d})


def U_target(m_, d_, x_):        # TARGET.md section 1, U_- (S5 (5.63b) at n = 4), transcribed here independently
    return (-400000 * d_ * (1 + m_ * d_)**3 * x_**4 - 1600 * (1 + m_ * d_)**2 * (50 * m_ * d_ - 16) * x_**3
            + 7680 * m_ * (1 + m_ * d_) * x_**2 - 16 * m_ * (5 * m_ * (96 - 4 * m_) * d_ + 480) * x_ + 64 * m_**3 + 384 * m_**2)


NEG_RESULT = [(7680, 3, 1, 1), (7680, 4, 0, 1), (80000, 3, 3, 3), (134400, 4, 2, 3), (28800, 5, 1, 3),
              (400000, 4, 4, 4), (1200000, 5, 3, 4), (1200000, 6, 2, 4), (400000, 7, 1, 4)]   # (c, eps, kappa, x)


def main(lean_path):
    text = open(lean_path, encoding='utf-8').read()
    Um, Pos, Neg = (lean_def(text, n) for n in ('Um', 'Pos', 'Neg'))
    res = {}
    res['1 Lean Um = TARGET U_-'] = sp.expand(Um - U_target(m, d, x)) == 0
    split = sp.expand(e**6 * U_target(1 / e**2, k * e, x) - (Pos - Neg))
    res['2 split eps^6 U_-(1/eps^2, kappa eps, x) = Pos - Neg'] = split == 0
    pc, nc = sp.Poly(Pos, e, k, x).coeffs(), sp.Poly(Neg, e, k, x).coeffs()
    res['3 Pos coefficients > 0 (6 terms)'] = len(pc) == 6 and all(c > 0 for c in pc)
    res['3 Neg coefficients > 0 (9 terms)'] = len(nc) == 9 and all(c > 0 for c in nc)
    res['3 Pos(0, 0, 0) = 64'] = Pos.subs({e: 0, k: 0, x: 0}) == 64
    res['4 Neg = RESULT.md nine monomials'] = sp.expand(Neg - sum(c * e**a * k**b * x**cx for c, a, b, cx in NEG_RESULT)) == 0
    res['5 kappa: (1+2md)^2 - (1+4mq^2/25) = 4m(d + m d^2 - q^2/25)'] = sp.expand(
        (1 + 2 * m * d)**2 - (1 + 4 * m * q**2 / 25) - 4 * m * (d + m * d**2 - q**2 / 25)) == 0
    corner = Neg.subs({e: sp.Rational(1, 12), k: sp.Rational(1, 5), x: 2})
    res['6 Neg(1/12, 1/5, 2) = 159997/17496'] = corner == sp.Rational(159997, 17496)
    res['6 64 - Neg(1/12, 1/5, 2) = 959747/17496'] = 64 - corner == sp.Rational(959747, 17496)
    res['6 1/12 >= 150^(-1/2), i.e. 144 <= 150'] = sp.Rational(1, 12) >= 1 / sp.sqrt(150)
    res['7 NC-A1d: 64 - Neg(1/2, 1/5, 2) = -33488'] = 64 - Neg.subs({e: sp.Rational(1, 2), k: sp.Rational(1, 5), x: 2}) == -33488
    worst, ok = None, True
    for l in (11, 12, 15, 30, 100):
        mv = sp.Integer((l - 1) * (l + 4))
        for qv in (0, sp.Rational(1, 2), sp.Rational(9, 10), sp.Rational(99, 100), 1):
            dv = (sp.sqrt(1 + 4 * mv * qv**2 / 25) - 1) / (2 * mv)
            for xv in (0, sp.Rational(1, 2), 1, sp.Rational(3, 2), 2):
                r = sp.N(U_target(mv, dv, xv) / mv**3 - sp.Rational(959747, 17496), 50)
                ok = ok and r >= 0
                worst = r if worst is None or r < worst else worst
    res['8 sanity grid: U_-/m^3 - 959747/17496 >= 0 (125 points)'] = ok
    print('8 smallest U_-/m^3 - 959747/17496 on the grid: %.6f' % float(worst))
    for key, v in res.items():
        print(f'{key}: {v}')
    allok = all(res.values())
    print('ALL LEMMA U CHECKS HOLD' if allok else 'A CHECK FAILED')
    return 0 if allok else 1


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1]))
