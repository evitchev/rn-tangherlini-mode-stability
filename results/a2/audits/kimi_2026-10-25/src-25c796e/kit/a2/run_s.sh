#!/usr/bin/env bash
# A2-S (results/a2/s/PREREG.md): the singular S-certificate for D = 6, l = 2, q in [q(1/8), 1], with its controls.
#   kit/a2/run_s.sh [OUTDIR]
# Exit 0 only if the main run is VERIFIED and every control ends with its registered verdict (PREREG section 4).
# With BHM_REF set to a directory of records, each result.json is also compared with the record of the same job.
set -uo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
py="${BHM_PYTHON:-python3}"
out="${1:-$root/kit/a2/out-s-$(hostname)-$(date +%Y%m%dT%H%M%S)}"
"$py" -c "import flint, sympy; assert flint.__version__ == '0.9.0' and flint.__FLINT_VERSION__ == '3.6.0' and sympy.__version__ == '1.14.0'" \
    || { echo "environment mismatch: see ENVIRONMENT.md" >&2; exit 2; }
commit="${BHM_COMMIT:-$(git -C "$root" rev-parse --short HEAD 2>/dev/null || echo unknown)}"
export BHM_ARCHIVE="${BHM_ARCHIVE:-unknown}"
ctls="none nc-a2 nc-zm nc-res nc-bound td-coeff td-verifier td-chart td-cover"
for c in $ctls; do
    d="$out/$c"; mkdir -p "$d"
    ( cd "$root/code" && BHM_COMMIT="$commit" PYTHONPATH="$root/code" timeout 43200 nice -n 19 "$py" -m a2.scert --out "$d" --control "$c" --root "$root" ) > "$d/run.log" 2>&1 &
done
wait
pos_only() {   # REJECT: <reasons>, every reason one of the four POS charts
    local v="$1" r
    [[ "$v" == "REJECT: "* ]] || return 1
    IFS=',' read -ra rs <<< "${v#REJECT: }"
    for r in "${rs[@]}"; do r="${r# }"; case "$r" in POS-O|"POS-O'"|POS-T|POS-C) ;; *) return 1 ;; esac; done
    return 0
}
ok=0
for c in $ctls; do
    d="$out/$c"
    v="$(tail -1 "$d/run.log")"
    case "$c" in
        none) [ "$v" = "VERIFIED" ] || ok=1 ;;
        nc-a2|nc-zm|nc-res) pos_only "$v" || ok=1 ;;
        nc-bound) [ "$v" = "REJECT: nc-bound (b)" ] || ok=1 ;;
        td-coeff) [[ "$v" == "REJECT: "*E0* ]] || ok=1 ;;
        td-verifier) [ "$v" = "REJECT: KAT" ] || ok=1 ;;
        td-chart) [ "$v" = "REJECT: POS-T" ] || ok=1 ;;
        td-cover) [ "$v" = "REJECT: COVER" ] || ok=1 ;;
    esac
    [ -f "$d/result.json" ] || ok=1
    if [ -n "${BHM_REF:-}" ]; then "$py" "$root/code/compare_runs.py" "$BHM_REF/$c/result.json" "$d/result.json" > "$d/compare.txt" 2>&1 || ok=1; fi
    echo "$c: ${v:0:200}"
done
if [ "$ok" -eq 0 ]; then echo "KIT PASS"; else echo "KIT FAIL"; fi
exit "$ok"
