"""Stage 2, step 2, HD-E (results/hd/elementary/PREREG.md): positivity of U_- for D = 7..11 where it holds.

    python -m hd.elementary --out DIR [--control NAME] [--root REPO]

D = n + 2 with n = 5..9; U_-, H_- are S5's (5.63b), (5.62b) at general n (ki.potentials), m = (l-1)(l+n),
(1 + 2 m delta)^2 = 1 + 4 m q^2/(n+1)^2.
E1  every l in [l_el(n), l0(n)] and q in [0, 99/100]: U_- > 0 on [0, x_H]   (l_el(5..9) = 4, 5, 6, 6, 7)
E2  each band with a screen onset q_on > 0: U_- > 0 for q in [0, q_split]     (the table BANDS)
E3  Lemma U(n), l > l0(n), q in [0, 1], x in [0, 2]: with eps = m^(-1/2) and kappa = m^(1/2) delta,
    eps^6 U_- = Pos - Neg, Pos(0) = 64, kappa <= 1/(n+1), x <= 2, eps <= eps_bar = 1/isqrt(m(l0 + 1)), so
    U_- >= m^3 (64 - Neg(eps_bar, 1/(n+1), 2)).  l0(n) is the least l0 >= max(l_el(n), 10), up to 400, at which
    that bound is > 0.
Part I for one (n, l, q_hi): A = (l+n) + (l-1) mu^2, B = 2l + n - 1, w = B mu/A, s = B((l+n) - (l-1) mu^2)/((n+1) A);
mu_lo = k/10000 with k the largest such that w(k/10000)^2 <= 1 - q_hi^2 (binary search; w increases, proved);
the coverage q(mu_lo)^2 >= q_hi^2 is checked exactly; U_- = F(t, mu)/Den(mu) in lowest terms, x = t x_H;
Den > 0 on [mu_lo, 1] and F > 0 on [0, 1] x [mu_lo, 1] by exact Bernstein bisection.
Gates: the KATs of a1.p1; E0n, U_minus(n) and H_minus(n) equal Kimi's independent transcription (BHM-036, archived,
SHA-256 checked) for n = 2..12; PARAM4, param_n(4, l) equals onset.param(l) for l = 2..5; H_- has positive
coefficients.
Fail-closed: VERIFIED and exit 0 only if every check holds.  --control (each must REJECT):
    nc-onset-h   E2's pipeline for D = 7, l = 2 up to q = 951/1000, past its horizon onset 0.9497
    nc-onset-i   E2's pipeline for D = 10, l = 3 up to q = 99/200, past its interior onset 0.4913
    nc-zero      D = 8, l = 2 on q in [0, 1/10]: a band from 0+, negative already at Q = 0
    nc-coverage  D = 7, l = 4 with mu_lo chosen for q = 98/100: the coverage check for 99/100 must fail
    nc-uniform   Lemma U(9) with l0 = 2 forced: the corner bound must fail
    td-coeff     U_minus(n) plus 16 n m^2 (the constant 16 n (n+2) m^2 K becomes 16 n (n+3) m^2 K): E0n must fail
    td-param     B = 2l + n instead of 2l + n - 1 in param_n: the identity s^2 = 1 + 4mq^2/(n+1)^2 must fail
    td-verifier  the verifier's acceptance threshold lowered to -1: the KATs must fail
"""
import argparse
import hashlib
import importlib.util
import os
import sys
import time
from math import isqrt

import sympy as sp
from flint import fmpq

from a1.p1 import kats, plain, positive_mu, tampered_prove_sign
from ki.potentials import H_minus, U_minus, d, m, x
from onset.bernstein import Poly2, Q, prove_sign
from onset.onset import mu, param, t
from qnm1c.common import CertificateError, dump_json, provenance

CONTROLS = ("none", "nc-onset-h", "nc-onset-i", "nc-zero", "nc-coverage", "nc-uniform", "td-coeff", "td-param",
            "td-verifier")
QMAX = sp.Rational(99, 100)
NGRID = 10000
MAX_DEPTH = 40
L_EL = {5: 4, 6: 5, 7: 6, 8: 6, 9: 7}
# the screen's onsets (BHM-014, results/screen/runs/record/main/result.json) and q_split = floor(1000 q_on)/1000 - 1/1000
BANDS = {(5, 2): ("0.949691435450051", "948/1000"), (5, 3): ("0.978974227897648", "977/1000"),
         (6, 3): ("0.945000892435492", "944/1000"), (6, 4): ("0.984607646581368", "983/1000"),
         (7, 3): ("0.922249047654215", "921/1000"), (7, 4): ("0.953118911659811", "952/1000"),
         (7, 5): ("0.988544342135894", "987/1000"),
         (8, 3): ("0.491294065310271", "490/1000"), (8, 4): ("0.921402689606592", "920/1000"),
         (8, 5): ("0.962330726004671", "961/1000"),
         (9, 4): ("0.898980683353904", "897/1000"), (9, 5): ("0.930967303640908", "929/1000"),
         (9, 6): ("0.969856860225322", "968/1000")}
KIMI_BUILD = "results/p3/audits/kimi_2026-10-22/own/build.py"
KIMI_BUILD_SHA256 = "399bf7e1c388475409bebdc6116bcacdce7e4d47311855ebfcea350a004c79cc"   # Kimi's SHA256SUMS (sealed)


def U_of(n, control):
    return U_minus(n) + (16 * n * m**2 if control == "td-coeff" else 0)


def param_n(n, ell, control="none"):
    L, nn = sp.Integer(ell), sp.Integer(n)
    A = (L + nn) + (L - 1) * mu**2
    B = 2 * L + nn - (0 if control == "td-param" else 1)
    w = B * mu / A
    s = B * ((L + nn) - (L - 1) * mu**2) / ((nn + 1) * A)
    mm = (L - 1) * (L + nn)
    return {"A": A, "w": w, "s": s, "m": mm, "delta": sp.cancel((s - 1) / (2 * mm)),
            "xH": sp.cancel(2 / (1 + w)), "q2": sp.cancel(1 - w**2)}


def gate_E0n(root, control):
    path = os.path.join(root, KIMI_BUILD)
    with open(path, "rb") as fh:
        sha_ok = hashlib.sha256(fh.read()).hexdigest() == KIMI_BUILD_SHA256
    spec = importlib.util.spec_from_file_location("kimi_build", path)
    kb = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(kb)
    km, kd = sp.symbols("m d")
    same = []
    for n in range(2, 13):
        ku, kh = kb.ki_Usymbol(n)
        ku = ku.subs({km: m, kd: d, kb.x: x})
        kh = kh.subs({km: m, kd: d, kb.x: x})
        same.append(sp.expand(U_of(n, control) - ku) == 0 and sp.expand(H_minus(n) - kh) == 0)
    return sha_ok and all(same), f"Kimi's build.py SHA-256 matches: {sha_ok}; n = 2..12 identical: {same}"


def gate_PARAM4():
    res = []
    for ell in range(2, 6):
        a, b = param_n(4, ell), param(ell)
        res.append(all(sp.cancel(a[k] - b[k]) == 0 for k in ("w", "s", "delta", "xH", "q2")))
    return all(res), f"param_n(4, l) = onset.param(l), l = 2..5: {res}"


def part1(verify, n, ell, q_hi, U, control="none", rule_q=None):
    """U_- > 0 on [0, x_H] for q in [0, q_hi].  Returns a record; raises CertificateError on failure."""
    P = param_n(n, ell, control)
    stats, minrec, rec = {}, {}, {"n": n, "D": n + 2, "ell": ell, "m": int(P["m"]), "q_hi": str(q_hi)}
    ids = [sp.cancel(P["s"] ** 2 - (1 + 4 * P["m"] * P["q2"] / (n + 1) ** 2)) == 0,
           sp.cancel(P["q2"].subs(mu, 1)) == 0, sp.cancel(P["q2"].subs(mu, 0) - 1) == 0,
           sp.cancel(P["delta"].subs(mu, 1)) == 0]
    if not all(ids):
        raise CertificateError(f"n={n} l={ell}: parametrisation identities fail: {ids}")
    wn, wd = sp.fraction(sp.cancel(sp.diff(P["w"], mu)))
    sw = 1 if sp.Poly(wn, mu).eval(sp.Rational(1, 2)) > 0 else -1
    sd = 1 if sp.Poly(wd, mu).eval(sp.Rational(1, 2)) > 0 else -1
    positive_mu(verify, sw * wn, 0, 1, stats, minrec, "w' numerator")
    positive_mu(verify, sd * wd, 0, 1, stats, minrec, "w' denominator")
    if sw * sd < 0:
        raise CertificateError(f"n={n} l={ell}: w is not increasing in mu")

    def w2(k):
        return sp.Rational(P["w"].subs(mu, sp.Rational(k, NGRID))) ** 2

    w2max = 1 - (rule_q if rule_q is not None else q_hi) ** 2
    lo, hi = 0, NGRID                        # w2(lo) = 0 <= w2max; find the largest k with w2(k) <= w2max
    if w2(hi) <= w2max:
        lo = hi
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if w2(mid) <= w2max:
            lo = mid
        else:
            hi = mid
    mu_lo = sp.Rational(lo, NGRID)
    q2_lo = 1 - w2(lo)
    covers = bool(q2_lo >= q_hi**2)
    rec.update({"mu_lo": str(mu_lo), "q_at_mu_lo_squared": str(q2_lo), "covers": covers})
    if not covers:
        raise CertificateError(f"n={n} l={ell}: [mu_lo, 1] = [{mu_lo}, 1] reaches only q^2 = {q2_lo} < {q_hi ** 2}")

    expr = U.subs({m: P["m"], d: P["delta"]}).subs(x, t * P["xH"])
    num, den = sp.fraction(sp.cancel(sp.together(expr)))
    if den.has(t):
        raise CertificateError(f"n={n} l={ell}: denominator depends on t")
    sg = 1 if sp.Poly(den, mu).eval(sp.Rational(1, 2)) > 0 else -1
    F, Den = sp.expand(sg * num), sp.expand(sg * den)
    if sp.cancel(F / Den - expr) != 0:
        raise CertificateError(f"n={n} l={ell}: F/Den differs from U_-")
    Fp = sp.Poly(F, t, mu)
    rec.update({"F_degrees": [Fp.degree(t), Fp.degree(mu)], "Den": str(sp.factor(Den))})
    positive_mu(verify, Den, mu_lo, 1, stats, minrec, "Den")
    F2 = Poly2({(i, j): Q(c) for (i, j), c in Fp.terms()})
    verify(F2, (fmpq(0), fmpq(1), Q(mu_lo), fmpq(1)), 1, MAX_DEPTH, stats, "F", minrec)
    den2 = Poly2({(0, j): Q(c) for (j,), c in sp.Poly(Den, mu).terms()})
    den_max = max(c for row in den2.bernstein(fmpq(0), fmpq(1), Q(mu_lo), fmpq(1)) for c in row)
    lower = minrec["F"] / den_max
    rec.update({"bernstein_leaves": stats["F"], "U_lower_bound": str(lower)})
    return rec


def lemma_U(n, U, l0_forced=None):
    """Lemma U(n).  Returns (ok, record)."""
    eps, kap, q2 = sp.symbols("eps kappa q2")
    Pexpr = sp.expand(eps**6 * U.subs({m: eps**-2, d: kap * eps}))
    is_poly = sp.fraction(sp.together(Pexpr))[1] == 1
    PP = sp.Poly(Pexpr, eps, kap, x)
    pos = {mon: c for mon, c in PP.terms() if c > 0}
    neg = {mon: -c for mon, c in PP.terms() if c < 0}

    def as_expr(dct):
        return sum((c * eps**a * kap**b * x**e for (a, b, e), c in dct.items()), sp.Integer(0))

    split_ok = sp.expand(Pexpr - (as_expr(pos) - as_expr(neg))) == 0
    const_ok = pos.get((0, 0, 0)) == 64
    kappa_ok = sp.expand((1 + 2 * m * d) ** 2 - 1 - 4 * m * q2 / (n + 1) ** 2
                         - 4 * m * (m * d**2 + d - q2 / (n + 1) ** 2)) == 0
    kbar = sp.Rational(1, n + 1)
    negx = as_expr(neg)

    def bound_at(l0):
        m0 = l0 * (l0 + 1 + n)                     # m(l0 + 1) = l0 (l0 + 1 + n)
        eb = sp.Rational(1, isqrt(m0))
        return m0, eb, bool(m0 * eb**2 >= 1), 64 - negx.subs({eps: eb, kap: kbar, x: 2})

    if l0_forced is not None:
        l0 = l0_forced
    else:
        l0 = max(L_EL[n], 10)
        while l0 <= 400 and not (bound_at(l0)[3] > 0):
            l0 += 1
    m0, eb, eps_ok, bound = bound_at(l0)
    checks = {"eps^6 U_- is a polynomial": bool(is_poly), "P = Pos - Neg": bool(split_ok),
              "Pos(0, 0, 0) = 64": bool(const_ok), "kappa identity from (5.58)": bool(kappa_ok),
              "eps_bar >= m0^(-1/2)": eps_ok, "64 - Neg(eps_bar, 1/(n+1), 2) > 0": bool(bound > 0)}
    rec = {"n": n, "l0": l0, "m0": m0, "eps_bar": str(eb), "kappa_max": str(kbar), "x_max": "2",
           "Neg_monomials": len(neg), "bound": str(bound), "bound_approx": float(bound), "checks": checks}
    return all(checks.values()), rec


def run(control, root):
    verify = tampered_prove_sign if control == "td-verifier" else prove_sign
    checks, rec, timing = {}, {"qmax": str(QMAX), "L_EL": {str(k): v for k, v in L_EL.items()},
                               "bands": {f"D={k[0] + 2} l={k[1]}": v for k, v in BANDS.items()}}, {}
    ok, res = kats(verify)
    checks["KAT"] = (ok, str(res))
    checks["E0n"] = gate_E0n(root, control)
    checks["PARAM4"] = gate_PARAM4()
    hpos = all(all(c > 0 for _, c in sp.Poly(H_minus(n), x, d, m).terms()) for n in range(5, 10))
    checks["H"] = (hpos, "H_- = m + n(n+1)x/2 + n(n+1) m delta x/2: every coefficient > 0, so H_- >= m > 0")

    jobs = []                                   # (label, n, ell, q_hi, rule_q)
    if control in ("none", "td-coeff", "td-param", "td-verifier"):
        for n in range(5, 10):
            jobs += [("E2", n, ell, sp.Rational(qs), None) for (nn, ell), (_, qs) in BANDS.items() if nn == n]
    elif control == "nc-onset-h":
        jobs = [("NC", 5, 2, sp.Rational(951, 1000), None)]
    elif control == "nc-onset-i":
        jobs = [("NC", 8, 3, sp.Rational(99, 200), None)]
    elif control == "nc-zero":
        jobs = [("NC", 6, 2, sp.Rational(1, 10), None)]
    elif control == "nc-coverage":
        jobs = [("NC", 5, 4, QMAX, sp.Rational(98, 100))]

    rec["E2"], rec["E1"], rec["E3"] = [], [], []
    l0s = {}
    if control in ("none", "td-coeff", "td-param", "td-verifier", "nc-uniform"):
        for n in ([9] if control == "nc-uniform" else range(5, 10)):
            t0 = time.time()
            okU, r = lemma_U(n, U_of(n, control), 2 if control == "nc-uniform" else None)
            rec["E3"].append(r)
            checks[f"E3 D={n + 2}"] = (okU, f"l >= {r['l0'] + 1}: U_- >= m^3 * {r['bound_approx']:.6g}")
            timing[f"E3 D={n + 2}"] = round(time.time() - t0, 2)
            l0s[n] = r["l0"]
    if control in ("none", "td-coeff", "td-param", "td-verifier"):
        for n in range(5, 10):
            jobs += [("E1", n, ell, QMAX, None) for ell in range(L_EL[n], l0s[n] + 1)]
    for label, n, ell, q_hi, rule_q in jobs:
        t0 = time.time()
        key = f"{label} D={n + 2} l={ell} q<={q_hi}"
        try:
            r = part1(verify, n, ell, q_hi, U_of(n, control), control, rule_q)
            checks[key] = (True, f"U_- > 0, lower bound {r['U_lower_bound'][:40]}")
        except CertificateError as exc:
            r = {"n": n, "ell": ell, "q_hi": str(q_hi), "failure": str(exc)}
            checks[key] = (False, str(exc))
        rec["E1" if label == "E1" else "E2"].append(r)
        timing[key] = round(time.time() - t0, 2)
    return checks, rec, timing


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--control", choices=CONTROLS, default="none")
    ap.add_argument("--root", default=os.path.join(os.path.dirname(__file__), "..", ".."))
    a = ap.parse_args(argv)
    t0 = time.time()
    record = {"claim": "results/hd/elementary/PREREG.md, HD-E (E1-E3)", "control": a.control,
              "provenance": provenance()}
    timing = {}
    try:
        checks, rec, timing = run(a.control, a.root)
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
    for k, v in record.get("checks", {}).items():
        print(f"{k}: {'PASS' if v['ok'] else 'FAIL'}  {v['detail'][:240]}")
    print(verdict[:2000])
    return 0 if verdict == "VERIFIED" else 1


if __name__ == "__main__":
    sys.exit(main())
