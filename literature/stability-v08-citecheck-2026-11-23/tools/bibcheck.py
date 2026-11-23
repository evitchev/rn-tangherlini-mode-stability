"""Compare each \\bibitem of v0.8 with the fetched records: arXiv API (latest version, title, authors) and Zenodo
(title, creators, version, whether it is the latest). Writes ledger/bibcheck.tsv.
Usage: python3 -B -I bibcheck.py <staging dir>"""
import json, os, re, sys, unicodedata
import xml.etree.ElementTree as ET
S = sys.argv[1]
BH = os.path.expanduser("[repository]")
T = open(os.path.join(BH, "paper/stability/versions/stability_v0.8.tex"), encoding="utf-8").read()
bib = T[T.index("\\begin{thebibliography}"):]
items = re.findall(r"\\bibitem\{(S\d+)\}(.*?)(?=\\bibitem|\\end\{thebibliography\})", bib, re.S)
A = "{http://www.w3.org/2005/Atom}"
api = ET.parse(os.path.join(S, "cache/records/arxiv_api.xml")).getroot()
rec = {}
for e in api.findall(A + "entry"):
    full = e.find(A + "id").text.rsplit("/abs/", 1)[1]
    base, ver = re.match(r"(.+?)(v\d+)$", full).groups()
    rec[base] = {"latest": ver, "title": " ".join(e.find(A + "title").text.split()),
                 "authors": [a.find(A + "name").text for a in e.findall(A + "author")],
                 "jref": (e.find("{http://arxiv.org/schemas/atom}journal_ref").text
                          if e.find("{http://arxiv.org/schemas/atom}journal_ref") is not None else "")}


def detex(s):
    s = re.sub(r"\\href\{[^}]*\}\{([^}]*)\}", r"\1", s)
    for a, b in [("\\\"o", "ö"), ("\\v{z}", "ž"), ("\\'c", "ć"), ("\\'o", "ó"), ("\\'A", "Á"), ("\\'a", "á"),
                 ("--", "–"), ("~", " "), ("\\emph{", ""), ("$", ""), ("\\", "")]:
        s = s.replace(a, b)
    return " ".join(s.replace("{", "").replace("}", "").split())


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower().replace("ø", "o"))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", s)


def surname(a):
    return norm(a.split()[-1])


out = [["S", "identifier", "cited_version", "latest_version", "title_match", "authors_match", "record_title",
        "record_authors", "journal_ref", "entry"]]
for k, body in items:
    e = detex(body.strip())
    m = re.search(r"arXiv:(\S+?)(v\d+)\.", e)
    title = re.search(r"\\emph\{(.*?)\},\s*(?:\\href|Zenodo)", body, re.S)
    t = detex(title.group(1)) if title else ""
    names = detex(body.split("\\emph{")[0]).rstrip(", ")
    au = [x.strip() for x in re.split(r",| and ", names) if x.strip()]
    if m:
        r = rec[m.group(1)]
        out.append([k, m.group(1), m.group(2), r["latest"], "yes" if norm(t) == norm(r["title"]) else "NO",
                    "yes" if [surname(a) for a in au] == [surname(a) for a in r["authors"]] else "NO",
                    r["title"], "; ".join(r["authors"]), r["jref"], e])
    else:
        z = re.search(r"zenodo\.(\d+)", body).group(1)
        j = json.load(open(os.path.join(S, "cache/records/zenodo_%s.json" % z), encoding="utf-8"))
        md = j["metadata"]
        rel = md.get("relations", {}).get("version", [{}])[0]
        zt = md["title"]
        out.append([k, "zenodo " + z, md.get("version", "") or ("index %s" % rel.get("index")),
                    "is_last=%s; concept %s" % (rel.get("is_last"), j.get("conceptrecid")),
                    "yes" if norm(t) == norm(zt) else "NO",
                    "yes" if [surname(a) for a in au] == [surname(c["name"].replace(",", " ")) if "," not in c["name"]
                                                          else norm(c["name"].split(",")[0]) for c in md["creators"]] else "NO",
                    zt, "; ".join(c["name"] for c in md["creators"]), md.get("publication_date", ""), e])
with open(os.path.join(S, "ledger/bibcheck.tsv"), "w", encoding="utf-8") as f:
    for o in out:
        f.write("\t".join(x.replace("\t", " ") for x in o) + "\n")
for o in out:
    print("\t".join(o[:6]), "|", o[6][:70] if o[4] == "NO" else "", "|", o[7][:80] if o[5] == "NO" else "", "|", o[8][:50])
