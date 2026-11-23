"""Stage A2, A2-E (results/a2/elementary/PREREG.md): U_- >= 0 on the closed exterior for 3 <= l <= 10 and every
q in [q(mu_lo(l)), 1], D = 6.  Then V_S- >= 0, so A_{l,q} >= 0.

    python -m a2.elementary --out DIR [--control NAME]

A1's P1 Part I (code/a1/p1.py) on the other side of its boxes: mu in [0, mu_lo(l)], with mu_lo(l) P1's lower end (the
largest k/1000 with w(k/1000)^2 <= 1 - (99/100)^2), so that A2-E's boxes meet P1's; mu = 0 is q = 1.  With x = t x_H,
U_- = F(t, mu)/Den(mu) in lowest terms (onset.onset's parametrisation).
  l = 4..10  Den > 0 on [0, mu_lo] and F > 0 on [0, 1] x [0, mu_lo], by exact Bernstein bisection.
  l = 3      F(1, 0) = 0 (c(3) = 0, E3), so no strict bound holds at that corner.  With s = 1 - t,
             F(1 - s, mu) = mu K(mu) + s G(s, mu), where K = F(1, mu)/mu and G = (F(1 - s, mu) - F(1, mu))/s are exact
             polynomial divisions (remainders 0, checked).  K > 0 on [0, mu_lo] and G > 0 on [0, 1] x [0, mu_lo] give
             F >= 0, with equality only at (t, mu) = (1, 0), the extremal horizon.
Fail-closed (RULES.md A2): VERIFIED and exit 0 only if every check holds; otherwise REJECT: <reasons>, exit 1.
--control (each must REJECT):
    nc-ell2      l = 2 on [0, mu_lo(2)]: its negative region (U_-(x_H) = -115200 at q = 1)
    nc-strict    l = 3 with a strict bound on F itself: F(1, 0) = 0 at a corner of the box
    nc-bump      l = 4 with F - 10^7 * 64 t^3 (1 - t)^3 Den: negative at t = 1/2
    td-coeff     the coefficient 7680 of U_- changed to 7681: the transcription gate E0 must fail
    td-verifier  the Bernstein verifier's acceptance threshold lowered from 0 to -1: the KATs must fail
"""
import argparse
import datetime
import os
import sys
import time
from fractions import Fraction

import sympy as sp
from flint import fmpq

from a1.p1 import MAX_DEPTH, QMAX, kats, plain, positive_mu, tampered_prove_sign
from ki.potentials import H_TARGET, H_minus, U_TARGET, U_minus, d, m, x
from onset.bernstein import Poly2, Q, prove_sign
from onset.onset import mu, param, t
from qnm1c.common import CertificateError, dump_json, provenance

CONTROLS = ("none", "nc-ell2", "nc-strict", "nc-bump", "td-coeff", "td-verifier")
ELLS = range(3, 11)
s = sp.Symbol("s")


def mu_lo(P):
    """A1's P1 lower end: the largest k/1000 with w(k/1000)^2 <= 1 - (99/100)^2."""
    def w_at(v):
        return sp.Rational(P["w"].subs(mu, v))
    k = 0
    while k < 1000 and w_at(sp.Rational(k + 1, 1000)) ** 2 <= 1 - QMAX ** 2:
        k += 1
    return sp.Rational(k, 1000)


def poly2(expr, a, b):
    """A polynomial in (a, b) as a Poly2 in the slots (t, mu)."""
    return Poly2({(i, j): Q(c) for (i, j), c in sp.Poly(expr, a, b).terms()})


def part(verify, ell, U, control):
    P = param(ell)
    stats, minrec = {}, {}
    rec = {"ell": ell, "m": int(P["m"])}
    ids = [sp.cancel(P["s"] ** 2 - (1 + 4 * P["m"] * P["q2"] / 25)) == 0, sp.cancel(P["q2"].subs(mu, 0) - 1) == 0]
    wn, wd = sp.fraction(sp.cancel(sp.diff(P["w"], mu)))
    sw = 1 if sp.Poly(wn, mu).eval(sp.Rational(1, 2)) > 0 else -1
    sd = 1 if sp.Poly(wd, mu).eval(sp.Rational(1, 2)) > 0 else -1
    positive_mu(verify, sw * wn, 0, 1, stats, minrec, "w' numerator")
    positive_mu(verify, sd * wd, 0, 1, stats, minrec, "w' denominator")
    if sw * sd < 0 or not all(ids):
        raise CertificateError(f"l={ell}: parametrisation: identities {ids}, w increasing {sw * sd > 0}")
    lo = mu_lo(P)
    q2_lo = 1 - sp.Rational(P["w"].subs(mu, lo)) ** 2
    rec.update({"mu_lo": str(lo), "q_at_mu_lo_squared": str(q2_lo),
                "q_at_mu_lo_approx": float(sp.sqrt(q2_lo).evalf(20)), "q(0) = 1": True})
    if q2_lo < QMAX ** 2:
        raise CertificateError(f"l={ell}: q(mu_lo)^2 = {q2_lo} < (99/100)^2, so [0, mu_lo] does not reach q_max")
    expr = U.subs({m: P["m"], d: P["delta"]}).subs(x, t * P["xH"])
    num, den = sp.fraction(sp.cancel(sp.together(expr)))
    if den.has(t):
        raise CertificateError(f"l={ell}: denominator depends on t")
    sg = 1 if sp.Poly(den, mu).eval(sp.Rational(1, 2)) > 0 else -1
    F, Den = sp.expand(sg * num), sp.expand(sg * den)
    if sp.cancel(F / Den - expr) != 0:
        raise CertificateError(f"l={ell}: F/Den differs from U_-")
    rec.update({"F_degrees": [sp.Poly(F, t, mu).degree(t), sp.Poly(F, t, mu).degree(mu)], "Den": str(sp.factor(Den))})
    positive_mu(verify, Den, 0, lo, stats, minrec, "Den")
    if ell == 3 and control != "nc-strict":
        Fs = sp.expand(F.subs(t, 1 - s))
        F1 = sp.expand(F.subs(t, 1))
        K, rK = sp.div(sp.Poly(F1, mu), sp.Poly(mu, mu))
        G, rG = sp.div(sp.Poly(sp.expand(Fs - F1), s, mu), sp.Poly(s, s, mu))
        identity = sp.expand(Fs - (mu * K.as_expr() + s * G.as_expr())) == 0
        rec["splitting"] = {"F(1, mu) divisible by mu": rK.is_zero, "F(1 - s, mu) - F(1, mu) divisible by s": rG.is_zero,
                            "F(1 - s, mu) = mu K + s G": identity, "F(1, 0)": str(F1.subs(mu, 0))}
        if not (rK.is_zero and rG.is_zero and identity):
            raise CertificateError(f"l=3: the splitting fails: {rec['splitting']}")
        positive_mu(verify, K.as_expr(), 0, lo, stats, minrec, "K")
        verify(poly2(G.as_expr(), s, mu), (fmpq(0), fmpq(1), fmpq(0), Q(lo)), 1, MAX_DEPTH, stats, "G", minrec)
        rec["bound"] = {"min_bernstein_K": str(minrec["K"]), "min_bernstein_G": str(minrec["G"])}
    else:
        if control == "nc-bump":
            F = sp.expand(F - 10 ** 7 * 64 * t ** 3 * (1 - t) ** 3 * Den)
        verify(poly2(F, t, mu), (fmpq(0), fmpq(1), fmpq(0), Q(lo)), 1, MAX_DEPTH, stats, "F", minrec)
        den2 = poly2(Den, t, mu)
        den_max = max(c for row in den2.bernstein(fmpq(0), fmpq(1), fmpq(0), Q(lo)) for c in row)
        lower = minrec["F"] / den_max
        rec["bound"] = {"min_bernstein_F": str(minrec["F"]), "max_bernstein_Den": str(den_max),
                        "U_lower_bound": str(lower),
                        "U_lower_bound_approx": float(Fraction(int(lower.p), int(lower.q)))}
    rec["bernstein_leaves"] = stats
    return rec


def run(control):
    verify = tampered_prove_sign if control == "td-verifier" else prove_sign
    checks, rec, timing = {}, {"qmax": str(QMAX)}, {}
    ok, res = kats(verify)
    checks["KAT"] = (ok, str(res))
    U = U_TARGET + (x ** 2 * m * (1 + m * d) if control == "td-coeff" else 0)
    e0u, e0h = sp.expand(U_minus(4) - U), sp.expand(H_minus(4) - H_TARGET)
    checks["E0"] = (e0u == 0 and e0h == 0, f"S5 (5.63b), (5.62b) at n = 4 minus TARGET.md's U_-, H_-: {e0u}, {e0h}")
    hpos = all(c > 0 for _, c in sp.Poly(H_TARGET, x, d, m).terms())
    checks["H"] = (hpos, "H_- = m + 10 x + 10 m delta x: every coefficient > 0, so H_- >= m > 0")
    ells = {"nc-ell2": [2], "nc-strict": [3], "nc-bump": [4]}.get(control, list(ELLS))
    rec["parts"] = []
    for ell in ells:
        t0 = time.time()
        try:
            r = part(verify, ell, U, control)
            checks[f"E l={ell}"] = (True, f"U_- >= 0 on [0, x_H] for q in [q(mu_lo), 1]: {r['bound']}")
        except CertificateError as exc:
            r = {"ell": ell, "failure": str(exc)[:600]}
            checks[f"E l={ell}"] = (False, str(exc)[:600])
        rec["parts"].append(r)
        timing[f"l={ell}"] = round(time.time() - t0, 2)
    return checks, rec, timing


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--control", choices=CONTROLS, default="none")
    a = ap.parse_args(argv)
    t0, start = time.time(), datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    record = {"claim": "results/a2/elementary/PREREG.md (A2-E: l = 3..10)", "control": a.control,
              "provenance": provenance(), "archive_sha256": os.environ.get("BHM_ARCHIVE", "unknown")}
    timing = {}
    try:
        checks, rec, timing = run(a.control)
        record.update(rec)
        record["checks"] = {k: {"ok": bool(ok), "detail": det} for k, (ok, det) in checks.items()}
        failed = [k for k, (ok, _) in checks.items() if not ok]
        verdict = "VERIFIED" if not failed else "REJECT: " + ", ".join(failed)
    except Exception as exc:  # noqa: BLE001  (fail-closed)
        verdict = f"REJECT: exception {type(exc).__name__}: {exc}"
    record["verdict"] = verdict
    record["timing"] = {**timing, "utc_start": start, "t_total_s": round(time.time() - t0, 2)}
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
