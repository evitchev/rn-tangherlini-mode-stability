#!/usr/bin/env bash
# HD-X-2 (results/hdx/critical/PREREG.md): the critical bands of D = 7..11 through extremality, by route (iii), with
# their controls.
#   kit/hdx/run_critical.sh [OUTDIR]
# Nine band jobs (control none), and every control on D = 7 l = 2 and D = 11 l = 4.  Exit 0 only if every band job is
# VERIFIED and every control ends in its registered form (code/hdx/kitcheck.py: =exact, ^prefix, +required|allowed).
# With BHM_REF set to a directory of records, each result.json is also compared with the record of the same job
# (code/compare_runs.py).  BHM_JOBS (default 8) jobs run at a time.
set -uo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
py="${BHM_PYTHON:-python3}"
out="${1:-$root/kit/hdx/out-critical-$(hostname)-$(date +%Y%m%dT%H%M%S)}"
nice -n 19 "$py" -c "import flint, sympy, gmpy2; assert flint.__version__ == '0.9.0' and flint.__FLINT_VERSION__ == '3.6.0' and sympy.__version__ == '1.14.0' and gmpy2.version() == '2.3.2'" \
    || { echo "environment mismatch (flint 0.9.0 / FLINT 3.6.0, sympy 1.14.0, gmpy2 2.3.2): see ENVIRONMENT.md" >&2; exit 2; }
commit="${BHM_COMMIT:-$(git -C "$root" rev-parse --short HEAD 2>/dev/null || echo unknown)}"
export BHM_ARCHIVE="${BHM_ARCHIVE:-unknown}"
par="${BHM_JOBS:-8}"
declare -A want=(
    [none]="=VERIFIED"
    [nc-ehat-low]="+POS-C|POS-O,POS-O',POS-T"
    [d0-corner]="+POS-C|POS-O,POS-O',POS-T"
    [nc-ehat-high]="+POS-T|POS-O,POS-O',POS-C"
    [d0-throat]="+POS-T|POS-O,POS-O',POS-C"
    [nc-Q0]="+INF,POS-O|POS-O',POS-T,POS-C"
    [nc-Qneg]="+INF,POS-O|POS-O',POS-T,POS-C"
    [td-nu]="+Z0,DIV-O,DIV-C,CORNER,FIRST,INF,POS-O,POS-O',POS-C|POS-T"
    [d6]="+POS-T|POS-O,POS-O',POS-C"
    [nc-bound]="=REJECT: nc-bound (b)"
    [td-coeff]="+E0n,Z0,DIV-O,DIV-C,THROAT,CORNER,FIRST,INF,POS-O,POS-O',POS-C|POS-T"
    [td-verifier]="=REJECT: KAT"
    [td-cover]="=REJECT: COVER"
    [td-div]="+DIV-T,DIV-C,THROAT,CORNER,FIRST,POS-T,POS-C|POS-O,POS-O'"
)
bands=(7,2 8,2 9,2 9,3 10,2 10,3 11,2 11,3 11,4)
controls=(nc-ehat-low d0-corner nc-ehat-high d0-throat nc-Q0 nc-Qneg td-nu d6 nc-bound td-coeff td-verifier td-cover td-div)
jobs_list=()
for b in "${bands[@]}"; do jobs_list+=("$b/none"); done
for b in 7,2 11,4; do for c in "${controls[@]}"; do jobs_list+=("$b/$c"); done; done
for j in "${jobs_list[@]}"; do
    b="${j%%/*}"; c="${j#*/}"
    d="$out/D${b/,/l}/$c"; mkdir -p "$d"
    while [ "$(jobs -rp | wc -l)" -ge "$par" ]; do wait -n; done
    ( cd "$root/code" && BHM_COMMIT="$commit" PYTHONPATH="$root/code" timeout 21600 nice -n 19 "$py" -m hdx.critical --out "$d" --band "$b" --control "$c" --root "$root" ) > "$d/run.log" 2>&1 &
done
wait
ok=0
for j in "${jobs_list[@]}"; do
    b="${j%%/*}"; c="${j#*/}"
    d="$out/D${b/,/l}/$c"
    v="$(tail -1 "$d/run.log")"
    if [ -f "$d/result.json" ]; then
        ( cd "$root/code" && PYTHONPATH="$root/code" nice -n 19 "$py" -m hdx.kitcheck "${want[$c]}" "$d/result.json" ) > "$d/kitcheck.txt" 2>&1 || ok=1
    else
        ok=1
    fi
    if [ -n "${BHM_REF:-}" ]; then nice -n 19 "$py" "$root/code/compare_runs.py" "$BHM_REF/D${b/,/l}/$c/result.json" "$d/result.json" > "$d/compare.txt" 2>&1 || ok=1; fi
    echo "D${b/,/l} $c: ${v:0:200}"
done
if [ "$ok" -eq 0 ]; then echo "KIT PASS"; else echo "KIT FAIL"; fi
exit "$ok"
