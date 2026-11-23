"""record_run.py -- bookkeeping only: append one run-of-record entry to runs.json from its log and outputs."""
import hashlib
import json
import re
import sys


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--id', required=True)
    ap.add_argument('--purpose', required=True)
    ap.add_argument('--log', required=True)
    ap.add_argument('--outputs', nargs='*', default=[])
    ap.add_argument('--code', nargs='*', default=[])
    ap.add_argument('--command', required=True)
    ap.add_argument('--expect', default='')
    ap.add_argument('--result', default='')
    args = ap.parse_args()
    txt = open(args.log, encoding='utf-8', errors='replace').read()
    lines = txt.splitlines()
    stamps = [l for l in lines if re.match(r'^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$', l)]
    hosts = [l for l in lines if re.match(r'^host-\d+$', l)]
    exit_m = re.findall(r'EXIT=(\d+)', txt)
    gate = [l for l in lines if l.startswith('GATE ')]
    guard = [l for l in lines if l.startswith('GUARD ')]
    uptime = [l for l in lines if 'load average' in l]
    rec = dict(id=args.id, purpose=args.purpose, kind='run of record', host=hosts[0] if hosts else None,
               hosts_seen=sorted(set(hosts)), start_utc=stamps[0] if stamps else None,
               end_utc=stamps[-1] if stamps else None, exit=int(exit_m[-1]) if exit_m else None,
               node_gate_uptime=uptime[0].strip() if uptime else None, gate=gate[0][5:] if gate else None,
               guard=guard[0][6:] if guard else None, command=args.command, expect=args.expect,
               result=args.result, log=args.log, log_sha256=sha(args.log),
               outputs={p: sha(p) for p in args.outputs}, code={p: sha(p) for p in args.code})
    d = json.load(open('runs.json'))
    assert all(r['id'] != args.id for r in d['phase2_runs']), 'duplicate id'
    d['phase2_runs'].append(rec)
    json.dump(d, open('runs.json', 'w'), indent=1)
    print(json.dumps(rec, indent=1))


if __name__ == '__main__':
    main()
