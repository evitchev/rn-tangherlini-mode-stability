# AUDIT_notes.md — working notes for the v0.4 delta audit (written before AUDIT.md)

Session-R secondary Fable, 2026-11-18. Raw outputs are in `logs/`; these notes say what was compared and how.
Repository paths are relative to `[repository]/` (HEAD de214de at the time of reading).

## N1. Item 1 — §4.7 against the RESULT lines and the records

Method: for each of the 14 rows I read the cited RESULT lines (`logs/item1_result_lines.log`, with context) and the named record
fields with `jq` (`logs/item1_records.log`; HD-S leaf sums in `logs/item1_hds_leaves.log`). Degrees of stored polynomials were
re-derived from the keys of their coefficient dictionaries (max exponent per variable); counts were summed by `jq`, not copied.
Nothing was computed beyond reading JSON and adding integers; nothing ran on host-1/005.

Checks that needed arithmetic of my own:
- E1 count: D = 7: ℓ = 4…10 (7), D = 8: 5…10 (6), D = 9: 6…11 (6), D = 10: 6…13 (8), D = 11: 7…14 (8); 7 + 6 + 6 + 8 + 8 = 35. The
  record's `E1` array has 35 entries.
- E2 leaves: 7 + 1 + 1 + 1 + 3 + 1 + 1 + 3 + 1 + 1 + 7 + 1 + 1 = 29 (RESULT l.29–41; record sum 29).
- HD-S boxes 9 + 5 + 22 + 10 + 3 + 22 + 11 + 9 + 2 + 22 + 21 + 11 + 8 + 22 + 23 + 13 + 11 + 7 = 231; N-leaves summed over the 18 records
  = 919, and per band equal to RESULT l.26–43 (27, 17, 84, 30, 11, 80, 33, 27, 10, 100, 63, 63, 24, 174, 75, 39, 39, 23).
- HD-X-E parts: n − 1 … ℓ₀ gives 7 + 6 + 6 + 7 + 7 = 33; the record has 33 parts, 5 with the `F(1 − s, μ) = μK + sG` splitting
  (ℓ = n − 1 at each D) and 28 without.
- "Leaf" semantics: `code/onset/bernstein.py`'s `prove_sign` is the counter behind every `bernstein_leaves` / "N > 0" count (p3's
  `scert.py` l.217–220 and hd's `scert.py` l.192–194 pass the same `stats` dict); see `logs/item1_p3_box_count.log` for what it counts.

## N2. Item 2 — the novelty claim

- (a) The claim (§1 l.130–132) is "relative to these sources"; it follows from the first "not found" item (l.124: no proof at any
  D ≥ 6, analytic or computer-assisted; relwork ledger q1 l.113–114) plus Theorem 1 (§3 l.171–177: A ≥ 0, hence no mode e^{κt}φ,
  κ > 0, φ ∈ L²), which is what §2 l.155–158 calls mode stability. Searched for stronger wording: abstract l.26–43, §1 l.107–132,
  §7 l.398–426. "We settle the open case" (l.107) is the same claim; "We do not claim a first computer-assisted proof of mode
  stability for a black hole" (l.131–132) is the right disclaimer against S37.
- (b) Each "not found" item against §1's own citations: item 1 vs S40 (Kerr–Newman, D = 4, analytic, real axis only), S49 (D = 4),
  S50 (neutral): no contradiction. Item 2 vs S37 (Kerr–de Sitter: neither charged nor higher-D), S39 (extremal Kerr, a count in a
  bounded domain), S58 (a test scalar field), S59 (an instability): no contradiction. Item 3 vs S53 (numerical S), S37 (Bernstein
  certificates, but not an S-deformation — relwork q3 l.64–65): no contradiction. Item 4 ("a closed form of the zero-energy solution
  at extremality for D ≥ 5"): the extremal-case screen itself records closed forms at extremality for the tensor and vector types
  (zmode q1 l.5–6, l.39–47: Pereñiguez–Cardoso) and for test fields; the item is true only for the scalar-type master equation, which
  it does not name. Fix: name the sector.
- (c) "What was searched" vs the two READMEs and `ledger/searches.md` (`logs/item2_screens.log`): services (relwork searches.md
  l.5–15), seeds and positive controls (l.63–64, 68–69; README l.164–166), 88 and 52 sources (relwork README l.162–163; zmode README
  l.19), not searched (relwork searches.md l.77–92: Google Scholar, ADS, MathSciNet, Semantic Scholar, OpenAlex deep paging, full texts
  of non-INSPIRE papers beyond those fetched, other repositories except through OpenAlex; l.74: arXiv math full texts). Dates: the
  relwork screen's queries are of 2026-11-17/18 (README l.6, l.133, l.147–148); the extremal screen's INSPIRE sessions were
  2026-10-26 and 2026-11-10 (zmode searches.md l.4), so "in November 2026" holds for S36 only. The "last query on 18 November, UTC"
  is consistent with the README's timestamps (predictions registered before searching at 03:26Z and resolved at 04:38Z on 11-18;
  the arXiv probe of 11-18); the per-query timestamps are in `cache/searches/search_log.tsv`, outside the brief's allow-list, so
  not read.

## N3. Item 3 — statements about the paper's own mathematics

Compared with §§2–6 (`DRAFT_v0.4.md` l.135–396): §7 l.412 (L² modes, κ > 0) with §2 l.155–158 and §3 l.177; §7 l.425 (the step to
A_{ℓ,1} ≥ 0) with §4.6 l.257–258 and Lemma 1 l.197–200; §7 l.424 (real potential) with §2 l.146–148, 152; §1 l.52–53 (negative
regions) with §4.5 l.239–242; §1 l.107–112 with §3, §4.2 l.215–221, §6 l.380–395; the abstract l.42–43 with §4.1 l.203–205, §3 l.179
and §6 l.390–392. Labels: "certified", "proved (pencil; audited n×)", "machine-checked", "numerical", "cited" as RULES.md A3 l.26–34.

## N4. Item 4 — anchored sentences about other works

Every anchor was read in the listed text layer (`logs/item4_anchors.log`; all 25 layers match the brief's hash prefixes,
`logs/hashes.log`). Two sentences say more than their anchor: S43 (the anchor itself credits Santos for the singly spinning case,
l.24–25) and S56 (l.6–14 does not mention computer assistance; l.99–103 does). S14, S26, S32, S9, S27, S33, S6, S23 and S31 are cited
without line anchors and are not in the brief's layer list; not checked.

## N5. The accepted-leaf conversion, by hand (for AUDIT.md §1.2)

`prove_sign` counts every box popped from its stack and bisects a rejected box into two, so each starting box gives a full binary
tree with E = 2L − 1 examined boxes for L accepted leaves, i.e. L = (E + 1)/2.
- T3: E = 3 per μ-box → L = 2; 8 μ-boxes → 16 accepted leaves (24 examined).
- E2: E = 7, 1, 1, 1, 3, 1, 1, 3, 1, 1, 7, 1, 1 → L = 4, 1, 1, 1, 2, 1, 1, 2, 1, 1, 4, 1, 1; sum 4 + 1 + 1 + 1 + 2 + 1 + 1 + 2 + 1 + 1 + 4 + 1 + 1 = 21
  (29 examined).
- HD-S: 231 starting boxes, 919 examined in all → L = (919 + 231)/2 = 1150/2 = 575 accepted leaves.
- HD-X-S chart O: E = 3 → L = 2 (D = 8 ℓ = 3); E = 5 → L = 3 (D = 10 ℓ = 4).
(The same three sums were also printed by one python3 one-liner on host-0 at 12:41 EST, against RULES.md B3; disclosed in AUDIT.md §8.)
