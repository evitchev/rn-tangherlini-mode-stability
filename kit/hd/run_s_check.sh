#!/usr/bin/env bash
# HD-S PREREG addendum 1 (results/hd/s/PREREG_ADDENDUM_1.md): X1, the controls on the three zeta-bands, and X2, the
# identity check of every sealed certificate, with its drill TD-X2.
#   kit/hd/run_s_check.sh [OUTDIR]
# Each job must end with exactly its registered verdict; at most BHM_JOBS (default 8) at a time.
set -uo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
py="${BHM_PYTHON:-python3}"
jobs="${BHM_JOBS:-8}"
out="${1:-$root/kit/hd/out-s-check-$(hostname)-$(date +%Y%m%dT%H%M%S)}"
"$py" -c "import flint, sympy, gmpy2; assert flint.__version__ == '0.9.0' and flint.__FLINT_VERSION__ == '3.6.0' and sympy.__version__ == '1.14.0' and gmpy2.version() == '2.3.2'" \
    || { echo "environment mismatch (flint 0.9.0 / FLINT 3.6.0, sympy 1.14.0, gmpy2 2.3.2): see ENVIRONMENT.md" >&2; exit 2; }
commit="${BHM_COMMIT:-$(git -C "$root" rev-parse --short HEAD 2>/dev/null || echo unknown)}"
mkdir -p "$out"
jobsfile="$out/jobs.txt"
: > "$jobsfile"
for b in 7,2 7,3 8,2 8,3 8,4 9,2 9,3 9,4 9,5 10,2 10,3 10,4 10,5 11,2 11,3 11,4 11,5 11,6; do echo "scheck $b none" >> "$jobsfile"; done
echo "scheck 7,2 td-direct" >> "$jobsfile"
echo "scheck 11,6 td-direct" >> "$jobsfile"
for b in 9,5 10,5 11,6; do echo "scert $b td-horizon" >> "$jobsfile"; echo "scert $b nc-bound" >> "$jobsfile"; done
runone() {
    local mod="$1" b="$2" c="$3" d="$out/$1-${2/,/-}-$3"
    mkdir -p "$d"
    ( cd "$root/code" && BHM_COMMIT="$commit" PYTHONPATH="$root/code" timeout 43200 nice -n 19 "$py" -m "hd.$mod" --out "$d" --band "$b" --control "$c" --root "$root" ) > "$d/run.log" 2>&1
}
export -f runone
export out root py commit
xargs -P "$jobs" -L 1 bash -c 'runone "$0" "$1" "$2"' < "$jobsfile"
ok=0
while read -r mod b c; do
    d="$out/$mod-${b/,/-}-$c"
    case "$mod $c" in
        "scheck none") want="VERIFIED" ;;
        "scheck td-direct") want="REJECT: X2" ;;
        "scert td-horizon") want="REJECT: td-horizon" ;;
        "scert nc-bound") want="REJECT: nc-bound (b)" ;;
    esac
    v="$(tail -1 "$d/run.log")"
    [ "$v" = "$want" ] || ok=1
    echo "$mod D=${b%,*} l=${b#*,} $c: ${v:0:160}"
done < "$jobsfile"
if [ "$ok" -eq 0 ]; then echo "KIT PASS"; else echo "KIT FAIL"; fi
exit "$ok"
