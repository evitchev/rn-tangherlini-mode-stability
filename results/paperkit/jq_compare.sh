#!/usr/bin/env bash
# The second comparator of the paper kit's dry run (results/paperkit/PREREG.md §4, I3). It runs on host-0, with jq and
# no Python, after a run's outputs are copied back.
#   results/paperkit/jq_compare.sh EXPECTED_TSV ROOT OUTDIR
# For each row of expected.tsv, the registered record (ROOT/record) and the new record
# (OUTDIR/part/piece/job/result.json) each go through jq -S -c with a walk that deletes the same keys as canon.py:
# compare_runs.py's masks and archive_sha256, and, for p3's rows, a top-level design_rule equal to 1. The two outputs'
# SHA-256 are then compared. This comparator is independent of canon.py's code and of Python's json module.
# jq 1.6 reads numbers as doubles. That is safe here because the records hold their exact values as strings
# (the inventory of 2026-11-18).
set -uo pipefail
exp="${1:?expected.tsv}"; root="${2:?ROOT}"; out="${3:?OUTDIR}"
filter='(if $p3 and (type == "object") and (.design_rule == 1) then del(.design_rule) else . end)
  | walk(if type == "object" then del(.timing, .host, .platform, .git_commit, .t_backward_s, .t_total_s, .t_design_s,
         .t_verify_s, .archive_sha256) else . end)'
cm=0; cn=0; km=0; kn=0; bad=0
while IFS=$'\t' read -r part piece job cls p3 sha rec; do
    case "$part" in "#"*|"") continue ;; esac
    flag=false; [ "$p3" = p3 ] && flag=true
    new="$out/$part/$piece/$job/result.json"
    if [ ! -f "$new" ]; then echo "MISSING  $part $piece $job ($cls)"; [ "$cls" = cited ] && bad=1; continue; fi
    a=$(jq -S -c --argjson p3 "$flag" "$filter" "$root/$rec" | sha256sum | cut -c1-64)
    b=$(jq -S -c --argjson p3 "$flag" "$filter" "$new" | sha256sum | cut -c1-64)
    if [ "$cls" = cited ]; then cn=$((cn + 1)); else kn=$((kn + 1)); fi
    if [ "$a" = "$b" ]; then
        if [ "$cls" = cited ]; then cm=$((cm + 1)); else km=$((km + 1)); fi
    else
        echo "MISMATCH  $part $piece $job ($cls)"; [ "$cls" = cited ] && bad=1
    fi
done < "$exp"
echo "jq comparator: cited $cm/$cn MATCH; controls $km/$kn MATCH"
if [ "$bad" -eq 0 ]; then echo "jq compare: PASS"; else echo "jq compare: FAIL"; fi
exit "$bad"
