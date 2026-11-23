#!/usr/bin/env python3
"""A2 reading check: METHOD.md's N at the degenerate horizon (q = 1), for P with a simple pole at z = 0.

N := U - 64 H^2 [(1 - z) f_z P + f(-P + (1 - z) P_z + P^2)]   (results/p3/METHOD.md, Lemma 2)
in units r_H = 1, z = 1 - 1/rho, x = x_H (1 - z)^(n-1); at q = 1: x_H = 2, f = (1 - (1 - z)^(n-1))^2,
delta = 1/((l + n)(n + 1)) (n = 4: 1/(5(l + 4)), TARGET_A2 E1).

D = 6 formulas copied from TARGET.md section 1 (lines 23-24); general-n U_- copied from
code/ki/potentials.py U_minus (lines 33-42).  Consistency check only, not an independent transcription.
"""
import sympy as sp

z, a, l = sp.symbols("z a ell")
b = sp.symbols("b0:4")
x, m, d = sp.symbols("x m delta")

U6 = (-400000 * d * (1 + m*d)**3 * x**4
      - 1600 * (1 + m*d)**2 * (50 * m * d - 16) * x**3
      + 7680 * m * (1 + m*d) * x**2
      - 16 * m * (5 * m * (96 - 4*m) * d + 480) * x
      + 64 * m**3 + 384 * m**2)
H6 = m + 10 * (1 + m*d) * x


def U_minus(n, K=1):
    return (- n**3 * (3*n - 2) * (n + 1)**4 * d * (1 + m*d)**3 * x**4
            - 4 * n**2 * (n + 1)**2 * (1 + m*d)**2 * ((n + 1) * (3*n - 2) * m * d - n**2) * x**3
            + 4 * (n + 1) * (1 + m*d) * (m * (n - 2) * (n - 4) * (n + 1) * (m + n**2 * K) * d
                                         + 4 * n * (2*n**2 - 3*n + 4) * m
                                         + n**2 * (n - 2) * (n - 4) * (n + 1) * K) * x**2
            - 16 * m * ((n + 1) * m * (-4*m + 3 * n**2 * (n - 2) * K) * d
                        + 3 * n * (n - 4) * m + 3 * n**2 * (n + 1) * (n - 2) * K) * x
            + 64 * m**3 + 16 * n * (n + 2) * m**2 * K)


def H_minus(n):
    return m + sp.Rational(n * (n + 1), 2) * (1 + m * d) * x


def N_extremal(n, U, H, P):
    sub = {m: (l - 1) * (l + n), d: 1 / ((l + n) * (n + 1))}
    X = 2 * (1 - z) ** (n - 1)
    Uz = U.subs(sub).subs(x, X)
    Hz = H.subs(sub).subs(x, X)
    f = (1 - (1 - z) ** (n - 1)) ** 2
    fz = sp.diff(f, z)
    return Uz - 64 * Hz**2 * ((1 - z) * fz * P + f * (-P + (1 - z) * sp.diff(P, z) + P**2)), Uz, Hz


print("== D = 6 (n = 4), q = 1, TARGET.md's U_-, H_-")
n = 4
P = a / z + b[0] + b[1] * z + b[2] * z**2
N, Uz, Hz = N_extremal(n, U6, H6, P)
Nt = sp.together(sp.expand(N))
num, den = sp.fraction(Nt)
print("denominator of N (after together):", sp.factor(den))
N0 = sp.limit(N, z, 0) if den.has(z) else sp.simplify(N.subs(z, 0))
N0 = sp.factor(sp.simplify(sp.cancel(sp.together(sp.expand(N)).subs(z, 0)))) if not den.has(z) else sp.factor(N0)
H2 = sp.simplify(Hz.subs(z, 0))
print("H_-(x_H = 2) =", sp.factor(H2))
c = sp.Rational(1, 9) * l * (l - 3)
claim = 576 * H2**2 * (c - a * (a + 1))
print("N(0) - 576 H(2)^2 (c - a(a+1)), c = l(l-3)/9:", sp.simplify(N0 - claim))
print("N(0)/(576 H(2)^2) at a = -1/2:", sp.factor(sp.simplify((N0 / (576 * H2**2)).subs(a, sp.Rational(-1, 2)))),
      " vs (2l-3)^2/36:", sp.simplify((N0 / (576 * H2**2)).subs(a, sp.Rational(-1, 2)) - (2*l - 3)**2 / 36))
print("bounded P (a = 0): N(0) = U(x_H) =", sp.factor(sp.simplify(N0.subs(a, 0))), "; at l = 2:", N0.subs({a: 0, l: 2}))
print("l = 2: H(2) =", H2.subs(l, 2), "; N(0) at a = -1/2:", sp.simplify(N0.subs({a: sp.Rational(-1, 2), l: 2})),
      "; window: N(0) > 0 iff a in", sp.solve(sp.Eq(c.subs(l, 2) - a*(a+1), 0), a))
print("l = 3: N(0) at a = 0:", sp.simplify(N0.subs({a: 0, l: 3})), "; at a = -1/2:", sp.simplify(N0.subs({a: sp.Rational(-1, 2), l: 3})))

print("\n== general n at q = 1 (potentials.U_minus), n = 4..9, l symbolic")
for n in range(4, 10):
    Pn = a / z + b[0] + b[1] * z
    Nn, Uzn, Hzn = N_extremal(n, U_minus(n), H_minus(n), Pn)
    numn, denn = sp.fraction(sp.together(sp.expand(Nn)))
    N0n = sp.simplify(sp.cancel(sp.together(sp.expand(Nn))).subs(z, 0))
    H2n = sp.simplify(Hzn.subs(z, 0))
    cn = sp.factor(sp.simplify(Uzn.subs(z, 0) / (64 * (n - 1)**2 * H2n**2)))
    ok = sp.simplify(N0n - 64 * (n - 1)**2 * H2n**2 * (cn - a * (a + 1))) == 0
    ok2 = sp.simplify(cn - l * (l - n + 1) / sp.Integer(n - 1)**2) == 0
    margin = sp.factor(sp.simplify(cn + sp.Rational(1, 4)))
    print(f"n = {n} (D = {n + 2}): N has z in denominator: {denn.has(z)}; c_n(l) = {cn} (= l(l-n+1)/(n-1)^2: {ok2}); "
          f"N(0) = 64(n-1)^2 H(2)^2 (c_n - a(a+1)): {ok}; c_n + 1/4 = {margin}; at l = 2: {sp.simplify(margin.subs(l, 2))}")
