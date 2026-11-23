#!/usr/bin/env bash
# pubkit2 run of record K1 (BHM-219), on host-1: a fresh clone of C1 from the bundle, a fresh venv from its lock, then
# the whole package. Everything under nice -n 19.      bash k1.sh RUNDIR C1
set -u
R="${1:?usage: k1.sh RUNDIR C1}"; C1="${2:?usage: k1.sh RUNDIR C1}"
cd "$R" || exit 1
echo "K1 on $(hostname), start $(date -u +%FT%TZ)"
git clone -q pubkit2.bundle repo || { echo "EXIT clone"; exit 1; }
( cd repo && test "$(git rev-parse HEAD)" = "$C1" \
    && git log -1 --format='commit %H, author %an <%ae>, committer %cn <%ce>' \
    && sha256sum -c --quiet SHA256SUMS && echo "SHA256SUMS OK" ) || { echo "EXIT clone check"; exit 1; }
mkdir -p out
(
  cd repo &&
  nice -n 19 "[python]/bin/python3.12" -m venv ../venv &&
  nice -n 19 ../venv/bin/python -m pip install -q --require-hashes -r requirements.lock &&
  ../venv/bin/python -m pip freeze &&
  BHM_PYTHON="$PWD/../venv/bin/python" nice -n 19 kit/stability/run.sh all ../out/all
)
echo "EXIT $?"
echo "K1 end $(date -u +%FT%TZ)"
