"""Generator for the certificate data in lean/BHModesOnset.lean, section "Generated" (session-L, 2026-10-22).

  [python-2]/bin/python3 -I -B gen_onset.py > gen_onset.out

Exact sympy only. Everything it prints is checked again by Lean, by `ring` or `norm_num`. Nothing here is trusted.
Setting (bh-modes results/onset/PREREG.md §1): l = 2, m = 6, A = 6 + mu^2, w = 7mu/A, s = 7(6 - mu^2)/(5A),
delta = (s - 1)/12, x_H = 2/(1 + w), x = t x_H. Then U_- = F(t, mu)/((mu + 1)^3 (mu + 6)) with F of degree (4, 4).
Prints:
  1. F, and Q = (F(t, mu) - F(1, mu))/(t - 1);
  2. the cofactor K with (6 + mu^2)^6 C(1 - w^2) = p(mu) K(mu), p = 10mu^3 - 11mu^2 + 228mu - 45,
     C = 3025Y^3 - 31521Y^2 + 99792Y - 68796;
  3. the Bernstein coefficients of F on [0, 7/8] x [1/6, 1] and [7/8, 1] x [1/4, 1], and of Q on [7/8, 1] x [1/6, 1/4],
     as Lean source;
  4. the isolating interval of the root of p and the induced bounds.
"""

from math import comb

import sympy as sp

t, mu, u, v, Y = sp.symbols('t mu u v Y')
m = 6
A = 6 + mu**2
w = 7 * mu / A
s = 7 * (6 - mu**2) / (5 * A)
d = sp.cancel((s - 1) / (2 * m))
xH = sp.cancel(2 / (1 + w))
x = t * xH
U = (-400000 * d * (1 + m * d)**3 * x**4 - 1600 * (1 + m * d)**2 * (50 * m * d - 16) * x**3 + 7680 * m * (1 + m * d) * x**2
     - 16 * m * (5 * m * (96 - 4 * m) * d + 480) * x + 64 * m**3 + 384 * m**2)
num, den = sp.fraction(sp.cancel(sp.together(U)))
assert sp.expand(den - (mu + 1)**3 * (mu + 6)) == 0
F = sp.expand(num)
Q = sp.expand(sp.cancel((F - F.subs(t, 1)) / (t - 1)))
p = 10 * mu**3 - 11 * mu**2 + 228 * mu - 45
C = 3025 * Y**3 - 31521 * Y**2 + 99792 * Y - 68796
lhs = sp.expand(sp.cancel(A**6 * C.subs(Y, 1 - w**2)))
Kq, Kr = sp.div(sp.Poly(lhs, mu), sp.Poly(p, mu))
assert Kr.is_zero
K = Kq.as_expr()


def lean(e):
    s_ = sp.sstr(sp.expand(e)).replace('**', ' ^ ')
    return s_


def bern(expr, t0, t1, m0, m1, dt, dm):
    e = sp.expand(expr.subs({t: t0 + (t1 - t0) * u, mu: m0 + (m1 - m0) * v}, simultaneous=True))
    P = sp.Poly(e, u, v)
    a = {(i, j): P.coeff_monomial(u**i * v**j) for i in range(dt + 1) for j in range(dm + 1)}
    return {(k, l): sum(sp.Rational(comb(k, i), comb(dt, i)) * sp.Rational(comb(l, j), comb(dm, j)) * a[(i, j)]
                        for i in range(k + 1) for j in range(l + 1)) for k in range(dt + 1) for l in range(dm + 1)}


def lean_poly(e, vars_):
    P = sp.Poly(sp.expand(e), *vars_)
    terms = []
    for mon, c in sorted(P.terms(), reverse=True):
        fac = ' * '.join(f'{vn} ^ {k}' for vn, k in zip([str(z) for z in vars_], mon) if k > 0)
        cs = sp.sstr(c)
        terms.append(f'({cs} : ℝ)' + (f' * {fac}' if fac else ''))
    return '\n    + '.join(terms)


def bern_def(name, b, dt, dm, c):
    """B(u, ub, v, vb) = sum b_kl * binom * u^k ub^(dt-k) v^l vb^(dm-l); and its split c * (u+ub)^dt (v+vb)^dm + rest."""
    full, rest = [], []
    for (k, l), bk in sorted(b.items()):
        mon = f'{comb(dt, k) * comb(dm, l)} * u ^ {k} * ub ^ {dt - k} * v ^ {l} * vb ^ {dm - l}'
        full.append(f'({sp.sstr(bk)} : ℝ) * ({mon})')
        if bk != c:
            rest.append(f'({sp.sstr(bk - c)} : ℝ) * ({mon})')
    out = [f'noncomputable def {name} (u ub v vb : ℝ) : ℝ :=\n    ' + '\n    + '.join(full), '',
           f'theorem {name}_split (u ub v vb : ℝ) :',
           f'    {name} u ub v vb = ({sp.sstr(c)} : ℝ) * ((u + ub) ^ {dt} * (v + vb) ^ {dm})',
           '      + (' + '\n      + '.join(rest) + ') := by',
           f'  unfold {name}; ring']
    return '\n'.join(out)


print('-- ===== Lean: definitions')
print('def Fp (t μ : ℝ) : ℝ :=\n    ' + lean_poly(F, (t, mu)).replace('mu', 'μ'))
print()
print('def Qp (t μ : ℝ) : ℝ :=\n    ' + lean_poly(Q, (t, mu)).replace('mu', 'μ'))
print()
print('def Kμ (μ : ℝ) : ℝ :=\n    ' + lean_poly(K, (mu,)).replace('mu', 'μ'))
for name, expr, box, dt in (('B1', F, (0, sp.Rational(7, 8), sp.Rational(1, 6), 1), 4),
                            ('B2', F, (sp.Rational(7, 8), 1, sp.Rational(1, 4), 1), 4),
                            ('B3', -Q, (sp.Rational(7, 8), 1, sp.Rational(1, 6), sp.Rational(1, 4)), 3)):
    b = bern(expr, *box, dt, 4)
    c = min(b.values())
    assert c > 0
    print()
    print(f'-- {name}: Bernstein form on {box} (t0, t1, mu0, mu1); min coefficient {sp.sstr(c)} ~ {float(c):.6g}')
    print(bern_def(name, b, dt, 4, c))
lo, hi = sp.Rational(19893240974, 10**11), sp.Rational(19893240975, 10**11)
print()
print('-- p(lo) < 0:', p.subs(mu, lo) < 0, ' p(hi) > 0:', p.subs(mu, hi) > 0)
q2 = 1 - w**2
print('-- q* bounds:', sp.Rational('0.9730564367')**2 < q2.subs(mu, hi), q2.subs(mu, lo) < sp.Rational('0.9730564368')**2)
