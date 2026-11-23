"""check_p3v3.py: checks of the bh-modes p3 Lean layer v3 (the general-n instance) outside Lean (session-L, 2026-10-23).

Run with an interpreter that has sympy, from this folder:
    python3 -I -B check_p3v3.py ../lean/BHModesP3.lean
It reads only the Lean file named on the command line. It exits 0 only if every check holds.

 1. Lines 1-520 are the v2 build's (sha256 of that prefix); the v3 section follows; the file ends with the namespace.
 2. The bodies of HmN and UmN are the c_n layer's Hm and Um, byte for byte (sha256 of each body).
 3. The file's own UmN at K = 1, y = 0 and HmN, parsed, equal the bh-modes lead's transcription of S5 (5.63b) and
    (5.62b) in code/ki/potentials.py (U_minus, H_minus; typed into this file below), symbolically in n.
 4. At n = 4 they equal the file's own TARGET.md polynomials Um and Hm (parsed), independently of UmN_four.
 5. The file's own Fn' is d/dz of its own Fn, for n = 2, ..., 12 (x_H a symbol).
 6. Fn at z = 1 - 1/rho is 1 - 2M/rho^(n-1) + (qM)^2/rho^(2(n-1)) with x_H = 2M, for n = 2, ..., 12.
 7. METHOD's N at z = 1, built from the parsed U, H, F, F', is 64 m^2 (m + n(n + 2)/4 - P^2 + P), for n = 2, ..., 12.
 8. Signs, exact: f(0) = 0 at q = 0, 3/5, 1 for n = 2, ..., 12; f > 0 and H > 0 on a grid (z, q, m, delta); and the
    controls of P3M19-P3M21: f = 0 at n = 1, f(0) = 1 at q^2 = 2, H = 0 at z = 1, m = 0, n = 2.
 9. prop3_Dn's binders are prop3_D6's with (U6, H6, F6, F6') -> (Un, Hn, Fn, Fn'), except the added n, hn and the
    changed hP, hP' (those of prop3_Ioo, written with set membership); the conclusions agree.
"""

import hashlib
import re
import sys

import sympy as sp

PREFIX_LINES = 520
PREFIX_SHA256 = 'eb9af1c12d32c2883c76d5aa0e89177b635063ffaa7438d1e5cf5acd6d054b29'  # v2 build, 1ade9f3e...
CN_BODY_SHA256 = {  # BHModesCn.lean (8baaffc7...), bodies of Hm and Um
    'HmN': 'f4a710dc71517c9622578c54af45c1d790e33d01a480f66488a90a0e6858b19f',
    'UmN': 'e69e48f7a9bca63111dcaa49750233f256f8f913cc7536195e2de224ea129ef9',
}

results = []


def check(name, ok, detail=''):
    results.append(bool(ok))
    print(f"{'ok  ' if ok else 'FAIL'} {name}{': ' + detail if detail else ''}")


def body(text, head):
    i = text.index(head)
    j = text.index(':=', i) + 2
    k = text.index('\n\n', j)
    return text[j:k]


def header(text, name):
    m = re.search(r'^theorem ' + re.escape(name) + r' ', text, re.M)
    start, depth = m.end(), 0
    for i in range(start, len(text)):
        c = text[i]
        if c in '([{':
            depth += 1
        elif c in ')]}':
            depth -= 1
        elif depth == 0 and text.startswith(':=', i):
            return text[start:i]
    raise SystemExit(f'no := after theorem {name}')


def binders(head):
    groups, depth, cur, rest_at = [], 0, None, None
    for i, c in enumerate(head):
        if c in '([{':
            if depth == 0 and c == '(':
                cur = i
            depth += 1
        elif c in ')]}':
            depth -= 1
            if depth == 0 and cur is not None:
                groups.append(head[cur + 1:i])
                cur = None
        elif depth == 0 and c == ':':
            rest_at = i
            break
    norm = lambda s: ' '.join(s.split())
    return [tuple(norm(p) for p in g.split(':', 1)) for g in groups], norm(head[rest_at + 1:])


n, K, m, delta, x, y, z, q, xH, rho, M, P1, Pd1 = sp.symbols('n K m delta x y z q xH rho M P1 Pd1')
SYMS = {'n': n, 'K': K, 'm': m, 'delta': delta, 'x': x, 'y': y, 'z': z, 'q': q, 'xH': xH}


def lean_to_sympy(s, extra=()):
    s = ' '.join(s.split()).replace('δ', 'delta').replace('^', '**')
    for a, b in extra:
        s = s.replace(a, b)
    return sp.sympify(s, locals=SYMS)


# code/ki/potentials.py (sha256 7d686b40...), U_minus and H_minus, typed here with symbolic n
d = delta
U_MINUS = (- n**3 * (3*n - 2) * (n + 1)**4 * d * (1 + m*d)**3 * x**4
           - 4 * n**2 * (n + 1)**2 * (1 + m*d)**2 * ((n + 1) * (3*n - 2) * m * d - n**2) * x**3
           + 4 * (n + 1) * (1 + m*d) * (m * (n - 2) * (n - 4) * (n + 1) * (m + n**2 * K) * d
                                        + 4 * n * (2*n**2 - 3*n + 4) * m
                                        + n**2 * (n - 2) * (n - 4) * (n + 1) * K) * x**2
           - 16 * m * ((n + 1) * m * (-4*m + 3 * n**2 * (n - 2) * K) * d
                       + 3 * n * (n - 4) * m + 3 * n**2 * (n + 1) * (n - 2) * K) * x
           + 64 * m**3 + 16 * n * (n + 2) * m**2 * K)
H_MINUS = m + sp.Rational(1, 2) * n * (n + 1) * (1 + m*d) * x


def main(path):
    raw = open(path, 'rb').read()
    text = raw.decode('utf-8')
    lines = raw.split(b'\n')

    # 1
    h = hashlib.sha256(b'\n'.join(lines[:PREFIX_LINES]) + b'\n').hexdigest()
    check("1. lines 1-520 are the v2 build's", h == PREFIX_SHA256, f'prefix sha256 {h[:16]}...')
    check('1. the v3 section starts at line 521', lines[PREFIX_LINES].decode('utf-8').startswith('/-! ### v3 (2026-10-23)'))
    check('1. the file ends with the namespace', text.endswith('end BHModes.P3\n'), f'{len(lines) - 1} lines')

    # 2
    bH = body(text, 'noncomputable def HmN (n m δ x : ℝ) : ℝ')
    bU = body(text, 'noncomputable def UmN (n K m δ x y : ℝ) : ℝ')
    for name, b in (('HmN', bH), ('UmN', bU)):
        hb = hashlib.sha256(b.encode('utf-8')).hexdigest()
        check(f"2. {name}'s body is the c_n layer's, byte for byte", hb == CN_BODY_SHA256[name], hb[:16] + '...')

    # 3
    HmN = lean_to_sympy(bH)
    UmN = lean_to_sympy(bU)
    check('3. UmN(K = 1, y = 0) = potentials.py U_minus(n), symbolic n',
          sp.expand(UmN.subs({K: 1, y: 0}) - U_MINUS.subs(K, 1)) == 0)
    check('3. UmN(K, y = 0) = U_minus(n, K), symbolic n and K', sp.expand(UmN.subs(y, 0) - U_MINUS) == 0)
    check('3. HmN = potentials.py H_minus(n), symbolic n', sp.expand(HmN - H_MINUS) == 0)

    # 4
    Um6 = lean_to_sympy(body(text, 'def Um (m δ x : ℝ) : ℝ'))
    Hm6 = lean_to_sympy(body(text, 'def Hm (m δ x : ℝ) : ℝ'))
    check("4. UmN(4, 1, m, delta, x, 0) = the file's TARGET.md Um", sp.expand(UmN.subs({n: 4, K: 1, y: 0}) - Um6) == 0)
    check("4. HmN(4, m, delta, x) = the file's TARGET.md Hm", sp.expand(HmN.subs(n, 4) - Hm6) == 0)

    # 5-7: parsed Fn, Fn', and N at z = 1
    X = '(xH * (1 - z) ** (n - 1))'
    sub = (('xn n q z', X), ('xH q', 'xH'))
    Fn = lean_to_sympy(body(text, 'noncomputable def Fn (n : ℕ) (q z : ℝ) : ℝ'), sub)
    Fd = lean_to_sympy(body(text, "noncomputable def Fn' (n : ℕ) (q z : ℝ) : ℝ"), sub)
    print(f'     parsed Fn  = {Fn}')
    print(f"     parsed Fn' = {Fd}")
    ok5 = all(sp.simplify(sp.diff(Fn.subs(n, k), z) - Fd.subs(n, k)) == 0 for k in range(2, 13))
    check("5. Fn' = d/dz Fn for n = 2..12", ok5)
    ok6 = all(sp.simplify(Fn.subs(n, k).subs({xH: 2 * M, z: 1 - 1 / rho})
                          - (1 - 2 * M / rho ** (k - 1) + (q * M) ** 2 / rho ** (2 * (k - 1)))) == 0
              for k in range(2, 13))
    check('6. Fn(1 - 1/rho) = 1 - 2M/rho^(n-1) + (qM)^2/rho^(2(n-1)), x_H = 2M, n = 2..12', ok6)
    ok7 = True
    for k in range(2, 13):
        Xk = xH * (1 - z) ** (k - 1)
        U = UmN.subs({n: k, K: 1, y: 0, x: Xk})
        H = HmN.subs({n: k, x: Xk})
        F, F1 = Fn.subs(n, k), Fd.subs(n, k)
        N = U - 64 * H ** 2 * ((1 - z) * F1 * P1 + F * (-P1 + (1 - z) * Pd1 + P1 ** 2))
        ok7 = ok7 and sp.expand(N.subs(z, 1) - 64 * m ** 2 * (m + sp.Rational(k * (k + 2), 4) - P1 ** 2 + P1)) == 0
    check('7. N(1) = 64 m^2 (m + n(n + 2)/4 - P(1)^2 + P(1)) for n = 2..12', ok7)

    # 8
    def xH_of(qv):
        return 2 / (1 + sp.sqrt(1 - qv ** 2)) if qv ** 2 <= 1 else sp.Integer(2)  # Real.sqrt of a negative is 0
    ok8a = all(sp.simplify(Fn.subs({n: k, xH: xH_of(qv), q: qv, z: 0})) == 0
               for k in range(2, 13) for qv in (sp.Integer(0), sp.Rational(3, 5), sp.Integer(1)))
    check('8. f(0) = 0 at q = 0, 3/5, 1 for n = 2..12', ok8a)
    zs = [sp.Rational(j, 20) for j in range(1, 20)]
    qs = [sp.Integer(0), sp.Rational(1, 2), sp.Rational(3, 5), sp.Rational(99, 100), sp.Integer(1)]
    fmin = min(Fn.subs({n: k, xH: xH_of(qv), q: qv, z: zv}).evalf(30)
               for k in range(2, 13) for qv in qs for zv in zs)
    check('8. f > 0 on z = j/20 (j = 1..19), q in {0, 1/2, 3/5, 99/100, 1}, n = 2..12', fmin > 0, f'min {fmin:.6g}')
    hmin = min(HmN.subs({n: k, m: mv, delta: dv, x: xH_of(qv) * (1 - zv) ** (k - 1)}).evalf(30)
               for k in range(2, 13) for qv in qs[::2] for zv in zs + [sp.Integer(1)]
               for mv in (sp.Rational(1, 10), sp.Integer(6), sp.Integer(100)) for dv in (sp.Integer(0), sp.Rational(1, 2)))
    check('8. H > 0 on that grid with z = 1 added, m in {1/10, 6, 100}, delta in {0, 1/2}', hmin > 0, f'min {hmin:.6g}')
    c19 = sp.simplify(Fn.subs({n: 1, xH: xH_of(sp.Rational(3, 5)), q: sp.Rational(3, 5), z: sp.Rational(1, 2)}))
    c20 = sp.simplify(Fn.subs({n: 2, xH: xH_of(sp.sqrt(2)), q: sp.sqrt(2), z: 0}))
    c21 = sp.simplify(HmN.subs({n: 2, m: 0, delta: 0, x: xH_of(sp.Integer(0)) * (1 - 1) ** (2 - 1)}))
    check('8. controls: f = 0 at n = 1; f(0) = 1 at q^2 = 2; H = 0 at z = 1, m = 0, n = 2',
          c19 == 0 and c20 == 1 and c21 == 0, f'{c19}, {c20}, {c21}')

    # 9
    b6, c6 = binders(header(text, 'prop3_D6'))
    bD, cD = binders(header(text, 'prop3_Dn'))
    def to_n(s):
        for a, b in (("F6' q", "Fn' n q"), ('U6 q m δ', 'Un n q m δ'), ('H6 q m δ', 'Hn n q m δ'), ('F6 q', 'Fn n q')):
            s = s.replace(a, b)
        return s
    m6 = [(nm, to_n(t)) for nm, t in b6]
    d6, dD = dict(m6), dict(bD)
    extra = [nm for nm, _ in bD if nm not in d6]
    changed = [nm for nm, _ in m6 if nm in dD and dD[nm] != d6[nm]]
    order = [nm for nm, _ in bD if nm in d6] == [nm for nm, _ in m6]
    check("9. prop3_Dn adds exactly n, hn", extra == ['n', 'hn'], ', '.join(f'{e} : {dD[e]}' for e in extra))
    check("9. otherwise only hP and hP' differ, in prop3_Ioo's form", order and changed == ['hP', "hP'"]
          and dD['hP'] == '∀ z ∈ Set.Ioo (0 : ℝ) 1, HasDerivAt P (P\' z) z'
          and dD["hP'"] == "ContinuousOn P' (Set.Ioo (0 : ℝ) 1)",
          '; '.join(f'{c} : {dD[c]}' for c in changed))
    check('9. the conclusions agree', to_n(c6) == cD, cD)

    ok = all(results)
    print('ALL P3 V3 CHECKS HOLD' if ok else 'A CHECK FAILED', f'({sum(results)}/{len(results)})')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
