"""Compare the Z build log's mutation verdicts with the registered predictions (first failure, exact set, judge pass)."""
import json, re, sys
lean, log = sys.argv[1], sys.argv[2]
lines = open(lean, encoding='utf-8').read().split('\n')
DECL = re.compile(r'^\s*(?:@\[[^\]]*\]\s*)?(?:(?:private|protected|noncomputable|nonrec|partial|unsafe)\s+)*'
                  r'(?:theorem|lemma|def|abbrev|instance|example|structure|inductive)\b\s*([^\s:(\[{]*)')
def enclosing(n):
    for i in range(min(n, len(lines)) - 1, -1, -1):
        m = DECL.match(lines[i])
        if m:
            return m.group(1).split('.')[-1]
reg = {
 'ZM1': ('z_id', {'z_id', 'partner', 'partner_ends'}),
 'ZM2': ('g_hasDerivAt', {'g_hasDerivAt', 'z_id', 'partner'}),
 'ZM3': ('z_id', {'z_id'}),
 'ZM4': ('gate_q1', {'gate_q1', 'gate_H', 'z_id'}),
 'ZM5': ('gate_q1', {'gate_q1', 'gate_H', 'z_id'}),
 'ZM6': ('z_id', {'z_id'}),
 'ZM7': ('z_id', {'z_id'}),
 'ZM8': ('partner', {'partner', 'partner_no_pole'}),
 'ZM9': ('partner', {'partner', 'partner_n4', 'partner_ends'}),
 'ZM10': ('gate_H', {'gate_H', 'z_id'}),
 'ZM11': ('gate_q1', {'gate_q1'}),
 'ZM12': ('partner', {'partner', 'partner_no_pole'}),
 'ZM13': ('g_hasDerivAt', {'g_hasDerivAt', 'deriv_g'}),
 'ZM14': ('z_id', {'z_id'}),
 'ZM15': ('z_id', {'z_id'}),
 'ZM16': ('z_id', {'z_id'}),
 'ZM17': ('partner_no_pole', {'partner_no_pole'}),
}
seen, allok = set(), True
for raw in open(log, encoding='utf-8'):
    if not raw.startswith('{"id"'):
        continue
    v = json.loads(raw)
    i = v['id']; seen.add(i)
    first = enclosing(v['first_error'][0]) if v['first_error'] else None
    fd, fs = reg[i]
    ok = (first == fd) and (set(v['failing_decls']) == fs) and v['pass']
    allok &= ok
    print(f"{i:6} {'AGREES' if ok else 'DIFFERS'}  first {first} (reg {fd}); set {sorted(v['failing_decls'])}"
          f"{'' if set(v['failing_decls']) == fs else ' (reg ' + str(sorted(fs)) + ')'}; errors {v['errors']}; "
          f"first_error {v['first_error']}; pass {v['pass']}"
          + (f"; error_text_found {v['error_text_found']}" if 'error_text_found' in v else ''))
print('all registered ids seen' if seen == set(reg) else f'MISSING {sorted(set(reg) - seen)}')
print('ALL AGREE' if allok and seen == set(reg) else 'NOT ALL AGREE')
