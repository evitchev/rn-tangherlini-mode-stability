"""Build the ledger from spec.py: extract each passage from the source's text layer (lines numbered as split("\\n")),
check that every quoted fragment of v0.8 (``...'') occurs verbatim, after normalisation, in the passage of the citation
it belongs to (the quote's own \\cite[...] if it sits in an anchor, else the next \\cite after it), and write
ledger/ledger.tsv and ledger/ledger.md. Usage: python3 -B -I build.py <staging dir>"""
import csv, os, re, sys, unicodedata
from collections import Counter
S = sys.argv[1]
sys.path.insert(0, os.path.join(S, "tools"))
from spec import CITATIONS, REFERENCES
import show

BH = os.path.expanduser("[repository]")
TEX = open(os.path.join(BH, "paper/stability/versions/stability_v0.8.tex"), encoding="utf-8").read()
body = TEX[:TEX.index("\\begin{thebibliography}")]
cites = list(csv.DictReader(open(os.path.join(S, "ledger/citations.tsv"), encoding="utf-8"), delimiter="\t"))
bib = {r["S"]: r for r in csv.DictReader(open(os.path.join(S, "ledger/bibcheck.tsv"), encoding="utf-8"), delimiter="\t")}
nums = {r["key"]: r["pdf_number"] for r in csv.DictReader(open(os.path.join(S, "ledger/numbers.tsv"), encoding="utf-8"),
                                                           delimiter="\t")}
assert [c["cite"] for c in cites] == [r[0] for r in CITATIONS], "spec rows do not follow citations.tsv"


def passage(s, ranges):
    L, out = show.lines(s), []
    for rg in ranges.split(";"):
        a, _, b = rg.partition("-")
        a, b = int(a), int(b or a)
        seg = [" ".join(L[i - 1].replace("\f", " ").split()) for i in range(a, b + 1)]
        out.append(" ".join(x for x in seg if x))
    return " [...] ".join(out)


def norm(t):
    t = t.replace("ﬁ", "fi").replace("ﬂ", "fl").replace("ﬀ", "ff").replace("\\ge", "≥")
    t = re.sub(r"\\[a-zA-Z]+", "", t)
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", "", t)


# Quotes and the cite each belongs to.
cite_spans = [m.span() for m in re.finditer(r"\\cite\s*(?:\[[^\]]*\])?\{[^}]*\}", body)]
assert len(cite_spans) == len(cites)
quotes = {}
for m in re.finditer(r"``(.*?)''", body, re.S):
    owner = next(i for i, (a, b) in enumerate(cite_spans) if b > m.start())
    between = body[m.end():cite_spans[owner][0]]
    if cite_spans[owner][0] > m.start() and ("\\file{" in between or len(between) > 400):
        continue                       # a quote of a repository file, not of a cited source
    quotes.setdefault(owner, []).append(" ".join(m.group(1).split()))

rows, problems = [], []
for i, (c, (row, verdict, basis, ranges, note)) in enumerate(zip(cites, CITATIONS)):
    keys = c["keys"].split(",")
    ps = ["%s: %s" % (k, passage(k, ranges[k])) for k in keys if k in ranges]
    check = ""
    if i in quotes:
        res = []
        for q in quotes[i]:
            ok = any(norm(q) in norm(passage(k, ranges[k])) for k in keys if k in ranges)
            res.append("\"%s\": %s" % (q, "verbatim" if ok else "NOT FOUND"))
            if not ok:
                problems.append((row, q))
        check = "; ".join(res)
    lines_read = "; ".join("%s l.%s" % (k, ranges[k].replace(";", ", ")) for k in keys if k in ranges)
    rows.append([row, c["keys"], c["pdf_numbers"], c["tex_line"], c["section"], c["anchor"] or "(none)", verdict, basis,
                 lines_read, " || ".join(ps), check, note])

for k, b in bib.items():
    verdict, note = REFERENCES.get(k, ("OK", ""))
    auto = "record: title match %s, authors match %s; cited %s, latest %s" % (
        b["title_match"], b["authors_match"], b["cited_version"], b["latest_version"])
    if verdict == "OK" and (b["title_match"] != "yes" or b["authors_match"] != "yes") and k not in REFERENCES:
        problems.append((k, auto))
    if b["cited_version"] != b["latest_version"] and b["identifier"][:6] != "zenodo" and k not in REFERENCES:
        problems.append((k, "newer version"))
    jr = (" Journal version: %s." % b["journal_ref"]) if b["journal_ref"] and b["identifier"][:6] != "zenodo" else ""
    rows.append(["R" + nums[k].strip("[]").zfill(2), k, nums[k], "", "References", "reference entry", verdict, "RECORD",
                 "", "Record: \"%s\"; %s" % (b["record_title"], b["record_authors"]), auto,
                 (note or "Authors, title and identifier match the record; the cited version is the latest.") + jr])
rows.sort(key=lambda r: (r[0][0] != "K", r[0]))

hdr = ["row", "keys", "pdf_numbers", "tex_line", "section", "anchor", "verdict", "basis", "lines_read", "passage",
       "check", "note"]
with open(os.path.join(S, "ledger/ledger.tsv"), "w", encoding="utf-8") as f:
    f.write("\t".join(hdr) + "\n")
    for r in rows:
        f.write("\t".join(x.replace("\t", " ").replace("\n", " ") for x in r) + "\n")

with open(os.path.join(S, "ledger/ledger.md"), "w", encoding="utf-8") as f:
    f.write("# Ledger: citation check of stability_v0.8.tex (sha256 975aa46e...02a4) and its PDF (23eae9d6...b1fe)\n\n")
    f.write("One entry per \\cite command (K01-K83, in the order of the text) and per reference entry (R01-R34, by the "
            "PDF's number). Keys are the S-labels; [n] is the PDF's number. Passages are from the text layers named in "
            "SOURCES.md (pdftotext -layout), lines counted as grep -n does; runs of spaces are collapsed, lines joined "
            "with a space, and \"[...]\" joins separate ranges. Basis: READ = read at the source for this check; COMPARED "
            "= an earlier check of mine covered the same claim at the same passage, and v0.8's wording was compared with "
            "the wording checked then; RECORD = checked against the record fetched on 2026-11-23.\n\n")
    for r in rows:
        f.write("## %s %s %s, %s, anchor %s: **%s** (%s)\n\n" % (
            r[0], r[1], r[2], ("tex l.%s (%s)" % (r[3], r[4])) if r[3] else "reference entry", r[5], r[6], r[7]))
        if r[8]:
            f.write("- Lines read: %s\n" % r[8])
        if r[9]:
            f.write("- Passage: %s\n" % r[9])
        if r[10]:
            f.write("- Check: %s\n" % r[10])
        f.write("- Note: %s\n\n" % r[11])

print(Counter(r[6] for r in rows if r[0][0] == "K"), Counter(r[7] for r in rows if r[0][0] == "K"))
print(Counter(r[6] for r in rows if r[0][0] == "R"))
print("quotes checked:", sum(len(v) for v in quotes.values()), "| problems:", problems)
