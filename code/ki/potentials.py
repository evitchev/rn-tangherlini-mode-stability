"""Kodama-Ishibashi scalar-type potentials of charged static black holes (SOURCES.md S5).

S5 (5.59)-(5.63), read from the rendered pages 24-25, at K = 1 and y = lambda r^2 = 0
(asymptotically flat), D = n + 2:

    f(Phi_pm')' + (omega^2 - V_S pm) Phi_pm = 0,   V_S pm = f U_pm / (64 r^2 H_pm^2),
    f = 1 - x + q^2 x^2 / 4,   x = 2M / r^(n-1),   q = Q/M  (extremal at q = 1),
    m = k^2 - n = l(l + n - 1) - n,   (1 + 2 m delta)^2 = 1 + 4 m q^2 / (n+1)^2   (5.58), (5.60).

Phi_- is the gravitational mode (the target), Phi_+ the electromagnetic one.  The
expressions are exact sympy polynomials in (x, m, delta); nothing here is evaluated.
"""
import sympy as sp

x, m, d = sp.symbols("x m delta")


def m_of(n, ell):
    """m = k^2 - n K with k^2 = l(l + n - 1) (S5 (5.39), K = 1)."""
    return ell * (ell + n - 1) - n


def H_minus(n):
    """S5 (5.62b)."""
    return m + sp.Rational(n * (n + 1), 2) * (1 + m * d) * x


def H_plus(n):
    """S5 (5.62a)."""
    return 1 - sp.Rational(n * (n + 1), 2) * d * x


def U_minus(n, K=1):
    """S5 (5.63b) at y = 0."""
    return (- n**3 * (3*n - 2) * (n + 1)**4 * d * (1 + m*d)**3 * x**4
            - 4 * n**2 * (n + 1)**2 * (1 + m*d)**2 * ((n + 1) * (3*n - 2) * m * d - n**2) * x**3
            + 4 * (n + 1) * (1 + m*d) * (m * (n - 2) * (n - 4) * (n + 1) * (m + n**2 * K) * d
                                         + 4 * n * (2*n**2 - 3*n + 4) * m
                                         + n**2 * (n - 2) * (n - 4) * (n + 1) * K) * x**2
            - 16 * m * ((n + 1) * m * (-4*m + 3 * n**2 * (n - 2) * K) * d
                        + 3 * n * (n - 4) * m + 3 * n**2 * (n + 1) * (n - 2) * K) * x
            + 64 * m**3 + 16 * n * (n + 2) * m**2 * K)


def U_plus(n, K=1):
    """S5 (5.63a) at y = 0."""
    return (- d**3 * n**3 * (3*n - 2) * (n + 1)**4 * (1 + m*d) * x**4
            + 4 * d**2 * n**2 * (n + 1)**2 * ((n + 1) * (3*n - 2) * m * d + 4 * n**2 + n - 2) * x**3
            + 4 * d * (n + 1) * ((n - 2) * (n - 4) * (n + 1) * (m + n**2 * K) * d
                                 - 7 * n**3 + 7 * n**2 - 14 * n + 8) * x**2
            + (16 * (n + 1) * (-4*m + 3 * n**2 * (n - 2) * K) * d - 16 * (3*n - 2) * (n - 2)) * x
            + 64 * m + 16 * n * (n + 2) * K)


# The n = 4 forms registered in TARGET.md section 1 (sealed); A2's check E0 compares them
# with U_minus(4) and H_minus(4).
U_TARGET = (-400000 * d * (1 + m*d)**3 * x**4
            - 1600 * (1 + m*d)**2 * (50 * m * d - 16) * x**3
            + 7680 * m * (1 + m*d) * x**2
            - 16 * m * (5 * m * (96 - 4*m) * d + 480) * x
            + 64 * m**3 + 384 * m**2)
H_TARGET = m + 10 * (1 + m*d) * x
