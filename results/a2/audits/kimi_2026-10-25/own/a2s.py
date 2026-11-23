"""A2-S, Kimi's own route.

The design: P(z, mu) = a(1+eps)/(z+eps) + p0(z), a = -2/5,
eps = 7 mu / (3(6+7mu+mu^2));  S = eps_d z + eps_n with eps_n = 7 mu,
eps_d = 3(6+7mu+mu^2);  Pi = a(eps_d + eps_n) + p0 S;  P = Pi / S.

  NL := N S^2 = U S^2 - 64 H^2 [fz1 Pi S + f(-Pi S + (1-z)(Pi_z S - eps_d Pi) + Pi^2)]

with fz1 = (1-z) f_z, built as a polynomial in (z, mu) on my rf machinery at n = 4,
then cleared by Den(mu) > 0 (proved factorwise).  p0 = sum c_j T_j(2z-1) from the pilot
record's cheb list (float.fromhex exact rationals), converted by my own Chebyshev
recurrence.
"""
import json
import os
import sys
from fractions import Fraction

from flint import fmpq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rfg import Ctx
from verify import verify_1d, verify_2d

HERE = os.path.dirname(os.path.abspath(__file__))


# ---------- polynomials in z with rf coefficients ----------

def z_add(ctx, A, B):
    out = dict(A)
    for k, v in B.items():
        out[k] = ctx.rf_add(out[k], v) if k in out else v
    return {k: v for k, v in out.items() if v[0]}


def z_mul(ctx, A, B):
    out = {}
    for i, vi in A.items():
        for j, vj in B.items():
            k = i + j
            out[k] = ctx.rf_add(out[k], ctx.rf_mul(vi, vj)) if k in out else ctx.rf_mul(vi, vj)
    return {k: v for k, v in out.items() if v[0]}


def z_scale(ctx, A, c):
    return {k: ctx.rf_scale(v, c) for k, v in A.items()}


def z_neg(ctx, A):
    return {k: ctx.rf_neg(v) for k, v in A.items()}


def z_diff(ctx, A):
    return {k - 1: ctx.rf_scale(v, k) for k, v in A.items() if k >= 1}


def z_pow(ctx, A, e):
    out = {0: ctx.rf_const(1)}
    for _ in range(e):
        out = z_mul(ctx, out, A)
    return out


def mul_1mz(ctx, A):
    """Multiply by (1 - z)."""
    out = dict(A)
    for k, v in A.items():
        nv = ctx.rf_neg(v)
        out[k + 1] = ctx.rf_add(out[k + 1], nv) if k + 1 in out else nv
    return {k: v for k, v in out.items() if v[0]}


def chebyshev_p0(cheb):
    """p0(z) = sum_j c_j T_j(2z-1), exact, via T_{j+1}(u) = 2u T_j - T_{j-1}."""
    Ts = [{0: Fraction(1)}, {0: Fraction(-1), 1: Fraction(2)}]
    for j in range(1, len(cheb) - 1):
        uTj = {}
        for k, v in Ts[j].items():
            uTj[k] = uTj.get(k, Fraction(0)) - v
            uTj[k + 1] = uTj.get(k + 1, Fraction(0)) + 2 * v
        nxt = {}
        for k, v in uTj.items():
            nxt[k] = nxt.get(k, Fraction(0)) + 2 * v
        for k, v in Ts[j - 1].items():
            nxt[k] = nxt.get(k, Fraction(0)) - v
        Ts.append({k: v for k, v in nxt.items() if v})
    p0 = {}
    for j, hexs in enumerate(cheb):
        c = Fraction(float.fromhex(hexs))   # the exact binary value
        for k, v in Ts[j].items():
            p0[k] = p0.get(k, Fraction(0)) + c * v
    return {k: v for k, v in p0.items() if v}


def build(ctx, cheb, a=Fraction(-2, 5), U2_tamper=None):
    """Return (Den, NL) with NL = N S^2 Den, dict {z_exp: {mu_exp: Fraction}}."""
    ell, n = ctx.ell, ctx.n
    assert (ell, n) == (2, 4)
    m = 6
    delta = ({0: Fraction(1, 5), 2: Fraction(-1, 5)}, (1, 0, 0))
    xH = (ctx.p_scale(ctx.A, 2), (0, 1, 1))
    Bc = 2 * ell + n - 1
    wnum = {1: Fraction(Bc)}
    q2 = ctx.rf_reduce((ctx.p_sub(ctx.p_mul(ctx.A, ctx.A), ctx.p_mul(wnum, wnum)), (2, 0, 0)))

    import sympy as sp
    sys.path.insert(0, "[kimi-folder]/bhm-p3-audit-2026-10-22/own")
    from build import ki_Usymbol
    mm, dd, xx = sp.symbols("m d x")
    Ux, Hx = ki_Usymbol(4)
    Uc = [sp.expand(Ux).coeff(xx, k) for k in range(5)]
    Hc = [sp.expand(Hx).coeff(xx, k) for k in range(2)]

    def ev(expr):
        expr = sp.Poly(sp.expand(expr), mm, dd)
        r = ctx.rf_const(0)
        for (i, j), c in expr.terms():
            term = ctx.rf_const(sp.Rational(c) * m**i)
            for _ in range(j):
                term = ctx.rf_mul(term, delta)
            r = ctx.rf_add(r, term)
        return r

    # (1-z)^3 as a z-poly with unit rf
    one = ctx.rf_const(1)
    Y3 = {0: one, 1: ctx.rf_const(-3), 2: ctx.rf_const(3), 3: ctx.rf_const(-1)}
    xpoly = {k: ctx.rf_mul(v, xH) for k, v in Y3.items()}     # x = xH (1-z)^3

    U = {}
    xHk = one
    Y3k = {0: one}
    for k in range(5):
        ck = ev(Uc[k])
        if U2_tamper is not None and k == 2:
            ck = ctx.rf_add(ck, ctx.rf_const(U2_tamper))
        ckx = ctx.rf_mul(ck, xHk)
        U = z_add(ctx, U, {j: ctx.rf_mul(v, ckx) for j, v in Y3k.items()})
        xHk = ctx.rf_mul(xHk, xH)
        Y3k = z_mul(ctx, Y3k, Y3)
    H = {0: ev(Hc[0])}
    H1x = ctx.rf_mul(ev(Hc[1]), xH)
    H = z_add(ctx, H, {j: ctx.rf_mul(v, H1x) for j, v in Y3.items()})

    f = z_add(ctx, {0: one}, z_neg(ctx, xpoly))
    x2 = z_mul(ctx, xpoly, xpoly)
    f = z_add(ctx, f, {k: ctx.rf_mul(v, ctx.rf_scale(q2, Fraction(1, 4)))
                       for k, v in x2.items()})
    Y6 = z_mul(ctx, Y3, Y3)
    fz1 = z_add(ctx, {j: ctx.rf_mul(v, ctx.rf_scale(xH, 3)) for j, v in Y3.items()},
                {j: ctx.rf_mul(v, ctx.rf_scale(ctx.rf_mul(q2, ctx.rf_mul(xH, xH)),
                                               Fraction(-3, 2)))
                 for j, v in Y6.items()})

    en_rf = ({1: Fraction(7)}, (0, 0, 0))                             # 7 mu
    ed_rf = ({0: Fraction(18), 1: Fraction(21), 2: Fraction(3)},
             (0, 0, 0))                                               # 3(6 + 7 mu + mu^2)
    S = {0: en_rf, 1: ed_rf}
    p0 = chebyshev_p0(cheb)
    p0z = {k: ctx.rf_const(v) for k, v in p0.items()}
    Pi = z_add(ctx, {0: ctx.rf_mul(ctx.rf_const(a), ctx.rf_add(ed_rf, en_rf))},
               z_mul(ctx, p0z, S))

    S2 = z_mul(ctx, S, S)
    Pi_z = z_diff(ctx, Pi)
    Pi2 = z_mul(ctx, Pi, Pi)
    H2 = z_mul(ctx, H, H)
    inner_mid = z_add(ctx, z_mul(ctx, Pi_z, S),
                      z_neg(ctx, {k: ctx.rf_mul(v, ed_rf) for k, v in Pi.items()}))
    bracket = z_add(ctx, z_mul(ctx, z_mul(ctx, fz1, Pi), S),
                    z_mul(ctx, f,
                          z_add(ctx, z_neg(ctx, z_mul(ctx, Pi, S)),
                                z_add(ctx, mul_1mz(ctx, inner_mid), Pi2))))
    Nt = z_add(ctx, z_mul(ctx, U, S2), z_scale(ctx, z_mul(ctx, H2, bracket), Fraction(-64)))
    E = ctx.common_den(Nt)
    Den = ctx.den_poly(E)
    Nc = ctx.clear(Nt, E)
    return Den, Nc, E


def to_fmpq2(Nc):
    out = {}
    for i, poly in Nc.items():
        for j, c in poly.items():
            if c:
                out[(i, j)] = fmpq(c.numerator, c.denominator)
    return out
