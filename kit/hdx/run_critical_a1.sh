#!/usr/bin/env bash
# HD-X-2, PREREG addendum 1 (results/hdx/critical/PREREG_ADDENDUM_1.md): BHM-143's 35 jobs, plus the six new controls
# (td-param, td-H, td-R, td-L, td-S, td-XN) on D = 7 l = 2 and D = 11 l = 4: 47 jobs.  The sealed kit/hdx/run_critical.sh
# is unchanged.
#   kit/hdx/run_critical_a1.sh [OUTDIR]
# KIT PASS only if
#   (a) each of the 35 original jobs is IDENTICAL after masking to BHM-144's record of the same job (by default
#       $root/results/hdx/critical/runs/record, or BHM_A1_BASE), apart from archive_sha256, which differs by
#       construction (this run is from another archive); output is never written inside that record;
#   (b) each of the 47 jobs ends in its registered form (code/hdx/kitcheck.py), the 12 new ones included;
#   (c) with BHM_REF set to a directory of records, each of the 47 jobs is also IDENTICAL after masking to that record.
# BHM_JOBS (default 8) jobs run at a time.
set -uo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
py="${BHM_PYTHON:-python3}"
out="${1:-$root/kit/hdx/out-critical-a1-$(hostname)-$(date +%Y%m%dT%H%M%S)}"
base="${BHM_A1_BASE:-$root/results/hdx/critical/runs/record}"
abs_out="$(realpath -m "$out")"; abs_base="$(realpath -m "$base")"
case "$abs_out/" in "$abs_base"/*) echo "refused: the output $abs_out lies inside BHM-144's record $abs_base" >&2; exit 2;; esac
[ -d "$base" ] || { echo "BHM-144's record not found: $base" >&2; exit 2; }
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
    [td-param]="=REJECT: PARAM"
    [td-H]="=REJECT: H"
    [td-R]="=REJECT: R"
    [td-L]="=REJECT: L"
    [td-S]="+PARAM,S,THROAT,FIRST,XN|POS-O,POS-O',POS-T,POS-C"
    [td-XN]="=REJECT: XN"
)
bands=(7,2 8,2 9,2 9,3 10,2 10,3 11,2 11,3 11,4)
original=(nc-ehat-low d0-corner nc-ehat-high d0-throat nc-Q0 nc-Qneg td-nu d6 nc-bound td-coeff td-verifier td-cover td-div)
added=(td-param td-H td-R td-L td-S td-XN)
jobs_list=()
for b in "${bands[@]}"; do jobs_list+=("$b/none"); done
for b in 7,2 11,4; do for c in "${original[@]}" "${added[@]}"; do jobs_list+=("$b/$c"); done; done
is_original() { local x; [ "$1" = none ] && return 0; for x in "${original[@]}"; do [ "$x" = "$1" ] && return 0; done; return 1; }
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
    note=""
    if [ -f "$d/result.json" ]; then
        ( cd "$root/code" && PYTHONPATH="$root/code" nice -n 19 "$py" -m hdx.kitcheck "${want[$c]}" "$d/result.json" ) > "$d/kitcheck.txt" 2>&1 || { ok=1; note="$note form"; }
    else
        ok=1; note="$note no-record"
    fi
    if is_original "$c"; then                                            # (a): against BHM-144's record
        nice -n 19 "$py" "$root/code/compare_runs.py" "$base/D${b/,/l}/$c/result.json" "$d/result.json" > "$d/compare-bhm144.txt" 2>&1
        other="$(grep '^DIFF' "$d/compare-bhm144.txt" | grep -v -c '^DIFF /archive_sha256: ')"
        last="$(tail -1 "$d/compare-bhm144.txt")"
        if [ "$last" = "IDENTICAL after masking" ] || { [ "$other" -eq 0 ] && [ "$last" = "1 difference(s)" ]; }; then
            echo "(a) IDENTICAL to BHM-144 after masking, apart from archive_sha256" >> "$d/compare-bhm144.txt"
        else
            ok=1; note="$note (a)"
        fi
    fi
    if [ -n "${BHM_REF:-}" ]; then                                       # (c)
        nice -n 19 "$py" "$root/code/compare_runs.py" "$BHM_REF/D${b/,/l}/$c/result.json" "$d/result.json" > "$d/compare.txt" 2>&1 || { ok=1; note="$note (c)"; }
    fi
    echo "D${b/,/l} $c: ${v:0:200}${note:+  FAILED:$note}"
done
if [ "$ok" -eq 0 ]; then echo "KIT PASS"; else echo "KIT FAIL"; fi
exit "$ok"
