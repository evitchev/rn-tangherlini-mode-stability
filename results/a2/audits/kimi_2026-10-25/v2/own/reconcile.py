"""Reconciliation: my kit reproductions vs the records, with the output logged.
(Added 2026-10-25 after the lead's receipt noted the comparison had no log.)
"""
import json

def strip(d):
    if isinstance(d, dict):
        return {k: strip(v) for k, v in d.items()
                if k not in ('timing', 'provenance', 't_design_s', 't_verify_s',
                             'utc_start', 'archive_sha256')}
    if isinstance(d, list):
        return [strip(x) for x in d]
    return d

for name, recp, myp in [
    ("elementary",
     "[repository]/results/a2/elementary/runs/record/none/result.json",
     "runs/run-elementary/none/result.json"),
    ("s",
     "[repository]/results/a2/s/runs/record/none/result.json",
     "runs/run-s/none/result.json"),
]:
    rec = json.load(open(recp))
    mine = json.load(open(myp))
    print(name, "substantively identical:", strip(rec) == strip(mine))
