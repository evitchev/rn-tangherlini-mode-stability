"""HD-X controls (Kimi):
(a) HD-X-E's check at D=7, ell=3 (= n-2, a band): must REJECT (corner value < 0 at (1,0));
(b) strict bound for ell = n-1 (D=7, ell=4) on its full box: refused with exact 0 at (1,0);
(c) HD-X-2's design with ehat below (1/k - 1/20) and above (2/(k-l) + 1/8) the window,
    band 7-2: the T chart must reject;
(d) HD-X-S's design with a = -4/5 (outside the window) at band 7-3: a chart must reject;
(e) planted bound state in the throat, band 7-2 at mu = 1/64: Q[b] < 0 rigorously over the
    whole support (weights as derived), then the certificate refuses the planted potential;
(f) verifier tamper: KATs.
"""
import json
import os
import sys
from fractions import Fraction

import sympy as sp
from flint import acb, fmpq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "[kimi-folder]/bhm-hd-elementary-audit-2026-10-23/own")
sys.path.insert(0, "[kimi-folder]/bhm-p3-audit-2026-10-22/own")
from rfg import Ctx
from hd import build_F
from hdxe import mu_lo_of, to_fmpq2
from hdx2 import build_NL
from hdxs import build_NL as build_NL_S, check_band as check_band_S
from verify import verify_1d, verify_2d, kat
from build import ki_Usymbol

HERE = os.path.dirname(os.path.abspath(__file__))


def flat(D):
    return {k: fmpq(v.numerator, v.denominator) for k, v in D.items() if v}


def chart_T(Nc):
    NT = {}
    for i, poly in Nc.items():
        for j, c in poly.items():
            NT[(i, i + j)] = NT.get((i, i + j), Fraction(0)) + c
    T = {}
    okd = True
    for (iz, im), c in NT.items():
        if im < 2:
            okd = False
        else:
            T[(iz, im - 2)] = c
    return T if okd else None


def main():
    # ---- (a) HD-X-E at D=7, ell=3 (n=5, ell = n-2)
    ctx = Ctx(3, 5)
    F, Den, E = build_F(ctx)
    mlo = mu_lo_of(ctx)
    okA, iA = verify_2d(to_fmpq2(F), fmpq(0), fmpq(1), fmpq(0),
                        fmpq(mlo.numerator, mlo.denominator))
    F10 = sum(poly.get(0, Fraction(0)) for poly in F.values())
    print(f"(a) D=7 ell=3 (a band): {'REJECT (correct)' if not okA else 'PASS (BAD)'}; "
          f"F(1,0) = {F10} (< 0: {F10 < 0})")
    ok_a = (not okA) and F10 < 0

    # ---- (b) strict bound for ell = n-1 = 4 at D = 7
    ctx = Ctx(4, 5)
    F, Den, E = build_F(ctx)
    mlo = mu_lo_of(ctx)
    okB, iB = verify_2d(to_fmpq2(F), fmpq(0), fmpq(1), fmpq(0),
                        fmpq(mlo.numerator, mlo.denominator))
    F10 = sum(poly.get(0, Fraction(0)) for poly in F.values())
    print(f"(b) D=7 ell=4 strict: {'REJECT (correct)' if not okB else 'PASS (BAD)'}; "
          f"F(1,0) = {F10} (exactly 0: {F10 == 0}); info={iB}")
    ok_b = (not okB) and F10 == 0

    # ---- (c) ehat outside the window (1/4, 1) at band 7-2
    oks = []
    for tag, shift in [("below", Fraction(1, 5) - Fraction(5, 8)), ("above", Fraction(9, 8) - Fraction(5, 8))]:
        ctx = Ctx(2, 5)
        Den, Nc, E = build_NL(ctx, ehat_shift=shift)
        T = chart_T(Nc)
        if T is None:
            print(f"(c) ehat {tag}: T division failed")
            oks.append(False)
            continue
        okT, iT = verify_2d(flat(T), fmpq(0), fmpq(8), fmpq(0), fmpq(1, 32))
        print(f"(c) ehat {tag} the window: T chart "
              f"{'REJECT (correct)' if not okT else 'PASS (BAD)'} "
              f"{ {k: str(v)[:90] for k, v in iT.items()} }")
        oks.append(not okT)
    ok_c = all(oks)

    # ---- (d) HD-X-S design with a = -4/5 at band 7-3
    designs = json.load(open(os.path.join(HERE, "..", "data", "designs.json")))
    r = check_band_S(7, 3, designs["7,3"] | {"a": "-4/5"})
    print(f"(d) HD-X-S a=-4/5 at 7-3: {'REJECT (correct)' if not r['ok'] else 'PASS (BAD)'} "
          f"POS={r['POS']}")
    ok_d = not r["ok"]

    # ---- (e) planted bound state in the throat, band 7-2 at mu = 1/64
    # the negative region of U_- at (n=5, ell=2, mu=1/64): find z_U
    n, ell = 5, 2
    m = (ell - 1) * (ell + n)
    mu_c = Fraction(1, 64)
    Bc = 2 * ell + n - 1
    A_ = (ell + n) + (ell - 1) * mu_c**2
    w_ = Bc * mu_c / A_
    q2_ = 1 - w_**2
    s_ = Bc * ((ell + n) - (ell - 1) * mu_c**2) / ((n + 1) * A_)
    del_ = (s_ - 1) / (2 * m)
    xH_ = 2 / (1 + w_)
    mm, dd, xx = sp.symbols("m d x")
    Ux, Hx = ki_Usymbol(n)
    U1 = sp.expand(Ux.subs({mm: m, dd: sp.Rational(del_.numerator, del_.denominator),
                            xx: sp.Rational(xH_.numerator, xH_.denominator) * (1 - sp.Symbol("z")) ** (n - 1)}))
    zv = sp.Symbol("z")
    roots = [rt for rt in sp.nroots(U1, n=30) if rt.is_real and 0 < float(rt) < 1]
    z_U = min(float(r) for r in roots) if roots else None
    print(f"(e) z_U (first root of U_- at mu=1/64) = {z_U}")
    za = int(z_U / 5 * 10000) / 10000
    zb = int(z_U * 4 / 5 * 10000) / 10000
    print(f"(e) support [za, zb] = [{za}, {zb}]")

    def b_and_db(r):
        z = 1 - 1 / r
        g = (z - acb(str(za))) * (acb(str(zb)) - z)
        gp = acb(str(zb)) + acb(str(za)) - 2 * z
        return g**2, 2 * g * gp / r**2

    Uc = [sp.expand(Ux.subs({mm: m, dd: sp.Rational(del_.numerator, del_.denominator)})).coeff(xx, k)
          for k in range(5)]
    Hc = [sp.expand(Hx.subs({mm: m, dd: sp.Rational(del_.numerator, del_.denominator)})).coeff(xx, k)
          for k in range(2)]

    def Uv(xv):
        return sum(acb(str(c)) * xv**k for k, c in enumerate(Uc))

    def Hv(xv):
        return sum(acb(str(c)) * xv**k for k, c in enumerate(Hc))

    ra, rb = 1 / (1 - zb), 1 / (1 - za)
    import flint
    flint.ctx.dps = 100
    def acbf(fr):
        return acb(str(fr))
    def Aint(r):
        bv, br = b_and_db(r)
        xv = acbf(xH_) / r**(n - 1)
        fv = 1 - xv + acbf(q2_) * xv**2 / 4
        return fv * br**2 + Uv(xv) / (64 * r**2 * Hv(xv)**2) * bv**2

    def Cint(r):
        bv, _ = b_and_db(r)
        return bv**3 / r**2

    lo = acbf(Fraction(1)) / (1 - acbf(Fraction(209, 10000)))
    hi = acbf(Fraction(1)) / (1 - acbf(Fraction(837, 10000)))
    A = acb.integral(lambda t, _: Aint(t), lo, hi)
    C = acb.integral(lambda t, _: Cint(t), lo, hi)
    K = int(2 * float(A.real.upper()) / float(C.real.lower())) + 1
    Q = A - K * C
    print(f"(e)(i) A = {A}, C = {C}, K = {K}, Q = {Q}, rigorously < 0: {bool(Q.real.upper() < 0)}")
    ok_e1 = bool(Q.real.upper() < 0)

    # (e)(ii): the band's certificate against the planted potential, at mu = 1/64:
    # rebuild NL with U -> U - 64 K H^2 b (b as a polynomial in z), evaluate at mu_c,
    # and check N' < 0 somewhere on the support (exact).
    ctx = Ctx(2, 5)
    Den, Nc, E = build_NL(ctx)
    # the bump, as z-poly with unit rf
    bz = ((zv - sp.Rational(str(za))) * (sp.Rational(str(zb)) - zv)) ** 2
    bz = sp.expand(bz)
    # N' = N - 64 K H^2 b  =>  NL' = NL - 64 K H^2 b S^2 R^2 ... in my normalisation
    # NL = N S^2 R^2 (cleared); the tamper subtracts 64 K H^2 b from N, i.e.
    # NL' = NL - 64 K H^2 b S^2 R^2 (before clearing); after clearing by Den (which is
    # mu-only), N' Den = (NL - 64 K H^2 b S^2 R^2) ... careful: my NL = (N S^2 R^2) * Den.
    # Work instead with N directly at mu = mu_c: evaluate my NL at mu_c (exact),
    # divide by (S^2 R^2) at mu_c, subtract 64 K H^2 b at mu_c, and check.
    def eval_at_mu(Nc, mu):
        out = {}
        for i, poly in Nc.items():
            v = Fraction(0)
            for j, c in poly.items():
                v += c * mu**j
            out[i] = v
        return out
    NL_at = eval_at_mu(Nc, mu_c)
    Den_at = sum(c * mu_c**j for j, c in Den.items())
    # N at mu_c = NL_at / (S^2 R^2) at mu_c / Den_at; on the support z > 0 so S^2 R^2 > 0
    # there; sign(N') = sign(NL' ) where NL' = NL_at - 64 K H^2 b S^2 R^2 Den_at^-1 * ...
    # Rather than divide: the claim is N' = N - 64 K H^2 b;  N = NL/(S^2 R^2 Den).
    # Work with M := N' * Den = NL/(S^2 R^2) - 64 K H^2 b Den: still rational.
    # Simplest exact route: evaluate everything at mu_c as rational z-polynomials and
    # divide by S^2 R^2 (polynomial division).
    # (e)(ii): rebuild NL with the planted U and refuse it on the T chart at mu = mu_c.
    # N -> N - 64 K H^2 b, so NL -> NL - 64 K H^2 b S^2 R^2 (then clear by Den as before).
    ctx2 = Ctx(2, 5)
    Den2, Nc2, E2 = build_NL(ctx2)
    # exact negativity of the planted N at the bump centre, z0 = (za+zb)/2, mu = mu_c:
    # N' = NL'/(S^2 R^2 Den); evaluate NL' at (z0, mu_c) exactly via Fractions.
    import hdx2 as H2mod
    # rebuild pieces to get S, R at mu_c as rationals: S = eps_n + eps_d z with
    # eps = ehat w/(1+w), ehat = 5/8 at this band:
    ehat = Fraction(5, 8)
    w_r = Fraction(w_.numerator, w_.denominator)
    eps_n_r = ehat * w_r
    eps_d_r = 1 + w_r
    k = n - 1
    z0 = (Fraction(str(za)) + Fraction(str(zb))) / 2
    from math import comb
    R_at = sum((1 - z0) ** j for j in range(k))
    S_at = eps_n_r + eps_d_r * z0
    # U, H at (xH_ (1-z0)^k, mu_c):
    U_at = sum(Fraction(sp.Rational(c)) * (xH_ * (1 - z0) ** k) ** kk for kk, c in enumerate(Uc))
    H_at = sum(Fraction(sp.Rational(c)) * (xH_ * (1 - z0) ** k) ** kk for kk, c in enumerate(Hc))
    NL_at_z0 = Fraction(0)
    for i, poly in Nc2.items():
        for j, c in poly.items():
            NL_at_z0 += c * z0**i * mu_c**j
    Den_at = sum(c * mu_c**j for j, c in Den2.items())
    b_at = ((z0 - Fraction(str(za))) * (Fraction(str(zb)) - z0)) ** 2
    N_at_z0 = NL_at_z0 / (S_at**2 * R_at**2 * Den_at)
    Np_at_z0 = N_at_z0 - 64 * K * H_at**2 * b_at
    print(f"(e)(ii) at the bump centre: N = {float(N_at_z0):.4f}, "
          f"N' = {float(Np_at_z0):.4f} (< 0: {Np_at_z0 < 0})")
    ok_e2 = Np_at_z0 < 0
    # and the full planted NL on the T chart must reject:
    bZ = {}
    for m_, c in sp.Poly(bz, sp.Symbol("z")).terms():
        bZ[m_[0]] = Fraction(sp.Rational(c))
    # H^2 b S^2 R^2 as z-poly of rf, then clear by Den:
    Hrf = {}
    Y = {0: ctx2.rf_const(1), 1: ctx2.rf_const(-1)}
    y = H2mod.z_pow(ctx2, Y, k)
    H1x = None
    _, delta, xH, w, q2 = H2mod.blocks(ctx2)
    mm, dd, xx = sp.symbols("m d x")
    Hc_rf = [sp.expand(Hx).coeff(xx, i) for i in range(2)]
    def ev2(expr):
        expr = sp.Poly(sp.expand(expr), mm, dd)
        r = ctx2.rf_const(0)
        for (i, j), cc in expr.terms():
            term = ctx2.rf_const(sp.Rational(cc) * m**i)
            for _ in range(j):
                term = ctx2.rf_mul(term, delta)
            r = ctx2.rf_add(r, term)
        return r
    H0 = [ev2(Hc_rf[0]), ev2(Hc_rf[1])]
    Hrf = {0: H0[0]}
    H1x = ctx2.rf_mul(H0[1], xH)
    Hrf = H2mod.z_add(ctx2, Hrf, {j: ctx2.rf_mul(v, H1x) for j, v in y.items()})
    H2 = H2mod.z_mul(ctx2, Hrf, Hrf)
    Brf = {i: ctx2.rf_const(c) for i, c in bZ.items()}
    Srf = {0: ctx2.rf_scale(w, Fraction(5, 8)), 1: ctx2.rf_add(ctx2.rf_const(1), w)}
    Rrf = {}
    Yj = {0: ctx2.rf_const(1)}
    for j in range(k):
        Rrf = H2mod.z_add(ctx2, Rrf, Yj)
        Yj = H2mod.z_mul(ctx2, Yj, Y)
    bump = H2mod.z_mul(ctx2, H2mod.z_mul(ctx2, H2, Brf), H2mod.z_mul(ctx2, H2mod.z_mul(ctx2, Srf, Srf), H2mod.z_mul(ctx2, Rrf, Rrf)))
    NLp = {}
    for i in set(Nc2) | set(bump):
        out = {}
        A = Nc2.get(i, {})
        Bv = bump.get(i)
        Bv = Bv[0] if Bv is not None else {}
        for j, c in A.items():
            out[j] = c
        for j, c in Bv.items():
            out[j] = out.get(j, Fraction(0)) - 64 * K * c
        NLp[i] = {j: c for j, c in out.items() if c}
    T2 = chart_T(NLp)
    okT2, iT2 = verify_2d(flat(T2), fmpq(0), fmpq(8), fmpq(0), fmpq(1, 32))
    print(f"(e)(ii) planted NL on the T chart: {'REJECT (correct)' if not okT2 else 'PASS (BAD)'} "
          f"{ {k: str(v)[:90] for k, v in iT2.items()} }")
    ok_e2 = ok_e2 and not okT2
    ok_e = ok_e1 and ok_e2
    # (f) verifier tamper: KAT suite
    ok_f = kat()
    okall = all([ok_a, ok_b, ok_c, ok_d, ok_e, ok_f])
    print("CONTROLS (a)-(f):", "ALL OK" if okall else "FAILURE")
    return 0 if okall else 1


if __name__ == "__main__":
    raise SystemExit(main())
