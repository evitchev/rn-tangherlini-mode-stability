"""The lead's spot check of Kimi's HD-X control (e) and (a), with the registered HD-X-2 code (6cedd44).

(e): band D = 7, l = 2 at mu = 1/64, on Kimi's support [209/10000, 837/10000] with b = ((z - za)(zb - z))^2:
  - C = int b^3 dz exactly, and whether it is (157/2500)^13/12012;
  - U_- < 0 on the support, exactly (no root of U_-'s numerator in [za, zb], and its sign at the midpoint);
  - A = Q[b] and Q = A - K C in Arb, with nc_bound_a's integrand (critical.py) and Kimi's K = 297809182.
(a): U_-(x_H) and H_-(x_H) at q = 1 for D = 7, l = 3.
Usage: python lead_check_hdx_e.py SRC/code
"""
import sys

sys.path.insert(0, sys.argv[1])

import sympy as sp
from flint import acb, ctx

from hd.elementary import U_of
from hd.scert import z
from hdx import critical as cr
from ki.potentials import H_minus, d, m, x
from onset.bernstein import Q
from onset.onset import mu

n, ell = 5, 2
dz = cr.design(n, ell, "none")
U, H = cr.potentials(n, ell, "none")
b = cr.build(n, ell, U, H, dz)
mc = sp.Rational(1, 64)
sub = {mu: mc}
za, zb = sp.Rational(209, 10000), sp.Rational(837, 10000)
bexpr = (z - za) ** 2 * (zb - z) ** 2

C = sp.integrate(sp.expand(bexpr ** 3), (z, za, zb))
print("C exact =", C)
print("C == (157/2500)^13/12012:", C == sp.Rational(157, 2500) ** 13 / 12012)
print("C ~", sp.N(C, 40))

Ud_c = sp.Rational(b["Ud"].as_expr().subs(sub))
Un_c = sp.Poly(sp.expand(b["Un"].as_expr().subs(sub)), z)
sgn = 1 if Ud_c > 0 else -1
mid = (za + zb) / 2
print("roots of U_-'s numerator in [za, zb]:", Un_c.count_roots(za, zb),
      "| sign of U_- at the midpoint:", sp.sign(sgn * Un_c.eval(mid)),
      "| U_- at z = 0:", sgn * Un_c.eval(0) / abs(Ud_c))
lo_roots = Un_c.intervals(inf=0, sup=1, eps=sp.Rational(1, 10 ** 12))
print("first root of U_- in (0, 1) lies in", [str(v) for v in min(lo_roots)[0]])

ctx.prec = 256
polys = {"kn": sp.Poly(sp.expand(b["fn"].as_expr().subs(sub) * (1 - z) ** 2 * sp.diff(bexpr, z) ** 2), z),
         "Un": Un_c, "Hn": sp.Poly(sp.expand(b["Hn"].as_expr().subs(sub)), z),
         "b2": sp.Poly(sp.expand(bexpr ** 2), z), "b3": sp.Poly(sp.expand(bexpr ** 3), z)}
cf = {key: [acb(Q(c)) for c in pl.all_coeffs()[::-1]] for key, pl in polys.items()}
fd_c = acb(Q(sp.Rational(b["fd"].as_expr().subs(sub))))
Hd2 = acb(Q(sp.Rational(b["Hd"].as_expr().subs(sub)))) ** 2
Ud_a = acb(Q(Ud_c))


def horner(cs, t):
    acc = acb(0)
    for c in reversed(cs):
        acc = acc * t + c
    return acc


def energy(t, analytic):
    Hv = horner(cf["Hn"], t)
    return horner(cf["kn"], t) / fd_c + horner(cf["Un"], t) * Hd2 / (64 * Ud_a * Hv * Hv) * horner(cf["b2"], t)


A = acb.integral(energy, acb(Q(za)), acb(Q(zb)))
Cb = acb.integral(lambda t, analytic: horner(cf["b3"], t), acb(Q(za)), acb(Q(zb)))
K = 297809182
print("A =", A.real.str(30, radius=True))
print("C (Arb) =", Cb.real.str(30, radius=True))
print("Q = A - K C =", (A - K * Cb).real.str(30, radius=True), "| < 0:", bool((A - K * Cb).real < 0))

u3 = U_of(5, "none")
h3 = H_minus(5)
vals = {x: 2, m: (3 - 1) * (3 + 5), d: sp.Rational(1, (5 + 1) * (3 + 5))}
print("(a) D = 7, l = 3, q = 1: U_-(x_H) =", sp.nsimplify(u3.subs(vals)), "| H_-(x_H) =", sp.nsimplify(h3.subs(vals)))
