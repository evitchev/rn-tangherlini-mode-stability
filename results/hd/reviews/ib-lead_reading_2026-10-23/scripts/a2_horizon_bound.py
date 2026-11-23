#!/usr/bin/env python3
"""A2 reading check, D = 6 (n = 4), l = 2, q -> 1 along TARGET_HD section 1's parametrisation (n = 4 case):
  A = 6 + mu^2, B = 7, w = B mu/A, s = 1 + 2 m delta = B((l + n) - (l - 1) mu^2)/((n + 1) A), m = 6,
  x_H = 2/(1 + w), k = x_H/x_- = (1 - w)/(1 + w), delta_t = 1 - k = 2w/(1 + w), f_z(0) = 3(1 - k) = 3 delta_t,
  W(0) = U_-(x_H)/(64 H_-(x_H)^2) (TARGET.md section 1, lines 23-24).
Prints, exactly then as decimals: q, delta_t, the inner horizon z_- = 1 - k^(-1/3) (float), W(0), and the horizon bound
W(0)/f_z(0), which any C^1 design must satisfy at z = 0 (N(0) >= 0 <=> P(0) <= W(0)/f_z(0)).
Also: c_n(l) and the q = 1 identity at n = 2, 3 (general-n U_- of code/ki/potentials.py, copied).
"""
from fractions import Fraction as F

import sympy as sp

x, m, d = sp.symbols("x m delta")
U6 = (-400000 * d * (1 + m*d)**3 * x**4 - 1600 * (1 + m*d)**2 * (50 * m * d - 16) * x**3
      + 7680 * m * (1 + m*d) * x**2 - 16 * m * (5 * m * (96 - 4*m) * d + 480) * x + 64 * m**3 + 384 * m**2)
H6 = m + 10 * (1 + m*d) * x
n, l, mm = 4, 2, 6
print("mu | q (decimal) | 1 - q | delta_t | z_- (inner horizon, float) | W(0) | horizon bound W(0)/f_z(0)")
for mu in (F(3, 25), F(1, 10), F(1, 100), F(1, 1000), F(1, 10000)):
    A = (l + n) + (l - 1) * mu * mu
    B = 2 * l + n - 1
    w = B * mu / A
    s = B * ((l + n) - (l - 1) * mu * mu) / ((n + 1) * A)
    dl = (s - 1) / (2 * mm)
    xH = 2 / (1 + w)
    k = (1 - w) / (1 + w)
    dt = 1 - k
    fz0 = 3 * dt
    sub = {m: mm, d: sp.Rational(dl.numerator, dl.denominator), x: sp.Rational(xH.numerator, xH.denominator)}
    W0 = sp.Rational(U6.subs(sub)) / (64 * sp.Rational(H6.subs(sub)) ** 2)
    hb = W0 / sp.Rational(fz0.numerator, fz0.denominator)
    q = float(1 - w * w) ** 0.5
    zm = 1 - float(k) ** (-1 / 3)
    print(f"{mu} | {q:.10f} | {1 - q:.3e} | {float(dt):.6g} | {zm:.6g} | {float(W0):.6g} | {float(hb):.6g}")

print("\n== q = 1, n = 2, 3: c_n(l) and N(0) for P = a/z + b0 + b1 z")
z, a, L = sp.symbols("z a ell")
b0, b1 = sp.symbols("b0 b1")


def U_minus(n, K=1):
    return (- n**3 * (3*n - 2) * (n + 1)**4 * d * (1 + m*d)**3 * x**4
            - 4 * n**2 * (n + 1)**2 * (1 + m*d)**2 * ((n + 1) * (3*n - 2) * m * d - n**2) * x**3
            + 4 * (n + 1) * (1 + m*d) * (m * (n - 2) * (n - 4) * (n + 1) * (m + n**2 * K) * d
                                         + 4 * n * (2*n**2 - 3*n + 4) * m
                                         + n**2 * (n - 2) * (n - 4) * (n + 1) * K) * x**2
            - 16 * m * ((n + 1) * m * (-4*m + 3 * n**2 * (n - 2) * K) * d
                        + 3 * n * (n - 4) * m + 3 * n**2 * (n + 1) * (n - 2) * K) * x
            + 64 * m**3 + 16 * n * (n + 2) * m**2 * K)


for n in (2, 3):
    sub = {m: (L - 1) * (L + n), d: 1 / ((L + n) * (n + 1))}
    X = 2 * (1 - z) ** (n - 1)
    Uz = U_minus(n).subs(sub).subs(x, X)
    Hz = (m + sp.Rational(n * (n + 1), 2) * (1 + m * d) * x).subs(sub).subs(x, X)
    f = (1 - (1 - z) ** (n - 1)) ** 2
    P = a / z + b0 + b1 * z
    N = Uz - 64 * Hz**2 * ((1 - z) * sp.diff(f, z) * P + f * (-P + (1 - z) * sp.diff(P, z) + P**2))
    Nc = sp.cancel(sp.together(sp.expand(N)))
    num, den = sp.fraction(Nc)
    N0 = sp.simplify(Nc.subs(z, 0))
    H2 = sp.simplify(Hz.subs(z, 0))
    cn = sp.factor(sp.simplify(Uz.subs(z, 0) / (64 * (n - 1) ** 2 * H2 ** 2)))
    ok = sp.simplify(N0 - 64 * (n - 1) ** 2 * H2 ** 2 * (cn - a * (a + 1))) == 0
    print(f"n = {n} (D = {n + 2}): z in denominator: {den.has(z)}; c_n = {cn}; identity: {ok}; "
          f"c_n + 1/4 = {sp.factor(cn + sp.Rational(1, 4))}; c_n at l = 2: {cn.subs(L, 2)}")
