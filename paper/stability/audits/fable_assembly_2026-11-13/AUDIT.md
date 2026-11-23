# bh-modes pencil audit: the assembly of Theorem 1 (draft v0.2, §5) — session-R secondary Fable

*2026-11-13. Brief: `paper/stability/briefs/BRIEF_fable_2026-11-13_assembly.md` (bh-modes repository), sha256
`b71e134939d07e65fa4051c8a900385f1ee04bb185d782477444583b6a21ad7f`, 101 lines, computed here at 12:05:40 EST with
`sha256sum` and equal to the session-R lead's value; `SEALED.sha256` not opened. Object: the frozen draft
`paper/stability/versions/DRAFT_v0.2.md`, sha256 `4441e48a3d487c70b618d94f8c65b40c67045916be491ac7d77992b9924e9bd0`,
323 lines, computed at the same time and equal to the lead's. A 0444 copy of the brief is beside this file. Pencil audit:
no computation was run anywhere (nothing on host-1 or host-2; on host-0 only reading, `jq`/`grep` on the records,
`sha256sum`, and writing inside this folder). Nothing outside the brief's allow-list was opened: no `audits/` folder
except my own two, no `reviews/` folder, no `REGISTRY.md`, `TODO.md`, `README.md`, `outbox/`, `SEALED.sha256`, nothing
under `paper/` but the frozen draft, nothing under `[deliveries]/` except this folder, no `[kimi-folder]/`. Kimi's
composition audits were not seen. Items 1–3 were done first. Seat time: 12:05:40 EST to the time in §10. The
comparisons and hand checks are in `AUDIT_notes.md` (N1–N8), written before this file.*

**Range ends were taken from the records, not from the draft.** The records are abbreviated as follows (all under the
bh-modes repository, `runs/record/` unless said): R-O2 = `results/onset/…/main/result.json`; R-T3 =
`results/p3/…/T3/result.json`; R-P1 = `results/a1/…/main/result.json`; R-A2E = `results/a2/elementary/…/none/result.json`;
R-A2S = `results/a2/s/…/none/result.json`; R-HDE = `results/hd/elementary/…/main/result.json`; R-HDS(D-ℓ) =
`results/hd/s/…/<D>-<ℓ>/result.json`; R-HDXE = `results/hdx/elementary/…/none/result.json`; R-HDXS(D-ℓ) =
`results/hdx/s/…/<D>-<ℓ>-none/result.json`; R-HDX2(Dℓ) = `results/hdx/critical/…/D<D>l<ℓ>/none/result.json`; R-Z(n) =
`results/extremal/…/zero_mode-<n>-none/result.json`. q(μ)² = 1 − w(μ)² with w = Bμ/A, A = (ℓ + n) + (ℓ − 1)μ²,
B = 2ℓ + n − 1 (param_n; onset.param at n = 4, equal by gate PARAM4); w increases on [0, 1] (gates O5/PARAM), so a
μ-box [a, b] is the q-interval [q(b), q(a)]. (99/100)² = 0.9801. Decimals below are mine, to 6–7 significant figures,
as sanity checks; every exact comparison is the record's gate field named, or an integer cross-multiplication done here.

## 0. Verdicts

| Item | Object | Verdict |
|---|---|---|
| 1 | D = 6 (§5.1): O2, T3, A2-S at ℓ = 2; P1 and A2-E at ℓ = 3–10; Lemma U at ℓ ≥ 11 cover (0, 1] | **SOUND** |
| 2 | D = 7–11, q ≤ 99/100 (§5.2): E1, E2, E3 and HD-S cover (0, 99/100] for every ℓ ≥ 2 | **SOUND** |
| 3 | D = 7–11, q ∈ [99/100, 1] (§5.3): HD-X-E, HD-X-S, HD-X-2, Lemma U(n) and Theorem 2 cover it for every ℓ ≥ 2 | **SOUND** |
| 4 | Each piece's route to A ≥ 0 (§5's conventions) | **SOUND** |
| 5 | Theorem 1 as §3 states it, and the corollary on L² modes | **SOUND** |

No item is GAP-MINOR, GAP-MAJOR or ERROR; no fix is required for the assembly's logic. §6 reports five places where a
number, decimal or range in §§3–5 (and §4, which the brief's "§§3–5" brackets) differs from the records' own corrected
values, and §7 gives the one-clause remarks. The verdicts are conditional on the certified pieces, which the brief makes
hypotheses (§8).

## 1. Item 1 — D = 6: SOUND

**ℓ = 2, three pieces** (N1). O2 gives U₋ ≥ 0 on [0, x_H(q)] for q ∈ [0, q_*] (results/onset/RESULT.md l.16), so
V ≥ 0 on (0, q_*]. T3 gives A ≥ 0 for μ ∈ [3/25, 1/5] through eight contiguous μ-boxes of width 1/100 (R-T3
`result.boxes_mu[0..7].mu`: [3/25, 13/100], …, [19/100, 1/5]), i.e. for q ∈ [q(1/5), q(3/25)] =
[√(21576/22801), √(31416/32041)] (re-derived: w(1/5) = 35/151, w(3/25) = 175/1253). A2-S gives N > 0 on (0, 1) for
μ ∈ [0, 1/8], i.e. q ∈ [q(1/8), 1] with q(1/8)² = 2961/3025 (re-derived: w(1/8) = 8/55). The two overlaps:
- q(1/5) < q_*: 21576/22801 = 0.94627428… against q_*² = 0.94683882904927334931… in the record's isolating interval of
  width ≤ 10⁻⁴⁵ (R-O2 `q_star_squared_interval`; μ_* = 0.198932… < 1/5 with w increasing). Exact, with a margin of
  5.6·10⁻⁴.
- q(1/8) < q(3/25): 2961·32041 = 94,873,401 < 3025·31416 = 95,033,400, so 2961/3025 < 31416/32041. Exact.
So (0, q_*] ∪ [q(1/5), q(3/25)] ∪ [q(1/8), 1] = (0, 1].

**How T3 is certified** (the brief's question). The p3 run of record (BHM-023, results/p3/RESULT.md l.8) carries the
registered verdict FAIL, because its must-pass known-answer gate G1 (D = 10, ℓ = 2, Q = 0) was rejected under design rule
1; T3, a stretch tier "reported either way", was VERIFIED in the same run (l.18), and RESULT.md l.22–26 states what is
certified: A_{2,q} ≥ 0 on all of T3. The rule-2 re-run (BHM-025, RULE2_RESULT.md l.10–13) passed G1, T1 and T2 and did
not re-run T3; PREREG_ADDENDUM_1.md l.47–49 registers that "the T1, T2 and T3 certificates of BHM-023 stand as verified;
a certificate's validity does not depend on how P was designed". My reading: this is right. T3's content is eight exact
Bernstein verifications of N > 0 for stored polynomials P(z, μ) (with L > 0 and Den > 0), each a proof on its own; G1's
failure was a completeness failure of design rule 1 at a different potential (it found no certificate for a true
statement), not an acceptance of a false one, and the soundness controls of the same run (NC-P1 planted bound state,
TD-P1, TD-P2, the KATs) all rejected as registered. A1's PREREG (BHM-047, §2 l.26–27) then used T3 explicitly, and T3 has
two second parties (Kimi, all six certificates; session-L's independent exact re-run of the eight boxes, BHM-056:
results/p3/RESULT_ADDENDUM_1.md §2). SOUND; remark R6 asks the draft to say this.

**ℓ = 3–10** (N2). P1 Part I gives U₋ > 0 on [0, x_H] for μ ∈ [μ_lo(ℓ), 1], i.e. q ∈ [0, q(μ_lo)], with
q(μ_lo)² ≥ (99/100)² exactly (R-P1 `part1[].covers_q_max` true); A2-E gives U₋ ≥ 0 on the closed exterior for
μ ∈ [0, μ_lo(ℓ)], i.e. q ∈ [q(μ_lo), 1]. The eight μ_lo and q(μ_lo)² are identical in the two records (table below), and
both use onset.param, so the two ranges meet at the same number: [0, q(μ_lo)] ∪ [q(μ_lo), 1] = [0, 1].

**ℓ ≥ 11.** Lemma U (P1 Part II) gives U₋ ≥ m³·959747/17496 > 0 for q ∈ [0, 1], x ∈ [0, 2] ⊇ [0, x_H] (R-P1 `part2`:
ell0 = 10, m0 = 150, ε̄ = 1/12, six checks true). Part I's top is ℓ₀ = 10, so the ℓ-partition 2 | 3–10 | ≥ 11 is complete.

**D = 6: every range end compared**

| ℓ | end | exact value | source | comparison |
|---|---|---|---|---|
| 2 | O2 upper end q_* | q_*² = the real root of 3025Y³ − 31521Y² + 99792Y − 68796; q_* = 0.9730564367… | results/onset/RESULT.md l.15; R-O2 `minimal_poly_q2`, `q_star_squared_interval`, `mu_star_interval` | > q(1/5): 21576/22801 = 0.94627428… < 0.94683882… (interval width ≤ 10⁻⁴⁵) |
| 2 | T3 lower end q(1/5) | √(21576/22801) = 0.9727663… | R-T3 `result.boxes_mu[7].mu[1]` = "1/5"; results/p3/RESULT_ADDENDUM_1.md l.16 | as above; the overlap (q(1/5), q_*] has width 2.9·10⁻⁴ |
| 2 | T3 upper end q(3/25) | √(31416/32041) = 0.9901988… | R-T3 `result.boxes_mu[0].mu[0]` = "3/25" | > q(1/8): 2961·32041 = 94,873,401 < 3025·31416 = 95,033,400 (exact) |
| 2 | A2-S lower end q(1/8) | √(2961/3025) = 0.9893649… | R-A2S `checks.PARAM.detail`; results/a2/s/RESULT.md l.11 | as above; overlap width 8.3·10⁻⁴ |
| 2 | A2-S upper end | 1 | results/a2/s/PREREG.md l.10; RESULT.md l.11 | Theorem 1's upper end |
| 3 | P1 upper = A2-E lower | μ_lo = 11/100, q² = 134331349/137053849 (0.980136) | R-P1 `part1[0]`; R-A2E `parts[0]` | identical; ≥ 0.9801 (covers_q_max true) |
| 4 | same | 103/1000, 63226555957929/64510244957929 (0.9801006) | R-P1 `part1[1]`; R-A2E `parts[1]` | identical; ≥ 0.9801: 64510244957929·0.9801 = 63,226,491,103,266 < 63,226,555,957,929 |
| 5 | same | 49/500, 312772999176/319113139801 (0.980132) | `part1[2]`; `parts[2]` | identical; covers true |
| 6 | same | 47/500, 27471514409/28023764409 (0.980294) | `part1[3]`; `parts[3]` | identical; covers true |
| 7 | same | 91/1000, 29925587924649/30523890174649 (0.980399) | `part1[4]`; `parts[4]` | identical; covers true |
| 8 | same | 89/1000, 142474321369809/145333802369809 (0.980325) | `part1[5]`; `parts[5]` | identical; covers true |
| 9 | same | 87/1000, 2613126399136/2665281539761 (0.980432) | `part1[6]`; `parts[6]` | identical; covers true |
| 10 | same | 43/500, 12122233672881/12366763922881 (0.980227) | `part1[7]`; `parts[7]` | identical; covers true |
| 3–10 | P1 lower end 0; A2-E upper end 1 | — | results/a1/RESULT.md l.11; results/a2/elementary/RESULT.md l.11 | union [0, 1] per ℓ |
| ≥ 11 | Lemma U | q ∈ [0, 1]; ℓ₀ = 10 | R-P1 `part2.ell0`, `part2.bound` = 959747/17496, checks all true; results/a1/PREREG.md l.20–22 | meets Part I's top ℓ = 10 |

## 2. Item 2 — D = 7–11, q ≤ 99/100: SOUND

For each D (N3–N5): ℓ > ℓ₀(D) is E3, Lemma U(n), q ∈ [0, 1], with ℓ₀ = 10, 10, 11, 13, 14 (R-HDE `E3[].l0`);
ℓ_el(D) ≤ ℓ ≤ ℓ₀(D) is E1, q ∈ [0, q(μ_lo)] with q(μ_lo)² ≥ (99/100)² exactly in all 35 entries (R-HDE `E1[].covers`
true, `q_hi` 99/100), ℓ_el = 4, 5, 6, 6, 7 (R-HDE `L_EL`); every ℓ < ℓ_el(D) is one of the 18 HD-S bands (2 + 3 + 4 + 4 + 5
= 18, the records R-HDS(D-ℓ) exist and are VERIFIED for exactly these). Each of the 13 onset bands meets E2 exactly: E2
gives U₋ > 0 on [0, q_split] with q(μ_lo)² ≥ q_split² (R-HDE `E2[].covers` true; `q_hi` = q_split), HD-S gives A ≥ 0 on
[q(μ_b), q(μ_a)] with q(μ_b)² ≤ q_split² and q(μ_a)² ≥ (99/100)² (R-HDS coverage fields "q(mu_b) <= q_lo or mu_b = 1"
and "q(mu_a) >= q_max", both true in all 18; HD-S's `q_lo` equals E2's `q_hi` band by band). Each of the 5 bands from
0⁺ has μ_b = 1, q(μ_b)² = 0, so HD-S alone gives [0, q(μ_a)] ⊇ [0, 99/100] (G-S6 held). The two HD-X-S bands that are
not HD-S bands, (10, 6) and (11, 7), lie in E1's range (ℓ_el(10) = 6, ℓ_el(11) = 7). So every ℓ ≥ 2 at every D is covered
on (0, 99/100]. The tables are in §3, one per D, with both regimes.

## 3. Item 3 — D = 7–11, q ∈ [99/100, 1]: SOUND

Partition of ℓ ≥ 2 at each D (n = D − 2): the 20 bands ℓ = 2, …, n − 2 (2, 3, 4, 5, 6 of them), split into the 11 with
2ℓ > n − 1 (HD-X-S) and the 9 with 2ℓ ≤ n − 1 (HD-X-2, the critical set); n − 1 ≤ ℓ ≤ ℓ₀(D) (HD-X-E, 33 cases); ℓ > ℓ₀
(Lemma U(n)). Complete at each D (N5). Lower ends: HD-X-S's q(1/8)² ≤ (99/100)² (R-HDXS PARAM, 11 bands); HD-X-2's
q(MU1)² ≤ (99/100)² (R-HDX2 PARAM, 9 bands); HD-X-E's lower end is not below 99/100, it is q(μ_lo) ≥ 99/100 with μ_lo
equal to HD-E's E1 end (R-HDXE `MEET`: 33 entries, `equal` and `meets` true; the q(μ_lo)² values equal E1's entry by entry),
so the sliver (99/100, q(μ_lo)) rests on E1 and the ranges meet at the same number; Lemma U(n) has no lower end. Upper
ends: 1 for HD-X-E, HD-X-S and Lemma U(n); 1 excluded for HD-X-2, whose q = 1 is Theorem 2's (R-Z(n) VERIFIED at
n = 4…9 and N; A_{ℓ,1} ≥ 0 for every ℓ ≥ 2). Every HD-X-S lower end is below the matching HD-S or E1 upper end, and every
HD-X-2 lower end is below its HD-S upper end, so the two regimes overlap (all nine HD-X-2 bands are HD-S bands).

**Per-D tables** (both regimes; sources: R-HDE `E2[]`/`E1[]`/`E3[]`, R-HDS `coverage`, R-HDXS `checks.PARAM.detail`,
R-HDX2 `q(MU1)^2` and `charts.MU1`, R-HDXE `MEET` and parts). "gate" = the record's field is true; decimals mine.

**D = 7 (n = 5): ℓ_el = 4, ℓ₀ = 10; bands ℓ = 2 (HD-X-2), 3 (HD-X-S); HD-X-E ℓ = 4–10; E3 ℓ ≥ 11.**

| ℓ | end | exact value | comparison |
|---|---|---|---|
| 2 | E2 upper q_split | 237/250 = 0.948 (q² 0.898704); E2 covers: q(176/625)² = 6872766153201/7647166153201 = 0.898734 ≥ | gate covers true |
| 2 | HD-S lower q(μ_b), μ_b = 2817/10000 | 450385526985669121/501172656585669121 = 0.898665 | ≤ q_split² (gate true; margin 3.9·10⁻⁵) |
| 2 | HD-S upper q(μ_a), μ_a = 1237/10000 | 482351496417168561/492144578017168561 = 0.9801012 | ≥ 0.9801 (gate true) |
| 2 | HD-X-2 lower q(MU1), MU1 = 1/8 | 197505/201601 = 0.979683 | ≤ 0.9801 (gate PARAM true); < HD-S upper (overlap) |
| 2 | HD-X-2 upper (open), then Theorem 2 | 1 | R-Z(5) VERIFIED |
| 3 | E2 upper q_split | 977/1000 (q² 0.954529) | gate covers true |
| 3 | HD-S lower, μ_b = 1719/10000 | 154985298094511521/162372700594511521 = 0.954503 | ≤ q_split² (gate true) |
| 3 | HD-S upper, μ_a = 283/2500 | 616496957997921/629010864247921 = 0.9801054 | ≥ 0.9801 (gate true) |
| 3 | HD-X-S lower q(1/8) | 64449/66049 = 0.975776 | ≤ 0.9801 (gate PARAM true); < HD-S upper |
| 3 | HD-X-S upper | 1 | claim "q ∈ [q(1/8), 1]" |
| 4–10 | E1 upper = HD-X-E lower q(μ_lo) | μ_lo = 1061/10000, 1011/10000, 487/5000, 59/625, 921/10000, 901/10000, 177/2000 | E1 covers true (each ≥ 0.9801; ℓ = 4: 88875546247769841/90676699847769841 = 0.980136); MEET equal true, same q² in both records |
| 4–10 | E1 lower 0; HD-X-E upper 1 | — | union [0, 1] |
| ≥ 11 | E3 | q ∈ [0, 1]; l0 = 10 | meets E1's top |

**D = 8 (n = 6): ℓ_el = 5, ℓ₀ = 10; bands ℓ = 2 (HD-X-2, from 0⁺), 3, 4 (HD-X-S); HD-X-E ℓ = 5–10; E3 ℓ ≥ 11.**

| ℓ | end | exact value | comparison |
|---|---|---|---|
| 2 | HD-S lower, μ_b = 1 | q² = 0 | from 0⁺ (G-S6 held) |
| 2 | HD-S upper, μ_a = 157/1250 | 17083021501189/17429648063689 = 0.9801128 | ≥ 0.9801 (gate true) |
| 2 | HD-X-2 lower, MU1 = 13/100 | 698908729/714118729 = 0.978701 | ≤ 0.9801 (gate true); < HD-S upper |
| 3 | E2 upper q_split | 118/125 = 0.944 (q² 0.891136) | gate covers true |
| 3 | HD-S lower, μ_b = 549/2000 | 3684836513121/4135077513121 = 0.891116 | ≤ q_split² (gate true) |
| 3 | HD-S upper, μ_a = 1157/10000 | 199657162856145201/203706576081145201 = 0.9801213 | ≥ 0.9801 (gate true) |
| 3 | HD-X-S lower q(1/8) | 81585/83521 = 0.976821 | ≤ 0.9801 (gate true); < HD-S upper |
| 4 | E2 upper q_split | 983/1000 (q² 0.966289) | gate covers true |
| 4 | HD-S lower, μ_b = 1421/10000 | 978026969107944729/1012152142007944729 = 0.966284 | ≤ q_split² (gate true; and by hand: 978026969107944729·10⁶ < 1012152142007944729·966289 = 978,031,481,148,714,904,240,681) |
| 4 | HD-S upper, μ_a = 68/625 | 3765525061221/3841839123721 = 0.980136 | ≥ 0.9801 (gate true) |
| 4 | HD-X-S lower q(1/8) | 402633/413449 = 0.973839 | ≤ 0.9801 (gate true); < HD-S upper |
| 5–10 | E1 upper = HD-X-E lower | μ_lo = 519/5000, 999/10000, 969/10000, 59/625, 231/2500, 907/10000 | E1 covers true; MEET equal true; same q² |
| ≥ 11 | E3 | l0 = 10 | meets E1's top |

**D = 9 (n = 7): ℓ_el = 6, ℓ₀ = 11; bands ℓ = 2 (0⁺), 3 (HD-X-2), 4, 5 (HD-X-S); HD-X-E ℓ = 6–11; E3 ℓ ≥ 12.**

| ℓ | end | exact value | comparison |
|---|---|---|---|
| 2 | HD-S lower, μ_b = 1 | 0 | from 0⁺ |
| 2 | HD-S upper, μ_a = 1271/10000 | 796755993449624481/812910403449624481 = 0.9801277 | ≥ 0.9801 (gate true) |
| 2 | HD-X-2 lower, MU1 = 13/100 | 7961448561/8130448561 = 0.979214 | ≤ 0.9801 (gate true); < HD-S upper |
| 3 | E2 upper q_split | 921/1000 (q² 0.848241) | gate covers true |
| 3 | HD-S lower, μ_b = 1659/5000 | 13843592400702961/16320645300702961 = 0.848225 | ≤ q_split² (gate true) |
| 3 | HD-S upper, μ_a = 589/5000 | 1711069078242249/1745761178242249 = 0.9801278 | ≥ 0.9801 (gate true) |
| 3 | HD-X-2 lower, MU1 = 3/25 | 2404864/2455489 = 0.979383 | ≤ 0.9801 (gate true); < HD-S upper |
| 4 | E2 upper q_split | 119/125 = 0.952 (q² 0.906304) | gate covers true |
| 4 | HD-S lower, μ_b = 489/2000 | 1812171689673769/1999642553673769 = 0.906248 | ≤ q_split² (gate true) |
| 4 | HD-S upper, μ_a = 139/1250 | 291488937834369/297405994084369 = 0.9801044 | ≥ 0.9801 (gate true) |
| 4 | HD-X-S lower q(1/8) | 9945/10201 = 0.974904 | ≤ 0.9801 (gate true); < HD-S upper |
| 5 | E2 upper q_split | 987/1000 (q² 0.974169) | gate covers true |
| 5 | HD-S lower, μ_b = 303/2500 | 38425874043609/39445974043609 = 0.974139 | ≤ q_split² (gate true) |
| 5 | HD-S upper, μ_a = 1061/10000 | 88875546247769841/90676699847769841 = 0.9801365 | ≥ 0.9801 (gate true) |
| 5 | HD-X-S lower q(1/8) | 36225/37249 = 0.972509 | ≤ 0.9801 (gate true); < HD-S upper |
| 6–11 | E1 upper = HD-X-E lower | μ_lo = 511/5000, 991/10000, 483/5000, 59/625, 463/5000, 911/10000 | E1 covers true; MEET equal true; same q² |
| ≥ 12 | E3 | l0 = 11 | meets E1's top |

**D = 10 (n = 8): ℓ_el = 6, ℓ₀ = 13; bands ℓ = 2 (0⁺), 3 (interior; both HD-X-2), 4, 5, 6 (HD-X-S; ℓ = 6 is E1 below
99/100); HD-X-E ℓ = 7–13; E3 ℓ ≥ 14.**

| ℓ | end | exact value | comparison |
|---|---|---|---|
| 2 | HD-S lower, μ_b = 1 | 0 | from 0⁺ |
| 2 | HD-S upper, μ_a = 321/2500 | 3841215986197681/3919140742447681 = 0.9801169 | ≥ 0.9801 (gate true) |
| 2 | HD-X-2 lower, MU1 = 13/100 | 9829338561/10033828561 = 0.979620 | ≤ 0.9801 (gate true); < HD-S upper |
| 3 | E2 upper q_split (interior band) | 49/100 = 0.490 (q² 0.2401) | gate covers true |
| 3 | HD-S lower, μ_b = 8301/10000 | 91914991536373201/383045380761373201 = 0.239959 (q = 0.489856…) | ≤ q_split² (gate true) |
| 3 | HD-S upper, μ_a = 299/2500 | 1164187484726301/1187794936288801 = 0.980125 | ≥ 0.9801 (gate true) |
| 3 | HD-X-2 lower, MU1 = 3/25 | 46562824/47513449 = 0.979992 (the largest of the nine) | ≤ 0.9801: 47513449·0.9801 = 46,567,931.4 > 46,562,824 (gate true); < HD-S upper |
| 4 | E2 upper q_split | 23/25 = 0.92 (q² 0.8464) | gate covers true |
| 4 | HD-S lower, μ_b = 3217/10000 | 142513652343129921/168386374843129921 = 0.846350 | ≤ q_split² (gate true) |
| 4 | HD-S upper, μ_a = 283/2500 | 616496957997921/629010864247921 = 0.9801054 | ≥ 0.9801 (gate true) |
| 4 | HD-X-S lower q(1/8) | 64449/66049 = 0.975776 | ≤ 0.9801 (gate true); < HD-S upper |
| 5 | E2 upper q_split | 961/1000 (q² 0.923521) | gate covers true |
| 5 | HD-S lower, μ_b = 429/2000 | 949834170649/1028514420649 = 0.9235011 | ≤ q_split² (gate true; by hand: 949834170649·10⁶ < 1028514420649·923521 = 949,854,666,272,185,129) |
| 5 | HD-S upper, μ_a = 541/5000 | 6517045060605261/6649208824667761 = 0.9801234 | ≥ 0.9801 (gate true) |
| 5 | HD-X-S lower q(1/8) | 42525/43681 = 0.973535 | ≤ 0.9801 (gate true); < HD-S upper |
| 6 | E1 upper q(μ_lo), μ_lo = 1043/10000 | 1580398467335649/1612456711335649 = 0.980119 | ≥ 0.9801 (covers true) |
| 6 | HD-X-S lower q(1/8) | 788697/811801 = 0.971540 | ≤ 0.9801 (gate true); < E1 upper: [0, q(μ_lo)] ∪ [q(1/8), 1] = [0, 1] |
| 7–13 | E1 upper = HD-X-E lower | μ_lo = 1011/10000, 197/2000, 963/10000, 59/625, 58/625, 457/5000, 901/10000 | E1 covers true; MEET equal true; same q² |
| ≥ 14 | E3 | l0 = 13 | meets E1's top |

**D = 11 (n = 9): ℓ_el = 7, ℓ₀ = 14; bands ℓ = 2, 3 (0⁺), 4 (all HD-X-2), 5, 6, 7 (HD-X-S; ℓ = 7 is E1 below 99/100);
HD-X-E ℓ = 8–14; E3 ℓ ≥ 15.**

| ℓ | end | exact value | comparison |
|---|---|---|---|
| 2 | HD-S lower, μ_b = 1 | 0 | from 0⁺ |
| 2 | HD-S upper, μ_a = 259/2000 | 211474330206729/215767514206729 = 0.9801027 | ≥ 0.9801 (gate true) |
| 2 | HD-X-2 lower, MU1 = 13/100 | 1321538729/1348578729 = 0.979950 | ≤ 0.9801 (gate true); < HD-S upper |
| 3 | HD-S lower, μ_b = 1 | 0 | from 0⁺ |
| 3 | HD-S upper, μ_a = 303/2500 | 153891955293609/157016011543609 = 0.9801036 | ≥ 0.9801 (gate true) |
| 3 | HD-X-2 lower, MU1 = 1/8 | 2961/3025 = 0.978843 | ≤ 0.9801 (gate true); < HD-S upper |
| 4 | E2 upper q_split | 897/1000 (q² 0.804609) | gate covers true |
| 4 | HD-S lower, μ_b = 1853/5000 | 90451546986883929/112426644586883929 = 0.804539 | ≤ q_split² (gate true) |
| 4 | HD-S upper, μ_a = 1149/10000 | 1666516108576123609/1700313254176123609 = 0.980123 | ≥ 0.9801 (gate true) |
| 4 | HD-X-2 lower, MU1 = 3/25 | 1015861/1038361 = 0.978332 | ≤ 0.9801 (gate true); < HD-S upper |
| 5 | E2 upper q_split | 929/1000 (q² 0.863041) | gate covers true |
| 5 | HD-S lower, μ_b = 59/200 | 1974131929/2287421929 = 0.8630380 | ≤ q_split² (gate true; by hand: 1974131929·10⁶ < 2287421929·863041 = 1,974,138,909,026,089) |
| 5 | HD-S upper, μ_a = 11/100 | 134331349/137053849 = 0.980136 | ≥ 0.9801 (gate true) |
| 5 | HD-X-S lower q(1/8) | 609/625 = 0.9744 | ≤ 0.9801 (gate true); < HD-S upper |
| 6 | E2 upper q_split | 121/125 = 0.968 (q² 0.937024) | gate covers true |
| 6 | HD-S lower, μ_b = 381/2000 | 15357181301769/16389437301769 = 0.9370170 | ≤ q_split² (gate true; by hand: 15357181301769·10⁶ < 16389437301769·937024 = 15,357,296,098,252,795,456) |
| 6 | HD-S upper, μ_a = 1061/10000 | 88875546247769841/90676699847769841 = 0.9801365 | ≥ 0.9801 (gate true) |
| 6 | HD-X-S lower q(1/8) | 36225/37249 = 0.972509 | ≤ 0.9801 (gate true); < HD-S upper |
| 7 | E1 upper q(μ_lo), μ_lo = 103/1000 | 63226555957929/64510244957929 = 0.9801006 | ≥ 0.9801 (covers true; exact as in §1, ℓ = 4) |
| 7 | HD-X-S lower q(1/8) | 257481/265225 = 0.970802 | ≤ 0.9801 (gate true); < E1 upper |
| 8–14 | E1 upper = HD-X-E lower | μ_lo = 1003/10000, 49/500, 961/10000, 59/625, 929/10000, 229/2500, 181/2000 | E1 covers true; MEET equal true; same q² |
| ≥ 15 | E3 | l0 = 14 | meets E1's top |

Coincidences checked (N3): equal q² values in different bands come from proportional (A, B), e.g. w = 5μ/(4 + μ²) for
both (7, 3) and (10, 4); they are not copy errors.

## 4. Item 4 — each piece's route to A ≥ 0: SOUND

| route | what the claim must say | pieces, and what their records say |
|---|---|---|
| U₋ ≥ 0 ⟹ V ≥ 0 ⟹ A ≥ 0 | U₋(x; q) ≥ 0 for every x in the open exterior (0, x_H(q)) at every q of the range; then V = fU₋/(64r²H₋²) ≥ 0 since f > 0 on the exterior (at q = 1, f = (1 − Y)² > 0 for ρ > 1), r > 0 and H₋ = m + n(n + 1)(1 + mδ)x/2 ≥ m > 0 (m > 0, δ ≥ 0, x ≥ 0); the form ∫(|φ′|² + V|φ|²) is then ≥ 0 term by term, with no other hypothesis | O2: U₋ ≥ 0 on [0, x_H], q ≤ q_*, zero only at (q_*, x_H) (RESULT l.16). P1: U₋ > 0 on [0, x_H], ℓ ≥ 3, q ≤ 99/100 (RESULT l.11). Lemma U, E3: U₋ ≥ m³(64 − Neg) > 0 on x ∈ [0, 2] ⊇ [0, x_H], q ∈ [0, 1] (needs κ ≤ 1/(n + 1), from q ≤ 1; R-P1 `part2`, R-HDE `E3`). E1, E2: U₋ > 0 on [0, x_H] (R-HDE). A2-E, HD-X-E: U₋ ≥ 0 on the closed exterior, strict except the touching ℓ, whose zero is at the extremal horizon, outside the open exterior (RESULTs l.11–12, l.26–31). All stronger than the route needs |
| N > 0 ⟹ Ṽ ≥ 0 ⟹ A ≥ 0 (Proposition 3) | for each q of the range a design P that is C¹ on (0, 1) with N ≥ 0 on (0, 1), with q² ≤ 1, m > 0, δ ≥ 0 (`prop3_Dn`'s hypotheses, read in my HD-X-2 audit), and the inverse tortoise map R with R′ = f(R) (pencil for 0 < q < 1, my A2; `tortoise_q1` at q = 1) | T3: P polynomial in (z, μ), N > 0 and L > 0 on [0, 1] × each μ-box (R-T3), so N ≥ 0 on (0, 1) for each μ, by METHOD.md's parameter-box remark; the n = 4 polynomial form (METHOD.md; Lean `prop3_D6`); q < 1 throughout. HD-S: P polynomial in z or P̂/(z + δ_b)^d with δ_b > 0, N·L·s^{2e} > 0 and L > 0 on [0, 1] × box (RESULT l.16–19; METHOD_ADDENDUM_2; `prop3_Dn`, `prop3_Dn_zeta`); q(μ_a) < 1. A2-S, HD-X-S: singular P with the pole at −ε ≤ 0, N > 0 on (0, 1) for μ ∈ [0, 1/8], q = 1 included: METHOD_ADDENDUM_3's form (P C¹ on (0, 1) only), `prop3_Ioo`/`prop3_Dn`, with R from `tortoise_q1` at μ = 0 (RESULTs l.11–13 and l.36–38). HD-X-2: μ ∈ (0, MU1], pole at −ε < 0, N > 0 on (0, 1) (RESULT l.61–68; my audit of this morning, items 1–4) |
| q = 1, Theorem 2 | u₀ solves the q = 1 zero-energy equation (Z-id) and u₀ > 0 (Z-pos), the tortoise map at q = 1 (`tortoise_q1`), S = −(log u₀)_{r*} ∈ C¹(ℝ), Lemma 1 with V + S′ − S² ≡ 0 | Z: VERIFIED at n = 4–9 and N (R-Z), gates q1, H, Z-pos, Z-inf, Z-thr, Z-id; Lean `A_nonneg` for every n ≥ 2, ℓ ≥ 2 (lean_z_d README l.80–89, read this morning). Used for the HD-X-2 endpoint; redundant elsewhere (A2-S, A2-E, HD-X-S, HD-X-E and Lemma U include q = 1) |

Each piece uses the route that fits its claim, as §5's conventions say. For the N > 0 route the records' claims are
stated on closed sets ([0, 1] × box) or on (0, 1) with μ-ranges, each at least what Proposition 3 needs; the pencil steps
inside the routes (Proposition 3's extensions, the tortoise maps, Lemma U's steps, Theorem 2's ground-state step) are
hypotheses here (§8), with their audits as the records list them.

## 5. Item 5 — Theorem 1 follows: SOUND

§3's Theorem 1 is the conjunction over D = 6, 7, 8, 9, 10, 11 of "for every integer ℓ ≥ 2 and every q ∈ (0, 1],
∫(|φ′|² + V_{ℓ,q}|φ|²) ≥ 0 for all φ ∈ C₀^∞(ℝ)". Items 1–3 give, at each D and each ℓ ≥ 2, a cover of (0, 1] by
certified q-ranges, and item 4 gives on each range exactly that inequality for φ ∈ C₀^∞(ℝ) (Lean's conclusions are for
C¹ compactly supported φ, a superset). The union over D is the statement. The corollary (N7): A_{ℓ,q} is, by §2, the
self-adjoint operator of this form on C₀^∞(ℝ); V is real, continuous and bounded on ℝ (H₋ ≥ m > 0; U₋ bounded on
[0, x_H]; V → 0 at both ends, like c/r*² at an extremal throat), so A = −d²/dr*² + V is self-adjoint on H²(ℝ), its form
is ≥ 0 on the form domain H¹ by density, and A ≥ 0. A mode e^{κt}φ with κ > 0 and 0 ≠ φ ∈ L² solves φ″ = (V + κ²)φ, so
φ″ ∈ L² and φ ∈ H² = dom(A), and ⟨φ, Aφ⟩ = −κ²‖φ‖² < 0 contradicts A ≥ 0. §2 defines a mode directly as an
eigenfunction of A ("i.e. A_{ℓ,q}φ = −κ²φ"), which makes the corollary immediate; the one-clause justification that a
classical L² solution lies in dom(A) is remark R7. At q = 1 the tortoise map onto ℝ is `tortoise_q1`, as §2 says.

## 6. Numbers, names and ranges in §§3–5 that differ from the records (the brief's "also report")

Agreeing (checked): the cubic for q_*² and q_* = 0.97305… (a prefix of 0.9730564…); the exact ends of T3 and A2-S; ℓ =
3–10 and ℓ ≥ 11 at D = 6; ℓ_el = 4, 5, 6, 6, 7; ℓ₀ = 10, 10, 11, 13, 14; the 18 bands, 13 with an onset and 5 from 0⁺,
with their (D, ℓ); the q_split values; the interior band's q(μ_b) < 0.490; the 20 bands and their 11 + 9 split; MEET;
q(1/8)² and q(MU1)² ≤ (99/100)² with 46562824/47513449 the largest, at D = 10 ℓ = 3; Theorem 2's statement and n-range;
MU1 ∈ {1/8, 13/100, 3/25}; the cover constants; every piece's name. Differing:

1. **l.154 (§4.3):** "the bound 959747/17496 ≈ 54.86". The records quote a certified lower bound inward:
   results/a1/RESULT_ADDENDUM_1.md (BHM-119) l.14–19 and l.27 correct "≈ 54.86" to **54.85** (four significant figures)
   or 54.855, in five places; the draft repeats the corrected value.
2. **l.213 (§5.1):** "[√(21576/22801), √(31416/32041)] = [0.97277…, 0.99019…]". The digits of √(21576/22801) are
   0.9727663… (results/p3/RESULT_ADDENDUM_1.md l.16); 0.97277 is the inward (rounded-up) lower end, so the ellipsis after
   it is misleading. Write "[0.97277, 0.99019] (inward)" or "[0.97276…, 0.99019…]".
3. **l.214 (§5.1):** "[√(2961/3025), 1] = [0.98936…, 1]". The digits are right (0.989365…), but §5's convention
   (l.203, "Decimals are inward") makes the lower end 0.98937 (results/a2/s/RESULT_ADDENDUM_1.md l.33;
   results/a2/STAGE_REPORT_ADDENDUM_1.md §3 l.32–39, which made exactly this point about the same number).
4. **l.230 (§5.2):** "q(μ_b) = 0.48986…": the digits are 0.489856…; 0.48986 is the inward value (HD-S's RESULT l.50
   writes the same). Same ellipsis point as 2.
5. **l.175–176 (§4.5):** "Each chart's polynomial comes after an exact division by a power of μ, z or σ. Their union
   covers (0, 1) × (0, μ₁]." For A2-S and HD-X-S, whose claims include q = 1, the cover that is proved and needed is
   (0, 1) × [0, μ₁] (results/a2/s/PREREG.md l.45; results/hdx/s/PREREG.md l.39), and their O and O′ charts use NL
   undivided; "(0, μ₁]" and divisions on all four charts describe HD-X-2 (§4.6) only. One sentence each, or "(0, 1) ×
   [0, μ₁], or (0, μ₁] for the critical bands".

None of these touches the assembly's logic or any claim.

## 7. Remarks (fixes of one clause or one sentence; no verdict depends on them)

- **R1–R5:** the five differences of §6, each a one-clause or one-sentence fix.
- **R6 (§5.1 or §6, T3's provenance).** Say that the run of record that produced T3 (BHM-023) carries the registered
  verdict FAIL, from the known-answer gate G1 under design rule 1; that T3's certificate is independent of that gate
  and of the design rule (eight exact verifications of stored polynomials, soundness controls passed); that G1 passed
  under rule 2 (BHM-025) without re-running T3; and that T3 has two second parties. §6's "Failed and void runs stay on
  the record" is generic, and a reader of "certified" in §5.1 would not expect a FAIL in the run of record.
- **R7 (§2, the notion of mode).** One clause: a classical L² solution of φ″ = (V + κ²)φ lies in H² = dom(A) because V
  is bounded, so "A ≥ 0 ⟹ no mode" needs nothing more (N7).
- **R8 (§5 conventions, l.202).** "Range ends are exact: rationals, or square roots of rationals" does not cover q_*,
  a cubic irrational; its comparison with √(21576/22801) is through O1's isolating interval (R-O2). One clause.
- **R9 (§5.3, HD-X-E's lower end).** The text has it right ("Each μ_lo equals HD-E's sealed E1 end (gate MEET), so these
  ranges meet §5.2's"); it could add that q(μ_lo) ≥ 99/100, so the sliver (99/100, q(μ_lo)) is E1's, as
  results/stage3/STAGE_REPORT_ADDENDUM_1.md §2 states. Clarity only.
- **R10 (§5.1, P1).** "(0, q(μ_lo(ℓ))]" is [0, q(μ_lo(ℓ))] in the record (q = 0 included); harmless.

## 8. Hypotheses assumed

1. **The certified pieces are valid as recorded** (the brief's instruction): O2 (BHM-017), T3 (BHM-023), P1 and Lemma U
   (BHM-052), A2-E (BHM-097), A2-S (BHM-101), HD-E E1–E3 (BHM-063), HD-S (BHM-078), HD-X-E (BHM-128), HD-X-S (BHM-132),
   HD-X-2 (BHM-144), Z (BHM-126). Their records were read, not re-run; their exact gate fields (covers, coverage, PARAM,
   MEET) are the exact comparisons, and my decimals and cross-multiplications are checks of them.
2. **The pencil steps inside the routes**, with the audits the records list: Lemmas 1–2 and Proposition 3 (METHOD.md,
   addenda 2–3; Lean `prop3_D6`, `prop3_Ioo`, `prop3_Dn`, `prop3_Dn_zeta`, read this morning), the inverse tortoise map
   for 0 < q < 1 (my A2) and at q = 1 (`tortoise_q1`), Lemma U's steps (a)–(d), Theorem 2's ground-state step (Lean
   `A_nonneg`), the reductions and covers of the singular designs (my A3 and this morning's audit; Kimi).
3. **S5's transcription** in `code/ki/potentials.py` and in Lean (gates E0/E0n; not re-checked).
4. **The parametrisation** q(μ)² = 1 − w(μ)², w = Bμ/A increasing, the same function in every piece at the same (n, ℓ)
   (gates O5/PARAM; PARAM4 ties onset.param to param_n at n = 4). It is what makes "the same μ_lo" mean "the same q".
5. **q_max(D) = 99/100 for every D = 7–11** (TARGET_HD_ADDENDUM_1.md §1, read today) and q_max = 99/100 at D = 6
   (TARGET_ADDENDUM_1.md §1).
6. The brief's description of the pieces matches the records (it does), and the draft's labels and second-party
   statements (§4.1, §4.6, §5.4) match the stage reports' addenda where I compared them (they do).

## 9. Files and line ranges read, per item (bh-modes repository paths; `all` = the whole file)

- **Item 1:** DRAFT_v0.2.md l.198–221; results/onset/PREREG.md all (85), RESULT.md all (70), R-O2 all; results/p3/PREREG.md
  all (65), PREREG_ADDENDUM_1.md all (49), RESULT.md all (63), RESULT_ADDENDUM_1.md all (50), RULE2_RESULT.md all (33),
  R-T3 (keys, `result.boxes_mu[].mu`, `bernstein`, `verdict`, `tier`; the eight P coefficient arrays not read);
  results/a1/PREREG.md all (135), PREREG_ADDENDUM_1.md all (45), RESULT.md all (91), RESULT_ADDENDUM_1.md all (27),
  STAGE_REPORT.md all (92), STAGE_REPORT_ADDENDUM_1.md all (29), R-P1 all; results/a2/elementary/PREREG.md all (64),
  RESULT.md all (55), R-A2E all; results/a2/s/PREREG.md all (107), PREREG_ADDENDUM_1.md all (86), RESULT.md all (64),
  RESULT_ADDENDUM_1.md all (54), R-A2S all; results/a2/STAGE_REPORT.md all (98), STAGE_REPORT_ADDENDUM_1.md all (84),
  STAGE_REPORT_ADDENDUM_2.md all (50); TARGET.md all (106); TARGET_ADDENDUM_1.md all (48); TARGET_A2.md all (137);
  TARGET_A2_ADDENDUM_1.md all (109).
- **Item 2:** DRAFT_v0.2.md l.222–233; results/hd/elementary/PREREG.md all (111), RESULT.md all (95), RESULT_ADDENDUM_1.md
  all (55), R-HDE all; results/hd/s/PREREG.md all (140), PREREG_ADDENDUM_1.md all (62), RESULT.md all (85),
  RESULT_ADDENDUM_1.md all (52), R-HDS for all 18 bands (fields `verdict`, `kind`, `q_lo`, `q_max`, `coverage`,
  `claim_q`; the certificate polynomials not read); results/hd/STAGE_REPORT.md all (101), STAGE_REPORT_ADDENDUM_1.md all
  (68), STAGE_REPORT_ADDENDUM_2.md all (43); TARGET_HD.md all (104); TARGET_HD_ADDENDUM_1.md all (43);
  code/hd/elementary.py l.47–61 (BANDS, L_EL), code/hd/scert.py l.51–63 and l.94–115 (Q_MAX, partition, coverage) (both
  read in full this morning).
- **Item 3:** DRAFT_v0.2.md l.235–249; results/hdx/elementary/PREREG.md all (102), RESULT.md all (57), R-HDXE (`verdict`,
  `checks`, `MEET` all 33, the 33 parts' D, ell, mu_lo, q², path, rule; A2E4); results/hdx/s/PREREG.md all (111, read
  this morning), RESULT.md all (53), R-HDXS for the 11 bands and the gate band (`verdict`, `claim`, PARAM, S, COVER,
  design); results/hdx/critical/PREREG.md all (219, this morning), PREREG_ADDENDUM_1.md all (99), RESULT.md all (92),
  RESULT_ADDENDUM_1.md all (46), R-HDX2 for the 9 bands (`verdict`, `claim`, `charts.MU1`, `q(MU1)^2`, PARAM, COVER,
  design); results/extremal/PREREG.md all (143), PREREG_ADDENDUM_1.md all (35), RESULT.md all (83), R-Z verdicts for
  n = 2–9 and N, and the full records for n = 9 and N; results/stage3/STAGE_REPORT.md all (195),
  STAGE_REPORT_ADDENDUM_1.md all (109), STAGE_REPORT_ADDENDUM_2.md all (60); TARGET_HD_ADDENDUM_2.md all (96),
  TARGET_HD_ADDENDUM_3.md all (22).
- **Item 4:** DRAFT_v0.2.md l.120–197 and l.200–207; results/p3/METHOD.md all (52), METHOD_ADDENDUM_1.md all (50),
  METHOD_ADDENDUM_2.md all (53), METHOD_ADDENDUM_3.md all (49) (read this morning); the pieces' claim paragraphs cited in
  §4; lean/lean_p3_sdeformation_v5_2026-10-24/lean/BHModesP3.lean l.173–200, 403–411, 528–555, 636–666 and
  lean/lean_z_d_2026-10-26/README.md (read this morning, for the HD-X-2 audit); my own
  results/stage3/audits/fable_2026-10-26/AUDIT.md §A2–A3 and results/hdx/critical/audits/fable_2026-11-13/AUDIT.md
  (mine, this morning).
- **Item 5:** DRAFT_v0.2.md l.67–118 (§§2–3), l.198–207, l.251–271; TARGET.md l.8–47; TARGET_A2.md l.9–39;
  results/a2/STAGE_REPORT_ADDENDUM_1.md §1; results/hd/STAGE_REPORT_ADDENDUM_1.md l.6–17;
  results/stage3/STAGE_REPORT_ADDENDUM_1.md §1.
- **Context:** DRAFT_v0.2.md all (323); CHARTER.md §5 and RULES.md §B (this morning); the records' inventories under
  results/{onset,p3,a1,a2,hd,hdx,extremal,stage3} (file names only, with every `audits/` and `reviews/` folder pruned).

## 10. Process and time

- Start 12:05:40 EST (both hashes computed); the allow-list read by 12:15:21 EST; `AUDIT_notes.md` finished 12:21:31
  EST; this file written next. End time: `STATE_LOG.md`'s last entry and the delivery message (from `date`). Inside the
  three-hour box; no stop condition was reached; items 1–3 were done first.
- No process run on any host (reading, `jq`/`grep`/`sed` on the records, `sha256sum` and file writing on host-0 only);
  no external contact; nothing written outside this folder; no git.
- Files here: `AUDIT.md` (this), `AUDIT_notes.md` (N1–N8, written first), `BRIEF_fable_2026-11-13_assembly.md` (a 0444
  copy of the brief, same sha256), `STATE.md`, `STATE_LOG.md`, `MESSAGES.md` (the last three evolve and are excluded
  from `SHA256SUMS`, which lists every other file).
