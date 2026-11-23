#!/usr/bin/env python3
"""Compare two JSON files field by field; print every differing path.

Usage: python3 -I jsondiff.py A.json B.json [mask_key ...]
Keys named in mask_key are skipped at any depth.
"""
import json
import sys


def walk(a, b, path, mask, out):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k in mask:
                continue
            if k not in a:
                out.append((path + [k], "<missing in A>", "present in B"))
            elif k not in b:
                out.append((path + [k], "present in A", "<missing in B>"))
            else:
                walk(a[k], b[k], path + [k], mask, out)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append((path, f"list len {len(a)}", f"list len {len(b)}"))
        for i, (x, y) in enumerate(zip(a, b)):
            walk(x, y, path + [i], mask, out)
    else:
        if a != b or type(a) is not type(b):
            out.append((path, a, b))


def main():
    fa, fb = sys.argv[1], sys.argv[2]
    mask = set(sys.argv[3:])
    a = json.load(open(fa))
    b = json.load(open(fb))
    out = []
    walk(a, b, [], mask, out)
    print(f"masked keys: {sorted(mask)}")
    print(f"differing leaves: {len(out)}")
    for p, x, y in out[:200]:
        sx, sy = repr(x), repr(y)
        print("/".join(map(str, p)), "|", sx[:160], "|", sy[:160])


if __name__ == "__main__":
    main()
