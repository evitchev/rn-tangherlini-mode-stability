"""Build the ledger from spec.py: extract each passage from the source's text layer (lines numbered as
split("\\n"), i.e. as grep -n and sed -n count them), check that every quoted fragment of the draft occurs verbatim in
its passage (after normalisation), and write ledger/ledger.tsv and ledger/ledger.md.
Usage: python3 -B -I build.py <staging dir>"""
import csv, os, re, sys, unicodedata
S = sys.argv[1]
sys.path.insert(0, os.path.join(S, "tools"))
from spec import CITATIONS, REFERENCES

BH = os.path.expanduser("[repository]")
DRAFT = open(os.path.join(BH, "paper/stability/versions/DRAFT_v0.4.md"), encoding="utf-8").read().split("\n")
src = {r["S"]: r for r in csv.DictReader(open(os.path.join(S, "tools/sources.tsv"), encoding="utf-8"), delimiter="\t")}
rec = {r["S"]: r for r in csv.DictReader(open(os.path.join(S, "ledger/records_parsed.tsv"), encoding="utf-8"), delimiter="\t")}
bib = {r["S"]: r for r in csv.DictReader(open(os.path.join(S, "ledger/bibcheck.tsv"), encoding="utf-8"), delimiter="\t")}
texts = {}


def text(s):
    if s not in texts:
        texts[s] = open(os.path.join(BH, src[s]["cache"], "paper.txt"), encoding="utf-8").read().split("\n")
    return texts[s]


def passage(s, ranges):
    L, out = text(s), []
    for rg in ranges.split(";"):
        a, _, b = rg.partition("-")
        a, b = int(a), int(b or a)
        seg = [" ".join(L[i - 1].replace("\f", " ").split()) for i in range(a, b + 1)]
        out.append(" ".join(x for x in seg if x))
    return " [...] ".join(out)


def norm(t):
    t = t.replace("ﬁ", "fi").replace("ﬂ", "fl").replace("ﬀ", "ff")
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", "", t)


def draft_text(lines):
    """The whole list item (or paragraph) that holds the citation's lines."""
    a, _, b = lines.partition("-")
    a, b = int(a), int(b or a)
    while a > 1 and not re.match(r"\s*(- |\*\*)", DRAFT[a - 1]) and DRAFT[a - 2].strip():
        a -= 1
    while b < len(DRAFT) and DRAFT[b].strip() and not re.match(r"\s*- ", DRAFT[b]):
        b += 1
    return " ".join(" ".join(DRAFT[i - 1].split()) for i in range(a, b + 1))


rows, problems = [], []
for k, (s, dl, sec, anchor, verdict, rng, manual, quote, note) in enumerate(CITATIONS, 1):
    p = manual or passage(s, rng)
    q = ""
    if quote:
        in_draft = norm(quote) in norm(draft_text(dl))
        in_src = norm(quote) in norm(passage(s, rng))
        q = "quote found verbatim in draft and source" if in_draft and in_src else "QUOTE CHECK FAILED"
        if not (in_draft and in_src):
            problems.append((k, s, in_draft, in_src))
    rows.append(["C%02d" % k, s, dl, sec, anchor, verdict, rng.replace(";", ", "), p, q, note, ""])

for k, n in enumerate(range(37, 60), 1):
    s = "S%d" % n
    r, b = rec[s], bib[s]
    verdict, note = REFERENCES.get(s, ("OK", ""))
    if s in ("S37", "S58", "S59"):
        rd = r["versions / record data"]
        p = "Zenodo record: title \"%s\"; creators %s; %s; %s" % (
            r["title (record)"], r["authors (record)"], re.sub(r", files: .*", "", rd), b["version_or_doi"])
    else:
        p = "arXiv abstract page of the cited version: title \"%s\"; authors %s; versions %s; %s; %s" % (
            r["title (record)"], r["authors (record)"], r["versions / record data"], b["version_or_doi"], b["date"])
    auto = "authors match: %s; title match (normalised): %s" % (b["authors_match"], b["title_match"])
    if verdict == "OK" and (b["authors_match"] != "yes" or b["title_match"] != "yes") and s != "S49":
        problems.append(("R%02d" % k, s, b["authors_match"], b["title_match"]))
    rows.append(["R%02d" % k, s, b["draft_line"], "References", "reference entry", verdict, "", p, auto,
                 note or "Authors, title and version match the record; SOURCES.md's date is the cited version's date.",
                 DRAFT[int(b["draft_line"]) - 1].strip() + " " + DRAFT[int(b["draft_line"])].strip()])

hdr = ["row", "S", "draft_line", "section", "anchor_in_draft", "verdict", "lines_read", "passage", "check", "note",
       "draft_entry"]
with open(os.path.join(S, "ledger/ledger.tsv"), "w", encoding="utf-8") as f:
    f.write("\t".join(hdr) + "\n")
    for r in rows:
        f.write("\t".join(x.replace("\t", " ") for x in r) + "\n")

with open(os.path.join(S, "ledger/ledger.md"), "w", encoding="utf-8") as f:
    f.write("# Ledger: citation check of DRAFT_v0.4.md (sha256 28af203a...8864)\n\n")
    f.write("One entry per citation (C01-C38) and per reference entry (R01-R23). Passages are from the text layers "
            "named in message 18 (pdftotext -layout, poppler 0.86.1). Line numbers count as grep -n does. Runs of "
            "spaces are collapsed and lines are joined with a space; \"[...]\" joins separate ranges. Otherwise the "
            "text is as in paper.txt, line-end hyphens included. Bracketed words in a passage are mine.\n\n")
    for r in rows:
        f.write("## %s %s, draft l.%s (%s), %s: **%s**\n\n" % (r[0], r[1], r[2], r[3], r[4], r[5]))
        if r[10]:
            f.write("- Draft entry: %s\n" % r[10])
        f.write("- Passage%s: %s\n" % (" (l.%s)" % r[6] if r[6] else "", r[7]))
        if r[8]:
            f.write("- Check: %s\n" % r[8])
        f.write("- Note: %s\n\n" % r[9])

from collections import Counter
print(Counter(r[5] for r in rows if r[0].startswith("C")), Counter(r[5] for r in rows if r[0].startswith("R")))
print("problems:", problems)
