#!/usr/bin/env bash
# One-command re-run of HD-S, the S-certificates on the 18 bands of D = 7-11 (results/hd/s/PREREG.md).
#   kit/hd/run_s.sh [OUTDIR]
# Needs the environment of ENVIRONMENT.md (set BHM_PYTHON).  Runs the 18 bands (each must print VERIFIED) and the
# controls and drills (each must print exactly its registered REJECT), at most BHM_JOBS (default 8) at a time, each
# under a 12-hour cap; then compares every band's JSON with the run of record if it exists.
set -uo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
py="${BHM_PYTHON:-python3}"
jobs="${BHM_JOBS:-8}"
refdir="${BHM_REF:-$root/results/hd/s/runs/record}"
out="${1:-$root/kit/hd/out-s-$(hostname)-$(date +%Y%m%dT%H%M%S)}"
"$py" -c "import flint, sympy; assert flint.__version__ == '0.9.0' and flint.__FLINT_VERSION__ == '3.6.0' and sympy.__version__ == '1.14.0'" \
    || { echo "environment mismatch: see ENVIRONMENT.md" >&2; exit 2; }
commit="${BHM_COMMIT:-$(git -C "$root" rev-parse --short HEAD 2>/dev/null || echo unknown)}"
mkdir -p "$out"
jobsfile="$out/jobs.txt"
: > "$jobsfile"
for b in 7,2 7,3 8,2 8,3 8,4 9,2 9,3 9,4 9,5 10,2 10,3 10,4 10,5 11,2 11,3 11,4 11,5 11,6; do echo "$b none" >> "$jobsfile"; done
for D in 7 8 9 10 11; do for c in td-coeff td-horizon nc-bound; do echo "$D,2 $c" >> "$jobsfile"; done; done
echo "7,2 td-verifier" >> "$jobsfile"
runone() {
    local b="$1" c="$2" d="$out/${1/,/-}"
    [ "$c" = none ] || d="$d-$c"
    mkdir -p "$d"
    ( cd "$root/code" && BHM_COMMIT="$commit" PYTHONPATH="$root/code" timeout 43200 nice -n 19 "$py" -m hd.scert --out "$d" --band "$b" --control "$c" --root "$root" ) > "$d/run.log" 2>&1
}
export -f runone
export out root py commit
xargs -P "$jobs" -L 1 bash -c 'runone "$0" "$1"' < "$jobsfile"
ok=0
while read -r b c; do
    d="$out/${b/,/-}"; [ "$c" = none ] || d="$d-$c"
    case "$c" in
        none) want="VERIFIED" ;;
        td-coeff) want="REJECT: E0n" ;;
        td-verifier) want="REJECT: KAT" ;;
        td-horizon) want="REJECT: td-horizon" ;;
        nc-bound) want="REJECT: nc-bound (b)" ;;
    esac
    v="$(tail -1 "$d/run.log")"
    [ "$v" = "$want" ] || ok=1
    echo "D=${b%,*} l=${b#*,} $c: ${v:0:160}"
    if [ "$c" = none ] && [ -f "$refdir/${b/,/-}/result.json" ]; then
        "$py" "$root/code/compare_runs.py" "$refdir/${b/,/-}/result.json" "$d/result.json" > "$d/compare.txt" || { ok=1; echo "  differs from the record: see $d/compare.txt"; }
    fi
done < "$jobsfile"
if [ "$ok" -eq 0 ]; then echo "KIT PASS"; else echo "KIT FAIL"; fi
exit "$ok"
