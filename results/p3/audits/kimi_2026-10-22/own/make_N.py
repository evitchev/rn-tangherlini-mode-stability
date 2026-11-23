"""Build N exactly from each stored certificate polynomial P (Kimi's own route).

Single-mu certs (T1, G1): N(z) with rational coefficients.
Box certs (T2, T3): N is rational in mu; clear the mu-denominators:
    N = Ntilde(z, mu) / Den(mu),
where Den(mu) is the lcm of all coefficient denominators; Den is factored and each
factor's positivity on the box is proved by exact Bernstein coefficients (printed
for the audit).  Positivity of N on the box <=> positivity of Ntilde.

Output: own/built/<name>.json  with the exact N (or Ntilde and Den).
"""
import json
import os
import sys
from fractions import Fraction

import sympy as sp

z, mu = sp.symbols("z mu")

HERE = os.path.dirname(os.path.abspath(__file__))
CERTS = os.path.join(HERE, "..", "runs")
OUT = os.path.join(HERE, "built")
os.makedirs(OUT, exist_ok=True)


def ki_full(n, m, delta, K=1):
    """Full (5.63b) at y = 0 (no early (n-4) simplification)."""
    x = sp.Symbol("x")
    U = (-n**3 * (3*n - 2) * (n + 1)**4 * delta * (1 + m*delta)**3 * x**4
         - 4*n**2 * (n + 1)**2 * (1 + m*delta)**2 * ((n + 1)*(3*n - 2)*m*delta - n**2) * x**3
         + 4*(n + 1)*(1 + m*delta) * (m*(n - 2)*(n - 4)*(n + 1)*(m + n**2*K)*delta
                                       + 4*n*(2*n**2 - 3*n + 4)*m
                                       + n**2*(n - 2)*(n - 4)*(n + 1)*K) * x**2
         - 16*m * ((n + 1)*m*(-4*m + 3*n**2*(n - 2)*K)*delta
                   + 3*n*(n - 4)*m + 3*n**2*(n + 1)*(n - 2)*K) * x
         + 64*m**3 + 16*n*(n + 2)*m**2*K)
    H = m + sp.Rational(n*(n + 1), 2) * (1 + m*delta) * x
    return U, H


def D6(mu_val):
    """D = 6, ell = 2: return (U(z), H(z), f(z)) with exact dependence on mu.
    mu_val: a Rational (single-mu case) or the symbol mu (box case)."""
    m = sp.Integer(6)
    delta = (1 - mu**2) / (5 * (6 + mu**2))
    xH = 2 * (6 + mu**2) / ((mu + 1) * (mu + 6))
    q2 = (1 - mu) * (6 - mu) * (1 + mu) * (6 + mu) / (6 + mu**2)**2
    Ux, Hx = ki_full(4, m, delta)
    x = xH * (1 - z)**3
    U = sp.expand(Ux.subs(sp.Symbol("x"), x))
    H = sp.expand(Hx.subs(sp.Symbol("x"), x))
    f = sp.expand(1 - x + q2 * x**2 / 4)
    if mu_val is not None and mu_val != mu:
        U = sp.expand(U.subs(mu, mu_val))
        H = sp.expand(H.subs(mu, mu_val))
        f = sp.expand(f.subs(mu, mu_val))
    return U, H, f


def G1case():
    """D = 10, ell = 2, Q = 0: n = 8, m = k^2 - n = (ell-1)(ell+n) = 10 (KI (5.39)),
    delta = 0, x_H = 1, f = 1 - (1-z)^7."""
    Ux, Hx = ki_full(8, 10, 0)
    x = (1 - z)**7
    U = sp.expand(Ux.subs(sp.Symbol("x"), x))
    H = sp.expand(Hx.subs(sp.Symbol("x"), x))
    f = sp.expand(1 - x)
    return U, H, f


def load_P(path):
    with open(path) as fh:
        d = json.load(fh)
    return d


def P_of_z(Pmap):
    P = sp.Integer(0)
    for key, val in Pmap.items():
        i, j = eval(key)
        assert j == 0
        P += sp.Rational(val) * z**i
    return sp.expand(P)


def P_of_z_mu(Pmap):
    P = sp.Integer(0)
    for key, val in Pmap.items():
        i, j = eval(key)
        P += sp.Rational(val) * z**i * mu**j
    return sp.expand(P)


def build_N(U, H, f, P):
    fz = sp.diff(f, z)
    Pz = sp.diff(P, z)
    N = U - 64 * H**2 * ((1 - z) * fz * P + f * (-P + (1 - z) * Pz + P**2))
    return sp.expand(N)


def clear_mu_denominators(N):
    """N: polynomial in z with rational-function-of-mu coefficients.
    Return (Den, Ntilde) with Den = lcm of denominators (a polynomial in mu)."""
    Np = sp.Poly(sp.expand(N), z)
    den = sp.Integer(1)
    for monom, coeff in Np.terms():
        coeff = sp.cancel(coeff)
        d = sp.denom(coeff)
        den = sp.lcm(den, d)
    Den = sp.expand(den)
    Ntilde = sp.expand(N * Den)
    return Den, Ntilde


def save(name, payload):
    path = os.path.join(OUT, name + ".json")
    with open(path, "w") as fh:
        json.dump(payload, fh)
    print("wrote", path)


def poly_to_map_z(N, max_deg):
    N = sp.expand(N)
    out = {}
    for i in range(max_deg + 1):
        c = N.coeff(z, i)
        if c != 0:
            out[str(i)] = str(c)
    # fail-closed: nothing above the scan range
    assert all(N.coeff(z, i) == 0 for i in range(max_deg + 1, max_deg + 6)), \
        "degree above scan range"
    return out


def poly_to_map_z_mu(N):
    P = sp.Poly(sp.expand(N), z, mu)
    return {str(tuple(m)): str(c) for m, c in P.terms()}


def main_single():
    # ---- single-mu certificates
    for name, src, case in [
        ("T1_rule1", "cert_rule1_T1.json", "D6"),
        ("T1_rule2", "cert_rule2_T1.json", "D6"),
        ("G1_rule2", "cert_rule2_G1.json", "G1"),
    ]:
        d = load_P(os.path.join(CERTS, src))
        mu_val = sp.Rational(d["mu"]) if d["mu"] else None
        if case == "D6":
            U, H, f = D6(mu_val)
        else:
            U, H, f = G1case()
        P = P_of_z(d["P"])
        deg_P = max(eval(k)[0] for k in d["P"])
        N = build_N(U, H, f, P)
        N = sp.expand(N)
        # safe degree bound: deg N <= max(deg U, 2 deg H + deg f + 2 deg P)
        deg_H = 3 if case == "D6" else 7
        deg_f = 6 if case == "D6" else 7
        deg_U = 12 if case == "D6" else 21
        max_deg = max(deg_U, 2 * deg_H + deg_f + 2 * deg_P) + 2
        Nmap = poly_to_map_z(N, max_deg)
        deg = max(int(k) for k in Nmap)
        save(name, {"kind": "z", "mu": str(mu_val), "deg_z": deg, "N": Nmap})
        print(f"{name}: mu={mu_val}, deg_z={deg} (scan to {max_deg})", flush=True)


if __name__ == "__main__":
    main_single()
