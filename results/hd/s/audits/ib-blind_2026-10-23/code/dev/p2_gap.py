"""p2_gap.py -- ib-blind phase 2, Part N decision: rho1* choice and the gap argument (PREREG sec. 3 Part N).

Inputs: the Part N band output (JSON from p2_sturm --mode band), optional refinement outputs, and the Part E
output (E1 pass/fail per candidate rho1*). Output: JSON + printed table. No new integration here.
"""
import json
import sys
import time
from fractions import Fraction as Fr

import mpmath as mp

CANDS = ['1.5', '2', '3', '5', '10', '30', '100']


def load_points(files):
    pts = {}
    for f in files:
        d = json.load(open(f))
        for r in d['results']:
            q = Fr(r['q'])
            pts[q] = r
    return [pts[k] for k in sorted(pts)], sorted(pts)


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--band', nargs='+', required=True)
    ap.add_argument('--E', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    print('START', time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), flush=True)
    rows, qs = load_points(args.band)
    E = json.load(open(args.E))['E']
    e1ok = {c: bool(E['E1'][c]['result']['ok']) for c in CANDS}
    out = dict(n_points=len(rows), q_min=str(qs[0]), q_max=str(qs[-1]), E1=e1ok)
    # per-point checks
    bad = []
    for r in rows:
        I, II = r['I'], r['II']
        okZ = (I['Z_sign'] == 0 and I['Z_prufer'] == 0 and II['Z_sign_N'] == 0 and II['Z_prufer_N'] == 0
               and II['Z_sign_2N'] == 0 and II['Z_prufer_2N'] == 0)
        okI_II = all(v['rel_diff_psi'] < 1e-8 and v['rel_diff_dpsi'] < 1e-8 for v in II['cmp'].values())
        ok45 = True
        if 'check45' in r:
            ok45 = (r['check45']['Z_sign'] == 0 and r['check45']['Z_prufer'] == 0 and
                    all(mp.mpf(v) < mp.mpf('1e-20') for v in r['check45']['rel_diff_psi'].values()))
        okjump = I['maxjump'] < 0.5 and II['maxjump_2N'] < 0.5
        okfro = mp.mpf(I['frob_min']) > 0
        if not (okZ and okI_II and ok45 and okjump and okfro):
            bad.append(dict(q=r['q'], okZ=okZ, okI_II=okI_II, ok45=ok45, okjump=okjump, okfro=okfro))
    out['point_failures'] = bad
    # rho1* choice
    chosen = None
    for c in CANDS:
        if not e1ok[c]:
            continue
        if all(mp.mpf(r['I']['at'][c]['psi']) > 0 and mp.mpf(r['I']['at'][c]['dpsi']) > 0 for r in rows):
            chosen = c
            break
    out['rho1_star'] = chosen
    # gap test on a(q) = psi(rho1*), b(q) = psi'(rho1*): local spacing h (uniform segments)
    if chosen is not None:
        res = {}
        for key in ('psi', 'dpsi'):
            vals = [float(mp.mpf(r['I']['at'][chosen][key])) for r in rows]
            qf = [float(q) for q in qs]
            n = len(qf)
            cells = []
            for i in range(n - 1):
                h = qf[i + 1] - qf[i]
                # second differences from the nearest uniform triple(s) of the same spacing
                d2 = []
                for j in (i - 1, i, i + 1):
                    if 0 <= j - 0 and j - 1 >= 0 and j + 1 < n:
                        h1, h2 = qf[j] - qf[j - 1], qf[j + 1] - qf[j]
                        if abs(h1 - h2) < 1e-12 and abs(h1 - h) < 1e-12:
                            d2.append(abs(vals[j + 1] - 2 * vals[j] + vals[j - 1]) / h1**2)
                if not d2:
                    d2 = [float('inf')]
                bound = 2.0 * h * h / 8 * max(d2)
                m = min(vals[i], vals[i + 1])
                cells.append(dict(q_lo=str(qs[i]), q_hi=str(qs[i + 1]), min=m, bound=bound, ok=bool(m > bound),
                                  margin_ratio=(m / bound if bound > 0 else float('inf'))))
            res[key] = dict(all_ok=all(c['ok'] for c in cells), n_cells=len(cells),
                            worst=min(cells, key=lambda c: c['margin_ratio']), failing=[c for c in cells if not c['ok']],
                            min_value=min(vals))
        out['gap'] = res
    out['part_N_pass'] = bool(chosen is not None and not bad and out.get('gap') and
                              all(v['all_ok'] for v in out['gap'].values()) and
                              qs[0] <= Fr(948, 1000) and qs[-1] >= Fr(99, 100))
    print(json.dumps(out, indent=1, default=str), flush=True)
    json.dump(out, open(args.out, 'w'), indent=1, default=str)
    print('END', time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), flush=True)


if __name__ == '__main__':
    main()
