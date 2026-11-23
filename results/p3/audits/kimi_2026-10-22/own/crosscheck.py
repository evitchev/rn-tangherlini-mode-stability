"""Cross-check: the rf.py/box route vs the sympy route, at mu = 1/6 with T1's P.
The two N's must be identical as polynomials in z with rational coefficients.
"""
import json
import os
import sys
from fractions import Fraction

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rf import p_eval, p_mul, p_pow, FACTORS
from make_boxes import P_to_PY, build_N_rf
from make_N import D6, build_N, load_P

HERE = os.path.dirname(os.path.abspath(__file__))
z = sp.symbols("z")


def rf_value(r, muval):
    n, e = r
    val = p_eval(n, muval)
    for i in range(3):
        fv = p_eval(FACTORS[i], muval)
        val /= fv ** e[i]
    return val


def main():
    muval = Fraction(1, 6)
    d = load_P(os.path.join(HERE, "..", "runs", "cert_rule1_T1.json"))
    # route 1: sympy
    U, H, f = D6(sp.Rational(1, 6))
    P = sp.Integer(0)
    for key, val in d["P"].items():
        i, j = eval(key)
        P += sp.Rational(val) * z**i
    N_sym_e = sp.expand(build_N(U, H, f, P))
    N_sym = {i: N_sym_e.coeff(z, i) for i in range(70)}
    N_sym = {i: c for i, c in N_sym.items() if c != 0}
    # route 2: rf machinery, evaluated at mu = 1/6
    PY = P_to_PY(d["P"])
    N_rf = build_N_rf(PY)   # Y-dict of rf, Y = 1 - z
    # convert to z-polynomial with rational coefficients
    N2 = {}
    for yexp, r in N_rf.items():
        c = rf_value(r, muval)          # Fraction
        # Y^yexp = (1 - z)^yexp
        for k in range(yexp + 1):
            coef = c * sp.binomial(yexp, k) * (-1) ** k
            N2[k] = N2.get(k, sp.Rational(0)) + sp.Rational(coef.numerator, coef.denominator)
    # compare
    allkeys = set(N2) | set(N_sym)
    bad = []
    for k in allkeys:
        a = N2.get(k, sp.Rational(0))
        b = N_sym.get(k, sp.Rational(0))
        if sp.expand(a - b) != 0:
            bad.append((k, a, b))
    if bad:
        print("CROSSCHECK FAILED:", bad[:5])
        return 1
    print("CROSSCHECK OK: rf route == sympy route,",
          len(allkeys), "coefficients compared")


if __name__ == "__main__":
    raise SystemExit(main())
