"""Compare the draft's reference entries S37-S59 with the fetched records (arXiv abstract page of the cited version;
Zenodo record), and SOURCES.md's dates with the record's date of the cited version.
Usage: python3 -B -I bibcheck.py <staging dir>"""
import csv, os, re, sys, unicodedata
S = sys.argv[1]
BH = os.path.expanduser("[repository]")
draft = open(os.path.join(BH, "paper/stability/versions/DRAFT_v0.4.md"), encoding="utf-8").read().split("\n")
src = open(os.path.join(BH, "SOURCES.md"), encoding="utf-8").read()
rec = {r["S"]: r for r in csv.DictReader(open(os.path.join(S, "ledger/records_parsed.tsv"), encoding="utf-8"), delimiter="\t")}
def norm(t):
    t = t.replace("$", "").replace("--", "-").replace("\\\"o", "o")
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9|<>]+", " ", t).strip()
entries, cur = {}, None
for i, l in enumerate(draft, 1):
    m = re.match(r"- \[(S\d+)\] (.*)", l)
    if m:
        cur = m.group(1); entries[cur] = [i, m.group(2)]
    elif cur and l.startswith("  ") and entries[cur][1]:
        entries[cur][1] += " " + l.strip()
    else:
        cur = None
MON = {m: i for i, m in enumerate("Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), 1)}
out = []
for n in range(37, 60):
    s = "S%d" % n
    line, e = entries[s]
    r = rec[s]
    m = re.match(r"(.*), (arXiv:\S+|Zenodo, doi:\S+.*)$", e)
    head, ident = m.group(1), m.group(2).rstrip(".")
    parts = head.split(", ")
    k = 0
    while k < len(parts) and (re.match(r"^(?:[A-Z]\.(?:-[A-Z]\.)?\s)+[A-Z][^\s,]*(?:\s(?:da\s)?[A-Z][^\s,]*)*$", parts[k]) or parts[k] == "Neko2333OWO"):
        k += 1
    authors, title = parts[:k], ", ".join(parts[k:])
    sur_d = [norm(a.split()[-1]) for a in authors]
    sur_r = [norm(a.split(",")[0]) for a in r["authors (record)"].split("; ")]
    if s == "S55":
        sur_r = ["teixeira da costa"]; sur_d = [norm("Teixeira da Costa")]
    au_ok = sur_d == sur_r
    ti_ok = norm(title) == norm(r["title (record)"])
    srow = re.search(r"^\| %s \| (.*?) \|" % s, src, re.M).group(1)
    if ident.startswith("arXiv"):
        v = re.search(r"v(\d+)$", ident).group(1)
        hist = dict(re.findall(r"v(\d+) [A-Z][a-z]{2}, (\d+ [A-Z][a-z]{2} \d{4})", r["versions / record data"]))
        latest = max(int(k) for k in hist)
        srcdate = re.search(r"\((\d+ [A-Z][a-z]{2} \d{4})\)", srow)
        date_ok = bool(srcdate) and srcdate.group(1) == hist.get(v)
        vnote = "cited v%s = latest v%d" % (v, latest) if int(v) == latest else "cited v%s, LATEST IS v%d" % (v, latest)
        out.append([s, str(line), "yes" if au_ok else "NO", "yes" if ti_ok else "NO",
                    vnote, "SOURCES date %s = v%s date: %s" % (srcdate.group(1) if srcdate else "?", v, "yes" if date_ok else "NO")])
    else:
        doi = re.search(r"doi:(\S+?)[ ,]", ident + " ").group(1)
        rd = r["versions / record data"]
        vdoi = re.search(r"^doi (\S+),", rd).group(1); cdoi = re.search(r"conceptdoi (\S+),", rd).group(1)
        kind = "version DOI" if doi == vdoi else "CONCEPT DOI (version DOI is %s)" % vdoi if doi == cdoi else "UNKNOWN DOI"
        pd = re.search(r"publication_date (\S+),", rd).group(1)
        out.append([s, str(line), "yes" if au_ok else "NO", "yes" if ti_ok else "NO", "draft doi %s = %s" % (doi, kind),
                    "record publication_date %s" % pd])
with open(os.path.join(S, "ledger/bibcheck.tsv"), "w", encoding="utf-8") as f:
    f.write("S\tdraft_line\tauthors_match\ttitle_match\tversion_or_doi\tdate\n")
    for o in out:
        f.write("\t".join(o) + "\n")
for o in out:
    print(" | ".join(o))
