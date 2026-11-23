#!/usr/bin/env bash
# A2-PILOT (results/a2/pilot/PREREG.md): the untrusted design pilot for D = 6, l = 2 near extremality.
#   kit/a2/run_pilot.sh [OUTDIR]
# Exit 0 only if the pilot is VALID (its gates and controls as registered).  With BHM_REF set to the record's
# result.json, the run is also compared with it (code/compare_runs.py).
set -uo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
py="${BHM_PYTHON:-python3}"
out="${1:-$root/kit/a2/out-pilot-$(hostname)-$(date +%Y%m%dT%H%M%S)}"
"$py" -c "import flint, sympy, gmpy2; assert flint.__version__ == '0.9.0' and flint.__FLINT_VERSION__ == '3.6.0' and sympy.__version__ == '1.14.0' and gmpy2.version() == '2.3.2'" \
    || { echo "environment mismatch (flint 0.9.0 / FLINT 3.6.0, sympy 1.14.0, gmpy2 2.3.2): see ENVIRONMENT.md" >&2; exit 2; }
commit="${BHM_COMMIT:-$(git -C "$root" rev-parse --short HEAD 2>/dev/null || echo unknown)}"
export BHM_ARCHIVE="${BHM_ARCHIVE:-unknown}"
mkdir -p "$out/main"
( cd "$root/code" && BHM_COMMIT="$commit" PYTHONPATH="$root/code" timeout 21600 nice -n 19 "$py" -m a2.pilot --out "$out/main" --root "$root" ) > "$out/main/run.log" 2>&1
s=$?
v="$(tail -1 "$out/main/run.log")"
ok=0
{ [ "$s" -eq 0 ] && [[ "$v" == VALID* ]]; } || ok=1
if [ -n "${BHM_REF:-}" ]; then "$py" "$root/code/compare_runs.py" "$BHM_REF" "$out/main/result.json" || ok=1; fi
echo "pilot: exit $s, $v"
if [ "$ok" -eq 0 ]; then echo "KIT PASS"; else echo "KIT FAIL"; fi
exit "$ok"
