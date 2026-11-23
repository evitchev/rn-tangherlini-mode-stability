"""HD-X-S, Kimi's own route (the 11 non-critical bands).

Design: P = a(1+eps)/(z+eps) + p0(z), eps = w/((n-1)(1+w)) = eps_n/eps_d.
S = eps_d z + eps_n, Pi = a(eps_d + eps_n) + p0 S, P = Pi/S.
NL := N S^2 = U S^2 - 64 H^2 [fz1 Pi S + f(-Pi S + (1-z)(Pi_z S - eps_d Pi) + Pi^2)],
built on my rf machinery at general n (helpers from hdx2.py), cleared by Den(mu).
Charts O, O', T, C as in the registered scheme; coverage verified by me.
"""
import json
import os
import sys
from fractions import Fraction

from flint import fmpq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rfg import Ctx
import hdx2 as H2
from a2s import chebyshev_p0, to_fmpq2
from verify import verify_1d, verify_2d

HERE = os.path.dirname(os.path.abspath(__file__))

BANDS_S = [(7, 3), (8, 3), (8, 4), (9, 4), (9, 5), (10, 4), (10, 5), (10, 6),
           (11, 5), (11, 6), (11, 7)]


def build_NL(ctx, a, p0z):
    """a: Fraction; p0z: {z_exp: Fraction}.  Returns (Den, NL, E)."""
    ell, n = ctx.ell, ctx.n
    k = n - 1
    m, delta, xH, w, q2 = H2.blocks(ctx)
    # U, H, f, fz1 as z-dicts of rf
    import sympy as sp
    sys.path.insert(0, "[kimi-folder]/bhm-p3-audit-2026-10-22/own")
    from build import ki_Usymbol
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

    U0 = [ev(Uc[i]) for i in range(5)]
    H0 = [ev(Hc[i]) for i in range(2)]
    Y = {0: ctx.rf_const(1), 1: ctx.rf_const(-1)}
    y = H2.z_pow(ctx, Y, k)
    U = {}
    xHk = ctx.rf_const(1)
    yk = {0: ctx.rf_const(1)}
    for i in range(5):
        U = H2.z_add(ctx, U, {j: ctx.rf_mul(v, ctx.rf_mul(U0[i], xHk)) for j, v in yk.items()})
        xHk = ctx.rf_mul(xHk, xH)
        yk = H2.z_mul(ctx, yk, y)
    H = {0: H0[0]}
    H1x = ctx.rf_mul(H0[1], xH)
    H = H2.z_add(ctx, H, {j: ctx.rf_mul(v, H1x) for j, v in y.items()})
    xpoly = {j: ctx.rf_mul(v, xH) for j, v in y.items()}
    x2 = H2.z_mul(ctx, xpoly, xpoly)
    f = H2.z_add(ctx, H2.z_add(ctx, {0: ctx.rf_const(1)}, H2.z_neg(ctx, xpoly)),
                 {j: ctx.rf_mul(v, ctx.rf_scale(q2, Fraction(1, 4))) for j, v in x2.items()})
    fz1 = H2.z_add(ctx, {j: ctx.rf_mul(v, ctx.rf_scale(xH, k)) for j, v in y.items()},
                   {j: ctx.rf_mul(v, ctx.rf_scale(q2, Fraction(-k, 2))) for j, v in x2.items()})
    # eps_n/eps_d = w/((n-1)(1+w)):  eps_n = w, eps_d = (n-1)(1+w)
    eps_n = w
    eps_d = ctx.rf_scale(ctx.rf_add(ctx.rf_const(1), w), Fraction(n - 1))
    S = {0: eps_n, 1: eps_d}
    p0_rf = {j: ctx.rf_const(c) for j, c in p0z.items()}
    Pi = H2.z_add(ctx, {0: ctx.rf_mul(ctx.rf_const(a), ctx.rf_add(eps_d, eps_n))},
                  H2.z_mul(ctx, p0_rf, S))
    S2 = H2.z_mul(ctx, S, S)
    Pi_z = H2.z_diff(ctx, Pi)
    Pi2 = H2.z_mul(ctx, Pi, Pi)
    H2q = H2.z_mul(ctx, H, H)
    inner_mid = H2.z_add(ctx, H2.z_mul(ctx, Pi_z, S),
                         H2.z_neg(ctx, {kk: ctx.rf_mul(v, eps_d) for kk, v in Pi.items()}))
    bracket = H2.z_add(ctx, H2.z_mul(ctx, H2.z_mul(ctx, fz1, Pi), S),
                       H2.z_mul(ctx, f,
                                H2.z_add(ctx, H2.z_neg(ctx, H2.z_mul(ctx, Pi, S)),
                                         H2.z_add(ctx, H2.mul_1mz(ctx, inner_mid), Pi2))))
    NL = H2.z_add(ctx, H2.z_mul(ctx, U, S2),
                  H2.z_scale(ctx, H2.z_mul(ctx, H2q, bracket), Fraction(-64)))
    E = ctx.common_den(NL)
    Den = ctx.den_poly(E)
    Nc = ctx.clear(NL, E)
    return Den, Nc, E


def check_band(D, ell, design):
    n = D - 2
    ctx = Ctx(ell, n)
    a = Fraction(design["a"])
    p0z = chebyshev_p0(design["cheb"])
    Den, Nc, E = build_NL(ctx, a, p0z)
    mu1 = Fraction(design.get("mu1", "1/8"))
    res = {"band": f"{D}-{ell}", "a": str(a), "deg": (max(Nc), max(max(p) for p in Nc.values()))}
    # coverage of q: q(mu1)^2 <= (99/100)^2
    Bc = 2 * ell + n - 1
    A1 = (ell + n) + (ell - 1) * mu1 * mu1
    q2 = 1 - Fraction(Bc * Bc) * mu1 * mu1 / (A1 * A1)
    res["q(mu1)^2"] = str(q2)
    res["cover"] = bool(q2 <= Fraction(99, 100) ** 2)
    # Den > 0 on [0, mu1]
    for fp, nm, e in zip((ctx.A, ctx.B, ctx.C), ("A", "B", "mu+1"), E):
        if e:
            fp_f = {k2: fmpq(v.numerator, v.denominator) for k2, v in fp.items()}
            ok, _ = verify_1d(fp_f, fmpq(0), fmpq(mu1.numerator, mu1.denominator))
            assert ok, nm
    res["Den>0"] = True
    # charts
    NT = {}
    for i, poly in Nc.items():
        for j, c in poly.items():
            NT[(i, i + j)] = NT.get((i, i + j), Fraction(0)) + c
    T = {}
    divT = True
    for (iz, im), c in NT.items():
        if im < 2:
            divT = False
        else:
            T[(iz, im - 2)] = c
    NCd = {}
    for i, poly in Nc.items():
        for j, c in poly.items():
            NCd[(i + j, j)] = NCd.get((i + j, j), Fraction(0)) + c
    Cp = {}
    divC = True
    for (iz, isg), c in NCd.items():
        if iz < 2:
            divC = False
        else:
            Cp[(iz - 2, isg)] = c
    res["DIV-T"], res["DIV-C"] = divT, divC
    tof = lambda Dd: {kk: fmpq(v.numerator, v.denominator) for kk, v in Dd.items() if v}
    okO, _ = verify_2d(to_fmpq2(Nc), fmpq(1, 4), fmpq(1), fmpq(0), fmpq(mu1.numerator, mu1.denominator))
    okOp, _ = verify_2d(to_fmpq2(Nc), fmpq(0), fmpq(1, 4), fmpq(1, 32), fmpq(mu1.numerator, mu1.denominator))
    okT = okC = False
    if divT:
        okT, _ = verify_2d(tof(T), fmpq(0), fmpq(8), fmpq(0), fmpq(1, 32))
    if divC:
        okC, _ = verify_2d(tof(Cp), fmpq(0), fmpq(1, 4), fmpq(0), fmpq(1, 8))
    res["POS"] = {"O": okO, "O'": okOp, "T": okT, "C": okC}
    res["ok"] = all([res["cover"], divT, divC, okO, okOp, okT, okC])
    return res


def main():
    with open(os.path.join(HERE, "..", "data", "designs.json")) as fh:
        designs = json.load(fh)
    results = {}
    for D, ell in BANDS_S:
        r = check_band(D, ell, designs[f"{D},{ell}"])
        results[f"{D}-{ell}"] = r
        print(f"{D}-{ell}: {'VERIFIED' if r['ok'] else 'FAILED'} a={r['a']} "
              f"deg={r['deg']} q(mu1)^2={float(Fraction(r['q(mu1)^2'])):.6f} POS={r['POS']}",
              flush=True)
    with open(os.path.join(HERE, "hdxs_results.json"), "w") as fh:
        json.dump(results, fh, indent=1, default=str)
    bad = [k for k, v in results.items() if not v["ok"]]
    print("HD-X-S:", "ALL BANDS VERIFIED" if not bad else f"FAILED: {bad}")
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main())
