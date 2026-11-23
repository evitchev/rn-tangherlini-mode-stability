"""p2_cert.py -- ib-blind phase 2, Parts E and C (exact), TP1, NEG1 certifier refusal, cross-evaluation.

N(z, mu) of PREREG L2, multiplied by D = 1296 E^4 (E = (1+mu)(7+mu) > 0), is a polynomial in (z, mu):
   N_D = U_D - G * (F1 P + F0 (-P + (1-z) P_z + P^2)),
   U_D = 1296 E^4 U_-,  G = 64*1296*E*(E H_-)^2,  F1 = E (1-z) f_z,  F0 = E f,
with x = 2A(1-z)^4/E (A = 7 + mu^2), delta = (1-mu^2)/(6A), q^2 = 1 - (8mu/A)^2, all from ki_s5.py via sympy.
"""
import json
import math
import os
import random
import sys
import time
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import sympy as sp  # noqa: E402
import mpmath as mp  # noqa: E402
from flint import fmpq, fmpq_poly  # noqa: E402
import p2_model_v1 as pm  # noqa: E402
import p2_bern_v1 as pb  # noqa: E402
import p2_sturm_v1 as ps  # noqa: E402

zS, muS, tS = sp.symbols('z mu t')
MU_LO, MU_HI, MU_A = Fr(1237, 10000), Fr(2817, 10000), Fr(2780, 10000)


def to_fmpq(r):
    r = sp.Rational(r)
    return fmpq(int(r.p), int(r.q))


def sym_to_bipoly(expr, zsym=zS):
    P = sp.Poly(sp.expand(expr), zsym, muS)
    terms = {}
    for (i, j), c in P.terms():
        terms.setdefault(j, {})[i] = to_fmpq(c)
    m = max(terms) if terms else 0
    cs = []
    for j in range(m + 1):
        d = terms.get(j, {})
        n = max(d) if d else 0
        cs.append(fmpq_poly([d.get(i, fmpq(0)) for i in range(n + 1)]))
    return pb.BiPoly(cs)


def bipoly_to_sym(P, zsym=zS):
    return sum(sp.Rational(int(v.p), int(v.q)) * zsym**i * muS**j
               for j, c in enumerate(P.c) for i, v in enumerate(c.coeffs()) if v != 0)


_PIECES = None


def pieces():
    global _PIECES
    if _PIECES is not None:
        return _PIECES
    A = 7 + muS**2
    E = (1 + muS) * (7 + muS)
    x = 2 * A * (1 - zS)**4 / E
    dl = (1 - muS**2) / (6 * A)
    q2 = 1 - (8 * muS / A)**2
    U = pm.ki.U_minus(n=5, m=7, d=dl, x=x, y=0, K=1, tamper=pm.TAMPER)
    H = pm.ki.H_minus(n=5, m=7, d=dl, x=x)
    f = 1 - x + q2 * x**2 / 4
    out = {}
    for name, e in (('UD', 1296 * E**4 * U), ('EH', E * H), ('F0', E * f), ('F1', E * (1 - zS) * sp.diff(f, zS))):
        c = sp.cancel(sp.together(e))
        num, den = sp.fraction(c)
        assert den.free_symbols == set() or sp.simplify(den) == 1, (name, den)
        out[name] = sp.expand(c)
    # hand-derived forms (redundant checks of the reduction)
    assert sp.expand(out['F0'] - (E - 2 * A * (1 - zS)**4 + (1 - muS) * (7 - muS) * (1 - zS)**8)) == 0
    assert sp.expand(out['EH'] - (7 * E + 5 * (49 - muS**2) * (1 - zS)**4)) == 0
    assert sp.expand(out['F1'] - (8 * A * (1 - zS)**4 - 8 * (1 - muS) * (7 - muS) * (1 - zS)**8)) == 0
    bp = {k: sym_to_bipoly(v) for k, v in out.items()}
    Eb = sym_to_bipoly(sp.expand(E))
    bp['E'] = Eb
    bp['G'] = Eb * bp['EH'] * bp['EH'] * (64 * 1296)
    bp['sym'] = out
    _PIECES = bp
    return bp


def N_D(P):
    pc = pieces()
    one_minus_z = pb.BiPoly([fmpq_poly([1, -1])])
    inner = pc['F1'] * P + pc['F0'] * (-P + one_minus_z * P.dz() + P * P)
    return pc['UD'] - pc['G'] * inner


def N_D_well(P, A_well):
    """Planted well on z in [0, 1/2]: N_D (1-z)^6 - 16 A G E z^2 (1-2z)^2  (PREREG NEG1; amend X3)."""
    pc = pieces()
    z6 = pb.BiPoly([fmpq_poly([1, -1])**6])
    bump = pb.BiPoly([fmpq_poly([0, 0, 1]) * fmpq_poly([1, -2])**2])
    return N_D(P) * z6 - pc['G'] * pc['E'] * bump * (16 * A_well)


def N_direct(zv, muv, P_sym):
    """Independent exact evaluation of 1296 E^4 N at a rational point (sympy, x_H = 2/(1+w) route)."""
    zv, muv = sp.Rational(zv), sp.Rational(muv)
    A = 7 + muv**2
    E = (1 + muv) * (7 + muv)
    w = 8 * muv / A
    q2 = 1 - w**2
    xH = 2 / (1 + w)
    dl = (1 - muv**2) / (6 * A)
    zz = sp.Symbol('zz')
    xe = xH * (1 - zz)**4
    fe = 1 - xe + q2 * xe**2 / 4
    f = fe.subs(zz, zv)
    fz = sp.diff(fe, zz).subs(zz, zv)
    x = xe.subs(zz, zv)
    U = pm.ki.U_minus(n=5, m=7, d=dl, x=x, y=0, K=1, tamper=pm.TAMPER)
    H = pm.ki.H_minus(n=5, m=7, d=dl, x=x)
    P = P_sym.subs({zS: zv, muS: muv})
    Pz = sp.diff(P_sym, zS).subs({zS: zv, muS: muv})
    N = U - 64 * H**2 * ((1 - zv) * fz * P + f * (-P + (1 - zv) * Pz + P**2))
    return 1296 * E**4 * N


def cross_eval(P, mu_l, mu_r, npts=50, seed=20261023):
    rnd = random.Random(seed)
    Nb = N_D(P)
    Ps = bipoly_to_sym(P)
    bad = 0
    for _ in range(npts):
        zv = Fr(rnd.randint(0, 10**6), 10**6)
        mv = Fr(mu_l) + (Fr(mu_r) - Fr(mu_l)) * Fr(rnd.randint(0, 10**6), 10**6)
        a = Nb(fmpq(zv.numerator, zv.denominator), fmpq(mv.numerator, mv.denominator))
        b = N_direct(sp.Rational(zv.numerator, zv.denominator), sp.Rational(mv.numerator, mv.denominator), Ps)
        if sp.Rational(int(a.p), int(a.q)) != sp.Rational(b):
            bad += 1
    return dict(points=npts, mismatches=bad, ok=(bad == 0))


# ----------------------------------------------------------------------------- Part E
def part_E():
    pc = pieces()
    res = {}
    # E2 cover (exact) and denominator positivity
    def q2(mu):
        w = Fr(8) * mu / (7 + mu * mu)
        return 1 - w * w
    res['E2'] = dict(q2_lo_ge=q2(MU_LO) >= Fr(99, 100)**2, q2_hi_le=q2(MU_HI) <= Fr(948, 1000)**2,
                     q_lo=str(math.sqrt(q2(MU_LO))), q_hi=str(math.sqrt(q2(MU_HI))),
                     D='1296*(1+mu)^4*(7+mu)^4 > 0 for mu >= 0 (product of positive factors)')
    res['E2']['ok'] = bool(res['E2']['q2_lo_ge'] and res['E2']['q2_hi_le'])
    # E0: U_D > 0 on [0,1] x [mu_a, mu_hi]
    t = time.time()
    r0 = pb.bernstein_positive(pc['UD'], (fmpq(0), fmpq(1)), (to_fmpq(sp.Rational(2780, 10000)),
                                                            to_fmpq(sp.Rational(2817, 10000))))
    res['E0'] = dict(result=r0, seconds=round(time.time() - t, 2))
    # E1 for each rho1* candidate: U_-(t x_H rho1^-4) > 0 on [0,1]_t x [mu_lo, mu_hi]
    A = 7 + muS**2
    E = (1 + muS) * (7 + muS)
    dl = (1 - muS**2) / (6 * A)
    res['E1'] = {}
    for c in ps.CANDS:
        rc = sp.Rational(c).limit_denominator(10)
        x = tS * 2 * A / (E * rc**4)
        U = pm.ki.U_minus(n=5, m=7, d=dl, x=x, y=0, K=1, tamper=pm.TAMPER)
        e = sp.cancel(sp.together(1296 * E**4 * U))
        num, den = sp.fraction(e)
        assert not den.free_symbols, den
        Pb = sym_to_bipoly(sp.expand(e), zsym=tS)
        t = time.time()
        r1 = pb.bernstein_positive(Pb, (fmpq(0), fmpq(1)), (to_fmpq(sp.Rational(1237, 10000)),
                                                            to_fmpq(sp.Rational(2817, 10000))))
        res['E1'][str(c)] = dict(result=r1, seconds=round(time.time() - t, 2))
    return res


# ----------------------------------------------------------------------------- fits
def cheb_nodes(M):
    # X_j = 2 z_j - 1 = cos(theta_j), theta_j = pi (j + 1/2)/M  (matches the coefficient formula in fit_poly)
    return [(1 + math.cos(math.pi * (j + 0.5) / M)) / 2 for j in range(M)]


def fit_poly(samples, d, eps1, eps2, cap=None):
    """Chebyshev fit (degree d) of T = P_true - eps1 - eps2*eta at the nodes; coefficients rounded to 2^-48."""
    M = len(samples)
    T = []
    for (P, eta) in samples:
        v = P - eps1 - eps2 * eta
        if cap is not None:
            v = max(min(v, cap), -cap)
        T.append(v)
    cs = []
    for k in range(d + 1):
        s = mp.fsum(T[j] * mp.cos(mp.pi * k * (j + mp.mpf(1) / 2) / M) for j in range(M)) * 2 / M
        if k == 0:
            s /= 2
        cs.append(fmpq(int(mp.nint(s * 2**48)), 2**48))
    X = fmpq_poly([-1, 2])                      # T_k(2z - 1)
    Tkm1, Tk = fmpq_poly([1]), X
    P = Tkm1 * cs[0]
    if d >= 1:
        P = P + Tk * cs[1]
    for k in range(2, d + 1):
        Tkm1, Tk = Tk, X * Tk * 2 - Tkm1
        P = P + Tk * cs[k]
    return P


SAMPLE_CACHE = {}


def samples_at(mu, well=None, M=160):
    key = (str(mu), str(well), M)
    if key in SAMPLE_CACHE:
        return SAMPLE_CACHE[key]
    zs = cheb_nodes(M)
    spec = dict(mu=str(mu)) if well is None else dict(mu=str(mu), well=str(well))
    out, P0, _ = ps.ptrue_samples(spec, zs, dps=30, K=60, rho_end=5 * 10**4)
    SAMPLE_CACHE[key] = (out, P0)
    return out, P0


ATTEMPTS = [(24, 0.02, 0.0), (32, 0.01, 0.05), (40, 0.005, 0.1), (40, 0.05, 0.2), (40, 0.002, 0.02)]


def lin_interp(Pl, Pr, mu_l, mu_r):
    dmu = fmpq(mu_r.numerator, mu_r.denominator) - fmpq(mu_l.numerator, mu_l.denominator)
    ml = fmpq(mu_l.numerator, mu_l.denominator)
    c1 = (Pr - Pl) * (1 / dmu)
    c0 = Pl - c1 * ml
    return pb.BiPoly([c0, c1])


def try_cell(mu_l, mu_r, attempts=ATTEMPTS, well=None, A_well=None):
    sl, P0l = samples_at(mu_l, well)
    sr, P0r = samples_at(mu_r, well)
    log = []
    for (d, e1, e2) in attempts:
        t = time.time()
        cap = 50 if well is not None else None
        Pl = fit_poly(sl, d, e1, e2, cap)
        Pr = fit_poly(sr, d, e1, e2, cap)
        P = lin_interp(Pl, Pr, mu_l, mu_r)
        zb = (fmpq(0), fmpq(1))
        mb = (fmpq(mu_l.numerator, mu_l.denominator), fmpq(mu_r.numerator, mu_r.denominator))
        if A_well is None:
            r = pb.bernstein_positive(N_D(P), zb, mb)
        else:
            ra = pb.bernstein_positive(N_D_well(P, A_well), (fmpq(0), fmpq(1, 2)), mb)
            rb = pb.bernstein_positive(N_D(P), (fmpq(1, 2), fmpq(1)), mb)
            r = dict(ok=bool(ra['ok'] and rb['ok']), well_part=ra, outer_part=rb)
        P0num = [float(P(fmpq(0), mb[0])), float(P(fmpq(0), mb[1]))]
        log.append(dict(d=d, eps1=e1, eps2=e2, ok=r['ok'], result=r, seconds=round(time.time() - t, 2),
                        P_sym=str(bipoly_to_sym(P)),
                        P0_cert=P0num, P0_true=[float(P0l), float(P0r)],
                        P1_cert=[float(P(fmpq(1), mb[0])), float(P(fmpq(1), mb[1]))]))
        if r['ok']:
            return True, P, log, (P0l, P0r)
    return False, None, log, (P0l, P0r)


def tp1(P, mu_l, mu_r, P0s):
    """TP1: P + Delta (forces N(0) < 0) and P - 20 (forces N(1) < 0) must be rejected."""
    mb = (fmpq(mu_l.numerator, mu_l.denominator), fmpq(mu_r.numerator, mu_r.denominator))
    gaps = [float(P0s[0]) - float(P(fmpq(0), mb[0])), float(P0s[1]) - float(P(fmpq(0), mb[1]))]
    Delta = Fr(math.ceil((max(gaps) + 0.1) * 1000), 1000)
    out = {}
    for name, Q in (('P_plus_Delta', P + fmpq(Delta.numerator, Delta.denominator)), ('P_minus_20', P - 20)):
        r = pb.bernstein_positive(N_D(Q), (fmpq(0), fmpq(1)), mb)
        out[name] = dict(rejected=not r['ok'], result=r)
    out['Delta'] = str(Delta)
    out['caught'] = all(v['rejected'] for k, v in out.items() if isinstance(v, dict))
    return out


def run_cell(args):
    mu_l, mu_r, depth = args
    t = time.time()
    ok, P, log, P0s = try_cell(Fr(mu_l), Fr(mu_r))
    res = dict(mu_l=str(mu_l), mu_r=str(mu_r), depth=depth, ok=ok, attempts=log, seconds=None)
    if ok:
        res['cross_eval'] = cross_eval(P, Fr(mu_l), Fr(mu_r))
        res['P_sym'] = str(bipoly_to_sym(P))
        res['P0_true'] = [str(P0s[0]), str(P0s[1])]
    res['seconds'] = round(time.time() - t, 2)
    return res


# ----------------------------------------------------------------------------- drivers
def cells_initial(n=16, lo=MU_LO, hi=MU_A):
    w = (hi - lo) / n
    return [(lo + i * w, lo + (i + 1) * w) for i in range(n)]


def main():
    import argparse
    import multiprocessing as mpc
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', required=True,
                    choices=['selftest', 'E', 'tp1_oob', 'C', 'neg1_refuse', 'neg1_refuse_post'])
    ap.add_argument('--workers', type=int, default=8)
    ap.add_argument('--well', default=None)
    ap.add_argument('--cfile', default=None, help='Part C output (for neg1_refuse_post)')
    ap.add_argument('--mu_hi_C', default=None, help='upper end of the Part C region (default MU_A)')
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    print('START', time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'mode', args.mode, flush=True)
    pm.guard()
    ok, gate = pm.node_gate(args.workers)
    if not ok:
        print('GATE FAIL: not starting', flush=True)
        sys.exit(4)
    st = pb.self_test()
    print('BERNSTEIN SELF-TEST', st['ok'], 'pos leaves', st['pos_case']['leaves'], 'neg failure',
          st['neg_case']['failure'], flush=True)
    t = time.time()
    pieces()
    print('pieces built in %.1fs; deg_z(UD)=%d deg_mu(UD)=%d deg_z(G)=%d deg_mu(G)=%d' %
          (time.time() - t, _PIECES['UD'].deg_z(), _PIECES['UD'].deg_mu(), _PIECES['G'].deg_z(),
           _PIECES['G'].deg_mu()), flush=True)
    out = dict(gate=gate, selftest=dict(ok=st['ok']), mode=args.mode)
    if args.mode == 'selftest':
        rnd = random.Random(7)
        Ptest = pb.BiPoly([fmpq_poly([fmpq(rnd.randint(-9, 9), rnd.randint(1, 5)) for _ in range(6)]),
                           fmpq_poly([fmpq(rnd.randint(-9, 9), rnd.randint(1, 5)) for _ in range(6)])])
        out['cross_eval_random_P'] = cross_eval(Ptest, Fr(3, 10), Fr(31, 100), npts=20)
        print('cross-eval (random P):', out['cross_eval_random_P'], flush=True)
    elif args.mode == 'E':
        out['E'] = part_E()
        print(json.dumps(out['E'], indent=1, default=str), flush=True)
    elif args.mode == 'tp1_oob':
        mu_l, mu_r = Fr(30, 100), Fr(31, 100)
        ok_c, P, log, P0s = try_cell(mu_l, mu_r)
        out['cell'] = dict(mu_l=str(mu_l), mu_r=str(mu_r), ok=ok_c, attempts=log)
        print('OOB cell certified:', ok_c, [(a['d'], a['eps1'], a['eps2'], a['ok']) for a in log], flush=True)
        if ok_c:
            out['cell']['cross_eval'] = cross_eval(P, mu_l, mu_r)
            out['TP1'] = tp1(P, mu_l, mu_r, P0s)
            print('TP1 (oob):', {k: (v['rejected'] if isinstance(v, dict) else v) for k, v in out['TP1'].items()},
                  flush=True)
    elif args.mode == 'C':
        mu_hi_C = Fr(args.mu_hi_C) if args.mu_hi_C else MU_A
        todo = [(str(a), str(b), 0) for a, b in cells_initial(16, MU_LO, mu_hi_C)]
        done = []
        w = gate['w']
        t_start = time.time()
        with mpc.get_context('fork').Pool(w) as pool:
            while todo:
                if time.time() - t_start > 3 * 3600:
                    print('S4: Part C budget exhausted', flush=True)
                    break
                batch, todo = todo, []
                for r in pool.imap(run_cell, batch):
                    print('cell [%s, %s] depth %d: %s  attempts=%s  %.0fs' % (
                        r['mu_l'], r['mu_r'], r['depth'], 'CERTIFIED' if r['ok'] else 'not certified',
                        [(a['d'], a['eps1'], a['eps2'], a['ok'], a['result'].get('leaves') if isinstance(
                            a['result'], dict) else None) for a in r['attempts']], r['seconds']), flush=True)
                    done.append(r)
                    if not r['ok'] and r['depth'] < 6:
                        a, b = Fr(r['mu_l']), Fr(r['mu_r'])
                        mid = (a + b) / 2
                        todo += [(str(a), str(mid), r['depth'] + 1), (str(mid), str(b), r['depth'] + 1)]
        out['cells'] = done
        # coverage: union of certified cells must equal [MU_LO, mu_hi_C]
        cert = sorted((Fr(r['mu_l']), Fr(r['mu_r'])) for r in done if r['ok'])
        cov, cur = True, MU_LO
        for a, b in cert:
            if a > cur:
                cov = False
                break
            cur = max(cur, b)
        cov = cov and cur >= mu_hi_C
        out['coverage'] = dict(certified_cells=len(cert), covers_region=cov, region=[str(MU_LO), str(mu_hi_C)])
        print('Part C coverage:', out['coverage'], flush=True)
        # TP1 on the first certified band cell (PREREG sec. 4)
        first = next((r for r in done if r['ok']), None)
        if first is not None:
            mu_l, mu_r = Fr(first['mu_l']), Fr(first['mu_r'])
            okc, P, log, P0s = try_cell(mu_l, mu_r)
            out['TP1_band'] = tp1(P, mu_l, mu_r, P0s) if okc else 'recert failed'
            print('TP1 (band, first certified cell):', out['TP1_band'] if not isinstance(out['TP1_band'], dict)
                  else out['TP1_band']['caught'], flush=True)
    elif args.mode == 'neg1_refuse':
        A_well = int(args.well)
        cells = cells_initial(16, MU_LO, MU_A)
        mu97 = None
        for a, b in cells:
            if pm.q_from_mu(b) <= mp.mpf('0.97') <= pm.q_from_mu(a):
                mu97 = (a, b)
        ok_c, P, log, P0s = try_cell(mu97[0], mu97[1], attempts=ATTEMPTS[1:], well=str(A_well), A_well=A_well)
        out['neg1_refuse'] = dict(cell=[str(mu97[0]), str(mu97[1])], A=A_well, certified=ok_c, attempts=log,
                                  refused=not ok_c)
        print('NEG1 certifier refusal (X3a): certified=%s -> %s' % (ok_c, 'OK (refused)' if not ok_c else
                                                                     'BUG (S3)'), flush=True)
    elif args.mode == 'neg1_refuse_post':
        A_well = int(args.well)
        C = json.load(open(args.cfile))
        rows = []
        for r in C['cells']:
            a, b = Fr(r['mu_l']), Fr(r['mu_r'])
            if not (pm.q_from_mu(b) <= mp.mpf('0.97') <= pm.q_from_mu(a)):
                continue
            for att in r['attempts']:
                if 'P_sym' not in att:
                    continue
                P = sym_to_bipoly(sp.sympify(att['P_sym']))
                mb = (fmpq(a.numerator, a.denominator), fmpq(b.numerator, b.denominator))
                ra = pb.bernstein_positive(N_D_well(P, A_well), (fmpq(0), fmpq(1, 2)), mb)
                rb = pb.bernstein_positive(N_D(P), (fmpq(1, 2), fmpq(1)), mb)
                rows.append(dict(cell=[r['mu_l'], r['mu_r']], d=att['d'], eps1=att['eps1'], eps2=att['eps2'],
                                 certified_with_well=bool(ra['ok'] and rb['ok']), well_part=ra))
        out['neg1_refuse_post'] = dict(rows=rows, all_refused=all(not x['certified_with_well'] for x in rows),
                                       n=len(rows))
        print('NEG1 post refusal (X3b):', out['neg1_refuse_post']['n'], 'P re-verified; all refused =',
              out['neg1_refuse_post']['all_refused'], flush=True)
    json.dump(out, open(args.out, 'w'), indent=1, default=str)
    print('END', time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), flush=True)


if __name__ == '__main__':
    main()
