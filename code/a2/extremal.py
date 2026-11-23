"""Stage A2: the exact extremal checks E0-E5 registered in TARGET_A2.md section 3.

    python -m a2.extremal --out DIR [--ell-max 1000] [--control NAME]

D = 6 (n = 4), K = 1, lambda = 0, q = 1, units M = 1 (so r_H = 1 and x = 2/r^3).
Every check is exact: sympy identities of rational functions in l (E0-E5), and an
independent python-flint fmpq evaluation for l = 2..ell_max (E1, E3, E4), which does not
use sympy.  Fail-closed (RULES.md A2): VERIFIED and exit 0 only if every check holds;
otherwise REJECT: <reasons> and exit 1.

--control selects a negative control or a tamper drill; each must REJECT:
    wrong-branch  delta from 1 + 2 m delta = -(2l+3)/5, the other root of (5.58) at q = 1
    false-claim   the claimed throat coefficient is l(l-3)/9 + 1/100
    tamper-U      the coefficient 7680 of U_- is changed to 7681 on every code path
"""
import argparse
import sys
import time

import sympy as sp
from flint import fmpq

from ki.potentials import H_TARGET, H_minus, U_TARGET, U_minus, d, m, m_of, x
from qnm1c.common import dump_json, provenance

ell, r, rho = sp.symbols("ell r rho")
CONTROLS = ("none", "wrong-branch", "false-claim", "tamper-U")


def symbolic_checks(control):
    """E0-E5 with sympy.  Returns (checks, facts); checks maps name -> (ok, detail)."""
    U = U_TARGET + (x**2 * m * (1 + m * d) if control == "tamper-U" else 0)
    checks, facts = {}, {}

    e0u = sp.expand(U_minus(4) - U)
    e0h = sp.expand(H_minus(4) - H_TARGET)
    checks["E0"] = (e0u == 0 and e0h == 0,
                    f"S5 (5.63b),(5.62b) at n=4 minus TARGET.md forms: U {e0u}, H {e0h}")

    ml = (ell - 1) * (ell + 4)
    sq = (2 * ell + 3) / sp.Integer(5)            # the positive root of (1 + 2 m delta)^2
    branch = -sq if control == "wrong-branch" else sq
    delta1 = sp.cancel((branch - 1) / (2 * ml))
    e1 = [sp.expand(m_of(4, ell) - ml), sp.expand(25 + 4 * ml - (2 * ell + 3) ** 2),
          sp.cancel(delta1 - 1 / (5 * (ell + 4)))]
    checks["E1"] = (all(v == 0 for v in e1), f"m - (l-1)(l+4), 25+4m-(2l+3)^2, delta - 1/(5(l+4)): {e1}")
    facts["delta_q1"] = str(delta1)

    f = (1 - 1 / r**3) ** 2
    e2 = [sp.expand((1 - x + x**2 / 4 - (1 - x / 2) ** 2)), f.subs(r, 1),
          sp.cancel((r - 1) ** 2 / f).subs(r, 1) - sp.Rational(1, 9)]
    checks["E2"] = (all(v == 0 for v in e2), f"f - (1-x/2)^2, f(1), lim (r-1)^2/f - 1/9: {e2}")

    sub = {m: ml, d: delta1}
    U2, H2 = U.subs(sub).subs(x, 2), H_TARGET.subs(sub).subs(x, 2)
    c = sp.factor(sp.cancel(U2 / (576 * H2**2)))
    claim = ell * (ell - 3) / sp.Integer(9) + (sp.Rational(1, 100) if control == "false-claim" else 0)
    e3 = sp.cancel(c - claim)
    checks["E3"] = (e3 == 0, f"c(l) = {c}; c - claimed = {e3}")
    facts["c"] = str(c)
    facts["H_minus_at_horizon"] = str(sp.factor(sp.cancel(H2)))

    e4 = sp.cancel(c + sp.Rational(1, 4) - (2 * ell - 3) ** 2 / sp.Integer(36))
    checks["E4"] = (e4 == 0, f"c + 1/4 - (2l-3)^2/36 = {e4}")

    xr = 2 / r**3
    Ur, Hr = U.subs(sub).subs(x, xr), H_TARGET.subs(sub).subs(x, xr)
    p = sp.cancel((r - 1) * sp.diff(f, r) / f)
    qt = sp.cancel((r - 1) ** 2 * Ur / (64 * r**2 * Hr**2 * f))   # (r-1)^2 V/f^2, V = f U/(64 r^2 H^2)
    p_num, p_den = sp.fraction(p)
    q_num, q_den = sp.fraction(qt)
    den1 = sp.Poly(sp.expand(q_den.subs(r, 1)), ell)
    roots_ok = den1.degree() >= 0 and not den1.is_zero and all(
        hi < 2 for (lo, hi), _ in den1.intervals())                # no zero of the denominator for l >= 2
    p1, q1 = sp.cancel(p.subs(r, 1)), sp.cancel(qt.subs(r, 1))
    indicial = rho**2 + (p1 - 1) * rho - q1
    roots = [(ell - 3) / sp.Integer(3), -ell / sp.Integer(3)]
    e5 = [p_den.subs(r, 1) != 0, roots_ok, sp.cancel(p1 - 2) == 0, sp.cancel(q1 - c) == 0,
          all(sp.cancel(indicial.subs(rho, z)) == 0 for z in roots)]
    checks["E5"] = (all(e5), f"p analytic at 1, (r-1)^2 V/f^2 analytic at 1 for l >= 2, p(1) = 2, "
                             f"q(1) = c, indicial roots (l-3)/3 and -l/3: {e5}; p(1) = {p1}, q(1) = {q1}")
    facts["indicial_roots"] = [str(z) for z in roots]
    facts["margin"] = str(sp.factor(c + sp.Rational(1, 4)))
    return checks, facts


def flint_checks(ell_max, control):
    """E1, E3, E4 for l = 2..ell_max in exact fmpq arithmetic (no sympy on this path)."""
    k7680 = 7681 if control == "tamper-U" else 7680
    for lv in range(2, ell_max + 1):
        mv = fmpq((lv - 1) * (lv + 4))
        if 25 + 4 * mv != (2 * lv + 3) ** 2:
            return False, f"l={lv}: 25 + 4m != (2l+3)^2"
        sq = fmpq(2 * lv + 3, 5) * (-1 if control == "wrong-branch" else 1)
        dv = (sq - 1) / (2 * mv)
        if dv != fmpq(1, 5 * (lv + 4)):
            return False, f"l={lv}: delta = {dv} != 1/(5(l+4))"
        md, xv = mv * dv, fmpq(2)
        U2 = (-400000 * dv * (1 + md) ** 3 * xv**4 - 1600 * (1 + md) ** 2 * (50 * md - 16) * xv**3
              + k7680 * mv * (1 + md) * xv**2 - 16 * mv * (5 * mv * (96 - 4 * mv) * dv + 480) * xv
              + 64 * mv**3 + 384 * mv**2)
        H2 = mv + 10 * (1 + md) * xv
        c = U2 / (576 * H2**2)
        claim = fmpq(lv * (lv - 3), 9) + (fmpq(1, 100) if control == "false-claim" else 0)
        if c != claim:
            return False, f"l={lv}: c = {c} != claimed {claim}"
        if c + fmpq(1, 4) != fmpq((2 * lv - 3) ** 2, 36):
            return False, f"l={lv}: margin != (2l-3)^2/36"
    return True, f"E1, E3, E4 exact for l = 2..{ell_max}"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--ell-max", type=int, default=1000)
    ap.add_argument("--control", choices=CONTROLS, default="none")
    a = ap.parse_args(argv)
    t0 = time.time()
    record = {"claim": "TARGET_A2.md section 3, checks E0-E5", "control": a.control,
              "ell_max": a.ell_max, "provenance": provenance()}
    try:
        checks, facts = symbolic_checks(a.control)
        checks["flint"] = flint_checks(a.ell_max, a.control)
        record["checks"] = {k: {"ok": bool(ok), "detail": det} for k, (ok, det) in checks.items()}
        record["facts"] = facts
        failed = [k for k, (ok, _) in checks.items() if not ok]
        verdict = "VERIFIED" if not failed else "REJECT: " + ", ".join(failed)
    except Exception as exc:  # noqa: BLE001  (fail-closed: any exception rejects)
        verdict = f"REJECT: exception {type(exc).__name__}: {exc}"
    record["verdict"] = verdict
    record["timing"] = {"t_total_s": round(time.time() - t0, 3)}
    dump_json(record, f"{a.out}/result.json")
    for k, v in record.get("checks", {}).items():
        print(f"{k}: {'PASS' if v['ok'] else 'FAIL'}  {v['detail']}")
    print(verdict)
    return 0 if verdict == "VERIFIED" else 1


if __name__ == "__main__":
    sys.exit(main())
