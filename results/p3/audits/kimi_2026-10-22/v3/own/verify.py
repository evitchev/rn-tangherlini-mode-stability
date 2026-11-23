"""Kimi's own exact positivity verifier (fail-closed).

Method: exact Bernstein coefficients with adaptive bisection, in exact rational
arithmetic (python-flint fmpq as bignum only; the algorithm is mine).

1D: p(z) = sum_j c_j z^j on [za, zb] (exact rationals).  Map to [0,1], Bernstein
coefficients b_i = sum_{j<=i} c_j C(i,j)/C(d,j).
  - min b_i > 0  =>  p >= min b_i > 0 on the closed interval: POSITIVE.
  - some b_i < 0  =>  evaluate p at the box centre exactly; if < 0: REJECT with the
    exact counterexample point; else bisect.
  - node cap exceeded: INCONCLUSIVE, which is a REJECT (fail-closed).

2D: tensor product on [0,1]x[0,1] after mapping the mu-box; same logic, bisect the
variable with the larger Bernstein spread.

Known-answer tests (control c): -1, z - 1/2, z(1-z) must all REJECT; 1 + z + z^2
must verify.  A tampered copy (accept threshold min > -1 instead of > 0) must be
caught by KAT-1.
"""
import json
import math
import os
import sys

from flint import fmpq

HERE = os.path.dirname(os.path.abspath(__file__))


# ---------- polynomials as dicts of fmpq ----------

def poly1_from_map(coeffs):
    return {int(i): fmpq(v) for i, v in coeffs.items()}


def poly2_from_map(coeffs):
    out = {}
    for key, v in coeffs.items():
        i, j = eval(key)
        out[(i, j)] = fmpq(v)
    return out


def scale_to_int_1d(p):
    den = 1
    for c in p.values():
        den = math.lcm(den, int(c.denominator))
    out = {}
    for i, c in p.items():
        t = c * den
        assert t.denominator == 1
        out[i] = int(t.numerator)
    return out, den


def scale_to_int_2d(p):
    den = 1
    for c in p.values():
        den = math.lcm(den, int(c.denominator))
    out = {}
    for ij, c in p.items():
        t = c * den
        assert t.denominator == 1
        out[ij] = int(t.numerator)
    return out, den


def substitute_1d(p, a, b):
    """z -> a + (b-a) t, exact."""
    h = b - a
    out = {}
    for j, c in p.items():
        for k in range(j + 1):
            out[k] = out.get(k, fmpq(0)) + c * math.comb(j, k) * a**(j - k) * h**k
    return out


def substitute_2d(p, za, zb, ma, mb):
    hz = zb - za
    hm = mb - ma
    out = {}
    for (i, j), c in p.items():
        for k in range(i + 1):
            for l in range(j + 1):
                key = (k, l)
                out[key] = out.get(key, fmpq(0)) + (
                    c * math.comb(i, k) * math.comb(j, l)
                    * za**(i - k) * ma**(j - l) * hz**k * hm**l)
    return out


def bernstein_1d(pint, d):
    """Integer-coefficient polynomial of degree <= d -> integer-scaled Bernstein
    coefficients beta_i = b_i * L where L = lcm_j C(d, j)  (positivity invariant)."""
    L = 1
    for j in range(d + 1):
        L = math.lcm(L, math.comb(d, j))
    beta = []
    for i in range(d + 1):
        s = 0
        ci = math.comb  # shorthand
        for j, c in pint.items():
            if j <= i:
                s += c * ci(i, j) * (L // ci(d, j))
        beta.append(s)
    return beta, L


def bernstein_2d(pint, d1, d2):
    L1 = 1
    for j in range(d1 + 1):
        L1 = math.lcm(L1, math.comb(d1, j))
    L2 = 1
    for j in range(d2 + 1):
        L2 = math.lcm(L2, math.comb(d2, j))
    beta = {}
    for i1 in range(d1 + 1):
        for i2 in range(d2 + 1):
            s = 0
            for (j1, j2), c in pint.items():
                if j1 <= i1 and j2 <= i2:
                    s += c * math.comb(i1, j1) * math.comb(i2, j2) \
                        * (L1 // math.comb(d1, j1)) * (L2 // math.comb(d2, j2))
            beta[(i1, i2)] = s
    return beta, L1 * L2


def eval_1d(p, t):
    return sum(c * t**i for i, c in p.items())


def eval_2d(p, t, s):
    return sum(c * t**i * s**j for (i, j), c in p.items())


# ---------- verifiers ----------

NODE_CAP = 200000


def verify_1d(p, a, b, tamper_margin=0):
    """Prove p > 0 on [a, b].  Returns (True, info) or (False, witness)."""
    stack = [(a, b)]
    nodes = 0
    min_margin = None
    while stack:
        za, zb = stack.pop()
        nodes += 1
        if nodes > NODE_CAP:
            return False, {"reason": "node cap exceeded (strict positivity not decided)",
                           "nodes": nodes}
        ps = substitute_1d(p, za, zb)
        d = max(ps)
        pint, den = scale_to_int_1d(ps)
        beta, L = bernstein_1d(pint, d)
        m = min(beta)
        margin = fmpq(m, L) / den          # true min Bernstein coefficient on this box
        if m > tamper_margin:
            if min_margin is None or margin < min_margin:
                min_margin = margin        # min over ACCEPTED boxes only
            continue
        # possible failure: evaluate at the box centre and at the argmin node
        c_mid = eval_1d(p, (za + zb) / 2)
        if c_mid <= 0:
            return False, {"reason": "negative value",
                           "z": str((za + zb) / 2), "value": str(c_mid)}
        i_min = beta.index(m)
        t_node = fmpq(i_min, d)
        z_node = za + (zb - za) * t_node
        v_node = eval_1d(p, z_node)
        if v_node <= 0:
            return False, {"reason": "non-positive value at Bernstein node",
                           "z": str(z_node), "value": str(v_node)}
        stack.append((za, (za + zb) / 2))
        stack.append(((za + zb) / 2, zb))
    return True, {"nodes": nodes, "min_bernstein_coeff": str(min_margin)}


def verify_2d(p, za, zb, ma, mb, tamper_margin=0):
    stack = [(za, zb, ma, mb)]
    nodes = 0
    while stack:
        box = stack.pop()
        nodes += 1
        if nodes > NODE_CAP:
            return False, {"reason": "node cap exceeded", "nodes": nodes}
        ps = substitute_2d(p, *box)
        d1 = max(i for i, _ in ps)
        d2 = max(j for _, j in ps)
        pint, den = scale_to_int_2d(ps)
        beta, _ = bernstein_2d(pint, d1, d2)
        m = min(beta.values())
        if m > tamper_margin:
            continue
        c_mid = eval_2d(p, (box[0] + box[1]) / 2, (box[2] + box[3]) / 2)
        if c_mid <= 0:
            return False, {"reason": "negative value",
                           "z": str((box[0] + box[1]) / 2),
                           "mu": str((box[2] + box[3]) / 2),
                           "value": str(c_mid)}
        (i_min, j_min) = min(beta, key=lambda k: beta[k])
        z_node = box[0] + (box[1] - box[0]) * fmpq(i_min, d1)
        m_node = box[2] + (box[3] - box[2]) * fmpq(j_min, d2)
        v_node = eval_2d(p, z_node, m_node)
        if v_node <= 0:
            return False, {"reason": "non-positive value at Bernstein node",
                           "z": str(z_node), "mu": str(m_node),
                           "value": str(v_node)}
        # bisect along the larger spread
        bz = [beta[(i, j)] for i in range(d1 + 1) for j in (0, d2)]
        bm = [beta[(i, j)] for i in (0, d1) for j in range(d2 + 1)]
        zspread = max(bz) - min(bz)
        mspread = max(bm) - min(bm)
        za2, zb2, ma2, mb2 = box
        if zspread >= mspread:
            zm = (za2 + zb2) / 2
            stack.append((za2, zm, ma2, mb2))
            stack.append((zm, zb2, ma2, mb2))
        else:
            mm = (ma2 + mb2) / 2
            stack.append((za2, zb2, ma2, mm))
            stack.append((za2, zb2, mm, mb2))
    return True, {"nodes": nodes}


# ---------- known-answer tests ----------

def kat():
    res = {}
    ok1, info1 = verify_1d({0: fmpq(-1)}, fmpq(0), fmpq(1))
    res["KAT1 p=-1 must REJECT"] = (not ok1, info1)
    ok2, info2 = verify_1d({1: fmpq(1), 0: fmpq(-1, 2)}, fmpq(0), fmpq(1))
    res["KAT2 p=z-1/2 must REJECT"] = (not ok2, info2)
    ok3, info3 = verify_1d({1: fmpq(1), 2: fmpq(-1)}, fmpq(0), fmpq(1))
    res["KAT3 p=z(1-z) strict must REJECT"] = (not ok3, info3)
    ok4, info4 = verify_1d({0: fmpq(1), 1: fmpq(1), 2: fmpq(1)}, fmpq(0), fmpq(1))
    res["KAT4 p=1+z+z^2 must PASS"] = (ok4, info4)
    # code tamper: accept margin corrupted
    okT, infoT = verify_1d({0: fmpq(-1)}, fmpq(0), fmpq(1), tamper_margin=-2)
    res["KAT5 tampered verifier accepts p=-1 (must be caught here)"] = (okT is True, infoT)
    # KAT6: substitution identity 1D.  p = z^2 - z + 3 on [1/2, 1]: z = 1/2 + t/2 gives
    # p = t^2/4 + 11/4 exactly.
    s6 = substitute_1d({2: fmpq(1), 1: fmpq(-1), 0: fmpq(3)}, fmpq(1, 2), fmpq(1))
    ok6 = {k: v for k, v in s6.items() if v} == {2: fmpq(1, 4), 0: fmpq(11, 4)}
    res["KAT6 substitute_1d coefficients exact"] = (ok6, {k: str(v) for k, v in s6.items()})
    # KAT7: substitution identity 2D.  p = t^2 mu on t in [1/2,1], mu in [2,3]:
    # t = 1/2 + t'/2, mu = 2 + mu'  =>  p = (1/4 + t'/2 + t'^2/4)(2 + mu').
    s7 = substitute_2d({(2, 1): fmpq(1)}, fmpq(1, 2), fmpq(1), fmpq(2), fmpq(3))
    want7 = {(0, 0): fmpq(1, 2), (1, 0): fmpq(1), (2, 0): fmpq(1, 2),
             (0, 1): fmpq(1, 4), (1, 1): fmpq(1, 2), (2, 1): fmpq(1, 4)}
    ok7 = s7 == want7
    res["KAT7 substitute_2d coefficients exact"] = (ok7, {k: str(v) for k, v in s7.items()})
    # KAT8: end-to-end on a non-unit box: p = t - 5/8 on t in [1/2, 3/4] is negative at the
    # left corner (p(1/2) = -1/8); the substituted constant coefficient must be -1/8.
    s8 = substitute_1d({1: fmpq(1), 0: fmpq(-5, 8)}, fmpq(1, 2), fmpq(3, 4))
    ok8, info8 = verify_1d({1: fmpq(1), 0: fmpq(-5, 8)}, fmpq(1, 2), fmpq(3, 4))
    res["KAT8 non-unit box rejection at corner"] = ((not ok8) and s8.get(0) == fmpq(-1, 8),
                                                    {k: str(v) for k, v in s8.items()})
    for k, (good, info) in res.items():
        print(("PASS " if good else "FAIL ") + k + "  " + str(info)[:100])
    return all(g for g, _ in res.values())


if __name__ == "__main__":
    if kat():
        print("KAT SUITE OK")
    else:
        print("KAT SUITE FAILURE")
        sys.exit(1)
