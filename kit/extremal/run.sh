#!/usr/bin/env bash
# Stage 3, item Z (results/extremal/PREREG.md): the extremal zero mode and its Darboux partner, with the controls.
#   kit/extremal/run.sh [OUTDIR]
# Every job must end as registered (PREREG section 4): an answer (no exception) for the claim and information jobs, and
# the exact registered verdict for every control.  At most BHM_JOBS (default 8) at a time.  With BHM_REF set to a
# directory of records, each result.json is also compared with the record of the same job.
set -uo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
py="${BHM_PYTHON:-python3}"
jobs="${BHM_JOBS:-8}"
out="${1:-$root/kit/extremal/out-$(hostname)-$(date +%Y%m%dT%H%M%S)}"
"$py" -c "import flint, sympy, gmpy2; assert flint.__version__ == '0.9.0' and flint.__FLINT_VERSION__ == '3.6.0' and sympy.__version__ == '1.14.0' and gmpy2.version() == '2.3.2'" \
    || { echo "environment mismatch (flint 0.9.0 / FLINT 3.6.0, sympy 1.14.0, gmpy2 2.3.2): see ENVIRONMENT.md" >&2; exit 2; }
commit="${BHM_COMMIT:-$(git -C "$root" rev-parse --short HEAD 2>/dev/null || echo unknown)}"
export BHM_ARCHIVE="${BHM_ARCHIVE:-unknown}"
mkdir -p "$out"
jobsfile="$out/jobs.txt"
: > "$jobsfile"
add() { local IFS='|'; echo "$*" >> "$jobsfile"; }
for n in 4 5 6 7 8 9 N 2 3; do add "$n" none answer; done
for n in 4 9; do
    add "$n" nc-nu "=REJECT: Z-inf, Z-id, P-reg, P-asym"
    add "$n" nc-exp "=REJECT: Z-thr, Z-id, P-reg, P-asym"
    add "$n" td-U "=REJECT: Z-inf, Z-thr, Z-id, P-reg, P-asym"
    add "$n" td-zid "=REJECT: Z-id, P-reg, P-asym"
    add "$n" td-preg "=REJECT: P-reg, P-asym"
done
runone() {
    local n c want
    IFS='|' read -r n c want <<< "$1"
    local d="$out/zero_mode-$n-$c"
    mkdir -p "$d"
    ( cd "$root/code" && BHM_COMMIT="$commit" PYTHONPATH="$root/code" timeout 21600 nice -n 19 "$py" -m extremal.zero_mode \
        --out "$d" --n "$n" --control "$c" ) > "$d/run.log" 2>&1
}
export -f runone
export out root py commit
xargs -P "$jobs" -d '\n' -n 1 bash -c 'runone "$0"' < "$jobsfile"
ok=0
while IFS='|' read -r n c want; do
    d="$out/zero_mode-$n-$c"
    v="$(tail -1 "$d/run.log" 2>/dev/null)"
    case "$want" in
        =*) [ "$v" = "${want#=}" ] || ok=1 ;;
        answer) case "$v" in "VERIFIED") ;; "REJECT: exception"*|"") ok=1 ;; "REJECT: "*) ;; *) ok=1 ;; esac ;;
        *) ok=1 ;;
    esac
    [ -f "$d/result.json" ] || ok=1
    if [ -n "${BHM_REF:-}" ]; then
        "$py" "$root/code/compare_runs.py" "$BHM_REF/$(basename "$d")/result.json" "$d/result.json" > "$d/compare.txt" 2>&1 || ok=1
    fi
    echo "n=$n $c: ${v:0:160}"
done < "$jobsfile"
if [ "$ok" -eq 0 ]; then echo "KIT PASS"; else echo "KIT FAIL"; fi
exit "$ok"
