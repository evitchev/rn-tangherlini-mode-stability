"""check_p3v4.py: checks of the bh-modes p3 Lean layer v4 (G-RES and the D = 4 Darboux identities) outside Lean
(session-L, 2026-10-24).

Run with an interpreter that has sympy, from this folder:
    python3 -I -B check_p3v4.py ../lean/BHModesP3.lean
It reads only the Lean file named on the command line. It exits 0 only if every check holds.

 1. Lines 1-681 are the v3 build's (sha256 of that prefix); the v4 section follows; the file ends with the namespace.
 2. G-RES, recomputed from bh-modes code/a2/scert.py's g_res (at 2416726; typed into this file below, with
    code/ki/potentials.py's U_TARGET and H_TARGET): N is a polynomial in z, N(0) = 576 H(2)^2 (l(l - 3)/9 - a(a + 1)),
    H(2) = (l + 3)(l + 4).
 3. The file's own pieces, parsed: Um and Hm are potentials.py's U_TARGET and H_TARGET; mEll and dEll are scert.py's m
    and delta; they satisfy S5 (5.58) at q = 1; Pres and Pres' are P and dP/dz; D6_extremal's three right sides are
    x6, F6 and F6' at q = 1; N built from the file's Nz, U6, H6, F6, F6', Pres and Pres' has the polynomial value at 0
    that g_res states; and g_res's Nz arguments are prop3_D6's at q = 1.
 4. The Darboux identities, recomputed from bh-modes [code of another line of this project]'s chandrasekhar (typed below, with
    potentials.py's U_minus(2) and H_minus(2) at delta = 0), and from the file's own f4, VKI4, VRW4, W4 (parsed, with
    UmN and HmN at n = 2): W^2 + W_* - kappa^2/(4 beta^2) = V_S-, W^2 - W_* - kappa^2/(4 beta^2) = Regge-Wheeler;
    W4_deriv's right side is dW/dr; H_- = (m r + 6M)/r; Regge-Wheeler's denominator is a power of r; V_S- itself has a
    double pole at r0 = -6M/m (so the Darboux partner removes a singularity that is there).
 5. Controls (each mutated statement of P3M25-P3M37 is false, not merely unproved).
"""

import hashlib
import re
import sys

import sympy as sp

PREFIX_LINES = 681
PREFIX_SHA256 = '92aaa876c73781abb6f37d3f3c44a7117365b10d43cfd795dd936c6a522d5292'  # v3 build, 3a2dcd68...

results = []


def check(name, ok, detail=''):
    results.append(bool(ok))
    print(f"{'ok  ' if ok else 'FAIL'} {name}{': ' + detail if detail else ''}")


def body(text, head):
    i = text.index(head)
    j = text.index(':=', i) + 2
    k = text.index('\n\n', j)
    return text[j:k]


def statement(text, name):
    m = re.search(r'^theorem ' + re.escape(name) + r' ', text, re.M)
    start, depth = m.end(), 0
    for i in range(start, len(text)):
        c = text[i]
        if c in '([{':
            depth += 1
        elif c in ')]}':
            depth -= 1
        elif depth == 0 and text.startswith(':=', i):
            return ' '.join(text[start:i].split())
    raise SystemExit(f'no := after theorem {name}')


def conclusion(text, name):
    """The statement after its binders: the text after the first ':' outside brackets."""
    st, depth = statement(text, name), 0
    for i, c in enumerate(st):
        if c in '([{':
            depth += 1
        elif c in ')]}':
            depth -= 1
        elif depth == 0 and c == ':':
            return st[i + 1:].strip()
    raise SystemExit(f'no conclusion in theorem {name}')


ell, a, b0, b1, z, m, delta, x, q, xH, M, r, U, H, F, Fd, P, Pd = sp.symbols(
    'ell a b0 b1 z m delta x q xH M r U H F Fd P Pd')
SYMS = {'ell': ell, 'a': a, 'b0': b0, 'b1': b1, 'z': z, 'm': m, 'delta': delta, 'x': x, 'q': q, 'xH': xH, 'M': M,
        'r': r, 'U': U, 'H': H, 'F': F, 'Fd': Fd, 'P': P, 'Pd': Pd}


def lean_to_sympy(s, extra=()):
    s = ' '.join(s.split())
    for old, new in extra:
        s = s.replace(old, new)
    s = s.replace('ℓ', 'ell').replace('δ', 'delta').replace('^', '**')
    return sp.sympify(s, locals=SYMS)


# code/ki/potentials.py (sha256 7d686b40...): U_TARGET, H_TARGET (n = 4), and U_minus(n), H_minus(n) (S5 (5.63b),
# (5.62b) at K = 1, y = 0), typed here.
d = delta
U_TARGET = (-400000 * d * (1 + m*d)**3 * x**4
            - 1600 * (1 + m*d)**2 * (50 * m * d - 16) * x**3
            + 7680 * m * (1 + m*d) * x**2
            - 16 * m * (5 * m * (96 - 4*m) * d + 480) * x
            + 64 * m**3 + 384 * m**2)
H_TARGET = m + 10 * (1 + m*d) * x


def U_minus(n, K=1):
    return (- n**3 * (3*n - 2) * (n + 1)**4 * d * (1 + m*d)**3 * x**4
            - 4 * n**2 * (n + 1)**2 * (1 + m*d)**2 * ((n + 1) * (3*n - 2) * m * d - n**2) * x**3
            + 4 * (n + 1) * (1 + m*d) * (m * (n - 2) * (n - 4) * (n + 1) * (m + n**2 * K) * d
                                         + 4 * n * (2*n**2 - 3*n + 4) * m
                                         + n**2 * (n - 2) * (n - 4) * (n + 1) * K) * x**2
            - 16 * m * ((n + 1) * m * (-4*m + 3 * n**2 * (n - 2) * K) * d
                        + 3 * n * (n - 4) * m + 3 * n**2 * (n + 1) * (n - 2) * K) * x
            + 64 * m**3 + 16 * n * (n + 2) * m**2 * K)


def H_minus(n):
    return m + sp.Rational(n * (n + 1), 2) * (1 + m * d) * x


def scert_g_res(U0=U_TARGET, H0=H_TARGET, mm=(ell - 1) * (ell + 4), dl=1 / (5 * (ell + 4)), Pz=a / z + b0 + b1 * z,
                f=None):
    """code/a2/scert.py g_res (at 2416726), typed here: (N polynomial in z, H(2), N(0) - claim), with options for the
    controls."""
    y = (1 - z) ** 3
    Uz = U0.subs({m: mm, d: dl, x: 2 * y})
    Hz = H0.subs({m: mm, d: dl, x: 2 * y})
    f = (1 - y) ** 2 if f is None else f
    N = Uz - 64 * Hz ** 2 * ((1 - z) * sp.diff(f, z) * Pz + f * (-Pz + (1 - z) * sp.diff(Pz, z) + Pz ** 2))
    num, den = sp.fraction(sp.cancel(sp.together(N)))
    poly = not den.has(z)
    H2 = sp.factor(H0.subs({m: mm, d: dl, x: 2}))
    diff = sp.cancel(num.subs(z, 0) / den - 576 * H2 ** 2 * (ell * (ell - 3) / sp.Integer(9) - a * (a + 1))) if poly \
        else None
    return poly, H2, diff, N


def main(path):
    raw = open(path, 'rb').read()
    text = raw.decode('utf-8')
    lines = raw.split(b'\n')

    # 1
    h = hashlib.sha256(b'\n'.join(lines[:PREFIX_LINES]) + b'\n').hexdigest()
    check("1. lines 1-681 are the v3 build's", h == PREFIX_SHA256, f'prefix sha256 {h[:16]}...')
    check('1. the v4 section starts at line 682', lines[PREFIX_LINES].decode('utf-8').startswith('/-! ### v4 (2026-10-24)'))
    check('1. the file ends with the namespace', text.endswith('end BHModes.P3\n'), f'{len(lines) - 1} lines')

    # 2
    poly, H2, diff, _ = scert_g_res()
    check('2. scert.py g_res: N is a polynomial in z', poly)
    check('2. scert.py g_res: N(0) - 576 H(2)^2 (l(l - 3)/9 - a(a + 1)) = 0', diff == 0, str(diff))
    check('2. scert.py g_res: H(2) = (l + 3)(l + 4)', sp.expand(H2 - (ell + 3) * (ell + 4)) == 0, str(H2))

    # 3: the file's own pieces
    Um = lean_to_sympy(body(text, 'def Um (m δ x : ℝ) : ℝ'))
    Hm = lean_to_sympy(body(text, 'def Hm (m δ x : ℝ) : ℝ'))
    check("3. the file's Um and Hm are potentials.py's U_TARGET and H_TARGET",
          sp.expand(Um - U_TARGET) == 0 and sp.expand(Hm - H_TARGET) == 0)
    mE = lean_to_sympy(body(text, 'def mEll (ℓ : ℝ) : ℝ'))
    dE = lean_to_sympy(body(text, 'noncomputable def dEll (ℓ : ℝ) : ℝ'))
    check("3. mEll and dEll are scert.py's (l - 1)(l + 4) and 1/(5(l + 4))",
          sp.expand(mE - (ell - 1) * (ell + 4)) == 0 and sp.simplify(dE - 1 / (5 * (ell + 4))) == 0, f'{mE}; {dE}')
    check('3. m = l(l + n - 1) - n at n = 4', sp.expand(mE - (ell * (ell + 3) - 4)) == 0)
    s558 = sp.simplify((1 + 2 * mE * dE) ** 2 - (1 + 4 * mE * 1 / sp.Integer(25)))
    check('3. S5 (5.58) at n = 4, q = 1: (1 + 2 m delta)^2 = 1 + 4 m q^2/25, and 1 + 2 m delta = (2l + 3)/5',
          s558 == 0 and sp.simplify(1 + 2 * mE * dE - (2 * ell + 3) / 5) == 0)
    Pr = lean_to_sympy(body(text, 'noncomputable def Pres (a b0 b1 z : ℝ) : ℝ'))
    Prd = lean_to_sympy(body(text, "noncomputable def Pres' (a b1 z : ℝ) : ℝ"))
    check("3. Pres = a/z + b0 + b1 z and Pres' = d/dz Pres",
          sp.simplify(Pr - (a / z + b0 + b1 * z)) == 0 and sp.simplify(sp.diff(Pr, z) - Prd) == 0)
    xH1 = lean_to_sympy(body(text, 'noncomputable def xH (q : ℝ) : ℝ'), (('Real.sqrt', 'sqrt'),)).subs(q, 1)
    x6 = lean_to_sympy(body(text, 'noncomputable def x6 (q z : ℝ) : ℝ'), (('xH q', '(xH)'),)).subs(xH, xH1)
    F6 = lean_to_sympy(body(text, 'noncomputable def F6 (q z : ℝ) : ℝ'), (('x6 q z', '(X6)'),)).subs(
        sp.Symbol('X6'), x6).subs(q, 1)
    F6d = lean_to_sympy(body(text, "noncomputable def F6' (q z : ℝ) : ℝ"), (('x6 q z', '(X6)'), ('xH q', '(xH)'))).subs(
        sp.Symbol('X6'), x6).subs({xH: xH1, q: 1})
    st = conclusion(text, 'D6_extremal')
    rhs = re.findall(r'= (.*?)(?: ∧|$)', st)
    rx, rf, rfd = (lean_to_sympy(s) for s in rhs)
    check("3. D6_extremal's right sides are x6, F6 and F6' at q = 1, and F6' = dF6/dz",
          xH1 == 2 and sp.expand(x6 - rx) == 0 and sp.expand(F6 - rf) == 0 and sp.expand(F6d - rfd) == 0
          and sp.expand(sp.diff(F6, z) - F6d) == 0, f'x_H(1) = {xH1}; {rhs}')
    Nzb = body(text, "noncomputable def Nz (U H F F' P P' : ℝ → ℝ) (z : ℝ) : ℝ")
    Nz = lean_to_sympy(Nzb, (("F' z", '(Fd)'), ("P' z", '(Pd)'), ('U z', '(U)'), ('H z', '(H)'), ('F z', '(F)'),
                             ('P z', '(P)')))
    N_file = Nz.subs({U: Um.subs({m: mE, delta: dE, x: x6}), H: Hm.subs({m: mE, delta: dE, x: x6}), F: F6, Fd: F6d,
                      P: Pr, Pd: Prd})
    num, den = sp.fraction(sp.cancel(sp.together(N_file)))
    st = statement(text, 'g_res')
    claim = st.split('p.eval 0 =', 1)[1]
    H2f = Hm.subs({m: mE, delta: dE, x: 2})
    claimed = lean_to_sympy(claim, (('Hm (mEll ℓ) (dEll ℓ) 2', '(H2)'),)).subs(sp.Symbol('H2'), H2f)
    check("3. N from the file's own definitions is a polynomial in z, with g_res's value at 0",
          not den.has(z) and sp.cancel(num.subs(z, 0) / den - claimed) == 0, ' '.join(claim.split()))
    st_d6 = statement(text, 'prop3_D6')
    hN = re.search(r'\(hN : ∀ z, 0 < z → z < 1 → 0 ≤ (Nz .*?) z\)', st_d6).group(1)
    want = hN.replace('U6 q m δ', 'U6 1 (mEll ℓ) (dEll ℓ)').replace('H6 q m δ', 'H6 1 (mEll ℓ) (dEll ℓ)').replace(
        "F6' q", "F6' 1").replace('F6 q', 'F6 1').replace(" P P'", " (Pres a b0 b1) (Pres' a b1)")
    check("3. g_res's and g_res_tendsto's N is prop3_D6's Nz at q = 1, m = mEll l, delta = dEll l, P = Pres",
          want in st and want in statement(text, 'g_res_tendsto'), want)

    # 4: the Darboux identities
    f = 1 - 2 * M / r
    Fc = f / (r * (m * r + 6 * M))
    beta, kap = 6 * M, m * (m + 2)
    Wj = beta * Fc + kap / (2 * beta)
    Wsj = f * sp.diff(Wj, r)
    U0 = U_minus(2).subs(d, 0).subs(x, 2 * M / r)
    H0 = H_minus(2).subs(d, 0).subs(x, 2 * M / r)
    VKIj = f * U0 / (64 * r ** 2 * H0 ** 2)
    RWj = f * ((m + 2) / r ** 2 - 6 * M / r ** 3)
    check('4. apparent.py chandrasekhar: V_S- = W^2 + W_* - kappa^2/(4 beta^2)',
          sp.cancel(Wj ** 2 + Wsj - kap ** 2 / (4 * beta ** 2) - VKIj) == 0)
    check('4. apparent.py chandrasekhar: Regge-Wheeler = W^2 - W_* - kappa^2/(4 beta^2)',
          sp.cancel(Wj ** 2 - Wsj - kap ** 2 / (4 * beta ** 2) - RWj) == 0)
    UmN = lean_to_sympy(body(text, 'noncomputable def UmN (n K m δ x y : ℝ) : ℝ'))
    HmN = lean_to_sympy(body(text, 'noncomputable def HmN (n m δ x : ℝ) : ℝ'))
    n_, K_, y_ = sp.symbols('n K y')
    f4 = lean_to_sympy(body(text, 'noncomputable def f4 (M r : ℝ) : ℝ'))
    U2 = UmN.subs({n_: 2, K_: 1, delta: 0, y_: 0, x: 2 * M / r})
    H2r = HmN.subs({n_: 2, delta: 0, x: 2 * M / r})
    VKI4 = lean_to_sympy(body(text, 'noncomputable def VKI4 (m M r : ℝ) : ℝ'),
                         (('f4 M r', '(f4)'), ('UmN 2 1 m 0 (2 * M / r) 0', '(U2)'), ('HmN 2 m 0 (2 * M / r)', '(H2)')))
    VKI4 = VKI4.subs({sp.Symbol('f4'): f4, sp.Symbol('U2'): U2, sp.Symbol('H2'): H2r})
    VRW4 = lean_to_sympy(body(text, 'noncomputable def VRW4 (m M r : ℝ) : ℝ'), (('f4 M r', '(f4)'),)).subs(
        sp.Symbol('f4'), f4)
    W4 = lean_to_sympy(body(text, 'noncomputable def W4 (m M r : ℝ) : ℝ'), (('f4 M r', '(f4)'),)).subs(
        sp.Symbol('f4'), f4)
    check("4. the file's f4, W4, VKI4 and VRW4 are apparent.py's f, W, V_S- and Regge-Wheeler",
          sp.cancel(f4 - f) == 0 and sp.cancel(W4 - Wj) == 0 and sp.cancel(VKI4 - VKIj) == 0
          and sp.cancel(VRW4 - RWj) == 0)
    st = conclusion(text, 'W4_deriv')
    Wd =lean_to_sympy(st.split('deriv (W4 m M) r =', 1)[1], (('f4 M r', '(f4)'),)).subs(sp.Symbol('f4'), f4)
    check("4. W4_deriv's right side is dW4/dr", sp.cancel(Wd - sp.diff(W4, r)) == 0)
    reps = (('deriv (W4 m M) r', '(Wd)'), ('VKI4 m M r', '(VKI)'), ('VRW4 m M r', '(VRW)'), ('W4 m M r', '(W)'),
            ('f4 M r', '(f4)'))  # VRW4 before W4: 'VRW4 m M r' contains 'W4 m M r'
    vals = {sp.Symbol('Wd'): sp.diff(W4, r), sp.Symbol('W'): W4, sp.Symbol('f4'): f4, sp.Symbol('VKI'): VKI4,
            sp.Symbol('VRW'): VRW4}
    for name in ('darboux_KI', 'darboux_RW'):
        lhs, rhs_ = conclusion(text, name).rsplit(' = ', 1)
        e = lean_to_sympy(lhs, reps).subs(vals) - lean_to_sympy(rhs_, reps).subs(vals)
        check(f"4. {name}'s statement, from the file's definitions, holds identically", sp.cancel(e) == 0,
              ' '.join((lhs + '=' + rhs_).split()))
    check('4. H_- (n = 2, delta = 0) at x = 2M/r is (m r + 6M)/r, zero at r0 = -6M/m',
          sp.cancel(H2r - (m * r + 6 * M) / r) == 0 and sp.simplify(H2r.subs(r, -6 * M / m)) == 0)
    rwden = sp.fraction(sp.cancel(Wj ** 2 - Wsj - kap ** 2 / (4 * beta ** 2)))[1]
    check('4. the Darboux partner W^2 - W_* - kappa^2/(4 beta^2) has denominator a power of r (as the job checks: m r + '
          '6M does not divide it)', sp.Poly(rwden, r).as_expr().free_symbols <= {r}
          and sp.rem(sp.Poly(rwden, r), sp.Poly(m * r + 6 * M, r)) != 0 and sp.Poly(rwden, r).is_monomial,
          str(sp.factor(rwden)))
    lead = sp.limit(sp.cancel(VKIj * (r + 6 * M / m) ** 2).subs({m: 4, M: 1}), r, sp.Rational(-3, 2))
    check('4. V_S- itself has a double pole at r0 (m = 4, M = 1: (r - r0)^2 V_S- -> 2 f(r0)^2 = 2(1 + m/3)^2 = 98/9)',
          lead == sp.Rational(98, 9), str(lead))

    # 5: controls, one per new mutation
    p25 = statement(text, 'g_res').replace('p.eval 0 = 576 * Hm', 'p.eval 0 = 575 * Hm').split('p.eval 0 =', 1)[1]
    c25 = lean_to_sympy(p25, (('Hm (mEll ℓ) (dEll ℓ) 2', '(H2)'),)).subs(sp.Symbol('H2'), H2f)
    c26 = claimed + 576 * H2f ** 2 * (a * (a + 1) - a * (a - 1))  # a(a + 1) -> a(a - 1) in the claim
    v0 = sp.cancel(num.subs(z, 0) / den)
    check('5. P3M25, P3M26: N(0) differs from 575 H(2)^2 (...) and from 576 H(2)^2 (l(l - 3)/9 - a(a - 1))',
          sp.cancel(v0 - c25) != 0 and sp.cancel(v0 - c26) != 0)
    d27, m31 = 1 / (4 * (ell + 4)), (ell - 1) * (ell + 5)
    bad = []
    for tag, mm, dd in (('P3M27', mE, d27), ('P3M31', m31, dE)):
        e1 = sp.expand(mm - (ell * (ell + 3) - 4))
        e2 = sp.simplify(1 + 2 * mm * dd - (2 * ell + 3) / 5)
        eh = sp.simplify(Hm.subs({m: mm, delta: dd, x: 2}) - (ell + 3) * (ell + 4))
        eu = sp.simplify(Um.subs({m: mm, delta: dd, x: 2}) - 576 * ((ell + 3) * (ell + 4)) ** 2 * ell * (ell - 3) / 9)
        if not ((e1 != 0 or e2 != 0) and eh != 0 and eu != 0):
            bad.append(tag)
    check('5. P3M27 (delta = 1/(4(l + 4))), P3M31 (m = (l - 1)(l + 5)): mEll_dEll_S5, H2_ell and U2_ell become false',
          not bad, ', '.join(bad))
    poly28 = scert_g_res(Pz=a / z ** 2 + b0 + b1 * z)
    N28 = Nz.subs({U: Um.subs({m: mE, delta: dE, x: x6}), H: Hm.subs({m: mE, delta: dE, x: x6}), F: F6, Fd: F6d,
                   P: a / z ** 2 + b0 + b1 * z, Pd: Prd})
    den28 = sp.fraction(sp.cancel(sp.together(N28)))[1]
    check("5. P3M28 (P = a/z^2 + b0 + b1 z, P' unchanged): N is no longer a polynomial in z; nor with P' = dP/dz",
          den28.has(z) and not poly28[0], f'denominator {sp.factor(den28)}')
    xHh = 2 / (1 + sp.sqrt(1 - sp.Rational(1, 4)))
    F6h = (1 - xHh * (1 - z) ** 3 + xHh ** 2 * (1 - z) ** 6 / 16)
    N29 = Nz.subs({U: Um.subs({m: mE, delta: dE, x: x6}), H: Hm.subs({m: mE, delta: dE, x: x6}), F: F6h,
                   Fd: sp.diff(F6h, z), P: Pr, Pd: Prd})
    den29 = sp.fraction(sp.cancel(sp.together(N29.subs({ell: 2, a: 1, b0: 0, b1: 0}))))[1]
    check('5. P3M29 (f and f_z at q = 1/2, U and H at q = 1): N has a pole at z = 0 (at l = 2, a = 1, b0 = b1 = 0)',
          den29.has(z) and sp.fraction(sp.cancel(sp.together(N29.subs({ell: 2, a: 1, b0: 0, b1: 0}))))[0].subs(z, 0) != 0)
    # P3M30: l = -4 with Lean's 1/0 = 0, so m = 0 and delta = 0
    p0_m4 = Um.subs({m: 0, delta: 0, x: 2}) - 64 * Hm.subs({m: 0, delta: 0, x: 2}) ** 2 * 9 * a * (a + 1)
    c30 = 576 * Hm.subs({m: 0, delta: 0, x: 2}) ** 2 * (sp.Integer(-4) * (-4 - 3) / 9 - a * (a + 1))
    check('5. P3M30: at l = -4 (Lean: dEll = 1/0 = 0, mEll = 0) p(0) = 204800 - 230400 a(a + 1), not g_res\'s value',
          sp.expand(p0_m4 - c30) != 0 and sp.expand(p0_m4 - (204800 - 230400 * a * (a + 1))) == 0,
          str(sp.expand(c30 - p0_m4)))
    Wb = 5 * M * Fc + kap / (2 * beta)
    Wk = beta * Fc + m * (m + 1) / (2 * beta)
    ok32 = all(sp.cancel(Wx ** 2 + s * f * sp.diff(Wx, r) - kap ** 2 / (4 * beta ** 2) - V) != 0
               for Wx in (Wb, Wk) for s, V in ((1, VKIj), (-1, RWj)))
    check('5. P3M32 (beta = 5M in W), P3M33 (kappa = m(m + 1) in W): both Darboux identities become false', ok32)
    check("5. P3M32: W4_deriv's stated derivative is not d/dr of 5M F + kappa/(2 beta)",
          sp.cancel(Wd - sp.diff(Wb, r)) != 0)
    check('5. P3M34 (Regge-Wheeler with m + 1): darboux_RW becomes false',
          sp.cancel(Wj ** 2 - Wsj - kap ** 2 / (4 * beta ** 2) - f * ((m + 1) / r ** 2 - 6 * M / r ** 3)) != 0)
    check('5. P3M35 (sign swapped): W^2 - W_* - kappa^2/(4 beta^2) is not V_S-', sp.cancel(RWj - VKIj) != 0)
    lim0 = sp.limit((VRW4 * r ** 4).subs({m: 4, M: 1}), r, 0)
    check('5. P3M36: Regge-Wheeler is not analytic at r = 0 (m = 4, M = 1: r^4 V -> 12 M^2 = 12)', lim0 == 12, str(lim0))
    check('5. P3M37: H_- at r = -3M/m is -m, not 0', sp.simplify(H2r.subs(r, -3 * M / m) + m) == 0)

    ok = all(results)
    print('ALL P3 V4 CHECKS HOLD' if ok else 'A CHECK FAILED', f'({sum(results)}/{len(results)})')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
