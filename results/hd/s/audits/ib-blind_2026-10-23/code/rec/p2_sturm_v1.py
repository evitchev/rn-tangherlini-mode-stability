"""p2_sturm.py -- ib-blind phase 2, Part N (numerical Sturm count) + helpers for NEG1/POS0 and Part C fits.

Integrator I : mpmath odefun (Taylor) on psi' = chi/f, chi' = W psi from the Frobenius start at rho0 = 1 + t0.
Integrator II: plain-float classical RK4 in u = log(rho - 1), N and 2N steps (Richardson), own float
               Frobenius start (order 30) at t0/2.
Zero count   : sign changes of psi at the nodes, and the unwrapped Pruefer angle theta = atan2(psi, chi),
               Z = floor(theta_end/pi). PREREG sec. 3, Part N.
"""
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import mpmath as mp  # noqa: E402
import p2_model_v1 as pm  # noqa: E402

CANDS = [1.5, 2, 3, 5, 10, 30, 100]          # rho_1* candidates (PREREG + amend: 1.5,2,3,5,10,30,100)


def t0_of(model):
    return min(model.R / 4, mp.mpf(1) / 50)


def integrate_I(model, dps=30, K=60, rho_end=100, n_nodes=4000, extra_nodes=()):
    """Return dict with nodes, psi, chi at nodes (mp), start info. Splits at rho = 2 if a well is present."""
    with mp.workdps(dps):
        t0 = t0_of(model)
        psi0, chi0, info = model.start(K, t0)
        rho0 = 1 + t0
        lo, hi = mp.log(t0), mp.log(mp.mpf(rho_end) - 1)
        nodes = [1 + mp.e**(lo + (hi - lo) * j / (n_nodes - 1)) for j in range(1, n_nodes)]
        nodes += [mp.mpf(c) for c in CANDS if rho0 < c <= rho_end]
        nodes += [mp.mpf(c) for c in extra_nodes if rho0 < c <= rho_end]
        nodes = sorted(set(nodes))
        bounds = [rho0, mp.mpf(rho_end)]
        if model.well is not None:
            bounds = [rho0, mp.mpf(2), mp.mpf(rho_end)]
        out_r, out_psi, out_chi = [rho0], [psi0], [chi0]
        y = [psi0, chi0]
        for a, b in zip(bounds[:-1], bounds[1:]):
            F = mp.odefun(lambda r, Y: [Y[1] / model.f(r), model.W(r) * Y[0]], a, y)
            for r in nodes:
                if a < r <= b:
                    v = F(r)
                    out_r.append(r)
                    out_psi.append(v[0])
                    out_chi.append(v[1])
            y = F(b)
        # Frobenius region [1, rho0]: psi from the series at a few points (must stay > 0)
        a_coef = info['a']
        fro_min = min(mp.fsum(a_coef[k] * (t0 * j / 8)**k for k in range(K + 1)) for j in range(0, 9))
        return dict(t0=t0, rho=out_r, psi=out_psi, chi=out_chi, frob_min=fro_min, frob_tail=info['tail_term'],
                    g0=info['g0'], W0=info['W0'])


def zero_counts(rho, psi, chi):
    sc = 0
    for i in range(1, len(psi)):
        if (psi[i - 1] > 0) != (psi[i] > 0):
            sc += 1
    th = [math.atan2(float(psi[0]), float(chi[0]))]
    maxjump = 0.0
    for i in range(1, len(psi)):
        t = math.atan2(float(psi[i]), float(chi[i]))
        prev = math.atan2(math.sin(th[-1]), math.cos(th[-1]))      # principal value of the running angle
        d = (t - prev + math.pi) % (2 * math.pi) - math.pi          # increment in (-pi, pi]
        maxjump = max(maxjump, abs(d))
        th.append(th[-1] + d)
    zp = math.floor(th[-1] / math.pi)
    return sc, zp, th[0], th[-1], maxjump


def integrate_II(mf, t0, N, rho_end=100, K=30):
    """Float RK4 in u = log(rho-1); returns values at the candidate radii, zero counts, theta data."""
    t0h = float(t0) / 2
    psi, chi = mf.start(K, t0h)
    u0 = math.log(t0h)
    stops = [c for c in CANDS if c <= rho_end]
    us = [math.log(c - 1) for c in stops]
    total = us[-1] - u0

    def rhs(u, p, c):
        t = math.exp(u)
        rho = 1 + t
        return t * c / mf.f(rho), t * mf.W(rho) * p
    vals = {}
    u = u0
    y = (psi, chi)
    sc = 0
    th = math.atan2(psi, chi)
    th0 = th
    maxjump = 0.0
    for c, ue in zip(stops, us):
        n = max(10, int(round(N * (ue - u) / total)))
        h = (ue - u) / n
        for _ in range(n):
            p, q = y
            k1 = rhs(u, p, q)
            k2 = rhs(u + h / 2, p + h / 2 * k1[0], q + h / 2 * k1[1])
            k3 = rhs(u + h / 2, p + h / 2 * k2[0], q + h / 2 * k2[1])
            k4 = rhs(u + h, p + h * k3[0], q + h * k3[1])
            yn = (p + h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]),
                  q + h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]))
            u += h
            if (yn[0] > 0) != (p > 0):
                sc += 1
            t = math.atan2(yn[0], yn[1])
            d = t - math.atan2(math.sin(th), math.cos(th))
            d = (d + math.pi) % (2 * math.pi) - math.pi
            maxjump = max(maxjump, abs(d))
            th += d
            y = yn
        u = ue
        rho = c
        vals[str(c)] = dict(psi=y[0], dpsi=y[1] / mf.f(rho))
    return dict(vals=vals, Z_sign=sc, Z_prufer=math.floor(th / math.pi), theta0=th0, theta_end=th,
                maxjump=maxjump)


def run_point(spec):
    """spec: dict(label, q (str) or mu (str 'p/q'), well (str or None), dps, K, check (bool), rho_end)."""
    t_start = time.time()
    from fractions import Fraction as Fr
    dps = spec.get('dps', 30)
    K = spec.get('K', 60)
    rho_end = spec.get('rho_end', 100)
    out = dict(spec=spec)
    with mp.workdps(dps):
        if 'mu' in spec:
            w, d = pm.params_from_mu(Fr(spec['mu']))
            model = pm.ModelMP(w, d, well=spec.get('well'))
            mf = pm.ModelF(w, d, well=spec.get('well'))
            out['q'] = mp.nstr(pm.q_from_mu(Fr(spec['mu'])), 20)
        else:
            w, d = pm.params_from_q(mp.mpf(Fr(spec['q']).numerator) / Fr(spec['q']).denominator)
            model = pm.ModelMP(w, d, well=spec.get('well'))
            mf = pm.ModelF(w, d, well=spec.get('well'))
            out['q'] = spec['q']
        r1 = integrate_I(model, dps=dps, K=K, rho_end=rho_end)
        sc, zp, th0, the, mj = zero_counts(r1['rho'], r1['psi'], r1['chi'])
        idx = {mp.nstr(r, 12): i for i, r in enumerate(r1['rho'])}
        at = {}
        for c in CANDS:
            if c <= rho_end:
                i = idx.get(mp.nstr(mp.mpf(c), 12))
                p, ch = r1['psi'][i], r1['chi'][i]
                at[str(c)] = dict(psi=mp.nstr(p, 25), dpsi=mp.nstr(ch / model.f(mp.mpf(c)), 25))
        imin = min(range(len(r1['psi'])), key=lambda i: r1['psi'][i])
        Pinf = r1['rho'][-1] * r1['chi'][-1] / (model.f(r1['rho'][-1]) * r1['psi'][-1])
        out['I'] = dict(dps=dps, K=K, t0=mp.nstr(r1['t0'], 10), frob_tail=mp.nstr(r1['frob_tail'], 5),
                        frob_min=mp.nstr(r1['frob_min'], 15), g0=mp.nstr(r1['g0'], 15),
                        P0=mp.nstr(r1['W0'] / r1['g0'], 15), Z_sign=sc, Z_prufer=zp, theta0=th0, theta_end=the,
                        maxjump=mj, n_nodes=len(r1['rho']), at=at,
                        psi_min=mp.nstr(r1['psi'][imin], 15), rho_at_psi_min=mp.nstr(r1['rho'][imin], 10),
                        P_at_end=mp.nstr(Pinf, 15))
    if spec.get('run_II', True):
        t0 = float(r1['t0'])
        A2 = integrate_II(mf, t0, 20000, rho_end=rho_end)
        B2 = integrate_II(mf, t0, 40000, rho_end=rho_end)
        cmp = {}
        for c in A2['vals']:
            pI = float(mp.mpf(out['I']['at'][c]['psi']))
            dI = float(mp.mpf(out['I']['at'][c]['dpsi']))
            pa, pb = A2['vals'][c]['psi'], B2['vals'][c]['psi']
            da, db = A2['vals'][c]['dpsi'], B2['vals'][c]['dpsi']
            cmp[c] = dict(psi_II=pb, dpsi_II=db, rich_err_psi=abs(pa - pb) / 15, rich_err_dpsi=abs(da - db) / 15,
                          rel_diff_psi=abs(pb - pI) / max(abs(pI), 1e-300),
                          rel_diff_dpsi=abs(db - dI) / max(abs(dI), 1e-300))
        out['II'] = dict(Z_sign_N=A2['Z_sign'], Z_prufer_N=A2['Z_prufer'], Z_sign_2N=B2['Z_sign'],
                         Z_prufer_2N=B2['Z_prufer'], maxjump_2N=B2['maxjump'], cmp=cmp)
    if spec.get('check'):
        with mp.workdps(45):
            if 'mu' in spec:
                w, d = pm.params_from_mu(Fr(spec['mu']))
            else:
                w, d = pm.params_from_q(mp.mpf(Fr(spec['q']).numerator) / Fr(spec['q']).denominator)
            m45 = pm.ModelMP(w, d, well=spec.get('well'))
            r45 = integrate_I(m45, dps=45, K=90, rho_end=rho_end, n_nodes=400)
            sc45, zp45, _, _, _ = zero_counts(r45['rho'], r45['psi'], r45['chi'])
            idx45 = {mp.nstr(r, 12): i for i, r in enumerate(r45['rho'])}
            agree = {}
            for c in CANDS:
                if c <= rho_end:
                    i = idx45[mp.nstr(mp.mpf(c), 12)]
                    p45 = r45['psi'][i]
                    p30 = mp.mpf(out['I']['at'][str(c)]['psi'])
                    agree[str(c)] = mp.nstr(abs(p45 - p30) / abs(p45), 5)
            out['check45'] = dict(Z_sign=sc45, Z_prufer=zp45, rel_diff_psi=agree)
    out['seconds'] = round(time.time() - t_start, 2)
    return out


def ptrue_samples(spec, zs, dps=30, K=60, rho_end=10**4):
    """P_true(z) = rho psi'/psi at the given z in (0,1) (mp strings), for Part C fits; also eta profile."""
    from fractions import Fraction as Fr
    with mp.workdps(dps):
        if 'mu' in spec:
            w, d = pm.params_from_mu(Fr(spec['mu']))
        else:
            w, d = pm.params_from_q(mp.mpf(Fr(spec['q']).numerator) / Fr(spec['q']).denominator)
        model = pm.ModelMP(w, d, well=spec.get('well'))
        t0 = t0_of(model)
        a, g, Wser = model.frobenius(K)
        rho0 = 1 + t0
        zs_mp = [mp.mpf(z) for z in zs]
        rhos = [1 / (1 - z) for z in zs_mp]
        inner = [r for r in rhos if r <= rho0]
        outer = sorted(r for r in rhos if r > rho0)
        res = {}
        for r in inner:
            t = r - 1
            psi = mp.fsum(a[k] * t**k for k in range(K + 1))
            dpsi = mp.fsum(k * a[k] * t**(k - 1) for k in range(1, K + 1))
            res[r] = (psi, dpsi)
        psi0 = mp.fsum(a[k] * t0**k for k in range(K + 1))
        dpsi0 = mp.fsum(k * a[k] * t0**(k - 1) for k in range(1, K + 1))
        rmid = mp.mpf(min(100, rho_end))
        bounds = [rho0, rmid] if model.well is None else [rho0, mp.mpf(2), rmid]
        y = [psi0, model.f(rho0) * dpsi0]
        for lo, hi in zip(bounds[:-1], bounds[1:]):
            F = mp.odefun(lambda r, Y: [Y[1] / model.f(r), model.W(r) * Y[0]], lo, y)
            for r in outer:
                if lo < r <= hi:
                    v = F(r)
                    res[r] = (v[0], v[1] / model.f(r))
            y = F(hi)
        if rho_end > rmid:
            # beyond rho = 100: u = log(rho) (odefun caps its Taylor step at 1/2, so rho steps would be ~1e5)
            def Fu(u, Y):
                r = mp.e**u
                return [r * Y[1] / model.f(r), r * model.W(r) * Y[0]]
            G = mp.odefun(Fu, mp.log(rmid), y)
            for r in outer:
                if r > rmid:
                    v = G(mp.log(r))
                    res[r] = (v[0], v[1] / model.f(r))
        out = []
        fz0 = g[0]                     # f_z(0) = f_rho(1) = g(0)
        for z, r in zip(zs_mp, rhos):
            psi, dpsi = res[r]
            P = r * dpsi / psi
            f = model.f(r)
            eta = (r * z * fz0 / (f * psi**2)) if z > 0 else mp.mpf(1)
            out.append((P, eta))
        P0 = Wser[0] / g[0]
        return out, P0, model


def gap_test(qs, vals, safety=2.0):
    """PREREG Part N gap rule on one function g sampled at qs (uniform spacing assumed per run)."""
    n = len(qs)
    h = qs[1] - qs[0]
    D2 = [None] * n
    for i in range(1, n - 1):
        D2[i] = (vals[i + 1] - 2 * vals[i] + vals[i - 1]) / h**2
    D2[0], D2[n - 1] = D2[1], D2[n - 2]
    cells = []
    for i in range(n - 1):
        bound = safety * (h**2 / 8) * max(abs(D2[i]), abs(D2[i + 1]))
        m = min(vals[i], vals[i + 1])
        cells.append(dict(i=i, q_lo=qs[i], q_hi=qs[i + 1], min=m, bound=bound, ok=bool(m > bound)))
    return cells


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', required=True, choices=['dev', 'band', 'pos0', 'neg1', 'refine'])
    ap.add_argument('--q', nargs='*', default=[])
    ap.add_argument('--well', default=None)
    ap.add_argument('--workers', type=int, default=8)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    print('START', time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'mode', args.mode, flush=True)
    pm.guard()
    ok, gate = pm.node_gate(args.workers)
    if not ok:
        print('GATE FAIL: not starting', flush=True)
        sys.exit(4)
    from fractions import Fraction as Fr
    if args.mode == 'band':
        specs = [dict(label='q%02d' % i, q=str(Fr(948, 1000) + Fr(i, 2000)), check=(i % 4 == 0)) for i in range(85)]
    elif args.mode == 'pos0':
        specs = [dict(label='q0', q='0', check=True)]
    elif args.mode == 'neg1':
        specs = [dict(label='neg1', q='97/100', well=args.well, check=True)]
    else:
        specs = [dict(label='p%d' % i, q=qq, check=(args.mode == 'refine'), well=args.well) for i, qq in enumerate(args.q)]
    import multiprocessing as mpc
    w = gate['w']
    results = []
    with mpc.get_context('fork').Pool(min(w, len(specs))) as pool:
        for r in pool.imap(run_point, specs):
            I = r['I']
            II = r.get('II', {})
            print('%s q=%s Z_I(sign,prufer)=(%d,%d) Z_II(N:%d,%d 2N:%d,%d) psi_min=%s @rho=%s P(100)=%s t=%.1fs'
                  % (r['spec']['label'], r['q'], I['Z_sign'], I['Z_prufer'], II.get('Z_sign_N', -1),
                     II.get('Z_prufer_N', -1), II.get('Z_sign_2N', -1), II.get('Z_prufer_2N', -1),
                     I['psi_min'], I['rho_at_psi_min'], I['P_at_end'], r['seconds']), flush=True)
            results.append(r)
            stop = (I['Z_sign'] >= 1 or I['Z_prufer'] >= 1) and (II.get('Z_sign_2N', 0) >= 1)
            if stop and args.mode == 'band':
                print('A3 STOP: Z >= 1 with both integrators at q =', r['q'], flush=True)
                pool.terminate()
                break
    json.dump(dict(gate=gate, results=results), open(args.out, 'w'), indent=1, default=str)
    print('END', time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), flush=True)
