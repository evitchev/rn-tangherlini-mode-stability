"""Prototype S-certificate for target A1, l = 2 (results/p3/PREREG.md, METHOD.md).

    python -m p3.scert --out DIR --tier {T1,T2,T3,G1,NC-P1,TD-P1,TD-P2}

S = -f (1 - z) P, z = 1 - 1/rho (units r_H = 1).  Then V + S' - S^2 = f N / (64 rho^2 H^2) with
    N = U - 64 H^2 [ (1 - z) f_z P + f (-P + (1 - z) P_z + P^2) ],
and N >= 0 on [0, 1] (z) proves A >= 0 (METHOD.md, Proposition 3).

design_*  : untrusted.  Double-precision Riccati integration in tau = log(z/(1-z)) and a
            Chebyshev-Lobatto fit of P_true - EPS; coefficients become exact binary rationals.
verify_*  : the trust base.  N is built exactly (sympy) from TARGET.md's U_-, H_- (E0 against
            S5 (5.63b)); N > 0 by exact Bernstein enclosures (onset.bernstein, python-flint fmpq).
Fail-closed: VERIFIED and exit 0 only if every check holds; otherwise REJECT: <reason>, exit 1.
"""
import argparse
import math
import sys
import time
from fractions import Fraction

import sympy as sp
from flint import acb, arb, ctx, fmpq

from ki.potentials import H_TARGET, H_minus, U_TARGET, U_minus, d, m, x
from onset.bernstein import Poly2, Q, prove_sign
from onset.onset import param
from qnm1c.common import CertificateError, dump_json, provenance

z, mu = sp.symbols("z mu")
EPS = Fraction(1, 50)
TIERS = ("T1", "T2", "T3", "G1", "NC-P1", "TD-P1", "TD-P2")


def R(fr):
    """Exact Fraction (or int) -> sympy Rational."""
    fr = Fraction(fr)
    return sp.Rational(fr.numerator, fr.denominator)


# ---------------------------------------------------------------- setting (exact)
def setting(kind, tamper=False):
    """Exact sympy data in (z, mu): x, f, U, H, and m.  kind: 'D6' (l = 2, charge via mu) or
    'G1' (D = 10, l = 2, Q = 0)."""
    if kind == "D6":
        n, ell = 4, 2
        P = param(ell)
        U = U_TARGET + (x**2 * m * (1 + m * d) if tamper else 0)
        if sp.expand(U_minus(4) - U) != 0:
            raise CertificateError("E0: TARGET.md's U_- differs from S5 (5.63b) at n = 4")
        xH, dl = P["xH"], P["delta"]
        k3 = sp.cancel((1 - P["w"]) / (1 + P["w"]))              # kappa^(n-1) = x_H / x_-
        mm, H = P["m"], H_TARGET
    else:
        n, ell = 8, 2
        mm = (ell - 1) * (ell + n)
        U, H = U_minus(n), H_minus(n)
        xH, dl, k3 = sp.Integer(1), sp.Integer(0), sp.Integer(0)
    X = xH * (1 - z) ** (n - 1)
    f = (1 - (1 - z) ** (n - 1)) * (1 - k3 * (1 - z) ** (n - 1))
    sub = {m: mm, d: dl}
    return {"n": n, "m": mm, "x": X, "f": f, "fz": sp.diff(f, z),
            "U": U.subs(sub).subs(x, X), "H": H.subs(sub).subs(x, X)}


def N_expr(S, P):
    return S["U"] - 64 * S["H"] ** 2 * ((1 - z) * S["fz"] * P
                                        + S["f"] * (-P + (1 - z) * sp.diff(P, z) + P**2))


# ---------------------------------------------------------------- design (untrusted, floats)
def numeric(S, muv):
    sub = {} if muv is None else {mu: R(muv)}
    W = sp.lambdify(z, (S["U"] / (64 * S["H"] ** 2)).subs(sub), "math")
    f = sp.lambdify(z, S["f"].subs(sub), "math")
    fz = sp.lambdify(z, S["fz"].subs(sub), "math")
    return W, f, fz


def riccati_values(S, muv, znodes, h=0.002):
    """P_true at the given ascending z-nodes in [0, 1] (regular solution at the horizon)."""
    W, f, fz = numeric(S, muv)
    P0 = W(0.0) / fz(0.0)
    cinf = W(1.0)
    Pinf = (1 + math.sqrt(1 + 4 * cinf)) / 2
    rhs = lambda tau, P: (lambda zz: zz * (P - P * P + (W(zz) - (1 - zz) * fz(zz) * P) / f(zz)))(
        1 / (1 + math.exp(-tau)))
    out, tau, P = [], -27.0, P0
    for zk in znodes:
        if zk <= 0:
            out.append(P0)
            continue
        if zk >= 1:
            out.append(Pinf)
            continue
        tk = math.log(zk / (1 - zk))
        while tau < tk:
            hh = min(h, tk - tau)
            k1 = rhs(tau, P)
            k2 = rhs(tau + hh / 2, P + hh / 2 * k1)
            k3 = rhs(tau + hh / 2, P + hh / 2 * k2)
            k4 = rhs(tau + hh, P + hh * k3)
            P += hh / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
            tau += hh
        out.append(P)
    return out


def cheb_nodes(dg):
    return [(1 - math.cos(math.pi * k / dg)) / 2 for k in range(dg + 1)]


def cheb_coeffs(vals):
    """Chebyshev-Lobatto interpolation (DCT-I): coefficients c_j of sum c_j T_j(u), u in [-1, 1],
    for values at u_k = -cos(pi k / dg)."""
    dg = len(vals) - 1
    c = []
    for j in range(dg + 1):
        s = 0.0
        for k, v in enumerate(vals):
            w = 0.5 if k in (0, dg) else 1.0
            s += w * v * math.cos(math.pi * j * (dg - k) / dg)
        c.append(s * 2 / dg * (0.5 if j in (0, dg) else 1.0))
    return c


def cheb_to_monomial(c, a, b, var):
    """Exact sympy polynomial in var of sum c_j T_j(u), u = (2 var - a - b)/(b - a)."""
    u = (2 * var - a - b) / (b - a)
    T = [sp.Integer(1), u]
    while len(T) < len(c):
        T.append(sp.expand(2 * u * T[-1] - T[-2]))
    return sp.expand(sum(R(Fraction(cj)) * T[j] for j, cj in enumerate(c)))


def design_point(S, muv, dz=28):
    zs = cheb_nodes(dz)
    vals = [v - float(EPS) for v in riccati_values(S, muv, zs)]
    return cheb_to_monomial(cheb_coeffs(vals), 0, 1, z)


def design_box(S, ma, mb, dz=28, dm=4):
    zs = cheb_nodes(dz)
    mus = [ma + (mb - ma) * t for t in cheb_nodes(dm)]
    grid = [[v - float(EPS) for v in riccati_values(S, Fraction(mv).limit_denominator(10**12), zs)]
            for mv in mus]                                       # grid[j][k]: mu_j, z_k
    ck = [cheb_coeffs([grid[j][k] for j in range(dm + 1)]) for k in range(dz + 1)]   # in mu, per z node
    P = 0
    for jj in range(dm + 1):                                     # mu-coefficient jj as a z-interpolant
        cz = cheb_coeffs([ck[k][jj] for k in range(dz + 1)])
        Pz = cheb_to_monomial(cz, 0, 1, z)
        u = (2 * mu - R(ma) - R(mb)) / R(mb - ma)
        Tm = sp.chebyshevt(jj, u)
        P += Pz * sp.expand(Tm)
    return sp.expand(P)


# ---------------------------------------------------------------- verification (exact)
def parts(S, muv=None):
    """Numerators and denominators of U, H, f; the denominators must not depend on z."""
    sub = {} if muv is None else {mu: R(muv)}
    out = {}
    for k in ("U", "H", "f"):
        num, den = sp.fraction(sp.cancel(sp.together(S[k].subs(sub))))
        if den.has(z):
            raise CertificateError(f"denominator of {k} depends on z")
        out[k] = (sp.expand(num), sp.expand(den))
    return out


def N_times_L(pp, P, extra=0):
    """N * L with L = U_den H_den^2 f_den, as a polynomial; extra adds -64 H^2 * extra to N."""
    (Un, Ud), (Hn, Hd), (fn, fd) = pp["U"], pp["H"], pp["f"]
    br = (1 - z) * sp.diff(fn, z) * P + fn * (-P + (1 - z) * sp.diff(P, z) + P**2)
    return sp.expand(Un * Hd**2 * fd - 64 * Hn**2 * Ud * (br + extra * fd)), sp.expand(Ud * Hd**2 * fd)


def poly2_of(expr):
    p = sp.Poly(expr, z, mu)
    return Poly2({(i, j): Q(c) for (i, j), c in p.terms()})


def verify(S, P, mbox, stats, label, pieces=None, extra=0):
    """N > 0 on [0, 1] x mbox (mbox = (a, b); a = b for a point), via N L > 0 and L > 0."""
    a, b = (Q(v) for v in mbox)
    point = mbox[0] == mbox[1]
    pp = parts(S, mbox[0] if point and S["n"] == 4 else None)
    if point and S["n"] == 4:
        P = P.subs(mu, R(mbox[0]))
    NL, L = N_times_L(pp, P, extra)
    Lp = poly2_of(L)
    prove_sign(Lp, (fmpq(0), fmpq(1), a, b), 1, 30, stats, label + ": L > 0")
    p2 = poly2_of(NL)
    for (z0, z1) in (pieces or [(fmpq(0), fmpq(1))]):
        prove_sign(p2, (z0, z1, a, b), 1, 40, stats, label + ": N > 0")
    return {"deg_z": p2.dt, "deg_mu": p2.dm}


def poly_coeffs(P):
    return {str(k): str(v) for k, v in sp.Poly(P, z, mu).as_dict().items()}


# ---------------------------------------------------------------- NC-P1 (planted bound state)
ZA, ZB = sp.Rational(3, 10), sp.Rational(3, 5)


def bump():
    return (z - ZA) ** 2 * (ZB - z) ** 2


def nc_p1(S, P_T1, muv, stats):
    """(a) certify Q[phi0] < 0 for V + W, W = -K_p f b/rho^2, phi0 = b on [ZA, ZB];
    (b) the T1 certificate checked against V + W must REJECT."""
    sub = {mu: R(muv)}
    b = bump()
    phi = b
    Uq, Hq, fq = (S[k].subs(sub) for k in ("U", "H", "f"))
    q1 = sp.expand(fq * sp.diff(phi, z) ** 2 * (1 - z) ** 2)
    W = sp.lambdify(z, Uq / (64 * Hq**2), "math")
    # design of K_p (floats): twice the ratio of the positive part to the bump part
    fl = lambda e: sp.lambdify(z, e, "math")
    nq = 2000
    zs = [float(ZA) + (float(ZB) - float(ZA)) * (i + 0.5) / nq for i in range(nq)]
    hz = (float(ZB) - float(ZA)) / nq
    I1 = sum(fl(q1)(t) + W(t) * fl(phi**2)(t) for t in zs) * hz
    I2 = sum(fl(b * phi**2)(t) for t in zs) * hz
    Kp = sp.Integer(math.ceil(2 * I1 / I2)) if I1 > 0 else sp.Integer(1)
    # (a) rigorous: Q = int_{ZA}^{ZB} [f phi_z^2 (1-z)^2 + (U/(64H^2) - K_p b) phi^2] dz
    ctx.prec = 128
    polys = {k: sp.Poly(sp.expand(e), z).all_coeffs()[::-1]
             for k, e in (("q1", q1), ("U", Uq), ("H", Hq), ("phi2", sp.expand(phi**2)),
                          ("bphi2", sp.expand(Kp * b * phi**2)))}
    cf = {k: [acb(Q(c)) for c in v] for k, v in polys.items()}

    def horner(cs, t):
        acc = acb(0)
        for c in reversed(cs):
            acc = acc * t + c
        return acc

    def integrand(t, analytic):
        Hv = horner(cf["H"], t)
        return (horner(cf["q1"], t) + horner(cf["U"], t) / (64 * Hv * Hv) * horner(cf["phi2"], t)
                - horner(cf["bphi2"], t))

    Qv = acb.integral(integrand, acb(Q(ZA)), acb(Q(ZB)))
    certified = bool(Qv.real < 0)
    # (b) the T1 certificate against V + W: piecewise N on [0, ZA], [ZA, ZB], [ZB, 1]
    # outside the bump V + W = V: the T1 certificate must still hold there (not part of the control)
    verify(S, P_T1, (muv, muv), stats, "NC-P1 outside the bump", pieces=[(fmpq(0), Q(ZA)), (Q(ZB), fmpq(1))])
    rejected, msg = False, ""
    try:
        verify(S, P_T1, (muv, muv), stats, "NC-P1 on the bump", pieces=[(Q(ZA), Q(ZB))], extra=Kp * b)
    except CertificateError as exc:
        rejected, msg = True, str(exc)[:300]
    return {"K_p": str(Kp), "Q_phi0": Qv.real.str(10), "bound_state_certified": certified,
            "T1_certificate_rejected_on_V_plus_W": rejected, "message": msg}


# ---------------------------------------------------------------- tiers
def run_tier(tier):
    rec, stats = {"tier": tier, "EPS": str(EPS)}, {}
    t0 = time.time()
    if tier == "G1":
        S = setting("G1")
        P = design_point(S, None)
        rec["t_design_s"] = round(time.time() - t0, 2)
        t1 = time.time()
        rec.update(verify(S, P, (0, 0), stats, "G1"))
        rec["t_verify_s"] = round(time.time() - t1, 2)
        rec["P"] = poly_coeffs(P)
        rec["boxes"] = stats
        return rec
    S = setting("D6", tamper=(tier == "TD-P1"))
    if tier in ("T1", "NC-P1", "TD-P1", "TD-P2"):
        muv = Fraction(1, 6)
        P = design_point(S, muv)
        if tier == "TD-P2":                     # raise P(0) by 1/10 above the horizon bound
            W0 = (S["U"] / (64 * S["H"] ** 2 * S["fz"])).subs({mu: R(muv)}).subs(z, 0)
            P = P + (W0 - P.subs(z, 0)) + sp.Rational(1, 10)
        rec["t_design_s"] = round(time.time() - t0, 2)
        t1 = time.time()
        if tier == "NC-P1":
            rec["NC-P1"] = nc_p1(S, P, muv, stats)
            ok = rec["NC-P1"]["bound_state_certified"] and rec["NC-P1"]["T1_certificate_rejected_on_V_plus_W"]
            if not ok:
                raise CertificateError(f"NC-P1 not as registered: {rec['NC-P1']}")
        else:
            rec.update(verify(S, P, (muv, muv), stats, tier))
        rec["t_verify_s"] = round(time.time() - t1, 2)
        rec["mu"] = str(muv)
        rec["P"] = poly_coeffs(P)
        rec["boxes"] = stats
        return rec
    boxes = ([(Fraction(97, 600), Fraction(103, 600))] if tier == "T2"
             else [(Fraction(12 + k, 100), Fraction(13 + k, 100)) for k in range(8)])
    rec["boxes_mu"] = []
    for (ma, mb) in boxes:
        tb = time.time()
        P = design_box(S, ma, mb)
        td = time.time() - tb
        st = {}
        info = verify(S, P, (ma, mb), st, f"{tier} mu in [{ma}, {mb}]")
        rec["boxes_mu"].append({"mu": [str(ma), str(mb)], "t_design_s": round(td, 2),
                                "t_verify_s": round(time.time() - tb - td, 2), "bernstein": st,
                                "P": poly_coeffs(P), **info})
    return rec


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--tier", choices=TIERS, required=True)
    a = ap.parse_args(argv)
    t0 = time.time()
    record = {"claim": "results/p3/PREREG.md", "tier": a.tier, "provenance": provenance()}
    try:
        record["result"] = run_tier(a.tier)
        verdict = "VERIFIED"
    except CertificateError as exc:
        verdict = f"REJECT: {exc}"
    except Exception as exc:  # noqa: BLE001  (fail-closed)
        verdict = f"REJECT: exception {type(exc).__name__}: {exc}"
    record["verdict"] = verdict
    record["timing"] = {"t_total_s": round(time.time() - t0, 2)}
    dump_json(record, f"{a.out}/result.json")
    r = record.get("result", {})
    for k in ("deg_z", "deg_mu", "boxes", "t_design_s", "t_verify_s", "NC-P1"):
        if k in r:
            print(f"{k}: {r[k]}")
    for bx in r.get("boxes_mu", []):
        print(f"mu {bx['mu']}: deg ({bx['deg_z']}, {bx['deg_mu']}), Bernstein {bx['bernstein']}, "
              f"design {bx['t_design_s']} s, verify {bx['t_verify_s']} s")
    print(verdict[:400])
    return 0 if verdict == "VERIFIED" else 1


if __name__ == "__main__":
    sys.exit(main())
