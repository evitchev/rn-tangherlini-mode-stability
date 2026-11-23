"""HD-X-2, Kimi's own route (the 9 critical bands).

Design (registered, fixed by rule):
  P = -nu - l y / ((z+eps) R) - (1-z) H_z/H + c mu,
  nu = l + n/2 - 1,  R = (1-y)/z,  H = H_-(x_H y),  y = (1-z)^k,  k = n-1,
  eps = eps_hat w/(1+w),  eps_hat = (1/k + 2/(k-l))/2,  c = 1/4.

My construction: S = eps_d z + eps_n (eps = eps_n/eps_d), D = S R H (H the rf-carrying
H_-(x_H y)), Pi = P D, and
  NL := N S^2 R^2 = U S^2 R^2 - 64 [ H (1-z) f_z Pi S R + f(-Pi D + (1-z)(Pi_z D - Pi D_z) + Pi^2) ],
cleared by my Den(mu) > 0.

Then: Z0 (NL(z,0) == 0), M = NL/mu (O, O'), T = NL(mu zeta, mu)/mu^2, C = NL(z, z sigma)/(z^2 sigma),
with positivity on the four boxes and the coverage argument.
"""
import json
import os
import sys
from fractions import Fraction

from flint import fmpq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "[kimi-folder]/bhm-p3-audit-2026-10-22/own")
from rfg import Ctx
from verify import verify_1d, verify_2d
from build import ki_Usymbol

HERE = os.path.dirname(os.path.abspath(__file__))

# z-dicts with rf coefficients

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
    out = dict(A)
    for k, v in A.items():
        nv = ctx.rf_neg(v)
        out[k + 1] = ctx.rf_add(out[k + 1], nv) if k + 1 in out else nv
    return {k: v for k, v in out.items() if v[0]}


def rf_of(ctx, poly):
    """Plain mu-poly {exp: Fraction} -> rf."""
    return (poly, (0, 0, 0))


def blocks(ctx):
    """delta, xH, w, q2 as rf for ctx = (ell, n)."""
    ell, n = ctx.ell, ctx.n
    m = (ell - 1) * (ell + n)
    Bc = 2 * ell + n - 1
    s_num = ctx.p_scale({0: Fraction(ell + n), 2: Fraction(-(ell - 1))}, Fraction(Bc, n + 1))
    s = (s_num, (1, 0, 0))
    delta = ctx.rf_scale(ctx.rf_sub(s, ctx.rf_const(1)), Fraction(1, 2 * m))
    xH = (ctx.p_scale(ctx.A, 2), (0, 1, 1))
    wnum = {1: Fraction(Bc)}
    w = (wnum, (1, 0, 0))
    q2n = ctx.p_sub(ctx.p_mul(ctx.A, ctx.A), ctx.p_mul(wnum, wnum))
    q2 = ctx.rf_reduce((q2n, (2, 0, 0)))
    return m, delta, xH, w, q2


def build_NL(ctx, ehat_shift=Fraction(0), c=Fraction(1, 4), nu_shift=Fraction(0)):
    """Build (Den, NL) with NL a z-dict of mu-polys (after clearing), for the HD-X-2 design."""
    ell, n = ctx.ell, ctx.n
    k = n - 1
    m, delta, xH, w, q2 = blocks(ctx)
    import sympy as sp
    mm, dd, xx = sp.symbols("m d x")
    Ux, Hx = ki_Usymbol(n)
    Uc = [sp.expand(Ux).coeff(xx, i) for i in range(5)]
    Hc = [sp.expand(Hx).coeff(xx, i) for i in range(2)]

    def ev(expr):
        expr = sp.Poly(sp.expand(expr), mm, dd)
        r = ctx.rf_const(0)
        for (i, j), cc in expr.terms():
            term = ctx.rf_const(sp.Rational(cc) * m**i)
            for _ in range(j):
                term = ctx.rf_mul(term, delta)
            r = ctx.rf_add(r, term)
        return r

    U0 = [ev(Uc[i]) for i in range(5)]   # coefficients of x^i, rf
    H0 = [ev(Hc[i]) for i in range(2)]

    # y = (1-z)^k ; Y = 1 - z as z-dict
    Y = {0: ctx.rf_const(1), 1: ctx.rf_const(-1)}
    y = z_pow(ctx, Y, k)
    # x = xH * y:  U = sum_i U0_i (xH y)^i, H = H0_0 + H0_1 xH y
    U = {}
    xHk = ctx.rf_const(1)
    yk = {0: ctx.rf_const(1)}
    for i in range(5):
        term = {j: ctx.rf_mul(v, ctx.rf_mul(U0[i], xHk)) for j, v in yk.items()}
        U = z_add(ctx, U, term)
        xHk = ctx.rf_mul(xHk, xH)
        yk = z_mul(ctx, yk, y)
    H = {0: H0[0]}
    H1x = ctx.rf_mul(H0[1], xH)
    H = z_add(ctx, H, {j: ctx.rf_mul(v, H1x) for j, v in y.items()})
    # f = 1 - x + q2 x^2/4 with x = xH y;  (1-z) f_z = k xH y - (k q2/2) xH^2 y^2
    xpoly = {j: ctx.rf_mul(v, xH) for j, v in y.items()}
    x2 = z_mul(ctx, xpoly, xpoly)
    f = z_add(ctx, z_add(ctx, {0: ctx.rf_const(1)}, z_neg(ctx, xpoly)),
              {j: ctx.rf_mul(v, ctx.rf_scale(q2, Fraction(1, 4))) for j, v in x2.items()})
    fz1 = z_add(ctx, {j: ctx.rf_mul(v, ctx.rf_scale(xH, k)) for j, v in y.items()},
                {j: ctx.rf_mul(v, ctx.rf_scale(q2, Fraction(-k, 2)))
                 for j, v in x2.items()})
    # R = (1 - y)/z = sum_{j=0}^{k-1} (1-z)^j
    R = {}
    Yj = {0: ctx.rf_const(1)}
    for j in range(k):
        R = z_add(ctx, R, Yj)
        Yj = z_mul(ctx, Yj, Y)
    # H_z = -k (1-z)^{k-1} H1x
    Ykm1 = z_pow(ctx, Y, k - 1)
    H_z = {j: ctx.rf_mul(v, ctx.rf_scale(H1x, -k)) for j, v in Ykm1.items()}
    # eps = ehat w/(1+w) = eps_n/eps_d
    ehat = Fraction(1, k) + Fraction(2, k - ell)
    ehat = ehat / 2 + ehat_shift
    # eps_n = ehat * w (rf), eps_d = 1 + w (rf)
    eps_n = ctx.rf_scale(w, ehat)
    eps_d = ctx.rf_add(ctx.rf_const(1), w)
    S = {0: eps_n, 1: eps_d}    # S = eps_n + eps_d z
    # D = S R H
    D = z_mul(ctx, z_mul(ctx, S, R), H)
    # Pi = -nu D - l y eps_d H - (1-z) H_z S R + c mu D
    nu = Fraction(2 * ell + n - 2, 2) + nu_shift
    Pi = z_neg(ctx, z_scale(ctx, D, nu))
    t2 = z_mul(ctx, z_mul(ctx, y, H), {0: eps_d})
    Pi = z_add(ctx, Pi, z_scale(ctx, t2, Fraction(-ell)))
    t3 = z_mul(ctx, mul_1mz(ctx, H_z), z_mul(ctx, S, R))
    Pi = z_add(ctx, Pi, z_neg(ctx, t3))
    mu_rf = ({1: Fraction(1)}, (0, 0, 0))
    Pi = z_add(ctx, Pi, {j: ctx.rf_mul(v, ctx.rf_scale(mu_rf, c)) for j, v in D.items()})
    # NL = U S^2 R^2 - 64 [ H fz1 Pi S R + f(-Pi D + (1-z)(Pi_z D - Pi D_z) + Pi^2) ]
    S2 = z_mul(ctx, S, S)
    R2 = z_mul(ctx, R, R)
    Pi_z = z_diff(ctx, Pi)
    D_z = z_diff(ctx, D)
    inner = z_add(ctx, z_neg(ctx, z_mul(ctx, Pi, D)),
                  z_add(ctx, mul_1mz(ctx, z_add(ctx, z_mul(ctx, Pi_z, D),
                                                z_neg(ctx, z_mul(ctx, Pi, D_z)))),
                        z_mul(ctx, Pi, Pi)))
    B = z_add(ctx, z_mul(ctx, z_mul(ctx, z_mul(ctx, H, fz1), Pi), z_mul(ctx, S, R)),
              z_mul(ctx, f, inner))
    NL = z_add(ctx, z_mul(ctx, U, z_mul(ctx, S2, R2)), z_scale(ctx, B, Fraction(-64)))
    E = ctx.common_den(NL)
    Den = ctx.den_poly(E)
    Nc = ctx.clear(NL, E)
    return Den, Nc, E


BANDS_2 = [(7, 2), (8, 2), (9, 2), (9, 3), (10, 2), (10, 3), (11, 2), (11, 3), (11, 4)]
MU1 = {(7, 2): Fraction(1, 8), (8, 2): Fraction(13, 100), (9, 2): Fraction(13, 100),
       (9, 3): Fraction(3, 25), (10, 2): Fraction(13, 100), (10, 3): Fraction(3, 25),
       (11, 2): Fraction(13, 100), (11, 3): Fraction(1, 8), (11, 4): Fraction(3, 25)}
