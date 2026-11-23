"""Stage 2, step 2, HD-S (results/hd/s/PREREG.md): S-certificates on the bands of D = 7..11.

    python -m hd.scert --out DIR --band D,L [--control NAME] [--root REPO]

One band (D, l) of TARGET_HD.md section 3, for q in [q_lo, q_max(D)] (TARGET_HD_ADDENDUM_1.md), in units r_H = 1 and
z = 1 - 1/rho (results/p3/METHOD.md):
  coverage  mu-boxes with exact rational ends partition [mu_a, mu_b]: q(mu_a)^2 >= q_max^2 and, for a band with an onset,
            q(mu_b)^2 <= q_lo^2 (mu_b = 1 for a band from 0+), checked exactly; w increases on [0, 1] (exact).
  design    (untrusted) per box: rule 2 with the band's eps, variable and degree (TARGET_HD_ADDENDUM_1.md), from
            hd.pilot's floats at the Chebyshev-Lobatto nodes in mu (degree DM) and in the variable: z on [0, 1], or
            zeta = z/(z + delta_b) on [0, 1/(1 + delta_b)] with delta_b a fixed rational per box.  The coefficients are
            the exact binary values of the floats.  Each box's planning record is written before its verification.
  verify    (the trust base) with P = Phat/s^e, s = z + delta_b and e = deg for a zeta-design (s = 1, e = 0 for z):
            NL := N L s^(2e) > 0 on [0, 1] x box and L = U_den H_den^2 f_den > 0 on the box, by exact Bernstein
            bisection (onset.bernstein.prove_sign).  N > 0 on [0, 1] proves A_{l,q} >= 0 for every q of the box
            (METHOD.md, Proposition 3).
  fallback  a box that does not verify is redesigned at the next two degrees of hd.pilot.DEGREES (capped at the last),
            then bisected in mu, at most BISECT times; the band is REJECT if a box fails after the last step.
Fail-closed: VERIFIED and exit 0 only if every check holds.
--control (each must REJECT):
    td-coeff     U_minus(n) plus 16 n m^2: E0n must fail
    td-verifier  the verifier's acceptance threshold lowered to -1: the KATs must fail
    td-horizon   the first box's certificate plus c (1 - z) s^e, c = W(0)/f_z(0) - P(0) + 1/10 at the box's lower end:
                 N < 0 at that corner
    nc-bound     a planted bound state at the first box's mid-point mu_c: W - K b on [3/10, 3/5], b = ((z - 3/10)(3/5 - z))^2,
                 K = 2 I1/I2: (a) the trial function b has certified negative energy (Arb), and (b) the first box's
                 certificate at mu_c is rejected on the planted potential
"""
import argparse
import json
import math
import os
import sys
import time
from fractions import Fraction

import sympy as sp
from flint import acb, ctx, fmpq

from a1.p1 import kats, plain, tampered_prove_sign
from hd.elementary import BANDS, U_of, gate_E0n, param_n
from hd.pilot import DEGREES, GRID, ZERO_BANDS, Setting, design_slack, design_value, riccati, slack, tabulate, Fit
from ki.potentials import H_minus, d, m, x
from onset.bernstein import Poly2, Q, prove_sign
from onset.onset import mu
from p3.scert import cheb_coeffs, cheb_to_monomial
from qnm1c.common import CertificateError, dump_json, provenance

z, v = sp.symbols("z v")
CONTROLS = ("none", "td-coeff", "td-verifier", "td-horizon", "nc-bound")
Q_MAX = {n: Fraction(99, 100) for n in range(5, 10)}            # TARGET_HD_ADDENDUM_1.md
# TARGET_HD_ADDENDUM_1.md: the pilot's design at q_max(D) for each band (n, l): (eps, variable, degree)
DESIGN = {(n, ell): (Fraction(1, 50), var, deg) for (n, ell), (var, deg) in {
    (5, 2): ("z", 20), (5, 3): ("z", 16), (6, 2): ("z", 24), (6, 3): ("z", 20), (6, 4): ("z", 20),
    (7, 2): ("z", 28), (7, 3): ("z", 24), (7, 4): ("z", 24), (7, 5): ("zeta", 20),
    (8, 2): ("z", 32), (8, 3): ("z", 28), (8, 4): ("z", 24), (8, 5): ("zeta", 24),
    (9, 2): ("z", 32), (9, 3): ("z", 32), (9, 4): ("z", 28), (9, 5): ("z", 28), (9, 6): ("zeta", 24)}.items()}
DM = 4
RATIO, GRAIN = Fraction(11, 10), 10000                          # mu_(i+1) = ceil(RATIO mu_i GRAIN)/GRAIN
BISECT = 3
MAX_DEPTH = 40
PILOT_RECORD = "results/hd/pilot/runs/record/main/result.json"
ZA, ZB = Fraction(3, 10), Fraction(3, 5)


def R(fr):
    fr = Fraction(fr)
    return sp.Rational(fr.numerator, fr.denominator)


# ---------------------------------------------------------------- the band
def band_data(n, ell):
    """q_lo (Fraction), its text, the kind."""
    if (n, ell) in BANDS:
        return Fraction(BANDS[(n, ell)][1]), BANDS[(n, ell)][1], "onset"
    if (n, ell) in ZERO_BANDS:
        return Fraction(0), "0", "from 0+"
    raise ValueError(f"(D, l) = ({n + 2}, {ell}) is not a band of TARGET_HD.md section 3")


def w_exact(n, ell, muv):
    B = 2 * ell + n - 1
    return Fraction(B) * muv / ((ell + n) + (ell - 1) * muv * muv)


def mu_float(n, ell, q):
    wv = math.sqrt(1 - q * q)
    if wv >= 1:
        return 1.0
    B = 2 * ell + n - 1
    return (B - math.sqrt(B * B - 4 * (ell - 1) * (ell + n) * wv * wv)) / (2 * (ell - 1) * wv)


def partition(n, ell, qmax, qlo):
    """The registered mu-boxes: mu_a = floor(mu(q_max) GRAIN)/GRAIN, mu_(i+1) = ceil(RATIO mu_i GRAIN)/GRAIN up to mu_b."""
    ma = Fraction(math.floor(mu_float(n, ell, float(qmax)) * GRAIN), GRAIN)
    mb = Fraction(1) if qlo == 0 else Fraction(math.ceil(mu_float(n, ell, float(qlo)) * GRAIN), GRAIN)
    edges = [ma]
    while edges[-1] < mb:
        edges.append(min(Fraction(math.ceil(RATIO * edges[-1] * GRAIN), GRAIN), mb))
    return list(zip(edges, edges[1:]))


def coverage(n, ell, boxes, qmax, qlo):
    ma, mb = boxes[0][0], boxes[-1][1]
    wa2, wb2 = w_exact(n, ell, ma) ** 2, w_exact(n, ell, mb) ** 2
    contiguous = all(a1 == b0 for (_, a1), (b0, _) in zip(boxes, boxes[1:])) and all(a < b for a, b in boxes)
    lo_ok = (mb == 1) if qlo == 0 else (1 - wb2 <= qlo * qlo)
    hi_ok = 1 - wa2 >= qmax * qmax and 0 < ma
    # w' = B((l + n) - (l - 1) mu^2)/A^2 and (l + n) - (l - 1) mu^2 >= n + 1 > 0 on [0, 1]: w increases
    winc = n + 1 > 0
    return (contiguous and lo_ok and hi_ok and winc,
            {"mu_a": str(ma), "mu_b": str(mb), "q(mu_a)^2": str(1 - wa2), "q(mu_b)^2": str(1 - wb2),
             "contiguous": contiguous, "q(mu_a) >= q_max": hi_ok, "q(mu_b) <= q_lo or mu_b = 1": lo_ok,
             "w increases on [0, 1]": winc})


def inward(q2_lo, q2_hi, digits=5):
    """Inward decimals of [sqrt(q2_lo), sqrt(q2_hi)]: the lower end rounded up, the upper end rounded down."""
    sc = 10 ** (2 * digits)

    def isqrt_floor(X):
        return math.isqrt(math.floor(X * sc))
    lo = isqrt_floor(q2_lo)
    if lo * lo < q2_lo * sc:
        lo += 1
    return f"{lo / 10 ** digits:.{digits}f}", f"{isqrt_floor(q2_hi) / 10 ** digits:.{digits}f}"


# ---------------------------------------------------------------- exact parts
def ratpoly(e):
    """A rational function of mu as (numerator, denominator) polynomials, the denominator > 0 at mu = 1/2."""
    num, den = sp.fraction(sp.cancel(sp.together(e)))
    if sp.Poly(den, mu).eval(sp.Rational(1, 2)) < 0:
        num, den = -num, -den
    return sp.expand(num), sp.expand(den)


def exact_parts(n, ell, control, UH=None):
    """U = Un/Ud, H = Hn/Hd, f = fn/fd, f_z = fzn/fd; Un, Hn, fn, fzn in Q[z, mu], Ud, Hd, fd in Q[mu] (as Polys in z, mu).
    UH: synthetic (U, H) in (x, m, delta), for the development tests."""
    p = param_n(n, ell)
    y = (1 - z) ** (n - 1)
    sub = {m: p["m"], d: p["delta"]}
    out = {}
    for key, expr in zip(("U", "H"), UH or (U_of(n, control), H_minus(n))):
        cs = {k: sp.cancel(sp.together(c.subs(sub) * p["xH"] ** k)) for (k,), c in sp.Poly(expr, x).terms()}
        den = sp.expand(sp.lcm_list([sp.fraction(c)[1] for c in cs.values()]))
        if sp.Poly(den, mu).eval(sp.Rational(1, 2)) < 0:
            den = -den
        num = sum(sp.cancel(c * den) * y ** k for k, c in cs.items())
        out[key] = (sp.Poly(sp.expand(num), z, mu), sp.Poly(den, z, mu))
    kn, kd = ratpoly((1 - p["w"]) / (1 + p["w"]))                  # k = x_H/x_- = (1 - w)/(1 + w)
    fn = sp.Poly(sp.expand((1 - y) * (kd - kn * y)), z, mu)
    out["f"] = (fn, sp.Poly(fn.as_expr().diff(z), z, mu), sp.Poly(kd, z, mu))
    return out


class Exact:
    def __init__(self, n, ell, control, UH=None):
        self.n, self.ell = n, ell
        pp = exact_parts(n, ell, control, UH)
        (self.Un, self.Ud), (self.Hn, self.Hd), (self.fn, self.fzn, self.fd) = pp["U"], pp["H"], pp["f"]
        self.A0 = self.Un * self.Hd ** 2 * self.fd
        self.HU = 64 * self.Hn ** 2 * self.Ud
        self.L = self.Ud * self.Hd ** 2 * self.fd
        self.one_z = sp.Poly(1 - z, z, mu)

    def NL(self, Phat, s, e, extra=None):
        """N L s^(2e) for P = Phat/s^e (s a Poly in z; e = 0 for a z-design); extra: N -> N - 64 H^2 extra."""
        Pz = Phat.diff(z)
        if e == 0:
            br = self.one_z * self.fzn * Phat + self.fn * (-Phat + self.one_z * Pz + Phat ** 2)
            s2e = sp.Poly(1, z, mu)
        else:
            se, se1 = s ** e, s ** (e - 1)
            br = (self.one_z * self.fzn * Phat * se
                  + self.fn * (-Phat * se + self.one_z * (Pz * s - e * Phat) * se1 + Phat ** 2))
            s2e = s ** (2 * e)
        out = self.A0 * s2e - self.HU * br
        if extra is not None:
            out = out - self.HU * self.fd * extra * s2e
        return out


def poly2(p):
    return Poly2({(i, j): Q(c) for (i, j), c in p.terms()})


def verify_box(E, Phat, s, e, box, verify, stats, label, extra=None):
    a, b = (Q(t) for t in box)
    verify(poly2(E.L), (fmpq(0), fmpq(1), a, b), 1, 30, stats, label + ": L > 0")
    nl = E.NL(Phat, s, e, extra)
    verify(poly2(nl), (fmpq(0), fmpq(1), a, b), 1, MAX_DEPTH, stats, label + ": N > 0")
    return {"deg_z": nl.degree(z), "deg_mu": nl.degree(mu)}


# ---------------------------------------------------------------- design (untrusted, floats)
def design_box(n, ell, box, var, deg, eps, funcs=None):
    """Phat (exact Poly in z, mu), s, e, delta_b, and the planning record of the box.  funcs: synthetic (U, H) floats."""
    ma, mb = box
    mid = (ma + mb) / 2
    dt = 2 * float(w_exact(n, ell, mid)) / (1 + float(w_exact(n, ell, mid)))
    delta_b = Fraction(dt).limit_denominator(1000) if var == "zeta" else None
    vmax = Fraction(1) if var == "z" else 1 / (1 + delta_b)
    vn = [float(vmax) * (1 - math.cos(math.pi * k / deg)) / 2 for k in range(deg + 1)]
    zn = [0.0] + [t if var == "z" else float(delta_b) * t / (1 - t) for t in vn[1:-1]] + [1.0]
    mus = [float(ma) + float(mb - ma) * (1 - math.cos(math.pi * j / DM)) / 2 for j in range(DM + 1)]
    grid, plan = [], []
    for mv in mus:
        S = Setting(n, ell, mv, funcs=funcs)
        sol = riccati(S, zn + list(GRID))
        vals = [design_value(S, zk, *sol[zk], float(eps)) for zk in zn]
        grid.append(vals)
        tab = tabulate(S)
        fit = Fit(S, var, cheb_coeffs(vals), float(vmax))
        if var == "zeta":
            fit.dt = float(delta_b)
        lmin = min(sol[t][1] for t in GRID[:-1])
        plan.append({"mu": mv, "q": S.q, "min_psi1": math.exp(lmin),
                     "sigma_design": design_slack(S, tab, sol, float(eps)), "sigma_fit": slack(tab, fit)[0]})
    ck = [cheb_coeffs([grid[j][k] for j in range(DM + 1)]) for k in range(deg + 1)]
    u = (2 * mu - R(ma) - R(mb)) / R(mb - ma)
    P = 0
    for jj in range(DM + 1):
        cv = cheb_coeffs([ck[k][jj] for k in range(deg + 1)])
        P += cheb_to_monomial(cv, 0, R(vmax), v) * sp.expand(sp.chebyshevt(jj, u))
    P = sp.Poly(sp.expand(P), v, mu)
    if var == "z":
        Phat, s, e = sp.Poly(P.as_expr().subs(v, z), z, mu), None, 0
    else:
        db = R(delta_b)
        Phat = sp.Poly(sum(c * mu ** j * z ** i * (z + db) ** (deg - i) for (i, j), c in P.terms()), z, mu)
        s, e = sp.Poly(z + db, z, mu), deg
    return Phat, s, e, delta_b, plan


# ---------------------------------------------------------------- one box, with the fallback
def certify(E, n, ell, box, design, verify, records, planfile, depth=0):
    """Certify the box (or its fallback pieces); appends one record per attempt; raises CertificateError on failure."""
    eps, var, deg = design
    degs = [g for g in DEGREES if g >= deg][:3]
    last = None
    for g in degs:
        t0 = time.time()
        Phat, s, e, delta_b, plan = design_box(n, ell, box, var, g, eps)
        rec = {"mu": [str(box[0]), str(box[1])], "variable": var, "degree": g, "eps": str(eps),
               "delta_b": None if delta_b is None else str(delta_b), "planning": plan}
        with open(planfile, "a") as fh:                              # the planning record, before verification
            fh.write(json.dumps(plain(rec), sort_keys=True) + "\n")
        rec["t_design_s"] = round(time.time() - t0, 2)
        t1, stats = time.time(), {}
        try:
            info = verify_box(E, Phat, s, e, box, verify, stats, f"D={n + 2} l={ell} mu in [{box[0]}, {box[1]}] deg {g}")
            rec.update(info, verified=True, bernstein=stats,
                       P={str(k): str(c) for k, c in Phat.as_dict().items()})
            rec["t_verify_s"] = round(time.time() - t1, 2)
            records.append(rec)
            return
        except CertificateError as exc:
            last = str(exc)[:400]
            rec.update(verified=False, failure=last, bernstein=stats, t_verify_s=round(time.time() - t1, 2))
            records.append(rec)
    if depth >= BISECT:
        raise CertificateError(f"box {box} failed after the fallback: {last}")
    mid = (box[0] + box[1]) / 2
    certify(E, n, ell, (box[0], mid), design, verify, records, planfile, depth + 1)
    certify(E, n, ell, (mid, box[1]), design, verify, records, planfile, depth + 1)


# ---------------------------------------------------------------- controls
def nc_bound(E, n, ell, box, design, verify, stats):
    """(a) the trial function b certifies a negative energy on W - K b at mu_c; (b) the box's certificate at mu_c fails."""
    muc = (box[0] + box[1]) / 2
    eps, var, deg = design
    Phat, s, e, delta_b, _ = design_box(n, ell, box, var, deg, eps)
    S = Setting(n, ell, float(muc))
    nq, h = 2000, float(ZB - ZA) / 2000
    I1 = I2 = 0.0
    for i in range(nq):
        t = float(ZA) + (i + 0.5) * h
        b = ((t - float(ZA)) * (float(ZB) - t)) ** 2
        bz = 2 * (t - float(ZA)) * (float(ZB) - t) * (float(ZA + ZB) - 2 * t)
        I1 += (S.f(t) * bz * bz * (1 - t) ** 2 + S.W(t) * b * b) * h
        I2 += b * b * b * h
    K = sp.Integer(math.ceil(2 * I1 / I2)) if I1 > 0 else sp.Integer(1)
    bexpr = (z - R(ZA)) ** 2 * (R(ZB) - z) ** 2
    sub = {mu: R(muc)}
    num = {k: sp.Poly(getattr(E, k).as_expr().subs(sub), z) for k in ("Un", "Hn", "fn")}
    den = {k: getattr(E, k).as_expr().subs(sub) for k in ("Ud", "Hd", "fd")}
    phi = bexpr
    q1 = sp.expand(num["fn"].as_expr() / den["fd"] * sp.diff(phi, z) ** 2 * (1 - z) ** 2)
    ctx.prec = 128
    polys = {"q1": q1, "U": num["Un"].as_expr() / den["Ud"], "H": num["Hn"].as_expr() / den["Hd"],
             "phi2": sp.expand(phi ** 2), "bphi2": sp.expand(K * bexpr * phi ** 2)}
    cf = {k: [acb(Q(c)) for c in sp.Poly(sp.expand(e_), z).all_coeffs()[::-1]] for k, e_ in polys.items()}

    def horner(cs, t):
        acc = acb(0)
        for c in reversed(cs):
            acc = acc * t + c
        return acc

    def integrand(t, analytic):
        Hv = horner(cf["H"], t)
        return horner(cf["q1"], t) + horner(cf["U"], t) / (64 * Hv * Hv) * horner(cf["phi2"], t) - horner(cf["bphi2"], t)

    Qv = acb.integral(integrand, acb(Q(ZA)), acb(Q(ZB)))
    certified = bool(Qv.real < 0)
    rejected, msg = False, ""
    try:                                     # the certificate at mu_c, against the planted potential, on the bump
        nl = E.NL(sp.Poly(Phat.as_expr().subs(mu, R(muc)), z, mu), s, e, sp.Poly(K * bexpr, z, mu))
        nlc = sp.Poly(nl.as_expr().subs(mu, R(muc)), z, mu)
        verify(poly2(nlc), (Q(ZA), Q(ZB), Q(muc), Q(muc)), 1, MAX_DEPTH, stats, "nc-bound on the bump")
    except CertificateError as exc:
        rejected, msg = True, str(exc)[:300]
    return {"mu_c": str(muc), "K": str(K), "Q_phi0": Qv.real.str(10), "bound_state_certified": certified,
            "certificate_rejected_on_planted": rejected, "message": msg}


def td_horizon(E, n, ell, box, design, verify, stats):
    """The first box's certificate plus c (1 - z) s^e with c = W(0)/f_z(0) - P(0) + 1/10 at mu = box[0]: must fail."""
    eps, var, deg = design
    Phat, s, e, delta_b, _ = design_box(n, ell, box, var, deg, eps)
    a = R(box[0])
    S0 = {k: getattr(E, k).as_expr().subs({z: 0, mu: a}) for k in ("Un", "Ud", "Hn", "Hd", "fzn", "fd")}
    W0 = (S0["Un"] / S0["Ud"]) / (64 * (S0["Hn"] / S0["Hd"]) ** 2)
    fz0 = S0["fzn"] / S0["fd"]
    P0 = Phat.as_expr().subs({z: 0, mu: a}) / (1 if e == 0 else R(delta_b) ** e)
    c = sp.Rational(W0 / fz0 - P0 + sp.Rational(1, 10))
    bump = sp.Poly(c * (1 - z) * (1 if e == 0 else s.as_expr() ** e), z, mu)
    return verify_box(E, Phat + bump, s, e, box, verify, stats, "td-horizon")


# ---------------------------------------------------------------- the run
def gate_pilot(root):
    """The band designs of DESIGN equal the pilot's at q_max(D) (results/hd/pilot/runs/record)."""
    with open(os.path.join(root, PILOT_RECORD)) as fh:
        rec = json.load(fh)
    ok = rec.get("verdict") == "VALID"
    for p in rec["result"]["pairs"]:
        key = (p["D"] - 2, p["l"])
        if p["rung"] == str(Q_MAX[key[0]]):
            dz = p["design"]
            ok = ok and key in DESIGN and DESIGN[key] == (Fraction(dz["eps"]), dz["variable"], dz["degree"])
    return ok and len(DESIGN) == 18, f"the pilot record is VALID and DESIGN equals its designs at q_max: {ok}"


def run(n, ell, control, root, out):
    verify = tampered_prove_sign if control == "td-verifier" else prove_sign
    checks, rec, timing = {}, {"D": n + 2, "l": ell}, {}
    ok, res = kats(verify)
    checks["KAT"] = (ok, str(res))
    checks["E0n"] = gate_E0n(root, "td-coeff" if control == "td-coeff" else "none")
    checks["PILOT"] = gate_pilot(root)
    hpos = all(c > 0 for _, c in sp.Poly(H_minus(n), x, d, m).terms())
    checks["H"] = (hpos, "H_- has positive coefficients, so H_- >= m > 0")
    qlo, qtext, kind = band_data(n, ell)
    qmax = Q_MAX[n]
    boxes = partition(n, ell, qmax, qlo)
    cov_ok, cov = coverage(n, ell, boxes, qmax, qlo)
    checks["coverage"] = (cov_ok, json.dumps(cov))
    rec.update({"kind": kind, "q_lo": qtext, "q_max": str(qmax), "design": [str(t) for t in DESIGN[(n, ell)]],
                "boxes_registered": [[str(a), str(b)] for a, b in boxes], "coverage": cov})
    lo, hi = inward(Fraction(cov["q(mu_b)^2"]), Fraction(cov["q(mu_a)^2"]))
    rec["claim_q"] = {"exact": f"[sqrt({cov['q(mu_b)^2']}), sqrt({cov['q(mu_a)^2']})]", "inward": [lo, hi]}
    if not all(okk for okk, _ in checks.values()):
        return checks, rec, timing
    t0 = time.time()
    E = Exact(n, ell, "none")
    timing["exact parts"] = round(time.time() - t0, 2)
    design = DESIGN[(n, ell)]
    if control == "td-horizon":
        stats = {}
        try:
            td_horizon(E, n, ell, boxes[0], design, verify, stats)
            checks["td-horizon"] = (True, "the tampered certificate verified (it must not)")
        except CertificateError as exc:
            checks["td-horizon"] = (False, str(exc)[:300])
        return checks, rec, timing
    if control == "nc-bound":
        stats = {}
        r = nc_bound(E, n, ell, boxes[0], design, verify, stats)
        rec["nc-bound"] = r
        checks["nc-bound (a)"] = (r["bound_state_certified"], f"Q[phi0] = {r['Q_phi0']}")
        checks["nc-bound (b)"] = (not r["certificate_rejected_on_planted"], r["message"] or "the certificate held")
        return checks, rec, timing
    records = []
    planfile = os.path.join(out, "planning.jsonl")
    for i, box in enumerate(boxes):
        t0 = time.time()
        key = f"box {i} mu in [{box[0]}, {box[1]}]"
        try:
            certify(E, n, ell, box, design, verify, records, planfile)
            checks[key] = (True, "N > 0 (with the fallback pieces, if any)")
        except CertificateError as exc:
            checks[key] = (False, str(exc)[:300])
        timing[key] = round(time.time() - t0, 2)
    rec["boxes"] = records
    if kind == "from 0+":
        last = [r for r in records if r["verified"] and Fraction(r["mu"][1]) == 1]
        checks["G-S6 (the box with Q = 0)"] = (bool(last), "the box ending at mu = 1 (q = 0, S6's known answer) verified")
    return checks, rec, timing


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--band", required=True, help="D,l")
    ap.add_argument("--control", choices=CONTROLS, default="none")
    ap.add_argument("--root", default=os.path.join(os.path.dirname(__file__), "..", ".."))
    a = ap.parse_args(argv)
    D, ell = (int(t) for t in a.band.split(","))
    t0 = time.time()
    record = {"claim": "results/hd/s/PREREG.md, HD-S", "band": f"D={D} l={ell}", "control": a.control,
              "provenance": provenance()}
    timing = {}
    try:
        checks, rec, timing = run(D - 2, ell, a.control, a.root, a.out)
        record.update(rec)
        record["checks"] = {k: {"ok": bool(ok), "detail": det} for k, (ok, det) in checks.items()}
        failed = [k for k, (ok, _) in checks.items() if not ok]
        verdict = "VERIFIED" if not failed else "REJECT: " + ", ".join(failed)
    except CertificateError as exc:
        verdict = f"REJECT: {exc}"
    except Exception as exc:  # noqa: BLE001  (fail-closed)
        verdict = f"REJECT: exception {type(exc).__name__}: {exc}"
    record["verdict"] = verdict
    record["timing"] = {**timing, "t_total_s": round(time.time() - t0, 2)}
    try:
        dump_json(plain(record), f"{a.out}/result.json")
    except Exception as exc:  # noqa: BLE001  (fail-closed: an unwritten record is a REJECT)
        verdict = record["verdict"] = f"REJECT: record not written: {type(exc).__name__}: {exc}"
    for k, val in record.get("checks", {}).items():
        print(f"{k}: {'PASS' if val['ok'] else 'FAIL'}  {val['detail'][:240]}")
    print(verdict[:2000])
    return 0 if verdict == "VERIFIED" else 1


if __name__ == "__main__":
    sys.exit(main())
