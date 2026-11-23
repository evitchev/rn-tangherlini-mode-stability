# bh-modes delta audit: draft v0.4, §§1, 4.7 and 7 — session-R secondary Fable

*2026-11-18. Brief: `paper/stability/briefs/BRIEF_fable_2026-11-18_v04_delta.md` (bh-modes repository), sha256
`646e127de8cc613ba9b876cb92bbb67ef5da95cd791d7223ae62b47cc01524af`, 131 lines, computed here at 12:22:40 EST with `sha256sum`
and equal to the session-R lead's cover; `SEALED.sha256` not opened. Object: the frozen draft
`paper/stability/versions/DRAFT_v0.4.md`, sha256 `28af203ac2910320c7466878fbbf8120b5a5e59bb73610d6f3006064357e8864` (517 lines);
v0.3 `7380111ba5e3f8ae948799caf4f3f28f6f481e0f87bfea2b223e23eaac5a6f17` (358 lines); `git diff --no-index` v0.3 → v0.4: 9 hunks,
+186/−27 lines (`logs/diff_v03_v04.log`). A 0444 copy of the brief is beside this file. Reading only: `cat`/`sed`/`awk`/`grep`, `jq`
on the records, `sha256sum`, and file writing inside this folder, all on host-0; one deviation is disclosed in §8. Nothing outside the
brief's allow-list was opened: no `RELATED_WORK.md`, `LITERATURE_ITEMS.md`, `AUDIT_TABLE.md`, `SOURCES.md`, `REGISTRY.md`, `TODO.md`,
`README.md`, `outbox/`, `SEALED.sha256`, no `*-lead-check/`, no `audits/` or `reviews/` folder but my own three, nothing under
`[deliveries]/` but this folder, no `[kimi-folder]/`. Session-L's citation check of v0.4 was not seen. Items 1 and 2 were done
first. The 25 text layers match the brief's hash prefixes and the 24 allow-list paths exist (`logs/hashes.log`). Working notes:
`AUDIT_notes.md` (N1–N4), written before this file; every check's output is in `logs/`.*

Repository paths below are relative to `[repository]/` (HEAD `de214de` while reading). "l." in the draft means a
line of `DRAFT_v0.4.md`; in a source, a line of its text layer as the brief lists it.

## 0. Verdicts

| Item | Object | Verdict |
|---|---|---|
| 1 | §4.7, every count and degree against its RESULT line and record field | **GAP-MINOR** — all 14 rows equal their sources; but the quantity the draft defines as a "leaf" (l.277–278) is not what the records' counts measure (§1.2). One sentence fixes it, or five numbers do |
| 2 | The novelty claim (§1 l.114–132) | **GAP-MINOR** — (a) the claim follows and nothing claims more; (b) one "not found" item needs its sector named; (c) "What was searched" is supported, with one date to widen |
| 3 | Statements in §§1 and 7 about the paper's own mathematics | **SOUND** — each consistent with §§2–6 and labelled as RULES.md A3 asks; one optional wording |
| 4 | Statements in §§1 and 7 about other works, at their anchors | **GAP-MINOR** — 28 of the 30 anchored or listed statements are supported as written; two say more than their anchor (S43, S56), each a one-clause or one-anchor fix |

No item is GAP-MAJOR or ERROR; no stop condition was reached. The fixes are F1.1, F2.1 (required for the text to say what the records
and the screens say) and F2.2–F2.4, F3.1, F4.1–F4.4 (wording and anchors, the operator's call).

## 1. Item 1 — §4.7 against the records: GAP-MINOR

### 1.1 The table, row by row

Each row of §4.7 (l.283–296) against the cited RESULT lines (`logs/item1_result_lines.log`) and the record fields read with `jq`
(`logs/item1_records.log`, `logs/item1_hds_leaves.log`). "=" means the draft's value equals the source's.

| Row (draft l.) | Draft's value | Source's value | Source | Match |
|---|---|---|---|---|
| O1, O2 (l.283) | F(t, μ) degree (4, 104), integer coefficients | (4, 104), integer coefficients | `results/onset/RESULT.md` l.10; record `F_degrees` [4, 104], `g_degree` 104 | = |
| | O1: one root, isolating interval width 5.9·10⁻⁴⁶ | one root in [0, 1], simple; width 5.9·10⁻⁴⁶ | RESULT l.15; record `checks.O1.detail` ("roots of g in [0,1]: 1; isolating interval width 5.9e-46") | = |
| | O2: three regions | three regions, one Bernstein box each | RESULT l.16; record `checks.O2.detail` (three named boxes, 1 each) | = |
| T3 (l.284) | N > 0 for q ∈ [0.97277, 0.99019] | inward [0.97277, 0.99019] (RESULT l.18's 0.99020 corrected) | `results/p3/RESULT.md` l.18; `RESULT_ADDENDUM_1.md` l.16 | = |
| | design P of degree (28, 4) | max exponents of `.result.boxes_mu[].P` keys: (28, 4) in all 8 boxes | record T3 | = |
| | N of degree (68, 16) | `deg_z` 68, `deg_mu` 16 in all 8 boxes | RESULT l.18; record | = |
| | 8 μ-boxes, 3 leaves each | 8 μ-boxes; "N > 0": 3 per box ("3 Bernstein boxes", RESULT) | RESULT l.18; record `.result.boxes_mu[].bernstein` | = as a count; see §1.2 |
| P1 Part I (l.285) | F of degree (4, 4); 8 values of ℓ, one leaf each (first node) | `F_degrees` [4, 4] and `bernstein_leaves.F` 1 for ℓ = 3…10 | `results/a1/RESULT.md` l.14–15; record `part1[]` | = |
| Lemma U(4) (l.286) | m⁻³U₋ ≥ 959747/17496; Neg: 9 monomials, one corner | 959747/17496; `Neg` has 9 keys; corner (1/12, 1/5, 2), Neg = 159997/17496 | RESULT l.35–39; record `part2` | = |
| A2-E (l.287) | F (4, 4); at ℓ = 3, F = μK + sG; 8 parts, one leaf each (K and G one each) | `F_degrees` [4, 4] ×8; ℓ = 3 split with K 1, G 1; ℓ = 4…10 F 1 | `results/a2/elementary/RESULT.md` l.16–25; record `.parts` | = |
| A2-S (l.288) | pole term + p₀ of degree 12; NL (38, 12) on O, O′; (38, 48) on T; (48, 12) on C; 4 charts, one leaf each | `design.degree` 12; `degrees` NL [38, 12], T [38, 48], C [48, 12]; POS-O, O′, T, C leaves 1 | `results/a2/s/RESULT.md` l.12–24; record | = |
| HD-E E1 (l.289) | 35 (D, ℓ); F (4, 4); 35 boxes, one leaf each | `E1` has 35 entries (7 + 6 + 6 + 8 + 8), `F_degrees` [4, 4], `bernstein_leaves` 1 each | `results/hd/elementary/RESULT.md` l.14–23; record | = |
| HD-E E2 (l.290) | 13 bands; F (4, 4); 29 leaves in all | 13 entries, [4, 4]; leaves 7, 1, 1, 1, 3, 1, 1, 3, 1, 1, 7, 1, 1, sum 29 | RESULT l.27–41; record `E2` | = as a count; see §1.2 |
| HD-E E3 (l.291) | Lemma U(n), n = 5–9, ℓ > ℓ₀; Neg: 10 monomials, one corner each | `E3`: n = 5…9, `l0` 10, 10, 11, 13, 14, `Neg_monomials` 10 each, bounds 399917/10368 … 19870/6561, one corner (ε̄, κ_max, x_max) each | `RESULT_ADDENDUM_1.md` l.23–29; record `E3[]` | = |
| HD-S (l.292) | 18 bands; designs of degree 16–32 in z or ζ, 4 in μ; N·L from (48, 16) to (96, 16); 231 μ-boxes, 919 leaves | design degrees 16…32, variable z or ζ; P's μ-exponent max 4 in every box of every band; (deg_z, deg_mu) per band from (48, 16) to (96, 16); boxes 231; "N > 0" counts sum 919, per band as RESULT l.26–43 | `results/hd/s/RESULT.md` l.24–45; the 18 records' `.boxes[]` | = as counts; see §1.2 |
| HD-X-E (l.293) | 33 parts (5 split, 28 strict), one leaf each; F (4, 4) | 33 parts; 5 with the μK + sG splitting (ℓ = n − 1 at D = 7…11), 28 without; `F_degrees` [4, 4]; leaves 1 (F, or K and G) | `results/hdx/elementary/RESULT.md` l.13; record `.parts` | = |
| HD-X-S (l.294) | 11 bands; designs 12–20; NL from (42, 12) to (70, 12); 4 charts per band, one leaf each, except O: 3 at D = 8 ℓ = 3 and 5 at D = 10 ℓ = 4 | `design.degree` 12, 16, 12, 12, 12, 20, 12, 12, 16, 12, 12; `degrees.NL` (42, 12) … (70, 12); `bernstein_leaves` POS-O 3 at 8-3, 5 at 10-4, all else 1 | `results/hdx/s/RESULT.md` l.14–26; the 11 `*-none` records | = as counts; see §1.2 |
| HD-X-2 (l.295) | 9 bands; closed-form design; NL from (24, 14) to (48, 14); 4 charts per band, one leaf each | `degrees.NL` [24, 14], [30, 14], [36, 14] ×2, [42, 14] ×2, [48, 14] ×3; POS-O, O′, T, C leaves 1; `q(MU1)^2` as RESULT l.20–28 | `results/hdx/critical/RESULT.md` l.13–28; the 9 `none` records | = |
| Z (l.296) | Theorem 2's identities and u₀ > 0, n = 4–9 and symbolic n; exact identities | claim jobs n = 4…9 VERIFIED each; `zero_mode-N-none` VERIFIED; n = 2, 3 information | `results/extremal/RESULT.md` l.11–20; records | = |

Also checked: §4.5's note on q_* (l.239–240): q_* = 0.9730564367… (onset RESULT l.15; record `q_star_decimal`), so "≈ 0.97306" and the
inward "0.97305" of §5.1 l.314 are both right. The source column's citations all point to the lines or fields that hold the values.

### 1.2 The one gap: what the records' "leaves" count

§4.7 l.277–278 defines: *A "leaf" is a box on which every Bernstein coefficient is positive, after any subdivision.* The counts in the
"Boxes and leaves" column that exceed 1 (T3 "3 leaves each", E2 "29 leaves", HD-S "919 leaves", HD-X-S "3" and "5") are copied
correctly from the records' `bernstein_leaves` fields and the "N > 0" entries, and the RESULT files call those fields "leaves"
(`results/hd/s/RESULT.md` l.21, `results/hd/elementary/RESULT.md` l.27). But the routine that produces every such count,
`code/onset/bernstein.py` `prove_sign` (l.69–97; `logs/item1_p3_box_count.log`), increments `stats[label]` once for every box it pops
from its stack (l.76–79), *before* the acceptance test `lo > 0` (l.80), and bisects a rejected box into two (l.93, l.96). So the count
is the number of boxes examined, internal nodes included; the accepted leaves — the boxes of the draft's definition — number
(count + 1)/2 per starting box. p3's, hd's, hdx's, a1's and a2's certificates all pass their `stats` to this routine (`code/p3/scert.py`
l.217–220, `code/hd/scert.py` l.192–194, `code/hd/elementary.py` l.155–159, `code/hdx/scert.py` l.313, `code/a1/p1.py` l.163). Where the
count is 1 the two readings agree, so P1, A2-E, A2-S, E1, HD-X-E, HD-X-2 and O2 are unaffected.

Under the draft's own definition the right values are (`logs/item1_p3_box_count.log`, hand arithmetic in `AUDIT_notes.md` N1):

| Row | Draft (= the records' count of boxes examined) | Accepted leaves, (count + 1)/2 per starting box |
|---|---|---|
| T3 | 3 per μ-box (24 in all) | 2 per μ-box (16 in all); the T3 record has no z-pieces, so each count is one bisection tree |
| HD-E E2 | 29 in all (7, 1, 1, 1, 3, 1, 1, 3, 1, 1, 7, 1, 1) | 21 in all (4, 1, 1, 1, 2, 1, 1, 2, 1, 1, 4, 1, 1) |
| HD-S | 919 over 231 μ-boxes | 575 = (919 + 231)/2 (no fallback pieces: RESULT l.19; no such field in the records) |
| HD-X-S, chart O | 3 at D = 8 ℓ = 3; 5 at D = 10 ℓ = 4 | 2 and 3 |

**F1.1 (one of two forms).** Either (a) keep the numbers and change the definition, l.277–278: *"Boxes" counts every box the adaptive
bisection examined, including those it then split, as the records' `bernstein_leaves` fields do; a certificate accepts a box when all
its Bernstein coefficients are positive, and the accepted boxes number (count + 1)/2 per starting box* — and write "boxes" for "leaves"
in the five entries; or (b) keep the definition and replace the five numbers by the accepted-leaf values above. (a) is the smaller
change and keeps the table equal to the records. The RESULT files' own column names ("Bernstein leaves", "leaves") carry the same
misnomer; that is a note for the bh-modes lead, not a defect of any certificate: the sign proofs are unaffected.

### 1.3 Remarks (no verdict depends on them)

- R1.1 For A2-S the row gives every chart's degree; for HD-X-S and HD-X-2 it gives NL (the O/O′ chart) only. The records also hold
  T and C: HD-X-S T from (42, 52) to (70, 80) and C from (52, 12) to (80, 12); HD-X-2 M (24, 13) … (48, 13), T (24, 36) … (48, 60), K
  (36, 13) … (60, 13). Adding them would make the three singular-design rows parallel.
- R1.2 l.284's "3 leaves each" cites `.result.boxes_mu[].P` for P's degree; the count itself is in `.result.boxes_mu[].bernstein`.

## 2. Item 2 — the novelty claim: GAP-MINOR

**(a) Does the claim follow, and does the draft claim more?** The claim (l.130–131): *Relative to these sources, Theorem 1 is the first
proof of mode stability of this sector for D = 6–11, for every ℓ ≥ 2 and every charge up to extremality.* It follows from the first
"not found" item (l.124: no proof, analytic or computer-assisted, for the charged scalar-type sector at any D ≥ 6; the screen's own
statement is relwork `ledger/q1_prior_results.md` l.113–114, "for any D ≥ 6 … small charge, single multipoles and near extremality"
included) together with Theorem 1 as §3 states it (l.171–177: A_{ℓ,q} ≥ 0 for D = 6–11, ℓ ≥ 2, q ∈ (0, 1], hence no mode e^{κt}φ with
κ > 0 and φ ∈ L²), which is what §2 l.155–158 calls a mode and what "mode stability" means in the sources' tables (S5 Table I, S28
Table 1: "D = 4, 5 OK / D ≥ 6 ?" in the scalar, Q ≠ 0 cell). The claim is narrower than the "not found" (D = 6–11 against any D ≥ 6)
and carries its qualifier. Nothing claims more: the abstract (l.26–43) states what Kodama and Ishibashi proved and left open and what
is shown here; §1 l.107 "We settle the open case for D = 6–11" is the same statement; l.131–132 disclaims "a first computer-assisted
proof of mode stability for a black hole", as S37 requires; §7 (l.398–426) makes no priority claim. SOUND.

**(b) Is each "not found" item consistent with what §1 cites?** Items 1–3, yes (`AUDIT_notes.md` N2): S40 is analytic, D = 4 and on
the real axis only; S49 and S50 are D = 4 or neutral; S37 is Kerr–de Sitter (neither charged nor higher-dimensional) and its Bernstein
certificates are not an S-deformation; S39 counts modes in a bounded domain of extremal Kerr; S58 treats a test scalar field; S59
certifies an instability. **Item 4 (l.128), "a closed form of the zero-energy solution at extremality for D ≥ 5", names no sector.**
The extremal-case screen that §1 relies on (S25) records closed-form extremal static solutions for the tensor and vector types
(Pereñiguez–Cardoso; `zmode-litcheck-2026-11-10/ledger/q1_static_solutions.md` l.5–6, l.39–47) and for test fields, and states its
negative for the scalar-type master equations only (l.3–4). As written the item contradicts the screen it rests on; in the paper's
context it is true. **F2.1:** write *"a closed form of the zero-energy solution of the scalar-type master equation at extremality for
D ≥ 5"* (or "of V_S−"). GAP-MINOR.

**(c) Is "What was searched" (l.115–122) supported by the two screens' own accounts?** Yes, line by line (`logs/item2_screens.log`):
the five services and what was searched in each (relwork `ledger/searches.md` l.5–15; the arXiv API "abstracts and titles, all
categories, math included", l.7); the ten seeds with complete OpenAlex citer sets, each found again by other queries (l.63–64, l.68–69;
README l.164–166); 88 sources read at their anchors in the screen for this paper and 52 in the extremal-case screen (relwork README
l.162–163; zmode README l.19); the "Not searched" list (relwork `searches.md` l.77–92: Google Scholar, ADS, MathSciNet, Semantic
Scholar, other repositories except through OpenAlex; l.74: "arXiv math full texts are not full-text searched by any service used").
Three points, none a contradiction:
- **F2.2 (dates).** "in November 2026 (the last query on 18 November, UTC)" holds for the screen for this paper (its README is dated
  2026-11-18 and its predictions were registered before searching at 03:26Z and resolved at 04:38Z on 2026-11-18, l.133, l.147–148).
  The extremal-case screen's INSPIRE sessions were 2026-10-26 and 2026-11-10 (zmode `ledger/searches.md` l.4). If the sentence is
  meant to cover both screens, write "in October and November 2026". The per-query timestamps are in `cache/searches/search_log.tsv`,
  outside the brief's allow-list; not read.
- **F2.3 (optional).** The ledger's own not-searched phrase is wider than the draft's "the full texts of arXiv's mathematics papers":
  "Full texts of non-INSPIRE papers beyond those fetched" (l.87), and it also lists OpenAlex deep paging with a key (l.82–86). The
  extremal-case screen adds books, theses and proceedings not on INSPIRE, and non-English literature (zmode `searches.md`
  l.138–142). A referee asking "what about books?" is answered by adding one clause.
- **F2.4 (optional).** l.119 "We read the relevant passages of the sources they returned: 88 …, and 52 …" reads as if the searches
  returned 88 and 52 sources; they returned 4,099 and 451 unique records (relwork README l.161; zmode `searches.md` l.11), of which 88
  and 52 were fetched and read at their anchors. "of 88 of the sources they returned" says it.

## 3. Item 3 — statements about the paper's own mathematics: SOUND

Each statement against §§2–6 (`AUDIT_notes.md` N3):
- §7 l.412 *"Theorem 1 is a statement about L² modes with κ > 0 (§2)"*: §2 l.155–158 defines a mode as e^{κt}φ, κ > 0, 0 ≠ φ ∈ L²(ℝ, dr*),
  and Theorem 1 (l.177) excludes exactly those. Consistent; and l.419 "Theorem 1 says nothing about these" scopes it against the
  Gevrey, Teukolsky and Aretakis notions. Labelled *certified* with its pencil and Lean parts (l.171–172), as A3 asks.
- §7 l.425 *"The step to A_{ℓ,1} ≥ 0 uses only that u₀ is a positive zero-energy solution (§4.6)"*: §4.6 l.257–258 uses u₀ > 0 (so
  w = (log u₀)_{r*} is smooth), the zero-energy equation (V = w² + w′), and Lemma 1 with S = −w (l.197–200), on r* ∈ ℝ at q = 1 (§2
  l.151). Nothing else enters. Consistent.
- §7 l.424 *"Our method uses a Schrödinger operator with a real potential, which the static master equations provide [S5]"*: §2
  l.146–148, l.152 (V real, continuous, bounded; A = −d²/dr*² + V). Consistent.
- §1 l.52–53 (V_S− has negative regions, so its sign does not decide): §4.5 l.239–242 (the bands). Consistent.
- §1 l.107–112 (Theorems 1 and 2; fail-closed certificates in exact rational arithmetic, registered before running, with negative
  controls, re-run by an independent party): §3, §4.2 l.215–221, §6 l.380–395. Consistent. **F3.1 (optional):** §6 and RULES.md A4
  distinguish a *reproduction* (the lead's re-run) from a *second party* (independently written code); l.112 "re-run by an independent
  party" blurs them. "re-derived by a second party with independently written code (§6)" matches §6 l.390 and the abstract l.42–43.
- §1 l.72–73 ("Our extremal step follows that route, with a closed form"): §4.6 l.257–258 and Theorem 2. Consistent.
- §7 l.402–403 (the D = 12–20 screen) is labelled *numerical, information only*; l.404–405 calls the large-D statements "not a proof at
  any finite D"; nothing numerical in §§1 or 7 is called proved. "Proved" is used for Kodama–Ishibashi's and Giorgi's theorems and
  for this paper's pencil steps only. A3 is kept.

## 4. Item 4 — statements about other works, at their anchors: GAP-MINOR

One line per anchored sentence (`logs/item4_anchors.log`; the layers are the brief's, hash prefixes checked). "Supported" means the
sentence says no more than the source at that anchor.

| Draft (l.) | Source, anchor | Verdict |
|---|---|---|
| l.50 "[S5, Table I: "d ≥ 6?"; S28, Table 1]" | S5 l.1899–1912: scalar, Q ≠ 0, K = 1, λ = 0: "d = 4, 5 OK / d ≥ 6 ?"; S28 l.740–752: "D = 4, 5 OK / D ≥ 6 ?" | supported |
| l.50–52 quote | S48 l.2275–2276, verbatim | supported |
| l.57–59 S-deformation of D = 4 leaves a negative region for n > 2; "except for some special cases" | S28 eqs. (76)–(77) at l.707–711; l.762–767 ("for n > 2, ṼS− becomes negative near the horizon in general … We have not been able to prove the stability for n > 2 by this method, except for some special cases") | supported |
| l.60 a horizon-regular S cannot remove the negative region near extremality | S5 l.1884–1887 | supported |
| l.61–62 quote | S48 l.2406–2407, verbatim | supported |
| l.69–70 and §7 l.404 large-D decay at Λ = 0 | S52 l.2477–2479 (§5.1, the shape-fluctuation spectrum of the RN black hole: "all quasinormal modes with l ≥ 2 have negative imaginary components"); S51 l.327–330 (Λ → 0 reproduces the RN modes; "At the both limits, the perturbations are stable") | supported; S52's anchor covers the shape fluctuations (§5.1), S51's carries the general statement |
| l.74 Kimura–Tanaka, regular S numerically, coupled systems | S53 l.525–530 | supported |
| l.76–77 Giorgi, linear stability, every \|Q\| < M | S49 l.20–30 | supported |
| l.78–79 Hung–Keller–Wang quote; decay for D ≤ 6 | S50 l.26–29 ("six or fewer spacetime dimensions") | supported |
| l.80–81 Hintz, Kerr–Newman separated; mode stability on the real axis for the radial ODEs | S40 l.7–12 | supported |
| l.82–83 "as a black box" | S41 l.444–445 | supported |
| l.83–84 Kerr–de Sitter "remains an open problem except in the slow-rotation regime" | S41 l.538–541 | supported |
| l.85–86 and §7 l.421 "the gravitational perturbations of five-dimensional Myers–Perry were separated only recently [S43]" | S43 l.11–27: two unequal spins; l.24–25 "In the singly spinning limit, we recover Santos's angular operators and radial equation" (Santos 2026, l.1026) | **says more**: the anchor credits Santos for the singly spinning case. **F4.1:** "with two independent spins were separated only recently [S43, l.11–26], after the singly spinning case" (both places) |
| l.86–87 Price's law assuming real-axis mode stability, "has not been shown to hold yet"; §7 l.422 | S42 l.163–164, l.446–447 | supported |
| l.90–91 Padhi claims a computer-assisted proof; spin ±2 Teukolsky, no outgoing modes with Im σ ≥ 0 | S37 l.10–15 | supported |
| l.91–92 "The certificates are exact except one step" | S37 l.126–128 ("All are exact except C9, which uses floating-point arithmetic with rigorous error bounds") | supported; **F4.2 (optional, fairness):** add "with rigorous error bounds" |
| l.92–93 "No human expert has yet checked the argument" | S37 l.1338, verbatim | supported |
| l.94–95 Chen et al., exactly one QNM in one bounded domain, within a numerical survey | S39 l.138–141, l.1845–1848 | supported |
| l.96–97 Goldstein–Jejjala, computer-assisted existence proof, Einstein–Weyl | S38 l.19–33 | supported |
| l.98–100 S58: certified spectral gap, test scalar field, one RNdS black hole; §7 l.411 | S58 l.8–22 | supported |
| l.98–100 S59: certified linear instability, 7D Myers–Perry; §7 l.423 | S59 l.8–22 | supported |
| l.102 Choptuik's spacetime, computer-assisted existence proof | S57 l.9–18 | supported |
| l.103–104 "Mode stability has been proved with computer assistance for a self-similar wave map [S56, l.6–14]" | S56 l.6–14: "We give a rigorous proof for its mode stability" — no word on computer assistance there; l.99–103: rigorous error estimates for all approximations, "unrealistic to perform all our computations without the aid of some computer algebra system" | **says more than the anchor**; true of the paper. **F4.3:** anchor l.99–103 (or "with computer-algebra assistance [S56, l.99–103]") |
| l.103–104 Larson–Penston, with computer assistance | S44 l.16–21 ("rigorous computer-assisted techniques in the intermediate regime") | supported |
| l.105 "Certified computation is also in use in geometric analysis [S46]" (no anchor) | S46 abstract l.14–19 ("verified numerics") | supported; **F4.4 (optional):** anchor l.14–19 |
| l.105 "and, with a Lean layer, for water waves [S47]" (no anchor) | S47 l.38, l.44, l.101–106, l.157 (formal verification in Lean) | supported; optional anchor l.101–106 |
| §7 l.408–409 dS RN unstable above a critical charge at large D | S51 l.26–30 | supported |
| §7 l.410–411 semiclassical QNMs near the ultracold limit, test scalar | S45 l.18–27 | supported |
| §7 l.414–415 QNMs of extremal RN on Gevrey-regular spaces | S54 l.8–24 (l.14–15) | supported |
| §7 l.416 Teukolsky on extremal Kerr, mode stability proved | S55 l.15–26 | supported |

Not checked, outside the brief's layer list: S6, S9, S14, S23, S26, S27, S31, S32 and S33 (cited without line anchors: l.48–49, 65–68,
72, 129, 187, 400, 407, 417). Session-L's citation check covers their quotes and bibliographic data.

## 5. Overclaim watch (the brief's "also report")

- The claim of l.130–131 is hedged ("Relative to these sources") and scoped to the sector, D = 6–11 and ℓ ≥ 2; l.131–132 disclaims the
  general computer-assisted first. A referee would not read it as an overclaim once F2.1 names the sector in the "not found" list.
- l.91–93 on S37 is accurate quotation; with F4.2 it is also complete. Without it, "exact except one step" can be read as an
  unqualified weakness that the source itself qualifies.
- l.119's "88" and "52" (F2.4) could be read as the size of the search; the screens read 4,099 and 451 records by title.
- §4.7 and §7 contain no sentence I would read as an overclaim; §7's negative scoping (l.400, l.406, l.419, l.425–426) is careful.

## 6. Hypotheses assumed

1. The RESULT files, addenda and `runs/record/*/result.json` under `results/` are the sealed ones (`SEALED.sha256` not opened; the
   records' `archive_sha256` and commits not re-verified). Their values were read, not re-run.
2. The 25 text layers are faithful `pdftotext -layout` outputs of the fetched PDFs (their hash prefixes equal the brief's table; the
   PDFs were not opened), and the draft's "l." anchors refer to them.
3. The two screens' README.md and ledger/ files describe their searches truthfully; `cache/searches/` and `screen/` were not read.
4. `code/onset/bernstein.py` at HEAD `de214de` is the routine that wrote the records' counts (the records' recorded commits were not
   checked out). Its logic (count before accept; binary bisection) is what §1.2 rests on.
5. The draft's statements about second parties and audits (§5.4, §6, the labels of §3) rest on `AUDIT_TABLE.md`, which is barred;
   they were checked for internal consistency only.

## 7. Files and line ranges read, per item (`all` = the whole file)

- **All items:** `DRAFT_v0.4.md` all (517); `git diff --no-index` v0.3 → v0.4 (saved, not read line by line beyond §§1, 4.7, 7);
  `RULES.md` all (194); `CHARTER.md` §5 (l.101–122) and the headers; the brief all (131).
- **Item 1:** `results/onset/RESULT.md` l.1–24; `results/p3/RESULT.md` l.8–30, `RESULT_ADDENDUM_1.md` l.8–22; `results/a1/RESULT.md`
  l.8–45; `results/a2/elementary/RESULT.md` l.8–30; `results/a2/s/RESULT.md` l.6–30; `results/hd/elementary/RESULT.md` l.8–45,
  `RESULT_ADDENDUM_1.md` l.15–35; `results/hd/s/RESULT.md` l.18–50; `results/hdx/elementary/RESULT.md` l.6–20; `results/hdx/s/RESULT.md`
  l.8–32; `results/hdx/critical/RESULT.md` l.6–32; `results/extremal/RESULT.md` l.6–24. Records (by `jq`, fields named in
  `logs/item1_records.log`): onset `main`; p3 `T3`; a1 `main`; a2/elementary `none`; a2/s `none`; hd/elementary `main`; hd/s the 18
  band records; hdx/elementary `none`; hdx/s the 11 `*-none`; hdx/critical the 9 `D*l*/none`; extremal `zero_mode-{4..9,N}-none`
  (verdicts). Code: `code/onset/bernstein.py` l.60–100; `code/p3/scert.py` l.200–226; `code/hd/scert.py` l.180–200; `code/hd/elementary.py`
  l.140–160; grep lines of `code/hdx/*.py`, `code/a1/p1.py`, `code/a2/*.py` (`logs/item1_p3_box_count.log`).
- **Item 2:** `literature/stability-relwork-2026-11-18/README.md` all (208) and `ledger/searches.md` all (134), `ledger/q1_prior_results.md`
  (grep lines; l.111–116), `q3_s_deformation.md` (grep; l.87–91), `q4_computer_assisted.md` (grep; l.129–134), `q5_math_literature.md`
  (grep); `literature/zmode-litcheck-2026-11-10/README.md` all (96), `ledger/searches.md` all (145), `ledger/q1_static_solutions.md`
  (grep; l.1–16, l.39–47).
- **Item 3:** `DRAFT_v0.4.md` §§2–6 (l.135–396) against §1 and §7.
- **Item 4:** the anchored lines of the 25 text layers with 2–4 lines of context, as `logs/item4_anchors.log` lists them; grep lines of
  S43 (Santos), S47 (Lean), S52 (section headers), S56 (computer/rigorous).
- **My own earlier audit** (format only): `[deliveries]/fable_assembly_audit_2026-11-13/AUDIT.md` l.1–40, 307–330, 364–380,
  `SHA256SUMS`, `LEAD_CHECK.md` l.1–12.

## 8. Process and time

- Start 12:22:40 EST (hashes), folder created 12:24:15 EST (`logs/START_TIME.txt`); the allow-list and the draft read by 12:30; items 1
  and 2 first; `AUDIT_notes.md` written before this file; the end time is `STATE_LOG.md`'s last entry and the delivery message. Inside
  the two-hour box; no stop condition reached.
- **Deviation from RULES.md B3, disclosed:** at 12:41 EST one `python3 -c` one-liner ran on host-0 to add integers for §1.2 ((919 +
  231)/2, the E2 and T3 sums; `logs/item1_p3_box_count.log`). B3 sends every one-liner to host-1/005. The three sums are redone by hand
  in `AUDIT_notes.md` N1 and §1.2 does not depend on the run. Also, at 12:23 EST, before the brief was read, one `ssh host-1 'hostname;
  uptime'` probe checked the host's reachability; no job was run there.
- Otherwise reading only on host-0 (`cat`, `sed`, `awk`, `grep`, `jq`, `sha256sum`, `git rev-parse`, `git diff --no-index` to a file);
  no network beyond that probe; no external contact; nothing written outside this folder; no git operation that changes anything.
- Files here: `AUDIT.md` (this), `AUDIT_notes.md`, `BRIEF_fable_2026-11-18_v04_delta.md` (0444 copy, same sha256), `logs/`
  (START_TIME.txt, hashes.log, diff_v03_v04.log, item1_result_lines.log, item1_records.log, item1_hds_leaves.log,
  item1_p3_box_count.log, item2_screens.log, item4_anchors.log), `STATE.md`, `STATE_LOG.md`, `MESSAGES.md` (the last three evolve and
  are excluded from `SHA256SUMS`, which lists every other file and is written outside any listed subtree).
