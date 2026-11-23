#!/usr/bin/env bash
# pubkit2 run of record K3 (BHM-219), on host-2: a fresh clone of C1 from the bundle, then the Lean part, with the
# toolchain and a copy of Mathlib's lean_path.txt given explicitly. Everything under nice -n 19.
#      bash k3.sh RUNDIR C1
set -u
R="${1:?usage: k3.sh RUNDIR C1}"; C1="${2:?usage: k3.sh RUNDIR C1}"
cd "$R" || exit 1
echo "K3 on $(hostname), start $(date -u +%FT%TZ)"
git clone -q pubkit2.bundle repo || { echo "EXIT clone"; exit 1; }
( cd repo && test "$(git rev-parse HEAD)" = "$C1" \
    && git log -1 --format='commit %H, author %an <%ae>, committer %cn <%ce>' \
    && sha256sum -c --quiet SHA256SUMS && echo "SHA256SUMS OK" ) || { echo "EXIT clone check"; exit 1; }
cp "$HOME/lean-setup/lean_path.txt" "$R/lean_path_copy.txt"
mkdir -p out
(
  cd repo &&
  BHM_LEAN_TOOLCHAIN="$HOME/.elan/toolchains/leanprover--lean4---v4.24.0" BHM_LEAN_PATH_FILE="$R/lean_path_copy.txt" \
      nice -n 19 kit/stability/run_lean.sh ../out/lean
)
echo "EXIT $?"
echo "K3 end $(date -u +%FT%TZ)"
