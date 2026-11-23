# Audit of the compositions inside Theorems A1 and HD

*Seat: Kimi K3, second auditor. Date: 2026-11-21. Brief:
`paper/stability/briefs/BRIEF_kimi_2026-11-20_assembly.md`, SHA-256
`41c519192e648e8dc3760a2a4789a56d54596e8ab56e56a46d7906ed83155c7b`.
Manifest: `BRIEF_kimi_2026-11-20_assembly_MANIFEST.sha256`, SHA-256
`ad629ed907392b7fb93103ba9d814a8974d6654f3ec0a7379dd5035f69b0d1ae`.
All 301 allow-listed files passed `sha256sum -c` from the repository root.
No external contact and no reading outside the allow-list.*

**Model and version.** Kimi K3 (API coding agent), with Python 3.12.8 and
`fractions.Fraction` for every exact range-end comparison. `audit_ranges.py`
ran on host-1 under `nice -n 19`; its log is `range_checks.log`. Decimal
checks ran on the same host (`decimal_checks.log`). No ODE, [another line of this project], or
certificate computation was rerun.

## Verdicts

- **Item 1, D = 6: SOUND.** The three ℓ = 2 pieces overlap exactly, P1 and
  A2-E meet at the same μ_lo for every ℓ = 3–10, and Lemma U covers ℓ ≥ 11
  for every q ∈ [0, 1]. T3's certificate stands for the right reason: its
  registered G1 design failed, but T3's exact polynomial certificates pass,
  and design rule 2 passes G1.
- **Item 2, D = 7–11, q ≤ 99/100: SOUND.** E1, E2, E3 and all 18 HD-S
  bands meet exactly. The D = 10 ℓ = 3 interior onset is strictly below
  q_split. The five from-0+ bands verify the box ending at μ = 1.
- **Item 3, routes to A ≥ 0: SOUND.** Every U₋-positivity route gives V ≥ 0
  on the exterior, and every N-positivity route satisfies Proposition 3 for
  the range used. No route is used outside its certified range.
- **Item 4, discrepancies: GAP-MINOR (reporting only).** One lower-decimal
  error was found: the frozen draft writes 0.98937 for A2-S's lower end,
  while the exact value rounds down to 0.98936, as `a2/s/RESULT.md` has it.
  No range meeting fails, and no other number, name or range mismatch was
  found.
- **Overall: SOUND, with that reporting correction.** There is no missing
  certificate or incorrect composition argument in the audited sections.

## Exact composition arguments

### D = 6, ℓ = 2

- O2 gives U₋ ≥ 0 on (0, q_*], hence V ≥ 0 on the exterior. The sealed
  interval for q_*² is exact and lies strictly above T3's lower end
  21576/22801. T3's other end is 31416/32041, and A2-S starts at 2961/3025,
  strictly below it. Therefore the three intervals overlap rather than
  merely touch.
- T3 has **eight** exact polynomial certificates, so its registered design
  failure is not a certificate failure. `RULE2_RESULT.md` then gives G1
  VERIFIED. The draft's distinction between registration and certificate is
  correct and is not a loophole: the exact T3 objects, not the design rule,
  are what is certified.
- A2-S's q(1/8)² = 2961/3025 ≤ (99/100)², so the final piece also reaches
  the A1/A2 meeting point.

### D = 6, ℓ = 3–10 and ℓ ≥ 11

For each ℓ = 3, …, 10, `a1/runs/record/main/result.json` and
`a2/elementary/runs/record/none/result.json` have literally the same
`mu_lo` and `q_at_mu_lo_squared`, and that squared value is ≥ (99/100)².
Hence P1's [0, q(μ_lo)] and A2-E's [q(μ_lo), 1] cover exactly. Lemma U's
bound 959747/17496 is positive and applies to every ℓ ≥ 11 and q ∈ [0, 1].

### D = 7–11, q ≤ 99/100

- E1 has 35 (D, ℓ) rows, all with q(μ_lo)² ≥ (99/100)² and with the
  elementary partition ℓ_el = 4, 5, 6, 6, 7 and ℓ₀ = 10, 10, 11, 13, 14.
- E2 has 13 onsets and each q(μ_lo)² is ≥ q_split². HD-S starts at or below
  that same q_split in every case. D = 10 ℓ = 3 has
  q(μ_b)² = 91914991536373201/383045380761373201 < (49/100)², strictly
  below the registered q_split = 0.490.
- E3's five ℓ₀ values agree with the draft and its bound is positive for
  every ℓ > ℓ₀ and q ∈ [0, 1].
- HD-S has 18 bands, each contiguous and VERIFIED, each q(μ_a)² ≥ (99/100)²
  and each q(μ_b)² ≤ q_split² (or zero for the five from-0+ bands). Every
  from-0+ band has a verified final box ending at μ = 1.
- The onward thresholds quoted in §5.3 also satisfy q(1/8)² ≤ (99/100)²
  and the largest q(MU1)² = 46562824/47513449 ≤ (99/100)². They do not
  differ from the ends used in the earlier HD-X audit.

## Routes to A ≥ 0

| Piece | What the route requires | Whether the record says it, and for what range |
|---|---|---|
| O2 | U₋ ≥ 0 on the exterior gives V ≥ 0 directly (§4.4) | Yes, on (0, q_*] |
| T3 | N > 0 invokes Proposition 3 (§4.1) | Yes, on its eight boxes |
| P1 | U₋ > 0 gives V > 0 directly | Yes, for q ≤ 99/100 |
| Lemma U | U₋ > 0 gives V > 0 directly | Yes, for ℓ ≥ 11 and q ≤ 1 |
| A2-E | U₋ ≥ 0 gives V ≥ 0 directly | Yes, on [q(μ_lo), 1] |
| A2-S | N > 0 invokes Proposition 3 for a C¹ design on (0, 1) | Yes, on [q(1/8), 1] |
| HD-E E1 | U₋ > 0 gives V > 0 directly | Yes, for each elementary ℓ and q ≤ 99/100 |
| HD-E E2 | U₋ > 0 gives V > 0 directly | Yes, on each of the 13 onsets up to q_split |
| HD-E E3 | U₋ > 0 gives V > 0 directly | Yes, for every ℓ > ℓ₀ and q ≤ 1 |
| HD-S | N·L·s^{2e} > 0, with the positive factor L·s^{2e}, invokes Proposition 3 | Yes, on every one of the 18 bands, including μ = 1 for the from-0+ bands |

The pencil steps inside these routes are hypotheses, not new claims proved
by this audit. In particular, the S-deformation identity, the tortoise map,
and Lemma U's monotonicity/corner arguments were not re-proved. Proposition
3's machine-checked status is taken as given.

## Hypotheses used

- The certified pieces, their controls, and their second-party status are
  hypotheses; they were not rerun. I compared their claims, ranges, and
  records, not the draft's account of them.
- The parametrisation q(μ) and its monotonicity are taken from the pieces'
  exact gates. For endpoint arithmetic I used q(μ)² = 1 − (Bμ/A)² with
  B = 2ℓ + n − 1 and A = (ℓ + n) + (ℓ − 1)μ².
- The pencil lemmas of §4.1 and §4.4 and Lemma U's steps are hypotheses.
- The frozen draft's §5.3 endpoints are taken as given from the earlier
  HD-X audit (BHM-160), as instructed. No new audit of that section was made.
- q_*² is read from `onset/runs/record/main/result.json`'s exact isolating
  interval, not re-isolated by me.

## Files and line ranges read

- `paper/stability/versions/DRAFT_v0.5.md`: 150–207, 208–315, 328–384.
- `results/onset/PREREG.md`: 1–85; `RESULT.md`: 1–70;
  `runs/record/main/result.json`: `q_star_squared_interval`, `minimal_poly_q2`.
- `results/p3/PREREG.md`: 1–65; `RESULT.md`: 1–63;
  `RULE2_RESULT.md`: 1–33; `METHOD.md`: 1–52;
  `runs/record/T3/result.json`: `result.boxes_mu`; `rule2/record/G1/result.json`: `verdict`.
- `results/a1/PREREG.md`: 1–135; `RESULT.md`: 1–91;
  `runs/record/main/result.json`: `part1` and the uniform bound.
- `results/a2/s/PREREG.md`: 1–107; `RESULT.md`: 1–64;
  `runs/record/none/result.json`: charts and `PARAM`.
- `results/a2/elementary/PREREG.md`: 1–64; `RESULT.md`: 1–55;
  `runs/record/none/result.json`: `parts`.
- `results/hd/elementary/PREREG.md`: 1–111; `RESULT.md`: 1–95;
  `RESULT_ADDENDUM_1.md`: 1–55; `runs/record/main/result.json`: `L_EL`, `E1`, `E2`, `E3`.
- `results/hd/s/PREREG.md`: 1–140; `RESULT.md`: 1–85;
  `RESULT_ADDENDUM_1.md`: 1–52; every band's `result.json`: `coverage`,
  `claim_q`, `verdict`, and the last box's `mu` and `verified`.

## Appendix A — exact range-end tables

Every row below is an exact `fractions.Fraction` comparison from
`audit_ranges.py`, not an approximate or sampled comparison. Each row's
left value, relation, right value and record source is shown. The complete
machine-readable form is `range_results.json`; the execution log is
`range_checks.log`. All 259 checks pass.

### D = 6

| Check | Left | Relation | Right | Source | OK |
|---|---|---|---|---|
| D6: T3 lower < O2's q_* interval lower end | 21576/22801 | < | 98250975923453282775110181479556452646592956062313618033845655646418970166348500804929933389/103767370865121456550439496271466377049577792779941907454834080211019555978294827145696167025 | onset result.json q_star_squared_interval; p3/PREREG.md:42 | True |
| D6: T3 lower < O2's q_* interval upper end | 21576/22801 | < | 2845287787581430822862476616601416214540084821278877924107620690877898388205588728188152536/3005039189656387103201290413774755488913110662792930961814927099700040745960805537430390561 | onset result.json q_star_squared_interval | True |
| D6: A2-S lower < T3 upper | 2961/3025 | < | 31416/32041 | a2/s/PREREG.md:10; p3/PREREG.md:42 | True |
| D6: A2-S q(1/8)^2 <= (99/100)^2 | 2961/3025 | <= | 9801/10000 | a2/s/PREREG.md:10,56 | True |
| D6: T3 lower is q(1/5)^2 | 21576/22801 | == | 21576/22801 | p3 result.json last mu-box (q decreases with mu) | True |
| D6: T3 upper is q(3/25)^2 | 31416/32041 | == | 31416/32041 | p3 result.json first mu-box (q decreases with mu) | True |
| D6: T3 has eight certified mu-boxes | 8 | == | 8 | p3/RESULT.md:18 | True |
| D6: rule-2 G1 is VERIFIED | VERIFIED | == | VERIFIED | p3/rule2/record/G1/result.json | True |
| D6 l=3: P1 and A2-E use the same mu_lo | 11/100 | == | 11/100 | a1 result.json part1.mu_lo; a2/elementary result.json parts.mu_lo | True |
| D6 l=3: P1 and A2-E have the same q(mu_lo)^2 | 134331349/137053849 | == | 134331349/137053849 | a1/a2 result.json q_at_mu_lo_squared | True |
| D6 l=3: q(mu_lo)^2 >= (99/100)^2 | 134331349/137053849 | >= | 9801/10000 | a1/PREREG.md:40-42; a2/elementary/PREREG.md:13,26 | True |
| D6 l=4: P1 and A2-E use the same mu_lo | 103/1000 | == | 103/1000 | a1 result.json part1.mu_lo; a2/elementary result.json parts.mu_lo | True |
| D6 l=4: P1 and A2-E have the same q(mu_lo)^2 | 63226555957929/64510244957929 | == | 63226555957929/64510244957929 | a1/a2 result.json q_at_mu_lo_squared | True |
| D6 l=4: q(mu_lo)^2 >= (99/100)^2 | 63226555957929/64510244957929 | >= | 9801/10000 | a1/PREREG.md:40-42; a2/elementary/PREREG.md:13,26 | True |
| D6 l=5: P1 and A2-E use the same mu_lo | 49/500 | == | 49/500 | a1 result.json part1.mu_lo; a2/elementary result.json parts.mu_lo | True |
| D6 l=5: P1 and A2-E have the same q(mu_lo)^2 | 312772999176/319113139801 | == | 312772999176/319113139801 | a1/a2 result.json q_at_mu_lo_squared | True |
| D6 l=5: q(mu_lo)^2 >= (99/100)^2 | 312772999176/319113139801 | >= | 9801/10000 | a1/PREREG.md:40-42; a2/elementary/PREREG.md:13,26 | True |
| D6 l=6: P1 and A2-E use the same mu_lo | 47/500 | == | 47/500 | a1 result.json part1.mu_lo; a2/elementary result.json parts.mu_lo | True |
| D6 l=6: P1 and A2-E have the same q(mu_lo)^2 | 27471514409/28023764409 | == | 27471514409/28023764409 | a1/a2 result.json q_at_mu_lo_squared | True |
| D6 l=6: q(mu_lo)^2 >= (99/100)^2 | 27471514409/28023764409 | >= | 9801/10000 | a1/PREREG.md:40-42; a2/elementary/PREREG.md:13,26 | True |
| D6 l=7: P1 and A2-E use the same mu_lo | 91/1000 | == | 91/1000 | a1 result.json part1.mu_lo; a2/elementary result.json parts.mu_lo | True |
| D6 l=7: P1 and A2-E have the same q(mu_lo)^2 | 29925587924649/30523890174649 | == | 29925587924649/30523890174649 | a1/a2 result.json q_at_mu_lo_squared | True |
| D6 l=7: q(mu_lo)^2 >= (99/100)^2 | 29925587924649/30523890174649 | >= | 9801/10000 | a1/PREREG.md:40-42; a2/elementary/PREREG.md:13,26 | True |
| D6 l=8: P1 and A2-E use the same mu_lo | 89/1000 | == | 89/1000 | a1 result.json part1.mu_lo; a2/elementary result.json parts.mu_lo | True |
| D6 l=8: P1 and A2-E have the same q(mu_lo)^2 | 142474321369809/145333802369809 | == | 142474321369809/145333802369809 | a1/a2 result.json q_at_mu_lo_squared | True |
| D6 l=8: q(mu_lo)^2 >= (99/100)^2 | 142474321369809/145333802369809 | >= | 9801/10000 | a1/PREREG.md:40-42; a2/elementary/PREREG.md:13,26 | True |
| D6 l=9: P1 and A2-E use the same mu_lo | 87/1000 | == | 87/1000 | a1 result.json part1.mu_lo; a2/elementary result.json parts.mu_lo | True |
| D6 l=9: P1 and A2-E have the same q(mu_lo)^2 | 2613126399136/2665281539761 | == | 2613126399136/2665281539761 | a1/a2 result.json q_at_mu_lo_squared | True |
| D6 l=9: q(mu_lo)^2 >= (99/100)^2 | 2613126399136/2665281539761 | >= | 9801/10000 | a1/PREREG.md:40-42; a2/elementary/PREREG.md:13,26 | True |
| D6 l=10: P1 and A2-E use the same mu_lo | 43/500 | == | 43/500 | a1 result.json part1.mu_lo; a2/elementary result.json parts.mu_lo | True |
| D6 l=10: P1 and A2-E have the same q(mu_lo)^2 | 12122233672881/12366763922881 | == | 12122233672881/12366763922881 | a1/a2 result.json q_at_mu_lo_squared | True |
| D6 l=10: q(mu_lo)^2 >= (99/100)^2 | 12122233672881/12366763922881 | >= | 9801/10000 | a1/PREREG.md:40-42; a2/elementary/PREREG.md:13,26 | True |
| D6: Lemma U's bound is positive | 959747/17496 | > | 0 | a1/RESULT.md:33-41 | True |
| HD-X-S q(1/8)^2 <= (99/100)^2 | 2961/3025 | <= | 9801/10000 | frozen draft:378 | True |
| HD-X-2's largest q(MU1)^2 <= (99/100)^2 | 46562824/47513449 | <= | 9801/10000 | frozen draft:379-380 | True |

### D = 7

| Check | Left | Relation | Right | Source | OK |
|---|---|---|---|---|
| D7 l=4: E1 q(mu_lo)^2 >= (99/100)^2 | 88875546247769841/90676699847769841 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D7 l=4: E1 ell is in the elementary partition | 4 | >= | 4 | hd/elementary/PREREG.md:15-17 | True |
| D7 l=4: E1 ell is at most E3's l0 | 4 | <= | 10 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D7 l=5: E1 q(mu_lo)^2 >= (99/100)^2 | 1260408306251809/1285961331251809 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D7 l=5: E1 ell is in the elementary partition | 5 | >= | 4 | hd/elementary/PREREG.md:15-17 | True |
| D7 l=5: E1 ell is at most E3's l0 | 5 | <= | 10 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D7 l=6: E1 q(mu_lo)^2 >= (99/100)^2 | 2990429575134561/3051144839134561 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D7 l=6: E1 ell is in the elementary partition | 6 | >= | 4 | hd/elementary/PREREG.md:15-17 | True |
| D7 l=6: E1 ell is at most E3's l0 | 6 | <= | 10 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D7 l=7: E1 q(mu_lo)^2 >= (99/100)^2 | 67062761304/68422526929 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D7 l=7: E1 ell is in the elementary partition | 7 | >= | 4 | hd/elementary/PREREG.md:15-17 | True |
| D7 l=7: E1 ell is at most E3's l0 | 7 | <= | 10 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D7 l=8: E1 q(mu_lo)^2 >= (99/100)^2 | 1671543602326909969/1705473242326909969 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D7 l=8: E1 ell is in the elementary partition | 8 | >= | 4 | hd/elementary/PREREG.md:15-17 | True |
| D7 l=8: E1 ell is at most E3's l0 | 8 | <= | 10 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D7 l=9: E1 q(mu_lo)^2 >= (99/100)^2 | 250379048467881/255452804717881 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D7 l=9: E1 ell is in the elementary partition | 9 | >= | 4 | hd/elementary/PREREG.md:15-17 | True |
| D7 l=9: E1 ell is at most E3's l0 | 9 | <= | 10 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D7 l=10: E1 q(mu_lo)^2 >= (99/100)^2 | 395748089556169/403768313556169 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D7 l=10: E1 ell is in the elementary partition | 10 | >= | 4 | hd/elementary/PREREG.md:15-17 | True |
| D7 l=10: E1 ell is at most E3's l0 | 10 | <= | 10 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D7 l=2: E2 q_hi is registered q_split | 237/250 | == | 237/250 | hd/elementary/PREREG.md:21-27 | True |
| D7 l=2: E2 q(mu_lo)^2 >= q_split^2 | 6872766153201/7647166153201 | >= | 56169/62500 | hd/elementary/RESULT.md:45 and PREREG.md:45-46 | True |
| D7 l=3: E2 q_hi is registered q_split | 977/1000 | == | 977/1000 | hd/elementary/PREREG.md:21-27 | True |
| D7 l=3: E2 q(mu_lo)^2 >= q_split^2 | 9686945043370161/10148120668370161 | >= | 954529/1000000 | hd/elementary/RESULT.md:45 and PREREG.md:45-46 | True |
| D7: E3's l0 is registered | 10 | == | 10 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D7: E3's uniform bound is positive | 399917/10368 | > | 0 | hd/elementary/RESULT_ADDENDUM_1.md:23-29 | True |
| D7 l=2: HD-S q(mu_b)^2 <= E2 q_split^2 | 450385526985669121/501172656585669121 | <= | 56169/62500 | hd/s result.json coverage and hd/elementary E2 q_hi | True |
| D7 l=2: HD-S q(mu_a)^2 >= (99/100)^2 | 482351496417168561/492144578017168561 | >= | 9801/10000 | hd/s/PREREG.md:32-37 and result.json coverage | True |
| D7 l=2: HD-S boxes are contiguous | True | == | True | hd/s result.json coverage.contiguous | True |
| D7 l=2: HD-S coverage is VERIFIED | VERIFIED | == | VERIFIED | hd/s result.json verdict | True |
| D7 l=3: HD-S q(mu_b)^2 <= E2 q_split^2 | 154985298094511521/162372700594511521 | <= | 954529/1000000 | hd/s result.json coverage and hd/elementary E2 q_hi | True |
| D7 l=3: HD-S q(mu_a)^2 >= (99/100)^2 | 616496957997921/629010864247921 | >= | 9801/10000 | hd/s/PREREG.md:32-37 and result.json coverage | True |
| D7 l=3: HD-S boxes are contiguous | True | == | True | hd/s result.json coverage.contiguous | True |
| D7 l=3: HD-S coverage is VERIFIED | VERIFIED | == | VERIFIED | hd/s result.json verdict | True |

### D = 8

| Check | Left | Relation | Right | Source | OK |
|---|---|---|---|---|
| D8 l=5: E1 q(mu_lo)^2 >= (99/100)^2 | 4668974966285821/4763672192848321 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D8 l=5: E1 ell is in the elementary partition | 5 | >= | 5 | hd/elementary/PREREG.md:15-17 | True |
| D8 l=5: E1 ell is at most E3's l0 | 5 | <= | 10 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D8 l=6: E1 q(mu_lo)^2 >= (99/100)^2 | 21886331153401/22329887153401 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D8 l=6: E1 ell is in the elementary partition | 6 | >= | 5 | hd/elementary/PREREG.md:15-17 | True |
| D8 l=6: E1 ell is at most E3's l0 | 6 | <= | 10 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D8 l=7: E1 q(mu_lo)^2 >= (99/100)^2 | 417695759704835689/426169882729835689 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D8 l=7: E1 ell is in the elementary partition | 7 | >= | 5 | hd/elementary/PREREG.md:15-17 | True |
| D8 l=7: E1 ell is at most E3's l0 | 7 | <= | 10 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D8 l=8: E1 q(mu_lo)^2 >= (99/100)^2 | 67062761304/68422526929 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D8 l=8: E1 ell is in the elementary partition | 8 | >= | 5 | hd/elementary/PREREG.md:15-17 | True |
| D8 l=8: E1 ell is at most E3's l0 | 8 | <= | 10 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D8 l=9: E1 q(mu_lo)^2 >= (99/100)^2 | 60367093243851/61592265509476 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D8 l=9: E1 ell is in the elementary partition | 9 | >= | 5 | hd/elementary/PREREG.md:15-17 | True |
| D8 l=9: E1 ell is at most E3's l0 | 9 | <= | 10 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D8 l=10: E1 q(mu_lo)^2 >= (99/100)^2 | 2532331545561553281/2583747108061553281 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D8 l=10: E1 ell is in the elementary partition | 10 | >= | 5 | hd/elementary/PREREG.md:15-17 | True |
| D8 l=10: E1 ell is at most E3's l0 | 10 | <= | 10 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D8 l=3: E2 q_hi is registered q_split | 118/125 | == | 118/125 | hd/elementary/PREREG.md:21-27 | True |
| D8 l=3: E2 q(mu_lo)^2 >= q_split^2 | 45546003396576/51106756912201 | >= | 13924/15625 | hd/elementary/RESULT.md:45 and PREREG.md:45-46 | True |
| D8 l=4: E2 q_hi is registered q_split | 983/1000 | == | 983/1000 | hd/elementary/PREREG.md:21-27 | True |
| D8 l=4: E2 q(mu_lo)^2 >= q_split^2 | 36170777841/37431027841 | >= | 966289/1000000 | hd/elementary/RESULT.md:45 and PREREG.md:45-46 | True |
| D8: E3's l0 is registered | 10 | == | 10 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D8: E3's uniform bound is positive | 1481614528/62748517 | > | 0 | hd/elementary/RESULT_ADDENDUM_1.md:23-29 | True |
| D8 l=2: HD-S q(mu_b)^2 <= E2 q_split^2 | 0 | <= | 0 | hd/s result.json coverage and hd/elementary E2 q_hi | True |
| D8 l=2: HD-S q(mu_a)^2 >= (99/100)^2 | 17083021501189/17429648063689 | >= | 9801/10000 | hd/s/PREREG.md:32-37 and result.json coverage | True |
| D8 l=2: HD-S boxes are contiguous | True | == | True | hd/s result.json coverage.contiguous | True |
| D8 l=2: HD-S coverage is VERIFIED | VERIFIED | == | VERIFIED | hd/s result.json verdict | True |
| D8 l=2: the from-0+ box ends at mu=1 and verifies | 1 | == | 1 | hd/s result.json last box and PREREG.md:77 | True |
| D8 l=2: the from-0+ box verifies | True | == | True | hd/s result.json last box verified | True |
| D8 l=3: HD-S q(mu_b)^2 <= E2 q_split^2 | 3684836513121/4135077513121 | <= | 13924/15625 | hd/s result.json coverage and hd/elementary E2 q_hi | True |
| D8 l=3: HD-S q(mu_a)^2 >= (99/100)^2 | 199657162856145201/203706576081145201 | >= | 9801/10000 | hd/s/PREREG.md:32-37 and result.json coverage | True |
| D8 l=3: HD-S boxes are contiguous | True | == | True | hd/s result.json coverage.contiguous | True |
| D8 l=3: HD-S coverage is VERIFIED | VERIFIED | == | VERIFIED | hd/s result.json verdict | True |
| D8 l=4: HD-S q(mu_b)^2 <= E2 q_split^2 | 978026969107944729/1012152142007944729 | <= | 966289/1000000 | hd/s result.json coverage and hd/elementary E2 q_hi | True |
| D8 l=4: HD-S q(mu_a)^2 >= (99/100)^2 | 3765525061221/3841839123721 | >= | 9801/10000 | hd/s/PREREG.md:32-37 and result.json coverage | True |
| D8 l=4: HD-S boxes are contiguous | True | == | True | hd/s result.json coverage.contiguous | True |
| D8 l=4: HD-S coverage is VERIFIED | VERIFIED | == | VERIFIED | hd/s result.json verdict | True |

### D = 9

| Check | Left | Relation | Right | Source | OK |
|---|---|---|---|---|
| D9 l=6: E1 q(mu_lo)^2 >= (99/100)^2 | 463823412241849/473223768241849 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D9 l=6: E1 ell is in the elementary partition | 6 | >= | 6 | hd/elementary/PREREG.md:15-17 | True |
| D9 l=6: E1 ell is at most E3's l0 | 6 | <= | 11 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D9 l=7: E1 q(mu_lo)^2 >= (99/100)^2 | 484312610547815049/494133420547815049 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D9 l=7: E1 ell is in the elementary partition | 7 | >= | 6 | hd/elementary/PREREG.md:15-17 | True |
| D9 l=7: E1 ell is at most E3's l0 | 7 | <= | 11 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D9 l=8: E1 q(mu_lo)^2 >= (99/100)^2 | 15447737457124281/15761381557124281 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D9 l=8: E1 ell is in the elementary partition | 8 | >= | 6 | hd/elementary/PREREG.md:15-17 | True |
| D9 l=8: E1 ell is at most E3's l0 | 8 | <= | 11 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D9 l=9: E1 q(mu_lo)^2 >= (99/100)^2 | 67062761304/68422526929 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D9 l=9: E1 ell is in the elementary partition | 9 | >= | 6 | hd/elementary/PREREG.md:15-17 | True |
| D9 l=9: E1 ell is at most E3's l0 | 9 | <= | 11 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D9 l=10: E1 q(mu_lo)^2 >= (99/100)^2 | 1057075793074089/1078512693074089 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D9 l=10: E1 ell is in the elementary partition | 10 | >= | 6 | hd/elementary/PREREG.md:15-17 | True |
| D9 l=10: E1 ell is at most E3's l0 | 10 | <= | 11 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D9 l=11: E1 q(mu_lo)^2 >= (99/100)^2 | 32048802264866241/32699460328866241 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D9 l=11: E1 ell is in the elementary partition | 11 | >= | 6 | hd/elementary/PREREG.md:15-17 | True |
| D9 l=11: E1 ell is at most E3's l0 | 11 | <= | 11 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D9 l=3: E2 q_hi is registered q_split | 921/1000 | == | 921/1000 | hd/elementary/PREREG.md:21-27 | True |
| D9 l=3: E2 q(mu_lo)^2 >= q_split^2 | 24612731484910569/29013727084910569 | >= | 848241/1000000 | hd/elementary/RESULT.md:45 and PREREG.md:45-46 | True |
| D9 l=4: E2 q_hi is registered q_split | 119/125 | == | 119/125 | hd/elementary/PREREG.md:21-27 | True |
| D9 l=4: E2 q(mu_lo)^2 >= q_split^2 | 4424493504621369/4881811729621369 | >= | 14161/15625 | hd/elementary/RESULT.md:45 and PREREG.md:45-46 | True |
| D9 l=5: E2 q_hi is registered q_split | 987/1000 | == | 987/1000 | hd/elementary/PREREG.md:21-27 | True |
| D9 l=5: E2 q(mu_lo)^2 >= q_split^2 | 88535629683843441/90882063283843441 | >= | 974169/1000000 | hd/elementary/RESULT.md:45 and PREREG.md:45-46 | True |
| D9: E3's l0 is registered | 11 | == | 11 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D9: E3's uniform bound is positive | 17257/2401 | > | 0 | hd/elementary/RESULT_ADDENDUM_1.md:23-29 | True |
| D9 l=2: HD-S q(mu_b)^2 <= E2 q_split^2 | 0 | <= | 0 | hd/s result.json coverage and hd/elementary E2 q_hi | True |
| D9 l=2: HD-S q(mu_a)^2 >= (99/100)^2 | 796755993449624481/812910403449624481 | >= | 9801/10000 | hd/s/PREREG.md:32-37 and result.json coverage | True |
| D9 l=2: HD-S boxes are contiguous | True | == | True | hd/s result.json coverage.contiguous | True |
| D9 l=2: HD-S coverage is VERIFIED | VERIFIED | == | VERIFIED | hd/s result.json verdict | True |
| D9 l=2: the from-0+ box ends at mu=1 and verifies | 1 | == | 1 | hd/s result.json last box and PREREG.md:77 | True |
| D9 l=2: the from-0+ box verifies | True | == | True | hd/s result.json last box verified | True |
| D9 l=3: HD-S q(mu_b)^2 <= E2 q_split^2 | 13843592400702961/16320645300702961 | <= | 848241/1000000 | hd/s result.json coverage and hd/elementary E2 q_hi | True |
| D9 l=3: HD-S q(mu_a)^2 >= (99/100)^2 | 1711069078242249/1745761178242249 | >= | 9801/10000 | hd/s/PREREG.md:32-37 and result.json coverage | True |
| D9 l=3: HD-S boxes are contiguous | True | == | True | hd/s result.json coverage.contiguous | True |
| D9 l=3: HD-S coverage is VERIFIED | VERIFIED | == | VERIFIED | hd/s result.json verdict | True |
| D9 l=4: HD-S q(mu_b)^2 <= E2 q_split^2 | 1812171689673769/1999642553673769 | <= | 14161/15625 | hd/s result.json coverage and hd/elementary E2 q_hi | True |
| D9 l=4: HD-S q(mu_a)^2 >= (99/100)^2 | 291488937834369/297405994084369 | >= | 9801/10000 | hd/s/PREREG.md:32-37 and result.json coverage | True |
| D9 l=4: HD-S boxes are contiguous | True | == | True | hd/s result.json coverage.contiguous | True |
| D9 l=4: HD-S coverage is VERIFIED | VERIFIED | == | VERIFIED | hd/s result.json verdict | True |
| D9 l=5: HD-S q(mu_b)^2 <= E2 q_split^2 | 38425874043609/39445974043609 | <= | 974169/1000000 | hd/s result.json coverage and hd/elementary E2 q_hi | True |
| D9 l=5: HD-S q(mu_a)^2 >= (99/100)^2 | 88875546247769841/90676699847769841 | >= | 9801/10000 | hd/s/PREREG.md:32-37 and result.json coverage | True |
| D9 l=5: HD-S boxes are contiguous | True | == | True | hd/s result.json coverage.contiguous | True |
| D9 l=5: HD-S coverage is VERIFIED | VERIFIED | == | VERIFIED | hd/s result.json verdict | True |

### D = 10

| Check | Left | Relation | Right | Source | OK |
|---|---|---|---|---|
| D10 l=6: E1 q(mu_lo)^2 >= (99/100)^2 | 1580398467335649/1612456711335649 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D10 l=6: E1 ell is in the elementary partition | 6 | >= | 6 | hd/elementary/PREREG.md:15-17 | True |
| D10 l=6: E1 ell is at most E3's l0 | 6 | <= | 13 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D10 l=7: E1 q(mu_lo)^2 >= (99/100)^2 | 1260408306251809/1285961331251809 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D10 l=7: E1 ell is in the elementary partition | 7 | >= | 6 | hd/elementary/PREREG.md:15-17 | True |
| D10 l=7: E1 ell is at most E3's l0 | 7 | <= | 13 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D10 l=8: E1 q(mu_lo)^2 >= (99/100)^2 | 4048726820785569/4130846664785569 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D10 l=8: E1 ell is in the elementary partition | 8 | >= | 6 | hd/elementary/PREREG.md:15-17 | True |
| D10 l=8: E1 ell is at most E3's l0 | 8 | <= | 13 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D10 l=9: E1 q(mu_lo)^2 >= (99/100)^2 | 44645608049199661/45551241838262161 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D10 l=9: E1 ell is in the elementary partition | 9 | >= | 6 | hd/elementary/PREREG.md:15-17 | True |
| D10 l=9: E1 ell is at most E3's l0 | 9 | <= | 13 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D10 l=10: E1 q(mu_lo)^2 >= (99/100)^2 | 67062761304/68422526929 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D10 l=10: E1 ell is in the elementary partition | 10 | >= | 6 | hd/elementary/PREREG.md:15-17 | True |
| D10 l=10: E1 ell is at most E3's l0 | 10 | <= | 13 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D10 l=11: E1 q(mu_lo)^2 >= (99/100)^2 | 2179183094109/2223388156609 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D10 l=11: E1 ell is in the elementary partition | 11 | >= | 6 | hd/elementary/PREREG.md:15-17 | True |
| D10 l=11: E1 ell is at most E3's l0 | 11 | <= | 13 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D10 l=12: E1 q(mu_lo)^2 >= (99/100)^2 | 247285019541480921/252302616766480921 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D10 l=12: E1 ell is in the elementary partition | 12 | >= | 6 | hd/elementary/PREREG.md:15-17 | True |
| D10 l=12: E1 ell is at most E3's l0 | 12 | <= | 13 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D10 l=13: E1 q(mu_lo)^2 >= (99/100)^2 | 250379048467881/255452804717881 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D10 l=13: E1 ell is in the elementary partition | 13 | >= | 6 | hd/elementary/PREREG.md:15-17 | True |
| D10 l=13: E1 ell is at most E3's l0 | 13 | <= | 13 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D10 l=3: E2 q_hi is registered q_split | 49/100 | == | 49/100 | hd/elementary/PREREG.md:21-27 | True |
| D10 l=3: E2 q(mu_lo)^2 >= q_split^2 | 919645821/3830248321 | >= | 2401/10000 | hd/elementary/RESULT.md:45 and PREREG.md:45-46 | True |
| D10 l=4: E2 q_hi is registered q_split | 23/25 | == | 23/25 | hd/elementary/PREREG.md:21-27 | True |
| D10 l=4: E2 q(mu_lo)^2 >= q_split^2 | 2174750600176/2569291615801 | >= | 529/625 | hd/elementary/RESULT.md:45 and PREREG.md:45-46 | True |
| D10 l=5: E2 q_hi is registered q_split | 961/1000 | == | 961/1000 | hd/elementary/PREREG.md:21-27 | True |
| D10 l=5: E2 q(mu_lo)^2 >= q_split^2 | 24494910640101/26521974702601 | >= | 923521/1000000 | hd/elementary/RESULT.md:45 and PREREG.md:45-46 | True |
| D10: E3's l0 is registered | 13 | == | 13 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D10: E3's uniform bound is positive | 79325/16384 | > | 0 | hd/elementary/RESULT_ADDENDUM_1.md:23-29 | True |
| D10 l=2: HD-S q(mu_b)^2 <= E2 q_split^2 | 0 | <= | 0 | hd/s result.json coverage and hd/elementary E2 q_hi | True |
| D10 l=2: HD-S q(mu_a)^2 >= (99/100)^2 | 3841215986197681/3919140742447681 | >= | 9801/10000 | hd/s/PREREG.md:32-37 and result.json coverage | True |
| D10 l=2: HD-S boxes are contiguous | True | == | True | hd/s result.json coverage.contiguous | True |
| D10 l=2: HD-S coverage is VERIFIED | VERIFIED | == | VERIFIED | hd/s result.json verdict | True |
| D10 l=2: the from-0+ box ends at mu=1 and verifies | 1 | == | 1 | hd/s result.json last box and PREREG.md:77 | True |
| D10 l=2: the from-0+ box verifies | True | == | True | hd/s result.json last box verified | True |
| D10 l=3: HD-S q(mu_b)^2 <= E2 q_split^2 | 91914991536373201/383045380761373201 | <= | 2401/10000 | hd/s result.json coverage and hd/elementary E2 q_hi | True |
| D10 l=3: HD-S q(mu_a)^2 >= (99/100)^2 | 1164187484726301/1187794936288801 | >= | 9801/10000 | hd/s/PREREG.md:32-37 and result.json coverage | True |
| D10 l=3: HD-S boxes are contiguous | True | == | True | hd/s result.json coverage.contiguous | True |
| D10 l=3: HD-S coverage is VERIFIED | VERIFIED | == | VERIFIED | hd/s result.json verdict | True |
| D10 l=3: HD-S starts strictly below q_split=0.490 | 91914991536373201/383045380761373201 | < | 2401/10000 | hd/s result.json coverage.q(mu_b)^2; hd/s/RESULT.md:50-51 | True |
| D10 l=4: HD-S q(mu_b)^2 <= E2 q_split^2 | 142513652343129921/168386374843129921 | <= | 529/625 | hd/s result.json coverage and hd/elementary E2 q_hi | True |
| D10 l=4: HD-S q(mu_a)^2 >= (99/100)^2 | 616496957997921/629010864247921 | >= | 9801/10000 | hd/s/PREREG.md:32-37 and result.json coverage | True |
| D10 l=4: HD-S boxes are contiguous | True | == | True | hd/s result.json coverage.contiguous | True |
| D10 l=4: HD-S coverage is VERIFIED | VERIFIED | == | VERIFIED | hd/s result.json verdict | True |
| D10 l=5: HD-S q(mu_b)^2 <= E2 q_split^2 | 949834170649/1028514420649 | <= | 923521/1000000 | hd/s result.json coverage and hd/elementary E2 q_hi | True |
| D10 l=5: HD-S q(mu_a)^2 >= (99/100)^2 | 6517045060605261/6649208824667761 | >= | 9801/10000 | hd/s/PREREG.md:32-37 and result.json coverage | True |
| D10 l=5: HD-S boxes are contiguous | True | == | True | hd/s result.json coverage.contiguous | True |
| D10 l=5: HD-S coverage is VERIFIED | VERIFIED | == | VERIFIED | hd/s result.json verdict | True |

### D = 11

| Check | Left | Relation | Right | Source | OK |
|---|---|---|---|---|
| D11 l=7: E1 q(mu_lo)^2 >= (99/100)^2 | 63226555957929/64510244957929 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D11 l=7: E1 ell is in the elementary partition | 7 | >= | 7 | hd/elementary/PREREG.md:15-17 | True |
| D11 l=7: E1 ell is at most E3's l0 | 7 | <= | 14 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D11 l=8: E1 q(mu_lo)^2 >= (99/100)^2 | 1098057088216569/1120335488216569 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D11 l=8: E1 ell is in the elementary partition | 8 | >= | 7 | hd/elementary/PREREG.md:15-17 | True |
| D11 l=8: E1 ell is at most E3's l0 | 8 | <= | 14 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D11 l=9: E1 q(mu_lo)^2 >= (99/100)^2 | 312772999176/319113139801 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D11 l=9: E1 ell is in the elementary partition | 9 | >= | 7 | hd/elementary/PREREG.md:15-17 | True |
| D11 l=9: E1 ell is at most E3's l0 | 9 | <= | 14 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D11 l=10: E1 q(mu_lo)^2 >= (99/100)^2 | 3569249455974032721/3641653502374032721 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D11 l=10: E1 ell is in the elementary partition | 10 | >= | 7 | hd/elementary/PREREG.md:15-17 | True |
| D11 l=10: E1 ell is at most E3's l0 | 10 | <= | 14 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D11 l=11: E1 q(mu_lo)^2 >= (99/100)^2 | 67062761304/68422526929 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D11 l=11: E1 ell is in the elementary partition | 11 | >= | 7 | hd/elementary/PREREG.md:15-17 | True |
| D11 l=11: E1 ell is at most E3's l0 | 11 | <= | 14 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D11 l=12: E1 q(mu_lo)^2 >= (99/100)^2 | 4361587221411889401/4449962619811889401 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D11 l=12: E1 ell is in the elementary partition | 12 | >= | 7 | hd/elementary/PREREG.md:15-17 | True |
| D11 l=12: E1 ell is at most E3's l0 | 12 | <= | 14 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D11 l=13: E1 q(mu_lo)^2 >= (99/100)^2 | 1168800942713829/1192481331776329 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D11 l=13: E1 ell is in the elementary partition | 13 | >= | 7 | hd/elementary/PREREG.md:15-17 | True |
| D11 l=13: E1 ell is at most E3's l0 | 13 | <= | 14 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D11 l=14: E1 q(mu_lo)^2 >= (99/100)^2 | 930301408094161/949171744094161 | >= | 9801/10000 | hd/elementary/PREREG.md:15-17,45-46 | True |
| D11 l=14: E1 ell is in the elementary partition | 14 | >= | 7 | hd/elementary/PREREG.md:15-17 | True |
| D11 l=14: E1 ell is at most E3's l0 | 14 | <= | 14 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D11 l=4: E2 q_hi is registered q_split | 897/1000 | == | 897/1000 | hd/elementary/PREREG.md:21-27 | True |
| D11 l=4: E2 q(mu_lo)^2 >= q_split^2 | 13702767677521/17029743677521 | >= | 804609/1000000 | hd/elementary/RESULT.md:45 and PREREG.md:45-46 | True |
| D11 l=5: E2 q_hi is registered q_split | 929/1000 | == | 929/1000 | hd/elementary/PREREG.md:21-27 | True |
| D11 l=5: E2 q(mu_lo)^2 >= q_split^2 | 111052634543953201/128663251568953201 | >= | 863041/1000000 | hd/elementary/RESULT.md:45 and PREREG.md:45-46 | True |
| D11 l=6: E2 q_hi is registered q_split | 121/125 | == | 121/125 | hd/elementary/PREREG.md:21-27 | True |
| D11 l=6: E2 q(mu_lo)^2 >= q_split^2 | 82385946456/87917587081 | >= | 14641/15625 | hd/elementary/RESULT.md:45 and PREREG.md:45-46 | True |
| D11: E3's l0 is registered | 14 | == | 14 | hd/elementary/RESULT.md:14-20 and E3.l0 | True |
| D11: E3's uniform bound is positive | 19870/6561 | > | 0 | hd/elementary/RESULT_ADDENDUM_1.md:23-29 | True |
| D11 l=2: HD-S q(mu_b)^2 <= E2 q_split^2 | 0 | <= | 0 | hd/s result.json coverage and hd/elementary E2 q_hi | True |
| D11 l=2: HD-S q(mu_a)^2 >= (99/100)^2 | 211474330206729/215767514206729 | >= | 9801/10000 | hd/s/PREREG.md:32-37 and result.json coverage | True |
| D11 l=2: HD-S boxes are contiguous | True | == | True | hd/s result.json coverage.contiguous | True |
| D11 l=2: HD-S coverage is VERIFIED | VERIFIED | == | VERIFIED | hd/s result.json verdict | True |
| D11 l=2: the from-0+ box ends at mu=1 and verifies | 1 | == | 1 | hd/s result.json last box and PREREG.md:77 | True |
| D11 l=2: the from-0+ box verifies | True | == | True | hd/s result.json last box verified | True |
| D11 l=3: HD-S q(mu_b)^2 <= E2 q_split^2 | 0 | <= | 0 | hd/s result.json coverage and hd/elementary E2 q_hi | True |
| D11 l=3: HD-S q(mu_a)^2 >= (99/100)^2 | 153891955293609/157016011543609 | >= | 9801/10000 | hd/s/PREREG.md:32-37 and result.json coverage | True |
| D11 l=3: HD-S boxes are contiguous | True | == | True | hd/s result.json coverage.contiguous | True |
| D11 l=3: HD-S coverage is VERIFIED | VERIFIED | == | VERIFIED | hd/s result.json verdict | True |
| D11 l=3: the from-0+ box ends at mu=1 and verifies | 1 | == | 1 | hd/s result.json last box and PREREG.md:77 | True |
| D11 l=3: the from-0+ box verifies | True | == | True | hd/s result.json last box verified | True |
| D11 l=4: HD-S q(mu_b)^2 <= E2 q_split^2 | 90451546986883929/112426644586883929 | <= | 804609/1000000 | hd/s result.json coverage and hd/elementary E2 q_hi | True |
| D11 l=4: HD-S q(mu_a)^2 >= (99/100)^2 | 1666516108576123609/1700313254176123609 | >= | 9801/10000 | hd/s/PREREG.md:32-37 and result.json coverage | True |
| D11 l=4: HD-S boxes are contiguous | True | == | True | hd/s result.json coverage.contiguous | True |
| D11 l=4: HD-S coverage is VERIFIED | VERIFIED | == | VERIFIED | hd/s result.json verdict | True |
| D11 l=5: HD-S q(mu_b)^2 <= E2 q_split^2 | 1974131929/2287421929 | <= | 863041/1000000 | hd/s result.json coverage and hd/elementary E2 q_hi | True |
| D11 l=5: HD-S q(mu_a)^2 >= (99/100)^2 | 134331349/137053849 | >= | 9801/10000 | hd/s/PREREG.md:32-37 and result.json coverage | True |
| D11 l=5: HD-S boxes are contiguous | True | == | True | hd/s result.json coverage.contiguous | True |
| D11 l=5: HD-S coverage is VERIFIED | VERIFIED | == | VERIFIED | hd/s result.json verdict | True |
| D11 l=6: HD-S q(mu_b)^2 <= E2 q_split^2 | 15357181301769/16389437301769 | <= | 14641/15625 | hd/s result.json coverage and hd/elementary E2 q_hi | True |
| D11 l=6: HD-S q(mu_a)^2 >= (99/100)^2 | 88875546247769841/90676699847769841 | >= | 9801/10000 | hd/s/PREREG.md:32-37 and result.json coverage | True |
| D11 l=6: HD-S boxes are contiguous | True | == | True | hd/s result.json coverage.contiguous | True |
| D11 l=6: HD-S coverage is VERIFIED | VERIFIED | == | VERIFIED | hd/s result.json verdict | True |

BHM-191 assembly audit: `[kimi-folder]/bhm-assembly-audit-2026-11-21/AUDIT.md` — items 1–3 SOUND; all 259 exact range-end checks pass; only A2-S's lower decimal needs correction from 0.98937 to 0.98936.
