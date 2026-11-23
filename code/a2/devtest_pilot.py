"""Development tests of a2.pilot, run before registration (results/a2/pilot/PREREG.md section 6).  Synthetic inputs
only: W = 12 - 7x in place of S5's U_-/(64 H_-^2), which has the same values at the extremal horizon (x = 2: -2, so
c = -2/9) and at infinity (12), and is otherwise unrelated.  T3's gate needs S5's potential and is not run.

    python -m a2.devtest_pilot
"""
import json
import subprocess
import sys
import tempfile

from a2 import pilot

SYN = (lambda mm, dd, xx: 64 * mm * mm * (12 - 7 * xx), lambda mm, dd, xx: mm)


def main():
    outs = []
    with tempfile.TemporaryDirectory() as tmp:
        for k in range(2):
            out = f"{tmp}/run{k}"
            code = pilot.main(["--out", out], funcs=SYN)
            rec = json.load(open(f"{out}/result.json"))
            print(f"synthetic run {k}: exit {code}, verdict {rec['verdict']!r}, least degree {rec.get('least_degree')}, "
                  f"gates {[(g, v['ok']) for g, v in rec.get('gates', {}).items()]}")
            outs.append(f"{out}/result.json")
        cmp = subprocess.run([sys.executable, "compare_runs.py"] + outs, capture_output=True, text=True)
        print("compare_runs:", cmp.stdout.strip().splitlines()[-1])


if __name__ == "__main__":
    main()
