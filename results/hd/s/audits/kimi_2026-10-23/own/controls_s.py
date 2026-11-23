"""HD-S controls (Kimi).

(a) Planted bound state on band 7-2's first box, at its midpoint mu_c:
    W = -K f b/rho^2, b(z) = ((z-3/10)(3/5-z))^2 on [3/10, 3/5] (0 outside).
    (i)  Q[b] = int f b_r^2 + (V+W)/f b^2 dr < 0 certified by rigorous acb integration
         (K = ceil(2 A/C) from acb-evaluated A, C);
    (ii) the same stored certificate P checked against the perturbed potential must REJECT
         in exact arithmetic (N' = N - 64 K H^2 b, my verifier).
(b) One stored certificate (7-2 box 0) with P's constant term raised by 1/10 must REJECT.
(c) Verifier tamper: KAT suite.
"""
import json
import os
import sys
from fractions import Fraction

import sympy as sp
from flint import acb, fmpq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "[kimi-folder]/bhm-p3-audit-2026-10-22/own")
from rfg import Ctx
from buildN import build_N, UH, blocks
from build import ki_Usymbol
from verify import verify_1d, verify_2d, kat

REC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")


def b_and_db(r):
    """b and b_r at r (acb), r in [10/7, 5/3] (the support, endpoints inclusive)."""
    z = 1 - 1 / r
    g = (z - acb(3) / 10) * (acb(3) / 5 - z)
    # b = g^2; g' = 9/10 - 2z; b_r = 2 g g' / r^2
    gp = acb(9) / 10 - 2 * z
    return g**2, 2 * g * gp / r**2


def main():
    with open(f"{REC}/7-2.json") as fh:
        d = json.load(fh)
    box = d["boxes"][0]
    n, ell = 5, 2
    m = (ell - 1) * (ell + n)
    ctx = Ctx(ell, n)
    ma, mb = (Fraction(x) for x in box["mu"])
    mu_c = (ma + mb) / 2

    # ---------- (a)(i): rigorous trial energy ----------
    muf = acb(f"{mu_c.numerator}/{mu_c.denominator}")
    Bc = 2 * ell + n - 1
    Af = (ell + n) + (ell - 1) * muf**2
    wf = Bc * muf / Af
    q2f = 1 - wf**2
    # delta exactly (the parametrisation is rational in mu)
    muF = mu_c
    AF = Fraction(ell + n) + (ell - 1) * muF**2
    sF = Fraction(Bc) * (Fraction(ell + n) - (ell - 1) * muF**2) / ((n + 1) * AF)
    delF = (sF - 1) / (2 * m)
    xHf = 2 / (1 + wf)
    mm, dd, xx = sp.symbols("m d x")
    Ux, Hx = ki_Usymbol(n)
    Uc = [sp.expand(Ux.subs({mm: m, dd: sp.Rational(delF.numerator, delF.denominator)})).coeff(xx, k) for k in range(5)]
    Hc = [sp.expand(Hx.subs({mm: m, dd: sp.Rational(delF.numerator, delF.denominator)})).coeff(xx, k) for k in range(2)]

    def Uv(xv):
        return sum(acb(str(c)) * xv**k for k, c in enumerate(Uc))

    def Hv(xv):
        return sum(acb(str(c)) * xv**k for k, c in enumerate(Hc))

    def Aint(r):   # f b_r^2 + (V/f) b^2 = f b_r^2 + U/(64 r^2 H^2) b^2
        bv, br = b_and_db(r)
        xv = xHf / r**(n - 1)
        fv = 1 - xv + q2f * xv**2 / 4
        return fv * br**2 + Uv(xv) / (64 * r**2 * Hv(xv)**2) * bv**2

    def Cint(r):   # (b/r^2) b^2 / ... W/f = -K b / r^2 -> W b^2 dr* = -K b^3/(r^2 f) dr
        bv, _ = b_and_db(r)
        xv = xHf / r**(n - 1)
        fv = 1 - xv + q2f * xv**2 / 4
        return bv**3 / (r**2 * fv)

    A = acb.integral(lambda t, _: Aint(t), acb(10) / 7, acb(5) / 3)
    C = acb.integral(lambda t, _: Cint(t), acb(10) / 7, acb(5) / 3)
    print("(a)(i) A =", A, " C =", C)
    # rigorous negativity of A - K*C with K = ceil(2 A_up / C_low)
    K = int(2 * float(A.real.upper()) / float(C.real.lower())) + 1
    Q = A - K * C
    print("(a)(i) K =", K, " Q = A - K C =", Q, " < 0 rigorously:", Q.real.upper() < 0)
    ok_ai = bool(Q.real.upper() < 0)

    # ---------- (a)(ii): exact rejection ----------
    # N'(Y) = N(Y) - 64 K H(Y)^2 b(Y) at mu_c
    Den, Nt, E = build_N(ctx, box)

    def rv(r_):
        nn, e = r_
        v = Fraction(0)
        for j, c in nn.items():
            v += c * mu_c**j
        for i in range(3):
            v /= sum(cc * mu_c**jj for jj, cc in ctx.FACTORS[i].items()) ** e[i]
        return v

    Den_v = sum(c * mu_c**j for j, c in Den.items())
    N1 = {}
    for yexp, poly in Nt.items():
        v = Fraction(0)
        for j, c in poly.items():
            v += c * mu_c**j
        N1[yexp] = v / Den_v
    U, H, xH_, q2_ = UH(ctx)
    H_at = {k: rv(v) for k, v in H.items()}
    H2 = {}
    for i, vi in H_at.items():
        for j, vj in H_at.items():
            H2[i + j] = H2.get(i + j, Fraction(0)) + vi * vj
    Ys = sp.Symbol("Y")
    bz = sp.expand(((sp.Symbol("zz") - sp.Rational(3, 10)) * (sp.Rational(3, 5) - sp.Symbol("zz")))**2)
    bY = sp.Poly(sp.expand(bz.subs(sp.Symbol("zz"), 1 - Ys)), Ys)
    bYd = {m_[0]: Fraction(c) for m_, c in bY.terms()}
    bH2 = {}
    for i, vi in H2.items():
        for j, vj in bYd.items():
            bH2[i + j] = bH2.get(i + j, Fraction(0)) + vi * vj
    Np = dict(N1)
    for k, v in bH2.items():
        Np[k] = Np.get(k, Fraction(0)) - 64 * K * v
    Np_f = {k: fmpq(v.numerator, v.denominator) for k, v in Np.items() if v}
    ok, info = verify_1d(Np_f, fmpq(0), fmpq(1))
    print("(a)(ii) verifier on perturbed N:", "REJECT (correct)" if not ok else "PASS (BAD)",
          {k2: str(v2)[:80] for k2, v2 in info.items()})
    ok_aii = not ok

    # ---------- (b): one stored certificate with one coefficient changed ----------
    box2 = dict(box)
    P2 = dict(box["P"])
    P2["(0, 0)"] = str(Fraction(P2["(0, 0)"]) + Fraction(1, 10))
    box2["P"] = P2
    Den2, Nt2, E2 = build_N(ctx, box2)
    N2 = {}
    for yexp, poly in Nt2.items():
        for j, c in poly.items():
            if c:
                N2[(yexp, j)] = fmpq(c.numerator, c.denominator)
    ok2, info2 = verify_2d(N2, fmpq(0), fmpq(1), fmpq(ma.numerator, ma.denominator),
                           fmpq(mb.numerator, mb.denominator))
    print("(b) tampered certificate:", "REJECT (correct)" if not ok2 else "PASS (BAD)",
          {k2: str(v2)[:100] for k2, v2 in info2.items()})
    ok_b = not ok2

    # ---------- (c) ----------
    ok_c = kat()
    print("CONTROLS:", "ALL OK" if (ok_ai and ok_aii and ok_b and ok_c) else "FAILURE")
    return 0 if (ok_ai and ok_aii and ok_b and ok_c) else 1


if __name__ == "__main__":
    raise SystemExit(main())
