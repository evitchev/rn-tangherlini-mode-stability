"""ki_s5.py -- my own transcription (ib-blind seat, 2026-10-23) of
Kodama-Ishibashi, hep-th/0308128 v4 (= S5), eqs. (2.19), (5.38)-(5.40),
(5.58), (5.60)-(5.63), (5.65)-(5.66), read with pdftotext only
(layout, raw and bbox modes; see TRANSCRIPTION.md for the glyph-position
evidence of every large delimiter), and of Kodama-Ishibashi Paper I,
hep-th/0305147 v3, eqs. (3.2)-(3.7) (the Q = 0 potential).

Symbols (S5 notation):
  n      : D = n + 2
  m      : m = k^2 - n K                          (5.39); K = 1: k^2 = l(l+n-1) (2.3)
  d      : delta, mu_S5 = (1 + 2 m delta) M      (5.60), mu_S5^2 = M^2 + 4 m Q^2/(n+1)^2 (5.58)
  x, y   : x = 2M/r^(n-1), y = lambda r^2        (5.40)
  z      : z = Q^2/r^(2n-2)                       (5.40)
  K      : sectional curvature sign of K^n
  f      : f = K - y - x + z                      (2.19)
NOTE the notation collision: S5's mu (here mu_S5) is NOT TARGET_HD's rational
parameter mu (called mu_T in this workspace).

No code from bh-modes or anyone else was used.
"""
import sympy as sp

n, m, d, x, y, K, z = sp.symbols('n m delta x y K z')


# ---------------- S5 (hep-th/0308128 v4) ----------------
def H_plus(n=n, m=m, d=d, x=x):
    """S5 (5.62a): H_+ = 1 - n(n+1)/2 * delta * x."""
    return 1 - sp.Rational(1, 2) * n * (n + 1) * d * x


def H_minus(n=n, m=m, d=d, x=x):
    """S5 (5.62b): H_- = m + n(n+1)/2 * (1 + m delta) * x."""
    return m + sp.Rational(1, 2) * n * (n + 1) * (1 + m * d) * x


def U_plus(n=n, m=m, d=d, x=x, y=y, K=K):
    """S5 (5.63a), bracket structure from glyph positions (TRANSCRIPTION.md sec. 2)."""
    return (
        (-4 * n**3 * (n + 2) * (n + 1)**2 * d**2 * x**2
         - 48 * n**2 * (n + 1) * (n - 2) * d * x
         - 16 * (n - 2) * (n - 4)) * y
        - d**3 * n**3 * (3 * n - 2) * (n + 1)**4 * (1 + m * d) * x**4
        + 4 * d**2 * n**2 * (n + 1)**2 * ((n + 1) * (3 * n - 2) * m * d + 4 * n**2 + n - 2) * x**3
        + 4 * d * (n + 1) * ((n - 2) * (n - 4) * (n + 1) * (m + n**2 * K) * d
                             - 7 * n**3 + 7 * n**2 - 14 * n + 8) * x**2
        + (16 * (n + 1) * (-4 * m + 3 * n**2 * (n - 2) * K) * d
           - 16 * (3 * n - 2) * (n - 2)) * x
        + 64 * m + 16 * n * (n + 2) * K
    )


def U_minus(n=n, m=m, d=d, x=x, y=y, K=K, tamper=None):
    """S5 (5.63b), bracket structure from glyph positions (TRANSCRIPTION.md sec. 2).

    tamper: None for the transcription; otherwise a label of a deliberate
    corruption used ONLY by the negative drills in check_transcription.py.
    """
    c_x3_inner = (n + 1) * (3 * n - 2) * m * d - n**2
    c_x4 = -n**3 * (3 * n - 2) * (n + 1)**4 * d * (1 + m * d)**3
    c_x2_first = m * (n - 2) * (n - 4) * (n + 1) * (m + n**2 * K) * d
    c0 = 64 * m**3 + 16 * n * (n + 2) * m**2 * K
    if tamper == 'T1_x3_sign':          # '- n^2' -> '+ n^2' (delta-free part)
        c_x3_inner = (n + 1) * (3 * n - 2) * m * d + n**2
    elif tamper == 'T2_x4_power':       # (n+1)^4 -> (n+1)^3 (delta-only term)
        c_x4 = -n**3 * (3 * n - 2) * (n + 1)**3 * d * (1 + m * d)**3
    elif tamper == 'T3_const':          # 64 m^3 -> 64 m^2
        c0 = 64 * m**2 + 16 * n * (n + 2) * m**2 * K
    elif tamper == 'T4_x2_delta_sq':    # delta -> delta^2 in an (n-2)(n-4) term
        c_x2_first = m * (n - 2) * (n - 4) * (n + 1) * (m + n**2 * K) * d**2
    elif tamper is not None:
        raise ValueError(tamper)
    return (
        (-4 * n**3 * (n + 2) * (n + 1)**2 * (1 + m * d)**2 * x**2
         + 48 * n**2 * (n + 1) * (n - 2) * m * (1 + m * d) * x
         - 16 * (n - 2) * (n - 4) * m**2) * y
        + c_x4 * x**4
        - 4 * n**2 * (n + 1)**2 * (1 + m * d)**2 * c_x3_inner * x**3
        + 4 * (n + 1) * (1 + m * d) * (c_x2_first
                                       + 4 * n * (2 * n**2 - 3 * n + 4) * m
                                       + n**2 * (n - 2) * (n - 4) * (n + 1) * K) * x**2
        - 16 * m * ((n + 1) * m * (-4 * m + 3 * n**2 * (n - 2) * K) * d
                    + 3 * n * (n - 4) * m + 3 * n**2 * (n + 1) * (n - 2) * K) * x
        + c0
    )


def f_S5(x=x, y=y, z=z, K=K):
    """S5 (2.19) with (5.40): f = K - lambda r^2 - 2M/r^(n-1) + Q^2/r^(2n-2) = K - y - x + z."""
    return K - y - x + z


def H_S5(n=n, m=m, x=x, z=z):
    """S5 (5.38): H = m + n(n+1)/2 x - n^2 z."""
    return m + sp.Rational(1, 2) * n * (n + 1) * x - n**2 * z


def V_S(sign, r, n=n, m=m, d=d, x=x, y=y, K=K, f=None, tamper=None):
    """S5 (5.61): V_S(+/-) = f U_(+/-) / (64 r^2 H_(+/-)^2)."""
    if sign == '-':
        U, H = U_minus(n, m, d, x, y, K, tamper=tamper), H_minus(n, m, d, x)
    else:
        U, H = U_plus(n, m, d, x, y, K), H_plus(n, m, d, x)
    return f * U / (64 * r**2 * H**2)


# ---------------- Paper I (hep-th/0305147 v3), Q = 0 ----------------
def H_I(n=n, m=m, x=x):
    """Paper I (3.2): H = m + n(n+1) x / 2."""
    return m + sp.Rational(1, 2) * n * (n + 1) * x


def Q_I(n=n, m=m, x=x, y=y, K=K):
    """Paper I (3.7); the leading minus sign stands OUTSIDE the big bracket of the y-term
    (glyph positions: '-' at x=128.76, '[' at x=139.08 on PDF page 8)."""
    return (
        -(n**3 * (n + 2) * (n + 1)**2 * x**2 - 12 * n**2 * (n + 1) * (n - 2) * m * x
          + 4 * (n - 2) * (n - 4) * m**2) * y
        + n**4 * (n + 1)**2 * x**3
        + n * (n + 1) * (4 * (2 * n**2 - 3 * n + 4) * m + n * (n - 2) * (n - 4) * (n + 1) * K) * x**2
        - 12 * n * ((n - 4) * m + n * (n + 1) * (n - 2) * K) * m * x
        + 16 * m**3 + 4 * K * n * (n + 2) * m**2
    )


def V_I(r, n=n, m=m, x=x, y=y, K=K, f=None):
    """Paper I (3.6): V_S = f Q / (16 r^2 H^2)."""
    return f * Q_I(n, m, x, y, K) / (16 * r**2 * H_I(n, m, x)**2)
