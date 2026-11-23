#!/usr/bin/env bash
# The paper kit's Lean part (kit/stability/README.md; registered in results/paperkit/PREREG.md, and for the public
# snapshot in results/pubkit/PREREG.md). It rebuilds each Lean development that the paper cites with that
# development's own build.sh (the offline build and audit: the source hash, compilation, the axiom audit, the negative
# controls and the mutation tests), from a fresh copy under OUTDIR. Then it compares the new BUILD_LOG.txt's verdict
# line with the archived one, and the whole log after masking its times (information).
#   kit/stability/run_lean.sh OUTDIR
# Each build.sh reads Lean 4.24.0 from $HOME/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean and Mathlib
# v4.24.0's oleans from the search path in $HOME/lean-setup/lean_path.txt, and runs python3 -B -I for its
# mutation tool. To use others, set BHM_LEAN_TOOLCHAIN (a Lean 4.24.0 toolchain directory) and BHM_LEAN_PATH_FILE (a
# file holding Mathlib's LEAN_PATH): each build then runs with a HOME under OUTDIR that holds both.
# Exit 0, ending "lean: KIT PASS", only if every build ends with its archived verdict line.
set -uo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
out="${1:-}"
[ -n "$out" ] || { sed -n 2,13p "$0"; exit 2; }
abs_out="$(realpath -m "$out")"
case "$abs_out/" in "$root/"*) echo "refused: OUTDIR $abs_out lies inside the kit's tree $root" >&2; exit 2 ;; esac
[ -e "$abs_out" ] && { echo "refused: OUTDIR $abs_out exists; give a new one" >&2; exit 2; }
lean_tc="${BHM_LEAN_TOOLCHAIN:-$HOME/.elan/toolchains/leanprover--lean4---v4.24.0}"
lean_path_file="${BHM_LEAN_PATH_FILE:-$HOME/lean-setup/lean_path.txt}"
lean_bin="$lean_tc/bin/lean"
[ -x "$lean_bin" ] || { echo "Lean 4.24.0 not found at $lean_bin" >&2; exit 2; }
[ -f "$lean_path_file" ] || { echo "Mathlib's LEAN_PATH file not found at $lean_path_file" >&2; exit 2; }
mkdir -p "$abs_out"
shim="$abs_out/.home"   # the HOME each build.sh sees: the toolchain and the LEAN_PATH file where build.sh looks
mkdir -p "$shim/.elan/toolchains" "$shim/lean-setup"
ln -s "$(realpath "$lean_tc")" "$shim/.elan/toolchains/leanprover--lean4---v4.24.0"
cp "$lean_path_file" "$shim/lean-setup/lean_path.txt"
echo "paper kit, Lean part: host $(hostname), $("$lean_bin" --version 2>&1 | head -1), start $(date -u +%FT%TZ)"
# The Lean developments the paper cites (paper/stability/AUDIT_TABLE.md): the n = 4 reduction and O2 (BHM-030), Lemma U
# at n = 4 (BHM-066), Proposition 3 on (0, 1) and at every n (BHM-090, BHM-091), G-RES (BHM-107), Z with the tortoise
# map at q = 1 (BHM-134, BHM-135), and the transcription of S5 (5.62b)-(5.63b) at n = 4 (BHM-030; Appendix A).
layers=(lean_onset_2026-10-22 lean_p3_sdeformation_2026-10-22 lean_lemmaU_2026-10-23 lean_p3_sdeformation_v2_2026-10-23
        lean_p3_sdeformation_v3_2026-10-23 lean_p3_sdeformation_v4_2026-10-24 lean_z_2026-10-26 lean_z_d_2026-10-26
        lean_a1_2026-10-22)
mask() { sed -E 's/(started|finished) [0-9]{8}T[0-9]{6}Z/\1 <time>/; s/logged [0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z/logged <time>/; s/seconds=[0-9]+/seconds=<n>/g' "$1"; }
verdict() { grep -E '^[A-Za-z0-9]+: (ALL CHECKS AS REQUIRED|A CHECK FAILED)' "$1" | tail -1; }
ok=0
for l in "${layers[@]}"; do
    cp -a "$root/lean/$l" "$abs_out/$l"
    ( cd "$abs_out/$l/lean" && HOME="$shim" nice -n 19 bash ./build.sh ) > "$abs_out/$l.build.out" 2>&1
    s=$?
    new="$abs_out/$l/lean/BUILD_LOG.txt"; old="$root/lean/$l/lean/BUILD_LOG.txt"
    vn="$( [ -f "$new" ] && verdict "$new" )"; vo="$(verdict "$old")"
    if [ -n "$vo" ] && [ "$vn" = "$vo" ]; then r="as archived"; else r="NOT as archived ($vo)"; ok=1; fi
    if [ -f "$new" ] && cmp -s <(mask "$old") <(mask "$new"); then m="identical after masking times"; else m="differs after masking times (information)"; fi
    echo "$l: build.sh exit $s; ${vn:-no verdict line} ($r); log $m"
done
echo "end $(date -u +%FT%TZ)"
if [ "$ok" -eq 0 ]; then echo "lean: KIT PASS"; else echo "lean: KIT FAIL"; fi
exit "$ok"
