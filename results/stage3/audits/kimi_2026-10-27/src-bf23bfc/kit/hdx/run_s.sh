#!/usr/bin/env bash
# HD-X-S: HD-X-1's singular S-certificates on the bands of hdx.bands, with every control and tamper of hdx.scert.
#   kit/hdx/run_s.sh [OUTDIR]                 every band (or BHM_BANDS="7,3 11,7"): none and each control
#   kit/hdx/run_s.sh --gate [OUTDIR]          the gate band 6,2 (none) against A2-S's record of record (hdx.gate)
# At most BHM_JOBS (default 8) jobs at a time, each under a 12-hour cap.  Exit 0 only if every job ends with its
# registered verdict (hdx.verdicts).  With BHM_REF set to a directory of records, each job's result.json is also
# compared with the record of the same job (code/compare_runs.py).
set -uo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
py="${BHM_PYTHON:-python3}"
jobs="${BHM_JOBS:-8}"
gate=0
if [ "${1:-}" = "--gate" ]; then gate=1; shift; fi
out="${1:-$root/kit/hdx/out-s-$(hostname)-$(date +%Y%m%dT%H%M%S)}"
"$py" -c "import flint, sympy, gmpy2; assert flint.__version__ == '0.9.0' and flint.__FLINT_VERSION__ == '3.6.0' and sympy.__version__ == '1.14.0' and gmpy2.version() == '2.3.2'" \
    || { echo "environment mismatch (flint 0.9.0 / FLINT 3.6.0, sympy 1.14.0, gmpy2 2.3.2): see ENVIRONMENT.md" >&2; exit 2; }
commit="${BHM_COMMIT:-$(git -C "$root" rev-parse --short HEAD 2>/dev/null || echo unknown)}"
export BHM_ARCHIVE="${BHM_ARCHIVE:-unknown}"
mkdir -p "$out"
jobsfile="$out/jobs.txt"
: > "$jobsfile"
if [ "$gate" -eq 1 ]; then
    echo "6,2 none" >> "$jobsfile"
else
    ctls="none nc-a2 nc-res nc-well d0 d6 td-coeff td-verifier td-chart td-cover td-H td-param td-design td-gres td-L td-S td-divT td-divC"
    for b in ${BHM_BANDS:-7,3 8,3 8,4 9,4 9,5 10,4 10,5 10,6 11,5 11,6 11,7}; do for c in $ctls; do echo "$b $c" >> "$jobsfile"; done; done
fi
runone() {
    local b="$1" c="$2" d="$out/${1/,/-}-$2"
    mkdir -p "$d"
    ( cd "$root/code" && BHM_COMMIT="$commit" PYTHONPATH="$root/code" timeout 43200 nice -n 19 "$py" -m hdx.scert --out "$d" --band "$b" --control "$c" --root "$root" ) > "$d/run.log" 2>&1
}
export -f runone
export out root py commit
xargs -P "$jobs" -L 1 bash -c 'runone "$0" "$1"' < "$jobsfile"
ok=0
while read -r b c; do
    d="$out/${b/,/-}-$c"
    ( cd "$root/code" && PYTHONPATH="$root/code" "$py" -m hdx.verdicts --control "$c" --record "$d/result.json" ) > "$d/verdict.txt" 2>&1 || ok=1
    echo "D=${b%,*} l=${b#*,} $(cat "$d/verdict.txt")"
    if [ "$gate" -eq 1 ]; then
        ( cd "$root/code" && PYTHONPATH="$root/code" "$py" -m hdx.gate --kind s --new "$d/result.json" \
              --ref "$root/results/a2/s/runs/record/none/result.json" ) > "$d/gate.txt" 2>&1 || ok=1
        echo "  against A2-S's record: $(tail -1 "$d/gate.txt")"
    fi
    if [ -n "${BHM_REF:-}" ]; then
        "$py" "$root/code/compare_runs.py" "$BHM_REF/${b/,/-}-$c/result.json" "$d/result.json" > "$d/compare.txt" 2>&1 || { ok=1; echo "  differs from the record: see $d/compare.txt"; }
    fi
done < "$jobsfile"
if [ "$ok" -eq 0 ]; then echo "KIT PASS"; else echo "KIT FAIL"; fi
exit "$ok"
