"""Stage 3, HD-X-S: the singular S-certificate of HD-X-1 for one band of D = 7..11 through extremality (2l > n - 1).

    python -m hdx.scert --out DIR --band D,L [--control NAME] [--root REPO]

A2-S (code/a2/scert.py; BHM-100, BHM-101, BHM-104) at general n.  One band (n, l) of hdx.bands, D = n + 2, for q in
[q(MU1), 1] with q(MU1)^2 <= (99/100)^2 (checked exactly), in units r_H = 1, z = 1 - 1/rho and TARGET_HD.md's mu
(q = 1 at mu = 0).  The design is HD-X-PILOT's sealed record for the band:
    P = a (1 + eps)/(z + eps) + p0(z),   a of hdx.bands,   eps = w/((n - 1)(1 + w)) = eps_n/eps_d,
p0 the recorded Chebyshev series, converted exactly to monomials.  With S = eps_d z + eps_n and Pi = a (eps_d + eps_n)
+ p0 S, P = Pi/S, and
    NL := N S^2 L = Un Hd^2 fd S^2 - 64 Hn^2 Ud [(1 - z) fzn Pi S + fn (-Pi S + (1 - z)(Pi_z S - eps_d Pi) + Pi^2)],
a polynomial in (z, mu), with L = Ud Hd^2 fd > 0 (hd.scert's exact parts at n).  NL vanishes at the corner (0, 0), so
[0, 1] x [0, MU1] is covered by A2-S's four charts, with hdx.bands' constants:
    O   (z, mu) in [Z1, 1] x [0, MU1]            NL > 0
    O'  (z, mu) in [0, Z1] x [MUT, MU1]          NL > 0
    T   z = mu zeta, (zeta, mu) in [0, ZT] x [0, MUT]      T = NL(mu zeta, mu)/mu^2 > 0
    C   mu = z sigma, (z, sigma) in [0, Z1] x [0, SIG1]    C = NL(z, z sigma)/z^2 > 0
with the exact divisions checked (DIV-T, DIV-C) and the coverage ZT SIG1 >= 1, ZT MUT <= Z1, Z1 SIG1 <= MU1 (COVER).
For every (z, mu) in (0, 1) x [0, MU1] some chart gives NL > 0, and S > 0, L > 0 there, so N > 0, and A_{l,q} >= 0 by
Proposition 3 for P C^1 on (0, 1) (Lean prop3_Ioo / prop3_Dn, every n >= 2).
Gates: KAT, E0n (S5's U_-, H_- against Kimi's transcription, n = 2..12), H, PARAM, DESIGN (the pilot record's seal; the
band's registered a and B_POLE), G-RES (at q = 1, N(0) = 64 (n - 1)^2 H(2)^2 (c - a(a + 1)) for P = a/z + b0 + b1 z,
c = l(l - n + 1)/(n - 1)^2, symbolic in l, a, b0, b1), COVER, L, S, DIV-T, DIV-C and the four charts.  THROAT
(information): T(zeta, 0) against 64 (n - 1)^2 H(2)^2 L(0) [(c - a - a^2)(eps_d(0) zeta + eps_n'(0))^2
+ (a^2 - a) eps_n'(0)^2].
--band 6,2 is the gate band (4, 2): A2-S's design (A2-PILOT's sealed record) and constants.  Its main record must equal
A2-S's (BHM-101) in every field A2-S's certificate determines (hdx.gate; kit/hdx/run_s.sh --gate).
Fail-closed: VERIFIED and exit 0 only if every check holds.
--control (each with its registered verdict; the parameters are hdx.bands.control_params):
    nc-a2       U - k_a2 H^2 x^4: the extremal throat coefficient becomes c' = -1/4 - 1/(4(n - 1)^2), so N(0) < 0 at
                q = 1 for every a (design-free)
    nc-res      the residue a_nc, outside the window (a_ot, a_pr)
    nc-well     a planted bound state at q = 1 on WELL's support, inside U_- < 0: (a) its trial function has certified
                negative energy (Arb), (b) the certificate on the planted potential is refused on the support
    d0          U - k_d0 H^2 x^4: c' = a(a + 1) exactly, the sharp zero margin at the blown-up corner
    d6          NL - K mu (z - mu)(3 mu - z), K = (4/MUT) T(2, MUT/2): a planted defect that vanishes at mu = 0
    td-coeff    U_- + 16 n m^2 (hd.elementary.U_of): E0n must fail
    td-verifier the verifier's acceptance threshold lowered to -1: the KATs must fail
    td-chart    the throat chart without the division by mu^2
    td-cover    SIG1 halved, so ZT SIG1 < 1
    td-H        the H gate on H_- - n(n + 1) x           td-param    PARAM on param_n's td-param (B = 2l + n)
    td-design   DESIGN against a changed hash            td-gres     G-RES's comparison on U_- + x^4
    td-L        the L gate on -L                         td-S        eps_n -> -eps_n: the pole inside the exterior
    td-divT     the throat chart divided by mu^3         td-divC     the corner chart divided by z^3
"""
import argparse
import datetime
import hashlib
import json
import math
import os
import re
import sys
import time
from fractions import Fraction

import sympy as sp
from flint import acb, ctx, fmpq

from a1.p1 import kats, plain, tampered_prove_sign
from a2.scert import P2, chart_C, chart_T, sealed_hash
from hd.elementary import U_of, gate_E0n, param_n
from hd.scert import Exact, z
from hdx.bands import B_POLE, BANDS, GATE, MU1, MUT, SIG1, WELL, Z1, ZT, control_params, label, residues
from ki.potentials import H_minus, U_minus, d, m, x
from onset.bernstein import Poly2, Q, prove_sign
from onset.onset import mu
from p3.scert import cheb_to_monomial
from qnm1c.common import CertificateError, dump_json, provenance

CONTROLS = ("none", "nc-a2", "nc-res", "nc-well", "d0", "d6", "td-coeff", "td-verifier", "td-chart", "td-cover",
            "td-H", "td-param", "td-design", "td-gres", "td-L", "td-S", "td-divT", "td-divC")
PILOT_RECORD = "results/hdx/pilot/runs/record/main/result.json"
A2_PILOT_RECORD = "results/a2/pilot/runs/record/main/result.json"
MAX_DEPTH = 40


def R(fr):
    fr = Fraction(fr)
    return sp.Rational(fr.numerator, fr.denominator)


def design(root, n, ell, design_rec=None, tamper=False):
    """p0 as an exact polynomial in z, from the sealed pilot record (A2-PILOT's for the gate band), or from a given
    design dict (development tests).  tamper (td-design): the record is compared with a sealed hash whose first digit
    is changed."""
    a_reg = residues(n, ell)[3]
    if design_rec is None:
        path = A2_PILOT_RECORD if (n, ell) == GATE else PILOT_RECORD
        try:
            with open(os.path.join(root, path), "rb") as fh:
                raw = fh.read()
        except OSError as exc:
            raise CertificateError(f"DESIGN: the pilot record {path} cannot be read: {exc}") from exc
        h = hashlib.sha256(raw).hexdigest()
        want = sealed_hash(root, path)
        if tamper and want:
            want = ("1" if want[0] != "1" else "2") + want[1:]
        if h != want:
            raise CertificateError(f"DESIGN: the pilot record's SHA-256 {h} is not the sealed one")
        rec = json.loads(raw)
        design_rec = rec["design"] if (n, ell) == GATE else rec.get("designs", {}).get(label(n, ell))
    if (design_rec is None or design_rec.get("a") != str(a_reg) or design_rec.get("b_pole") != str(B_POLE)
            or ((n, ell) != GATE and design_rec.get("mu1") != str(MU1))):
        raise CertificateError(f"DESIGN: not the registered family for D = {n + 2}, l = {ell}: {design_rec}")
    cs = [Fraction.from_float(float.fromhex(v)) for v in design_rec["cheb"]]
    return sp.Poly(cheb_to_monomial(cs, 0, 1, z), z), int(design_rec["degree"])


def parts(n, ell, UH, p0, a, flip=False):
    """The exact pieces: E (hd.scert.Exact), eps_n, eps_d, S, Pi and NL, as Polys in (z, mu).
    flip (td-S): eps_n -> -eps_n, which moves the pole to z = +eps, inside the exterior."""
    E = Exact(n, ell, "none", UH=UH)
    p = param_n(n, ell)
    en, ed = sp.fraction(sp.cancel(p["w"] / ((n - 1) * (1 + p["w"]))))
    if sp.Poly(ed, mu).eval(sp.Rational(1, 2)) < 0:
        en, ed = -en, -ed
    if flip:
        en = -en
    S = sp.Poly(ed * z + en, z, mu)
    Pi = sp.Poly(a * (ed + en) + p0.as_expr() * (ed * z + en), z, mu)
    Sz = sp.Poly(ed, z, mu)
    one_z = sp.Poly(1 - z, z, mu)
    br = (one_z * E.fzn * Pi * S + E.fn * (-Pi * S + one_z * (Pi.diff(z) * S - Sz * Pi) + Pi ** 2))
    NL = E.A0 * S ** 2 - E.HU * br
    return E, sp.expand(en), sp.expand(ed), S, Pi, NL


def g_res(n, extra=0):
    """At q = 1, N(0) for P = a/z + b0 + b1 z equals 64 (n - 1)^2 H(2)^2 (c - a(a + 1)), c = l(l - n + 1)/(n - 1)^2,
    identically in l, a, b0, b1, and N is a polynomial in z.  extra (td-gres): the comparison is run on U_- + extra."""
    ell, a, b0, b1 = sp.symbols("ell a b0 b1")
    mm, dl = (ell - 1) * (ell + n), 1 / ((ell + n) * sp.Integer(n + 1))
    y = (1 - z) ** (n - 1)
    U = (U_minus(n) + extra).subs({m: mm, d: dl, x: 2 * y})
    H = H_minus(n).subs({m: mm, d: dl, x: 2 * y})
    f = (1 - y) ** 2
    P = a / z + b0 + b1 * z
    N = U - 64 * H ** 2 * ((1 - z) * sp.diff(f, z) * P + f * (-P + (1 - z) * sp.diff(P, z) + P ** 2))
    num, den = sp.fraction(sp.cancel(sp.together(N)))
    poly_in_z = not den.has(z)
    H2 = sp.factor(H_minus(n).subs({m: mm, d: dl, x: 2}))
    c = ell * (ell - n + 1) / sp.Integer((n - 1) ** 2)
    diff = sp.cancel(num.subs(z, 0) / den - 64 * (n - 1) ** 2 * H2 ** 2 * (c - a * (a + 1)))
    return (poly_in_z and diff == 0,
            f"N polynomial in z: {poly_in_z}; H(2) = {H2}; N(0) - 64 (n-1)^2 H(2)^2 (c - a(a+1)) = {diff} (n = {n})")


def nc_well(n, ell, E, S, verify, stats, NL):
    """(a) the trial function b on WELL's support has certified negative energy on W - K b at q = 1; (b) NL of the
    planted potential, at q = 1, is refused on the support."""
    za, zb = (R(t) for t in WELL[(n, ell)])
    sub = {mu: 0}
    num = {k: sp.Poly(getattr(E, k).as_expr().subs(sub), z) for k in ("Un", "Hn", "fn")}
    den = {k: getattr(E, k).as_expr().subs(sub) for k in ("Ud", "Hd", "fd")}
    bexpr = (z - za) ** 2 * (zb - z) ** 2
    fq = num["fn"].as_expr() / den["fd"]
    Wq = (num["Un"].as_expr() / den["Ud"]) / (64 * (num["Hn"].as_expr() / den["Hd"]) ** 2)
    fqf, Wqf, bf, bzf = (sp.lambdify(z, e_, "math") for e_ in (fq, Wq, bexpr, sp.diff(bexpr, z)))
    nq, h = 2000, float(zb - za) / 2000
    I1f = I2f = 0.0
    for k in range(nq):
        t = float(za) + (k + 0.5) * h
        I1f += (fqf(t) * bzf(t) ** 2 * (1 - t) ** 2 + Wqf(t) * bf(t) ** 2) * h
        I2f += bf(t) ** 3 * h
    K = sp.Integer(math.ceil(2 * I1f / I2f)) if I1f > 0 else sp.Integer(1)
    ctx.prec = 256
    polys = {"q1": sp.expand(fq * den["fd"] * sp.diff(bexpr, z) ** 2 * (1 - z) ** 2), "U": num["Un"].as_expr(),
             "H": num["Hn"].as_expr(), "phi2": sp.expand(bexpr ** 2), "bphi2": sp.expand(K * bexpr * bexpr ** 2)}
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

    Qv = acb.integral(integrand, acb(Q(za)), acb(Q(zb)))
    certified = bool(Qv.real < 0)
    rejected, msg = False, ""
    try:
        extra = sp.Poly(K * bexpr, z, mu) * E.HU * E.fd * S ** 2
        nl = sp.Poly((NL - extra).as_expr().subs(mu, 0), z, mu)
        verify(P2(dict(nl.terms())), (Q(za), Q(zb), fmpq(0), fmpq(0)), 1, MAX_DEPTH, stats, "nc-well on the support")
    except CertificateError as exc:
        rejected, msg = True, str(exc)[:300]
    return certified, rejected, {"support": [str(za), str(zb)], "K": str(K), "I1_float": I1f, "Q_b": Qv.real.str(10),
                                 "message": msg}


def run(root, n, ell, control, UH=None, design_rec=None):
    verify = tampered_prove_sign if control == "td-verifier" else prove_sign
    checks, rec, timing = {}, {"control": control, "n": n, "D": n + 2, "ell": ell}, {}
    c_ex, apr, aot, a_reg, beta0 = residues(n, ell)
    ctl = control_params(n, ell)
    ok, res = kats(verify)
    checks["KAT"] = (ok, str(res))
    U0, H0 = UH if UH is not None else (U_of(n, "td-coeff" if control == "td-coeff" else "none"), H_minus(n))
    if UH is None:
        checks["E0n"] = gate_E0n(root, control)
    Hg = H0 - n * (n + 1) * x if control == "td-H" else H0       # td-H: the H gate with its x-coefficient negative
    checks["H"] = (all(c > 0 for _, c in sp.Poly(Hg, x, d, m).terms()), "every coefficient of H_- > 0")
    U = U0
    if control == "nc-a2":
        U = U - R(ctl["k_a2"]) * H0 ** 2 * x ** 4
    if control == "d0":
        U = U - R(ctl["k_d0"]) * H0 ** 2 * x ** 4
    a = R(ctl["a_nc"]) if control == "nc-res" else R(a_reg)
    p = param_n(n, ell, "td-param" if control == "td-param" else "none")
    wn, wd = sp.fraction(sp.cancel(sp.diff(p["w"], mu)))
    wsign = [sp.Poly(e, mu).eval(sp.Rational(1, 2)) > 0 for e in (wn, wd)]
    try:
        for e, sg, lab in ((wn, wsign[0], "w' numerator"), (wd, wsign[1], "w' denominator")):
            pm = Poly2({(0, j): Q(c) for (j,), c in sp.Poly((1 if sg else -1) * e, mu).terms()})
            verify(pm, (fmpq(0), fmpq(1), fmpq(0), fmpq(1)), 1, 30, {}, lab)
        winc = wsign[0] == wsign[1]
    except CertificateError:
        winc = False
    mu1 = R(MU1)
    q2_1 = sp.cancel(p["q2"].subs(mu, mu1))
    pid = [sp.cancel(p["s"] ** 2 - (1 + 4 * p["m"] * p["q2"] / (n + 1) ** 2)) == 0,
           sp.cancel(p["q2"].subs(mu, 0) - 1) == 0, q2_1 <= sp.Rational(99, 100) ** 2, winc]
    checks["PARAM"] = (all(pid), f"s^2 = 1 + 4 m q^2/{(n + 1) ** 2}, q(0) = 1, q({mu1})^2 = {q2_1} <= (99/100)^2, "
                                 f"w increasing on [0, 1]: {pid}")
    t0 = time.time()
    try:
        p0, deg = design(root, n, ell, design_rec, tamper=control == "td-design")
    except CertificateError as exc:                                # DESIGN fails under its own label
        checks["DESIGN"] = (False, str(exc)[:300])
        return checks, rec, timing
    rec["design"] = {"degree": deg, "a": str(a), "p0": {str(k): str(v) for k, v in p0.as_dict().items()}}
    checks["DESIGN"] = (True, (f"pilot record sealed; degree {deg}" if design_rec is None
                               else f"a given design (development tests); degree {deg}"))
    checks["G-RES"] = (g_res(n, x ** 4 if control == "td-gres" else 0) if UH is None
                       else (True, "not run on synthetic inputs"))
    sig1 = R(SIG1) / 2 if control == "td-cover" else R(SIG1)
    z1, zt, mut = R(Z1), R(ZT), R(MUT)
    cov = [zt * sig1 >= 1, zt * mut <= z1, z1 * sig1 <= mu1, 0 < mut < mu1, 0 < z1 < 1]
    checks["COVER"] = (all(cov), f"ZT SIG1 >= 1, ZT MUT <= Z1, Z1 SIG1 <= MU1, 0 < MUT < MU1, 0 < Z1 < 1: {cov}")
    E, en, ed, S, Pi, NL = parts(n, ell, (U, H0), p0, a, flip=control == "td-S")
    if control == "d6":                    # a planted throat defect that vanishes at mu = 0 (BHM-104's D6)
        T2, _ = chart_T(NL)
        Kd6 = 4 / mut * sum(c * sp.Integer(2) ** i * (mut / 2) ** j for (i, j), c in T2.items())
        rec["d6"] = {"K": str(Kd6), "defect": "K mu (z - mu)(3 mu - z)"}
        NL = NL - sp.Poly(Kd6 * mu * (z - mu) * (3 * mu - z), z, mu)
    timing["build_s"] = round(time.time() - t0, 1)
    rec["eps"] = {"num": str(en), "den": str(ed)}
    stats, minrec = {}, {}

    def pos_mu(expr, label_):
        pm = Poly2({(0, j): Q(c) for (j,), c in sp.Poly(expr, mu).terms()})
        verify(pm, (fmpq(0), fmpq(1), fmpq(0), Q(mu1)), 1, 30, stats, label_, minrec)
    try:
        pos_mu((-1 if control == "td-L" else 1) * sp.Poly(E.L.as_expr(), z, mu).as_expr(), "L")
        checks["L"] = (True, f"L = Ud Hd^2 fd > 0 on [0, {mu1}]")
    except CertificateError as exc:
        checks["L"] = (False, str(exc)[:300])
    en_ok = sp.Poly(en, mu).as_expr().subs(mu, 0) == 0 and all(c > 0 for c in sp.Poly(sp.cancel(en / mu), mu).coeffs())
    try:
        pos_mu(ed, "eps_d")
        checks["S"] = (en_ok, f"eps_n = {en} >= 0 (zero only at mu = 0), eps_d > 0 on [0, {mu1}]; so S > 0 for z > 0")
    except CertificateError as exc:
        checks["S"] = (False, str(exc)[:300])
    T, tdiv = chart_T(NL, divide=control != "td-chart", k=3 if control == "td-divT" else 2)
    C, cdiv = chart_C(NL, k=3 if control == "td-divC" else 2)
    checks["DIV-T"] = (tdiv, "NL(mu zeta, mu) divisible by mu^" + ("3 (td-divT)" if control == "td-divT" else "2"))
    checks["DIV-C"] = (cdiv, "NL(z, z sigma) divisible by z^" + ("3 (td-divC)" if control == "td-divC" else "2"))
    if T is not None and UH is None:
        zv = sp.Symbol("zeta")
        Tp = sp.Poly(sum(c * zv ** i * mu ** j for (i, j), c in T.items()), zv, mu)
        T0 = sp.Poly(Tp.as_expr().subs(mu, 0), zv)
        L0 = sp.Poly(E.L.as_expr(), z, mu).as_expr().subs({mu: 0, z: 0})
        H2 = H_minus(n).subs({m: (ell - 1) * (ell + n), d: sp.Rational(1, (ell + n) * (n + 1)), x: 2})
        edo, enp = sp.Poly(ed, mu).as_expr().subs(mu, 0), sp.diff(en, mu).subs(mu, 0)
        cc = R(c_ex)
        pencil = 64 * (n - 1) ** 2 * H2 ** 2 * L0 * ((cc - a - a ** 2) * (edo * zv + enp) ** 2 + enp ** 2 * (a ** 2 - a))
        throat = str(sp.expand(T0.as_expr() - pencil))
    else:
        throat = "not run"
    rec["THROAT"] = {"T(zeta, 0) - pencil limit": throat,
                     "information": "T(zeta, 0) = 64 (n-1)^2 H(2)^2 L(0) [(c - a - a^2)(eps_d(0) zeta + eps_n'(0))^2 "
                                    "+ (a^2 - a) eps_n'(0)^2]"}
    for lab_, terms, box in (("POS-O", dict(NL.terms()), (Q(z1), fmpq(1), fmpq(0), Q(mu1))),
                             ("POS-O'", dict(NL.terms()), (fmpq(0), Q(z1), Q(mut), Q(mu1))),
                             ("POS-T", T, (fmpq(0), Q(zt), fmpq(0), Q(mut))),
                             ("POS-C", C, (fmpq(0), Q(z1), fmpq(0), Q(sig1)))):
        t1 = time.time()
        if terms is None:                                          # no chart after a failed division
            checks[lab_] = (False, "not run: the chart's division failed")
            continue
        try:
            verify(P2(terms), box, 1, MAX_DEPTH, stats, lab_, minrec)
            checks[lab_] = (True, f"> 0 on {[str(v) for v in box]}; least Bernstein coefficient {minrec[lab_]}")
        except CertificateError as exc:                            # the point first, before the long value
            msg = str(exc)
            mt = re.search(r"at \(t, mu\) = \(([^)]*)\)", msg)
            checks[lab_] = (False, ((f"at ({mt.group(1)}); " if mt else "") + msg)[:400])
        timing[lab_] = round(time.time() - t1, 1)
    if control == "nc-well":
        certified, rejected, info = nc_well(n, ell, E, S, verify, stats, NL)
        rec["nc-well"] = info
        checks["nc-well (a)"] = (certified, f"Q[b] certified < 0: {certified}; {info}")
        checks["nc-well (b)"] = (not rejected, f"the certificate on the planted potential: rejected {rejected}")
    rec["degrees"] = {"NL": [NL.degree(z), NL.degree(mu)],
                      "T": None if T is None else [max(i for i, _ in T), max(j for _, j in T)],
                      "C": None if C is None else [max(i for i, _ in C), max(j for _, j in C)]}
    rec["bernstein_leaves"] = stats
    rec["min_bernstein"] = {k: str(v) for k, v in minrec.items()}
    return checks, rec, timing


def parse_band(s):
    D, ell = (int(t) for t in s.split(","))
    nb = (D - 2, ell)
    if nb != GATE and nb not in BANDS:
        raise ValueError(f"D = {D}, l = {ell} is not a band of hdx.bands")
    return nb


def main(argv=None, UH=None, design_rec=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--band", required=True, help="D,l: a band of hdx.bands, or 6,2 (the gate band)")
    ap.add_argument("--control", choices=CONTROLS, default="none")
    ap.add_argument("--root", default=os.path.join(os.path.dirname(__file__), "..", ".."))
    a = ap.parse_args(argv)
    t0, start = time.time(), datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    record = {"claim": f"HD-X-S (HD-X-1's S-certificate), band D,l = {a.band}, q in [q({MU1}), 1]", "control": a.control,
              "provenance": provenance(), "archive_sha256": os.environ.get("BHM_ARCHIVE", "unknown")}
    timing = {}
    try:
        n, ell = parse_band(a.band)
        checks, rec, timing = run(a.root, n, ell, a.control, UH, design_rec)
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
