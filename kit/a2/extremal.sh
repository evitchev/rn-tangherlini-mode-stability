#!/usr/bin/env bash
# One-command re-run of A2's exact extremal checks E0-E5 (TARGET_A2.md section 3, BHM-009).
#   kit/a2/extremal.sh [OUTDIR]
# Needs the environment of ENVIRONMENT.md (python-flint 0.9.0 / FLINT 3.6.0, sympy 1.14.0);
# set BHM_PYTHON to that interpreter.  Runs the main check (must print VERIFIED) and the three
# registered controls (each must REJECT), then compares the main JSON with the run of record
# (masking timings and host).  Exit 0 only if all of that holds.
set -uo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
py="${BHM_PYTHON:-python3}"
ref="${BHM_REF:-$root/results/a2/extremal/runs/record/main/result.json}"
out="${1:-$root/kit/a2/out-$(hostname)-$(date +%Y%m%dT%H%M%S)}"
"$py" -c "import flint, sympy, gmpy2; assert flint.__version__ == '0.9.0' and flint.__FLINT_VERSION__ == '3.6.0' and sympy.__version__ == '1.14.0' and gmpy2.version() == '2.3.2'" \
    || { echo "environment mismatch (flint 0.9.0 / FLINT 3.6.0, sympy 1.14.0, gmpy2 2.3.2): see ENVIRONMENT.md" >&2; exit 2; }
commit="${BHM_COMMIT:-$(git -C "$root" rev-parse --short HEAD 2>/dev/null || echo unknown)}"
ok=0
for c in none wrong-branch false-claim tamper-U; do
    d="$out/$c"; [ "$c" = none ] && d="$out/main"
    mkdir -p "$d"
    ( cd "$root/code" && BHM_COMMIT="$commit" PYTHONPATH="$root/code" nice -n 19 "$py" -m a2.extremal --out "$d" --control "$c" ) > "$d/run.log" 2>&1
    s=$?
    v="$(tail -1 "$d/run.log")"
    if [ "$c" = none ]; then
        { [ "$s" -eq 0 ] && [ "$v" = VERIFIED ]; } || ok=1
    else
        { [ "$s" -ne 0 ] && [[ "$v" == REJECT* ]]; } || ok=1
    fi
    echo "$c: exit $s, $v"
done
if [ -f "$ref" ]; then "$py" "$root/code/compare_runs.py" "$ref" "$out/main/result.json" || ok=1; fi
if [ "$ok" -eq 0 ]; then echo "KIT PASS"; else echo "KIT FAIL"; fi
exit "$ok"
