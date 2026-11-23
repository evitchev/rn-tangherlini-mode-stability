"""Extract every \\cite command of v0.8 with its line, keys, anchor and section; number the references by first
citation (the PDF's order) and check that order against the PDF's own reference list.
Usage: python3 -B -I citations.py <staging dir>"""
import os, re, subprocess, sys
S = sys.argv[1]
BH = os.path.expanduser("[repository]")
V = os.path.join(BH, "paper/stability/versions")
T = open(os.path.join(V, "stability_v0.8.tex"), encoding="utf-8").read().split("\n")
CITE = re.compile(r"\\cite\s*(?:\[([^\]]*)\])?\{([^}]*)\}")
SEC = re.compile(r"\\(section|subsection)\*?\{(.*)")
rows, sec, order = [], "", []
for i, line in enumerate(T, 1):
    if line.startswith("\\begin{thebibliography}"):
        break
    m = SEC.match(line)
    if m:
        lab = re.search(r"\\label\{([^}]*)\}", line)
        sec = lab.group(1) if lab else m.group(2)[:40]
    for c in CITE.finditer(line):
        keys = [k.strip() for k in c.group(2).split(",")]
        for k in keys:
            if k not in order:
                order.append(k)
        rows.append([i, sec, ",".join(keys), c.group(1) or ""])
num = {k: n for n, k in enumerate(order, 1)}
# The PDF's reference list: "[n] <authors>..." lines after the last "References" heading.
subprocess.run(["pdftotext", "-layout", os.path.join(V, "stability_v0.8.pdf"), os.path.join(S, "cache/v08.txt")],
               check=True)
P = open(os.path.join(S, "cache/v08.txt"), encoding="utf-8").read()
refs = P[P.rfind("References"):]
pdf_first = dict(re.findall(r"^\s*\[(\d+)\]\s+(.{0,60})", refs, re.M))
bib = {}
for i, line in enumerate(T, 1):
    m = re.match(r"\\bibitem(?:\[[^\]]*\])?\{([^}]*)\}", line)
    if m:
        bib[m.group(1)] = (i, " ".join(T[i:i + 2]))
with open(os.path.join(S, "ledger/citations.tsv"), "w", encoding="utf-8") as f:
    f.write("cite\ttex_line\tsection\tkeys\tpdf_numbers\tanchor\n")
    for n, (i, s, keys, a) in enumerate(rows, 1):
        f.write("K%02d\t%d\t%s\t%s\t%s\t%s\n" % (n, i, s, keys, ",".join("[%d]" % num[k] for k in keys.split(",")), a))
with open(os.path.join(S, "ledger/numbers.tsv"), "w", encoding="utf-8") as f:
    f.write("key\tpdf_number\tbibitem_line\tpdf_reference_list_start\n")
    for k in order:
        f.write("%s\t[%d]\t%d\t%s\n" % (k, num[k], bib[k][0], pdf_first.get(str(num[k]), "MISSING").strip()))
print(len(rows), "cites;", sum(1 for r in rows if r[3]), "with anchor;", len(order), "keys cited;", len(bib), "bibitems")
print("cited but no bibitem:", [k for k in order if k not in bib], "| bibitem never cited:", [k for k in bib if k not in num])
print("bibitem order == first-citation order:", list(bib) == order)
for k in order:
    print(k, "[%d]" % num[k], "| tex:", re.sub(r"\s+", " ", bib[k][1])[:70], "| pdf:", pdf_first.get(str(num[k]), "MISSING")[:50])
