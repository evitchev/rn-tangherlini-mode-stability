"""Exact onset of the negative region of V_S- for D = 6 (results/onset/PREREG.md).

    python -m onset.onset --out DIR [--control NAME]

Rational parametrisation of the charge, for l >= 2, m = (l - 1)(l + 4) and mu in [0, 1]:
    A(mu) = (l + 4) + (l - 1) mu^2,
    w = sqrt(1 - q^2) = (2l + 3) mu / A,     s = 1 + 2 m delta = (2l + 3)((l + 4) - (l - 1) mu^2) / (5A),
so that s^2 = 1 + 4 m q^2/25 exactly; mu = 1 is q = 0 and mu = 0 is q = 1, monotonically.
With x = t x_H, x_H = 2/(1 + w) and t in [0, 1], U_-(x; delta) = F(t, mu)/Den(mu) with F a
polynomial with integer coefficients and Den > 0 on [0, 1].  g(mu) := F(1, mu) is U_- at the
horizon.  Every check is exact (sympy / python-flint fmpq, fmpz_poly); verdict VERIFIED and exit
0 only if all of O1-O5 hold, otherwise REJECT: <reasons> and exit 1.
"""
import argparse
import sys
import time
from fractions import Fraction

import sympy as sp
from flint import arb, ctx, fmpq, fmpz_poly

from ki.potentials import U_TARGET, U_minus, d, m, x
from onset.bernstein import Poly2, Q, prove_sign
from qnm1c.common import CertificateError, dump_json, provenance

t, mu, Y = sp.symbols("t mu Y")
CONTROLS = ("none", "nc-o1", "nc-o2", "pc-o1", "td-o1", "td-o2")
Q_PRED = (Fraction("0.9730564367"), Fraction("0.9730564368"))     # registered prediction for q_*


def param(ell):
    L = sp.Integer(ell)
    A = (L + 4) + (L - 1) * mu**2
    w = (2 * L + 3) * mu / A
    s = (2 * L + 3) * ((L + 4) - (L - 1) * mu**2) / (5 * A)
    mm = (L - 1) * (L + 4)
    return {"A": A, "w": w, "s": s, "m": mm, "delta": sp.cancel((s - 1) / (2 * mm)),
            "xH": sp.cancel(2 / (1 + w)), "q2": sp.cancel(1 - w**2)}


def positive_on_unit(poly_mu, a=0, b=1):
    """Exact: the univariate polynomial is > 0 on [a, b] (Bernstein, adaptive)."""
    p2 = Poly2({(0, j): Q(c) for (j,), c in sp.Poly(poly_mu, mu).terms()})
    prove_sign(p2, (fmpq(0), fmpq(1), Q(a), Q(b)), 1, 30, {}, "univariate")
    return True


def build(ell, U):
    P = param(ell)
    expr = U.subs({m: P["m"], d: P["delta"]}).subs(x, t * P["xH"])
    num, den = sp.fraction(sp.together(sp.expand(expr)))
    num, den = sp.expand(num), sp.expand(den)
    if den.has(t):
        raise CertificateError("denominator depends on t")
    sign = 1 if sp.Poly(den, mu).eval(sp.Rational(1, 2)) > 0 else -1
    F = sp.Poly(sign * num, t, mu)
    return P, F, sign * den


def to_poly2(F):
    return Poly2({(i, j): Q(c) for (i, j), c in F.terms()})


def q_of(P, muv):
    """q(mu)^2 as an exact rational."""
    return Fraction(str(sp.Rational(P["q2"].subs(mu, muv))))


def run(control):
    rec, checks = {}, {}
    U = U_TARGET + (x**2 * m * (1 + m * d) if control == "td-o1" else 0)
    ell = 3 if control == "pc-o1" else 2

    # O5: transcription and parametrisation
    e0 = sp.expand(U_minus(4) - U)
    checks["E0"] = (e0 == 0, f"S5 (5.63b) at n = 4 minus TARGET.md's U_-: {e0}")
    P, F, Den = build(ell, U)
    o5 = [sp.cancel(P["s"]**2 - (1 + 4 * P["m"] * P["q2"] / 25)) == 0,
          positive_on_unit(sp.numer(sp.cancel(sp.diff(P["w"], mu)))),        # w increasing
          positive_on_unit(Den),                                                # Den > 0
          sp.cancel(P["q2"].subs(mu, 1)) == 0, sp.cancel(P["q2"].subs(mu, 0)) == 1]
    checks["O5"] = (all(o5), f"s^2 = 1 + 4mq^2/25, w increasing, Den > 0 on [0,1], q(1) = 0, q(0) = 1: {o5}")
    rec["F_degrees"] = [F.degree(t), F.degree(mu)]
    F2 = to_poly2(F)

    if control == "pc-o1":                       # l = 3, q <= q(1/30) ~ 0.99908: F > 0 everywhere
        stats = {}
        prove_sign(F2, (fmpq(0), fmpq(1), fmpq(1, 30), fmpq(1)), 1, 40, stats, "PC-O1")
        checks["PC-O1"] = (True, f"l = 3: U_- > 0 on the exterior for q <= q(1/30)^(1/2) = "
                                 f"{float(q_of(P, sp.Rational(1, 30))) ** 0.5:.6f}; boxes {stats}")
        return checks, rec

    # O1: the onset as an algebraic number
    g = sp.Poly(F.as_expr().subs(t, 1), mu)
    g0, g1 = g.eval(0), g.eval(1)
    nroots = g.count_roots(0, 1)
    ivs = g.intervals(eps=sp.Rational(1, 10**45), inf=0, sup=1)
    ok1 = (g0 < 0 < g1 and nroots == 1 and len(ivs) == 1 and ivs[0][1] == 1)
    (a, b), _ = ivs[0] if ivs else ((sp.Integer(0), sp.Integer(0)), 0)
    if control == "nc-o1":                       # false claim: the onset lies in mu in [0.20, 0.21]
        a, b = sp.Rational(20, 100), sp.Rational(21, 100)
        ok1 = ok1 and g.count_roots(a, b) == 1
    qa2, qb2 = q_of(P, a), q_of(P, b)            # q decreasing in mu: q(b) <= q_* <= q(a)
    in_pred = (qb2 >= Q_PRED[0] ** 2 and qa2 <= Q_PRED[1] ** 2)
    facs = [fa for fa, _ in sp.factor_list(g.as_expr())[1]]
    pmin = [fa for fa in facs if sp.Poly(fa, mu).eval(a) * sp.Poly(fa, mu).eval(b) < 0]
    flint_roots = [rt for rt, mult in fmpz_poly([int(c) for c in reversed(sp.Poly(pmin[0], mu).all_coeffs())]
                                                ).complex_roots() if rt.imag == 0] if pmin else []
    in01 = [rt for rt in flint_roots if rt.real > 0 and rt.real < 1]
    flint_ok = len(in01) == 1 and in01[0].real.overlaps(arb(Q(a)).union(arb(Q(b))))
    PY = sp.Poly(sp.resultant(sp.Poly(pmin[0], mu).as_expr(),
                              P["A"] ** 2 * Y - (P["A"] ** 2 - (2 * ell + 3) ** 2 * mu**2), mu), Y) if pmin else None
    yfacs = [fa for fa, _ in sp.factor_list(PY.as_expr())[1]] if PY is not None else []
    yb, ya = sp.Rational(qb2.numerator, qb2.denominator), sp.Rational(qa2.numerator, qa2.denominator)
    ymin = [fa for fa in yfacs if sp.Poly(fa, Y).eval(yb) * sp.Poly(fa, Y).eval(ya) <= 0]
    checks["O1"] = (ok1 and in_pred and len(pmin) == 1 and flint_ok and len(ymin) == 1,
                    f"g(0) = {g0} < 0 < g(1) = {g1}; roots of g in [0,1]: {nroots}; isolating interval "
                    f"width {float(b - a):.1e}; q_* in prediction {in_pred}; one irreducible factor "
                    f"vanishing there: {len(pmin) == 1}; Arb isolation agrees: {flint_ok}; "
                    f"minimal polynomial of q_*^2 found: {len(ymin) == 1}")
    ctx.prec = 200
    qlo = arb(Q(qb2)).sqrt()
    qhi = arb(Q(qa2)).sqrt()
    rec.update({"g_coeffs": [str(c) for c in g.all_coeffs()], "g_degree": g.degree(),
                "mu_star_interval": [str(a), str(b)],
                "q_star_squared_interval": [str(qb2), str(qa2)],
                "q_star_decimal": [qlo.str(45, radius=False), qhi.str(45, radius=False)],
                "minimal_poly_mu": str(pmin[0]) if pmin else None,
                "minimal_poly_q2": str(ymin[0]) if ymin else None})

    # O3: below the onset in mu (q above q_*), U_-(x_H) < 0  <=>  g < 0 on [0, mu_*)
    checks["O3"] = (ok1, "g < 0 on [0, mu_*) and > 0 on (mu_*, 1]: one simple root in [0, 1] and the "
                         "end signs (O1)")

    # O2: positivity for mu in [mu_*, 1] (q in [0, q_*]), with the corner lemma at (t, mu) = (1, mu_*).
    # The split (tau, mu_c) is an implementation parameter: each attempt that succeeds is a proof.
    alo = Q(a)
    if control == "nc-o2":                       # false claim: positivity up to q = 0.975 (mu = 0.191)
        alo = fmpq(191, 1000)
        prove_sign(F2, (fmpq(0), fmpq(1), alo, fmpq(1)), 1, 40, {}, "NC-O2")
    dF = Poly2({(i - 1, j): c * i for (i, j), c in F2.terms.items() if i >= 1})
    failures = []
    for k in range(4):
        tau, muc = fmpq(1, 8 * 2**k), Q(b) + fmpq(1, 64 * 2**k)
        stats = {}
        try:
            prove_sign(F2, (fmpq(0), 1 - tau, alo, fmpq(1)), 1, 40, stats, "O2 far from the horizon")
            prove_sign(F2, (1 - tau, fmpq(1), muc, fmpq(1)), 1, 40, stats, "O2 near the horizon, mu >= mu_c")
            prove_sign(dF, (1 - tau, fmpq(1), alo, muc), 1 if control == "td-o2" else -1, 40, stats,
                       "O2 corner: dF/dt < 0")
            break
        except CertificateError as exc:
            failures.append(f"tau = {tau}: {exc}")
            if control == "td-o2":
                raise
    else:
        raise CertificateError("O2 not proved for any split: " + " | ".join(failures))
    rec["O2_split"] = {"tau": str(tau), "mu_c": str(muc), "earlier_attempts": failures}
    checks["O2"] = (True, f"F > 0 on [0, 1 - tau] x [mu_lo, 1] and on [1 - tau, 1] x [mu_c, 1]; "
                          f"dF/dt < 0 on [1 - tau, 1] x [mu_lo, mu_c] (tau = {tau}, mu_c = mu_hi + {muc - Q(b)}); "
                          f"so U_- >= 0 on the exterior for q <= q_*, = 0 only at (q_*, x_H). "
                          f"Bernstein boxes: {stats}")

    # O4: range of S5 (6.24) for l = 2: b(x_H) = 2m - 10 (1 + m delta) x_H, root exactly at mu = 3/4 (q = 3/5)
    bk = sp.cancel(2 * P["m"] - 10 * (1 + P["m"] * P["delta"]) * P["xH"])
    bn, bd = sp.fraction(bk)
    bp = sp.Poly(bn * (1 if sp.Poly(bd, mu).eval(sp.Rational(1, 2)) > 0 else -1), mu)
    o4 = [bp.eval(sp.Rational(3, 4)) == 0, bp.count_roots(0, 1) == 1, bp.eval(0) < 0 < bp.eval(1),
          positive_on_unit(bd * (1 if sp.Poly(bd, mu).eval(sp.Rational(1, 2)) > 0 else -1)),
          sp.Rational(P["q2"].subs(mu, sp.Rational(3, 4))) == sp.Rational(9, 25)]
    checks["O4"] = (all(o4), f"(6.24) bracket at the horizon vanishes only at mu = 3/4 (q = 3/5), "
                             f"> 0 for q < 3/5, < 0 for q > 3/5: {o4}")
    return checks, rec


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--control", choices=CONTROLS, default="none")
    a = ap.parse_args(argv)
    t0 = time.time()
    record = {"claim": "results/onset/PREREG.md, O1-O5", "control": a.control, "provenance": provenance()}
    try:
        checks, rec = run(a.control)
        record.update(rec)
        record["checks"] = {k: {"ok": bool(ok), "detail": det} for k, (ok, det) in checks.items()}
        failed = [k for k, (ok, _) in checks.items() if not ok]
        verdict = "VERIFIED" if not failed else "REJECT: " + ", ".join(failed)
    except CertificateError as exc:
        verdict = f"REJECT: {exc}"
    except Exception as exc:  # noqa: BLE001  (fail-closed)
        verdict = f"REJECT: exception {type(exc).__name__}: {exc}"
    record["verdict"] = verdict
    record["timing"] = {"t_total_s": round(time.time() - t0, 2)}
    dump_json(record, f"{a.out}/result.json")
    for k, v in record.get("checks", {}).items():
        print(f"{k}: {'PASS' if v['ok'] else 'FAIL'}  {v['detail']}")
    for k in ("q_star_decimal", "mu_star_interval", "minimal_poly_mu", "minimal_poly_q2"):
        if k in record:
            print(f"{k}: {record[k]}")
    print(verdict)
    return 0 if verdict == "VERIFIED" else 1


if __name__ == "__main__":
    sys.exit(main())
