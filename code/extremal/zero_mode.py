"""Stage 3, item Z, and [another line of this project] (b'): the extremal zero mode of the scalar-type master equation, and its Darboux partner
(results/extremal/PREREG.md).

    python -m extremal.zero_mode --out DIR --n {2..9|N} [--control NAME]

D = n + 2, K = 1, Lambda = 0, q = 1, r_H = 1.  Put Y = rho^-(n-1), so x = 2Y and f = (1 - Y)^2.  At q = 1, S5 (5.58)
gives m = (l - 1)(l + n) and delta = 1/((l + n)(n + 1)), on the branch 1 + 2 m delta > 0.  The omega = 0 master
equation is (f u')' = (W/rho^2) u with W = U_-/(64 H_-^2), i.e. V = f W/rho^2.

The candidate (planning data, results/planning/stage3_2026-10-25/) is
    u0 = rho^-nu (1 - Y)^-alpha / h,   nu = l + n/2 - 1,   alpha = l/(n - 1),   h = (l - 1) + n Y.
With g = rho u0'/u0 = -nu - (n - 1) alpha Y/(1 - Y) + n (n - 1) Y/h, rational in (Y, l[, n]), the equation is
    Z-id:  2(n-1) Y (1-Y) g + (1-Y)^2 (g^2 - g - (n-1) Y g_Y) = W.
In the tortoise variable the superpotential is w = f g/rho, V = w^2 + w', and the Darboux partner is
    Vt = w^2 - w' = f Ut/rho^2,   Ut = (1-Y)^2 (g^2 + g + (n-1) Y g_Y) - 2(n-1) Y (1-Y) g.

Checks, in this order (PREREG section 2):
    q1     (n+1)^2 delta (1 + m delta) = 1 and 1 + 2 m delta = (2l + n - 1)/(n + 1): the extremal point of (5.58)
    H      H_-(x = 2Y) = (l + n) h, so u0 = rho^-nu (1 - Y)^-alpha (l + n)/H_-
    Z-pos  h has positive coefficients in (t, Y) at l = 2 + t (and n = 2 + s when n is symbolic): h >= 1 on the exterior
    Z-inf  W(0) = nu (nu + 1): the decaying exponent at infinity
    Z-thr  alpha (alpha - 1) (n - 1)^2 = W(1): u0's exponent solves the throat's indicial equation
    Z-id   the identity above, exact
    P-reg  Ut has no pole at the zeros of h, i.e. of H_- (computed only when Z-id holds; otherwise failed)
    P-asym Ut(0) = nu (nu - 1) and Ut(1) = l (l + n - 1) (computed only when Z-id holds)
--control (registered verdicts in PREREG section 3):
    nc-nu     nu + 1 in the candidate
    nc-exp    alpha = (l + 1)/(n - 1) in the candidate
    td-U      U_- + 64 m^2, the transcription tampered
    td-zid    the identity's first term with 1 in place of 2, the code path tampered
    td-preg   Ut computed with the signs of V, the partner's code path tampered
Fail-closed (RULES.md A2): VERIFIED and exit 0 only if every check holds; otherwise REJECT: <failed checks>, exit 1.
"""
import argparse
import datetime
import os
import sys
import time

import sympy as sp

from ki.potentials import d, m, x
from kimaster.master import NSYM, master
from qnm1c.common import CertificateError, dump_json, provenance

Y, ELL, T, S = sp.symbols("Y ell t s")
CONTROLS = ("none", "nc-nu", "nc-exp", "td-U", "td-zid", "td-preg")
ORDER = ("q1", "H", "Z-pos", "Z-inf", "Z-thr", "Z-id", "P-reg", "P-asym")


def show(e):
    return str(sp.factor(e))


def big(e, n):
    """A large expression as a string: factored for an integer n, as it stands for n symbolic."""
    return str(e) if n == "N" else show(e)


def nn_of(n):
    return NSYM if n == "N" else sp.Integer(n)


def candidate(n, control):
    """(g, nu, alpha, h) of u0, with the control's change applied."""
    nn = nn_of(n)
    nu = ELL + nn / 2 - 1 + (1 if control == "nc-nu" else 0)
    alpha = (ELL + (1 if control == "nc-exp" else 0)) / (nn - 1)
    h = (ELL - 1) + nn * Y
    g = -nu - (nn - 1) * alpha * Y / (1 - Y) + nn * (nn - 1) * Y / h
    return g, nu, alpha, h


def extremal_md(nn, ell):
    return (ell - 1) * (ell + nn), 1 / ((ell + nn) * (nn + 1))


def potential_W(n, control, UH):
    """W(Y) = U_-/(64 H_-^2) at q = 1, x = 2Y; and H_-(Y) there."""
    nn = nn_of(n)
    U, H = UH(n, "minus")
    if control == "td-U":
        U = U + 64 * m ** 2
    mm, dl = extremal_md(nn, ELL)
    sub = {m: mm, d: dl, x: 2 * Y}
    return sp.cancel(sp.together(U.subs(sub) / (64 * H.subs(sub) ** 2))), sp.cancel(H.subs(sub))


def lhs(n, g, control):
    nn = nn_of(n)
    two = 1 if control == "td-zid" else 2
    gY = sp.diff(g, Y)
    return two * (nn - 1) * Y * (1 - Y) * g + (1 - Y) ** 2 * (g ** 2 - g - (nn - 1) * Y * gY)


def partner(n, g, control):
    nn = nn_of(n)
    gY = sp.diff(g, Y)
    if control == "td-preg":
        return sp.cancel(sp.together(lhs(n, g, "none")))
    return sp.cancel(sp.together((1 - Y) ** 2 * (g ** 2 + g + (nn - 1) * Y * gY) - 2 * (nn - 1) * Y * (1 - Y) * g))


def positive_coeffs(expr, gens):
    p = sp.Poly(sp.expand(expr), *gens)
    return all(c > 0 for c in p.coeffs()), str(p.as_expr())


def classify(n):
    """For integer n: in each band l = 2..n-2, is u0 throat-principal?  The throat exponents in s are
    1/2 +- |2l - n + 1|/(2(n - 1)); u0's is alpha = l/(n - 1)."""
    out = {}
    for ell in range(2, n - 1):
        a = sp.Rational(ell, n - 1)
        lo = sp.Rational(1, 2) - sp.Abs(sp.Rational(2 * ell - n + 1, 2 * (n - 1)))
        out[f"l={ell}"] = {"alpha": str(a), "alpha_minus": str(lo), "throat_principal": bool(a == lo),
                           "2l<=n-1": 2 * ell <= n - 1}
    return out


def run_case(n, control, UH=master, cand=candidate):
    nn = nn_of(n)
    g, nu, alpha, h = cand(n, control)
    W, Hq = potential_W(n, control, UH)
    mm, dl = extremal_md(nn, ELL)
    checks, facts = {}, {}
    q2 = sp.cancel((nn + 1) ** 2 * dl * (1 + mm * dl))
    br = sp.cancel(1 + 2 * mm * dl - (2 * ELL + nn - 1) / (nn + 1))
    checks["q1"] = (q2 == 1 and br == 0, f"(n+1)^2 delta (1 + m delta) = {show(q2)}; 1 + 2 m delta - (2l+n-1)/(n+1) = {br}")
    hd = sp.cancel(Hq - (ELL + nn) * h)
    checks["H"] = (hd == 0, f"H_-(2Y) - (l + n) h = {show(hd)}")
    sub = {ELL: 2 + T}
    gens = [T, Y]
    if n == "N":
        sub[NSYM] = 2 + S
        gens = [T, S, Y]
    ok, hs = positive_coeffs(h.subs(sub), gens)
    checks["Z-pos"] = (ok, f"h at l = 2 + t{', n = 2 + s' if n == 'N' else ''}: {hs}")
    W0, W1 = sp.cancel(W.subs(Y, 0)), sp.cancel(W.subs(Y, 1))
    inf = sp.cancel(W0 - nu * (nu + 1))
    checks["Z-inf"] = (inf == 0, f"W(0) - nu (nu + 1) = {show(inf)}")
    thr = sp.cancel(alpha * (alpha - 1) * (nn - 1) ** 2 - W1)
    checks["Z-thr"] = (thr == 0, f"alpha (alpha - 1) (n-1)^2 - W(1) = {show(thr)}; W(1) = {show(W1)}")
    zid = sp.cancel(sp.together(lhs(n, g, control) - W))
    checks["Z-id"] = (zid == 0, "identity residual " + ("0" if zid == 0 else "nonzero: " + str(sp.factor(zid))[:300]))
    if zid == 0:
        Ut = partner(n, g, control)
        den = sp.fraction(Ut)[1]
        y0 = sp.solve(h, Y)[0]
        at0 = sp.cancel(den.subs(Y, y0))
        checks["P-reg"] = (at0 != 0, f"denominator of Ut: {show(den)}; at the zero Y0 = {y0} of h: {show(at0)}")
        a0, a1 = sp.cancel(Ut.subs(Y, 0) - nu * (nu - 1)), sp.cancel(Ut.subs(Y, 1) - ELL * (ELL + nn - 1))
        checks["P-asym"] = (a0 == 0 and a1 == 0, f"Ut(0) - nu (nu - 1) = {show(a0)}; Ut(1) - l (l + n - 1) = {show(a1)}")
        facts["Ut"] = big(Ut, n)
        facts["Ut_polynomial_in_Y"] = sp.Poly(den, Y).degree() == 0
        if control == "none":
            facts["comparisons"] = compare(n, Ut, UH)
    else:
        checks["P-reg"] = (False, "not computed: Z-id failed")
        checks["P-asym"] = (False, "not computed: Z-id failed")
    facts["W"] = big(W, n)
    if n != "N":
        facts["throat_classification"] = classify(int(n))
    return checks, facts


def compare(n, Ut, UH):
    """Information: is the partner another sector's potential at q = 1?  Ut against W_+ at the same l, and W_- at l -+ 1."""
    nn = nn_of(n)
    out = {}
    Up, Hp = UH(n, "plus")
    mm, dl = extremal_md(nn, ELL)
    sub = {m: mm, d: dl, x: 2 * Y}
    Wp = sp.cancel(sp.together(Up.subs(sub) / (64 * Hp.subs(sub) ** 2)))
    out["Ut == W_plus(l)"] = sp.cancel(Ut - Wp) == 0
    U, H = UH(n, "minus")
    for k in (-1, 1):
        mk, dk = extremal_md(nn, ELL + k)
        sk = {m: mk, d: dk, x: 2 * Y}
        Wk = sp.cancel(sp.together(U.subs(sk) / (64 * H.subs(sk) ** 2)))
        out[f"Ut == W_minus(l{k:+d})"] = sp.cancel(Ut - Wk) == 0
    return out


def main(argv=None, UH=master, cand=candidate):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", required=True)
    ap.add_argument("--control", choices=CONTROLS, default="none")
    a = ap.parse_args(argv)
    t0, start = time.time(), datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    record = {"claim": "results/extremal/PREREG.md: Z, the extremal zero mode, and its Darboux partner", "n": a.n,
              "control": a.control, "provenance": provenance(), "archive_sha256": os.environ.get("BHM_ARCHIVE", "unknown")}
    try:
        n = a.n if a.n == "N" else int(a.n)
        if n != "N" and not 2 <= n <= 9:
            raise CertificateError("n outside 2..9")
        checks, facts = run_case(n, a.control, UH, cand)
        record["checks"] = {k: {"ok": bool(checks[k][0]), "detail": checks[k][1]} for k in ORDER}
        record["facts"] = facts
        failed = [k for k in ORDER if not checks[k][0]]
        verdict = "VERIFIED" if not failed else "REJECT: " + ", ".join(failed)
    except Exception as exc:  # noqa: BLE001  (fail-closed: any exception rejects)
        verdict = f"REJECT: exception {type(exc).__name__}: {exc}"
    record["verdict"] = verdict
    record["timing"] = {"utc_start": start, "t_total_s": round(time.time() - t0, 3)}
    os.makedirs(a.out, exist_ok=True)
    dump_json(record, f"{a.out}/result.json")
    for k, v in record.get("checks", {}).items():
        print(f"{k}: {'PASS' if v['ok'] else 'FAIL'}  {v['detail'][:400]}")
    print(verdict)
    return 0 if verdict == "VERIFIED" else 1


if __name__ == "__main__":
    sys.exit(main())
