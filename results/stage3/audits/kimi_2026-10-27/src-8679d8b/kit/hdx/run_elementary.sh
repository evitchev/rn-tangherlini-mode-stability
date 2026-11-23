#!/usr/bin/env bash
# HD-X-E (results/hdx/elementary/PREREG.md): U_- >= 0 for D = 7..11, l = n - 1..l0(n) and q in [q(mu_lo), 1], with its
# controls.
#   kit/hdx/run_elementary.sh [OUTDIR]
# Exit 0 only if the main run is VERIFIED and every control ends with its registered verdict.  With BHM_REF set to a
# directory of records, each result.json is also compared with the record of the same job (code/compare_runs.py).
set -uo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
py="${BHM_PYTHON:-python3}"
out="${1:-$root/kit/hdx/out-elementary-$(hostname)-$(date +%Y%m%dT%H%M%S)}"
"$py" -c "import flint, sympy, gmpy2; assert flint.__version__ == '0.9.0' and flint.__FLINT_VERSION__ == '3.6.0' and sympy.__version__ == '1.14.0' and gmpy2.version() == '2.3.2'" \
    || { echo "environment mismatch (flint 0.9.0 / FLINT 3.6.0, sympy 1.14.0, gmpy2 2.3.2): see ENVIRONMENT.md" >&2; exit 2; }
commit="${BHM_COMMIT:-$(git -C "$root" rev-parse --short HEAD 2>/dev/null || echo unknown)}"
export BHM_ARCHIVE="${BHM_ARCHIVE:-unknown}"
declare -A want=([none]="VERIFIED" [nc-band]="REJECT: E D=7 l=3, E D=11 l=7" [nc-strict]="REJECT: E D=7 l=4, E D=11 l=8"
                 [nc-bump]="REJECT: E D=7 l=5, E D=11 l=9" [td-coeff]="REJECT: E0n*" [td-verifier]="REJECT: KAT*"
                 [td-mulo]="REJECT: MEET*")
jobs=(none nc-band nc-strict nc-bump td-coeff td-verifier td-mulo)
for c in "${jobs[@]}"; do
    d="$out/$c"; mkdir -p "$d"
    ( cd "$root/code" && BHM_COMMIT="$commit" PYTHONPATH="$root/code" timeout 21600 nice -n 19 "$py" -m hdx.elementary --out "$d" --control "$c" --root "$root" ) > "$d/run.log" 2>&1 &
done
wait
ok=0
for c in "${jobs[@]}"; do
    d="$out/$c"
    v="$(tail -1 "$d/run.log")"
    w="${want[$c]}"
    if [[ "$w" == *"*" ]]; then [[ "$v" == ${w%\*}* ]] || ok=1; else [ "$v" = "$w" ] || ok=1; fi
    [ -f "$d/result.json" ] || ok=1
    if [ -n "${BHM_REF:-}" ]; then "$py" "$root/code/compare_runs.py" "$BHM_REF/$c/result.json" "$d/result.json" > "$d/compare.txt" 2>&1 || ok=1; fi
    echo "$c: ${v:0:200}"
done
if [ "$ok" -eq 0 ]; then echo "KIT PASS"; else echo "KIT FAIL"; fi
exit "$ok"
