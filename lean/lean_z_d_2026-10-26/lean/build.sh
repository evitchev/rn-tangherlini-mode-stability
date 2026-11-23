#!/usr/bin/env bash
# build.sh: offline build and audit of the bh-modes Z Lean layer, item (d) (BHM-126) (session-L, 2026-10-26).
# It follows the IBCertificates format and build rules (bh-modes RULES.md F) and exits 0 only if every check holds.
#  1. sources: BHModesZd.lean against SOURCES.tsv; a scan for sorry, admit, axiom, native_decide and the like.
#  2. compile: Lean 4.24.0 with the prebuilt Mathlib v4.24.0 oleans. Required: exit 0, 0 errors, 0 warnings, no sorry.
#  3. axioms: `#print axioms` for every theorem header. Only propext, Classical.choice and Quot.sound may occur, and the
#     count must equal the number of theorem headers in the source.
#  4. negative controls: two false proofs that must be rejected.
#  5. mutations: tools as vendored (vendor/mutation.py, a byte copy; vendor/VENDOR.sha256). Each mutated copy must fail
#     at the registered declaration, after the mutated line, not by a parse error or an unknown name, and with the
#     registered error text where one is given. The registration's sha256 is logged before the first mutation run.
#  6. writes BUILD_LOG.txt and a timestamped copy under logs/.
# Limits: one Lean process at a time, each under `ulimit -v 8000000` and `timeout`. Python with -B -I. Nothing is
# deleted: a previous build/ goes to .trash/.
set -u
cd "$(dirname "$0")"
LEAN_BIN=$HOME/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean
MATHLIB_LEAN_PATH=$(cat "$HOME/lean-setup/lean_path.txt")
MEM_KB=8000000; TMO=1800
REG=../review/ZD_MUTATION_REGISTRATION.md
TS=$(date -u +%Y%m%dT%H%M%SZ)
mkdir -p logs .trash
[ -d build ] && mv build ".trash/build_$TS"
mkdir -p build/olean build/mut build/neg
LOG=BUILD_LOG.txt; : > "$LOG"; fail=0
say() { printf '%s\n' "$*" >> "$LOG"; }
bad() { say "FAIL: $*"; fail=1; }
run_lean() {  # $1 = log; rest = lean args. Writes "exit seconds" to $1.rc
  local log=$1; shift
  ( ulimit -v "$MEM_KB"; export LEAN_PATH="$MATHLIB_LEAN_PATH:$PWD/build/olean"; s=$(date +%s)
    timeout "$TMO" "$LEAN_BIN" "$@" > "$log" 2>&1; echo "$? $(( $(date +%s) - s ))" > "$log.rc" )
}
say "bh-modes Z Lean layer, item (d) (BHM-126): build and audit, started $TS"
say "lean: $("$LEAN_BIN" --version 2>&1)"
case "$("$LEAN_BIN" --version 2>&1)" in *"version 4.24.0"*) ;; *) bad "toolchain is not Lean 4.24.0" ;; esac

say ""; say "== 1. sources"
want=$(awk -F'\t' '$1 == "BHModesZd.lean" {print $2}' SOURCES.tsv); have=$(sha256sum BHModesZd.lean | cut -c1-64)
[ -n "$want" ] && [ "$want" = "$have" ] && say "ok   BHModesZd.lean $have" || bad "BHModesZd.lean hash $have, SOURCES.tsv has '$want'"
say "scan for sorry / admit / axiom / native_decide / implemented_by / extern (informational):"
grep -nE '\bsorry\b|\badmit\b|^axiom |native_decide|implemented_by|@\[extern' BHModesZd.lean >> "$LOG" 2>&1 || say "  (no occurrence)"

say ""; say "== 2. compile"
run_lean build/compile.log -o build/olean/BHModesZd.olean -i build/olean/BHModesZd.ilean BHModesZd.lean
read -r rc secs < build/compile.log.rc
ne=$(grep -c ': error' build/compile.log); nw=$(grep -c ': warning' build/compile.log); ns=$(grep -c "declaration uses 'sorry'" build/compile.log)
say "BHModesZd: exit=$rc seconds=$secs errors=$ne warnings=$nw sorry=$ns"
[ "$rc" = 0 ] && [ "$ne" = 0 ] && [ "$nw" = 0 ] && [ "$ns" = 0 ] || bad "compile"

say ""; say "== 3. axioms"
names=$(grep -oE "^theorem [A-Za-z0-9_']+" BHModesZd.lean | awk '{print $2}')
{ echo "import BHModesZd"; for t in $names; do echo "#print axioms BHModes.Z.$t"; done; } > build/Axioms.lean
run_lean build/axioms.log build/Axioms.lean
read -r arc asecs < build/axioms.log.rc
nt=$(echo "$names" | grep -c .); np=$(grep -cE "depends on axioms|does not depend on any axioms" build/axioms.log)
nonstd=$(grep -oE "depends on axioms: \[[^]]*\]" build/axioms.log | sed 's/.*\[//; s/\]//' | tr ',' '\n' | sed 's/^ *//' | grep -vxE 'propext|Classical.choice|Quot.sound' | sort -u | paste -sd' ')
say "theorem headers: $nt; #print axioms entries: $np; exit=$arc; axioms outside {propext, Classical.choice, Quot.sound}: ${nonstd:-none}"
grep -E "depends on axioms|does not depend" build/axioms.log | sed 's/^/  /' >> "$LOG"
[ "$arc" = 0 ] && [ "$nt" = "$np" ] && [ -z "$nonstd" ] || bad "axiom audit"

say ""; say "== 4. checker negative controls (false proofs; each must be rejected)"
printf 'import Mathlib.Tactic.NormNum\ntheorem bogus : (2:ℝ) + 2 = 5 := by norm_num\n' > build/neg/NC1_two_plus_two.lean
printf 'import Mathlib.Tactic.Ring\ntheorem bogus (l : ℝ) : l * (l - 3) / 9 + 1 / 4 = (2 * l + 3) ^ 2 / 36 := by ring\n' > build/neg/NC2_false_margin.lean
for n in NC1_two_plus_two NC2_false_margin; do
  run_lean "build/neg/$n.out" "build/neg/$n.lean"; read -r nrc nsecs < "build/neg/$n.out.rc"
  nne=$(grep -c ': error' "build/neg/$n.out"); say "$n: exit=$nrc errors=$nne  ($(sed -n 2p build/neg/$n.lean))"
  [ "$nrc" != 0 ] && [ "$nne" -ge 1 ] || bad "negative control $n was accepted"
done

say ""; say "== 5. mutations (registration: $(basename "$REG") sha256 $(sha256sum "$REG" | cut -c1-64), logged $(date -u +%FT%TZ), before the first run)"
npass=0; nmut=0
for id in $(python3 -B -I -c 'import json; print(" ".join(s["id"] for s in json.load(open("mutations.json", encoding="utf-8"))))'); do
  nmut=$((nmut + 1)); mkdir -p "build/mut/$id"
  line=$(python3 -B -I vendor/mutation.py apply mutations.json "$id" . "build/mut/$id") || { bad "mutation $id could not be applied"; continue; }
  run_lean "build/mut/$id/lean.out" "build/mut/$id/BHModesZd.lean"; read -r mrc msecs < "build/mut/$id/lean.out.rc"
  python3 -B -I vendor/mutation.py judge mutations.json "$id" "build/mut/$id/BHModesZd.lean" "build/mut/$id/lean.out" "$mrc" "$line" > "build/mut/$id/verdict.json"
  v=$(cat "build/mut/$id/verdict.json"); say "$v"
  python3 -B -I -c 'import json,sys; sys.exit(0 if json.loads(sys.argv[1]).get("pass") else 1)' "$v" && npass=$((npass + 1)) || bad "mutation $id"
done
say "mutations failing as required: $npass / $nmut"

say ""
[ "$fail" = 0 ] && say "BHModesZd: ALL CHECKS AS REQUIRED" || say "BHModesZd: A CHECK FAILED"
say "finished $(date -u +%Y%m%dT%H%M%SZ)"
cp "$LOG" "logs/BUILD_LOG_$TS.txt"
cat "$LOG"
exit "$fail"
