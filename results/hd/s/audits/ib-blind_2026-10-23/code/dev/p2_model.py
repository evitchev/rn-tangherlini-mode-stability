"""p2_model.py -- ib-blind phase 2: the n = 5, l = 2 model built from the frozen transcription.

Single source of truth: code/ki_s5.py (frozen, sha256 b2585fb0...). U_- and H_- coefficients are
extracted from it with sympy at run time, honouring IB_TAMPER (TP2 drill) exactly like the guard.

  f(rho)  = (1 - rho^-4)(1 - kap rho^-4),  kap = (1-w)/(1+w)   (= 1 - x + q^2 x^2/4, x = x_H rho^-4)
  W(rho)  = U_-(x)/(64 rho^2 H_-(x)^2)                          (= V/f), units r_H = 1
  ODE     : (f psi')' = W psi  (' = d/drho),  chi := f psi' = dpsi/dr*
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.dirname(HERE)                 # .../code  (frozen phase-1 modules live here)
if CODE not in sys.path:
    sys.path.insert(0, CODE)

import sympy as sp            # noqa: E402
import mpmath as mp           # noqa: E402
import ki_s5 as ki            # noqa: E402
import check_transcription as ct  # noqa: E402

TAMPER = os.environ.get('IB_TAMPER') or None


# ----------------------------------------------------------------------------- guard (TP2)
def guard():
    """Run C1-C10 of the frozen check_transcription on the U_- this process will use; abort on FAIL."""
    t = TAMPER
    res = {'C1': ct.C1(t), 'C2': ct.C2(t), 'C3': ct.C3(t), 'C4': ct.C4(t), 'C5': ct.C5(),
           'C6': ct.C6(t)[0], 'C7': ct.C7()[0], 'C8': ct.C8(t, verbose=False)[0], 'C9': ct.C9(),
           'C10': ct.C10(t, verbose=False)[0]}
    ok = all(bool(v) for v in res.values())
    print('GUARD tamper=%s %s -> %s' % (t, {k: bool(v) for k, v in res.items()}, 'PASS' if ok else 'FAIL'),
          flush=True)
    if not ok:
        print('GUARD ABORT: transcription checks failed; nothing computed.', flush=True)
        sys.exit(3)
    return res


# ----------------------------------------------------------------------------- node gate (A1)
def node_gate(requested=8):
    load1 = float(open('/proc/loadavg').read().split()[0])
    nproc = os.cpu_count()
    mem = {}
    for line in open('/proc/meminfo'):
        k, v = line.split(':', 1)
        mem[k.strip()] = int(v.strip().split()[0])
    avail_gb = mem['MemAvailable'] / 1024.0 / 1024.0
    w = min(int(requested), 8, nproc - 2 - int(math.ceil(load1)))
    while w >= 1 and avail_gb < 16 + 2 * w:
        w -= 1
    ok = w >= 1
    info = dict(load1=load1, nproc=nproc, mem_available_gb=round(avail_gb, 2), requested=int(requested), w=w,
                rule='w <= min(8, nproc-2-ceil(load1)); MemAvailable >= 16 GB + 2 GB*w', ok=ok)
    print('GATE %s' % info, flush=True)
    return ok, info


# ----------------------------------------------------------------------------- coefficients
_dl, _xx = sp.symbols('delta x')


def _coeff_table(expr):
    P = sp.Poly(sp.expand(expr), _xx)
    out = []
    for k in range(P.degree() + 1):
        ck = sp.Poly(P.coeff_monomial(_xx**k), _dl)
        cs = [sp.Integer(c) for c in reversed(ck.all_coeffs())]
        assert all(c.is_Integer for c in cs)
        out.append([int(c) for c in cs])
    return out


UC = _coeff_table(ki.U_minus(n=5, m=7, d=_dl, x=_xx, y=0, K=1, tamper=TAMPER))   # U_- = sum_k (sum_j UC[k][j] d^j) x^k
HC = _coeff_table(ki.H_minus(n=5, m=7, d=_dl, x=_xx))                            # H_- = 7 + (15 + 105 d) x


def _pv(cs, t):
    s = 0
    for c in reversed(cs):
        s = s * t + c
    return s


# ----------------------------------------------------------------------------- parameters
def params_from_q(q):
    """mpmath, current precision. q: string/int/mpf."""
    q = mp.mpf(q) if not isinstance(q, mp.mpf) else q
    w = mp.sqrt(1 - q * q)
    s = mp.sqrt(1 + 7 * q * q / 9)
    return w, (s - 1) / 14


def params_from_mu(mu):
    """mu: fractions.Fraction or (p, q) -> exact (w, delta) as Fractions."""
    from fractions import Fraction as Fr
    mu = Fr(mu)
    A = 7 + mu * mu
    return Fr(8) * mu / A, (1 - mu * mu) / (6 * A)


def q_from_mu(mu):
    from fractions import Fraction as Fr
    w, _ = params_from_mu(mu)
    return mp.sqrt(mp.mpf(1) - mp.mpf(w.numerator) ** 2 / mp.mpf(w.denominator) ** 2)


class ModelMP:
    """mpmath model at the current precision. well: amplitude A of -A*16(rho-1)^2(2-rho)^2 on [1,2] (NEG1)."""

    def __init__(self, w, delta, well=None):
        to = (lambda v: mp.mpf(v.numerator) / v.denominator) if hasattr(w, 'numerator') else mp.mpf
        self.w = to(w)
        self.delta = to(delta)
        self.kap = (1 - self.w) / (1 + self.w)
        self.xH = 2 / (1 + self.w)
        self.U = [_pv([mp.mpf(c) for c in cs], self.delta) for cs in UC]
        self.H = [_pv([mp.mpf(c) for c in cs], self.delta) for cs in HC]
        self.well = None if well is None else mp.mpf(well)
        self.R = 1 - self.kap ** (mp.mpf(1) / 4) if self.kap > 0 else mp.mpf(1)

    def f(self, rho):
        r4 = 1 / rho**4
        return (1 - r4) * (1 - self.kap * r4)

    def W(self, rho):
        x = self.xH / rho**4
        U = _pv(self.U, x)
        H = _pv(self.H, x)
        val = U / (64 * rho**2 * H**2)
        if self.well is not None and rho < 2:
            val -= self.well * 16 * (rho - 1)**2 * (2 - rho)**2
        return val

    # ---- power series in t = rho - 1 (truncated at order K) ----
    @staticmethod
    def _mul(a, b, K):
        return [mp.fsum(a[i] * b[k - i] for i in range(k + 1)) for k in range(K + 1)]

    @staticmethod
    def _inv(a, K):
        out = [1 / a[0]]
        for k in range(1, K + 1):
            out.append(-mp.fsum(a[i] * out[k - i] for i in range(1, k + 1)) / a[0])
        return out

    def series(self, K):
        """Taylor data (g, W) at t = 0, where f = t g."""
        rinv4 = [(-1)**k * mp.binomial(k + 3, 3) for k in range(K + 1)]
        rinv2 = [(-1)**k * (k + 1) for k in range(K + 1)]
        om = [(-1)**k * mp.binomial(k + 4, 3) for k in range(K + 1)]        # (1 - (1+t)^-4)/t
        fac = [1 - self.kap * rinv4[0]] + [-self.kap * rinv4[k] for k in range(1, K + 1)]
        g = self._mul(om, fac, K)
        x = [self.xH * c for c in rinv4]
        U = [mp.mpf(0)] * (K + 1)
        for c in reversed(self.U):                                           # Horner in series
            U = self._mul(U, x, K)
            U[0] += c
        H = [self.H[0] + self.H[1] * x[0]] + [self.H[1] * x[k] for k in range(1, K + 1)]
        Wser = self._mul(self._mul(U, rinv2, K), self._inv(self._mul(H, H, K), K), K)
        Wser = [c / 64 for c in Wser]
        if self.well is not None:                                            # -16A (t^2 - 2t^3 + t^4)
            for k, c in ((2, -16), (3, 32), (4, -16)):
                if k <= K:
                    Wser[k] += c * self.well
        return g, Wser

    def frobenius(self, K):
        """Coefficients a_N of the solution analytic at t = 0 with a_0 = 1 (double exponent 0)."""
        g, Wser = self.series(K)
        a = [mp.mpf(1)]
        for N in range(1, K + 1):
            s1 = mp.fsum(a[k] * Wser[N - 1 - k] for k in range(N))
            s2 = mp.fsum(k * a[k] * g[N - k] for k in range(1, N))
            a.append((s1 - N * s2) / (N * N * g[0]))
        return a, g, Wser

    def start(self, K, t0):
        a, g, Wser = self.frobenius(K)
        psi = mp.fsum(a[k] * t0**k for k in range(K + 1))
        dpsi = mp.fsum(k * a[k] * t0**(k - 1) for k in range(1, K + 1))
        tail = abs(a[K]) * t0**K
        return psi, self.f(1 + t0) * dpsi, dict(a=a, g0=g[0], W0=Wser[0], tail_term=tail)


class ModelF:
    """Plain-float model (integrator II); separate code path from ModelMP."""

    def __init__(self, w, delta, well=None):
        self.w = float(w)
        self.delta = float(delta)
        self.kap = (1 - self.w) / (1 + self.w)
        self.xH = 2 / (1 + self.w)
        self.U = [_pv([float(c) for c in cs], self.delta) for cs in UC]
        self.H = [_pv([float(c) for c in cs], self.delta) for cs in HC]
        self.well = None if well is None else float(well)

    def f(self, rho):
        r4 = rho**-4
        return (1 - r4) * (1 - self.kap * r4)

    def W(self, rho):
        x = self.xH * rho**-4
        U = _pv(self.U, x)
        H = _pv(self.H, x)
        val = U / (64 * rho * rho * H * H)
        if self.well is not None and rho < 2:
            val -= self.well * 16 * (rho - 1)**2 * (2 - rho)**2
        return val

    def start(self, K, t0):
        """Float Frobenius series of order K (own implementation, float arithmetic)."""
        from math import comb
        rinv4 = [(-1)**k * comb(k + 3, 3) for k in range(K + 1)]
        rinv2 = [(-1)**k * (k + 1) for k in range(K + 1)]
        om = [(-1)**k * comb(k + 4, 3) for k in range(K + 1)]

        def mul(a, b):
            return [sum(a[i] * b[k - i] for i in range(k + 1)) for k in range(K + 1)]

        def inv(a):
            out = [1 / a[0]]
            for k in range(1, K + 1):
                out.append(-sum(a[i] * out[k - i] for i in range(1, k + 1)) / a[0])
            return out
        fac = [1 - self.kap] + [-self.kap * rinv4[k] for k in range(1, K + 1)]
        g = mul(om, fac)
        x = [self.xH * c for c in rinv4]
        U = [0.0] * (K + 1)
        for c in reversed(self.U):
            U = mul(U, x)
            U[0] += c
        H = [self.H[0] + self.H[1] * x[0]] + [self.H[1] * x[k] for k in range(1, K + 1)]
        Wser = [c / 64 for c in mul(mul(U, rinv2), inv(mul(H, H)))]
        if self.well is not None:
            for k, c in ((2, -16), (3, 32), (4, -16)):
                Wser[k] += c * self.well
        a = [1.0]
        for N in range(1, K + 1):
            s1 = sum(a[k] * Wser[N - 1 - k] for k in range(N))
            s2 = sum(k * a[k] * g[N - k] for k in range(1, N))
            a.append((s1 - N * s2) / (N * N * g[0]))
        psi = sum(a[k] * t0**k for k in range(K + 1))
        dpsi = sum(k * a[k] * t0**(k - 1) for k in range(1, K + 1))
        return psi, self.f(1 + t0) * dpsi
