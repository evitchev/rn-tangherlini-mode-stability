"""Pull title, authors and version history from the fetched arXiv abstract pages and Zenodo records, and compare the
seven lead-fetched PDFs with fresh fetches. Usage: python3 -B -I parse_records.py <staging dir>"""
import hashlib, html, json, os, re, sys
S = sys.argv[1]
BH = os.path.expanduser("[repository]")
R = os.path.join(S, "cache/records")
out = []
for fn in sorted(os.listdir(R)):
    p = os.path.join(R, fn)
    s = fn.split("_")[0]
    if fn.endswith("_abs.html"):
        t = open(p, encoding="utf-8").read()
        h1 = re.search(r'<h1 class="title mathjax">(.*?)</h1>', t, re.S).group(1)
        title = " ".join(html.unescape(re.sub(r"<[^>]+>", "", h1)).split()).replace("Title:", "").strip()
        auth = [html.unescape(a) for a in re.findall(r'<meta name="citation_author" content="([^"]*)"', t)]
        hist = re.search(r"Submission history</h2>(.*?)</div>", t, re.S).group(1)
        hist = " ".join(re.sub(r"<[^>]+>", " ", hist).split())
        vers = ["v%s %s" % m for m in re.findall(r"\[v(\d+)\] ([A-Z][a-z]{2}, \d+ [A-Z][a-z]{2} \d{4})", hist)]
        out.append([s, title, "; ".join(auth), " | ".join(vers)])
    elif fn.endswith("_zenodo.json"):
        j = json.load(open(p, encoding="utf-8"))
        m = j["metadata"]
        files = "; ".join("%s %s" % (f["key"], f.get("checksum", "")) for f in j.get("files", []))
        out.append([s, m["title"], "; ".join(c.get("name", "") + (" [" + c.get("affiliation", "") + "]" if c.get("affiliation") else "")
                    for c in m.get("creators", [])),
                    "doi %s, conceptdoi %s, id %s, version %s, publication_date %s, created %s, updated %s, files: %s" % (
                        j.get("doi"), j.get("conceptdoi"), j.get("id"), m.get("version"), m.get("publication_date"),
                        j.get("created", "")[:10], j.get("updated", "")[:10], files)])
with open(os.path.join(S, "ledger/records_parsed.tsv"), "w", encoding="utf-8") as f:
    f.write("S\ttitle (record)\tauthors (record)\tversions / record data\n")
    for o in out:
        f.write("\t".join(o) + "\n")
for o in out:
    print(" || ".join(o))
print()
for s, d in [("S41", "2606.28253"), ("S42", "2610.33812"), ("S43", "2611.21591"), ("S44", "2509.12435"),
             ("S45", "2610.28367"), ("S46", "2611.16908"), ("S47", "2611.07395")]:
    a = hashlib.sha256(open(os.path.join(S, "cache/pdfs", s + ".pdf"), "rb").read()).hexdigest()
    b = hashlib.sha256(open(os.path.join(BH, "literature/cache", d, "paper.pdf"), "rb").read()).hexdigest()
    print(s, "fresh fetch equals lead's PDF:", a == b)
