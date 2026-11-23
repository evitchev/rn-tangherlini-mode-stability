"""HD-E, Kimi's own route: E1 (per D), E2 (13 bands), exact.

For each (n, ell, q_hi): build U_-(t x_H) = F(t, mu)/Den(mu) exactly with my own
QQ(mu) arithmetic (rfg.Ctx, per-(n,ell) factors A, B, mu+1), using my own KI (5.63b)
transcription at general n (imported from my p3 audit's build.py).  Then:
  - parametrisation identities (s^2 law, q(1)=0, q(0)=1, delta(1)=0), w increasing;
  - mu_lo = k/10000 largest with w(mu_lo)^2 <= 1 - q_hi^2 (binary search), and the exact
    coverage check q(mu_lo)^2 >= q_hi^2;
  - Den > 0 on [mu_lo, 1] and F > 0 on [0,1] x [mu_lo, 1] (my exact Bernstein verifier).
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
from build import ki_Usymbol   # my own general-n KI (5.62b)/(5.63b) transcription

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "built")
os.makedirs(OUT, exist_ok=True)

import sympy as sp


def UH_general(n, m, delta):
    """U_-, H_- as polynomials in x (sympy, symbolic m, delta)."""
    return ki_Usymbol(n)


def blocks(ctx):
    """delta(ell), xH as rf for ctx = (ell, n)."""
    ell, n = ctx.ell, ctx.n
    m = (ell - 1) * (ell + n)
    B = 2 * ell + n - 1
    A = ctx.A
    # s = B ((l+n) - (l-1) mu^2) / ((n+1) A);  delta = (s-1)/(2m)
    s_num = ctx.p_scale({0: Fraction(ell + n), 2: Fraction(-(ell - 1))},
                        Fraction(B, n + 1))
    s = (s_num, (1, 0, 0))
    delta = ctx.rf_scale(ctx.rf_sub(s, ctx.rf_const(1)), Fraction(1, 2 * m))
    # xH = 2 A / ((mu+1) Bpoly)
    xH = (ctx.p_scale(A, 2), (0, 1, 1))
    return m, delta, xH


def build_F(ctx, tamper_const=None):
    """U_-(t x_H) as dict {t_exp: rf}; F, Den, E.  tamper_const adds to U's constant."""
    ell, n = ctx.ell, ctx.n
    m = (ell - 1) * (ell + n)
    mm, dd, xx = sp.symbols("m d x")
    Ux, Hx = ki_Usymbol(n)
    # coefficients of x^k, as sympy polys in (m, d)
    Uc = [sp.expand(Ux).coeff(xx, k) for k in range(5)]
    # rf for delta
    m_rf, delta, xH = blocks(ctx)
    def ev(expr):
        """sympy poly in (m,d) -> rf, with m an integer."""
        expr = sp.Poly(sp.expand(expr), mm, dd)
        r = ctx.rf_const(0)
        for (i, j), c in expr.terms():
            term = ctx.rf_const(sp.Rational(c) * m**i)
            for _ in range(j):
                term = ctx.rf_mul(term, delta)
            r = ctx.rf_add(r, term)
        return r
    Ur = {}
    for k in range(5):
        ck = ev(Uc[k])
        if tamper_const is not None and k == 0:
            ck = ctx.rf_add(ck, ctx.rf_const(tamper_const))
        Ur[k] = ck
    U = {}
    xHk = ctx.rf_const(1)
    for k in range(5):
        Ur[k] = ctx.rf_mul(Ur[k], xHk)
        xHk = ctx.rf_mul(xHk, xH)
        if Ur[k][0]:
            U[k] = Ur[k]
    E = ctx.common_den(U)
    Den = ctx.den_poly(E)
    F = ctx.clear(U, E)
    return F, Den, E


def mu_lo_of(ctx, q_hi, grid=10000):
    """Largest k/grid with w(k/grid)^2 <= 1 - q_hi^2 (binary search)."""
    ell, n = ctx.ell, ctx.n
    B = 2 * ell + n - 1
    lim = 1 - q_hi**2

    def w2(k):
        mk = Fraction(k, grid)
        A = (ell + n) + (ell - 1) * mk * mk
        return Fraction(B * B) * mk * mk / (A * A)

    lo, hi = 0, grid
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if w2(mid) <= lim:
            lo = mid
        else:
            hi = mid
    return Fraction(lo, grid)


def coverage_ok(ctx, mlo, q_hi):
    ell, n = ctx.ell, ctx.n
    B = 2 * ell + n - 1
    A = (ell + n) + (ell - 1) * mlo * mlo
    q2 = 1 - Fraction(B * B) * mlo * mlo / (A * A)
    return q2, q2 >= q_hi**2


def param_checks(ctx):
    """Exact parametrisation identities at (n, ell), symbolic."""
    ell, n = ctx.ell, ctx.n
    m = (ell - 1) * (ell + n)
    B = 2 * ell + n - 1
    mu_ = sp.symbols("mu")
    A = (ell + n) + (ell - 1) * mu_**2
    w = B * mu_ / A
    s = B * ((ell + n) - (ell - 1) * mu_**2) / ((n + 1) * A)
    q2 = 1 - w**2
    assert sp.simplify(s**2 - (1 + 4 * m * q2 / (n + 1)**2)) == 0, "s^2 law"
    assert sp.simplify(w.subs(mu_, 1)) == 1 and sp.simplify(w.subs(mu_, 0)) == 0
    assert sp.simplify(s.subs(mu_, 1)) == 1
    # w increasing: numerator of w' = B((l+n) - (l-1) mu^2)/A^2 * ... : check with verifier
    wp_num = {0: fmpq(B * (ell + n)), 2: fmpq(-B * (ell - 1))}
    ok, _ = verify_1d(wp_num, fmpq(0), fmpq(1))
    assert ok, "w not increasing"


def to_fmpq2(F):
    out = {}
    for t, poly in F.items():
        for j, c in poly.items():
            if c:
                out[(t, j)] = fmpq(c.numerator, c.denominator)
    return out


def check_one(n, ell, q_hi, tag=""):
    ctx = Ctx(ell, n)
    param_checks(ctx)
    F, Den, E = build_F(ctx)
    mlo = mu_lo_of(ctx, q_hi)
    q2_lo, cov = coverage_ok(ctx, mlo, q_hi)
    if not cov:
        return False, {"reason": "coverage failed", "mu_lo": str(mlo)}
    Den_f = {k: fmpq(v.numerator, v.denominator) for k, v in Den.items()}
    okD, iD = verify_1d(Den_f, fmpq(mlo.numerator, mlo.denominator), fmpq(1))
    okF, iF = verify_2d(to_fmpq2(F), fmpq(0), fmpq(1),
                        fmpq(mlo.numerator, mlo.denominator), fmpq(1))
    info = {"mu_lo": str(mlo), "q2(mu_lo)": float(q2_lo), "Den_exps": list(E),
            "Den_ok": okD, "F_ok": okF, "F_nodes": iF.get("nodes"),
            "F_info": {k: str(v)[:120] for k, v in iF.items()}}
    return okD and okF, info


# The 13 E2 bands: (D, ell, q_split)
BANDS = [(7, 2, Fraction(948, 1000)), (7, 3, Fraction(977, 1000)),
         (8, 3, Fraction(944, 1000)), (8, 4, Fraction(983, 1000)),
         (9, 3, Fraction(921, 1000)), (9, 4, Fraction(952, 1000)), (9, 5, Fraction(987, 1000)),
         (10, 3, Fraction(490, 1000)), (10, 4, Fraction(920, 1000)), (10, 5, Fraction(961, 1000)),
         (11, 4, Fraction(897, 1000)), (11, 5, Fraction(929, 1000)), (11, 6, Fraction(968, 1000))]

L_EL = {5: 4, 6: 5, 7: 6, 8: 6, 9: 7}   # n -> ell_el
Q99 = Fraction(99, 100)


def main(l0_map=None):
    """l0_map: n -> my Lemma-U threshold (from lemmaUn.py).  E1 covers [l_el, l0]."""
    results = {}
    for n in range(5, 10):
        D = n + 2
        l0 = l0_map[n]
        for ell in range(L_EL[n], l0 + 1):
            ok, info = check_one(n, ell, Q99)
            results[f"E1 D={D} l={ell}"] = (ok, info)
            print(f"E1 D={D} l={ell}: {'POSITIVE' if ok else 'REJECT'} "
                  f"mu_lo={info.get('mu_lo')} nodes={info.get('F_nodes')}", flush=True)
    for D, ell, qs in BANDS:
        n = D - 2
        ok, info = check_one(n, ell, qs)
        results[f"E2 D={D} l={ell}"] = (ok, info)
        print(f"E2 D={D} l={ell} q<={qs}: {'POSITIVE' if ok else 'REJECT'} "
              f"mu_lo={info.get('mu_lo')} nodes={info.get('F_nodes')}", flush=True)
    with open(os.path.join(HERE, "e12_results.json"), "w") as fh:
        json.dump({k: {"ok": v[0], **v[1]} for k, v in results.items()}, fh, indent=1)
    bad = {k: v for k, v in results.items() if not v[0]}
    print("E1+E2:", "ALL POSITIVE" if not bad else f"FAILURES: {list(bad)}")
    return 0 if not bad else 1


if __name__ == "__main__":
    # l0_map is injected by run_all.py after Lemma U(n) is derived
    raise SystemExit(main())
