#!/usr/bin/env bash
# A2-S addendum 1 (results/a2/s/PREREG_ADDENDUM_1.md): a control for each gate that had none, the reading's drills D0
# and D6, the inward decimals X0, and the main run's consistency X1 with BHM-101's sealed record.
#   kit/a2/run_s_check.sh [OUTDIR]
# Exit 0 only if every job ends with its registered verdict.  With BHM_REF set to a directory of records, each
# result.json is also compared with the record of the same job (code/compare_runs.py).
set -uo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
py="${BHM_PYTHON:-python3}"
out="${1:-$root/kit/a2/out-s-check-$(hostname)-$(date +%Y%m%dT%H%M%S)}"
"$py" -c "import flint, sympy, gmpy2; assert flint.__version__ == '0.9.0' and flint.__FLINT_VERSION__ == '3.6.0' and sympy.__version__ == '1.14.0' and gmpy2.version() == '2.3.2'" \
    || { echo "environment mismatch (flint 0.9.0 / FLINT 3.6.0, sympy 1.14.0, gmpy2 2.3.2): see ENVIRONMENT.md" >&2; exit 2; }
commit="${BHM_COMMIT:-$(git -C "$root" rev-parse --short HEAD 2>/dev/null || echo unknown)}"
export BHM_ARCHIVE="${BHM_ARCHIVE:-unknown}"
ctls="none td-H td-param td-design td-gres td-L td-S td-divT td-divC d0 d6"
for c in $ctls; do
    d="$out/$c"; mkdir -p "$d"
    ( cd "$root/code" && BHM_COMMIT="$commit" PYTHONPATH="$root/code" timeout 43200 nice -n 19 "$py" -m a2.scert --out "$d" --control "$c" --root "$root" ) > "$d/run.log" 2>&1 &
done
wait
d="$out/scheck"; mkdir -p "$d"
( cd "$root/code" && BHM_COMMIT="$commit" PYTHONPATH="$root/code" timeout 3600 nice -n 19 "$py" -m a2.scheck --out "$d" --main "$out/none/result.json" --root "$root" ) > "$d/run.log" 2>&1
only_pos() {   # every reason after the first n is a POS chart
    local v="$1" skip="$2" r i=0
    IFS=',' read -ra rs <<< "${v#REJECT: }"
    for r in "${rs[@]}"; do r="${r# }"; i=$((i + 1)); [ "$i" -le "$skip" ] && continue
        case "$r" in POS-O|"POS-O'"|POS-T|POS-C) ;; *) return 1 ;; esac; done
    return 0
}
ok=0
for c in $ctls scheck; do
    d="$out/$c"
    v="$(tail -1 "$d/run.log")"
    case "$c" in
        none|scheck) [ "$v" = "VERIFIED" ] || ok=1 ;;
        td-H) [ "$v" = "REJECT: H" ] || ok=1 ;;
        td-param) [ "$v" = "REJECT: PARAM" ] || ok=1 ;;
        td-design) [ "$v" = "REJECT: DESIGN" ] || ok=1 ;;
        td-gres) [ "$v" = "REJECT: G-RES" ] || ok=1 ;;
        td-L) [ "$v" = "REJECT: L" ] || ok=1 ;;
        td-S) { [[ "$v" == "REJECT: S"* ]] && only_pos "$v" 1; } || ok=1 ;;
        td-divT) [ "$v" = "REJECT: DIV-T, POS-T" ] || ok=1 ;;
        td-divC) [ "$v" = "REJECT: DIV-C, POS-C" ] || ok=1 ;;
        d0) { [ "$v" = "REJECT: POS-C" ] && grep -q "^POS-C: FAIL  at (0, 0); POS-C: sign\*p = 0 <= 0" "$d/run.log"; } || ok=1 ;;
        d6) { [[ "$v" == "REJECT: "*POS-T* ]] && only_pos "$v" 0 \
              && grep -Eq "^POS-T: FAIL  at \([^,]+, [^0][^)]*\);" "$d/run.log"; } || ok=1 ;;
    esac
    [ -f "$d/result.json" ] || ok=1
    if [ -n "${BHM_REF:-}" ]; then "$py" "$root/code/compare_runs.py" "$BHM_REF/$c/result.json" "$d/result.json" > "$d/compare.txt" 2>&1 || ok=1; fi
    echo "$c: ${v:0:200}"
done
if [ "$ok" -eq 0 ]; then echo "KIT PASS"; else echo "KIT FAIL"; fi
exit "$ok"
