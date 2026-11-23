"""Kimi's own transcription and assembly for the p3 audit.

Part 1: Kodama-Ishibashi hep-th/0308128 (5.62b), (5.63b) at general n, K=1, y=0
(transcribed from the rendered PDF page 25), specialised to D=6 (n=4) and compared
term-by-term with TARGET.md section 1; the parametrisation identities of the brief
(delta(mu), x_H(mu), q^2(mu), s^2 = 1 + 4 m q^2/25) checked as exact identities.

Part 2: the S-deformation identity, with P an ABSTRACT function of z:
    V~ = V + dS/dr* - S^2,  S = -f(1-z)P(z)  ==>  V~ = f N / (64 rho^2 H_-^2),
    N = U_- - 64 H_-^2 [(1-z) f_z P + f(-P + (1-z) P_z + P^2)].
Derived here from scratch (V = f U_-/(64 r^2 H_-^2), dr*/dr = 1/f, r_H = 1).
"""
import sympy as sp

x, z, mu = sp.symbols("x z mu")


def ki_Usymbol(n, K=1):
    """KI (5.63b) at y = 0 (lambda = 0).  Returns U_-(x; m, delta)."""
    m, d = sp.symbols("m d")
    U = (-n**3 * (3*n - 2) * (n + 1)**4 * d * (1 + m*d)**3 * x**4
         - 4*n**2 * (n + 1)**2 * (1 + m*d)**2 * ((n + 1)*(3*n - 2)*m*d - n**2) * x**3
         + 4*(n + 1)*(1 + m*d) * (m*(n - 2)*(n - 4)*(n + 1)*(m + n**2*K)*d
                                  + 4*n*(2*n**2 - 3*n + 4)*m
                                  + n**2*(n - 2)*(n - 4)*(n + 1)*K) * x**2
         - 16*m * ((n + 1)*m*(-4*m + 3*n**2*(n - 2)*K)*d
                   + 3*n*(n - 4)*m + 3*n**2*(n + 1)*(n - 2)*K) * x
         + 64*m**3 + 16*n*(n + 2)*m**2*K)
    H = m + sp.Rational(n*(n + 1), 2) * (1 + m*d) * x     # KI (5.62b)
    return U, H


def target_UH_D6():
    """TARGET.md section 1 at D = 6 (n = 4), ell = 2 (m = 6)."""
    m, d = sp.symbols("m d")
    U = (-400000 * d * (1 + m*d)**3 * x**4
         - 1600 * (1 + m*d)**2 * (50*m*d - 16) * x**3
         + 7680 * m * (1 + m*d) * x**2
         - 16*m * (5*m*(96 - 4*m)*d + 480) * x
         + 64*m**3 + 384*m**2)
    H = m + 10 * (1 + m*d) * x
    return U, H


def part1():
    m, d = sp.symbols("m d")
    U4, H4 = ki_Usymbol(4)
    Ut, Ht = target_UH_D6()
    assert sp.expand(U4 - Ut) == 0, "U_- mismatch with TARGET.md"
    assert sp.expand(H4 - Ht) == 0, "H_- mismatch with TARGET.md"
    print("part1: KI (5.62b)/(5.63b) at n=4 == TARGET.md transcription (symbolic, all m, d)")

    # G1 quantities: n = 8, Q = 0 => delta = 0; ell = 2 => m = k^2 - nK = 2*9 - 8 = 10
    # (KI (5.39); corrected after an initial wrong m = 14 from TARGET's n=4-only formula)
    U8, H8 = ki_Usymbol(8)
    U8 = sp.expand(U8.subs({d: 0, m: 10}))
    H8 = sp.expand(H8.subs({d: 0, m: 10}))
    print("part1: G1 (n=8, Q=0): U_- =", U8, " H_- =", H8)

    # parametrisation identities (ell = 2 => m = 6)
    delta = (1 - mu**2) / (5 * (6 + mu**2))
    xH = 2 * (6 + mu**2) / ((mu + 1) * (mu + 6))
    w = 7 * mu / (6 + mu**2)
    q2 = 1 - w**2
    s = 1 + 2 * 6 * delta
    assert sp.simplify(s**2 - (1 + 4 * 6 * q2 / 25)) == 0
    # x_H = 2/(1 + sqrt(1-q^2)) with sqrt(1-q^2) = w:
    assert sp.simplify(xH - 2 / (1 + w)) == 0
    # kappa^3 = x_H^2 q^2 / 4 = (1-w)/(1+w):
    kap3 = sp.simplify(xH**2 * q2 / 4)
    assert sp.simplify(kap3 - (1 - w) / (1 + w)) == 0
    print("part1: parametrisation identities exact (s^2 law, x_H, kappa^3 = (1-w)/(1+w))")
    print("part1: q^2(mu) =", sp.factor(q2))


def part2():
    """The identity with P an abstract function of z.  r_H = 1, rho = r = 1/(1-z)."""
    rho = 1 / (1 - z)
    P = sp.Function("P")
    fz, U, H = sp.symbols("fz U H")   # stand-ins; f handled explicitly
    # f as a function of z is generic here: keep f(z) abstract to prove the ALGEBRAIC identity.
    f = sp.Function("f")
    S = -f(z) * (1 - z) * P(z)
    # dr*/dr = 1/f, r = rho:  dS/dr* = f * dS/drho = f * dS/dz * (1-z)^2
    dS_dst = f(z) * sp.diff(S, z) * (1 - z)**2
    V = f(z) * U / (64 * rho**2 * H**2)
    Vt = sp.expand(V + dS_dst - S**2)
    N = U - 64 * H**2 * ((1 - z) * sp.diff(f(z), z) * P(z)
                         + f(z) * (-P(z) + (1 - z) * sp.diff(P(z), z) + P(z)**2))
    target = f(z) * N / (64 * rho**2 * H**2)
    diff = sp.expand(Vt - target)
    assert diff == 0, diff
    print("part2: identity  V~ = f N /(64 rho^2 H_-^2)  holds for abstract f(z), P(z)")


if __name__ == "__main__":
    part1()
    part2()
    print("BUILD-PARTS-1-2 OK")
