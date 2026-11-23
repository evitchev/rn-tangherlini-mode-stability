"""A2-S symbolic gate G-RES and the controls (Kimi).

G-RES: at q = 1, P = a/z + b0 + b1 z:  N(0) = 576 H_-(2)^2 (l(l-3)/9 - a(a+1)),
derived here symbolically in (ell, a, b0, b1) from my own transcription.

Controls:
(a) A2-E's check at ell = 2 on [0,1] x [0, mu_lo(2)] must REJECT (corner value -115200);
(b) strict bound for ell = 3 on its full box must fail with value exactly 0 at (1, 0);
(c) design with a = -7/10 must REJECT (residue outside the window);
(d) zero-margin: a = -2/3 makes N's corner limit exactly 0, rest positive; a strict check
    must refuse;
(e) planted bound state in the throat at q = 1: b = ((z-1/20)(1/5-z))^2 on
    z in [1/20, 1/5] (r in [20/19, 5/4]); Q[b] < 0 certified by rigorous acb integration
    over the whole support with the quadratic form's weights; the certificate at mu = 0
    against V + W must then REJECT;
(f) verifier tamper: KAT suite.
"""
import json
import os
import sys
from fractions import Fraction

import sympy as sp
from flint import acb, fmpq

sys.path.insert(0, "[kimi-folder]/bhm-p3-audit-2026-10-22/own")
sys.path.insert(0, "[kimi-folder]/bhm-a1-audit-2026-10-23/own")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rfg import Ctx
from a2s import build, to_fmpq2, chebyshev_p0
from part1 import build_F, mu_lo_of
from verify import verify_1d, verify_2d, kat
from build import ki_Usymbol

HERE = os.path.dirname(os.path.abspath(__file__))


def gres():
    """N(0) at q=1 with P = a/z + b0 + b1 z, symbolic in ell, a, b0, b1."""
    ell, a, b0, b1, z = sp.symbols("ell a b0 b1 z")
    m = (ell - 1) * (ell + 4)
    delta = 1 / (5 * (ell + 4))
    mm, dd = sp.symbols("m d")
    Ux, Hx = ki_Usymbol(4)
    U2 = sp.expand(Ux.subs({mm: m, dd: delta, sp.Symbol("x"): 2}))      # U_-(x_H), q = 1
    H2v = sp.expand(Hx.subs({mm: m, dd: delta, sp.Symbol("x"): 2}))
    f = (1 - (1 - z) ** 3) ** 2
    P = a / z + b0 + b1 * z
    fz = sp.diff(f, z)
    bracket = (1 - z) * fz * P + f * (-P + (1 - z) * sp.diff(P, z) + P ** 2)
    lim = sp.limit(bracket, z, 0)
    N0 = sp.simplify(U2 - 64 * H2v ** 2 * lim)
    claim = 576 * H2v ** 2 * (ell * (ell - 3) / 9 - a * (a + 1))
    assert sp.simplify(N0 - claim) == 0, (sp.simplify(N0), claim)
    print("G-RES: N(0) = 576 H_-(2)^2 (l(l-3)/9 - a(a+1))  (symbolic in l, a; b0, b1 drop out):")
    print("  derived lim_{z->0} bracket =", sp.simplify(lim), " (independent of b0, b1)")


def main():
    gres()
    design = json.load(open(os.path.join(HERE, "..", "data", "design.json")))

    # ---- (a) A2-E at ell = 2
    ctx2 = Ctx(2, 4)
    F2, Den2, _ = build_F(ctx2)
    mlo2 = mu_lo_of(ctx2)
    F2f = {}
    for t, poly in F2.items():
        for j, c in poly.items():
            if c:
                F2f[(t, j)] = fmpq(c.numerator, c.denominator)
    okA, iA = verify_2d(F2f, fmpq(0), fmpq(1), fmpq(0), fmpq(mlo2.numerator, mlo2.denominator))
    # corner value F(1, 0) = Den(0) * U_-(2) = -115200 * Den(0)
    corner = sum(c for t, poly in F2.items() for j, c in poly.items() if j == 0)
    corner = sum(c for t, poly in F2.items() if t == 0 for c in poly.values())  # F(t=1): sum over t
    F10 = sum(c for t, poly in F2.items() for j, c in poly.items() if j == 0)   # wrong; fix below
    F10 = sum(sum(p2.values()) for t2, p2 in F2.items())  # no: F(1,0) = sum_{t} c_{t,0}
    F10 = sum(poly.get(0, Fraction(0)) for t2, poly in F2.items())
    print(f"(a) ell=2: verify -> {'REJECT (correct)' if not okA else 'PASS (BAD)'}; "
          f"F(1,0) = {F10} (= U_-(x_H) * Den(0) at q=1)")
    ok_a = (not okA) and F10 < 0

    # ---- (b) strict bound for ell = 3 must fail with value exactly 0 at (1, 0)
    ctx3 = Ctx(3, 4)
    F3, Den3, _ = build_F(ctx3)
    F3f = {}
    for t, poly in F3.items():
        for j, c in poly.items():
            if c:
                F3f[(t, j)] = fmpq(c.numerator, c.denominator)
    okB, iB = verify_2d(F3f, fmpq(0), fmpq(1), fmpq(0),
                        fmpq(mu_lo_of(ctx3).numerator, mu_lo_of(ctx3).denominator))
    F310 = sum(poly.get(0, Fraction(0)) for t2, poly in F3.items())
    print(f"(b) ell=3 strict: {'REJECT (correct)' if not okB else 'PASS (BAD)'} {iB}; "
          f"F(1,0) = {F310} (exactly 0: {F310 == 0})")
    ok_b = (not okB) and F310 == 0

    # ---- (c) a = -7/10
    Den, Nc, E = build(Ctx(2, 4), design["cheb"], a=Fraction(-7, 10))
    Cc = {}
    for i, poly in Nc.items():
        for j, c in poly.items():
            CC = {}
            NC = {}
            NC[(i + j, j)] = c
    # charts C and T for the tampered design
    NT = {}
    for i, poly in Nc.items():
        for j, c in poly.items():
            NT[(i, i + j)] = NT.get((i, i + j), Fraction(0)) + c
    T = {}
    divokT = True
    for (iz, im), c in NT.items():
        if im < 2:
            divokT = False
        else:
            T[(iz, im - 2)] = c
    NCd = {}
    for i, poly in Nc.items():
        for j, c in poly.items():
            NCd[(i + j, j)] = NCd.get((i + j, j), Fraction(0)) + c
    Cp = {}
    divokC = True
    for (iz, isg), c in NCd.items():
        if iz < 2:
            divokC = False
        else:
            Cp[(iz - 2, isg)] = c
    oks = []
    if divokT:
        okT, iT = verify_2d({k: fmpq(v.numerator, v.denominator) for k, v in T.items() if v},
                            fmpq(0), fmpq(8), fmpq(0), fmpq(1, 32))
        oks.append(("T", okT, iT))
    if divokC:
        okC, iC = verify_2d({k: fmpq(v.numerator, v.denominator) for k, v in Cp.items() if v},
                            fmpq(0), fmpq(1, 4), fmpq(0), fmpq(1, 8))
        oks.append(("C", okC, iC))
    print(f"(c) a=-7/10: divisions T:{divokT} C:{divokC}; chart verdicts: "
          f"{[(n, ok) for n, ok, _ in oks]}")
    for nm, okc, ic in oks:
        if not okc:
            print(f"    {nm} rejects:", {k: str(v)[:100] for k, v in ic.items()})
    ok_c = any(not okc for _, okc, _ in oks)

    # ---- (d) zero-margin: the design moved to the window's edge, a = -1/3, with the
    # planted p0 -> p0 - 1/10 (chosen so the rest stays positive).  Then N'(0) = 0 exactly
    # (G-RES: c(2) = -2/9 = a(a+1) at a = -1/3), and a strict check must refuse.
    z = sp.symbols("z")
    xx = sp.Symbol("x")
    Ux, Hx = ki_Usymbol(4)
    xq1 = 2 * (1 - z) ** 3
    Uq1z = sp.expand(Ux.subs({sp.Symbol("m"): 6, sp.Symbol("d"): sp.Rational(1, 30), xx: xq1}))
    Hq1z = sp.expand(Hx.subs({sp.Symbol("m"): 6, sp.Symbol("d"): sp.Rational(1, 30), xx: xq1}))
    fq1 = (1 - (1 - z) ** 3) ** 2
    p0 = chebyshev_p0(design["cheb"])
    p0z = sum(c * z**k for k, c in p0.items()) + sp.Rational(-1, 10)
    Pq1 = sp.Rational(-1, 3) / z + p0z
    fz1 = sp.expand((1 - z) * sp.diff(fq1, z))
    Npr = sp.expand(Uq1z - 64 * Hq1z ** 2 * (fz1 * Pq1 + fq1 * (-Pq1 + (1 - z) * sp.diff(Pq1, z) + Pq1 ** 2)))
    Np0 = sp.expand(Npr).subs(z, 0)
    c1 = sp.expand(Npr).coeff(z, 1)
    print(f"(d) a=-1/3, p0-1/10: N'(0) = {Np0} (exactly 0: {Np0 == 0}); order-1 coeff = {c1}")
    quo = sp.expand(sp.quo(sp.Poly(Npr, z), sp.Poly(z, z)).as_expr())
    Qmap = {}
    for i in range(sp.degree(sp.Poly(quo, z)) + 1):
        c = sp.expand(quo).coeff(z, i)
        if c != 0:
            Qmap[i] = fmpq(str(sp.Rational(c)))
    okRest, iRest = verify_1d(Qmap, fmpq(0), fmpq(1))
    Nmap = {}
    for i in range(sp.degree(sp.Poly(Npr, z)) + 1):
        c = sp.expand(Npr).coeff(z, i)
        if c != 0:
            Nmap[i] = fmpq(str(sp.Rational(c)))
    okD, iD = verify_1d(Nmap, fmpq(0), fmpq(1))
    print(f"(d) the rest positive (N'/z > 0 on [0,1]): {okRest} {iRest}")
    print(f"(d) strict check on N' (exact zero at z=0): "
          f"{'REJECT (correct)' if not okD else 'PASS (BAD)'} "
          f"{ {k: str(v)[:80] for k, v in iD.items()} }")
    ok_d = okRest and (not okD) and (Np0 == 0)

    # ---- (e) planted bound state in the throat at q = 1
    # b = ((z - 1/20)(1/5 - z))^2, z in [1/20, 1/5] <=> r in [20/19, 5/4]
    def b_and_db(r):
        z = 1 - 1 / r
        g = (z - acb(1) / 20) * (acb(1) / 5 - z)
        gp = acb(1) / 5 + acb(1) / 20 - 2 * z   # derivative of (z-1/20)(1/5-z)
        return g**2, 2 * g * gp / r**2

    # at q = 1 (mu = 0): delta = 1/(5(l+4)) = 1/30 at l=2, x_H = 2, q2 = 0
    del1 = sp.Rational(1, 30)
    Ux, Hx = ki_Usymbol(4)
    mm, dd, xx = sp.symbols("m d x")
    Uq1 = sp.expand(Ux.subs({mm: 6, dd: del1}))
    Hq1 = sp.expand(Hx.subs({mm: 6, dd: del1}))
    Uc = [sp.expand(Uq1).coeff(xx, k) for k in range(5)]
    Hc = [sp.expand(Hq1).coeff(xx, k) for k in range(2)]

    def Uv(xv):
        return sum(acb(str(c)) * xv**k for k, c in enumerate(Uc))

    def Hv(xv):
        return sum(acb(str(c)) * xv**k for k, c in enumerate(Hc))

    def Aint(r):
        bv, br = b_and_db(r)
        xv = 2 / r**3
        fv = (1 - xv / 2) ** 2
        return fv * br**2 + Uv(xv) / (64 * r**2 * Hv(xv)**2) * bv**2

    def Cint(r):   # -int W b^2 dr* = K int b^3 r^-2 dr  (f cancels; rho = r)
        bv, _ = b_and_db(r)
        return bv**3 / r**2

    A = acb.integral(lambda t, _: Aint(t), acb(20) / 19, acb(5) / 4)
    C = acb.integral(lambda t, _: Cint(t), acb(20) / 19, acb(5) / 4)
    K = int(2 * float(A.real.upper()) / float(C.real.lower())) + 1
    Q = A - K * C
    print(f"(e)(i) throat bound state: A = {A}, C = {C}, K = {K}, Q = {Q}, "
          f"rigorously < 0: {bool(Q.real.upper() < 0)}")
    ok_e1 = bool(Q.real.upper() < 0)

    # (e)(ii): the certificate at mu=0 (q=1) against V + W: U_-' = U_- - 64 K H^2 b
    # Build N at mu = 0 directly (exact, single variable):
    #   N = U - 64 H^2 [fz1 P + f(-P + (1-z) P_z + P^2)], P = a/z + p0, a = -2/5
    z = sp.symbols("z")
    fq1 = (1 - (1 - z) ** 3) ** 2
    Uq1z = sp.expand(Uq1.subs(xx, 2 * (1 - z) ** 3))
    Hq1z = sp.expand(Hq1.subs(xx, 2 * (1 - z) ** 3))
    bz = ((z - sp.Rational(1, 20)) * (sp.Rational(1, 5) - z)) ** 2
    Up = sp.expand(Uq1z - 64 * K * Hq1z ** 2 * bz)
    p0 = chebyshev_p0(design["cheb"])
    p0z = sum(c * z**k for k, c in p0.items())
    Pq1 = sp.Rational(-2, 5) / z + p0z
    fz1 = sp.expand((1 - z) * sp.diff(fq1, z))
    Npr = sp.expand(Up - 64 * Hq1z ** 2 * (fz1 * Pq1 + fq1 * (-Pq1 + (1 - z) * sp.diff(Pq1, z) + Pq1 ** 2)))
    Npr_z2 = sp.expand(Npr * z ** 2)
    Npr_map = {}
    for i in range(sp.degree(sp.Poly(Npr_z2, z)) + 1):
        c = sp.expand(Npr_z2).coeff(z, i)
        if c != 0:
            Npr_map[i] = fmpq(str(sp.Rational(c)))
    okE, iE = verify_1d(Npr_map, fmpq(0), fmpq(1))
    print(f"(e)(ii) certificate at q=1 against V+W: {'REJECT (correct)' if not okE else 'PASS (BAD)'} "
          f"{ {k: str(v)[:80] for k, v in iE.items()} }")
    ok_e = ok_e1 and not okE

    # ---- (f)
    ok_f = kat()

    allok = all([ok_a, ok_b, ok_c, ok_d, ok_e, ok_f])
    print("CONTROLS:", "ALL OK" if allok else "FAILURE")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
