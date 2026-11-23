"""Part I of the P1 audit (Kimi's own route): per ell = 3..L, build
    U_-(t x_H) = F_ell(t, mu) / Den_ell(mu)
exactly, check the parametrisation identities and w increasing, compute
mu_lo = k/1000 (largest k with w(k/1000)^2 <= 1 - (99/100)^2), check coverage
q(mu_lo)^2 >= (99/100)^2 exactly, and prove Den > 0 and F > 0 on the closed
box with my own Bernstein verifier.

KI (5.63b) at n = 4 with general m (my transcription; the coefficients below
are it, specialised: the (n-4)-vanishing terms at n = 4 are shown):
    U = -400000 d (1+md)^3 x^4 - 1600 (1+md)^2 (50 m d - 16) x^3
        + 7680 m (1+md) x^2 - 16 m (5 m (96 - 4 m) d + 480) x + 64 m^3 + 384 m^2
    H = m + 10 (1 + m d) x
Parametrisation (onset PREREG section 1, general ell):
    A = (ell+4) + (ell-1) mu^2,  w = (2l+3) mu / A,
    s = 1 + 2 m delta = (2l+3)((ell+4) - (ell-1) mu^2)/(5 A),
    x_H = 2/(1+w) = 2A/((mu+1) B),  B = (ell-1) mu + (ell+4).
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
OUT = os.path.join(HERE, "built")
os.makedirs(OUT, exist_ok=True)


def blocks(ctx):
    """delta, xH, q2 as rf for the ctx's ell."""
    ell = ctx.ell
    m = (ell - 1) * (ell + 4)
    A = ctx.A
    B = ctx.B
    # s = (2l+3)((l+4) - (l-1) mu^2) / (5 A);  delta = (s - 1)/(2m)
    s_num = ctx.p_scale(ctx.p_sub({0: Fraction(ell + 4)},
                                  {2: Fraction(ell - 1)}), Fraction(2 * ell + 3, 5))
    s = (s_num, (1, 0, 0))
    delta = ctx.rf_scale(ctx.rf_sub(s, ctx.rf_const(1)), Fraction(1, 2 * m))
    # xH = 2A / ((mu+1) B)
    xH = (ctx.p_scale(A, 2), (0, 1, 1))
    # q2 = 1 - w^2,  w = (2l+3) mu / A
    wnum = {1: Fraction(2 * ell + 3)}
    q2n = ctx.p_sub(ctx.p_mul(A, A), ctx.p_mul(wnum, wnum))
    q2 = ctx.rf_reduce((q2n, (2, 0, 0)))
    return m, delta, xH, q2


def build_F(ctx, tamper_U2=False):
    m, delta, xH, q2 = blocks(ctx)
    one = ctx.rf_const(1)
    md = ctx.rf_scale(delta, m)
    one_md = ctx.rf_add(one, md)
    U0 = ctx.rf_const(64 * m**3 + 384 * m**2)
    U1 = ctx.rf_scale(ctx.rf_add(ctx.rf_scale(delta, 5 * m * (96 - 4 * m)),
                                 ctx.rf_const(480)), -16 * m)
    c7680 = 7681 if tamper_U2 else 7680
    U2 = ctx.rf_scale(one_md, c7680 * m)
    U3 = ctx.rf_scale(ctx.rf_mul(ctx.rf_mul(one_md, one_md),
                                 ctx.rf_sub(ctx.rf_scale(delta, 50 * m),
                                            ctx.rf_const(16))), -1600)
    U4 = ctx.rf_scale(ctx.rf_mul(delta, ctx.rf_mul(ctx.rf_mul(one_md, one_md),
                                                   one_md)), -400000)
    Uk = [U0, U1, U2, U3, U4]
    xHk = [ctx.rf_const(1)]
    for _ in range(4):
        xHk.append(ctx.rf_mul(xHk[-1], xH))
    U = {k: ctx.rf_mul(Uk[k], xHk[k]) for k in range(5)}
    E = ctx.common_den(U)
    Den = ctx.den_poly(E)
    F = ctx.clear(U, E)
    return F, Den, E


def mu_lo_of(ctx):
    ell = ctx.ell
    best = None
    for k in range(0, 1001):
        mk = Fraction(k, 1000)
        A = (ell + 4) + (ell - 1) * mk * mk
        w2 = Fraction(2 * ell + 3) ** 2 * mk * mk / (A * A)
        if w2 <= 1 - Fraction(99, 100) ** 2:
            best = k
        else:
            break
    return Fraction(best, 1000)


def coverage_check(ctx, mlo):
    """q(mu_lo)^2 >= (99/100)^2, exact."""
    ell = ctx.ell
    A = (ell + 4) + (ell - 1) * mlo * mlo
    w2 = Fraction(2 * ell + 3) ** 2 * mlo * mlo / (A * A)
    q2 = 1 - w2
    return q2, q2 >= Fraction(99, 100) ** 2


def w_increasing(ctx):
    """w' numerator (2l+3)(A - 2(l-1) mu^2 - ...) : w' = (2l+3)(A - mu A')/A^2;
    A - mu A' = (l+4) + (l-1)mu^2 - 2(l-1)mu^2 = (l+4) - (l-1) mu^2."""
    ell = ctx.ell
    num = {0: fmpq((2 * ell + 3) * (ell + 4)), 2: fmpq(-(2 * ell + 3) * (ell - 1))}
    ok, _ = verify_1d(num, fmpq(0), fmpq(1))
    return ok


def to_fmpq2(F):
    out = {}
    for t, poly in F.items():
        for j, c in poly.items():
            if c:
                out[(t, j)] = fmpq(c.numerator, c.denominator)
    return out


def main(L=10):
    results = {}
    for ell in range(3, L + 1):
        ctx = Ctx(ell)
        m = (ell - 1) * (ell + 4)
        # parametrisation identities (exact, symbolic via Fractions on samples is NOT a
        # proof; do them symbolically with sympy)
        import sympy as sp
        mu_ = sp.symbols("mu")
        A = (ell + 4) + (ell - 1) * mu_**2
        w = (2 * ell + 3) * mu_ / A
        s = (2 * ell + 3) * ((ell + 4) - (ell - 1) * mu_**2) / (5 * A)
        q2 = 1 - w**2
        assert sp.simplify(s**2 - (1 + 4 * m * q2 / 25)) == 0
        assert sp.simplify(w.subs(mu_, 1)) == 1 and sp.simplify(w.subs(mu_, 0)) == 0
        assert sp.simplify(s.subs(mu_, 1)) == 1     # delta(1) = 0
        F, Den, E = build_F(ctx)
        mlo = mu_lo_of(ctx)
        q2_lo, cov = coverage_check(ctx, mlo)
        assert cov, f"coverage failed for ell={ell}"
        # Den > 0 and F > 0
        Den_f = {k: fmpq(v.numerator, v.denominator) for k, v in Den.items()}
        okD, iD = verify_1d(Den_f, fmpq(mlo.numerator, mlo.denominator), fmpq(1))
        F2 = to_fmpq2(F)
        okF, iF = verify_2d(F2, fmpq(0), fmpq(1), fmpq(mlo.numerator, mlo.denominator), fmpq(1))
        okw = w_increasing(ctx)
        ok = okD and okF and okw
        results[ell] = ok
        print(f"ell={ell}: m={m} mu_lo={mlo} q(mu_lo)^2={float(q2_lo):.6f} "
              f"Den_exps={E} Den>0:{okD} F>0:{okF} w-inc:{okw} nodes={iF.get('nodes')}",
              flush=True)
        with open(os.path.join(OUT, f"F_ell{ell}.json"), "w") as fh:
            json.dump({"ell": ell, "mu_lo": str(mlo), "Den_exps": list(E),
                       "Den": {str(k): str(v) for k, v in Den.items()},
                       "F": {f"({t}, {j})": str(c) for t, pp in F.items()
                             for j, c in pp.items() if c}}, fh)
    print("PART I:", "ALL POSITIVE" if all(results.values()) else "FAILURES: " + str(results))
    return 0 if all(results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
