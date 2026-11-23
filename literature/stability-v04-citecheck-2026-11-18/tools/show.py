"""Print lines of a source's text layer, numbered as split("\\n") (= grep -n, sed -n), with two lines of context marked.
Usage: python3 -B -I show.py <staging dir> <S> <a> <b> [ctx]"""
import csv, os, sys
S, s, a, b = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
ctx = int(sys.argv[5]) if len(sys.argv) > 5 else 2
BH = os.path.expanduser("[repository]")
rows = {r["S"]: r for r in csv.DictReader(open(os.path.join(S, "tools/sources.tsv"), encoding="utf-8"), delimiter="\t")}
L = open(os.path.join(BH, rows[s]["cache"], "paper.txt"), encoding="utf-8").read().split("\n")
for i in range(max(1, a - ctx), min(len(L), b + ctx) + 1):
    mark = ">" if a <= i <= b else " "
    print("%s%5d| %s" % (mark, i, L[i - 1].replace("\f", "<FF>")))
