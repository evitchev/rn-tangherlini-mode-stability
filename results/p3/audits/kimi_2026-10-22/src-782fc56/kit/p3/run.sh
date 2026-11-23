#!/usr/bin/env bash
# One-command re-run of the l = 2 prototype certificate (results/p3/PREREG.md, BHM-022).
#   kit/p3/run.sh [OUTDIR]
# Needs the environment of ENVIRONMENT.md (set BHM_PYTHON).  Must pass: T1 and G1 VERIFIED;
# NC-P1 VERIFIED (= bound state certified and the T1 certificate rejected on V + W); TD-P1 and
# TD-P2 REJECT.  T2 and T3 are run and reported either way.  Exit 0 only if the must-pass items hold.
set -uo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
py="${BHM_PYTHON:-python3}"
out="${1:-$root/kit/p3/out-$(hostname)-$(date +%Y%m%dT%H%M%S)}"
"$py" -c "import flint, sympy; assert flint.__version__ == '0.9.0' and sympy.__version__ == '1.14.0'" \
    || { echo "environment mismatch: see ENVIRONMENT.md" >&2; exit 2; }
commit="${BHM_COMMIT:-$(git -C "$root" rev-parse --short HEAD 2>/dev/null || echo unknown)}"
ok=0
for t in T1 G1 NC-P1 TD-P1 TD-P2 T2 T3; do
    mkdir -p "$out/$t"
    ( cd "$root/code" && BHM_COMMIT="$commit" PYTHONPATH="$root/code" nice -n 19 "$py" -m p3.scert --out "$out/$t" --tier "$t" ) > "$out/$t/run.log" 2>&1
    s=$?
    v="$(tail -1 "$out/$t/run.log")"
    case "$t" in
        T1|G1|NC-P1) { [ "$s" -eq 0 ] && [ "$v" = VERIFIED ]; } || ok=1 ;;
        TD-P1|TD-P2) { [ "$s" -ne 0 ] && [[ "$v" == REJECT* ]]; } || ok=1 ;;
    esac
    echo "$t: exit $s, ${v:0:200}"
done
if [ "$ok" -eq 0 ]; then echo "KIT PASS (must-pass items; T2, T3 as reported above)"; else echo "KIT FAIL"; fi
exit "$ok"
