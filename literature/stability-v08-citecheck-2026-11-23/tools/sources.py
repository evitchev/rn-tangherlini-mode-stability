"""Build tools/sources.tsv: for each reference entry of v0.8 (its \\bibitem keys), the SOURCES.md bibliographic columns
(ID, Source, Fetched, hashes; the Status column is not read) and the bh-modes copy of its PDF and text layer, found by
SHA-256 prefix. Also my own earlier copy, if any (my deliveries only).
Usage: python3 -B -I sources.py <staging dir>"""
import hashlib, os, re, sys
S = sys.argv[1]
BH = os.path.expanduser("[repository]")
MINE = os.path.expanduser("[deliveries]")
NOT_MINE = ("fable_", "kimi_", "ib-", "ib_")
tex = open(os.path.join(BH, "paper/stability/versions/stability_v0.8.tex"), encoding="utf-8").read()
keys = re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^}]*)\}", tex)
rows = {}
for l in open(os.path.join(BH, "SOURCES.md"), encoding="utf-8"):
    if re.match(r"^\| S\d+ \|", l):
        c = [x.strip().replace("\x00", "\\|") for x in l.strip().replace("\\|", "\x00").strip("|").split("|")]
        rows[c[0]] = {"ID": c[0], "Source": c[1], "Fetched": c[3], "hashes": c[4]}


def h(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def pdfs(root, skip_dirs=()):
    for d, ds, fs in os.walk(root):
        ds[:] = [x for x in ds if x != ".git" and not x.startswith(skip_dirs)]
        for f in fs:
            if f.endswith(".pdf"):
                yield os.path.join(d, f)


bh_index, my_index = {}, {}
for p in pdfs(os.path.join(BH, "literature")):
    bh_index.setdefault(h(p)[:16], []).append(p)
for p in pdfs(MINE, NOT_MINE):
    my_index.setdefault(h(p)[:16], []).append(p)
out = ["\t".join(["S", "pdf16", "txt16", "bh_copy", "my_copy", "source", "fetched"])]
for k in keys:
    r = rows[k]
    m = re.search(r"`([0-9a-f]{16})` / `([0-9a-f]{16})`", r["hashes"])
    p16, t16 = m.groups()
    cands = sorted(bh_index.get(p16, []))
    pick = "-"
    for c in cands:
        t = os.path.join(os.path.dirname(c), "paper.txt")
        if os.path.exists(t) and h(t)[:16] == t16:
            pick = os.path.relpath(os.path.dirname(c), BH)
            break
    mine = sorted(my_index.get(p16, []))
    out.append("\t".join([k, p16, t16, pick, os.path.relpath(os.path.dirname(mine[0]), MINE) if mine else "-",
                          r["Source"], r["Fetched"]]))
open(os.path.join(S, "tools/sources.tsv"), "w", encoding="utf-8").write("\n".join(out) + "\n")
for o in out:
    print("\t".join(o.split("\t")[:5]))
