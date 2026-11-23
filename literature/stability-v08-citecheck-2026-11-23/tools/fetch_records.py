"""Fetch, by identifier only: one arXiv API request listing the 31 cited arXiv identifiers (no version, so the API
returns each paper's latest version), and the Zenodo record of each of the three Zenodo sources. Every request is
logged. No search is made. Usage: python3 -B -I fetch_records.py <staging dir>"""
import csv, datetime, hashlib, os, re, sys, time, urllib.error, urllib.request
S = sys.argv[1]
UA = "session-L-literature-screen/1.0 (research prototype; small logged batches)"
BH = os.path.expanduser("[repository]")
tex = open(os.path.join(BH, "paper/stability/versions/stability_v0.8.tex"), encoding="utf-8").read()
ids = re.findall(r"\\href\{https://arxiv\.org/abs/([^}]+?)v\d+\}", tex)
zen = re.findall(r"\\href\{https://doi\.org/10\.5281/zenodo\.(\d+)\}", tex)
log = open(os.path.join(S, "cache/records/fetch_log.tsv"), "a", encoding="utf-8")


def get(url, path):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            body, code = r.read(), r.status
    except urllib.error.HTTPError as e:
        body, code = e.read(), e.code
    except Exception as e:
        body, code = repr(e).encode(), 0
    with open(path, "wb") as f:
        f.write(body)
    log.write("\t".join([t, url, str(code), str(len(body)), hashlib.sha256(body).hexdigest(),
                         os.path.relpath(path, S)]) + "\n")
    log.flush()
    print(code, url[:120], len(body))
    time.sleep(4)


print(len(ids), "arXiv ids;", len(zen), "Zenodo records")
get("https://export.arxiv.org/api/query?id_list=" + ",".join(ids) + "&max_results=50",
    os.path.join(S, "cache/records/arxiv_api.xml"))
for z in zen:
    get("https://zenodo.org/api/records/" + z, os.path.join(S, "cache/records/zenodo_%s.json" % z))
