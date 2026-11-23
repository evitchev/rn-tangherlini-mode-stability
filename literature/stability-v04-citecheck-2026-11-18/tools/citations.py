"""List the in-scope citations of DRAFT_v0.4.md: every citation of S37-S59 in section 1 (l.45-134) and section 7
(l.398-427), and the anchored citations of S28 in section 1. Writes ledger/citations.tsv.
Usage: python3 -B -I citations.py <staging dir>"""
import os, re, sys
S = sys.argv[1]
D = os.path.expanduser("[repository]/paper/stability/versions/DRAFT_v0.4.md")
text = open(D, encoding="utf-8").read()
starts = [0]
for m in re.finditer("\n", text):
    starts.append(m.end())
def line_of(pos):
    lo, hi = 0, len(starts) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if starts[mid] <= pos: lo = mid
        else: hi = mid - 1
    return lo + 1
rows = []
for m in re.finditer(r"\[(S\d+[^\]]*)\]", text):
    l0, l1 = line_of(m.start()), line_of(m.end() - 1)
    sec = "1" if 45 <= l0 <= 134 else "7" if 398 <= l0 <= 427 else None
    if sec is None:
        continue
    for part in re.split(r";\s*", " ".join(m.group(1).split())):
        mm = re.match(r"(S\d+)(?:,\s*(.*))?$", part)
        s, anchor = mm.group(1), (mm.group(2) or "")
        n = int(s[1:])
        if 37 <= n <= 59 or (s == "S28" and sec == "1" and anchor):
            rows.append([s, "%d" % l0 if l0 == l1 else "%d-%d" % (l0, l1), "§" + sec, anchor or "(none)"])
with open(os.path.join(S, "ledger/citations.tsv"), "w", encoding="utf-8") as f:
    f.write("S\tdraft_line\tsection\tanchor\n")
    for i, r in enumerate(rows, 1):
        f.write("\t".join(r) + "\n")
for i, r in enumerate(rows, 1):
    print(i, *r)
