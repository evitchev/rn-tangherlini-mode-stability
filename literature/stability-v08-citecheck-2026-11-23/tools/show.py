"""Page helpers for the text layers (pdftotext -layout; a form feed ends each PDF page; lines numbered as split("\\n")).
  show.py <staging> S page <S> <p>        print PDF page p of source S with its line numbers
  show.py <staging> S lines <S> <a> <b>   print lines a..b with the PDF page of each
  show.py <staging> S find <S> <text>     lines containing text (case-insensitive, spaces collapsed), with pages"""
import csv, os, re, sys
S = sys.argv[1]
BH = os.path.expanduser("[repository]")
src = {r["S"]: r for r in csv.DictReader(open(os.path.join(S, "tools/sources.tsv"), encoding="utf-8"), delimiter="\t")}


def lines(s):
    return open(os.path.join(BH, src[s]["bh_copy"], "paper.txt"), encoding="utf-8").read().split("\n")


def page_of_lines(s):
    """The PDF page (1-based) of each line. pdftotext ends each page with a form feed, so a line that starts with
    "\\f" is the first line of the next page."""
    res, p = [], 1
    for L in lines(s):
        k = L.count("\f")
        res.append(p + k)
        p += k
    return res


if __name__ == "__main__":
    mode, s = sys.argv[2], sys.argv[3]
    L, P = lines(s), page_of_lines(s)
    if mode == "page":
        p = int(sys.argv[4])
        for i, (l, q) in enumerate(zip(L, P), 1):
            if q == p:
                print("%5d  %s" % (i, l.replace("\f", "")))
    elif mode == "lines":
        a, b = int(sys.argv[4]), int(sys.argv[5])
        for i in range(a, b + 1):
            print("%5d p%-3d %s" % (i, P[i - 1], L[i - 1].replace("\f", "")))
    elif mode == "find":
        t = " ".join(" ".join(sys.argv[4:]).lower().split())
        for i, l in enumerate(L, 1):
            if t in " ".join(l.lower().split()):
                print("%5d p%-3d %s" % (i, P[i - 1], l.replace("\f", "").strip()[:150]))
