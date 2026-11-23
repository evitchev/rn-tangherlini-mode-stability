"""Build Ntilde(Y, mu) and Den(mu) for the box certificates (Kimi's own route).

Y = 1 - z.  N = U - 64 H^2 [(1-z) f_z P + f(-P + (1-z) P_z + P^2)], with
    X = xH * Y^3,  f = 1 - X + q2 X^2 / 4,  (1-z) f_z = 3X - 3 q2 X^2,
    (1-z) P_z = -Y P_Y.
All in exact QQ(mu) arithmetic (rf.py).  Output: own/built/<name>_box<k>.json
with Den (factored exponent form + expanded polynomial) and Ntilde {(i,j): coeff}.
"""
import json
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rf import (rf_const, rf_mul, rf_add, rf_sub, rf_neg, rf_scale,
                y_add, y_mul, y_scale_rf, y_neg, y_negYPY,
                common_den, den_poly, clear)

HERE = os.path.dirname(os.path.abspath(__file__))
CERTS = os.path.join(HERE, "..", "runs")
OUT = os.path.join(HERE, "built")
os.makedirs(OUT, exist_ok=True)


def D6_rfs():
    """The rf building blocks for D = 6, ell = 2 (m = 6)."""
    one = rf_const(1)
    delta = ({0: Fraction(1, 5), 2: Fraction(-1, 5)}, (1, 0, 0))     # (1-mu^2)/(5(6+mu^2))
    md = rf_scale(delta, 6)
    one_md = rf_add(one, md)                                          # 1 + m delta
    xH = ({0: Fraction(12), 2: Fraction(2)}, (0, 1, 1))              # 2(6+mu^2)/((mu+1)(mu+6))
    q2 = ({0: Fraction(36), 2: Fraction(-37), 4: Fraction(1)}, (2, 0, 0))
    return delta, md, one_md, xH, q2


def build_N_rf(PY):
    """PY: P as a Y-dict of rf.  Returns N as a Y-dict of rf."""
    delta, md, one_md, xH, q2 = D6_rfs()
    # U = sum_k Uk X^k with X = xH Y^3 (KI (5.63b) at n = 4, m = 6)
    U0 = rf_const(27648)                       # 64 m^3 + 384 m^2
    U1 = rf_scale(rf_add(rf_scale(delta, 2160), rf_const(480)), -96)   # -16m(5m(96-4m)d + 480)
    U2 = rf_scale(one_md, 46080)               # 7680 m (1 + m d)
    U3 = rf_scale(rf_mul(rf_mul(one_md, one_md),
                         rf_sub(rf_scale(delta, 300), rf_const(16))), -1600)  # -1600(1+md)^2(50md-16)
    U4 = rf_scale(rf_mul(delta, rf_mul(rf_mul(one_md, one_md), one_md)), -400000)
    Uk = [U0, U1, U2, U3, U4]
    xHk = [rf_const(1)]
    for _ in range(4):
        xHk.append(rf_mul(xHk[-1], xH))
    U = {}
    for k in range(5):
        U = y_add(U, {3 * k: rf_mul(Uk[k], xHk[k])})
    # H = m + 10 (1 + m d) X
    H = {0: rf_const(6), 3: rf_scale(rf_mul(one_md, xH), 10)}
    H2 = y_mul(H, H)
    # f = 1 - X + q2 X^2 / 4
    f = {0: rf_const(1), 3: rf_neg(xH), 6: rf_mul(rf_scale(rf_mul(xH, xH), Fraction(1, 4)), q2)}
    # (1 - z) f_z = 3X - (3/2) q2 X^2   [f = 1 - X + q2 X^2/4, X = xH Y^3, Y = 1-z]
    fz1 = {3: rf_scale(xH, 3), 6: rf_scale(rf_mul(q2, rf_mul(xH, xH)), Fraction(-3, 2))}
    nYPY = y_negYPY(PY)
    P2 = y_mul(PY, PY)
    bracket_inner = y_add(y_neg(PY), y_add(nYPY, P2))     # -P + (1-z) P_z + P^2
    B = y_add(y_mul(fz1, PY), y_mul(f, bracket_inner))
    return y_add(U, y_scale_rf(y_mul(H2, B), Fraction(-64)))


def P_to_PY(Pmap):
    """Certificate map "(i, j)" -> coeff of z^i mu^j  ==>  Y-dict of rf (Y = 1-z)."""
    Pz = {}
    for key, val in Pmap.items():
        i, j = eval(key)
        Pz.setdefault(i, {})[j] = Fraction(val)
    base = {0: rf_const(1), 1: rf_const(-1)}   # 1 - Y
    PY = {}
    for i, mupart in Pz.items():
        crf = ({jj: c for jj, c in mupart.items()}, (0, 0, 0))
        p = {0: rf_const(1)}
        for _ in range(i):
            p = y_mul(p, base)
        PY = y_add(PY, y_scale_rf(p, crf))
    return PY


def to_sparse_2d(Ntilde):
    out = {}
    for i, numpoly in Ntilde.items():
        for j, c in numpoly.items():
            if c:
                out[f"({i}, {j})"] = str(c)
    return out


def main():
    for name, src in [
        ("T2_rule1", "cert_rule1_T2.json"),
        ("T3_rule1", "cert_rule1_T3.json"),
        ("T2_rule2", "cert_rule2_T2.json"),
    ]:
        with open(os.path.join(CERTS, src)) as fh:
            d = json.load(fh)
        for k, box in enumerate(d["boxes_mu"]):
            mua, mub = box["mu"]
            PY = P_to_PY(box["P"])
            N = build_N_rf(PY)
            E = common_den(N)
            Den = den_poly(E)
            Ntilde = clear(N, E)
            payload = {
                "kind": "Y_mu", "Y_meaning": "1-z", "mu_box": [mua, mub],
                "Den_exps": list(E),
                "Den": {str(kk): str(vv) for kk, vv in Den.items()},
                "deg_Y": max(Ntilde),
                "deg_mu": max(max(pp) for pp in Ntilde.values()),
                "Ntilde": to_sparse_2d(Ntilde),
            }
            outp = os.path.join(OUT, f"{name}_box{k}.json")
            with open(outp, "w") as fh:
                json.dump(payload, fh)
            print(f"{name} box{k}: mu in [{mua},{mub}] deg_Y={payload['deg_Y']} "
                  f"deg_mu={payload['deg_mu']} Den_exps={E}", flush=True)


if __name__ == "__main__":
    main()
