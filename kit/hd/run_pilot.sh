#!/usr/bin/env bash
# One-command re-run of HD-PILOT, the untrusted design pilot of D = 7-11 (results/hd/pilot/PREREG.md).
#   kit/hd/run_pilot.sh [OUTDIR]
# Needs the environment of ENVIRONMENT.md (set BHM_PYTHON).  Runs the pilot with its gates and controls (must print
# VALID), then compares the JSON with the run of record if it exists.
set -uo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
py="${BHM_PYTHON:-python3}"
ref="${BHM_REF:-$root/results/hd/pilot/runs/record/main/result.json}"
out="${1:-$root/kit/hd/out-pilot-$(hostname)-$(date +%Y%m%dT%H%M%S)}"
"$py" -c "import flint, sympy, gmpy2; assert flint.__version__ == '0.9.0' and flint.__FLINT_VERSION__ == '3.6.0' and sympy.__version__ == '1.14.0' and gmpy2.version() == '2.3.2'" \
    || { echo "environment mismatch (flint 0.9.0 / FLINT 3.6.0, sympy 1.14.0, gmpy2 2.3.2): see ENVIRONMENT.md" >&2; exit 2; }
commit="${BHM_COMMIT:-$(git -C "$root" rev-parse --short HEAD 2>/dev/null || echo unknown)}"
ok=0
d="$out/main"
mkdir -p "$d"
( cd "$root/code" && BHM_COMMIT="$commit" PYTHONPATH="$root/code" nice -n 19 "$py" -m hd.pilot --out "$d" --root "$root" ) > "$d/run.log" 2>&1
s=$?
v="$(tail -1 "$d/run.log")"
{ [ "$s" -eq 0 ] && [ "$v" = VALID ]; } || ok=1
echo "pilot: exit $s, ${v:0:200}"
grep '^q_max' "$d/run.log"
if [ -f "$ref" ]; then "$py" "$root/code/compare_runs.py" "$ref" "$d/result.json" || ok=1; fi
if [ "$ok" -eq 0 ]; then echo "KIT PASS"; else echo "KIT FAIL"; fi
exit "$ok"
