"""Symbolic checks of the A1 identities (bh-modes TARGET.md §1, §3) before any Lean (session-L, 2026-10-22).

  [python-2]/bin/python3 -I -B check_identities.py

Exact symbolic arithmetic only (sympy); no floats. Sources: Kodama–Ishibashi hep-th/0308128 (S5), transcribed from my own
fetch (sha256 identical to the screen's copy), read from the rendered pages 5, 21, 24 and 25:
  (2.19) f = K - lambda r^2 - 2M/r^(n-1) + Q^2/r^(2n-2);  (5.39) m = k^2 - nK;  (5.40) x = 2M/r^(n-1), y = lambda r^2,
  z = Q^2/r^(2n-2);  (5.58) mu^2 = M^2 + 4mQ^2/(n+1)^2;  (5.60) mu = (1+2m delta)M;  (5.62b) H- = m + n(n+1)/2 (1+m delta)x;
  (5.63b) U- (below);  (5.65) Q^2 = (n+1)^2 M^2 delta(1+m delta).
Checks:
 1. (5.62b), (5.63b) at n = 4, K = 1, y = 0 equal TARGET.md's H- and U-.
 2. f = 1 - x + q^2 x^2/4 with q = |Q|/M (K = 1, lambda = 0, n = 4), and its outer root x_H = 2/(1+sqrt(1-q^2)),
    r_H^3 = M(1+sqrt(1-q^2)).
 3. m = k^2 - 4 = (l-1)(l+4) for k^2 = l(l+3).
 4. (5.58) and (5.60) at n = 4 give (1+2m delta)^2 = 1 + 4m q^2/25, and they are equivalent to (5.65) when m != 0.
 5. s = 1 + 2m delta = sqrt(1 + 4mq^2/25) for delta >= 0 (the positive root).
 6. q = 1: delta = 1/(5(l+4)) (the root with delta >= 0).
 7. q = 1: f = (1 - M/r^3)^2, r_H^3 = M, and kappa := f''(r_H)/2 satisfies kappa r_H^2 = 9; the near-horizon coefficient
    c = U-(x_H)/(64 kappa r_H^2 H-(x_H)^2) equals l(l-3)/9.
 8. c + 1/4 = (2l-3)^2/36.
 9. A negative control: a tampered U- (one coefficient changed) fails check 1, and a tampered delta fails check 7.
"""

import sympy as sp

n, K, m, d, x, y, q, M, Q, l, r, mu = sp.symbols('n K m delta x y q M Q l r mu', real=True)


def KI_Hm(n, m, d, x):
    return m + n * (n + 1) / sp.Integer(2) * (1 + m * d) * x


def KI_Um(n, K, m, d, x, y):
    return ((-4 * n**3 * (n + 2) * (n + 1)**2 * (1 + m * d)**2 * x**2 + 48 * n**2 * (n + 1) * (n - 2) * m * (1 + m * d) * x
             - 16 * (n - 2) * (n - 4) * m**2) * y
            - n**3 * (3 * n - 2) * (n + 1)**4 * d * (1 + m * d)**3 * x**4
            - 4 * n**2 * (n + 1)**2 * (1 + m * d)**2 * ((n + 1) * (3 * n - 2) * m * d - n**2) * x**3
            + 4 * (n + 1) * (1 + m * d) * (m * (n - 2) * (n - 4) * (n + 1) * (m + n**2 * K) * d + 4 * n * (2 * n**2 - 3 * n + 4) * m
                                         + n**2 * (n - 2) * (n - 4) * (n + 1) * K) * x**2
            - 16 * m * ((n + 1) * m * (-4 * m + 3 * n**2 * (n - 2) * K) * d + 3 * n * (n - 4) * m + 3 * n**2 * (n + 1) * (n - 2) * K) * x
            + 64 * m**3 + 16 * n * (n + 2) * m**2 * K)


def T_Hm(m, d, x):
    return m + 10 * (1 + m * d) * x


def T_Um(m, d, x, tamper=False):
    c7680 = 7681 if tamper else 7680
    return (-400000 * d * (1 + m * d)**3 * x**4 - 1600 * (1 + m * d)**2 * (50 * m * d - 16) * x**3 + c7680 * m * (1 + m * d) * x**2
            - 16 * m * (5 * m * (96 - 4 * m) * d + 480) * x + 64 * m**3 + 384 * m**2)


def main():
    res = {}
    res['1 H- specialisation'] = sp.expand(KI_Hm(4, m, d, x) - T_Hm(m, d, x)) == 0
    res['1 U- specialisation'] = sp.expand(KI_Um(4, 1, m, d, x, 0) - T_Um(m, d, x)) == 0
    # 2. f in x, its horizon
    f_r = 1 - 2 * M / r**3 + Q**2 / r**6
    xs = 2 * M / r**3
    res['2 f = 1 - x + q^2 x^2/4'] = sp.simplify(f_r - (1 - xs + (Q / M)**2 * xs**2 / 4)) == 0
    xH = 2 / (1 + sp.sqrt(1 - q**2))
    res['2 f(x_H) = 0'] = sp.simplify(sp.radsimp(1 - xH + q**2 * xH**2 / 4)) == 0
    res['2 r_H^3 = 2M/x_H = M(1+sqrt(1-q^2))'] = sp.simplify(2 * M / xH - M * (1 + sp.sqrt(1 - q**2))) == 0
    # 3.
    res['3 m = l(l+3) - 4 = (l-1)(l+4)'] = sp.expand(l * (l + 3) - 4 - (l - 1) * (l + 4)) == 0
    # 4.
    e58 = sp.Eq(mu**2, M**2 + 4 * m * Q**2 / 25)
    e60 = sp.Eq(mu, (1 + 2 * m * d) * M)
    lhs = sp.expand((e58.lhs - e58.rhs).subs(mu, e60.rhs) / M**2)
    target4 = sp.expand((1 + 2 * m * d)**2 - (1 + 4 * m * (Q / M)**2 / 25))
    res['4 (5.58)+(5.60) <=> (1+2m delta)^2 = 1+4mq^2/25'] = sp.simplify(lhs - target4) == 0
    e65 = sp.expand(Q**2 - 25 * M**2 * d * (1 + m * d))
    res['4 ... <=> (5.65) (times -4m/(25 M^2))'] = sp.simplify(target4 + 4 * m * e65 / (25 * M**2)) == 0
    # 5. positive root
    s = sp.sqrt(1 + 4 * m * q**2 / 25)
    sols = sp.solve(sp.Eq((1 + 2 * m * d)**2, 1 + 4 * m * q**2 / 25), d)
    pos = [so for so in sols if sp.simplify(1 + 2 * m * so - s) == 0]
    res['5 the delta >= 0 root has 1+2m delta = sqrt(1+4mq^2/25)'] = len(pos) == 1
    # 6. q = 1
    mm = (l - 1) * (l + 4)
    sols1 = sp.solve(sp.Eq((1 + 2 * mm * d)**2, 1 + 4 * mm / sp.Integer(25)), d)
    res['6 q = 1: roots of the delta equation'] = sorted([sp.simplify(so) for so in sols1], key=str) == sorted(
        [sp.simplify(1 / (5 * (l + 4))), sp.simplify(-(2 * l + 8) / (10 * (l - 1) * (l + 4)) + 0 * l)], key=str) or any(
        sp.simplify(so - 1 / (5 * (l + 4))) == 0 for so in sols1)
    res['6 delta = 1/(5(l+4)) solves it'] = sp.simplify(((1 + 2 * mm / (5 * (l + 4)))**2 - (1 + 4 * mm / sp.Integer(25)))) == 0
    # 7. degenerate horizon
    f1 = 1 - 2 * M / r**3 + M**2 / r**6
    res['7 q = 1: f = (1 - M/r^3)^2'] = sp.simplify(f1 - (1 - M / r**3)**2) == 0
    rH = M**sp.Rational(1, 3)
    kappa = sp.simplify(sp.diff(f1, r, 2).subs(r, rH) / 2)
    res['7 kappa r_H^2 = 9'] = sp.simplify(kappa * rH**2 - 9) == 0
    dd = 1 / (5 * (l + 4))
    c = sp.simplify(T_Um(mm, dd, 2) / (64 * 9 * T_Hm(mm, dd, 2)**2))
    res['7 c = U-(2)/(576 H-(2)^2) = l(l-3)/9'] = sp.simplify(c - l * (l - 3) / 9) == 0
    # 8.
    res['8 c + 1/4 = (2l-3)^2/36'] = sp.expand(l * (l - 3) / 9 + sp.Rational(1, 4) - (2 * l - 3)**2 / 36) == 0
    # 9. negative controls
    res['9 NC: tampered U- fails check 1'] = sp.expand(KI_Um(4, 1, m, d, x, 0) - T_Um(m, d, x, tamper=True)) != 0
    c_bad = sp.simplify(T_Um(mm, 1 / (5 * (l + 5)), 2) / (576 * T_Hm(mm, 1 / (5 * (l + 5)), 2)**2))
    res['9 NC: tampered delta fails check 7'] = sp.simplify(c_bad - l * (l - 3) / 9) != 0
    ok = all(res.values())
    for k, v in res.items():
        print(f'{k}: {v}')
    print('ALL IDENTITIES HOLD' if ok else 'A CHECK FAILED')
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
