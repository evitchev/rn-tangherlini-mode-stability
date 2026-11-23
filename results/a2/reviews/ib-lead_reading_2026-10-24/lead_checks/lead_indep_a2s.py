"""The lead's independent check of A2-S's polynomial and of its positivity at fixed charges (not bh-modes code).
N is built here from TARGET.md section 1 as printed (U_-, H_-, f, x, delta), the design as registered in PREREG section 2
(P = a(1 + eps)/(z + eps) + p0, a = -2/5, eps = w/(3(1 + w))), and the Chebyshev coefficients of the sealed pilot record
(float.hex -> exact, sum c_j T_j(2z - 1), c_0 not halved).  N = U - 64 H^2 [(1 - z) f_z P + f(-P + (1 - z) P_z + P^2)]
(METHOD's N = Lean's Nz).  The only bh-modes input besides the record is the labelling w = sqrt(1 - q^2) = 7 mu/(6 + mu^2).
(1) Exact identity against bh-modes' NL/(S^2 L) (their a2.scert.parts, imported from the 25c796e byte copy): as
    polynomials in z at mu = 0, 1/64, 1/8, and at 30 rational points (z, mu), throat points z = mu*zeta included.
(2) Exact Sturm root counts (sympy count_roots) of N (z + eps)^2 on the CLOSED interval [0, 1] at fixed mu, and its sign
    at z = 1/2.  0 roots and a positive sign mean N > 0 on [0, 1] at that charge.  Independent of Bernstein.
usage: lead_indep_a2s.py TREE PILOT_RECORD"""
import json
import random
import sys
import time
from fractions import Fraction

import sympy as sp

TREE, REC = sys.argv[1], sys.argv[2]
z = sp.Symbol("z")
ELL = 2
m = sp.Integer((ELL - 1) * (ELL + 4))
a = sp.Rational(-2, 5)
rec = json.load(open(REC))
cheb = [Fraction.from_float(float.fromhex(v)) for v in rec["design"]["cheb"]]
u = 2 * z - 1
Tch = [sp.Integer(1), u]
while len(Tch) < len(cheb):
    Tch.append(sp.expand(2 * u * Tch[-1] - Tch[-2]))
p0 = sp.expand(sum(sp.Rational(c.numerator, c.denominator) * Tch[j] for j, c in enumerate(cheb)))
print(f"design: a = {a}, degree {sp.degree(p0, z)}, {len(cheb)} Chebyshev coefficients, beta0 = {rec['design'].get('beta0')}")


def lead_N(muv):
    """N(z) at the charge labelled by mu (a rational), as an exact sympy expression in z; and eps."""
    w = 7 * muv / (6 + muv ** 2)
    q2 = 1 - w ** 2
    s = sp.sqrt(1 + 4 * m * q2 / 25)                    # (1 + 2 m delta)^2 = 1 + 4 m q^2/25
    assert s.is_Rational, s
    delta = (s - 1) / (2 * m)
    assert delta >= 0
    xH = 2 / (1 + w)
    x = xH * (1 - z) ** 3
    f = 1 - x + q2 * x ** 2 / 4
    H = m + 10 * (1 + m * delta) * x
    U = (-400000 * delta * (1 + m * delta) ** 3 * x ** 4 - 1600 * (1 + m * delta) ** 2 * (50 * m * delta - 16) * x ** 3
         + 7680 * m * (1 + m * delta) * x ** 2 - 16 * m * (5 * m * (96 - 4 * m) * delta + 480) * x + 64 * m ** 3 + 384 * m ** 2)
    eps = w / (3 * (1 + w))
    P = a * (1 + eps) / (z + eps) + p0
    N = U - 64 * H ** 2 * ((1 - z) * sp.diff(f, z) * P + f * (-P + (1 - z) * sp.diff(P, z) + P ** 2))
    return N, eps, q2


sys.path.insert(0, TREE + "/code")
from a2 import scert as sc                                  # noqa: E402  (comparison only)
from ki.potentials import H_TARGET, U_TARGET                # noqa: E402
from onset.onset import mu as MU                            # noqa: E402
zz = sc.z
p0b, _ = sc.design(TREE)
E, en, ed, S, Pi, NL = sc.parts(U_TARGET, H_TARGET, p0b, sc.A_RES)
Lp = sp.Poly(E.L.as_expr(), zz, MU)


def theirs_N_poly(muv):
    """bh-modes' NL(z, mu)/(eps_d^2 L) at fixed mu, as a polynomial in z; equals N (z + eps)^2."""
    nl = sp.Poly(NL.as_expr().subs(MU, muv), zz)
    edv = sp.Rational(sp.sympify(ed).subs(MU, muv))
    lv = sp.Rational(Lp.as_expr().subs({MU: muv, zz: 0}))
    assert sp.Poly(Lp.as_expr(), zz).degree() <= 0 if Lp.as_expr().has(zz) is False else True
    return sp.Poly((nl.as_expr() / (edv ** 2 * lv)).subs(zz, z), z)


print("\n(1) identity, as polynomials in z")
for muv in (sp.Integer(0), sp.Rational(1, 64), sp.Rational(1, 8)):
    t0 = time.time()
    N, eps, q2 = lead_N(muv)
    mine = sp.Poly(sp.cancel(N * (z + eps) ** 2) if eps != 0 else sp.cancel(N * z ** 2), z)
    th = theirs_N_poly(muv)
    print(f"  mu = {muv}: q^2 = {q2}; eps = {eps}; degree {mine.degree()}; mine - theirs == 0: {(mine - th).is_zero}"
          f"  ({time.time() - t0:.1f} s)")

print("\n(1') identity at 30 rational points (z, mu)")
random.seed(20261024)
pts = [(sp.Rational(random.randint(1, 999), 1000), sp.Rational(random.randint(0, 125), 1000)) for _ in range(20)]
for muv in (sp.Rational(1, 1000), sp.Rational(1, 64), sp.Rational(1, 33)):
    for zeta in (sp.Rational(1, 2), sp.Integer(2), sp.Integer(7)):
        pts.append((muv * zeta, muv))
pts.append((sp.Rational(1, 7), sp.Integer(0)))
bad = 0
for (zv, muv) in pts:
    N, eps, _ = lead_N(muv)
    mine = sp.Rational(N.subs(z, zv))
    nl = sp.Rational(NL.as_expr().subs({zz: zv, MU: muv}))
    sv = sp.Rational(S.as_expr().subs({zz: zv, MU: muv}))
    lv = sp.Rational(Lp.as_expr().subs({zz: zv, MU: muv}))
    th = nl / (sv ** 2 * lv)
    bad += (mine != th)
print(f"  {len(pts)} points, mismatches: {bad}")

print("\n(2) Sturm: real roots of N (z + eps)^2 on the closed interval [0, 1], and the sign at z = 1/2")
for muv in (sp.Integer(0), sp.Rational(1, 10 ** 6), sp.Rational(1, 10 ** 4), sp.Rational(1, 1000), sp.Rational(1, 100),
            sp.Rational(1, 32), sp.Rational(1, 16), sp.Rational(1, 10), sp.Rational(1, 8)):
    t0 = time.time()
    N, eps, q2 = lead_N(muv)
    num = sp.Poly(sp.cancel(N * (z + eps) ** 2), z) if eps != 0 else sp.Poly(sp.cancel(N), z)
    k = num.count_roots(0, 1)
    sgn = sp.sign(num.eval(sp.Rational(1, 2)))
    lo = min(float(num.eval(sp.Rational(j, 200))) for j in range(0, 201))
    print(f"  mu = {str(muv):>9}: q^2 = {float(q2):.12f}; polynomial {'N' if eps == 0 else 'N (z + eps)^2'} of degree "
          f"{num.degree()}; roots in [0, 1]: {k}; sign at 1/2: {sgn}; min on a 201-point grid (float, info) {lo:.6g}"
          f"  ({time.time() - t0:.1f} s)")
