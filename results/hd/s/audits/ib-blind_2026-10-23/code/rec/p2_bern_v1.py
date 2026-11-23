"""p2_bern.py -- ib-blind phase 2: exact bivariate polynomials and the tensor-Bernstein positivity verifier.

BiPoly: sum_j c_j(z) mu^j with c_j in flint.fmpq_poly (exact rationals).
bernstein_positive(P, z-box, mu-box): all Bernstein coefficients on every leaf > 0  =>  P > 0 on the box.
Exact throughout (python-flint fmpq / fmpq_mat). PREREG sec. 3, Parts C and E.
"""
import random
from math import comb

from flint import fmpq, fmpq_poly, fmpq_mat


class BiPoly:
    def __init__(self, cs):
        cs = [c if isinstance(c, fmpq_poly) else fmpq_poly(c) for c in cs]
        while len(cs) > 1 and cs[-1] == 0:
            cs.pop()
        self.c = cs if cs else [fmpq_poly([0])]

    @staticmethod
    def const(v):
        return BiPoly([fmpq_poly([v])])

    @staticmethod
    def z_poly(p):
        return BiPoly([p])

    @staticmethod
    def mu_poly(coeffs):           # coeffs ascending in mu (numbers)
        return BiPoly([fmpq_poly([c]) for c in coeffs])

    def __add__(self, o):
        o = o if isinstance(o, BiPoly) else BiPoly.const(o)
        n = max(len(self.c), len(o.c))
        z = fmpq_poly([0])
        return BiPoly([(self.c[j] if j < len(self.c) else z) + (o.c[j] if j < len(o.c) else z) for j in range(n)])

    __radd__ = __add__

    def __neg__(self):
        return BiPoly([-c for c in self.c])

    def __sub__(self, o):
        return self + (-(o if isinstance(o, BiPoly) else BiPoly.const(o)))

    def __rsub__(self, o):
        return (-self) + o

    def __mul__(self, o):
        if not isinstance(o, BiPoly):
            return BiPoly([c * o for c in self.c])
        out = [fmpq_poly([0])] * (len(self.c) + len(o.c) - 1)
        for i, a in enumerate(self.c):
            if a == 0:
                continue
            for j, b in enumerate(o.c):
                out[i + j] = out[i + j] + a * b
        return BiPoly(out)

    __rmul__ = __mul__

    def dz(self):
        return BiPoly([c.derivative() for c in self.c])

    def deg_z(self):
        return max(c.degree() for c in self.c)

    def deg_mu(self):
        return len(self.c) - 1

    def __call__(self, z, mu):
        s = fmpq(0)
        for c in reversed(self.c):
            s = s * mu + c(z)
        return s

    def matrix(self):
        n, m = max(self.deg_z(), 0), self.deg_mu()
        A = fmpq_mat(n + 1, m + 1)
        for j, c in enumerate(self.c):
            cs = c.coeffs()
            for i, v in enumerate(cs):
                A[i, j] = v
        return A


def _T(n):
    """Monomial -> Bernstein on [0,1]: b_k = sum_{i<=k} C(k,i)/C(n,i) a_i."""
    T = fmpq_mat(n + 1, n + 1)
    for k in range(n + 1):
        for i in range(k + 1):
            T[k, i] = fmpq(comb(k, i), comb(n, i))
    return T


def _S(n, a, h):
    """Coefficients of p(a + h X) from those of p(x): S[i', i] = C(i, i') a^(i-i') h^(i')."""
    S = fmpq_mat(n + 1, n + 1)
    apow = [fmpq(1)]
    for _ in range(n):
        apow.append(apow[-1] * a)
    hpow = [fmpq(1)]
    for _ in range(n):
        hpow.append(hpow[-1] * h)
    for i in range(n + 1):
        for ip in range(i + 1):
            S[ip, i] = comb(i, ip) * apow[i - ip] * hpow[ip]
    return S


_TCACHE = {}


def bernstein_coeffs(A, z0, hz, m0, hm):
    n, m = A.nrows() - 1, A.ncols() - 1
    if n not in _TCACHE:
        _TCACHE[n] = _T(n)
    if m not in _TCACHE:
        _TCACHE[m] = _T(m)
    Tn, Tm = _TCACHE[n], _TCACHE[m]
    L = Tn * _S(n, z0, hz)
    R = Tm * _S(m, m0, hm)
    return L * A * R.transpose()


def bernstein_positive(P, zbox=(fmpq(0), fmpq(1)), mubox=(fmpq(0), fmpq(1)), max_leaves=4096,
                       max_dz=10, max_dm=6, verbose=False):
    """Return dict(ok, leaves, min_coeff_seen, failure=None|{'corner':(z,mu),'value':v} | 'cap')."""
    A = P.matrix()
    n, m = A.nrows() - 1, A.ncols() - 1
    stack = [(fmpq(zbox[0]), fmpq(zbox[1]) - fmpq(zbox[0]), 0, fmpq(mubox[0]), fmpq(mubox[1]) - fmpq(mubox[0]), 0)]
    leaves = 0
    visited = 0
    minpos = None
    while stack:
        z0, hz, dz, m0, hm, dm = stack.pop()
        visited += 1
        B = bernstein_coeffs(A, z0, hz, m0, hm)
        corners = [((z0, m0), B[0, 0]), ((z0 + hz, m0), B[n, 0]), ((z0, m0 + hm), B[0, m]),
                   ((z0 + hz, m0 + hm), B[n, m])]
        for pt, v in corners:
            if v < 0:
                return dict(ok=False, leaves=leaves, visited=visited, failure=dict(corner=(str(pt[0]), str(pt[1])),
                                                                                  value=str(v)))
        bmin = min(B[k, l] for k in range(n + 1) for l in range(m + 1))
        if bmin > 0:
            leaves += 1
            minpos = bmin if minpos is None or bmin < minpos else minpos
            if leaves > max_leaves:
                return dict(ok=False, leaves=leaves, visited=visited, failure='cap')
            continue
        if dz >= max_dz and dm >= max_dm:
            return dict(ok=False, leaves=leaves, visited=visited,
                        failure=dict(depth_cap=(str(z0), str(hz), str(m0), str(hm)), bmin=str(bmin)))
        # choose the axis with the larger variation of the Bernstein net (scaled), within depth caps
        vz = max((abs(B[k + 1, l] - B[k, l]) for k in range(n) for l in range(m + 1)), default=fmpq(0)) * n
        vm = max((abs(B[k, l + 1] - B[k, l]) for k in range(n + 1) for l in range(m)), default=fmpq(0)) * m
        split_z = (dm >= max_dm) or (dz < max_dz and vz >= vm)
        if visited + len(stack) > 4 * max_leaves:
            return dict(ok=False, leaves=leaves, visited=visited, failure='cap')
        if split_z:
            h2 = hz / 2
            stack.append((z0 + h2, h2, dz + 1, m0, hm, dm))
            stack.append((z0, h2, dz + 1, m0, hm, dm))
        else:
            h2 = hm / 2
            stack.append((z0, hz, dz, m0 + h2, h2, dm + 1))
            stack.append((z0, hz, dz, m0, h2, dm + 1))
    return dict(ok=True, leaves=leaves, visited=visited, min_leaf_coeff=str(minpos), failure=None)


def self_test(seed=20261023):
    """Bernstein routine checks: corner property, enclosure at random points, known pass/fail cases."""
    rnd = random.Random(seed)
    for trial in range(20):
        n, m = rnd.randint(1, 9), rnd.randint(0, 4)
        P = BiPoly([fmpq_poly([fmpq(rnd.randint(-50, 50), rnd.randint(1, 9)) for _ in range(n + 1)])
                    for _ in range(m + 1)])
        z0, hz = fmpq(rnd.randint(0, 7), 8), fmpq(1, 8)
        m0, hm = fmpq(rnd.randint(0, 3), 4), fmpq(1, 4)
        B = bernstein_coeffs(P.matrix(), z0, hz, m0, hm)
        nn, mm = B.nrows() - 1, B.ncols() - 1
        assert B[0, 0] == P(z0, m0) and B[nn, mm] == P(z0 + hz, m0 + hm), 'corner property'
        assert B[nn, 0] == P(z0 + hz, m0) and B[0, mm] == P(z0, m0 + hm), 'corner property'
        lo = min(B[k, l] for k in range(nn + 1) for l in range(mm + 1))
        hi = max(B[k, l] for k in range(nn + 1) for l in range(mm + 1))
        for _ in range(10):
            zz = z0 + hz * fmpq(rnd.randint(0, 100), 100)
            mu = m0 + hm * fmpq(rnd.randint(0, 100), 100)
            v = P(zz, mu)
            assert lo <= v <= hi, 'enclosure'
    # (z - 1/3)^2 + (mu - 1/2)^2 + 1/1000 > 0 on [0,1]^2 : must certify
    zp = fmpq_poly([fmpq(-1, 3), 1])
    Ppos = BiPoly([zp * zp + fmpq(1, 4) + fmpq(1, 1000), fmpq_poly([-1]), fmpq_poly([1])])
    r1 = bernstein_positive(Ppos)
    assert r1['ok'], r1
    # same minus 1/500 : negative near (1/3, 1/2) : must fail with a negative corner
    Pneg = Ppos - fmpq(1, 500)
    r2 = bernstein_positive(Pneg)
    assert not r2['ok'] and isinstance(r2['failure'], dict), r2
    return dict(ok=True, pos_case=r1, neg_case=r2)
