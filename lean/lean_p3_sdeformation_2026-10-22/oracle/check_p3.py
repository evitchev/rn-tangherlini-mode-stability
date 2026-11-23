"""Independent checks of METHOD.md Lemmas 1-2, Proposition 3's algebra and the Remarks, outside Lean (session-L, 2026-10-22).

  [python-2]/bin/python3 -I -B check_p3.py

sympy for the exact parts, mpmath for one numerical quadrature. Sources: bh-modes results/p3/METHOD.md and TARGET.md §1.
Checks:
 1. Lemma 1, pointwise: with phi = a + i b, |phi'|^2 + V|phi|^2 = |phi' + S phi|^2 + (V + S' - S^2)|phi|^2 - (S|phi|^2)'.
 2. Lemma 1, integrated, on one example: phi = (1 - x^2)^3 (1 + 3i x/10) on [-1, 1] (C^2 with compact support),
    S = sin(2x) + x/3, V = cos(3x) - 1/2; both sides by mpmath quadrature at 40 digits.
 3. Lemma 2 with sympy doing the calculus: z = 1 - 1/rho, f(rho) = F(z), beta = (1 - z)P(z), S = -f beta,
    Vt = f U/(64 rho^2 H^2) + f dS/drho - S^2 (dS/dr* = f dS/drho), against f N/(64 rho^2 H^2) with METHOD's N.
    F, P, U and H are undefined functions, so the chain rule is sympy's.
 4. D = 6: F6' = dF6/dz; F6(0) = 0 with x_H = 2/(1 + sqrt(1 - q^2)); F6 at z = 1 - 1/rho is 1 - 2M/rho^3 + (qM)^2/rho^6
    when M(1 + sqrt(1 - q^2)) = 1; N(1) = 64 m^2 (m + 6 - P(1)^2 + P(1)); for m = 6 the roots of N(1) are P(1) = -3, 4.
 5. N(0) = U(0) - 64 H(0)^2 f_z(0) P(0) when f(0) = 0; the eps-shift; rho f' = (1 - z) f_z.
 6. Negative controls: N with 63 in place of 64 fails check 3; F6' with 2 in place of 3 fails check 4.
"""

import mpmath as mp
import sympy as sp

x, rho, z, q, m, d, M, eps = sp.symbols('x rho z q m delta M epsilon', real=True)
a, b, ap, bp, S, Sp, V = sp.symbols('a b ap bp S Sp V', real=True)
F, P, U, H = (sp.Function(n) for n in ('F', 'P', 'U', 'H'))


def Nz(Uz, Hz, Fz, Fpz, Pz, Ppz, zz, c64=64):
    return Uz - c64 * Hz**2 * ((1 - zz) * Fpz * Pz + Fz * (-Pz + (1 - zz) * Ppz + Pz**2))


def check1():
    lhs = (ap**2 + bp**2) + V * (a**2 + b**2)
    sq = (ap + S * a)**2 + (bp + S * b)**2
    deriv = Sp * (a**2 + b**2) + S * 2 * (a * ap + b * bp)
    return sp.expand(lhs - (sq + (V + Sp - S**2) * (a**2 + b**2) - deriv)) == 0


def check2():
    mp.mp.dps = 40
    phi = lambda t: (1 - t**2)**3 * (1 + 3j * t / 10)
    dphi = lambda t: mp.diff(phi, t)
    Sf = lambda t: mp.sin(2 * t) + t / 3
    dS = lambda t: 2 * mp.cos(2 * t) + mp.mpf(1) / 3
    Vf = lambda t: mp.cos(3 * t) - mp.mpf(1) / 2
    lhs = mp.quad(lambda t: abs(dphi(t))**2 + Vf(t) * abs(phi(t))**2, [-1, 0, 1])
    r1 = mp.quad(lambda t: abs(dphi(t) + Sf(t) * phi(t))**2, [-1, 0, 1])
    r2 = mp.quad(lambda t: (Vf(t) + dS(t) - Sf(t)**2) * abs(phi(t))**2, [-1, 0, 1])
    return abs(lhs - (r1 + r2)) < mp.mpf(10)**-30, mp.nstr(lhs, 20), mp.nstr(r1 + r2, 20)


def check3(c64=64):
    zr = 1 - 1 / rho
    f = F(zr)
    beta = (1 - zr) * P(zr)
    Sr = -f * beta
    Vt = f * U(zr) / (64 * rho**2 * H(zr)**2) + f * sp.diff(Sr, rho) - Sr**2
    Fz = sp.diff(F(z), z).subs(z, zr)
    Pz = sp.diff(P(z), z).subs(z, zr)
    target = f * Nz(U(zr), H(zr), f, Fz, P(zr), Pz, zr, c64) / (64 * rho**2 * H(zr)**2)
    return sp.simplify(sp.expand(Vt - target)) == 0


def d6(c3=3):
    xH = 2 / (1 + sp.sqrt(1 - q**2))
    x6 = xH * (1 - z)**3
    F6 = 1 - x6 + q**2 * x6**2 / 4
    F6p = c3 * xH * (1 - z)**2 * (1 - q**2 * x6 / 2)
    Hm = m + 10 * (1 + m * d) * x6
    Um = (-400000 * d * (1 + m * d)**3 * x6**4 - 1600 * (1 + m * d)**2 * (50 * m * d - 16) * x6**3
          + 7680 * m * (1 + m * d) * x6**2 - 16 * m * (5 * m * (96 - 4 * m) * d + 480) * x6 + 64 * m**3 + 384 * m**2)
    return xH, x6, F6, F6p, Hm, Um


def check4(c3=3):
    xH, x6, F6, F6p, Hm, Um = d6(c3)
    res = {}
    res["4 F6' = dF6/dz"] = sp.simplify(sp.diff(F6, z) - F6p) == 0
    res['4 F6(0) = 0'] = sp.simplify(sp.radsimp(F6.subs(z, 0))) == 0
    Msol = 1 / (1 + sp.sqrt(1 - q**2))
    f_target = 1 - 2 * Msol / rho**3 + (q * Msol)**2 / rho**6
    res['4 F6(1 - 1/rho) = TARGET f'] = sp.simplify(F6.subs(z, 1 - 1 / rho) - f_target) == 0
    P1, Pp1 = sp.symbols('P1 Pp1', real=True)
    N1 = Nz(Um.subs(z, 1), Hm.subs(z, 1), F6.subs(z, 1), F6p.subs(z, 1), P1, Pp1, 1)
    res['4 N(1) = 64 m^2 (m + 6 - P1^2 + P1)'] = sp.expand(N1 - 64 * m**2 * (m + 6 - P1**2 + P1)) == 0
    res['4 m = 6: roots of N(1) are -3, 4'] = sorted(sp.solve(sp.Eq(N1.subs(m, 6), 0), P1)) == [-3, 4]
    return res


def check5():
    res = {}
    U0, H0, Fp0, P0, Pp0 = sp.symbols('U0 H0 Fp0 P0 Pp0', real=True)
    res['5 N(0) when f(0) = 0'] = sp.expand(Nz(U0, H0, 0, Fp0, P0, Pp0, 0) - (U0 - 64 * H0**2 * Fp0 * P0)) == 0
    Uz, Hz, Fz, Fpz, Pz, Ppz = sp.symbols('Uz Hz Fz Fpz Pz Ppz', real=True)
    shift = Nz(Uz, Hz, Fz, Fpz, Pz - eps, Ppz, z) - Nz(Uz, Hz, Fz, Fpz, Pz, Ppz, z)
    res['5 eps-shift'] = sp.expand(shift - 64 * Hz**2 * eps * ((1 - z) * Fpz + Fz * (2 * Pz - 1 - eps))) == 0
    zr = 1 - 1 / rho
    res["5 rho f' = (1 - z) f_z"] = sp.simplify(rho * (1 - zr)**2 * Fpz - (1 - zr) * Fpz) == 0
    return res


def main():
    res = {'1 Lemma 1 pointwise': check1()}
    ok2, l2, r2 = check2()
    res[f'2 Lemma 1 integrated (lhs {l2}, rhs {r2})'] = ok2
    res['3 Lemma 2 (sympy chain rule)'] = check3()
    res.update(check4())
    res.update(check5())
    res['6 NC: N with 63 fails check 3'] = not check3(c64=63)
    res["6 NC: F6' with 2 fails check 4"] = not check4(c3=2)["4 F6' = dF6/dz"]
    for k, v in res.items():
        print(f'{k}: {v}')
    ok = all(res.values())
    print('ALL P3 CHECKS HOLD' if ok else 'A CHECK FAILED')
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
