#!/usr/bin/env bash
# One-command re-run of A1's P1 certificate, l >= 3 (results/a1/PREREG.md, BHM-047).
#   kit/a1/run.sh [OUTDIR]
# Needs the environment of ENVIRONMENT.md (set BHM_PYTHON).  Runs the main certificate (must
# print VERIFIED), the negative controls NC-A1a-d and the tamper drills TD-A1a-c (each must
# REJECT), then compares the main JSON with the run of record if it exists.
set -uo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
py="${BHM_PYTHON:-python3}"
ref="${BHM_REF:-$root/results/a1/runs/record/main/result.json}"
out="${1:-$root/kit/a1/out-$(hostname)-$(date +%Y%m%dT%H%M%S)}"
"$py" -c "import flint, sympy, gmpy2; assert flint.__version__ == '0.9.0' and flint.__FLINT_VERSION__ == '3.6.0' and sympy.__version__ == '1.14.0' and gmpy2.version() == '2.3.2'" \
    || { echo "environment mismatch (flint 0.9.0 / FLINT 3.6.0, sympy 1.14.0, gmpy2 2.3.2): see ENVIRONMENT.md" >&2; exit 2; }
commit="${BHM_COMMIT:-$(git -C "$root" rev-parse --short HEAD 2>/dev/null || echo unknown)}"
ok=0
for c in none nc-ell2 nc-bump nc-coverage nc-uniform td-coeff td-split td-verifier; do
    d="$out/$c"; [ "$c" = none ] && d="$out/main"
    mkdir -p "$d"
    ( cd "$root/code" && BHM_COMMIT="$commit" PYTHONPATH="$root/code" nice -n 19 "$py" -m a1.p1 --out "$d" --control "$c" ) > "$d/run.log" 2>&1
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
