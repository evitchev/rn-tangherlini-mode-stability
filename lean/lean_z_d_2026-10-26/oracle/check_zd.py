"""check_zd.py: checks of the bh-modes Z Lean layer, item (d) (BHM-126; the lead's message 9), outside Lean
(session-L, 2026-10-26).

Run with an interpreter that has sympy and mpmath, from this folder:
    python3 -I -B check_zd.py ../lean/BHModesZd.lean
It reads only the Lean file named on the command line and the mutations.json beside it. It exits 0 only if every
check holds.

The parser is check_z.py's (application, fun, + - * / ^, unary minus), extended with postfix ⁻¹, type ascriptions
(n : ℝ), dotted names (Real.log) and ∧. The file's own definitions (Hm, Um, mm, δ1, nu, g, W, Ut, Yr, fr, dg, wr, dwr,
Vr, Vtr, u0) become curried Python functions, so the statements checked are the file's text, not a retyping.
Two ways to differentiate in ρ:
- n symbolic: Yr n ρ is replaced by a symbol Y, and d/dρ is the total derivative ∂_ρ − ((n − 1)Y/ρ)∂_Y;
- n = 2..9: Yr n ρ = ρ^(−(n−1)) and d/dρ is sympy's.

 1. Provenance: lines 36-174 are lean_z's BHModesZ.lean lines 25-163, and lines 180-239 are p3 v5's BHModesP3.lean
    lines 86-145 (sha256 of each block); the file ends with the namespace; the theorems are the expected 46.
 2. fr_S5 and Vr_S5 hold identically; dg is ∂_Y g.
 3. Yr_hasDerivAt, fr_hasDerivAt and wr_hasDerivAt: the stated derivatives are the derivatives (n symbolic, n = 2..9).
 4. riccati_plus and riccati_minus hold identically (n symbolic, n = 2..9), with deriv (wr n ℓ) and deriv (g n ℓ)
    computed here; so do V_eq and Vt_eq.
 5. log_u0_hasDerivAt: d(log u₀)/dρ = g/ρ (n symbolic; n = 2..9). Information: Vr − Vtr = 2 f dw/dρ is not 0.
 6. Information, numerically (mpmath, 30 digits), at n = 2, 4, 9: r*(2) = 0; r* increases; r*(ρ) ≥ ρ − 2 (ρ ≥ 2);
    r*(ρ) ≤ (1 − 1/(ρ − 1))/(n − 1)² (1 < ρ ≤ 2); R = (r*)⁻¹ at t = −1000..1000 with dR/dt = f(R); and the
    S-deformation identity ∫(fφ_ρ² + Vφ²/f)dρ = ∫(fφ_ρ − wφ)²/f dρ for a bump φ at n = 4, ℓ = 2 (the form of
    A_{ℓ,1} in ρ, with dr* = dρ/f).
 7. Controls: each spec of mutations.json (ZD1-ZD15), applied as text, makes its target false (algebraically where
    the target is an identity, numerically where it is an analytic statement).
"""

import hashlib
import json
import os
import re
import sys

import mpmath as mp
import sympy as sp

Z_BLOCK = (36, 174, 'db0d9ea14a33f02ce180652050e42bd6b47fdc672c949e4b62ff708c23da61ff')  # lean_z l. 25-163
P_BLOCK = (180, 239, '1e4354ce068c108d827907a5486da79f2e88d74622562f7a2602552c15f4a307')  # p3 v5 l. 86-145
EXPECTED_THEOREMS = [
    'gate_q1', 'gate_H', 'g_hasDerivAt', 'deriv_g', 'z_id', 'partner', 'partner_n4', 'partner_ends', 'partner_no_pole',
    'sdef_identity', 'form_nonneg_of_sdef',
    'fr_S5', 'Yr_mem', 'fr_pos', 'fr_le_one', 'one_sub_Yr_le', 'fr_le_sq', 'Yr_hasDerivAt', 'fr_hasDerivAt',
    'invfr_continuousOn', 'tort_hasDerivAt', 'tort_strictMonoOn', 'tort_ge', 'tort_le', 'tort_surjOn', 'tort_bijOn',
    'tortoise_q1', 'Rt_spec', 'Rt_tort', 'Rt_strictMono', 'Rt_continuous', 'Rt_hasDerivAt', 'Vr_S5', 'wr_hasDerivAt',
    'riccati_plus', 'riccati_minus', 'V_eq', 'Vt_eq', 'u0_pos', 'log_u0_hasDerivAt', 'w_log_deriv', 'S_eq',
    'W_continuousAt', 'Vr_continuousAt', 'zero_mode', 'A_nonneg']

results = []


def check(name, ok, detail=''):
    results.append(bool(ok))
    print(f"{'ok  ' if ok else 'FAIL'} {name}{': ' + detail if detail else ''}")


# ---------------------------------------------------------------- a small Lean term parser
TOKEN = re.compile(r"\s*(?:(=>)|(⁻¹)|(\d+)|([A-Za-z_Ͱ-Ͽᴀ-ᶿℓ][A-Za-z0-9_'.Ͱ-Ͽ₀-₉ℓ]*)|(\S))")


def tokens(s):
    out, i = [], 0
    while i < len(s):
        m = TOKEN.match(s, i)
        if not m or m.end() == i:
            if s[i:].strip() == '':
                break
            raise SystemExit(f'cannot tokenise at {s[i:i + 20]!r}')
        arrow, inv, num, ident, sym = m.groups()
        out.append(('=>', '=>') if arrow else ('inv', '⁻¹') if inv else ('num', num) if num
                   else ('id', ident) if ident else ('sym', sym))
        i = m.end()
    return out


class Parser:
    BIN = {'+': 65, '-': 65, '*': 70, '/': 70, '^': 75, '=': 50}

    def __init__(self, s):
        self.t, self.i = tokens(s), 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else ('eof', None)

    def take(self):
        tok = self.peek()
        self.i += 1
        return tok

    def starts_atom(self, tok):
        return tok[0] in ('num', 'id') and tok[1] != 'fun' or tok == ('sym', '(')

    def expr(self, rbp=0):
        left = self.nud(self.take())
        while True:
            tok = self.peek()
            if tok[0] == 'inv':
                self.take()
                left = ('inv', left)
            elif tok[0] == 'sym' and tok[1] in self.BIN:
                lbp = self.BIN[tok[1]]
                if lbp <= rbp:
                    break
                self.take()
                right = self.expr(lbp - 1 if tok[1] == '^' else lbp)
                left = ('bin', tok[1], left, right)
            elif self.starts_atom(tok) or tok == ('id', 'fun'):
                if 1024 <= rbp:
                    break
                left = ('app', left, self.expr(1024))
            else:
                break
        return left

    def nud(self, tok):
        if tok == ('id', 'fun'):
            var = self.take()[1]
            assert self.take() == ('=>', '=>'), 'expected =>'
            return ('lam', var, self.expr(0))
        if tok == ('sym', '('):
            e = self.expr(0)
            if self.peek() == ('sym', ':'):          # a type ascription (n : ℝ)
                depth = 0
                while not (self.peek() == ('sym', ')') and depth == 0):
                    t = self.take()
                    depth += (t == ('sym', '(')) - (t == ('sym', ')'))
            assert self.take() == ('sym', ')'), 'expected )'
            return e
        if tok == ('sym', '-'):
            return ('neg', self.expr(74))
        if tok[0] == 'num':
            return ('num', int(tok[1]))
        if tok[0] == 'id':
            return ('var', tok[1])
        raise SystemExit(f'unexpected token {tok}')


def parse(s):
    p = Parser(' '.join(s.split()))
    e = p.expr(0)
    assert p.peek()[0] == 'eof', f'trailing tokens {p.t[p.i:]}'
    return e


T = sp.Symbol('t_dummy')


def evaluate(node, env):
    kind = node[0]
    if kind == 'num':
        return sp.Integer(node[1])
    if kind == 'var':
        if node[1] not in env:
            raise SystemExit(f'unknown name {node[1]}')
        return env[node[1]]
    if kind == 'app':
        return evaluate(node[1], env)(evaluate(node[2], env))
    if kind == 'neg':
        return -evaluate(node[1], env)
    if kind == 'inv':
        return 1 / evaluate(node[1], env)
    if kind == 'lam':
        return lambda v, n=node, e=env: evaluate(n[2], {**e, n[1]: v})
    if kind == 'bin':
        a, b = evaluate(node[2], env), evaluate(node[3], env)
        return {'+': lambda: a + b, '-': lambda: a - b, '*': lambda: a * b, '/': lambda: a / b,
                '^': lambda: a ** b, '=': lambda: (a, b)}[node[1]]()
    raise SystemExit(f'bad node {node}')


def definition(text, name):
    m = re.search(r'^(?:noncomputable )?def ' + re.escape(name) + r' ((?:\([^)]*\) ?)*): [^\n]*?:=', text, re.M)
    if m is None:
        raise SystemExit(f'no def {name}')
    params = [p for grp in re.findall(r'\(([^)]*)\)', m.group(1)) for p in grp.split(':')[0].split()]
    k = text.index('\n\n', m.end())
    return params, text[m.end():k]


def curried(params, body, env):
    tree = parse(body)

    def build(bound, rest):
        if not rest:
            return evaluate(tree, {**env, **bound})
        return lambda v: build({**bound, rest[0]: v}, rest[1:])
    return build({}, params)


def header(text, name):
    m = re.search(r'^theorem ' + re.escape(name) + r' ', text, re.M)
    if m is None:
        raise SystemExit(f'no theorem {name}')
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


def split_header(h):
    groups, depth, cur = [], 0, None
    for i, c in enumerate(h):
        if c in '([{':
            if depth == 0:
                cur = i
            depth += 1
        elif c in ')]}':
            depth -= 1
            if depth == 0:
                groups.append(h[cur + 1:i])
        elif depth == 0 and c == ':':
            return groups, h[i + 1:].strip()
    raise SystemExit('no conclusion')


DEFS = ('Hm', 'Um', 'mm', 'δ1', 'nu', 'g', 'W', 'Ut', 'Yr', 'fr', 'dg', 'wr', 'dwr', 'Vr', 'Vtr', 'u0')
n, l, rho, Y = sp.symbols('n ell rho Y', positive=True)


def file_env(text, mode, nval=None):
    """mode 'Y': Yr n ρ is the symbol Y, deriv is the total d/dρ (on functions of ρ) or ∂_Y (on functions of Y).
    mode 'rho': Yr n ρ = ρ^(−(n−1)) with n = nval, deriv is sympy's d/dρ (or d/dY for functions of Y)."""
    env = {'Real.log': sp.log}

    def deriv(f):
        def at(x):
            if x == rho:                                    # a function of ρ
                e = f(rho)
                if mode == 'Y':
                    return sp.diff(e, rho) + sp.diff(e, Y) * (-(n - 1) * Y / rho)
                return sp.diff(e, rho)
            return sp.diff(f(T), T).subs(T, x)              # a function of another variable (g's Y)
        return at
    env['deriv'] = deriv
    env['HasDerivAt'] = lambda f: lambda d: lambda x: (deriv(f)(x), d)
    for name in DEFS:
        params, body = definition(text, name)
        env[name] = curried(params, body, env)
        if name == 'Yr':
            env['Yr'] = (lambda nn: lambda r: Y) if mode == 'Y' else (lambda nn: lambda r: r ** (-(nval - 1)))
    return env


def zero(e):
    e = sp.together(sp.expand_log(e, force=True))
    num, _ = sp.fraction(e)
    num = sp.expand(num)
    if num.is_polynomial(*sorted(num.free_symbols, key=str)):
        return num == 0
    return sp.simplify(e) == 0


def statement_pairs(text, name, mode, nval=None):
    env = {**file_env(text, mode, nval), 'n': n if mode == 'Y' else sp.Integer(nval), 'ℓ': l, 'ρ': rho}
    _, concl = split_header(header(text, name))
    return [evaluate(parse(part), env) for part in concl.split(' ∧ ')]


def holds(text, name, mode, nval=None):
    return all(zero(a - b) for a, b in statement_pairs(text, name, mode, nval))


def holds_all(text, name):
    return holds(text, name, 'Y') and all(holds(text, name, 'rho', k) for k in range(2, 10))


# ---------------------------------------------------------------- numerics (information)
mp.mp.dps = 30


def f_num(nn, r):
    return (1 - r ** (-(nn - 1))) ** 2


def tort_num(nn, r):
    return mp.quad(lambda s: 1 / f_num(nn, s), [2, r]) if r != 2 else mp.mpf(0)


def R_num(nn, t):
    guess = 1 + 1 / ((nn - 1) ** 2 * (1 + abs(t))) if t < 0 else 2 + t
    return mp.findroot(lambda r: tort_num(nn, r) - t, (guess, guess * 1.0001 if t >= 0 else 1 + (guess - 1) * 1.5),
                       solver='secant')


def numeric_pieces(text, nn, ll):
    env = {**file_env(text, 'rho', nn), 'n': sp.Integer(nn), 'ℓ': sp.Integer(ll), 'ρ': rho}
    w = env['wr'](sp.Integer(nn))(sp.Integer(ll))(rho)
    V = env['Vr'](sp.Integer(nn))(sp.Integer(ll))(rho)
    f = env['fr'](sp.Integer(nn))(rho)
    return (sp.lambdify(rho, w, 'mpmath'), sp.lambdify(rho, V, 'mpmath'), sp.lambdify(rho, f, 'mpmath'))


def bump(a, b):
    def phi(r):
        if r <= a or r >= b:
            return mp.mpf(0)
        return mp.exp(-1 / ((r - a) * (b - r)))
    return phi


def forms(text, nn, ll, a, b, shift=0):
    w, V, f = numeric_pieces(text, nn, ll)
    phi = bump(a, b)
    dphi = lambda r: mp.diff(phi, r)
    lhs = mp.quad(lambda r: f(r) * dphi(r) ** 2 + (V(r) - shift) * phi(r) ** 2 / f(r), [a, (a + b) / 2, b])
    rhs = mp.quad(lambda r: (f(r) * dphi(r) - w(r) * phi(r)) ** 2 / f(r), [a, (a + b) / 2, b])
    return lhs, rhs


def main(path):
    raw = open(path, 'rb').read()
    text = raw.decode('utf-8')
    lines = raw.split(b'\n')

    # 1
    for (a, b, want), what in ((Z_BLOCK, "lean_z's lines 25-163"), (P_BLOCK, "p3 v5's lines 86-145")):
        h = hashlib.sha256(b'\n'.join(lines[a - 1:b]) + b'\n').hexdigest()
        check(f'1. lines {a}-{b} are {what}', h == want, f'sha256 {h[:16]}...')
    check('1. the file ends with the namespace', text.endswith('end BHModes.Z\n'), f'{len(lines) - 1} lines')
    names = re.findall(r"^theorem ([A-Za-z0-9_']+)", text, re.M)
    check('1. the theorems are the expected 46, in order', names == EXPECTED_THEOREMS, f'{len(names)} theorems')

    # 2
    check('2. fr_S5 holds identically', holds(text, 'fr_S5', 'Y'))
    check('2. Vr_S5 holds identically', holds(text, 'Vr_S5', 'Y'))
    envY = {**file_env(text, 'Y'), 'n': n, 'ℓ': l}
    check("2. dg is ∂_Y g", zero(envY['dg'](n)(l)(Y) - sp.diff(envY['g'](n)(l)(Y), Y)))

    # 3
    for name in ('Yr_hasDerivAt', 'fr_hasDerivAt', 'wr_hasDerivAt'):
        check(f'3. {name}: the stated derivative is the derivative (n symbolic; n = 2..9)', holds_all(text, name))

    # 4
    for name in ('riccati_plus', 'riccati_minus', 'V_eq', 'Vt_eq'):
        check(f'4. {name} holds identically (n symbolic; n = 2..9)', holds_all(text, name))

    # 5
    check('5. log_u0_hasDerivAt: d(log u₀)/dρ = g/ρ (n symbolic; n = 2..9)', holds_all(text, 'log_u0_hasDerivAt'))
    envY = {**file_env(text, 'Y'), 'n': n, 'ℓ': l}
    check('5. information: Vr − Vtr is not 0', not zero(envY['Vr'](n)(l)(rho) - envY['Vtr'](n)(l)(rho)))

    # 6
    ok_t = True
    for nn in (2, 4, 9):
        ok_t &= abs(tort_num(nn, mp.mpf(2))) < mp.mpf(10) ** -25
        pts = [mp.mpf(x) for x in ('1.001', '1.01', '1.3', '1.9', '2', '2.5', '5', '20')]
        vals = [tort_num(nn, r) for r in pts]
        ok_t &= all(x < y for x, y in zip(vals, vals[1:]))
        ok_t &= all(tort_num(nn, r) >= r - 2 for r in pts if r >= 2)
        ok_t &= all(tort_num(nn, r) <= (1 - 1 / (r - 1)) / (nn - 1) ** 2 for r in pts if r <= 2)
    check('6. information: r*(2) = 0, r* increases, r* ≥ ρ − 2, r* ≤ (1 − 1/(ρ − 1))/(n − 1)² (n = 2, 4, 9)', ok_t)
    worst = mp.mpf(0)
    for nn in (2, 4, 9):
        for t in (-1000, -10, 0, 10, 1000):
            R = R_num(nn, mp.mpf(t))
            dR = mp.diff(lambda s: R_num(nn, s), mp.mpf(t))
            worst = max(worst, abs(tort_num(nn, R) - t), abs(dR - f_num(nn, R)) / f_num(nn, R))
    check('6. information: R(t) inverts r* and dR/dt = f(R) at t = −1000..1000 (n = 2, 4, 9)',
          worst < mp.mpf(10) ** -8, mp.nstr(worst, 3))
    lhs, rhs = forms(text, 4, 2, mp.mpf('1.2'), mp.mpf(4))
    check('6. information: the S-deformation identity for a bump at n = 4, ℓ = 2, both sides > 0',
          abs(lhs - rhs) < mp.mpf(10) ** -15 * abs(lhs) and rhs > 0, f'{mp.nstr(lhs, 12)} vs {mp.nstr(rhs, 12)}')

    # 7
    specs = json.load(open(os.path.join(os.path.dirname(path), 'mutations.json'), encoding='utf-8'))
    for spec in specs:
        sid, target = spec['id'], spec['decl']
        if text.count(spec['old']) != 1:
            check(f'7. {sid}: its old string occurs once', False)
            continue
        mutated = text.replace(spec['old'], spec['new'])
        try:
            false = CONTROL[sid](text, mutated, target) if sid in CONTROL else not holds_all(mutated, target)
        except (SystemExit, Exception) as exc:
            check(f'7. {sid}: the mutated {target} is false', False, f'evaluation failed: {exc}')
            continue
        check(f'7. {sid}: the mutated {target} is false', false, spec['note'])

    ok = all(results)
    print('ALL ZD CHECKS HOLD' if ok else 'A CHECK FAILED', f'({sum(results)}/{len(results)})')
    return 0 if ok else 1


def _no_preimage_of_minus_one(text, mutated, target):
    # tort(2) = 0 and tort increases, so tort > 0 on (2, ∞): −1 ∈ univ has no preimage in Ioi 2.
    return all(abs(tort_num(nn, mp.mpf(2))) < mp.mpf(10) ** -25 and tort_num(nn, mp.mpf('2.0001')) > 0
               for nn in (2, 4, 9))


def _increases(text, mutated, target):
    return all(tort_num(nn, mp.mpf('1.5')) < tort_num(nn, mp.mpf(3)) for nn in (2, 4, 9))


def _tort_derivative_is_one_over_f(text, mutated, target):
    r = mp.mpf(3)
    return all(abs(mp.diff(lambda s: tort_num(nn, s), r) * f_num(nn, r) - 1) < mp.mpf(10) ** -10 for nn in (2, 4, 9))


def _dR_is_f(text, mutated, target):
    out = True
    for nn in (2, 4, 9):
        R = R_num(nn, mp.mpf(0))
        dR = mp.diff(lambda s: R_num(nn, s), mp.mpf(0))
        out &= abs(dR - f_num(nn, R)) < mp.mpf(10) ** -10 and abs(dR - 1 / f_num(nn, R)) > mp.mpf(10) ** -3
    return out


def _zero_mode_partner(text, mutated, target):
    envY = {**file_env(text, 'Y'), 'n': n, 'ℓ': l}
    return not zero(envY['Vr'](n)(l)(rho) - envY['Vtr'](n)(l)(rho))


def _form_shift_negative(text, mutated, target):
    lhs, _ = forms(text, 4, 2, mp.mpf(100), mp.mpf(300), shift=1)
    return lhs < 0


def _tort_le_mutated(text, mutated, target):
    r = mp.mpf('1.001')
    return tort_num(3, r) > (1 - 1 / (r - 1)) / (3 - 1)


def _bernoulli_mutated(text, mutated, target):
    nn, r = 2, sp.Integer(2)
    return 1 - r ** (-(nn - 1)) > (nn - 2) * (r - 1)


CONTROL = {
    'ZD1': _no_preimage_of_minus_one,
    'ZD2': _increases,
    'ZD3': _tort_derivative_is_one_over_f,
    'ZD4': _dR_is_f,
    'ZD10': _zero_mode_partner,
    'ZD11': _form_shift_negative,
    'ZD13': _tort_le_mutated,
    'ZD14': _bernoulli_mutated,
}

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
