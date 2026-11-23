"""p2_controls.py -- ib-blind phase 2, NEG1 ground truth (rigorous integrals, python-flint acb.integral).

At q = 97/100, phi = (rho-1)(2-rho) on [1,2] (0 elsewhere), b = 16 (rho-1)^2 (2-rho)^2 on [1,2]:
  I1 = int f phi'^2, I2 = int W phi^2, I3 = int phi^2/f (= ||phi||^2 in L2(dr*)), I4 = int b phi^2 (= 8/315),
  A  = max(1, ceil(sup((I1 + I2 + 0.1 I3)/I4)) + 1),  Q[phi] = I1 + I2 - A I4  (must be <= -0.1 I3 - I4 < 0).
A3: if sup(I1 + I2) < 0 the unperturbed operator already has negative spectrum at q = 0.97 -> STOP.
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
from flint import arb, acb, ctx, fmpq  # noqa: E402
import p2_model_v1 as pm  # noqa: E402


def neg1_integrals(prec=128, qnum=97, qden=100):
    ctx.prec = prec
    q = arb(qnum) / qden
    w = (1 - q * q).sqrt()
    s = (1 + 7 * q * q / 9).sqrt()
    dl = (s - 1) / 14
    xH = 2 / (1 + w)
    kap = (1 - w) / (1 + w)
    Uc = [pm._pv([arb(c) for c in cs], dl) for cs in pm.UC]
    Hc = [pm._pv([arb(c) for c in cs], dl) for cs in pm.HC]

    def f(r):
        r4 = 1 / r**4
        return (1 - r4) * (1 - kap * r4)

    def W(r):
        x = xH / r**4
        U = pm._pv(Uc, x)
        H = pm._pv(Hc, x)
        return U / (64 * r * r * H * H)

    I1 = acb.integral(lambda r, a: f(r) * (3 - 2 * r)**2, 1, 2)
    I2 = acb.integral(lambda r, a: W(r) * ((r - 1) * (2 - r))**2, 1, 2)
    I3 = acb.integral(lambda r, a: (r - 1) * (2 - r)**2 * r**4 / ((r + 1) * (r * r + 1) * (1 - kap / r**4)), 1, 2)
    I4 = acb.integral(lambda r, a: 16 * ((r - 1) * (2 - r))**4, 1, 2)
    res = dict(I1=str(I1.real), I2=str(I2.real), I3=str(I3.real), I4=str(I4.real),
               I4_exact='8/315', I4_contains_exact=bool((I4.real - arb(8) / 315).contains(0)),
               imag_ok=bool(I1.imag.contains(0) and I2.imag.contains(0) and I3.imag.contains(0)))
    S12 = I1.real + I2.real
    res['I1_plus_I2'] = str(S12)
    res['A3_unperturbed_negative'] = bool(S12 < 0)          # arb comparison: True only if certainly < 0
    ratio = (S12 + I3.real / 10) / I4.real
    import math
    sup = float(ratio.mid()) + float(ratio.rad()) + 1e-9      # only needs to be an upper bound; arb checks below
    A = max(1, int(math.ceil(sup)) + 1)
    Q = S12 - A * I4.real
    res['A'] = A
    res['Q_phi'] = str(Q)
    res['Q_certified_negative'] = bool(Q < 0)
    res['Q_le_minus_0p1_I3_minus_I4'] = bool(Q + I3.real / 10 + I4.real <= 0)
    res['Rayleigh_quotient_upper'] = str(Q / I3.real)
    return res


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--qnum', type=int, default=97)
    ap.add_argument('--qden', type=int, default=100)
    args = ap.parse_args()
    print('START', time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), flush=True)
    pm.guard()
    ok, gate = pm.node_gate(1)
    if not ok:
        sys.exit(4)
    t = time.time()
    r = neg1_integrals(qnum=args.qnum, qden=args.qden)
    r['q'] = '%d/%d' % (args.qnum, args.qden)
    r['seconds'] = round(time.time() - t, 2)
    print(json.dumps(r, indent=1), flush=True)
    if r['A3_unperturbed_negative']:
        print('A3 STOP: unperturbed I1 + I2 < 0 at q = 97/100 (witness phi). Hand back at once.', flush=True)
    json.dump(dict(gate=gate, neg1=r), open(args.out, 'w'), indent=1)
    print('END', time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), flush=True)
