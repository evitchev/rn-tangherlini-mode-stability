"""check_p3v2.py: checks of the bh-modes p3 Lean layer v2 outside Lean (session-L, 2026-10-23).

Run with an interpreter that has sympy, from this folder:
    python3 -I -B check_p3v2.py ../lean/BHModesP3.lean
It reads only the Lean file named on the command line. It exits 0 only if every check holds.

 1. Lines 1-392 of the v2 file are the first build's, by the sha256 of that prefix, and the new section follows.
 2. prop3_Ioo's binders are prop3's, in the same order, except hP and hP'; the two conclusions are identical.
 3. prop3_near's binders are prop3_Ioo's, except the added (a b), ha, hb and the changed hP, hP'; same conclusion.
 4. prop3_zeta's binders are prop3_Ioo's, except those that name P, P' or the zeta data; same conclusion.
 5. The file's own Pzeta' (parsed) is d/dz of the file's own Pzeta (parsed), for d = 0, ..., 12, with P-hat an
    undefined function (sympy).
 6. The same for a symbolic nonnegative integer d.
 7. Negative control: mutation P3M12's variant, (d + 1) P-hat in place of d P-hat, is not the derivative for any
    d = 0, ..., 12.
 8. The pole: 1/(z + delta) tends to +infinity as z -> -delta from above (sympy limit).
"""

import hashlib
import re
import sys

import sympy as sp

PREFIX_LINES = 392
PREFIX_SHA256 = '70d14327b29fd5f2713bad70646b4301c321f62f05023a34fb169e80c288e94b'  # first build, 9cbce71a...

results = []


def check(name, ok, detail=''):
    results.append(bool(ok))
    print(f"{'ok  ' if ok else 'FAIL'} {name}{': ' + detail if detail else ''}")


def header(text, name):
    """The text of `theorem name` from its binders to the := that starts its proof."""
    m = re.search(r'^theorem ' + re.escape(name) + r' ', text, re.M)
    start = m.end()
    depth = 0
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
    """(ordered list of (names, type) for the top-level binder groups, conclusion), whitespace collapsed."""
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
    out = []
    for g in groups:
        names, typ = g.split(':', 1)
        out.append((norm(names), norm(typ)))
    return out, norm(head[rest_at + 1:])


def main(path):
    raw = open(path, 'rb').read()
    text = raw.decode('utf-8')
    lines = raw.split(b'\n')

    # 1
    prefix = b'\n'.join(lines[:PREFIX_LINES]) + b'\n'
    h = hashlib.sha256(prefix).hexdigest()
    check('1. lines 1-392 are the first build\'s', h == PREFIX_SHA256, f'prefix sha256 {h[:16]}...')
    check('1. the new section starts at line 393',
          lines[PREFIX_LINES].decode('utf-8').startswith('/-! ### v2 (2026-10-23)'))
    check('1. the file ends with the namespace', text.endswith('end BHModes.P3\n'), f'{len(lines) - 1} lines')

    # 2
    b3, c3 = binders(header(text, 'prop3'))
    bI, cI = binders(header(text, 'prop3_Ioo'))
    names3, namesI = [n for n, _ in b3], [n for n, _ in bI]
    changed = [n for (n, t), (m, u) in zip(b3, bI) if t != u]
    check('2. prop3_Ioo has prop3\'s binders, in order', names3 == namesI, ' '.join(namesI))
    check('2. only hP and hP\' differ', changed == ['hP', "hP'"],
          '; '.join(f'{n} : {dict(b3)[n]}  ->  {dict(bI)[n]}' for n in changed))
    check('2. identical conclusions', c3 == cI, cI)

    # 3
    bN, cN = binders(header(text, 'prop3_near'))
    namesN = [n for n, _ in bN]
    extra = [n for n in namesN if n not in namesI]
    common = [n for n in namesN if n in namesI]
    changedN = [n for n in common if dict(bN)[n] != dict(bI)[n]]
    check('3. prop3_near adds exactly (a b), ha, hb', extra == ['a b', 'ha', 'hb'] and common == namesI,
          ', '.join(f'{n} : {dict(bN)[n]}' for n in extra))
    check('3. only hP and hP\' differ from prop3_Ioo', changedN == ['hP', "hP'"],
          '; '.join(f'{n} : {dict(bN)[n]}' for n in changedN))
    check('3. identical conclusions', cN == cI)

    # 4
    bZ, cZ = binders(header(text, 'prop3_zeta'))
    dZ, dI = dict(bZ), dict(bI)
    same = [n for n in namesI if n in dZ and dZ[n] == dI[n]]
    diffZ = [n for n, _ in bZ if n not in same]
    diffI = [n for n in namesI if n not in same]
    check('4. prop3_zeta keeps every binder of prop3_Ioo that does not name P, P\' or zeta data',
          diffI == ["U H F F' P P' R", 'hP', "hP'", 'hN']
          and diffZ == ["U H F F' Ph Ph' R", 'δ', 'd', 'hδ', 'hPh', "hPh'", 'hN'],
          f'prop3_Ioo only: {diffI}; prop3_zeta only: {diffZ}')
    check('4. its hN is prop3_Ioo\'s with P, P\' := Pzeta, Pzeta\'',
          dZ['hN'] == dI['hN'].replace("Nz U H F F' P P' z", "Nz U H F F' (Pzeta Ph δ d) (Pzeta' Ph Ph' δ d) z"),
          dZ['hN'])
    check('4. identical conclusions', cZ == cI)

    # 5-7: the file's own Pzeta and Pzeta'
    def body(name):
        m = re.search(r'^noncomputable def ' + re.escape(name) + r' [^\n]*?:=\s*(.*?)\n\n', text, re.M | re.S)
        return ' '.join(m.group(1).split())

    def to_sympy(s):
        s = s.replace("Ph' z", 'Php(z)').replace('Ph z', 'Ph(z)').replace('δ', 'delta').replace('^', '**')
        return s

    z, delta = sp.symbols('z delta')
    Ph, Php = sp.Function('Ph'), sp.Function('Php')
    loc = {'z': z, 'delta': delta, 'Ph': Ph, 'Php': Php}
    sP, sD = body('Pzeta'), body("Pzeta'")
    print(f'     parsed Pzeta  := {sP}')
    print(f"     parsed Pzeta' := {sD}")

    def deriv_matches(dval, dexpr_src):
        loc_d = dict(loc, d=dval)
        P = sp.sympify(to_sympy(sP), locals=loc_d)
        D = sp.sympify(to_sympy(dexpr_src), locals=loc_d)
        dP = sp.diff(P, z).subs(sp.Derivative(Ph(z), z), Php(z))
        return sp.simplify(dP - D) == 0

    ok5 = all(deriv_matches(k, sD) for k in range(13))
    check("5. Pzeta' is d/dz Pzeta for d = 0..12", ok5)
    dsym = sp.Symbol('d', integer=True, nonnegative=True)
    P = sp.sympify(to_sympy(sP), locals=dict(loc, d=dsym))
    D = sp.sympify(to_sympy(sD), locals=dict(loc, d=dsym))
    dP = sp.diff(P, z).subs(sp.Derivative(Ph(z), z), Php(z))
    diff = sp.simplify(sp.powsimp(sp.expand((dP - D) * (z + delta) ** (dsym + 1)), force=True))
    check("6. the same for symbolic d", diff == 0, f'(dP - Pzeta\') (z + delta)^(d+1) = {diff}')
    bad = sD.replace('- d * Ph z', '- (d + 1) * Ph z')
    check('7. control: the P3M12 variant is not the derivative, for every d = 0..12',
          bad != sD and not any(deriv_matches(k, bad) for k in range(13)), bad)

    # 8
    lim = sp.limit(1 / (z + delta), z, -delta, '+')
    check('8. 1/(z + delta) -> +oo as z -> -delta from above', lim == sp.oo, str(lim))

    ok = all(results)
    print('ALL P3 V2 CHECKS HOLD' if ok else 'A CHECK FAILED', f'({sum(results)}/{len(results)})')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
