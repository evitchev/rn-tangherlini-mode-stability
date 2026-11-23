"""For each source: the full SHA-256 of the bh-modes copy's PDF and text layer, whether their first 16 hex match
SOURCES.md (sources.tsv), whether the PDF equals my own earlier copy (if I fetched it), and whether a fresh
pdftotext -layout of the PDF reproduces paper.txt byte for byte. Usage: python3 -B -I hashes.py <staging dir>"""
import csv, hashlib, os, subprocess, sys
S = sys.argv[1]
BH = os.path.expanduser("[repository]")
MINE = os.path.expanduser("[deliveries]")


def h(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


rows = list(csv.DictReader(open(os.path.join(S, "tools/sources.tsv"), encoding="utf-8"), delimiter="\t"))
os.makedirs(os.path.join(S, "cache/textcheck"), exist_ok=True)
out = [["S", "pdf_sha256", "txt_sha256", "pdf16_matches_SOURCES", "txt16_matches_SOURCES", "pdf_equals_my_copy",
        "fresh_pdftotext_equals_txt"]]
for r in rows:
    d = os.path.join(BH, r["bh_copy"])
    hp, ht = h(os.path.join(d, "paper.pdf")), h(os.path.join(d, "paper.txt"))
    mine = "n/a (not fetched by me)" if r["my_copy"] == "-" else (
        "yes" if h(os.path.join(MINE, r["my_copy"], "paper.pdf")) == hp else "NO")
    fresh = os.path.join(S, "cache/textcheck", r["S"] + ".txt")
    subprocess.run(["pdftotext", "-layout", os.path.join(d, "paper.pdf"), fresh], check=True, stderr=subprocess.DEVNULL)
    out.append([r["S"], hp, ht, "yes" if hp[:16] == r["pdf16"] else "NO", "yes" if ht[:16] == r["txt16"] else "NO",
                mine, "yes" if h(fresh) == ht else "NO"])
with open(os.path.join(S, "ledger/source_hashes.tsv"), "w", encoding="utf-8") as f:
    for o in out:
        f.write("\t".join(o) + "\n")
from collections import Counter
for i, name in enumerate(out[0][3:], 3):
    print(name, Counter(o[i] for o in out[1:]))
