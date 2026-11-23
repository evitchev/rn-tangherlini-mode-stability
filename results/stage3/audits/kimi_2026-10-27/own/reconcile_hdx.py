"""Reconciliation of my HD-X kit reproductions against the records (log kept)."""
import json, os
def strip(d):
    if isinstance(d, dict): return {k: strip(v) for k,v in d.items() if k not in ('timing','provenance','t_design_s','t_verify_s','utc_start','archive_sha256','t_total_s')}
    if isinstance(d, list): return [strip(x) for x in d]
    return d
pairs = [
  ("hdxe", "[repository]/results/hdx/elementary/runs/record", "runs/run-elementary", ""),
  ("hdxs", "[repository]/results/hdx/s/runs/record", "runs/run-s", ""),
  ("hdx2", "[repository]/results/hdx/critical/runs/record", "runs/run-critical", "/none"),
]
for name, recdir, mydir, sub in pairs:
    jobs = [j for j in sorted(os.listdir(recdir)) if os.path.isdir(f"{recdir}/{j}") and os.path.exists(f"{recdir}/{j}{sub}/result.json")]
    ndiff = sum(1 for j in jobs if strip(json.load(open(f"{recdir}/{j}{sub}/result.json"))) != strip(json.load(open(f"{mydir}/{j}{sub}/result.json"))))
    print(name, "jobs compared:", len(jobs), "differing:", ndiff)
