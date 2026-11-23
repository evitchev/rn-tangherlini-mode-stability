"""Compare the Z item (d) build log's mutation verdicts with the registered predictions (first failure, exact set, judge pass)."""
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
 'ZD1': ('tortoise_q1', {'tortoise_q1'}),
 'ZD2': ('tortoise_q1', {'tortoise_q1'}),
 'ZD3': ('tort_hasDerivAt', {'tort_hasDerivAt', 'tort_strictMonoOn', 'tort_ge', 'tort_le', 'tortoise_q1', 'Rt_hasDerivAt'}),
 'ZD4': ('Rt_hasDerivAt', {'Rt_hasDerivAt', 'w_log_deriv', 'zero_mode', 'A_nonneg'}),
 'ZD5': ('riccati_plus', {'riccati_plus', 'V_eq'}),
 'ZD6': ('riccati_minus', {'riccati_minus', 'Vt_eq'}),
 'ZD7': ('V_eq', {'V_eq', 'zero_mode', 'A_nonneg'}),
 'ZD8': ('log_u0_hasDerivAt', {'log_u0_hasDerivAt', 'w_log_deriv'}),
 'ZD9': ('log_u0_hasDerivAt', {'log_u0_hasDerivAt'}),
 'ZD10': ('zero_mode', {'zero_mode'}),
 'ZD11': ('A_nonneg', {'A_nonneg'}),
 'ZD12': ('Vr_S5', {'Vr_S5', 'V_eq', 'Vr_continuousAt'}),
 'ZD13': ('tort_le', {'tort_le', 'tort_surjOn'}),
 'ZD14': ('one_sub_Yr_le', {'one_sub_Yr_le', 'fr_le_sq'}),
 'ZD15': ('wr_hasDerivAt', {'wr_hasDerivAt', 'riccati_plus', 'riccati_minus'}),
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
