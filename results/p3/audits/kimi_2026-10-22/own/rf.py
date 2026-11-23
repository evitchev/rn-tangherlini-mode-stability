"""Exact arithmetic in QQ(mu) with denominators factored as
    (mu^2+6)^e1 (mu+1)^e2 (mu+6)^e3
(Kimi's own, for the p3 box certificates).  Constant denominators live in the
numerator's Fraction coefficients.

rf = (num, (e1, e2, e3));  num = dict {exponent: Fraction}.

Also: polynomials in Y (= 1 - z) with rf coefficients, as dict {y_exp: rf}.
"""
from fractions import Fraction

F1 = {0: Fraction(6), 2: Fraction(1)}   # mu^2 + 6
F2 = {0: Fraction(1), 1: Fraction(1)}   # mu + 1
F3 = {0: Fraction(6), 1: Fraction(1)}   # mu + 6
FACTORS = (F1, F2, F3)


# ---------- plain polynomials over QQ (dict exp -> Fraction) ----------

def p_add(a, b):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, Fraction(0)) + v
        if out[k] == 0:
            del out[k]
    return out


def p_neg(a):
    return {k: -v for k, v in a.items()}


def p_sub(a, b):
    return p_add(a, p_neg(b))


def p_mul(a, b):
    out = {}
    for i, vi in a.items():
        for j, vj in b.items():
            out[i + j] = out.get(i + j, Fraction(0)) + vi * vj
    return {k: v for k, v in out.items() if v != 0}


def p_scale(a, c):
    return {k: v * c for k, v in a.items() if v * c != 0}


def p_pow(a, n):
    out = {0: Fraction(1)}
    for _ in range(n):
        out = p_mul(out, a)
    return out


def p_divmod(a, b):
    """Exact division by monic b.  Returns quotient or None if not divisible."""
    a = dict(a)
    db = max(b)
    q = {}
    while a and max(a) >= db:
        k = max(a) - db
        c = a[max(a)] / b[db]
        q[k] = c
        for j, vj in b.items():
            a[k + j] = a.get(k + j, Fraction(0)) - c * vj
            if a[k + j] == 0:
                del a[k + j]
    return (q if not a else None), None


def p_eval(a, t):
    return sum(v * t**k for k, v in a.items())


# ---------- rational functions ----------

def rf_const(c):
    return ({0: Fraction(c)}, (0, 0, 0))


def rf_mul(a, b):
    na, ea = a
    nb, eb = b
    n = p_mul(na, nb)
    e = tuple(x + y for x, y in zip(ea, eb))
    return rf_reduce((n, e))


def rf_reduce(a):
    n, e = a
    e = list(e)
    for i, Fi in enumerate(FACTORS):
        while e[i] > 0:
            q, _ = p_divmod(n, Fi)
            if q is None:
                break
            n = q
            e[i] -= 1
    return (n, tuple(e))


def rf_add(a, b):
    na, ea = a
    nb, eb = b
    E = tuple(max(x, y) for x, y in zip(ea, eb))
    f1 = {0: Fraction(1)}
    f2 = {0: Fraction(1)}
    for i in range(3):
        f1 = p_mul(f1, p_pow(FACTORS[i], E[i] - ea[i]))
        f2 = p_mul(f2, p_pow(FACTORS[i], E[i] - eb[i]))
    n = p_add(p_mul(na, f1), p_mul(nb, f2))
    return rf_reduce((n, E))


def rf_neg(a):
    return (p_neg(a[0]), a[1])


def rf_sub(a, b):
    return rf_add(a, rf_neg(b))


def rf_scale(a, c):
    return (p_scale(a[0], Fraction(c)), a[1])


# ---------- polynomials in Y with rf coefficients ----------

def y_add(A, B):
    out = dict(A)
    for k, v in B.items():
        out[k] = rf_add(out[k], v) if k in out else v
    return out


def y_mul(A, B):
    out = {}
    for i, vi in A.items():
        for j, vj in B.items():
            k = i + j
            prod = rf_mul(vi, vj)
            out[k] = rf_add(out[k], prod) if k in out else prod
    return out


def y_scale_rf(A, r):
    if isinstance(r, Fraction):
        return {k: rf_scale(v, r) for k, v in A.items()}
    return {k: rf_mul(v, r) for k, v in A.items()}


def y_neg(A):
    return {k: rf_neg(v) for k, v in A.items()}


def y_from_P_in_z(Pz):
    """P(z) -> P(1 - Y).  Pz: dict {z_exp: Fraction}."""
    out = {}
    for i, c in Pz.items():
        # (1 - Y)^i
        term = {0: rf_const(c)}
        base = {0: rf_const(1), 1: rf_const(-1)}  # 1 - Y
        p = {0: rf_const(1)}
        for _ in range(i):
            p = y_mul(p, base)
        out = y_add(out, y_scale_rf(p, c))
    return out


def y_negYPY(PY):
    """Given P as Y-dict, return -Y * dP/dY  (= (1-z) dP/dz)."""
    out = {}
    for j, c in PY.items():
        if j >= 1:
            out[j] = rf_scale(c, -Fraction(j))
    return out


def common_den(A):
    E = [0, 0, 0]
    for v in A.values():
        for i in range(3):
            E[i] = max(E[i], v[1][i])
    return tuple(E)


def den_poly(E):
    d = {0: Fraction(1)}
    for i in range(3):
        d = p_mul(d, p_pow(FACTORS[i], E[i]))
    return d


def clear(A, E):
    """Multiply every coefficient by Den = prod F_i^E_i; result: dict {y: (numpoly in mu)}."""
    out = {}
    for k, (n, e) in A.items():
        f = {0: Fraction(1)}
        for i in range(3):
            f = p_mul(f, p_pow(FACTORS[i], E[i] - e[i]))
        out[k] = p_mul(n, f)
    return out
