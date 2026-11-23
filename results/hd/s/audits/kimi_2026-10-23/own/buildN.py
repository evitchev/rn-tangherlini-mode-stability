"""HD-S: Kimi's own N builder and per-box verifier.

For a band (n, ell) and a certificate box with P (z-design) or (Phat, delta_b, d)
(zeta-design), in Y = 1 - z:

    N = U - 64 H^2 [(1-z) f_z P + f(-P + (1-z) P_z + P^2)]
    x = xH Y^{n-1},  f = 1 - x + q2 x^2/4,
    (1-z) f_z = (n-1) xH Y^{n-1} - (n-1)(q2/2) xH^2 Y^{2(n-1)},
    (1-z) P_z = -Y P_Y.
  zeta: P = Phat/s^d, s = (1+delta_b) - Y:
    N s^{2d} = U s^{2d} - 64 H^2 [fz1 Phat s^d + f(-Phat s^d + (-Y Phat_Y) s^d
               - d Y Phat s^{d-1} + Phat^2)].

Everything in exact QQ(mu) arithmetic (rfg.Ctx); the common denominator Den(mu) is a
product of A = (l+n)+(l-1)mu^2, B = (l-1)mu+(l+n), mu+1 (all > 0 on [0,1], proved
factorwise by my verifier).  Ntilde = N [x s^{2d}] * Den is a polynomial in (Y, mu).
"""
import json
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rfg import Ctx

HERE = os.path.dirname(os.path.abspath(__file__))


# ---------- Y-dicts with rf coefficients (Y = 1 - z) ----------

def y_add(ctx, A, B):
    out = dict(A)
    for k, v in B.items():
        out[k] = ctx.rf_add(out[k], v) if k in out else v
    return {k: v for k, v in out.items() if v[0]}


def y_mul(ctx, A, B):
    out = {}
    for i, vi in A.items():
        for j, vj in B.items():
            k = i + j
            out[k] = ctx.rf_add(out[k], ctx.rf_mul(vi, vj)) if k in out else ctx.rf_mul(vi, vj)
    return {k: v for k, v in out.items() if v[0]}


def y_pow(ctx, A, e):
    out = {0: ctx.rf_const(1)}
    for _ in range(e):
        out = y_mul(ctx, out, A)
    return out


def y_scale(ctx, A, c):
    return {k: ctx.rf_scale(v, c) for k, v in A.items()}


def y_neg(ctx, A):
    return {k: ctx.rf_neg(v) for k, v in A.items()}


def blocks(ctx):
    """delta, xH, q2 as rf for ctx = (ell, n); m integer."""
    ell, n = ctx.ell, ctx.n
    m = (ell - 1) * (ell + n)
    Bc = 2 * ell + n - 1
    s_num = ctx.p_scale({0: Fraction(ell + n), 2: Fraction(-(ell - 1))},
                        Fraction(Bc, n + 1))
    s = (s_num, (1, 0, 0))
    delta = ctx.rf_scale(ctx.rf_sub(s, ctx.rf_const(1)), Fraction(1, 2 * m))
    xH = (ctx.p_scale(ctx.A, 2), (0, 1, 1))
    wnum = {1: Fraction(Bc)}
    q2n = ctx.p_sub(ctx.p_mul(ctx.A, ctx.A), ctx.p_mul(wnum, wnum))
    q2 = ctx.rf_reduce((q2n, (2, 0, 0)))
    return m, delta, xH, q2


def UH(ctx):
    """U, H as Y-dicts of rf (Y = 1-z), from my KI transcription (general n)."""
    import sympy as sp
    sys.path.insert(0, "[kimi-folder]/bhm-p3-audit-2026-10-22/own")
    from build import ki_Usymbol
    ell, n = ctx.ell, ctx.n
    m = (ell - 1) * (ell + n)
    mm, dd, xx = sp.symbols("m d x")
    Ux, Hx = ki_Usymbol(n)
    Uc = [sp.expand(Ux).coeff(xx, k) for k in range(5)]
    Hc = [sp.expand(Hx).coeff(xx, k) for k in range(2)]
    m_rf, delta, xH, q2 = blocks(ctx)

    def ev(expr):
        expr = sp.Poly(sp.expand(expr), mm, dd)
        r = ctx.rf_const(0)
        for (i, j), c in expr.terms():
            term = ctx.rf_const(sp.Rational(c) * m**i)
            for _ in range(j):
                term = ctx.rf_mul(term, delta)
            r = ctx.rf_add(r, term)
        return r

    U, H = {}, {}
    xHk = ctx.rf_const(1)
    for k in range(5):
        ck = ev(Uc[k])
        if ck[0]:
            U[k * (n - 1)] = ctx.rf_mul(ck, xHk)
        if k < 2:
            hk = ev(Hc[k])
            if hk[0]:
                H[k * (n - 1)] = ctx.rf_mul(hk, xHk)
        xHk = ctx.rf_mul(xHk, xH)
    return U, H, xH, q2


def fz1_f(ctx, xH, q2):
    """(1-z) f_z and f as Y-dicts."""
    n = ctx.n
    xH2 = ctx.rf_mul(xH, xH)
    fz1 = {n - 1: ctx.rf_scale(xH, n - 1),
           2 * (n - 1): ctx.rf_scale(ctx.rf_mul(q2, xH2), Fraction(-(n - 1), 2))}
    f = {0: ctx.rf_const(1),
         n - 1: ctx.rf_neg(xH),
         2 * (n - 1): ctx.rf_scale(ctx.rf_mul(q2, xH2), Fraction(1, 4))}
    return fz1, f


def P_to_PY(ctx, Pmap):
    """cert map "(i, j)" -> coeff of z^i mu^j  ==>  Y-dict of rf (Y = 1 - z)."""
    Pz = {}
    for key, val in Pmap.items():
        i, j = eval(key)
        Pz.setdefault(i, {})[j] = Fraction(val)
    base = {0: ctx.rf_const(1), 1: ctx.rf_const(-1)}   # 1 - Y
    PY = {}
    for i, mupart in Pz.items():
        crf = ({jj: c for jj, c in mupart.items()}, (0, 0, 0))
        p = {0: ctx.rf_const(1)}
        for _ in range(i):
            p = y_mul(ctx, p, base)
        PY = y_add(ctx, PY, {kk: ctx.rf_mul(vv, crf) for kk, vv in p.items()})
    return PY


def negYPY(ctx, PY):
    out = {}
    for j, c in PY.items():
        if j >= 1:
            out[j] = ctx.rf_scale(c, -Fraction(j))
    return out


def build_N(ctx, box):
    """Return (Den, Ntilde) with Ntilde a dict {Y: {mu: Fraction}}."""
    U, H, xH, q2 = UH(ctx)
    fz1, f = fz1_f(ctx, xH, q2)
    H2 = y_mul(ctx, H, H)
    PY = P_to_PY(ctx, box["P"])
    nYPY = negYPY(ctx, PY)
    if box["variable"] == "z":
        P2 = y_mul(ctx, PY, PY)
        inner = y_add(ctx, y_neg(ctx, PY), y_add(ctx, nYPY, P2))
        B = y_add(ctx, y_mul(ctx, fz1, PY), y_mul(ctx, f, inner))
        N = y_add(ctx, U, y_scale(ctx, y_mul(ctx, H2, B), Fraction(-64)))
    else:
        db = Fraction(box["delta_b"])
        d = int(box["degree"])
        s = {0: ctx.rf_const(1 + db), 1: ctx.rf_const(-1)}   # (1+db) - Y
        sd = y_pow(ctx, s, d)
        s2d = y_pow(ctx, s, 2 * d)
        # -Y Phat_Y is already nYPY; - d Y Phat s^{d-1}:
        sd1 = y_pow(ctx, s, d - 1) if d >= 1 else {0: ctx.rf_const(1)}
        YPhat = {k + 1: v for k, v in PY.items()}            # Y * Phat
        inner = y_add(ctx,
                      y_neg(ctx, y_mul(ctx, PY, sd)),
                      y_add(ctx, y_mul(ctx, nYPY, sd),
                            y_add(ctx, y_scale(ctx, y_mul(ctx, YPhat, sd1), Fraction(-d)),
                                  y_mul(ctx, PY, PY))))
        B = y_add(ctx, y_mul(ctx, y_mul(ctx, fz1, PY), sd), y_mul(ctx, f, inner))
        N = y_add(ctx, y_mul(ctx, U, s2d),
                  y_scale(ctx, y_mul(ctx, H2, B), Fraction(-64)))
    E = ctx.common_den(N)
    Den = ctx.den_poly(E)
    Nt = ctx.clear(N, E)
    return Den, Nt, E
