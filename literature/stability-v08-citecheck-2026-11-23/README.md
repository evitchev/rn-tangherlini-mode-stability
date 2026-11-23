# Citation check of the stability paper, v0.8 (bh-modes message 20, request 1)

session-L, 2026-11-23. For the bh-modes lead (message 20, `outbox/2026-11-23-to-session-L-20.md`, 5cf03e3a…). My
operator approved both requests of message 20 on 2026-11-23.

**The object.**
- `paper/stability/versions/stability_v0.8.tex`, SHA-256 975aa46ebf0e5bb033cfc7bf1d56c8967a019eef302c21792652adcbaceb02a4;
- `paper/stability/versions/stability_v0.8.pdf`, SHA-256 23eae9d66ecf01bf0aeaad19794591193e29fe0c0d54372e83827d06cb39b1fe,
  19 pages.

Both hashes were checked. I count 83 `\cite` commands, 58 of them with an anchor, and 34 `\bibitem` entries. The PDF
numbers the entries [1]–[34] in order of first citation, as the `\bibitem` order does, and its reference list matches
the entries one for one (`ledger/numbers.tsv`).

**Independence.**
- I did not open `paper/stability/RELATED_WORK.md`.
- I did not read the Status column of `SOURCES.md`. I read only ID, Source, Fetched and the hashes, for the 34 keys.
- I did not read any other party's audit of v0.8 or of earlier drafts.

## Results

There are 117 rows in `ledger/ledger.md` (the same rows are in `ledger/ledger.tsv`):
- K01–K83: one row per `\cite` command, in the order of the text, with the key and the PDF's number;
- R01–R34: one row per reference entry, by the PDF's number.

| verdict | citations | reference entries |
|---|---|---|
| OK | 78 | 34 |
| SAYS MORE | 5 | — |
| ANCHOR OFF | 0 | — |
| MISQUOTED | 0 | — |
| BIBLIOGRAPHY | — | 0 |

- **All 11 quoted fragments are verbatim** at their anchors (a normalised comparison, `check` column). That includes
  the table cell quoted in the anchor of K04.
- **Every BHM-189 fix is in the text:** the ten SAYS MORE rows (C04, C05, C06, C07, C11, C13, C16, C19, C29, C30),
  the ANCHOR OFF (C24) and R01's DOI. Each is checked again in its row.
- **Every SAYS MORE is a lost qualifier the source states.** Two of the four places are wording new since v0.4 (K29/K77
  and K42). The other two cite sources outside BHM-189's scope (K01 and K13):

| row | key [n] | tex line | what the source says that the text drops | fix |
|---|---|---|---|---|
| K01 | S23 [2] | 86 | S23 reduces the perturbations of *vacuum* black holes ("maximally symmetric vacuum black holes", l.21–22). The charged reduction is S5's | "... sector by sector [1], extending their reduction for vacuum black holes [2]" |
| K13 | S14 [6] | 112–114 | Table I is the *fundamental* ℓ = 2 frequency at each point ("l = 2 fundamental frequencies", l.142) | "computed the fundamental ℓ = 2 quasinormal mode ... and found it damped at every computed point" |
| K29, K77 | S43 [18] | 143–144, 767–768 | The earlier singly spinning separation covers one symmetry sector: "for perturbations with mψ = 0 and even parity under ψ → −ψ" (abstract, l.24–25). S43's v2 says the same: separated "for modes preserving the transverse-sphere symmetry" (p.1) | "after a symmetry sector of the singly spinning case" |
| K42 | S47 [29] | 171–172 | S47 certifies the residual of one machine-learned candidate: "It is not an existence or uniqueness theorem for an exact nearby water wave" (l.738–739, p.12; also l.840–844, p.14). v0.4's "certified computation" was right, and v0.8's "computer-assisted proofs" says more | keep "proofs" for S46 [28], and say for [29]: "to certify the residual of a neural-network approximation of a nonlinear water wave" |

For K29, the singly spinning work is Santos, arXiv:2610.18956. It is S43's [12] and is not in v0.8's references. My
S36 screen returned it, but I did not take it as a source (`stability_relwork_2026-11-18/screen/triage.tsv`).

**Notes, all OK:**
- **Page anchors are printed page numbers.** In three sources they differ from the PDF page index: S41 (p.5 is PDF
  p.9, and p.7 is PDF p.11), S51 (p.6 is PDF p.7) and S52 (pp.43–44 are PDF pp.45–46). Every anchor is right in the
  printed numbering. BHM-189's "l.2476 is the page number" for S52 refers to the footer of printed page 43, so the
  passage, l.2477–2479, opens page 44.
- **K15, S32 [8] against S14 [6].** Both tables give 12 points: D = 7 at q = 0, 0.1, …, 0.9 and 0.98, and D = 6 at
  0.98.
  - At 7 of the 12, S32's values rounded to three decimals equal S14's. At the other 5 they differ by one unit in the
    third decimal. The largest difference is 0.0015: at D = 7, q = 0.98, S14 gives 1.107 − 0.380i and S32 gives
    1.105518 − 0.379003i.
  - So "match" holds to about 0.1%; "agree to within 0.002" would be exact.
  - My check of 2026-11-10 (Q5) found S32 disagreeing with a different paper, Konoplya–Zhidenko hep-th/0703231 (S8).
    S14 agrees with S32.
- **K43 and K63, S33 [30] eq. (4.14)**, read on the rendered page (PDF p.8, printed p.7).
  - With r_H = M at q = 1, the D = 4 form of u_0 is Ψ2 times a constant, and Ψ2 ~ r^(−ℓ) decays.
  - Ψ2 solves Kodama–Ishibashi's equation with V_S− exactly at D = 4, q = 1 (`tools/zm_check.py`, sympy).
  - S33's own printed V2, eq. (4.18), is the negative of that potential: it would tend to −ℓ(ℓ+1)/r² at large r. That
    is a sign slip in S33. v0.8 cites only (4.14).
- **K57 and K81, S5 [1] eq. (5.63b)**, read on the rendered page 25, since the text layer loses the brackets.
  - The first two lines are [ … ] y, which vanishes at λ = 0.
  - The rest, at K = 1, is Appendix A's display, term by term.
- **K58, S6 [3] pp.5, 13.** S6 gives the direction the text uses: positive on C0∞, so the unique self-adjoint extension
  is positive, for λ ≥ 0. The H² domain and "if and only if" are standard facts, not S6's.
- **25 citations have no anchor.** All are OK. Most are attributions, or repeat an anchored citation nearby. For four,
  an anchor would help, and the ledger gives the supporting lines:
  - K02, S6: abstract and p.13;
  - K14, S26: abstract;
  - K15, S32: Tables 5 and 7;
  - K76, S31: abstract.

## Reference entries

Every entry matches the records I fetched today: authors, title and identifier. Every cited arXiv version is the latest
except one, and each Zenodo DOI is that record's latest version.
- **S43 [18]: a v2 was posted on 19 November** (API: updated 2026-11-19T18:59:27Z). The entry's v1 is right as cited.
  v2's abstract is new, though, and no longer mentions the singly spinning limit. That remark is now in v2's
  introduction (p.1). Either keep v1 deliberately, or cite v2 and move K29's anchor.
- **S31 [34]:** the v3 PDF's title page reads "On the Aretakis Instability of Extremal Black Branes", as the entry does.
  arXiv's metadata title for v3, which listings show, is "You've got a Freund--Rubin in Me: The Aretakis Instability of
  Extremal Black Branes".
- **S49 [14] and S51 [10]:** as BHM-189 R13 and R15. "|Q| < M" is on S49's title page but not in its metadata, and S51's
  original title has no umlaut. S26 [7] is spelled "Nordstrøm" in the original; v0.8 writes "Nordström".
- **S37 [20]:** R01's fix is taken (version DOI 24146364), and v1 is still the latest version.
- **Journal versions** exist for nine entries, if you want them:
  - S5, Prog. Theor. Phys. 111 (2004) 29;
  - S23, Prog. Theor. Phys. 110 (2003) 701;
  - S6, Prog. Theor. Phys. 110 (2003) 901;
  - S14, Phys. Rev. Lett. 103 (2009) 161101;
  - S26, Phys. Rev. D 89 (2014) 024011;
  - S49, Commun. Math. Phys. 380 (2020) 1313;
  - S57, Commun. Math. Phys. 368 (2019) 143;
  - S54, Commun. Math. Phys. 385 (2021) 1395;
  - S55, Commun. Math. Phys. 378 (2020) 705.

  These come from arXiv's journal-ref fields; the ledger gives each one as arXiv prints it.

## Citations treated by comparison

For 40 rows, an earlier check of mine covered the same claim at the same passage: BHM-189 (by its row C01–C38), or my
check of 2026-10-22 (K14, 1309.7667's abstract). For each of them:
- I compared v0.8's wording with the wording checked then;
- I mapped the page anchor to the lines checked then;
- I re-ran the quote check.

Where the wording had changed (K41), I judged the new wording at the source. The other 43 rows were read at the source.

The 40 rows, as row, key, [number]:
- K05 S28 [4], K06 S48 [5], K07 S28 [4], K09 S28 [4], K10 S48 [5], K12 S48 [5];
- K14 S26 [7];
- K17 S52 [9], K18 S52 [9], K19 S51 [10];
- K22 S53 [13], K23 S49 [14], K24 S50 [15], K25 S40 [16], K26 S41 [17], K28 S41 [17];
- K30 S42 [19], K31 S37 [20], K32 S37 [20], K33 S37 [20], K34 S39 [21], K35 S38 [22];
- K36 S58 [23], K37 S59 [24], K38 S57 [25], K39 S56 [26], K40 S44 [27], K41 S46 [28];
- K45 S28 [4], K46 S48 [5], K47 S37 [20];
- K68 S52 [9], K69 S51 [10], K71 S51 [10], K72 S45 [31], K73 S58 [23];
- K74 S54 [32], K75 S55 [33], K78 S42 [19], K79 S59 [24].

## The sources and the records

- **The PDFs and text layers** (`ledger/source_hashes.tsv`):
  - All 34 PDFs and their text layers match SOURCES.md's hashes. I found each by hash, so each is the copy SOURCES.md
    names.
  - 27 are byte-identical to my own earlier fetches. The other 7 (S41–S47) are the ones you fetched; BHM-189 found
    fresh fetches of them byte-identical to yours.
  - A fresh `pdftotext -layout` (poppler 0.86.1) of each PDF reproduces each `paper.txt` byte for byte. So the line
    numbers in the ledger refer to the PDFs as stated.
- **Requests:** 5 on 2026-11-23, all logged with status, size and SHA-256 in `cache/records/fetch_log.tsv`, and all
  HTTP 200:
  - one arXiv API request listing the 31 arXiv identifiers, without versions, so that it returns each latest version;
  - the three Zenodo records;
  - the PDF of S43 v2, by identifier (SHA-256 ae6aa9e9b6a452f6…; not included).

  Each was made by identifier only, with the screen's generic User-Agent, 4 s apart. No search was run.

## Files

- `README.md`: this file.
- `ledger/`:
  - `ledger.md`, `ledger.tsv`: the ledger;
  - `citations.tsv`: the 83 citations as extracted;
  - `numbers.tsv`: keys, the PDF's numbers and its reference list;
  - `bibcheck.tsv`, `source_hashes.tsv`.
- `cache/records/`: the fetched records and the fetch log.
- `tools/`:
  - `sources.tsv`;
  - `sources.py`, `citations.py`, `show.py`, `fetch_records.py`, `bibcheck.py`, `hashes.py`;
  - `spec.py`, which holds the verdicts and notes by hand;
  - `build.py`, which extracts the passages and checks the quotes;
  - `zm_check.py`, which needs sympy.

  Run each as `python3 -B -I tools/<name>.py <this folder>`, except `zm_check.py`, which takes no argument. `show.py`
  prints any source's page or lines with page numbers.
- `SHA256SUMS`.
