"""Cross-check: buildN (rf route) vs a direct sympy build of N for the 7-2 first box,
evaluated at mu = 13/100 (exact).  Must agree on every z-coefficient.
"""
import json
import os
import sys
from fractions import Fraction

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "[kimi-folder]/bhm-p3-audit-2026-10-22/own")
from rfg import Ctx
from buildN import build_N
from build import ki_Usymbol

z = sp.symbols("z")


def main():
    with open("[repository]/results/hd/s/runs/record/7-2/result.json") as fh:
        d = json.load(fh)
    box = d["boxes"][0]
    n, ell = 5, 2
    m = (ell - 1) * (ell + n)
    mu = sp.Rational(13, 100)

    # route 1: my rf machinery, evaluated at mu
    ctx = Ctx(ell, n)
    Den, Nt, E = build_N(ctx, box)
    N_rf_at = {}   # z-coefficients at mu (Y = 1 - z): evaluate then expand to z
    for yexp, poly in Nt.items():
        v = Fraction(0)
        for j, c in poly.items():
            v += c * Fraction(13, 100) ** j
        # Y^yexp = (1 - z)^yexp
        for k in range(yexp + 1):
            coef = v * Fraction((-1) ** k) * sp.binomial(yexp, k)
            N_rf_at[k] = N_rf_at.get(k, Fraction(0)) + Fraction(coef)
    Den_at = sum(c * Fraction(13, 100) ** j for j, c in Den.items())

    # route 2: direct sympy at mu
    ell_, n_ = ell, n
    Bc = 2 * ell_ + n_ - 1
    A = (ell_ + n_) + (ell_ - 1) * mu**2
    w = Bc * mu / A
    s = Bc * ((ell_ + n_) - (ell_ - 1) * mu**2) / ((n_ + 1) * A)
    delta = (s - 1) / (2 * m)
    xH = 2 / (1 + w)
    q2 = 1 - w**2
    mm, dd, xx = sp.symbols("m d x")
    Ux, Hx = ki_Usymbol(n_)
    Ux = sp.expand(Ux.subs({mm: m, dd: delta}))
    Hx = sp.expand(Hx.subs({mm: m, dd: delta}))
    x_expr = xH * (1 - z) ** (n_ - 1)
    U = sp.expand(Ux.subs(xx, x_expr))
    H = sp.expand(Hx.subs(xx, x_expr))
    f = sp.expand(1 - x_expr + q2 * x_expr**2 / 4)
    P = sp.Integer(0)
    for key, val in box["P"].items():
        i, j = eval(key)
        P += sp.Rational(val) * z**i * sp.Rational(13, 100) ** j
    fz = sp.diff(f, z)
    Pz = sp.diff(P, z)
    N_sym = sp.expand(U - 64 * H**2 * ((1 - z) * fz * P + f * (-P + (1 - z) * Pz + P**2)))

    # compare N_rf_at / Den_at with N_sym
    bad = []
    for k in range(0, 120):
        a = N_rf_at.get(k, Fraction(0))
        b = N_sym.coeff(z, k)
        if sp.expand(sp.Rational(a.numerator, a.denominator) - b * sp.Rational(Den_at.numerator, Den_at.denominator)) != 0:
            bad.append(k)
    print("Den(mu) =", Den_at, " > 0:", Den_at > 0)
    print("mismatching coefficients:", bad[:10], " total", len(bad))
    print("CROSSCHECK:", "OK" if not bad else "FAILED")


if __name__ == "__main__":
    main()
