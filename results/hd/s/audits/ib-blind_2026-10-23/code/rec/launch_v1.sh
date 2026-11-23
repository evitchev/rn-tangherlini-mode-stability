#!/bin/bash
# launch.sh NAME TIMEOUT -- CMD...   (runs on the node, in [session-R-runs]/hds_2026-10-23)
# Detached run with the A1 node-gate header; PID (= process group id) in out/NAME.pid; full log in logs/NAME.log.
NAME=$1; TO=$2; shift 3
cd [session-R-runs]/hds_2026-10-23 || exit 1
setsid bash -c "{ date -u +%Y-%m-%dT%H:%M:%SZ; hostname; uptime; nproc; free -g; ulimit -v 8000000; timeout $TO nice -n 19 $*; echo EXIT=\$?; date -u +%Y-%m-%dT%H:%M:%SZ; hostname; } > logs/$NAME.log 2>&1" < /dev/null > /dev/null 2>&1 &
echo $! > out/$NAME.pid
echo "launched $NAME pid $(cat out/$NAME.pid)"
