#!/usr/bin/env bash
# One-command re-run of HD-E, the elementary part of D = 7-11 (results/hd/elementary/PREREG.md, BHM-062).
#   kit/hd/run_elementary.sh [OUTDIR]
# Needs the environment of ENVIRONMENT.md (set BHM_PYTHON).  Runs the main certificate (must
# print VERIFIED), the negative controls NC-E1..E5 and the tamper drills TD-E1..E3 (each must
# REJECT), then compares the main JSON with the run of record if it exists.
set -uo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
py="${BHM_PYTHON:-python3}"
ref="${BHM_REF:-$root/results/hd/elementary/runs/record/main/result.json}"
out="${1:-$root/kit/hd/out-elementary-$(hostname)-$(date +%Y%m%dT%H%M%S)}"
"$py" -c "import flint, sympy; assert flint.__version__ == '0.9.0' and flint.__FLINT_VERSION__ == '3.6.0' and sympy.__version__ == '1.14.0'" \
    || { echo "environment mismatch: see ENVIRONMENT.md" >&2; exit 2; }
commit="${BHM_COMMIT:-$(git -C "$root" rev-parse --short HEAD 2>/dev/null || echo unknown)}"
ok=0
for c in none nc-onset-h nc-onset-i nc-zero nc-coverage nc-uniform td-coeff td-param td-verifier; do
    d="$out/$c"; [ "$c" = none ] && d="$out/main"
    mkdir -p "$d"
    ( cd "$root/code" && BHM_COMMIT="$commit" PYTHONPATH="$root/code" nice -n 19 "$py" -m hd.elementary --out "$d" --control "$c" --root "$root" ) > "$d/run.log" 2>&1
    s=$?
    v="$(tail -1 "$d/run.log")"
    case "$c" in
        none) { [ "$s" -eq 0 ] && [ "$v" = VERIFIED ]; } || ok=1 ;;
        *)    { [ "$s" -ne 0 ] && [[ "$v" == REJECT* ]]; } || ok=1 ;;
    esac
    echo "$c: exit $s, ${v:0:200}"
done
if [ -f "$ref" ]; then "$py" "$root/code/compare_runs.py" "$ref" "$out/main/result.json" || ok=1; fi
if [ "$ok" -eq 0 ]; then echo "KIT PASS"; else echo "KIT FAIL"; fi
exit "$ok"
