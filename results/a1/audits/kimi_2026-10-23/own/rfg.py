"""Exact QQ(mu) arithmetic with per-ell denominator factors (Kimi, a1 audit).

For general ell (D = 6): the parametrisation brings in
    A(mu) = (ell-1) mu^2 + (ell+4)     [denominator of s = 1 + 2 m delta, w]
    B(mu) = (ell-1) mu + (ell+4)       [denominator of x_H = 2A/((mu+1) B)]
    C(mu) = mu + 1
An rf is (num, (eA, eB, eC)) with num a dict {exp: Fraction}; constant denominators
live in the numerators.  Same design as my p3-onset rf.py (validated there).
"""
from fractions import Fraction


class Ctx:
    def __init__(self, ell):
        self.ell = ell
        self.A = {0: Fraction(ell + 4), 2: Fraction(ell - 1)}
        self.B = {0: Fraction(ell + 4), 1: Fraction(ell - 1)}
        self.C = {0: Fraction(1), 1: Fraction(1)}
        self.FACTORS = (self.A, self.B, self.C)

    # ---- polynomials over QQ (dicts) ----
    @staticmethod
    def p_add(a, b):
        out = dict(a)
        for k, v in b.items():
            out[k] = out.get(k, Fraction(0)) + v
            if out[k] == 0:
                del out[k]
        return out

    @staticmethod
    def p_neg(a):
        return {k: -v for k, v in a.items()}

    def p_sub(self, a, b):
        return self.p_add(a, self.p_neg(b))

    @staticmethod
    def p_mul(a, b):
        out = {}
        for i, vi in a.items():
            for j, vj in b.items():
                out[i + j] = out.get(i + j, Fraction(0)) + vi * vj
        return {k: v for k, v in out.items() if v != 0}

    @staticmethod
    def p_scale(a, c):
        return {k: v * c for k, v in a.items() if v * c != 0}

    def p_pow(self, a, n):
        out = {0: Fraction(1)}
        for _ in range(n):
            out = self.p_mul(out, a)
        return out

    @staticmethod
    def p_eval(a, t):
        return sum(v * t**k for k, v in a.items())

    @staticmethod
    def p_div_exact(a, b):
        """quotient if b divides a exactly over QQ, else None"""
        a = dict(a)
        db = max(b)
        lb = b[db]
        q = {}
        while a and max(a) >= db:
            k = max(a) - db
            c = a[max(a)] / lb
            q[k] = c
            for j, vj in b.items():
                a[k + j] = a.get(k + j, Fraction(0)) - c * vj
                if a[k + j] == 0:
                    del a[k + j]
        return q if not a else None

    # ---- rational functions ----
    def rf_const(self, c):
        return ({0: Fraction(c)}, (0, 0, 0))

    def rf_reduce(self, a):
        n, e = a
        e = list(e)
        for i, Fi in enumerate(self.FACTORS):
            while e[i] > 0:
                q = self.p_div_exact(n, Fi)
                if q is None:
                    break
                n = q
                e[i] -= 1
        return (n, tuple(e))

    def rf_mul(self, a, b):
        n = self.p_mul(a[0], b[0])
        e = tuple(x + y for x, y in zip(a[1], b[1]))
        return self.rf_reduce((n, e))

    def rf_add(self, a, b):
        na, ea = a
        nb, eb = b
        E = tuple(max(x, y) for x, y in zip(ea, eb))
        f1 = {0: Fraction(1)}
        f2 = {0: Fraction(1)}
        for i in range(3):
            f1 = self.p_mul(f1, self.p_pow(self.FACTORS[i], E[i] - ea[i]))
            f2 = self.p_mul(f2, self.p_pow(self.FACTORS[i], E[i] - eb[i]))
        n = self.p_add(self.p_mul(na, f1), self.p_mul(nb, f2))
        return self.rf_reduce((n, E))

    def rf_neg(self, a):
        return (self.p_neg(a[0]), a[1])

    def rf_sub(self, a, b):
        return self.rf_add(a, self.rf_neg(b))

    def rf_scale(self, a, c):
        return (self.p_scale(a[0], Fraction(c)), a[1])

    # ---- polynomials in t with rf coefficients ----
    def y_add(self, A_, B_):
        out = dict(A_)
        for k, v in B_.items():
            out[k] = self.rf_add(out[k], v) if k in out else v
        return out

    def common_den(self, A_):
        E = [0, 0, 0]
        for v in A_.values():
            for i in range(3):
                E[i] = max(E[i], v[1][i])
        return tuple(E)

    def den_poly(self, E):
        d = {0: Fraction(1)}
        for i in range(3):
            d = self.p_mul(d, self.p_pow(self.FACTORS[i], E[i]))
        return d

    def clear(self, A_, E):
        out = {}
        for k, (n, e) in A_.items():
            f = {0: Fraction(1)}
            for i in range(3):
                f = self.p_mul(f, self.p_pow(self.FACTORS[i], E[i] - e[i]))
            out[k] = self.p_mul(n, f)
        return out
