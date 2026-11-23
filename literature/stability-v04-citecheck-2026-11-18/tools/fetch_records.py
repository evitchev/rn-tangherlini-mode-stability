"""Fetch, by identifier only, the arXiv abstract page of each cited version, the Zenodo record of each Zenodo source,
and (for the seven sources the lead fetched) the arXiv PDF of the cited version. Every request is logged.
Usage: python3 -B -I fetch_records.py <staging dir>"""
import csv, hashlib, os, sys, time, urllib.request, urllib.error, datetime
S = sys.argv[1]
UA = "session-L-literature-screen/1.0 (research prototype; small logged batches)"
CITED = {"S28": "gr-qc/0312012v1", "S38": "2609.21797v2", "S39": "2610.39095v3", "S40": "2609.33661v1",
         "S41": "2606.28253v2", "S42": "2610.33812v1", "S43": "2611.21591v1", "S44": "2509.12435v1",
         "S45": "2610.28367v1", "S46": "2611.16908v1", "S47": "2611.07395v1", "S48": "1103.6148v2",
         "S49": "1910.05630v2", "S50": "1809.05144v1", "S51": "1511.06059v2", "S52": "1511.03432v2",
         "S53": "1809.00795v3", "S54": "1910.08479v2", "S55": "1910.02854v1", "S56": "1411.2947v3",
         "S57": "1203.3766v1"}
ZEN = {"S37": "24146363", "S58": "24285821", "S59": "24288754"}
LEAD_FETCHED = ["S41", "S42", "S43", "S44", "S45", "S46", "S47"]
log = open(os.path.join(S, "cache/records/fetch_log.tsv"), "a", encoding="utf-8")
def get(url, path):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    t = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
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
    print(code, url, len(body))
    time.sleep(4)
for s, aid in CITED.items():
    get("https://arxiv.org/abs/" + aid, os.path.join(S, "cache/records", s + "_abs.html"))
for s, zid in ZEN.items():
    get("https://zenodo.org/api/records/" + zid, os.path.join(S, "cache/records", s + "_zenodo.json"))
os.makedirs(os.path.join(S, "cache/pdfs"), exist_ok=True)
for s in LEAD_FETCHED:
    get("https://arxiv.org/pdf/" + CITED[s], os.path.join(S, "cache/pdfs", s + ".pdf"))
