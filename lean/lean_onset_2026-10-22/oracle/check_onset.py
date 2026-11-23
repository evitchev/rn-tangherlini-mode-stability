"""Independent checks of item (b) outside Lean, and a cross-check against the bh-modes onset record (session-L, 2026-10-22).

  [python-2]/bin/python3 -I -B check_onset.py RECORD_JSON

RECORD_JSON is bh-modes results/onset/runs/record/main/result.json (read only; this script prints no paths).
Exact sympy except where noted.
 1. U_- straight from TARGET.md at rational points (t, mu), against F(t, mu)/((mu + 1)^3 (mu + 6)) of the Lean file.
 2. g(mu) = F(1, mu) = 1024 (mu + 15) p(mu); p and C irreducible over Q; one real root each; q_* to 30 digits.
 3. The record: its minimal polynomials are the same strings; its 45-digit mu_* interval lies inside
    (0.19893240974, 0.19893240975); its q_* decimal lies in (0.9730564367, 0.9730564368); its degree-104 g is my g times
    a polynomial with no root in [0, 1].
 4. O4: the bracket 2m - 10(1 + m delta) x_H equals 4(4mu - 3)/(mu + 1).
 5. A sanity grid (exact rationals): F >= 0 for mu in [mu_hi, 1], t in [0, 1], and F(1, mu) < 0 for mu in [0, mu_lo].
"""

import json
import sys
from fractions import Fraction

import sympy as sp

t, mu, Y = sp.symbols('t mu Y')
F = (-10240 * t**4 * mu**4 + 194560 * t**4 * mu**3 - 1290240 * t**4 * mu**2 + 3317760 * t**4 * mu - 2211840 * t**4
     + 38912 * t**3 * mu**4 - 466944 * t**3 * mu**3 + 1419264 * t**3 * mu**2 - 221184 * t**3 * mu + 663552 * t**3
     - 36864 * t**2 * mu**4 + 184320 * t**2 * mu**3 + 1105920 * t**2 * mu + 1327104 * t**2
     - 9216 * t * mu**4 - 18432 * t * mu**3 - 645120 * t * mu**2 - 1271808 * t * mu - 635904 * t
     + 27648 * mu**4 + 248832 * mu**3 + 580608 * mu**2 + 525312 * mu + 165888)          # lean/BHModesOnset.lean `Fp`
p = 10 * mu**3 - 11 * mu**2 + 228 * mu - 45
C = 3025 * Y**3 - 31521 * Y**2 + 99792 * Y - 68796
LO, HI = sp.Rational(19893240974, 10**11), sp.Rational(19893240975, 10**11)


def Um(m, d, x):
    return (-400000 * d * (1 + m * d)**3 * x**4 - 1600 * (1 + m * d)**2 * (50 * m * d - 16) * x**3 + 7680 * m * (1 + m * d) * x**2
            - 16 * m * (5 * m * (96 - 4 * m) * d + 480) * x + 64 * m**3 + 384 * m**2)


def main(record_path):
    res = {}
    # 1. TARGET.md's U_- at rational points
    ok = True
    for mv in (sp.Rational(1, 7), sp.Rational(1, 5), sp.Rational(1, 2), sp.Rational(9, 10), sp.Integer(1)):
        w = 7 * mv / (6 + mv**2)
        q2 = 1 - w**2
        d = (sp.sqrt(1 + 24 * q2 / 25) - 1) / 12          # TARGET.md's delta from q, positive root
        d = sp.nsimplify(sp.radsimp(d))
        xH = 2 / (1 + sp.sqrt(1 - q2))
        for tv in (sp.Integer(0), sp.Rational(1, 3), sp.Rational(7, 8), sp.Integer(1)):
            lhs = sp.nsimplify(sp.radsimp(Um(6, d, tv * xH)))
            rhs = F.subs({t: tv, mu: mv}) / ((mv + 1)**3 * (mv + 6))
            ok = ok and sp.simplify(lhs - rhs) == 0
    res['1 TARGET U_- = F/Den at 20 rational points'] = ok
    # 2. factorisation, irreducibility, roots
    res['2 F(1, mu) = 1024 (mu + 15) p(mu)'] = sp.expand(F.subs(t, 1) - 1024 * (mu + 15) * p) == 0
    res['2 p irreducible over Q'] = len(sp.factor_list(p)[1]) == 1 and sp.factor_list(p)[1][0][1] == 1
    res['2 C irreducible over Q'] = len(sp.factor_list(C)[1]) == 1 and sp.factor_list(C)[1][0][1] == 1
    res['2 p has one real root, in (LO, HI)'] = len(sp.real_roots(p)) == 1 and sp.Poly(p, mu).count_roots(LO, HI) == 1
    res['2 C has one real root'] = len(sp.real_roots(C)) == 1
    qstar = sp.sqrt(sp.real_roots(C)[0]).evalf(30)
    print('q_* =', qstar)
    # 3. the record
    rec = json.load(open(record_path, encoding='utf-8'))
    res['3 record minimal polynomial of mu_*'] = rec['minimal_poly_mu'] == '10*mu**3 - 11*mu**2 + 228*mu - 45'
    res['3 record minimal polynomial of q_*^2'] = rec['minimal_poly_q2'] == '3025*Y**3 - 31521*Y**2 + 99792*Y - 68796'
    a, b = (Fraction(s) for s in rec['mu_star_interval'])
    res['3 record mu_* interval inside (LO, HI)'] = Fraction(19893240974, 10**11) < a <= b < Fraction(19893240975, 10**11)
    qd = [Fraction(s) for s in rec['q_star_decimal']]
    res['3 record q_* decimal inside (0.9730564367, 0.9730564368)'] = all(
        Fraction('0.9730564367') < v < Fraction('0.9730564368') for v in qd)
    grec = sp.Poly([sp.Integer(c) for c in rec['g_coeffs']], mu)
    Qt, R = sp.div(grec, sp.Poly(1024 * (mu + 15) * p, mu))
    res['3 record g = my g * cofactor, exactly'] = R.is_zero
    res['3 cofactor has no root in [0, 1]'] = R.is_zero and Qt.count_roots(0, 1) == 0
    print('record g degree', grec.degree(), '; cofactor degree', Qt.degree())
    # 4. O4
    d = (1 - mu**2) / (5 * (6 + mu**2))
    xH = 2 * (6 + mu**2) / ((mu + 1) * (mu + 6))
    res['4 bracket = 4(4mu - 3)/(mu + 1)'] = sp.simplify(12 - 10 * (1 + 6 * d) * xH - 4 * (4 * mu - 3) / (mu + 1)) == 0
    # 5. sanity grid
    grid_ok = True
    for i in range(41):
        mv = HI + (1 - HI) * sp.Rational(i, 40)
        for j in range(41):
            grid_ok = grid_ok and F.subs({t: sp.Rational(j, 40), mu: mv}) >= 0
    for i in range(41):
        grid_ok = grid_ok and F.subs({t: 1, mu: LO * sp.Rational(i, 40)}) < 0
    res['5 sanity grid'] = grid_ok
    for k, v in res.items():
        print(f'{k}: {v}')
    allok = all(res.values())
    print('ALL ONSET CHECKS HOLD' if allok else 'A CHECK FAILED')
    return 0 if allok else 1


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1]))
