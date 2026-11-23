#!/usr/bin/env bash
# The paper kit for the stability theorem (paper/stability, Theorem 1; the operator's ruling BHM-182, item 4;
# registered in results/paperkit/PREREG.md). It re-runs, from this archive, every certificate the theorem cites, with
# each certificate's registered controls and drills. It then compares every new record with its registered record in
# the canonical form of kit/stability/canon.py, against the hashes in kit/stability/expected.tsv.
#   kit/stability/run.sh PART OUTDIR       PART: selftest, A1, A2, HD, HDX, Z, or all (selftest first, then the five)
# Needs the environment of ENVIRONMENT.md: set BHM_PYTHON to the venv's python. Optional: BHM_JOBS (default 8), and
# BHM_COMMIT and BHM_ARCHIVE (the commit and the archive's SHA-256, written into the records' provenance).
# Exit 0, ending "<PART>: KIT PASS", only if every sub-kit ends with KIT PASS, every p3 tier ends with its record's
# verdict line, and canon.py finds every cited job's new record equal to its registered record. OUTDIR must not exist
# yet, and must lie outside the kit's own tree.
set -uo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
part="${1:-}"; out="${2:-}"
case "$part" in selftest|A1|A2|HD|HDX|Z|all) ;; *) sed -n 2,12p "$0"; exit 2 ;; esac
[ -n "$out" ] || { sed -n 2,12p "$0"; exit 2; }
abs_out="$(realpath -m "$out")"
case "$abs_out/" in
    "$root/"*) echo "refused: OUTDIR $abs_out lies inside the kit's tree $root" >&2; exit 2 ;;
esac
[ -e "$abs_out" ] && { echo "refused: OUTDIR $abs_out exists; give a new one" >&2; exit 2; }
py="${BHM_PYTHON:-python3}"
"$py" -c "import flint, sympy, gmpy2, mpmath; assert flint.__version__ == '0.9.0' and flint.__FLINT_VERSION__ == '3.6.0' and sympy.__version__ == '1.14.0' and gmpy2.version() == '2.3.2' and mpmath.__version__ == '1.3.0'" \
    || { echo "environment mismatch (python-flint 0.9.0 / FLINT 3.6.0, sympy 1.14.0, gmpy2 2.3.2, mpmath 1.3.0): see ENVIRONMENT.md" >&2; exit 2; }
commit="${BHM_COMMIT:-$(git -C "$root" rev-parse --short HEAD 2>/dev/null || echo unknown)}"
export BHM_PYTHON="$py" BHM_JOBS="${BHM_JOBS:-8}" BHM_COMMIT="$commit" BHM_ARCHIVE="${BHM_ARCHIVE:-unknown}"
unset BHM_REF BHM_A1_BASE BHM_BANDS
exp="$root/kit/stability/expected.tsv"
canon="$root/kit/stability/canon.py"
mkdir -p "$abs_out"
echo "paper kit: part $part, commit $commit, archive ${BHM_ARCHIVE:0:16}, host $(hostname), python $("$py" -c 'import sys; print(sys.version.split()[0])'), start $(date -u +%FT%TZ)"

subkit() {  # PART PIECE KIT [ARGS...]: run one sub-kit into OUTDIR/PART/PIECE; its log beside it
    local p="$1" pc="$2" k="$3"; shift 3
    local d="$abs_out/$p/$pc"
    mkdir -p "$abs_out/$p"
    echo "== $p $pc: $k $*"
    bash "$root/$k" "$@" "$d" > "$d.kit.log" 2>&1
    local s=$? last
    last="$(tail -1 "$d.kit.log")"
    echo "   exit $s, $last"
    [ "$s" -eq 0 ] && [ "$last" = "KIT PASS" ]
}

p3tiers() {  # A1's p3 piece: the seven tiers of p3 under design rule 1, each against its record's verdict line
    local d="$abs_out/A1/p3" ok=0 t s v w
    mkdir -p "$d"
    echo "== A1 p3: the seven tiers of p3.scert (design rule 1), each against its record's verdict line"
    for t in T1 G1 NC-P1 TD-P1 TD-P2 T2 T3; do
        mkdir -p "$d/$t"
        ( cd "$root/code" && BHM_COMMIT="$commit" PYTHONPATH="$root/code" nice -n 19 "$py" -m p3.scert --out "$d/$t" --tier "$t" ) > "$d/$t/run.log" 2>&1
        s=$?
        v="$(tail -1 "$d/$t/run.log")"
        w="$(tail -1 "$root/results/p3/runs/record/$t/run.log")"
        if [ "$v" = "$w" ] && { if [ "$w" = VERIFIED ]; then [ "$s" -eq 0 ]; else [ "$s" -ne 0 ]; fi; }; then
            echo "   $t: exit $s, ${v:0:120} (as its record)"
        else
            ok=1; echo "   $t: exit $s, ${v:0:120} (NOT as its record: ${w:0:120})"
        fi
    done
    if [ "$ok" -eq 0 ]; then echo "   KIT PASS"; else echo "   KIT FAIL"; fi
    return "$ok"
}

run_part() {  # PART
    local p="$1" r=0
    echo "=== part $p, start $(date -u +%FT%TZ)"
    case "$p" in
        A1)  subkit A1 onset kit/onset/run.sh || r=1
             p3tiers || r=1
             subkit A1 a1 kit/a1/run.sh || r=1 ;;
        A2)  subkit A2 a2-elementary kit/a2/run_elementary.sh || r=1
             subkit A2 a2-s kit/a2/run_s.sh || r=1
             subkit A2 a2-s-check kit/a2/run_s_check.sh || r=1 ;;
        HD)  subkit HD hd-elementary kit/hd/run_elementary.sh || r=1
             subkit HD hd-s kit/hd/run_s.sh || r=1
             subkit HD hd-s-check kit/hd/run_s_check.sh || r=1 ;;
        HDX) subkit HDX hdx-elementary kit/hdx/run_elementary.sh || r=1
             subkit HDX hdx-s kit/hdx/run_s.sh || r=1
             subkit HDX hdx-s-gate kit/hdx/run_s.sh --gate || r=1
             subkit HDX hdx-critical kit/hdx/run_critical.sh || r=1
             subkit HDX hdx-critical-a1 kit/hdx/run_critical_a1.sh || r=1 ;;
        Z)   subkit Z extremal kit/extremal/run.sh || r=1 ;;
    esac
    ( cd "$root/code" && PYTHONPATH="$root/code" nice -n 19 "$py" "$canon" compare "$exp" "$root" "$abs_out" "$p" ) > "$abs_out/$p.canon.txt" 2>&1 || r=1
    tail -2 "$abs_out/$p.canon.txt" | sed 's/^/   /'
    echo "=== part $p, end $(date -u +%FT%TZ)"
    if [ "$r" -eq 0 ]; then echo "$p: KIT PASS"; else echo "$p: KIT FAIL"; fi
    return "$r"
}

rc=0
if [ "$part" = selftest ] || [ "$part" = all ]; then
    echo "=== selftest (the kit's own controls KC1-KC6), start $(date -u +%FT%TZ)"
    ( cd "$root/code" && PYTHONPATH="$root/code" nice -n 19 "$py" "$canon" selftest "$exp" "$root" "$abs_out/selftest" ) > "$abs_out/selftest.txt" 2>&1 || rc=1
    sed 's/^/   /' "$abs_out/selftest.txt"
    if [ "$rc" -eq 0 ]; then echo "selftest: KIT PASS"; else echo "selftest: KIT FAIL"; fi
fi
if [ "$part" = all ]; then
    for p in A1 A2 HD HDX Z; do run_part "$p" || rc=1; done
    echo "end $(date -u +%FT%TZ)"
    if [ "$rc" -eq 0 ]; then echo "all: KIT PASS"; else echo "all: KIT FAIL"; fi
elif [ "$part" != selftest ]; then
    run_part "$part" || rc=1
fi
exit "$rc"
