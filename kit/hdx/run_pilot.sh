#!/usr/bin/env bash
# HD-X-PILOT: the untrusted design pilot of HD-X-1 on every band of hdx.bands, and its gate against A2-PILOT.
#   kit/hdx/run_pilot.sh [OUTDIR]
# Two jobs: main (hdx.pilot, every band) and gate-a2 (hdx.pilot --gate-a2 --legacy-f, the gate band (4, 2) in this
# engine).  Exit 0 only if main is VALID with every band qualifying (no K3), gate-a2 is VALID, and gate-a2's record
# equals A2-PILOT's record of record (hdx.gate --kind pilot).  With BHM_REF set to a directory of records (main/,
# gate-a2/), each result.json is also compared with the record of the same job (code/compare_runs.py).
set -uo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
py="${BHM_PYTHON:-python3}"
out="${1:-$root/kit/hdx/out-pilot-$(hostname)-$(date +%Y%m%dT%H%M%S)}"
"$py" -c "import flint, sympy, gmpy2; assert flint.__version__ == '0.9.0' and flint.__FLINT_VERSION__ == '3.6.0' and sympy.__version__ == '1.14.0' and gmpy2.version() == '2.3.2'" \
    || { echo "environment mismatch (flint 0.9.0 / FLINT 3.6.0, sympy 1.14.0, gmpy2 2.3.2): see ENVIRONMENT.md" >&2; exit 2; }
commit="${BHM_COMMIT:-$(git -C "$root" rev-parse --short HEAD 2>/dev/null || echo unknown)}"
export BHM_ARCHIVE="${BHM_ARCHIVE:-unknown}"
mkdir -p "$out/main" "$out/gate-a2"
( cd "$root/code" && BHM_COMMIT="$commit" PYTHONPATH="$root/code" timeout 43200 nice -n 19 "$py" -m hdx.pilot --out "$out/main" --root "$root" ) > "$out/main/run.log" 2>&1 &
( cd "$root/code" && BHM_COMMIT="$commit" PYTHONPATH="$root/code" timeout 21600 nice -n 19 "$py" -m hdx.pilot --out "$out/gate-a2" --gate-a2 --legacy-f --root "$root" ) > "$out/gate-a2/run.log" 2>&1 &
wait
ok=0
v="$(tail -1 "$out/main/run.log")"
{ [[ "$v" == VALID* ]] && [[ "$v" != *K3* ]]; } || ok=1
g="$(tail -1 "$out/gate-a2/run.log")"
[[ "$g" == VALID* ]] || ok=1
( cd "$root/code" && PYTHONPATH="$root/code" nice -n 19 "$py" -m hdx.gate --kind pilot --new "$out/gate-a2/result.json" \
      --ref "$root/results/a2/pilot/runs/record/main/result.json" ) > "$out/gate-a2/gate.txt" 2>&1 || ok=1
if [ -n "${BHM_REF:-}" ]; then
    for j in main gate-a2; do "$py" "$root/code/compare_runs.py" "$BHM_REF/$j/result.json" "$out/$j/result.json" > "$out/$j/compare.txt" 2>&1 || ok=1; done
fi
echo "main: ${v:0:300}"
echo "gate-a2: ${g:0:200}; against A2-PILOT's record: $(tail -1 "$out/gate-a2/gate.txt")"
if [ "$ok" -eq 0 ]; then echo "KIT PASS"; else echo "KIT FAIL"; fi
exit "$ok"
