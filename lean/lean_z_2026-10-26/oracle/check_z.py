"""check_z.py: checks of the bh-modes Z Lean layer (BHM-126, the extremal zero mode) outside Lean (session-L,
2026-10-26).

Run with an interpreter that has sympy and mpmath, from this folder:
    python3 -I -B check_z.py ../lean/BHModesZ.lean [POTENTIALS_PY]
It reads only the files named on the command line. It exits 0 only if every check holds.

A small parser reads Lean terms (application by juxtaposition, fun x => e, + - * / ^, unary minus) and evaluates them
in sympy. The file's own definitions (Hm, Um, mm, δ1, nu, g, W, Ut) become curried Python functions, and
deriv f y is sympy's derivative of f at y. So the statements checked below are the file's text, not a retyping.
(The parser is check_p3v5.py's, with ℓ added to the identifier characters, HasDerivAt read as a pair, and ∧ split.)

 1. Provenance: the c_n layer's definitions in the file (from `/-- S5 (5.62b) at general n. -/` to the line of
    `def δ1`) are lean_cn_2026-10-23's lines 24-43, byte for byte (sha256 of that block); the file ends with the
    namespace; the theorem names are the expected ones.
 2. (b) gate_q1 and gate_H hold identically in n, ℓ and Y.
 3. g_hasDerivAt's derivative is sympy's derivative of the file's g, and deriv_g's conclusion holds.
 4. (a) z_id holds identically in n, ℓ and Y, with ∂_Y g computed by sympy from the file's g (not taken from
    g_hasDerivAt). Information: without the ∂_Y g term, or with g's coefficient −1 in the bracket replaced by +1, it
    does not.
 5. (c) partner holds identically; partner_n4 and partner_ends hold identically. partner_no_pole: its function is
    partner's left side, character for character; its binders are as expected; and at the zero Y₀ = (1 − ℓ)/n of
    (ℓ − 1) + nY, the expression at Y₀ ± 10⁻²⁰ is within 10⁻¹⁵ of Ut(Y₀) at sample (n, ℓ) (mpmath, 60 digits).
 6. Information: g = ρ ∂_ρ log u₀ for u₀ = ρ^(−ν)(1 − Y)^(−ℓ/(n−1))/((ℓ − 1) + nY), Y = ρ^(−(n−1)), at sample
    points (mpmath, 50 digits). With POTENTIALS_PY (bh-modes code/ki/potentials.py), the file's Um and Hm at K = 1,
    y = 0 equal U_minus(n) and H_minus(n) there for n = 2..11.
 7. Controls: each spec of mutations.json (ZM1-ZM17), applied as text to this file, makes its target false.
    - For a changed conclusion or definition: the target's conclusion no longer holds identically.
    - ZM11 and ZM12 weaken a hypothesis. They are shown false at a point the weakened hypotheses allow, evaluated
      with Lean's conventions: x/0 = 0, and deriv f y = 0 where f is not differentiable (g is unbounded near its
      pole when n(n − 1)(ℓ − 1) ≠ 0).
    - ZM17 moves P-reg's limit to Ut(Y₀) + 1; the expression's values near Y₀ approach Ut(Y₀) instead.
"""

import hashlib
import importlib.util
import json
import os
import re
import sys

import mpmath as mp
import sympy as sp

CN_BLOCK_SHA256 = 'ef3ad025862f7547d67a12e577ba686a9853b5d80f02e831a050ba1b382d2bda'  # lean_cn_2026-10-23 BHModesCn.lean lines 24-43
EXPECTED_THEOREMS = ['gate_q1', 'gate_H', 'g_hasDerivAt', 'deriv_g', 'z_id', 'partner', 'partner_n4', 'partner_ends',
                     'partner_no_pole']

results = []


def check(name, ok, detail=''):
    results.append(bool(ok))
    print(f"{'ok  ' if ok else 'FAIL'} {name}{': ' + detail if detail else ''}")


# ---------------------------------------------------------------- a small Lean term parser (check_p3v5.py's)
TOKEN = re.compile(r"\s*(?:(=>)|(\d+)|([A-Za-z_Ͱ-Ͽᴀ-ᶿℓ][A-Za-z0-9_'Ͱ-Ͽ₀-₉ℓ]*)|(\S))")


def tokens(s):
    out, i = [], 0
    while i < len(s):
        m = TOKEN.match(s, i)
        if not m or m.end() == i:
            if s[i:].strip() == '':
                break
            raise SystemExit(f'cannot tokenise at {s[i:i + 20]!r}')
        arrow, num, ident, sym = m.groups()
        out.append(('=>', '=>') if arrow else ('num', num) if num else ('id', ident) if ident else ('sym', sym))
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
            if tok[0] == 'sym' and tok[1] in self.BIN:
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
            assert self.take() == ('sym', ')'), 'expected )'
            return e
        if tok == ('sym', '-'):
            return ('neg', self.expr(74))  # as in Lean: -x ^ 2 is -(x ^ 2), -a * b is (-a) * b
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


def deriv(f):
    return lambda y: sp.diff(f(T), T).subs(T, y)


def has_deriv_at(f):
    return lambda d: lambda y: (sp.diff(f(T), T).subs(T, y), d)


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
    if kind == 'lam':
        return lambda v, n=node, e=env: evaluate(n[2], {**e, n[1]: v})
    if kind == 'bin':
        a, b = evaluate(node[2], env), evaluate(node[3], env)
        div = env.get('__div__', lambda x, y: x / y)
        return {'+': lambda: a + b, '-': lambda: a - b, '*': lambda: a * b, '/': lambda: div(a, b),
                '^': lambda: a ** b, '=': lambda: (a, b)}[node[1]]()
    raise SystemExit(f'bad node {node}')


def definition(text, name):
    """(parameter names, body) of `def name (params) : type := body`."""
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
    """(binder groups as text, conclusion)."""
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


DEFS = ('Hm', 'Um', 'mm', 'δ1', 'nu', 'g', 'W', 'Ut')
n, l, Y = sp.symbols('n ell Y')


def lean_div(a, b):
    """Lean's division on ℝ: x / 0 = 0."""
    return sp.Integer(0) if b == 0 else a / b


def file_env(text, lean=False):
    """The file's own definitions, as curried functions (later ones may use earlier ones)."""
    env = {'deriv': deriv, 'HasDerivAt': has_deriv_at}
    if lean:
        env['__div__'] = lean_div
    for name in DEFS:
        params, body = definition(text, name)
        env[name] = curried(params, body, env)
    return env


def zero(e):
    """e ≡ 0 as a rational function: its numerator over a common denominator expands to 0. A numerator that is not
    a polynomial (an unresolved nested fraction) falls back to cancel."""
    num, _ = sp.fraction(sp.together(e))
    num = sp.expand(num)
    if num.is_polynomial(*sorted(num.free_symbols, key=str)):
        return num == 0
    return sp.cancel(sp.together(sp.expand(e))) == 0


def conclusion_pairs(text, name):
    """The theorem's conclusion as a list of (lhs, rhs), evaluated with n, ℓ, Y as symbols."""
    env = {**file_env(text), 'n': n, 'ℓ': l, 'Y': Y}
    _, concl = split_header(header(text, name))
    return [evaluate(parse(part), env) for part in concl.split(' ∧ ')]


def holds(text, name):
    return all(zero(a - b) for a, b in conclusion_pairs(text, name))


# ZM11 and ZM12 weaken a hypothesis; each is refuted at a point the weakened hypotheses allow and the original ones
# do not, with Lean's conventions. deriv0: Lean's deriv of g at its pole is 0, since g is not differentiable there.
WITNESS = {
    'ZM11': ({'n': 1, 'ℓ': -1}, False),                          # n + 1 = 2, ℓ + n = 0: Lean's δ1 = 1/0 = 0
    'ZM12': ({'n': 4, 'ℓ': 3, 'Y': sp.Rational(-1, 2)}, True),   # (ℓ − 1) + nY = 0, 1 − Y = 3/2: the pole of g
}


def witness_false(text, mutated, target, point, deriv0):
    env = {**file_env(mutated, lean=True), **{k: sp.sympify(v) for k, v in point.items()}}
    if deriv0:
        env['deriv'] = lambda f: lambda y: sp.Integer(0)

    def hyps(t):
        groups, _ = split_header(header(t, target))
        out = []
        for grp in groups:
            if '≠' in grp:
                a, b = grp.split(':', 1)[1].split('≠')
                out.append(evaluate(parse(a), env) != evaluate(parse(b), env))
        return out
    allowed = all(hyps(mutated))            # the weakened hypotheses hold at the point
    excluded = not all(hyps(text))          # an original hypothesis fails there
    _, concl = split_header(header(mutated, target))
    pairs = [evaluate(parse(part), env) for part in concl.split(' ∧ ')]
    fails = any(sp.simplify(a - b) != 0 for a, b in pairs)
    return allowed and excluded and fails


def partner_near_zero(text, offset=0):
    """max over sample (n, ℓ) of |E(Y₀ ± ε) − (Ut(Y₀) + offset)| at the zero Y₀ = (1 − ℓ)/n, and min |W(Y₀ ± ε)|."""
    env = {**file_env(text), 'n': n, 'ℓ': l, 'Y': Y}
    gv = env['g'](n)(l)(Y)
    E = (1 - Y) ** 2 * (gv ** 2 + gv + (n - 1) * Y * sp.diff(gv, Y)) - 2 * (n - 1) * Y * (1 - Y) * gv
    fE = sp.lambdify((n, l, Y), E, 'mpmath')
    fU = sp.lambdify((n, l, Y), env['Ut'](n)(l)(Y), 'mpmath')
    fW = sp.lambdify((n, l, Y), env['W'](n)(l)(Y), 'mpmath')
    mp.mp.dps = 60
    worst, wmin = mp.mpf(0), mp.inf
    for nn, ll in [(4, 2), (4, 3), (5, 2), (9, 7), ('6.5', '2.25')]:
        nn, ll = mp.mpf(nn), mp.mpf(ll)
        y0 = (1 - ll) / nn
        for eps in (mp.mpf(10) ** -20, -mp.mpf(10) ** -20):
            worst = max(worst, abs(fE(nn, ll, y0 + eps) - (fU(nn, ll, y0) + offset)))
            wmin = min(wmin, abs(fW(nn, ll, y0 + eps)))
    return worst, wmin


def main(path, potentials=None):
    raw = open(path, 'rb').read()
    text = raw.decode('utf-8')
    lines = raw.split(b'\n')

    # 1
    start = next(i for i, ln in enumerate(lines) if ln == '/-- S5 (5.62b) at general n. -/'.encode())
    stop = next(i for i, ln in enumerate(lines) if ln.startswith(b'def \xce\xb41 '))
    block = b'\n'.join(lines[start:stop + 1]) + b'\n'
    h = hashlib.sha256(block).hexdigest()
    check(f'1. lines {start + 1}-{stop + 1} are the c_n layer\'s definitions (lean_cn_2026-10-23, l. 24-43)',
          h == CN_BLOCK_SHA256, f'sha256 {h[:16]}...')
    check('1. the file ends with the namespace', text.endswith('end BHModes.Z\n'), f'{len(lines) - 1} lines')
    names = re.findall(r"^theorem ([A-Za-z0-9_']+)", text, re.M)
    check('1. the theorems are the expected ones, in order', names == EXPECTED_THEOREMS, ', '.join(names))

    # 2
    check('2. gate_q1: (n + 1)^2 δ1 (1 + m δ1) = 1 holds identically', holds(text, 'gate_q1'))
    check('2. gate_H: H₋(2Y) = (ℓ + n)((ℓ − 1) + nY) holds identically', holds(text, 'gate_H'))

    # 3
    check("3. g_hasDerivAt: the stated derivative is sympy's derivative of the file's g", holds(text, 'g_hasDerivAt'))
    check("3. deriv_g's conclusion holds", holds(text, 'deriv_g'))

    # 4
    check('4. z_id holds identically in n, ℓ, Y (∂_Y g by sympy from the file\'s g)', holds(text, 'z_id'))
    env = {**file_env(text), 'n': n, 'ℓ': l, 'Y': Y}
    gv = env['g'](n)(l)(Y)
    gY = sp.diff(gv, Y)
    Wv = env['W'](n)(l)(Y)
    no_d = 2 * (n - 1) * Y * (1 - Y) * gv + (1 - Y) ** 2 * (gv ** 2 - gv) - Wv
    plus_g = 2 * (n - 1) * Y * (1 - Y) * gv + (1 - Y) ** 2 * (gv ** 2 + gv - (n - 1) * Y * gY) - Wv
    check('4. information: without the ∂_Y g term, or with +g in the bracket, z_id fails',
          not zero(no_d) and not zero(plus_g))
    check('4. sanity: W is not constant in Y', not zero(sp.diff(Wv, Y)))

    # 5
    check('5. partner holds identically in n, ℓ, Y', holds(text, 'partner'))
    check('5. partner_n4 holds identically', holds(text, 'partner_n4'))
    check('5. partner_ends holds identically', holds(text, 'partner_ends'))
    groups, concl = split_header(header(text, 'partner_no_pole'))
    bnames = [b.split(':', 1)[0].strip() for b in groups]
    check("5. partner_no_pole's binders", bnames == ['n ℓ Y₀', 'hn', 'hY'], ', '.join(bnames))
    lam = re.search(r'^Filter\.Tendsto \(fun Y => (.*)\) \(nhdsWithin Y₀ \{Y₀\}ᶜ\) \(nhds \(Ut n ℓ Y₀\)\)$', concl)
    p_lhs = split_header(header(text, 'partner'))[1]
    p_lhs = p_lhs[:p_lhs.rindex(' = Ut n ℓ Y')].strip()
    check("5. partner_no_pole's function is partner's left side, character for character",
          lam is not None and lam.group(1).strip() == p_lhs)
    near, wpole = partner_near_zero(text)
    check('5. at Y₀ = (1 − ℓ)/n, the partner expression at Y₀ ± 10⁻²⁰ is within 10⁻¹⁵ of Ut(Y₀)',
          near < mp.mpf(10) ** -15, mp.nstr(near, 3))
    check('5. information: W itself has a pole there (|W(Y₀ ± 10⁻²⁰)| > 10³⁰)', wpole > mp.mpf(10) ** 30,
          mp.nstr(wpole, 3))

    # 6
    mp.mp.dps = 50
    worst = mp.mpf(0)
    gfun = sp.lambdify((n, l, Y), gv, 'mpmath')
    for (nn, ll, rho) in [(4, 2, '1.7'), (5, 3, '1.2'), (9, 7, '3.3'), (6.5, 2.25, '1.05'), (11, 30, '2.0')]:
        nn, ll, rho = mp.mpf(nn), mp.mpf(ll), mp.mpf(rho)
        nu = ll + nn / 2 - 1
        u0 = lambda r: r ** (-nu) * (1 - r ** (-(nn - 1))) ** (-ll / (nn - 1)) / ((ll - 1) + nn * r ** (-(nn - 1)))
        lhs = rho * mp.diff(lambda r: mp.log(u0(r)), rho)
        worst = max(worst, abs(lhs - gfun(nn, ll, rho ** (-(nn - 1)))))
    check('6. information: g = ρ ∂_ρ log u₀ at five sample points', worst < mp.mpf(10) ** -40, mp.nstr(worst, 3))
    if potentials:
        digest = hashlib.sha256(open(potentials, 'rb').read()).hexdigest()
        spec = importlib.util.spec_from_file_location('bhm_potentials', potentials)
        P = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(P)
        same = True
        for nn in range(2, 12):
            subs = {P.m: sp.Symbol('m'), P.d: sp.Symbol('delta'), P.x: sp.Symbol('x')}
            U_code = P.U_minus(nn).subs(subs)
            H_code = P.H_minus(nn).subs(subs)
            U_file = env['Um'](sp.Integer(nn))(1)(sp.Symbol('m'))(sp.Symbol('delta'))(sp.Symbol('x'))(0)
            H_file = env['Hm'](sp.Integer(nn))(sp.Symbol('m'))(sp.Symbol('delta'))(sp.Symbol('x'))
            same = same and zero(U_code - U_file) and zero(H_code - H_file)
        check('6. information: Um and Hm at K = 1, y = 0 equal potentials.py\'s U_minus and H_minus, n = 2..11', same,
              f'potentials.py sha256 {digest[:16]}...')
    else:
        print('skip 6. information: no potentials.py given')

    # 7: controls (the specs' replacements, applied to the file's text)
    specs = json.load(open(os.path.join(os.path.dirname(path), 'mutations.json'), encoding='utf-8'))
    for spec in specs:
        if text.count(spec['old']) != 1:
            check(f"7. {spec['id']}: its old string occurs once", False)
            continue
        mutated = text.replace(spec['old'], spec['new'])
        target = spec['decl']
        try:
            if spec['id'] in WITNESS:
                false = witness_false(text, mutated, target, *WITNESS[spec['id']])
            elif spec['id'] == 'ZM17':
                near, _ = partner_near_zero(text, offset=1)
                false = near > mp.mpf(1) / 2
            else:
                false = not holds(mutated, target)
        except (SystemExit, Exception) as exc:  # a mutation that breaks the evaluation is reported, not hidden
            check(f"7. {spec['id']}: the mutated {target} is false", False, f'evaluation failed: {exc}')
            continue
        check(f"7. {spec['id']}: the mutated {target} is false", false, spec['note'])

    ok = all(results)
    print('ALL Z CHECKS HOLD' if ok else 'A CHECK FAILED', f'({sum(results)}/{len(results)})')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
