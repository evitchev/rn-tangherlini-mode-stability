#!/usr/bin/env bash
# Re-runs under design rule 2 (results/p3/PREREG_ADDENDUM_1.md, BHM-024).
#   kit/p3/run_rule2.sh [OUTDIR]
# Must pass: G1 and T1 VERIFIED, TD-P2 REJECT (rule 2).  T2 (rule 2) is reported either way.
set -uo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
py="${BHM_PYTHON:-python3}"
out="${1:-$root/kit/p3/rule2-$(hostname)-$(date +%Y%m%dT%H%M%S)}"
commit="${BHM_COMMIT:-$(git -C "$root" rev-parse --short HEAD 2>/dev/null || echo unknown)}"
ok=0
for t in G1 T1 TD-P2 T2; do
    mkdir -p "$out/$t"
    ( cd "$root/code" && BHM_COMMIT="$commit" PYTHONPATH="$root/code" nice -n 19 "$py" -m p3.scert --out "$out/$t" --tier "$t" --design-rule 2 ) > "$out/$t/run.log" 2>&1
    s=$?
    v="$(tail -1 "$out/$t/run.log")"
    case "$t" in
        G1|T1) { [ "$s" -eq 0 ] && [ "$v" = VERIFIED ]; } || ok=1 ;;
        TD-P2) { [ "$s" -ne 0 ] && [[ "$v" == REJECT* ]]; } || ok=1 ;;
    esac
    echo "$t (rule 2): exit $s, ${v:0:200}"
done
if [ "$ok" -eq 0 ]; then echo "KIT PASS (rule 2 must-pass items)"; else echo "KIT FAIL"; fi
exit "$ok"
