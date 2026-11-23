"""Item (c), option B: an independent exact re-run of bh-modes T3, the l = 2 certificates (session-L, 2026-10-23).

Registered before any run in p3_T3_rerun_registration_2026-10-22/REGISTRATION.md (sha256 1224713c...).

  [python-2]/bin/python3 -I -B p3rerun.py ka     LEAN_ONSET
  [python-2]/bin/python3 -I -B p3rerun.py dev    LEAN_ONSET
  [python-2]/bin/python3 -I -B p3rerun.py record LEAN_ONSET T3_RECORD T3_REPRO OUT_JSON

LEAN_ONSET is the item (b) Lean file BHModesOnset.lean; its Fp, B1 and B2 are read. T3_RECORD and T3_REPRO are bh-modes
results/p3/runs/{record,repro-*}/T3/result.json (read only). No paths are printed.

Route R (the trust base) and the Bernstein search use Python integers only. sympy is imported only for X1 and for X3
at z = 0. Polynomials are dicts {(i, j): c} for z^i mu^j (or t^i mu^j), or arrays p[i][j] on a local unit square.
"""

import hashlib
import json
import math
import random
import re
import sys
import time
from fractions import Fraction as Fr

REGISTRATION_SHA256 = '1224713c339f41741cc4b8c3a3ca25d75c9cebb700fca9617d10a74f18550ea2'
T3_SHA256_PREFIX = 'f893d820aa0f289f'          # results/p3/RESULT.md
T3_RANGE = (Fr(3, 25), Fr(1, 5))
SEED = 20261022
NPTS = 40
MAX_DEPTH, MAX_LEAVES = 40, 4096

# item (b)'s Fp, transcribed; checked against the Lean file at every start (U_- = Fp(t, mu)/((mu + 1)^3 (mu + 6)))
F_HARD = {(4, 4): -10240, (4, 3): 194560, (4, 2): -1290240, (4, 1): 3317760, (4, 0): -2211840,
          (3, 4): 38912, (3, 3): -466944, (3, 2): 1419264, (3, 1): -221184, (3, 0): 663552,
          (2, 4): -36864, (2, 3): 184320, (2, 1): 1105920, (2, 0): 1327104,
          (1, 4): -9216, (1, 3): -18432, (1, 2): -645120, (1, 1): -1271808, (1, 0): -635904,
          (0, 4): 27648, (0, 3): 248832, (0, 2): 580608, (0, 1): 525312, (0, 0): 165888}
# fhat = (1 + mu)(6 + mu) f and Hhat = (1 + mu) H_-, in (t, mu)
FHAT_T = {(0, 0): 6, (0, 1): 7, (0, 2): 1, (1, 0): -12, (1, 2): -2, (2, 0): 6, (2, 1): -7, (2, 2): 1}
HHAT_T = {(0, 0): 6, (0, 1): 6, (1, 0): 24, (1, 1): -4}
DEN = {(0, 0): 6, (0, 1): 19, (0, 2): 21, (0, 3): 9, (0, 4): 1}          # (mu + 1)^3 (mu + 6)
T_OF_Z = {(0, 0): 1, (1, 0): -3, (2, 0): 3, (3, 0): -1}                   # t = (1 - z)^3
ONE_MINUS_Z = {(0, 0): 1, (1, 0): -1}
BETA = {(1, 0): Fr(27, 4), (2, 0): Fr(-27, 2), (3, 0): Fr(27, 4)}          # (27/4) z (1 - z)^2


# ---------------------------------------------------------------- dict polynomials

def padd(*ps):
    out = {}
    for p in ps:
        for k, c in p.items():
            out[k] = out.get(k, 0) + c
    return {k: c for k, c in out.items() if c != 0}


def pscale(p, c):
    return {k: v * c for k, v in p.items() if v * c != 0}


def pmul(p, q):
    out = {}
    for (i1, j1), c1 in p.items():
        for (i2, j2), c2 in q.items():
            k = (i1 + i2, j1 + j2)
            out[k] = out.get(k, 0) + c1 * c2
    return {k: c for k, c in out.items() if c != 0}


def pdz(p):
    return {(i - 1, j): i * c for (i, j), c in p.items() if i > 0}


def peval(p, z, mu):
    return sum(c * z**i * mu**j for (i, j), c in p.items())


def t_to_z(p_t):
    """Substitute t = (1 - z)^3."""
    powers = [{(0, 0): 1}]
    for _ in range(max(a for a, _ in p_t)):
        powers.append(pmul(powers[-1], T_OF_Z))
    out = {}
    for (a, j), c in p_t.items():
        for (i, _), d in powers[a].items():
            out[(i, j)] = out.get((i, j), 0) + c * d
    return {k: c for k, c in out.items() if c != 0}


def den_lcm(p):
    L = 1
    for v in p.values():
        L = math.lcm(L, Fr(v).denominator)
    return L


# ---------------------------------------------------------------- the Lean file

def lean_block(text, header):
    i = text.index(header)
    return text[i + len(header):].split('\n\n', 1)[0]


def parse_lean_Fp(text):
    block = lean_block(text, 'def Fp (t μ : ℝ) : ℝ :=')
    assert ' - (' not in block
    F = {}
    terms = re.findall(r'\((-?\d+) : ℝ\)((?: \* [tμ] \^ \d+)*)', block)
    for c, mon in terms:
        a = j = 0
        for v, e in re.findall(r'([tμ]) \^ (\d+)', mon):
            if v == 't':
                a = int(e)
            else:
                j = int(e)
        F[(a, j)] = F.get((a, j), 0) + int(c)
    assert len(terms) == 24, len(terms)
    return F


def parse_lean_B(text, name):
    block = lean_block(text, f'noncomputable def {name} (u ub v vb : ℝ) : ℝ :=')
    B = {}
    pat = r'\((-?\d+(?:/\d+)?) : ℝ\) \* \((\d+) \* u \^ (\d+) \* ub \^ (\d+) \* v \^ (\d+) \* vb \^ (\d+)\)'
    for c, bi, i, ib, j, jb in re.findall(pat, block):
        i, ib, j, jb, bi = int(i), int(ib), int(j), int(jb), int(bi)
        assert i + ib == 4 and j + jb == 4 and bi == math.comb(4, i) * math.comb(4, j)
        B[(i, j)] = Fr(c)
    assert len(B) == 25, len(B)
    return B


# ---------------------------------------------------------------- arrays on a unit square, Bernstein

def affine1d(c, X0, Xw, Xd):
    """Coefficients in u of sum_i c_i (X0 + Xw u)^i Xd^(n - i), n = len(c) - 1 (Horner)."""
    n = len(c) - 1
    r = [c[n]]
    for i in range(n - 1, -1, -1):
        new = [0] * (len(r) + 1)
        for k, v in enumerate(r):
            new[k] += v * X0
            new[k + 1] += v * Xw
        new[0] += c[i] * Xd ** (n - i)
        r = new
    return r


def half_left(c):
    n = len(c) - 1
    return [v << (n - i) for i, v in enumerate(c)]


def half_right(c):
    d = half_left(c)
    n = len(d) - 1
    for i in range(n):
        for k in range(n - 1, i - 1, -1):
            d[k] += d[k + 1]
    return d


def normalise(arr):
    g = math.gcd(*[v for row in arr for v in row])
    return [[v // g for v in row] for row in arr] if g > 1 else arr


def split(arr, axis, side):
    f = half_left if side == 0 else half_right
    if axis == 'z':
        cols = [f([arr[i][j] for i in range(len(arr))]) for j in range(len(arr[0]))]
        out = [[cols[j][i] for j in range(len(arr[0]))] for i in range(len(arr))]
    else:
        out = [f(row) for row in arr]
    return normalise(out)


_BINOM = {}


def binom_table(n):
    if n not in _BINOM:
        _BINOM[n] = [[math.comb(n - i, k - i) if k >= i else 0 for k in range(n + 1)] for i in range(n + 1)]
    return _BINOM[n]


def bern_scaled(arr):
    """beta[k][l] = C(nz, k) C(ns, l) b[k][l]: same signs as the Bernstein coefficients b on the unit square."""
    nz, ns = len(arr) - 1, len(arr[0]) - 1
    Cz, Cs = binom_table(nz), binom_table(ns)
    A = [[sum(Cz[i][k] * arr[i][j] for i in range(k + 1)) for j in range(ns + 1)] for k in range(nz + 1)]
    return [[sum(Cs[j][l] * A[k][j] for j in range(l + 1)) for l in range(ns + 1)] for k in range(nz + 1)]


def to_array(p, nz, ns):
    arr = [[0] * (ns + 1) for _ in range(nz + 1)]
    for (i, j), c in p.items():
        arr[i][j] = c
    return arr


def box_poly(p, x0, x1, y0, y1):
    """p(x0 + (x1 - x0)u, y0 + (y1 - y0)v) times M = Dx^nz Dy^ns > 0, integer coefficients; returns (arr, M)."""
    nz, ns = max(i for i, _ in p), max(j for _, j in p)
    arr = to_array(p, nz, ns)
    Dx = math.lcm(x0.denominator, x1.denominator)
    Dy = math.lcm(y0.denominator, y1.denominator)
    cols = [affine1d([arr[i][j] for i in range(nz + 1)], int(x0 * Dx), int((x1 - x0) * Dx), Dx) for j in range(ns + 1)]
    arr = [[cols[j][i] for j in range(ns + 1)] for i in range(nz + 1)]
    arr = [affine1d(row, int(y0 * Dy), int((y1 - y0) * Dy), Dy) for row in arr]
    return arr, Dx**nz * Dy**ns


def corners(arr):
    c00 = arr[0][0]
    c10 = sum(arr[i][0] for i in range(len(arr)))
    c01 = sum(arr[0])
    c11 = sum(map(sum, arr))
    return [((0, 0), c00), ((1, 0), c10), ((0, 1), c01), ((1, 1), c11)]


def ratio(B):
    nz, ns = len(B) - 1, len(B[0]) - 1
    b = [Fr(B[k][l], math.comb(nz, k) * math.comb(ns, l)) for k in range(nz + 1) for l in range(ns + 1)]
    return float(min(b) / max(abs(v) for v in b))


def search(arr, max_depth=MAX_DEPTH, max_leaves=MAX_LEAVES):
    """The registered decision on the local unit square: corner check, Bernstein test, bisection by width x degree."""
    nz, ns = len(arr) - 1, len(arr[0]) - 1
    stack = [(normalise(arr), 0, Fr(0), Fr(1), Fr(0), Fr(1))]
    leaves, nodes = [], 0
    while stack:
        q, d, z0, z1, s0, s1 = stack.pop()
        nodes += 1
        for (cz, cs), v in corners(q):
            if v <= 0:
                return {'verdict': 'REJECT', 'z': (z0, z1)[cz], 's': (s0, s1)[cs], 'depth': d,
                        'nodes': nodes, 'leaves': len(leaves)}
        B = bern_scaled(q)
        if all(b > 0 for row in B for b in row):
            leaves.append((d, ratio(B)))
            if len(leaves) > max_leaves:
                return {'verdict': 'UNDECIDED', 'reason': 'leaf budget', 'nodes': nodes, 'leaves': len(leaves)}
            continue
        if d >= max_depth:
            return {'verdict': 'UNDECIDED', 'reason': 'depth budget', 'nodes': nodes, 'leaves': len(leaves)}
        if (z1 - z0) * nz >= (s1 - s0) * ns:
            zm = (z0 + z1) / 2
            stack.append((split(q, 'z', 1), d + 1, zm, z1, s0, s1))
            stack.append((split(q, 'z', 0), d + 1, z0, zm, s0, s1))
        else:
            sm = (s0 + s1) / 2
            stack.append((split(q, 's', 1), d + 1, z0, z1, sm, s1))
            stack.append((split(q, 's', 0), d + 1, z0, z1, s0, sm))
    return {'verdict': 'VERIFIED', 'leaves': len(leaves), 'nodes': nodes,
            'max_depth': max(d for d, _ in leaves), 'min_ratio': min(r for _, r in leaves)}


def corners_only(arr):
    return 'VERIFIED' if all(v > 0 for _, v in corners(arr)) else 'REJECT'


# ---------------------------------------------------------------- route R (the trust base)

class RouteR:
    """N = Nt / (Den L^2), Nt = F L^2 - 64 Hhat^2 [(1 - z) fhat_z Ph L + fhat (-Ph L + (1 - z) Ph_z L + Ph^2)], P = Ph/L."""

    def __init__(self, F_t):
        self.F = t_to_z(F_t)
        self.fh = t_to_z(FHAT_T)
        self.fhz = pdz(self.fh)
        self.H = t_to_z(HHAT_T)
        self.H2 = pmul(self.H, self.H)

    def build(self, Pq):
        L = den_lcm(Pq)
        Ph = {}
        for k, v in Pq.items():
            w = Fr(v) * L
            assert w.denominator == 1
            if w:
                Ph[k] = w.numerator
        Pz = pdz(Ph)
        br = padd(pscale(pmul(pmul(ONE_MINUS_Z, self.fhz), Ph), L),
                  pmul(self.fh, padd(pscale(Ph, -L), pscale(pmul(ONE_MINUS_Z, Pz), L), pmul(Ph, Ph))))
        return padd(pscale(self.F, L * L), pscale(pmul(self.H2, br), -64)), L

    def value(self, Nt, L, z, mu):
        return Fr(peval(Nt, z, mu)) / (peval(DEN, z, mu) * L * L)

    def point(self, Pq, z, mu):
        """Route R's closed forms evaluated at one point, without expanding N."""
        P, Pz = peval(Pq, z, mu), peval(pdz(Pq), z, mu)
        fh, fhz, H = peval(self.fh, z, mu), peval(self.fhz, z, mu), peval(self.H, z, mu)
        num = peval(self.F, z, mu) - 64 * H * H * ((1 - z) * fhz * P + fh * (-P + (1 - z) * Pz + P * P))
        return Fr(num) / peval(DEN, z, mu)


def box_array(Nt, a, b):
    """g(z, s) = Nt(z, a + (b - a)s) D^deg_mu, integer coefficients, the same sign as N on the box."""
    nz, nm = max(i for i, _ in Nt), max(j for _, j in Nt)
    D = math.lcm(a.denominator, b.denominator)
    arr = to_array(Nt, nz, nm)
    arr = [affine1d(row, int(a * D), int((b - a) * D), D) for row in arr]
    return normalise(arr)


# ---------------------------------------------------------------- route P and the other cross-checks

def Um(m, d, x):
    return (-400000 * d * (1 + m * d)**3 * x**4 - 1600 * (1 + m * d)**2 * (50 * m * d - 16) * x**3
            + 7680 * m * (1 + m * d) * x**2 - 16 * m * (5 * m * (96 - 4 * m) * d + 480) * x + 64 * m**3 + 384 * m**2)


def exact_sqrt(r):
    r = Fr(r)
    a, b = math.isqrt(r.numerator), math.isqrt(r.denominator)
    if a * a != r.numerator or b * b != r.denominator:
        raise ValueError('not a rational square')
    return Fr(a, b)


def N_routeP(Pq, z, mu):
    """PREREG section 1's factored f and TARGET.md's H_-, U_- and delta, with exact fractions."""
    w = 7 * mu / (6 + mu**2)
    q2 = 1 - w**2
    xH = 2 / (1 + exact_sqrt(1 - q2))
    assert 1 - xH + q2 * xH**2 / 4 == 0
    d = (exact_sqrt(1 + Fr(24, 25) * q2) - 1) / 12          # (1 + 2 m delta)^2 = 1 + 4 m q^2/25, m = 6
    xm = 4 / (q2 * xH)                                      # the other root: x_H x_- = 4/q^2
    assert xH + xm == 4 / q2
    k3 = xH / xm
    t = (1 - z)**3
    f = (1 - t) * (1 - k3 * t)
    fz = 3 * (1 - z)**2 * (1 + k3 - 2 * k3 * t)
    x = xH * t
    H = 6 + 10 * (1 + 6 * d) * x
    P, Pz = peval(Pq, z, mu), peval(pdz(Pq), z, mu)
    return Um(6, d, x) - 64 * H**2 * ((1 - z) * fz * P + f * (-P + (1 - z) * Pz + P**2))


def route_L(Pq):
    """X1: Nz built by sympy from the item (a) Lean definitions U6, H6, F6, F6' (x_H = 2/(1 + w), q^2 = 1 - w^2)."""
    import sympy as sp
    z, mu = sp.symbols('z mu')
    w = 7 * mu / (6 + mu**2)
    xH, q2, d = 2 / (1 + w), 1 - w**2, (1 - mu**2) / (5 * (6 + mu**2))
    x = xH * (1 - z)**3
    F6 = 1 - x + q2 * x**2 / 4
    F6p = 3 * xH * (1 - z)**2 * (1 - q2 * x / 2)
    H6 = 6 + 10 * (1 + 6 * d) * x
    P = sum(sp.Rational(Fr(v).numerator, Fr(v).denominator) * z**i * mu**j for (i, j), v in Pq.items())
    N = Um(6, d, x) - 64 * H6**2 * ((1 - z) * F6p * P + F6 * (-P + (1 - z) * sp.diff(P, z) + P**2))
    num, den = sp.fraction(sp.cancel(sp.together(N)))
    return sp.Poly(num, z, mu), sp.Poly(den, z, mu)


def X1(Nt, L, routeL):
    import sympy as sp
    z, mu = sp.symbols('z mu')
    num, den = routeL
    lhs = num * sp.Poly((mu + 1)**3 * (mu + 6) * L**2, z, mu)
    rhs = sp.Poly.from_dict({k: v for k, v in Nt.items()}, z, mu) * den
    return (lhs - rhs).is_zero


def X2(R, Nt, L, Pq, pts):
    return sum(R.value(Nt, L, zz, mm) == N_routeP(Pq, zz, mm) for zz, mm in pts)


def X3(Nt, L, Pq):
    """N(1, mu) = 2304 (12 - P(1)^2 + P(1)) and N(0, mu) = U_-(x_H) - 64 H_-(x_H)^2 f_z(0) P(0, mu), as identities."""
    Ph = {k: (Fr(v) * L).numerator for k, v in Pq.items()}
    at1 = {}
    for (i, j), c in Nt.items():
        at1[(0, j)] = at1.get((0, j), 0) + c
    P1 = {}
    for (i, j), c in Ph.items():
        P1[(0, j)] = P1.get((0, j), 0) + c
    rhs1 = pscale(pmul(padd({(0, 0): 12 * L * L}, pscale(pmul(P1, P1), -1), pscale(P1, L)), DEN), 2304)
    ok1 = padd(at1, pscale(rhs1, -1)) == {}
    import sympy as sp
    mu = sp.symbols('mu')
    w = 7 * mu / (6 + mu**2)
    xH, q2, d = 2 / (1 + w), 1 - w**2, (1 - mu**2) / (5 * (6 + mu**2))
    P0 = sum(sp.Rational(Fr(v).numerator, Fr(v).denominator) * mu**j for (i, j), v in Pq.items() if i == 0)
    rhs0 = Um(6, d, xH) - 64 * (6 + 10 * (1 + 6 * d) * xH)**2 * (3 * xH * (1 - q2 * xH / 2)) * P0
    at0 = sum(c * mu**j for (i, j), c in Nt.items() if i == 0)
    ok0 = sp.cancel(rhs0 * (mu + 1)**3 * (mu + 6) * L**2 - at0) == 0
    return ok1, ok0


def draw_points(rng, a, b, n=NPTS):
    pts = []
    for _ in range(n):
        dz = rng.randint(1, 1000)
        zz = Fr(rng.randint(0, dz), dz)
        while True:
            dm = rng.randint(100, 1000)
            lo, hi = math.ceil(a * dm), math.floor(b * dm)
            if lo <= hi:
                break
        pts.append((zz, Fr(rng.randint(lo, hi), dm)))
    return pts


# ---------------------------------------------------------------- planted certificates

def planted_A(R, Pq, a, b):
    z0, mu0 = Fr(1, 3), a + (b - a) / 3
    for j in range(-20, 11):
        c = Fr(2)**j
        Pt = padd({k: Fr(v) for k, v in Pq.items()}, pscale(BETA, c))
        val = R.point(Pt, z0, mu0)
        if val < 0:
            return c, Pt, z0, mu0, val
    return None


def planted_B(Pq):
    Pt = {k: Fr(v) for k, v in Pq.items()}
    S = {}
    for (i, j), v in Pt.items():
        S[j] = S.get(j, 0) + v
    add = {(28, j): -s for j, s in S.items()}
    add[(28, 0)] = add.get((28, 0), 0) + 5
    return padd(Pt, add)


def run_planted(R, Pt, a, b):
    Nt, L = R.build(Pt)
    res = search(box_array(Nt, a, b))
    if res['verdict'] == 'REJECT':
        mu = a + (b - a) * res['s']
        res['mu'] = mu
        res['N'] = R.value(Nt, L, res['z'], mu)
        res['N_routeP'] = N_routeP(Pt, res['z'], mu)
    return res, Nt, L


# ---------------------------------------------------------------- the known-answer gates

def ka_gates(lean_text, verbose=True):
    F = parse_lean_Fp(lean_text)
    out = {'F transcription = Lean Fp': F == F_HARD}
    for name, box in (('B1', (Fr(0), Fr(7, 8), Fr(1, 6), Fr(1))), ('B2', (Fr(7, 8), Fr(1), Fr(1, 4), Fr(1)))):
        lean_B = parse_lean_B(lean_text, name)
        arr, M = box_poly(F, *box)
        B = bern_scaled(arr)
        mine = {(k, l): Fr(B[k][l], math.comb(4, k) * math.comb(4, l) * M) for k in range(5) for l in range(5)}
        key = 'KA1' if name == 'B1' else 'KA2'
        out[f'{key} 25 Bernstein coefficients = Lean {name}'] = mine == lean_B
        out[f'{key} minimum'] = str(min(mine.values()))
        out[f'{key} search verdict'] = search(arr)['verdict']
    ka3 = [[316, -900, 900], [-600, 0, 0], [900, 0, 0]]          # 900[(z - 1/3)^2 + (s - 1/2)^2 - 1/100]
    ka4 = [[334, -900, 900], [-600, 0, 0], [900, 0, 0]]          # 900[(z - 1/3)^2 + (s - 1/2)^2 + 1/100]
    r3, r4 = search(ka3), search(ka4)
    out['KA3 REJECT'] = r3['verdict'] == 'REJECT'
    out['KA3 detail'] = {k: str(v) for k, v in r3.items()}
    out['KA4 VERIFIED'] = r4['verdict'] == 'VERIFIED'
    out['KA4 detail'] = {k: str(v) for k, v in r4.items()}
    ok = (out['F transcription = Lean Fp'] and out['KA1 25 Bernstein coefficients = Lean B1']
          and out['KA2 25 Bernstein coefficients = Lean B2'] and out['KA1 search verdict'] == 'VERIFIED'
          and out['KA2 search verdict'] == 'VERIFIED' and out['KA3 REJECT'] and out['KA4 VERIFIED'])
    if verbose:
        for k, v in out.items():
            print(f'  {k}: {v}')
        print('  KNOWN-ANSWER GATES:', 'PASS' if ok else 'FAIL')
    return ok, out, F


# ---------------------------------------------------------------- modes

def parse_P(Pd):
    out = {}
    for k, c in Pd.items():
        i, j = (int(s) for s in k.strip('()').split(','))
        out[(i, j)] = Fr(c)
    return out


def one_box(R, R_tampered, Pq, a, b, pts, label):
    """Everything registered for one box. Returns a JSON-ready dict."""
    r = {'box': [str(a), str(b)]}
    t0 = time.time()
    Nt, L = R.build(Pq)
    r['degrees'] = [max(i for i, _ in Nt), max(j for _, j in Nt)]
    rl = route_L(Pq)
    r['X1'] = X1(Nt, L, rl)
    r['X2 points equal'] = X2(R, Nt, L, Pq, pts)
    r['X3 z=1'], r['X3 z=0'] = X3(Nt, L, Pq)
    r['t_construction_s'] = round(time.time() - t0, 1)
    t1 = time.time()
    arr = box_array(Nt, a, b)
    res = search(arr)
    if res['verdict'] == 'REJECT':
        mu = a + (b - a) * res['s']
        res['mu'] = mu
        res['N'] = R.value(Nt, L, res['z'], mu)
        res['N_routeP'] = N_routeP(Pq, res['z'], mu)
    r['search'] = {k: str(v) for k, v in res.items()}
    r['t_search_s'] = round(time.time() - t1, 1)
    r['DR1 corner-only on P'] = corners_only(arr)
    pa = planted_A(R, Pq, a, b)
    if pa is None:
        r['NP-A'] = 'void: no c up to 2^10 makes the witness negative'
    else:
        c, Pt, z0, mu0, val = pa
        resA, NtA, LA = run_planted(R, Pt, a, b)
        r['NP-A c'] = str(c)
        r['NP-A witness'] = {'z': str(z0), 'mu': str(mu0), 'N (route R, closed forms)': str(val),
                             'N (route R, expanded)': str(R.value(NtA, LA, z0, mu0)),
                             'N (route P)': str(N_routeP(Pt, z0, mu0)), 'N ~': float(val)}
        r['NP-A search'] = {k: str(v) for k, v in resA.items()}
        r['DR1 corner-only on NP-A'] = corners_only(box_array(NtA, a, b))
    resB, _, _ = run_planted(R, planted_B(Pq), a, b)
    r['NP-B search'] = {k: str(v) for k, v in resB.items()}
    NtT, LT = R_tampered.build(Pq)
    r['DR2 X1 on tampered'] = X1(NtT, LT, rl)
    r['DR2 X2 points equal on tampered'] = X2(R_tampered, NtT, LT, Pq, pts)
    r['t_total_s'] = round(time.time() - t0, 1)
    v = r['search']['verdict']
    print(f'  {label} [{a}, {b}] deg {r["degrees"]}: X1 {r["X1"]}, X2 {r["X2 points equal"]}/{len(pts)}, '
          f'X3 {r["X3 z=1"]}/{r["X3 z=0"]}; search {v} ({r["search"].get("leaves")} leaves, '
          f'{r["search"].get("nodes")} nodes, max depth {r["search"].get("max_depth", r["search"].get("depth"))}, '
          f'min ratio {r["search"].get("min_ratio", "-")}); {r["t_total_s"]} s')
    print(f'      NP-A c = {r.get("NP-A c")}: {r["NP-A search"]["verdict"] if "NP-A search" in r else r["NP-A"]}'
          f' at (z, mu) = ({r.get("NP-A search", {}).get("z")}, {r.get("NP-A search", {}).get("mu")}), '
          f'depth {r.get("NP-A search", {}).get("depth")}; witness N ~ {r.get("NP-A witness", {}).get("N ~")}')
    print(f'      NP-B: {r["NP-B search"]["verdict"]} at (z, mu) = ({r["NP-B search"].get("z")}, '
          f'{r["NP-B search"].get("mu")}), depth {r["NP-B search"].get("depth")}, N = {r["NP-B search"].get("N")}')
    print(f'      DR1 corner-only: on P {r["DR1 corner-only on P"]}, on NP-A {r.get("DR1 corner-only on NP-A")}; '
          f'DR2 (tampered F): X1 {r["DR2 X1 on tampered"]}, X2 equal at {r["DR2 X2 points equal on tampered"]}/{len(pts)}')
    return r


def mode_dev(lean_text):
    print('dev: helper self-tests')
    rng = random.Random(1)
    c = [rng.randint(-10**6, 10**6) for _ in range(9)]
    print('  half_left = affine1d(0, 1, 2):', half_left(c) == affine1d(c, 0, 1, 2))
    print('  half_right = affine1d(1, 1, 2):', half_right(c) == affine1d(c, 1, 1, 2))
    p = {(i, j): rng.randint(-50, 50) for i in range(4) for j in range(3)}
    arr = to_array(p, 3, 2)
    B = bern_scaled(arr)
    ok = True
    for zz, ss in ((Fr(1, 3), Fr(2, 7)), (Fr(5, 9), Fr(1, 2)), (Fr(0), Fr(1))):
        val = sum(B[k][l] * zz**k * (1 - zz)**(3 - k) * ss**l * (1 - ss)**(2 - l) for k in range(4) for l in range(3))
        ok = ok and val == peval(p, zz, ss)
    print('  scaled Bernstein form reproduces p at 3 points:', ok)
    R = RouteR(F_HARD)
    print('  t_to_z(fhat) at a point = fhat(t(z)):',
          peval(R.fh, Fr(2, 7), Fr(1, 9)) == peval(FHAT_T, (1 - Fr(2, 7))**3, Fr(1, 9)))
    print('dev: known-answer gates')
    ka_gates(lean_text)
    print('dev: a synthetic P of degree (28, 4) on [3/25, 13/100] (not T3 data)')
    rng = random.Random(2)
    Psyn = {(i, j): Fr(rng.randint(-2**60, 2**60), 2**60) for i in range(29) for j in range(5)}
    a, b = Fr(3, 25), Fr(13, 100)
    pts = draw_points(random.Random(3), a, b)
    Ft = dict(F_HARD)
    Ft[(0, 0)] += 1
    one_box(R, RouteR(Ft), Psyn, a, b, pts, 'synthetic')


def mode_record(lean_text, rec_path, rep_path, out_json):
    t_start = time.time()
    out = {'registration_sha256': REGISTRATION_SHA256, 'code_sha256': hashlib.sha256(open(__file__, 'rb').read()).hexdigest()}
    print('record: known-answer gates (must pass before the run of record)')
    ok, ka, F = ka_gates(lean_text)
    out['KA'] = {k: (v if isinstance(v, (bool, str, dict)) else str(v)) for k, v in ka.items()}
    if not ok:
        print('KNOWN-ANSWER GATES FAILED: the run of record does not start')
        json.dump(out, open(out_json, 'w', encoding='utf-8'), indent=1)
        return 1
    raw = open(rec_path, 'rb').read()
    out['D1'] = hashlib.sha256(raw).hexdigest().startswith(T3_SHA256_PREFIX)
    rec = json.loads(raw.decode('utf-8'))['result']['boxes_mu']
    rep = json.load(open(rep_path, encoding='utf-8'))['result']['boxes_mu']
    out['D2'] = len(rec) == len(rep) and all(x['mu'] == y['mu'] and x['P'] == y['P'] for x, y in zip(rec, rep))
    boxes = [(Fr(x['mu'][0]), Fr(x['mu'][1])) for x in rec]
    out['D3'] = (len(boxes) == 8 and boxes[0][0] == T3_RANGE[0] and boxes[-1][1] == T3_RANGE[1]
                 and all(boxes[k][1] == boxes[k + 1][0] for k in range(7))
                 and all(0 < b - a <= Fr(1, 100) for a, b in boxes))
    print(f'record: D1 {out["D1"]}, D2 {out["D2"]}, D3 {out["D3"]}')
    R = RouteR(F)
    Ft = dict(F)
    Ft[(0, 0)] += 1                                         # DR2: 165888 -> 165889
    R_t = RouteR(Ft)
    rng = random.Random(SEED)
    out['boxes'] = []
    for k, (a, b) in enumerate(boxes):
        pts = draw_points(rng, a, b)
        r = one_box(R, R_t, parse_P(rec[k]['P']), a, b, pts, f'box {k}')
        out['boxes'].append(r)
    bx = out['boxes']
    out['C-B'] = ('VERIFIED' if out['D1'] and out['D3'] and all(
        r['X1'] and r['X2 points equal'] == NPTS and r['X3 z=1'] and r['X3 z=0'] and r['search']['verdict'] == 'VERIFIED'
        for r in bx) else 'NOT VERIFIED')
    pred = {
        'KA1-KA4 and X1-X3 hold': ok and all(r['X1'] and r['X2 points equal'] == NPTS and r['X3 z=1'] and r['X3 z=0'] for r in bx),
        'C-B VERIFIED on all eight boxes': out['C-B'] == 'VERIFIED',
        'NP-A not VERIFIED on any box (must)': all(r.get('NP-A search', {}).get('verdict') in ('REJECT', 'UNDECIDED') for r in bx),
        'NP-A REJECT with an exact counterexample on all eight (predicted)': all(
            r.get('NP-A search', {}).get('verdict') == 'REJECT' and Fr(r['NP-A search']['N']) <= 0 for r in bx),
        'NP-B REJECT on all eight (must)': all(r['NP-B search']['verdict'] == 'REJECT' for r in bx),
        'NP-B at depth 0, corner (1, a_k), N = -18432 (predicted)': all(
            r['NP-B search'].get('depth') == '0' and r['NP-B search'].get('z') == '1'
            and r['NP-B search'].get('mu') == r['box'][0] and r['NP-B search'].get('N') == '-18432' for r in bx),
        'DR1 corner-only VERIFIES NP-A where P_k is VERIFIED (predicted)': all(
            r.get('DR1 corner-only on NP-A') == 'VERIFIED' for r in bx if r['search']['verdict'] == 'VERIFIED'),
        'DR2 X1 fails and X2 fails at all 40 points (predicted)': all(
            (not r['DR2 X1 on tampered']) and r['DR2 X2 points equal on tampered'] == 0 for r in bx),
    }
    out['registered predictions'] = pred
    out['D2 (reported)'] = out['D2']
    out['t_total_s'] = round(time.time() - t_start, 1)
    print('record: registered predictions')
    for k, v in pred.items():
        print(f'  {k}: {v}')
    print(f'record: C-B {out["C-B"]}; total {out["t_total_s"]} s')
    print('ALL AS REGISTERED' if all(pred.values()) else 'A REGISTERED PREDICTION MISSED (reported as it stands)')
    json.dump(out, open(out_json, 'w', encoding='utf-8'), indent=1, default=str)
    return 0 if out['C-B'] == 'VERIFIED' else 2


def main(argv):
    mode, lean = argv[1], open(argv[2], encoding='utf-8').read()
    if mode == 'ka':
        return 0 if ka_gates(lean)[0] else 1
    if mode == 'dev':
        mode_dev(lean)
        return 0
    if mode == 'record':
        return mode_record(lean, argv[3], argv[4], argv[5])
    raise SystemExit('unknown mode')


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
