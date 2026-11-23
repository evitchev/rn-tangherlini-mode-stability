"""A1 for l >= 3 (results/a1/PREREG.md, P1): U_- > 0 on the closed exterior, D = 6, every l >= 3,
every q in [0, 99/100].  Then V_S- > 0 on the exterior and A_{l,q} >= 0.

    python -m a1.p1 --out DIR [--control NAME] [--ell0 10]

Part I, 3 <= l <= ell0.  onset.onset's rational parametrisation of the charge (A = (l+4) + (l-1) mu^2,
w = sqrt(1 - q^2) = (2l+3) mu / A, s = 1 + 2 m delta = (2l+3)((l+4) - (l-1) mu^2)/(5A)) and x = t x_H.
In lowest terms U_- = F(t, mu)/Den(mu).  mu_lo(l) = k/1000 with k the largest integer such that
w(k/1000)^2 <= 1 - (99/100)^2; since w increases with mu, [mu_lo, 1] covers q in [0, 99/100] (checked
exactly).  Den > 0 on [mu_lo, 1] and F > 0 on [0, 1] x [mu_lo, 1] are proved by exact Bernstein
bisection (onset.bernstein.prove_sign).

Part II, l > ell0 (the uniform lemma).  With eps = m^(-1/2) and kappa = m^(1/2) delta,
eps^6 U_-(x; m = eps^-2, delta = kappa eps) = P(eps, kappa, x), a polynomial.  Split P = Pos - Neg with
nonnegative coefficients; Pos has constant term 64.  For m >= m0 = m(ell0 + 1) and q in [0, 1]:
0 < eps <= eps_bar = 1/isqrt(m0); kappa^2 = m delta^2 = q^2/25 - delta, so 0 <= kappa <= 1/5;
0 <= x <= x_H <= 2.  On that box Pos >= 64 and Neg <= Neg(eps_bar, 1/5, 2), so
U_- = m^3 P >= m^3 (64 - Neg(eps_bar, 1/5, 2)), and the check is 64 - Neg(eps_bar, 1/5, 2) > 0.

Fail-closed (RULES.md A2): VERIFIED and exit 0 only if every check holds; otherwise REJECT: <reasons>
and exit 1.  --control selects a negative control or a tamper drill; each must REJECT:
    nc-ell2      Part I for l = 2 on q in [0, 99/100]: the certified negative region (BHM-017, O3)
    nc-bump      l = 3 with U_- - 10^7 * 64 t^3 (1 - t)^3: negative at t = 1/2, unchanged at t = 0, 1
    nc-coverage  mu_lo chosen for q = 98/100: the exact coverage check for 99/100 must fail
    nc-uniform   Part II with ell0 = 1 (m0 = 6, so l = 2 included): the corner bound must fail
    td-coeff     the coefficient 7680 of U_- changed to 7681: the transcription gate E0 must fail
    td-split     Part II with the x^4 monomials dropped from Neg: the identity P = Pos - Neg must fail
    td-verifier  the Bernstein verifier's acceptance threshold lowered from 0 to -1: the KATs must fail
"""
import argparse
import sys
import time
from fractions import Fraction
from math import isqrt

import sympy as sp
from flint import fmpq
from sympy.logic.boolalg import BooleanAtom

from ki.potentials import H_TARGET, H_minus, U_TARGET, U_minus, d, m, x
from onset.bernstein import Poly2, Q, prove_sign
from onset.onset import mu, param, t
from qnm1c.common import CertificateError, dump_json, provenance

CONTROLS = ("none", "nc-ell2", "nc-bump", "nc-coverage", "nc-uniform", "td-coeff", "td-split",
            "td-verifier")
QMAX = sp.Rational(99, 100)                  # q_max (TARGET_ADDENDUM_1.md)
MAX_DEPTH = 40


def tampered_prove_sign(p, box, sign, max_depth, stats, label, minrec=None):
    """TD-A1c: prove_sign with its acceptance test lo > 0 lowered to lo > -1.  Otherwise identical."""
    stack = [(box, 0)]
    while stack:
        (t0, t1, m0, m1), depth = stack.pop()
        b = p.bernstein(t0, t1, m0, m1)
        lo = min(sign * c for row in b for c in row)
        stats[label] = stats.get(label, 0) + 1
        if lo > -1:                                          # the tamper
            if minrec is not None:                           # recorded as prove_sign does (addendum 1)
                minrec[label] = lo if label not in minrec else min(minrec[label], lo)
            continue
        for (tt, mm) in ((t0, m0), (t0, m1), (t1, m0), (t1, m1)):
            if sign * p.value(tt, mm) <= 0:
                raise CertificateError(f"{label}: corner counterexample at ({tt}, {mm})")
        if depth >= max_depth:
            raise CertificateError(f"{label}: undecided at depth {depth}")
        tm = (t0 + t1) / 2
        stack += [((t0, tm, m0, m1), depth + 1), ((tm, t1, m0, m1), depth + 1)]
    return True


def kats(verify):
    """Known-answer tests of the verifier (each must come out as stated) and of Q."""
    box = (fmpq(0), fmpq(1), fmpq(0), fmpq(1))
    quad = {(2, 0): 1, (1, 0): -1, (0, 2): 1, (0, 1): -1}

    def accepts(terms):
        try:
            verify(Poly2(terms), box, 1, 30, {}, "KAT")
            return True
        except CertificateError:
            return False

    res = {
        "KAT1 -1 rejected": not accepts({(0, 0): -1}),
        "KAT2 (t-1/2)^2+(mu-1/2)^2-1/100 rejected": not accepts({**quad, (0, 0): fmpq(49, 100)}),
        "KAT3 t(1-t)+mu (zero at a corner) rejected": not accepts({(1, 0): 1, (2, 0): -1, (0, 1): 1}),
        "KAT4 (t-1/2)^2+(mu-1/2)^2+1/100 accepted": accepts({**quad, (0, 0): fmpq(51, 100)}),
    }
    try:
        Q(0.1)
        refused = False
    except TypeError:
        refused = True
    res["KAT5 Q refuses floats, keeps exact inputs"] = (
        refused and Q("0.1") == fmpq(1, 10) and Q(Fraction(1, 3)) == fmpq(1, 3)
        and Q(sp.Rational(2, 7)) == fmpq(2, 7))
    return all(res.values()), res


def rat(v):
    return sp.Rational(v)


def positive_mu(verify, poly_mu, a, b, stats, minrec, label):
    """Exact: the univariate polynomial in mu is > 0 on [a, b]."""
    p2 = Poly2({(0, j): Q(c) for (j,), c in sp.Poly(poly_mu, mu).terms()})
    verify(p2, (fmpq(0), fmpq(1), Q(a), Q(b)), 1, 30, stats, label, minrec)


def part1(verify, ell, U, rule_q, bump):
    """Part I for one l.  Returns (ok, record); raises CertificateError on a failed proof."""
    P = param(ell)
    stats, minrec, rec = {}, {}, {"ell": ell, "m": int(P["m"])}
    ids = [sp.cancel(P["s"] ** 2 - (1 + 4 * P["m"] * P["q2"] / 25)) == 0,
           sp.cancel(P["q2"].subs(mu, 1)) == 0, sp.cancel(P["q2"].subs(mu, 0) - 1) == 0,
           sp.cancel(P["delta"].subs(mu, 1)) == 0]
    wn, wd = sp.fraction(sp.cancel(sp.diff(P["w"], mu)))
    sw = 1 if sp.Poly(wn, mu).eval(sp.Rational(1, 2)) > 0 else -1
    sd = 1 if sp.Poly(wd, mu).eval(sp.Rational(1, 2)) > 0 else -1
    positive_mu(verify, sw * wn, 0, 1, stats, minrec, "w' numerator")
    positive_mu(verify, sd * wd, 0, 1, stats, minrec, "w' denominator")
    if sw * sd < 0:
        raise CertificateError(f"l={ell}: w is not increasing in mu")
    rec["parametrisation"] = {"s^2 = 1 + 4mq^2/25, q(1) = 0, q(0) = 1, delta(1) = 0": ids,
                              "w increasing on [0, 1]": True}

    def w_at(v):
        return rat(P["w"].subs(mu, v))

    w2max = 1 - rule_q ** 2
    k = 0
    while k < 1000 and w_at(sp.Rational(k + 1, 1000)) ** 2 <= w2max:
        k += 1
    mu_lo = sp.Rational(k, 1000)
    q2_lo = 1 - w_at(mu_lo) ** 2
    covers = q2_lo >= QMAX ** 2
    rec.update({"mu_lo": str(mu_lo), "q_at_mu_lo_squared": str(q2_lo),
                "q_at_mu_lo_approx": float(sp.sqrt(q2_lo).evalf(20)), "covers_q_max": bool(covers)})
    if not covers:
        raise CertificateError(f"l={ell}: [mu_lo, 1] = [{mu_lo}, 1] reaches only q^2 = {q2_lo} < (99/100)^2")

    expr = U.subs({m: P["m"], d: P["delta"]}).subs(x, t * P["xH"])
    num, den = sp.fraction(sp.cancel(sp.together(expr)))
    if den.has(t):
        raise CertificateError(f"l={ell}: denominator depends on t")
    sg = 1 if sp.Poly(den, mu).eval(sp.Rational(1, 2)) > 0 else -1
    F, Den = sp.expand(sg * num), sp.expand(sg * den)
    if bump:                                    # NC-A1b: plant a negative region at t = 1/2
        F = sp.expand(F - 10**7 * 64 * t**3 * (1 - t) ** 3 * Den)
    elif sp.cancel(F / Den - expr) != 0:
        raise CertificateError(f"l={ell}: F/Den differs from U_-")
    Fp = sp.Poly(F, t, mu)
    rec.update({"F_degrees": [Fp.degree(t), Fp.degree(mu)], "Den_degree": sp.Poly(Den, mu).degree(),
                "Den": str(sp.factor(Den))})
    positive_mu(verify, Den, mu_lo, 1, stats, minrec, "Den")
    F2 = Poly2({(i, j): Q(c) for (i, j), c in Fp.terms()})
    verify(F2, (fmpq(0), fmpq(1), Q(mu_lo), fmpq(1)), 1, MAX_DEPTH, stats, "F", minrec)
    den2 = Poly2({(0, j): Q(c) for (j,), c in sp.Poly(Den, mu).terms()})
    den_max = max(c for row in den2.bernstein(fmpq(0), fmpq(1), Q(mu_lo), fmpq(1)) for c in row)
    lower = minrec["F"] / den_max
    rec.update({"bernstein_leaves": stats, "min_bernstein_F": str(minrec["F"]),
                "max_bernstein_Den": str(den_max),
                "U_lower_bound": str(lower),
                "U_lower_bound_approx": float(Fraction(int(lower.p), int(lower.q)))})
    return all(ids), rec


def part2(U, ell0, tamper_split):
    """Part II, the uniform lemma for l > ell0.  Returns (ok, record)."""
    eps, kap, q2 = sp.symbols("eps kappa q2")
    Pexpr = sp.expand(eps**6 * U.subs({m: eps**-2, d: kap * eps}))
    is_poly = sp.fraction(sp.together(Pexpr))[1] == 1
    PP = sp.Poly(Pexpr, eps, kap, x)
    pos = {mon: c for mon, c in PP.terms() if c > 0}
    neg = {mon: -c for mon, c in PP.terms() if c < 0}
    if tamper_split:                            # TD-A1b
        neg = {mon: c for mon, c in neg.items() if mon[2] != 4}

    def as_expr(dct):
        return sum((c * eps**a * kap**b * x**e for (a, b, e), c in dct.items()), sp.Integer(0))

    split_ok = sp.expand(Pexpr - (as_expr(pos) - as_expr(neg))) == 0
    const_ok = pos.get((0, 0, 0)) == 64
    kappa_ok = sp.expand((1 + 2 * m * d) ** 2 - 1 - 4 * m * q2 / 25 - 4 * m * (m * d**2 + d - q2 / 25)) == 0
    m0 = ell0 * (ell0 + 5)                       # m(ell0 + 1) = ell0 (ell0 + 5)
    eps_bar = sp.Rational(1, isqrt(m0))
    eps_ok = bool(m0 * eps_bar**2 >= 1)          # a sympy Boolean otherwise (addendum 1)
    neg_corner = as_expr(neg).subs({eps: eps_bar, kap: sp.Rational(1, 5), x: 2})
    bound = 64 - neg_corner
    checks = {"eps^6 U_- is a polynomial in (eps, kappa, x)": is_poly,
              "P = Pos - Neg": split_ok, "Pos(0, 0, 0) = 64": const_ok,
              "(1 + 2 m delta)^2 = 1 + 4 m q^2/25  <=>  m delta^2 + delta = q^2/25": kappa_ok,
              "eps_bar >= m0^(-1/2)": eps_ok, "64 - Neg(eps_bar, 1/5, 2) > 0": bool(bound > 0)}
    rec = {"ell0": ell0, "m0": m0, "eps_bar": str(eps_bar), "kappa_max": "1/5", "x_max": "2",
           "Pos": {str(k): str(v) for k, v in sorted(pos.items())},
           "Neg": {str(k): str(v) for k, v in sorted(neg.items())},
           "Neg_at_corner": str(neg_corner), "bound": str(bound),
           "bound_approx": float(bound), "checks": checks}
    return all(checks.values()), rec


def run(control, ell0):
    verify = tampered_prove_sign if control == "td-verifier" else prove_sign
    checks, rec = {}, {"qmax": str(QMAX), "ell0": ell0}
    ok, res = kats(verify)
    checks["KAT"] = (ok, str(res))

    U = U_TARGET + (x**2 * m * (1 + m * d) if control == "td-coeff" else 0)
    e0u, e0h = sp.expand(U_minus(4) - U), sp.expand(H_minus(4) - H_TARGET)
    checks["E0"] = (e0u == 0 and e0h == 0, f"S5 (5.63b), (5.62b) at n = 4 minus TARGET.md's U_-, H_-: {e0u}, {e0h}")
    hpos = all(c > 0 for _, c in sp.Poly(H_TARGET, x, d, m).terms())
    checks["H"] = (hpos, "H_- = m + 10 x + 10 m delta x: every coefficient > 0, so H_- >= m > 0")

    if control in ("none", "td-coeff", "td-verifier"):
        ells = list(range(3, ell0 + 1))
    elif control == "nc-ell2":
        ells = [2]
    elif control in ("nc-bump", "nc-coverage"):
        ells = [3]
    else:
        ells = []
    rule_q = sp.Rational(98, 100) if control == "nc-coverage" else QMAX
    rec["part1"] = []
    timing = {}
    for ell in ells:
        t0 = time.time()
        try:
            ok, r = part1(verify, ell, U, rule_q, control == "nc-bump")
            checks[f"P1 l={ell}"] = (ok, f"U_- > 0 on [0, x_H] for q <= q(mu_lo), lower bound {r['U_lower_bound_approx']:.6g}")
        except CertificateError as exc:
            r = {"ell": ell, "failure": str(exc)}
            checks[f"P1 l={ell}"] = (False, str(exc))
        rec["part1"].append(r)
        timing[f"part1 l={ell}"] = round(time.time() - t0, 2)

    if control in ("none", "td-coeff", "td-verifier", "nc-uniform", "td-split"):
        t0 = time.time()
        ok, r = part2(U, 1 if control == "nc-uniform" else ell0, control == "td-split")
        rec["part2"] = r
        checks["P1 uniform"] = (ok, f"l >= {r['ell0'] + 1} (m >= {r['m0']}), q in [0, 1], x in [0, 2]: "
                                    f"U_- >= m^3 (64 - Neg(corner)) = m^3 * {r['bound_approx']:.6g}")
        timing["part2"] = round(time.time() - t0, 2)
    return checks, rec, timing


def plain(obj):
    """The record in plain JSON types: dicts, lists, str, int, float, bool (addendum 1)."""
    if isinstance(obj, dict):
        return {str(k): plain(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [plain(v) for v in obj]
    if isinstance(obj, (bool, BooleanAtom)):
        return bool(obj)
    if isinstance(obj, (str, int, float)) or obj is None:
        return obj
    return str(obj)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--control", choices=CONTROLS, default="none")
    ap.add_argument("--ell0", type=int, default=10)
    a = ap.parse_args(argv)
    t0 = time.time()
    record = {"claim": "results/a1/PREREG.md, P1 (A1 for l >= 3)", "control": a.control,
              "provenance": provenance()}
    timing = {}
    try:
        checks, rec, timing = run(a.control, a.ell0)
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
        print(f"{k}: {'PASS' if v['ok'] else 'FAIL'}  {v['detail'][:300]}")
    print(verdict)
    return 0 if verdict == "VERIFIED" else 1


if __name__ == "__main__":
    sys.exit(main())
