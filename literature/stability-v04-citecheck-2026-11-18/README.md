# Citation check of the stability draft v0.4 (bh-modes message 18)

session-L, 2026-11-18. For the bh-modes lead (message 18; the operator's ruling BHM-182, item 5). My operator approved
the task on 2026-11-18.

**The object.** `paper/stability/versions/DRAFT_v0.4.md`, SHA-256
28af203ac2910320c7466878fbbf8120b5a5e59bb73610d6f3006064357e8864 (checked), 517 lines.

**Independence.**
- I did not open `paper/stability/RELATED_WORK.md`.
- I did not read the Status column of `SOURCES.md`; I read only ID, Source, Fetched and the hashes, for S28 and S37–S59.
- I did not read any other party's audit of v0.4.

## Results

61 rows in `ledger/ledger.md` (the same rows in `ledger/ledger.tsv`):
- C01–C38: one row per citation. That is every citation of S37–S59 in §1 and §7 (35), S28's eqs. (76)–(77) and
  l.762–767, and also S28's Table 1 (C01), the one other anchored S28 citation in §1.
- R01–R23: the reference entries S37–S59.

| verdict | citations | reference entries |
|---|---|---|
| OK | 27 | 22 |
| SAYS MORE | 10 | — |
| ANCHOR OFF | 1 | — |
| MISQUOTED | 0 | — |
| BIBLIOGRAPHY | — | 1 |

- **All nine quoted fragments are verbatim** at their anchors (a normalised comparison, `check` column).
- **Every SAYS MORE is the loss of one qualifier the source states**, and each has a fix of a few words:

| row | draft line | source | what the source says that the draft drops |
|---|---|---|---|
| C04 | 58–59 | S28 l.762–767 | the negative region appears for n > 2 "in general"; n = 3 (D = 5) is a special case where the method works (S28 l.774–776; S48 l.2263–2265). As written, the sentence conflicts with the draft's own l.49 |
| C05 | 61–62 | S48 l.2406–2408 | the quote stops before "that could apply to generic cases" (l.2407–2408) |
| C06, C29 | 69–70, 404 | S52 l.2477–2479 | these are the *light* quasinormal modes of the membrane (l.2438–2439, section 5); l.2476 is the page number |
| C07, C30 | 69–70, 404 | S51 l.326–330 | the same: modes of the leading-order effective theory, which at L → ∞ reproduce S52's |
| C11 | 81 | S40 l.7–12 | "subextremal" Kerr–Newman (l.7) |
| C13 | 84 | S41 l.539–541 | "(see also [Hin25b] for the small mass regime)" (l.541): a second regime where Kerr–de Sitter mode stability is known |
| C16 | 91 | S37 l.10–15 | "in the full subextremal range" (l.8–10) |
| C19 | 95 | S39 l.139–141, l.1845–1848 | "this domain, angular branch, and Riemann sheet" (l.1846–1848): the draft keeps only the domain |

- **ANCHOR OFF, C24 (S56, draft l.103).** The cited abstract (l.6–14) gives the mode stability proof but not the
  computer assistance. That is at l.100–103 (all rational arithmetic; "without the aid of some computer algebra
  system"). Right lines: l.6–7 and l.100–103.
- **BIBLIOGRAPHY, R01 (S37).** doi:10.5281/zenodo.24146363 is Zenodo's concept DOI, which resolves to the latest version.
  v1's own DOI is 10.5281/zenodo.24146364. Write "doi:10.5281/zenodo.24146364 (v1, 11 Nov 2026)", or drop "v1". The
  slip is mine: my S36 screen gave the concept DOI the same way.
- **Eight citations have no anchor.** All are OK, and the ledger gives lines that support each:
  - S46 l.14–19 and S47 l.32–44 (C26, C27);
  - S37 l.10–15 (C28);
  - S58 l.8–12, l.16–17 (C33);
  - S43 l.11–13 (C36);
  - S42 l.163–164, l.446–447 (C37);
  - S59 l.8–10, l.17–20 (C38).
- **Smaller notes, all OK:**
  - S49's title ends "|Q| < M" on the paper's title page but not in arXiv's metadata (R13).
  - S51's title has no umlaut in the original (R15).
  - S43's own abstract names an earlier special case of the separation, Santos's singly spinning sector (C14).
  - S57's existence result is local and "interpreted as" Choptuik's solution (C23).

## The sources and the records

- **The PDFs and text layers** (`ledger/source_hashes.tsv`):
  - All 24 PDFs (S28, S37–S59) and their text layers match SOURCES.md's hashes.
  - The 17 that came from my fetches (S28, and 16 of S37–S59) are byte-identical to my copies.
  - Fresh fetches today of the seven PDFs you fetched (S41–S47) are byte-identical to yours.
  - A fresh `pdftotext -layout` (poppler 0.86.1) of each PDF reproduces each `paper.txt` byte for byte. So the line
    anchors refer to the PDFs as stated.
- **The records** (`cache/records/`, `ledger/records_parsed.tsv`, `ledger/bibcheck.tsv`):
  - For each arXiv source, the abstract page of the cited version; for each Zenodo source, the record.
  - Every cited arXiv version is the latest one.
  - Each SOURCES.md date is that version's date on arXiv.
  - Authors and titles match except as noted in R01 and R13.

## Requests

31 requests on 2026-11-18, all logged with status, size and SHA-256 in `cache/records/fetch_log.tsv`:
- 21 arXiv abstract pages;
- 3 Zenodo records;
- 7 arXiv PDFs.

Each was fetched by identifier only, with the screen's generic User-Agent, 4 s apart; no search was run. All returned
HTTP 200. The seven PDFs and the regenerated text layers are not included, since they are byte-identical to your copies.

## Outside the scope

§1 l.114–121 describe my screens. The figures agree with my records:
- 88 sources in S36 and 52 in S25;
- the last query at 04:30Z on 18 November;
- the services searched and not searched.

One nuance: one of the 88 (Murata, 1211.6903) was a byte copy from S25, not returned by S36's queries (S36,
`ledger/searches.md`).

## Files

- `README.md`: this file.
- `ledger/`:
  - `ledger.md`, `ledger.tsv`: the ledger;
  - `citations.tsv`: the in-scope citations as extracted;
  - `bibcheck.tsv`, `records_parsed.tsv`, `source_hashes.tsv`.
- `cache/records/`: the fetched records and the fetch log.
- `tools/`:
  - `sources.tsv`;
  - `hashes.py`, `fetch_records.py`, `parse_records.py`, `citations.py`, `bibcheck.py`, `show.py`;
  - `spec.py`, which holds the verdicts and notes by hand;
  - `build.py`, which extracts the passages and checks the quotes.

  Run each as `python3 -B -I tools/<name>.py <this folder>`.
- `SHA256SUMS`.
