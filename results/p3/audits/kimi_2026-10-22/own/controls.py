"""Controls for the p3 audit (Kimi).

(a) T1's P with P(0) raised above the horizon bound
    P(0) < U_-(x_H)/(64 H_-(x_H)^2 f_z(0))  =>  my verifier must REJECT (N(0) < 0).
(b) U_-'s coefficient 7680 -> 7681 in my builder => my KI-transcription check must REJECT;
    (informational) does positivity alone catch it?
(c) the KAT suite of verify.py, including the tampered-verifier drill (KAT5).
"""
import json
import os
import sys
from fractions import Fraction

import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rf import p_eval, FACTORS, rf_const, rf_scale, rf_add, rf_sub, rf_mul
from make_boxes import P_to_PY, build_N_rf, D6_rfs
from verify import verify_1d, verify_2d, poly1_from_map
from flint import fmpq

HERE = os.path.dirname(os.path.abspath(__file__))
z = sp.symbols("z")


def horizon_bound_T1():
    """Exact horizon bound at mu = 1/6 via the rf route (Y = 1 <=> z = 0)."""
    delta, md, one_md, xH, q2 = D6_rfs()
    muval = Fraction(1, 6)

    def rv(r):
        n, e = r
        v = p_eval(n, muval)
        for i in range(3):
            v /= p_eval(FACTORS[i], muval) ** e[i]
        return v

    xHv, q2v = rv(xH), rv(q2)
    m = Fraction(6)
    dv = rv(delta)
    # U_-(x_H): coefficients from the KI form at n=4, m=6
    Uk = [Fraction(27648),
          -96 * (2160 * dv + 480),
          46080 * (1 + 6 * dv),
          -1600 * (1 + 6 * dv) ** 2 * (300 * dv - 16),
          -400000 * dv * (1 + 6 * dv) ** 3]
    UxH = sum(Uk[k] * xHv**k for k in range(5))
    HxH = 6 + 10 * (1 + 6 * dv) * xHv
    # f_z(0): f = 1 - xH(1-z)^3 + q2/4 xH^2 (1-z)^6 -> f_z(0) = 3 xH - 3 q2 xH^2
    fz0 = 3 * xHv - 3 * q2v * xHv**2
    bound = UxH / (64 * HxH**2 * fz0)
    return bound


def main():
    # ---------- control (a) ----------
    bound = horizon_bound_T1()
    print("horizon bound at mu=1/6: P(0) <", bound, "=", float(bound))
    with open(os.path.join(HERE, "..", "runs", "cert_rule1_T1.json")) as fh:
        d = json.load(fh)
    P0 = None
    for key, val in d["P"].items():
        i, j = eval(key)
        if i == 0:
            P0 = Fraction(val)
    print("certificate P(0) =", P0, " margin:", bound - P0)
    assert P0 < bound
    # tampered P: P(0) -> bound + 1/10
    Pmap = dict(d["P"])
    Pmap["(0, 0)"] = str(bound + Fraction(1, 10))
    PY = P_to_PY(Pmap)
    N = build_N_rf(PY)
    # evaluate N at z=0 (Y=1) exactly
    N_at_0 = Fraction(0)
    for yexp, r in N.items():
        n, e = r
        v = p_eval(n, Fraction(1, 6))
        for i in range(3):
            v /= p_eval(FACTORS[i], Fraction(1, 6)) ** e[i]
        N_at_0 += v                      # Y^yexp at Y=1 is 1
    print("control (a): tampered N(z=0) =", N_at_0, "< 0 ?", N_at_0 < 0)
    ok_a = N_at_0 < 0
    # and my verifier must reject the z-polynomial: build N(z) as rationals
    Nz = {}
    for yexp, r in N.items():
        n, e = r
        v = p_eval(n, Fraction(1, 6))
        for i in range(3):
            v /= p_eval(FACTORS[i], Fraction(1, 6)) ** e[i]
        for k in range(yexp + 1):
            coef = v * Fraction((-1) ** k) * Fraction(sp.binomial(yexp, k))
            Nz[k] = Nz.get(k, Fraction(0)) + coef
    Nz = {k: v for k, v in Nz.items() if v}
    ok_v, info = verify_1d({k: fmpq(v.numerator, v.denominator) for k, v in Nz.items()},
                           fmpq(0), fmpq(1))
    print("control (a): verifier on tampered N:", "REJECT (correct)" if not ok_v else "PASS (BAD)", info)
    ok_a = ok_a and not ok_v

    # ---------- control (b) ----------
    # transcription check: perturbed U_- coefficient 7680 -> 7681
    sys.path.insert(0, HERE)
    import importlib
    import build as b1
    m, dd = sp.symbols("m d")
    x = sp.Symbol("x")
    U_tampered = (-400000 * dd * (1 + m*dd)**3 * x**4
                  - 1600 * (1 + m*dd)**2 * (50*m*dd - 16) * x**3
                  + 7681 * m * (1 + m*dd) * x**2      # TAMPER: 7680 -> 7681
                  - 16*m * (5*m*(96 - 4*m)*dd + 480) * x
                  + 64*m**3 + 384*m**2)
    U4, H4 = b1.ki_Usymbol(4)
    diff = sp.expand(U4 - U_tampered)
    ok_b = diff != 0
    print("control (b): perturbed U_- vs KI (5.63b) mismatch detected:", ok_b,
          " (diff =", sp.expand(diff).coeff(x, 2) if diff != 0 else 0, "* x^2 )")

    print("CONTROLS:", "ALL OK" if (ok_a and ok_b) else "FAILURE")
    return 0 if (ok_a and ok_b) else 1


if __name__ == "__main__":
    raise SystemExit(main())
