"""Stage A2, A2-S (results/a2/s/PREREG.md): the singular S-certificate for D = 6, l = 2 and q in [q(1/8), 1].

    python -m a2.scert --out DIR [--control NAME] [--root REPO]

Units r_H = 1, z = 1 - 1/rho, mu the charge parameter of TARGET.md section 1 (q = 1 at mu = 0).  The design is A2-PILOT's
(BHM-095): P = a (1 + eps)/(z + eps) + p0(z), a = -2/5, eps = w/(3(1 + w)) = eps_n/eps_d, p0 the recorded degree-12
Chebyshev series, converted exactly to monomials.  With S = eps_d z + eps_n (S_z = eps_d) and Pi = a (eps_d + eps_n) + p0 S,
P = Pi/S, and
    NL := N S^2 L = Un Hd^2 fd S^2 - 64 Hn^2 Ud [(1 - z) fzn Pi S + fn (-Pi S + (1 - z)(Pi_z S - eps_d Pi) + Pi^2)],
a polynomial in (z, mu), with L = Ud Hd^2 fd > 0 (hd.scert's exact parts at n = 4).  NL vanishes at the corner (0, 0),
so [0, 1] x [0, MU1] is covered by four charts:
    O   (z, mu) in [Z1, 1] x [0, MU1]            NL > 0
    O'  (z, mu) in [0, Z1] x [MUT, MU1]          NL > 0
    T   z = mu zeta, (zeta, mu) in [0, ZT] x [0, MUT]      T = NL(mu zeta, mu)/mu^2 > 0
    C   mu = z sigma, (z, sigma) in [0, Z1] x [0, SIG1]    C = NL(z, z sigma)/z^2 > 0
with the exact divisions checked (DIV-T, DIV-C) and the coverage ZT SIG1 >= 1, ZT MUT <= Z1, Z1 SIG1 <= MU1 (COVER).
For every (z, mu) in (0, 1) x [0, MU1] some chart gives NL > 0, and S > 0, L > 0 there, so N > 0, and A_{2,q} >= 0 by
Proposition 3 for P C^1 on (0, 1) (Lean prop3_Ioo / prop3_Dn).
Gates: KAT, E0, H, PARAM, DESIGN (the pilot record's seal), G-RES (N(0) at q = 1 for P = a/z + p, symbolic in l and a),
COVER, L, S, DIV-T, DIV-C, and the positivity of the four charts.  THROAT (information): T(zeta, 0) against the pencil limit.
Fail-closed: VERIFIED and exit 0 only if every check holds.
--control (each with its registered verdict, PREREG section 4):
    nc-a2       U - 2 H^2 x^4: the extremal throat coefficient becomes -1/4 - 1/36, so N(0) < 0 at q = 1 for every a
    nc-zm       U - H^2 x^4 (coefficient -1/4) with a = -1/2: N(0) = 0 at q = 1, the zero margin
    nc-res      the residue a = -7/10, outside the window (-2/3, -1/3)
    nc-bound    a planted bound state at q = 1 on [1/20, 1/5]: (a) its trial function has certified negative energy, (b) the
                certificate is refused there
    td-coeff    U's coefficient 7680 changed to 7681: E0 must fail
    td-verifier the verifier's acceptance threshold lowered to -1: the KATs must fail
    td-chart    the throat chart without the division by mu^2
    td-cover    SIG1 = 1/16, so ZT SIG1 < 1
"""
import argparse
import datetime
import hashlib
import json
import math
import os
import sys
import time
from fractions import Fraction

import sympy as sp
from flint import acb, ctx, fmpq

from a1.p1 import kats, plain, tampered_prove_sign
from hd.elementary import param_n
from hd.scert import Exact, z
from ki.potentials import H_TARGET, H_minus, U_TARGET, U_minus, d, m, x
from onset.bernstein import Poly2, Q, prove_sign
from onset.onset import mu
from p3.scert import cheb_to_monomial
from qnm1c.common import CertificateError, dump_json, provenance

CONTROLS = ("none", "nc-a2", "nc-zm", "nc-res", "nc-bound", "td-coeff", "td-verifier", "td-chart", "td-cover")
N_DIM, ELL = 4, 2
A_RES = sp.Rational(-2, 5)
MU1, Z1, ZT, SIG1, MUT = sp.Rational(1, 8), sp.Rational(1, 4), sp.Integer(8), sp.Rational(1, 8), sp.Rational(1, 32)
PILOT_RECORD = "results/a2/pilot/runs/record/main/result.json"
MAX_DEPTH = 40
ZA, ZB = sp.Rational(1, 20), sp.Rational(1, 5)


def sealed_hash(root, path):
    with open(os.path.join(root, "SEALED.sha256")) as fh:
        for line in fh:
            parts = line.split()
            if len(parts) == 2 and parts[1] == path:
                return parts[0]
    return None


def design(root, design_rec=None):
    """p0 as an exact polynomial in z, from the sealed pilot record (or a given design dict, for the devtests)."""
    if design_rec is None:
        path = os.path.join(root, PILOT_RECORD)
        with open(path, "rb") as fh:
            raw = fh.read()
        h = hashlib.sha256(raw).hexdigest()
        if h != sealed_hash(root, PILOT_RECORD):
            raise CertificateError(f"DESIGN: the pilot record's SHA-256 {h} is not the sealed one")
        design_rec = json.loads(raw)["design"]
    if design_rec is None or design_rec.get("a") != "-2/5" or design_rec.get("b_pole") != "1/2":
        raise CertificateError(f"DESIGN: not the registered family: {design_rec}")
    cs = [Fraction.from_float(float.fromhex(v)) for v in design_rec["cheb"]]
    return sp.Poly(cheb_to_monomial(cs, 0, 1, z), z), int(design_rec["degree"])


def parts(U, H, p0, a):
    """The exact pieces: E (hd.scert.Exact), eps_n, eps_d, S, Pi and NL, as Polys in (z, mu)."""
    E = Exact(N_DIM, ELL, "none", UH=(U, H))
    p = param_n(N_DIM, ELL)
    en, ed = sp.fraction(sp.cancel(p["w"] / (3 * (1 + p["w"]))))
    if sp.Poly(ed, mu).eval(sp.Rational(1, 2)) < 0:
        en, ed = -en, -ed
    S = sp.Poly(ed * z + en, z, mu)
    Pi = sp.Poly(a * (ed + en) + p0.as_expr() * (ed * z + en), z, mu)
    Sz = sp.Poly(ed, z, mu)
    one_z = sp.Poly(1 - z, z, mu)
    br = (one_z * E.fzn * Pi * S + E.fn * (-Pi * S + one_z * (Pi.diff(z) * S - Sz * Pi) + Pi ** 2))
    NL = E.A0 * S ** 2 - E.HU * br
    return E, sp.expand(en), sp.expand(ed), S, Pi, NL


def chart_T(NL, divide=True):
    """NL(mu zeta, mu)/mu^2 as a dict {(i, j): c} in (zeta, mu)."""
    out = {}
    for (i, j), c in NL.terms():
        out[(i, i + j)] = out.get((i, i + j), 0) + c
    if not divide:
        return out, True
    ok = all(j >= 2 for (_, j) in out)
    return {(i, j - 2): c for (i, j), c in out.items()}, ok


def chart_C(NL):
    """NL(z, z sigma)/z^2 as a dict {(i, j): c} in (z, sigma)."""
    out = {}
    for (i, j), c in NL.terms():
        out[(i + j, j)] = out.get((i + j, j), 0) + c
    ok = all(i >= 2 for (i, _) in out)
    return {(i - 2, j): c for (i, j), c in out.items()}, ok


def P2(terms):
    return Poly2({k: Q(c) for k, c in terms.items() if c != 0})


def g_res():
    """N(0) at q = 1 for P = a/z + b0 + b1 z equals 576 H(2)^2 (l(l-3)/9 - a(a+1)), identically in l, a, b0, b1."""
    ell, a, b0, b1 = sp.symbols("ell a b0 b1")
    mm, dl = (ell - 1) * (ell + 4), 1 / (5 * (ell + 4))
    y = (1 - z) ** 3
    U = U_TARGET.subs({m: mm, d: dl, x: 2 * y})
    H = H_TARGET.subs({m: mm, d: dl, x: 2 * y})
    f = (1 - y) ** 2
    P = a / z + b0 + b1 * z
    N = U - 64 * H ** 2 * ((1 - z) * sp.diff(f, z) * P + f * (-P + (1 - z) * sp.diff(P, z) + P ** 2))
    num, den = sp.fraction(sp.cancel(sp.together(N)))
    poly_in_z = not den.has(z)
    H2 = sp.factor(H_TARGET.subs({m: mm, d: dl, x: 2}))
    diff = sp.cancel(num.subs(z, 0) / den - 576 * H2 ** 2 * (ell * (ell - 3) / sp.Integer(9) - a * (a + 1)))
    return poly_in_z and diff == 0, f"N polynomial in z: {poly_in_z}; H(2) = {H2}; N(0) - 576 H(2)^2 (c - a(a+1)) = {diff}"


def nc_bound(E, S, Pi, verify, stats):
    """(a) the trial function b on [ZA, ZB] has certified negative energy on W - K b at q = 1; (b) NL refused there."""
    sub = {mu: 0}
    num = {k: sp.Poly(getattr(E, k).as_expr().subs(sub), z) for k in ("Un", "Hn", "fn")}
    den = {k: getattr(E, k).as_expr().subs(sub) for k in ("Ud", "Hd", "fd")}
    bexpr = (z - ZA) ** 2 * (ZB - z) ** 2
    fq = num["fn"].as_expr() / den["fd"]
    Wq = (num["Un"].as_expr() / den["Ud"]) / (64 * (num["Hn"].as_expr() / den["Hd"]) ** 2)
    I1f = sum(float((fq * sp.diff(bexpr, z) ** 2 * (1 - z) ** 2 + Wq * bexpr ** 2).subs(z, ZA + (ZB - ZA) * (k + sp.Rational(1, 2)) / 400))
              for k in range(400)) * float(ZB - ZA) / 400
    I2f = sum(float((bexpr ** 3).subs(z, ZA + (ZB - ZA) * (k + sp.Rational(1, 2)) / 400)) for k in range(400)) * float(ZB - ZA) / 400
    K = sp.Integer(math.ceil(2 * I1f / I2f)) if I1f > 0 else sp.Integer(1)
    ctx.prec = 128
    polys = {"q1": sp.expand(fq * den["fd"] * sp.diff(bexpr, z) ** 2 * (1 - z) ** 2), "fd": den["fd"],
             "U": num["Un"].as_expr(), "H": num["Hn"].as_expr(), "phi2": sp.expand(bexpr ** 2),
             "bphi2": sp.expand(K * bexpr * bexpr ** 2)}
    cf = {k: [acb(Q(c)) for c in sp.Poly(sp.expand(e_), z).all_coeffs()[::-1]] for k, e_ in polys.items()}
    Ud, Hd, fd = (acb(Q(sp.Rational(den[k]))) for k in ("Ud", "Hd", "fd"))

    def horner(cs, t):
        acc = acb(0)
        for c in reversed(cs):
            acc = acc * t + c
        return acc

    def integrand(t, analytic):
        Hv = horner(cf["H"], t) / Hd
        return (horner(cf["q1"], t) / fd + horner(cf["U"], t) / Ud / (64 * Hv * Hv) * horner(cf["phi2"], t)
                - horner(cf["bphi2"], t))

    Qv = acb.integral(integrand, acb(Q(ZA)), acb(Q(ZB)))
    certified = bool(Qv.real < 0)
    rejected, msg = False, ""
    try:
        extra = sp.Poly(K * bexpr, z, mu) * E.HU * E.fd * S ** 2
        nl = sp.Poly((parts_cache["NL"] - extra).as_expr().subs(mu, 0), z, mu)
        verify(P2(dict(nl.terms())), (Q(ZA), Q(ZB), fmpq(0), fmpq(0)), 1, MAX_DEPTH, stats, "nc-bound on the bump")
    except CertificateError as exc:
        rejected, msg = True, str(exc)[:300]
    return certified, rejected, {"K": str(K), "I1_float": I1f, "Q_b": Qv.real.str(10), "message": msg}


parts_cache = {}


def run(root, control, UH=None, design_rec=None):
    verify = tampered_prove_sign if control == "td-verifier" else prove_sign
    checks, rec, timing = {}, {"control": control}, {}
    ok, res = kats(verify)
    checks["KAT"] = (ok, str(res))
    U0, H0 = UH if UH is not None else (U_TARGET, H_TARGET)
    U = U0 + (x ** 2 * m * (1 + m * d) if control == "td-coeff" else 0)
    if UH is None:
        e0u, e0h = sp.expand(U_minus(4) - U), sp.expand(H_minus(4) - H0)
        checks["E0"] = (e0u == 0 and e0h == 0, f"S5 (5.63b), (5.62b) at n = 4 minus TARGET.md's U_-, H_-: {e0u}, {e0h}")
    checks["H"] = (all(c > 0 for _, c in sp.Poly(H0, x, d, m).terms()), "every coefficient of H_- > 0")
    if control == "nc-a2":
        U = U - 2 * H0 ** 2 * x ** 4
    if control == "nc-zm":
        U = U - H0 ** 2 * x ** 4
    a = {"nc-zm": sp.Rational(-1, 2), "nc-res": sp.Rational(-7, 10)}.get(control, A_RES)
    p = param_n(N_DIM, ELL)
    wn, wd = sp.fraction(sp.cancel(sp.diff(p["w"], mu)))
    wsign = [sp.Poly(e, mu).eval(sp.Rational(1, 2)) > 0 for e in (wn, wd)]
    try:
        for e, sg, lab in ((wn, wsign[0], "w' numerator"), (wd, wsign[1], "w' denominator")):
            pm = Poly2({(0, j): Q(c) for (j,), c in sp.Poly((1 if sg else -1) * e, mu).terms()})
            verify(pm, (fmpq(0), fmpq(1), fmpq(0), fmpq(1)), 1, 30, {}, lab)
        winc = wsign[0] == wsign[1]
    except CertificateError:
        winc = False
    q2_1 = sp.cancel(p["q2"].subs(mu, MU1))
    pid = [sp.cancel(p["s"] ** 2 - (1 + 4 * p["m"] * p["q2"] / 25)) == 0, sp.cancel(p["q2"].subs(mu, 0) - 1) == 0,
           q2_1 <= sp.Rational(99, 100) ** 2, winc]
    checks["PARAM"] = (all(pid), f"s^2 = 1 + 4 m q^2/25, q(0) = 1, q(1/8)^2 = {q2_1} <= (99/100)^2, "
                                 f"w increasing on [0, 1]: {pid}")
    t0 = time.time()
    p0, deg = design(root, design_rec)
    rec["design"] = {"degree": deg, "a": str(a), "p0": {str(k): str(v) for k, v in p0.as_dict().items()}}
    checks["DESIGN"] = (True, (f"pilot record sealed; degree {deg}" if design_rec is None
                               else f"a given design (development tests); degree {deg}"))
    checks["G-RES"] = g_res() if UH is None else (True, "not run on synthetic inputs")
    sig1 = sp.Rational(1, 16) if control == "td-cover" else SIG1
    cov = [ZT * sig1 >= 1, ZT * MUT <= Z1, Z1 * sig1 <= MU1, 0 < MUT < MU1, 0 < Z1 < 1]
    checks["COVER"] = (all(cov), f"ZT SIG1 >= 1, ZT MUT <= Z1, Z1 SIG1 <= MU1, 0 < MUT < MU1, 0 < Z1 < 1: {cov}")
    E, en, ed, S, Pi, NL = parts(U, H0, p0, a)
    parts_cache["NL"] = NL
    timing["build_s"] = round(time.time() - t0, 1)
    rec["eps"] = {"num": str(en), "den": str(ed)}
    stats, minrec = {}, {}

    def pos_mu(expr, label):
        pm = Poly2({(0, j): Q(c) for (j,), c in sp.Poly(expr, mu).terms()})
        verify(pm, (fmpq(0), fmpq(1), fmpq(0), Q(MU1)), 1, 30, stats, label, minrec)
    try:
        pos_mu(sp.Poly(E.L.as_expr(), z, mu).as_expr(), "L")
        checks["L"] = (True, "L = Ud Hd^2 fd > 0 on [0, 1/8]")
    except CertificateError as exc:
        checks["L"] = (False, str(exc)[:300])
    en_ok = sp.Poly(en, mu).as_expr().subs(mu, 0) == 0 and all(c > 0 for c in sp.Poly(sp.cancel(en / mu), mu).coeffs())
    try:
        pos_mu(ed, "eps_d")
        checks["S"] = (en_ok, f"eps_n = {en} >= 0 (zero only at mu = 0), eps_d > 0 on [0, 1/8]; so S > 0 for z > 0")
    except CertificateError as exc:
        checks["S"] = (False, str(exc)[:300])
    T, tdiv = chart_T(NL, divide=control != "td-chart")
    C, cdiv = chart_C(NL)
    checks["DIV-T"] = (tdiv, "NL(mu zeta, mu) divisible by mu^2")
    checks["DIV-C"] = (cdiv, "NL(z, z sigma) divisible by z^2")
    Tp = sp.Poly(sum(c * sp.Symbol("zeta") ** i * mu ** j for (i, j), c in T.items()), sp.Symbol("zeta"), mu)
    T0 = sp.Poly(Tp.as_expr().subs(mu, 0), sp.Symbol("zeta"))
    zt = sp.Symbol("zeta")
    L0 = sp.Poly(E.L.as_expr(), z, mu).as_expr().subs({mu: 0, z: 0})
    c_ = sp.Rational(-2, 9)
    pencil = 576 * 30 ** 2 * L0 * ((c_ - a - a ** 2) * (18 * zt + 7) ** 2 + 49 * (a ** 2 - a))
    rec["THROAT"] = {"T(zeta, 0) - pencil limit": str(sp.expand(T0.as_expr() - pencil)) if UH is None else "not run",
                     "information": "T(zeta, 0) = 576 H(2)^2 L(0) [(c - a - a^2)(18 zeta + 7)^2 + 49 (a^2 - a)] at l = 2"}
    for label, terms, box in (("POS-O", dict(NL.terms()), (Q(Z1), fmpq(1), fmpq(0), Q(MU1))),
                              ("POS-O'", dict(NL.terms()), (fmpq(0), Q(Z1), Q(MUT), Q(MU1))),
                              ("POS-T", T, (fmpq(0), Q(ZT), fmpq(0), Q(MUT))),
                              ("POS-C", C, (fmpq(0), Q(Z1), fmpq(0), Q(sig1)))):
        t1 = time.time()
        try:
            verify(P2(terms), box, 1, MAX_DEPTH, stats, label, minrec)
            checks[label] = (True, f"> 0 on {[str(v) for v in box]}; least Bernstein coefficient {minrec[label]}")
        except CertificateError as exc:
            checks[label] = (False, str(exc)[:400])
        timing[label] = round(time.time() - t1, 1)
    if control == "nc-bound":
        certified, rejected, info = nc_bound(E, S, Pi, verify, stats)
        rec["nc-bound"] = info
        checks["nc-bound (a)"] = (certified, f"Q[b] certified < 0: {certified}; {info}")
        checks["nc-bound (b)"] = (not rejected, f"the certificate on the planted potential: rejected {rejected}")
    rec["degrees"] = {"NL": [NL.degree(z), NL.degree(mu)], "T": [max(i for i, _ in T), max(j for _, j in T)],
                      "C": [max(i for i, _ in C), max(j for _, j in C)]}
    rec["bernstein_leaves"] = stats
    rec["min_bernstein"] = {k: str(v) for k, v in minrec.items()}
    return checks, rec, timing


def main(argv=None, UH=None, design_rec=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--control", choices=CONTROLS, default="none")
    ap.add_argument("--root", default=os.path.join(os.path.dirname(__file__), "..", ".."))
    a = ap.parse_args(argv)
    t0, start = time.time(), datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    record = {"claim": "results/a2/s/PREREG.md (A2-S: l = 2, q in [q(1/8), 1])", "control": a.control,
              "provenance": provenance(), "archive_sha256": os.environ.get("BHM_ARCHIVE", "unknown")}
    timing = {}
    try:
        checks, rec, timing = run(a.root, a.control, UH, design_rec)
        record.update(rec)
        record["checks"] = {k: {"ok": bool(ok), "detail": det} for k, (ok, det) in checks.items()}
        failed = [k for k, (ok, _) in checks.items() if not ok]
        verdict = "VERIFIED" if not failed else "REJECT: " + ", ".join(failed)
    except Exception as exc:  # noqa: BLE001  (fail-closed)
        verdict = f"REJECT: exception {type(exc).__name__}: {exc}"
    record["verdict"] = verdict
    record["timing"] = {**timing, "utc_start": start, "t_total_s": round(time.time() - t0, 1)}
    try:
        os.makedirs(a.out, exist_ok=True)
        dump_json(plain(record), f"{a.out}/result.json")
    except Exception as exc:  # noqa: BLE001
        verdict = record["verdict"] = f"REJECT: record not written: {type(exc).__name__}: {exc}"
    for k, v in record.get("checks", {}).items():
        print(f"{k}: {'PASS' if v['ok'] else 'FAIL'}  {v['detail'][:300]}")
    print(verdict)
    return 0 if verdict == "VERIFIED" else 1


if __name__ == "__main__":
    sys.exit(main())
