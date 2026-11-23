"""Hash each source PDF and text layer, compare with SOURCES.md, with my own earlier fetch, and with a fresh
pdftotext -layout run of the same PDF. Usage: python3 -B -I hashes.py <staging dir>"""
import csv, hashlib, os, re, subprocess, sys
S = sys.argv[1]
BH = os.path.expanduser("[repository]")
MINE = os.path.expanduser("[deliveries]")
def h(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()
src = open(os.path.join(BH, "SOURCES.md"), encoding="utf-8").read()
rows = list(csv.DictReader(open(os.path.join(S, "tools/sources.tsv"), encoding="utf-8"), delimiter="\t"))
out = [["S", "pdf_sha256", "txt_sha256", "pdf16_matches_SOURCES", "txt16_matches_SOURCES", "pdf_equals_my_fetch",
        "fresh_pdftotext_equals_txt"]]
for r in rows:
    d = os.path.join(BH, r["cache"])
    pdf, txt = os.path.join(d, "paper.pdf"), os.path.join(d, "paper.txt")
    hp, ht = h(pdf), h(txt)
    m = re.search(r"^\| %s \|.*`([0-9a-f]{16})` / `([0-9a-f]{16})`" % r["S"], src, re.M)
    p16 = "yes" if m and m.group(1) == hp[:16] else "NO"
    t16 = "yes" if m and m.group(2) == ht[:16] else "NO"
    if r["mine"] == "-":
        mine = "n/a (lead's fetch)"
    else:
        mp = os.path.join(MINE, r["mine"], "paper.pdf")
        mine = "yes" if os.path.exists(mp) and h(mp) == hp else "NO"
    os.makedirs(os.path.join(S, "cache/textcheck"), exist_ok=True)
    fresh = os.path.join(S, "cache/textcheck", r["S"] + ".txt")
    subprocess.run(["pdftotext", "-layout", pdf, fresh], check=True, stderr=subprocess.DEVNULL)
    fr = "yes" if h(fresh) == ht else "NO"
    out.append([r["S"], hp, ht, p16, t16, mine, fr])
with open(os.path.join(S, "ledger/source_hashes.tsv"), "w", encoding="utf-8") as f:
    for o in out:
        f.write("\t".join(o) + "\n")
for o in out:
    print(o[0], *o[3:])
