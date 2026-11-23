"""HD-E full own-suite runner (Kimi): Lemma U(n), then E1+E2, then controls."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import lemmaUn
import hd
import controls_hd


def main():
    print("=== Lemma U(n) ===", flush=True)
    rc1 = lemmaUn.main()
    l0s = {int(k): v["l0"] for k, v in
           json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                       "lemmaU_results.json"))).items()}
    print("=== E1 + E2 ===", flush=True)
    rc2 = hd.main(l0s)
    print("=== controls ===", flush=True)
    rc3 = controls_hd.main()
    print("RUN_ALL:", "ALL OK" if (rc1 == 0 and rc2 == 0 and rc3 == 0) else "FAILURE")
    return 0 if (rc1 == 0 and rc2 == 0 and rc3 == 0) else 1


if __name__ == "__main__":
    raise SystemExit(main())
