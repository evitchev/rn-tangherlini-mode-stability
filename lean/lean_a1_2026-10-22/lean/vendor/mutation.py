"""Mutation tests for build.sh.

  mutation.py apply SPECS ID SRCDIR OUTDIR
      Write OUTDIR/<file> with the one replacement of spec ID applied (the old string
      must occur exactly once).  Prints the 1-based line of the replacement.
      Multi-site specs (S1a phase 2b) carry "sites": [{"old", "new"}, ...] instead of
      "old"/"new": every old string must occur exactly once in the unmutated file, the
      sites must not overlap, and all replacements are applied; the printed line is the
      first site's (the earliest in the file).
  mutation.py judge SPECS ID MUTATED_FILE LEAN_OUTPUT RC MUT_LINE [UPSTREAM_RC]
      Decide whether the mutated copy failed for the intended reason.  Prints one JSON
      line and exits 0 only if: the Lean exit code is non-zero; at least one error was
      reported; no error is a parse error or an unknown identifier/constant (a broken
      mutation, not a failed proof); no error sits before the mutated line; and the
      expected declaration is among the declarations carrying an error.
      Downstream specs (a "downstream" field, S1a): the mutation is applied to "file", which
      must still compile (UPSTREAM_RC = 0), and the unmodified downstream file, compiled
      against it, is judged: MUTATED_FILE is then the downstream file, MUT_LINE is 0, and the
      expected declaration must also be the first failing one in file order.
      Specs with an "error_text" field {decl: text} (S1c phase C2, the lead's condition on
      S20) also require, for each decl, an error inside that decl whose message's first line
      is exactly the text.
"""

import json
import re
import sys

DECL = re.compile(
    r'^\s*(?:@\[[^\]]*\]\s*)?(?:(?:private|protected|noncomputable|nonrec|partial|unsafe)\s+)*'
    r'(?:theorem|lemma|def|abbrev|instance|example|structure|inductive)\b\s*([^\s:(\[{]*)')
ERR = re.compile(r'^(?P<file>[^\s:][^:]*\.lean):(?P<line>\d+):(?P<col>\d+): error(?:\([^)]*\))?:\s?(?P<msg>.*)$')
BROKEN = ('unexpected', 'unknown identifier', 'unknown constant', 'unterminated')


def load(specs, ident):
    for spec in json.load(open(specs, encoding='utf-8')):
        if spec['id'] == ident:
            return spec
    raise SystemExit(f'no spec {ident}')


def apply(specs, ident, srcdir, outdir):
    spec = load(specs, ident)
    text = open(f'{srcdir}/{spec["file"]}', encoding='utf-8').read()
    sites = spec['sites'] if 'sites' in spec else [{'old': spec['old'], 'new': spec['new']}]
    spans = []
    for site in sites:
        if text.count(site['old']) != 1:
            raise SystemExit(f'{ident}: old string occurs {text.count(site["old"])} times')
        pos = text.index(site['old'])
        spans.append((pos, pos + len(site['old']), site['new']))
    spans.sort()
    if any(a[1] > b[0] for a, b in zip(spans, spans[1:])):
        raise SystemExit(f'{ident}: overlapping sites')
    out = text
    for start, end, new in reversed(spans):
        out = out[:start] + new + out[end:]
    open(f'{outdir}/{spec["file"]}', 'w', encoding='utf-8').write(out)
    print(text[:spans[0][0]].count('\n') + 1)


def enclosing(lines, lineno):
    for i in range(min(lineno, len(lines)) - 1, -1, -1):
        m = DECL.match(lines[i])
        if m:
            return m.group(1).split('.')[-1] or '(anonymous)'
    return '(top)'


def judge(specs, ident, mutated, output, rc, mut_line, upstream_rc=0):
    spec = load(specs, ident)
    downstream = 'downstream' in spec
    lines = open(mutated, encoding='utf-8').read().split('\n')
    errors = []
    for raw in open(output, encoding='utf-8', errors='replace'):
        m = ERR.match(raw.rstrip('\n'))
        if m:
            ln = int(m.group('line'))
            errors.append((ln, m.group('msg').strip(), enclosing(lines, ln)))
    failing = sorted({e[2] for e in errors})
    broken = [e for e in errors if e[1].lower().startswith(BROKEN[0]) or any(b in e[1].lower() for b in BROKEN[1:])]
    early = [e for e in errors if e[0] < mut_line]
    ok = (rc != 0 and bool(errors) and not broken and not early and spec['decl'] in failing)
    first_decl = min(errors)[2] if errors else None
    if downstream:
        ok = ok and upstream_rc == 0 and first_decl == spec['decl']
    want = spec.get('error_text', {})
    text_ok = all(any(e[2] == d and e[1] == t for e in errors) for d, t in want.items())
    ok = ok and text_ok
    print(json.dumps({'id': ident, 'file': spec['file'], **({'downstream': spec['downstream'],
                      'upstream_exit': upstream_rc, 'first_failing_decl': first_decl} if downstream else {}),
                      **({'error_text': want, 'error_text_found': text_ok} if want else {}),
                      'expected_decl': spec['decl'], 'exit': rc,
                      'errors': len(errors), 'failing_decls': failing,
                      'first_error': errors[0][:2] if errors else None,
                      'broken_mutation': bool(broken), 'error_before_mutation': bool(early),
                      'mutation_line': mut_line, 'pass': ok}, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'apply':
        apply(*sys.argv[2:6])
    elif cmd == 'judge':
        a = sys.argv[2:]
        sys.exit(judge(a[0], a[1], a[2], a[3], int(a[4]), int(a[5]), int(a[6]) if len(a) > 6 else 0))
    else:
        raise SystemExit(__doc__)
