"""Lead drills on A2-S (bh-modes 25c796e byte copy; read-only imports; nothing in the tree is edited).
Each drill monkeypatches one input of a2.scert and runs its own main(), which prints the per-check lines and the verdict.
  D0  sharp zero margin: a = -2/5 kept, U -> U - (16/25) H^2 x^4, so c' = -2/9 - 4/225 = -6/25 = a(a+1) exactly
  D1  gate S: the pole moved inside the exterior (eps_n -> -eps_n, i.e. P = a(1-eps)/(z-eps) + p0)
  D2  gate DIV-T: the throat chart divided by mu^3 instead of mu^2
  D3  gate G-RES: g_res's comparison run on a U whose x = 2 value is changed (U + x^4)
  D5  nc-bound's planted potential W - K b (K = 3403781, b = ((z-1/20)(1/5-z))^2) run through all four charts, every mu
  D6  a planted throat defect that vanishes at mu = 0: NL - K mu (z - mu)(3 mu - z), K = 128 T(2, 1/64), so that
      T(2, 1/64) is made negative while T(zeta, 0) is unchanged
usage: drills.py TREE OUTROOT DRILL"""
import os
import sys
TREE, OUT, DRILL = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, TREE + "/code")
import sympy as sp
from a2 import scert as sc
from ki.potentials import H_TARGET, U_TARGET, x, m, d
from onset.onset import mu
z = sc.z
orig_parts, orig_chart_T = sc.parts, sc.chart_T
out = os.path.join(OUT, DRILL)
argv = ["--out", out, "--root", TREE]

if DRILL == "D0":
    sys.exit(sc.main(argv, UH=(U_TARGET - sp.Rational(16, 25) * H_TARGET**2 * x**4, H_TARGET)))

if DRILL == "D1":
    def parts_flip(U, H, p0, a):
        E, en, ed, S, Pi, NL = orig_parts(U, H, p0, a)
        en = -en
        S = sp.Poly(ed * z + en, z, mu)
        Pi = sp.Poly(a * (ed + en) + p0.as_expr() * (ed * z + en), z, mu)
        Sz = sp.Poly(ed, z, mu)
        one_z = sp.Poly(1 - z, z, mu)
        br = (one_z * E.fzn * Pi * S + E.fn * (-Pi * S + one_z * (Pi.diff(z) * S - Sz * Pi) + Pi ** 2))
        NL = E.A0 * S ** 2 - E.HU * br
        return E, sp.expand(en), sp.expand(ed), S, Pi, NL
    sc.parts = parts_flip
    sys.exit(sc.main(argv))

if DRILL == "D2":
    def chart_T3(NL, divide=True):
        o = {}
        for (i, j), c in NL.terms():
            o[(i, i + j)] = o.get((i, i + j), 0) + c
        ok = all(j >= 3 for (_, j) in o)
        return {(i, j - 3): c for (i, j), c in o.items()}, ok
    sc.chart_T = chart_T3
    sys.exit(sc.main(argv))

if DRILL == "D3":
    ell, a, b0, b1 = sp.symbols("ell a b0 b1")
    mm, dl = (ell - 1) * (ell + 4), 1 / (5 * (ell + 4))
    y = (1 - z) ** 3
    for lab, UU in (("untampered (= g_res)", U_TARGET), ("tampered U + x^4", U_TARGET + x**4)):
        U = UU.subs({m: mm, d: dl, x: 2 * y})
        H = H_TARGET.subs({m: mm, d: dl, x: 2 * y})
        f = (1 - y) ** 2
        P = a / z + b0 + b1 * z
        N = U - 64 * H ** 2 * ((1 - z) * sp.diff(f, z) * P + f * (-P + (1 - z) * sp.diff(P, z) + P ** 2))
        num, den = sp.fraction(sp.cancel(sp.together(N)))
        H2 = sp.factor(H_TARGET.subs({m: mm, d: dl, x: 2}))
        diff = sp.cancel(num.subs(z, 0) / den - 576 * H2 ** 2 * (ell * (ell - 3) / sp.Integer(9) - a * (a + 1)))
        print(f"G-RES comparison, {lab}: poly in z {not den.has(z)}; diff = {diff}; gate {'PASS' if (not den.has(z) and diff == 0) else 'FAIL'}")
    sys.exit(0)

if DRILL == "D5":
    K = sp.Integer(3403781)
    b = (z - sc.ZA) ** 2 * (sc.ZB - z) ** 2
    def parts_bound(U, H, p0, a):
        E, en, ed, S, Pi, NL = orig_parts(U, H, p0, a)
        NL = NL - sp.Poly(K * b, z, mu) * E.HU * E.fd * S ** 2
        return E, en, ed, S, Pi, NL
    sc.parts = parts_bound
    sys.exit(sc.main(argv))

if DRILL == "D6":
    p0, deg = sc.design(TREE)
    E, en, ed, S, Pi, NL = orig_parts(U_TARGET, H_TARGET, p0, sc.A_RES)
    T, _ = sc.chart_T(NL)
    zt = sp.Symbol("zeta")
    Texpr = sum(c * zt ** i * mu ** j for (i, j), c in T.items())
    T2 = sp.Rational(Texpr.subs({zt: 2, mu: sp.Rational(1, 64)}))
    K = sp.ceiling(128 * T2)
    print(f"D6: T(2, 1/64) = {float(T2):.6g}; K = 128 T(2, 1/64) rounded up = {K}")
    def parts_throat(U, H, p0_, a):
        E_, en_, ed_, S_, Pi_, NL_ = orig_parts(U, H, p0_, a)
        return E_, en_, ed_, S_, Pi_, NL_ - sp.Poly(K * mu * (z - mu) * (3 * mu - z), z, mu)
    sc.parts = parts_throat
    sys.exit(sc.main(argv))
print("unknown drill"); sys.exit(2)
