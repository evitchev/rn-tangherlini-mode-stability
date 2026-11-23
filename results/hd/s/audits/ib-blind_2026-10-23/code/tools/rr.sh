#!/bin/bash
# rr.sh NAME TIMEOUT -- CMD...   launch a run of record on $NODE (default host-2) via code/rec/launch_v1.sh,
# wait by PID only (no process listing), then fetch logs/NAME.log and out/NAME*.json back to host-0.
NODE=${NODE:-host-2}
NAME=$1; TO=$2; shift 3
W=[session-R-runs]/hds_2026-10-23
timeout 60 ssh -o BatchMode=yes $NODE "cd [session-R-runs]/hds_2026-10-23 && bash code/rec/launch_v1.sh $NAME $TO -- $*" || exit 1
while true; do
  st=$(timeout 60 ssh -o BatchMode=yes $NODE "cd [session-R-runs]/hds_2026-10-23 && if ps -o pid= -p \$(cat out/$NAME.pid) > /dev/null; then echo RUNNING; else echo DONE; fi")
  [ "$st" = "DONE" ] && break
  sleep 15
done
timeout 120 scp -o BatchMode=yes -q $NODE:ib-blind/hds_2026-10-23/logs/$NAME.log $W/logs/
timeout 120 scp -o BatchMode=yes -q "$NODE:ib-blind/hds_2026-10-23/out/$NAME*.json" $W/out/ 2>/dev/null
echo "FETCHED $NAME"; grep -v "C9:" $W/logs/$NAME.log | tail -40
