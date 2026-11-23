# CHECKS — files read and small computations for READING.md (draft of 2026-10-23)

## A. Setting

- Host host-0 (the session's host), 2026-10-23, 12:30–13:05 EDT. Read-only everywhere except this working folder; no git
  command that changes state (only `git log`, `git show --stat`, `git diff`, `git rev-parse`); no messages; nothing on other nodes.
- bh-modes at `b22c087` (the last commit, 12:29:59 −04:00, only fills in BHM-083's commit cell; `cf129f2` before it).
- Every computation ran under `ulimit -v 4000000` and `timeout 600`. Exact checks used Python `fractions` (system
  `/usr/bin/python3 -I`); symbolic checks used sympy 1.14.0 in `[python-2]/bin/python -I` (Python 3.12.8). No bh-modes code
  was imported or run: the D = 6 formulas were copied from `TARGET.md` §1 (l. 23-24) and the general-n U₋, H₋ from
  `code/ki/potentials.py` (l. 23-42), so the A2 checks test consistency with bh-modes' transcription, not S5 itself.
- Scripts are in `[workdir]/scripts/`; outputs in `[workdir]/*.out` and `[workdir]/hd_reading_draft/outputs/` (hashes in E).

## B. Files read, with SHA-256 (paths relative to `[repository]` unless they start with `[deliveries]`)

```
a4426f34c407f9a13f62b8513e26f64181b0f8f26b170ec1e8702c7dff0b89c3  results/hd/STAGE_REPORT.md  [read in full]
a97bf15b76e9676e8ba3ef067da18936356a418a0c7d701c66640d0bbca6c3b9  results/hd/elementary/RESULT.md  [read in full]
12ddc5fdd43208007f583f9b4a9bc65624a2589f9de3ce2690c4a392d7e88209  results/hd/elementary/PREREG.md  [hashed only (not read)]
1c799e3804375923477c3e3cfb51b9c0a5cd7a2d1471bd0963266ab5ddee3a1c  results/hd/pilot/RESULT.md  [read in full]
a152da20f880a2705e80e324e97326e06f15642c09a17e0e02f64c19cc29ccf8  results/hd/pilot/PREREG.md  [read in full]
3c6a5a1b5decda0708f48de78629932ceb3a34c978de01c89d9abfbfbeb8e230  results/hd/pilot/PREREG_ADDENDUM_1.md  [read in full]
24fc3a7c31872f353628b329421ebc73428f9cadd38c4469c1d4c4368119ec7b  results/hd/s/RESULT.md  [read in full]
e2adad67c875915dea47effee0d440d5e5bc06643cef22e8f467c0cea92edc66  results/hd/s/PREREG.md  [read in full]
e5e9c7df35402576e80c2ac45ec63a36faa3535d3a48352c795a0c827cba416d  results/hd/s/briefs/BRIEF_kimi_2026-10-23.md  [read in full]
1339b7fbd0c0761e055e375501bbb857485fc728c40c5c2b2bf2e0e19a8703dd  results/hd/s/briefs/BRIEF_ib-blind_2026-10-23.md  [read in full]
b895ecba9a23c34af45423913cbf2af07ab2549ab1b3855ca4be9e596fde7494  TARGET_HD.md  [read in full]
01fa84643e2f567a91f9f9db3dd39fe75db6f8d3d1c7f57d76793459df6670b2  TARGET_HD_ADDENDUM_1.md  [read in full]
d8207fbfa6b8cd157b5f792e806c2bea49da5ccabffec1bed29feb96beed9c5e  TARGET_A2.md  [read in full]
9dfbc64602583872959e12b684b9138e2352dd09963dc14840cb1389e4c7dd27  TARGET.md  [read l. 1-60]
5f4662f0a3a641abfbba9186e8938bbff16035098d34de794fc5db9f5996989e  RULES.md  [read in full]
88e4038aa53dfb779cda35107bd4a9aaabe0006f3a6dd3120387a957c55e7d4b  REGISTRY.md  [read rows BHM-010, 017, 021-023, 025, 030, 035, 046, 058, 066-083 (grep)]
eaa6d62aabe212bed4f8f6f2686080feebc58fc8a22c20cf6cb347177c01fecf  SEALED.sha256  [all 346 entries verified (C1)]
8a4c4d71b11366981734d73705dfdd186a259c64bfd9f5e1b6a7bc9ff9c0b30d  results/p3/METHOD.md  [read in full]
25fc9a35d0efec47ce5b604e65d0d33d952600b0f164e0e4713867679ac7f4d3  results/p3/METHOD_ADDENDUM_1.md  [read in full]
2b26da61e9faf2f75b76d6ded3b071b6f393c06546e323e33896463c769bc5de  results/p3/audits/fable_2026-10-22/AUDIT.md  [read l. 1-60, grep]
7b38c5e665e5fbea08c253897bc8ee981416dcbfac7f0eb775c20c40fbe4d155  results/p3/audits/kimi_2026-10-22/AUDIT.md  [grep (l. 18-29, 81-84, 112)]
9cbce71a5027e8e02f845eacab87fabf0f3f51364dc4ba8d35b5921bb56b8061  lean/lean_p3_sdeformation_2026-10-22/lean/BHModesP3.lean  [read l. 1-30, 205-250, 350-372, grep]
2001288a4388358fd0e1c4246aac4eda3d4c96bb71fb3b12b6cf96d4a276bd9d  lean/lean_p3_sdeformation_erratum_2026-10-23/ERRATUM.md  [read l. 1-60]
8a67a9e6d381a6a272465ce1ecf2f97ba167789e03561705ba796ded3773e410  code/hd/scert.py  [read in full]
27f7bac39f0d36a763add5999a53ed1449fe4a1ccff899a9d80192fc4107f909  code/hd/pilot.py  [git diff 8c2d6d2..710488b only]
b77e92151ca9d7f668bdcd9fb1bcdbcec0feadb27b74bc81d1bc63eeefc57014  code/hd/elementary.py  [hashed only (prefix compared with RESULT)]
7d686b40ad32654445ba89e4fedd03d3e3e9a375045f8311218427c3cb21328f  code/ki/potentials.py  [read l. 1-70 (U_minus, H_minus, the n = 4 forms)]
29c30345dec7b2fe53bfae75edda38cddb4bcbac098567ae3dc2a7cfc7fff8ab  code/qnm1c/common.py  [read provenance(), l. 91-116]
c479f3119e6b08c72cd882d251ec77d9a0f65b2b1a9d7e9e07bf9a6a77c56583  code/compare_runs.py  [grep (MASK_KEYS, l. 12)]
17954fc041e1119322b5786540308b8598a4d2a103e18b387ba7686329d7b55c  code/p3/scert.py  [hashed only]
a0b1ec5c952055ed2519b01ae3040f2347c8864990e3fd32ae733dcaadebfb8c  code/onset/bernstein.py  [hashed only (prefix compared with RESULT)]
ab9c97ee203c7e6cd47f5f97d8b1f8ec93aa972d681dbf0482c22c8375501198  kit/hd/run_pilot.sh  [read in full]
5a949ed1fcf4076eb2ba8f99abf63d491fe72e5765c3d3f4f674a1c4dac5a8f1  [deliveries]/ib-blind_hd-s_2026-10-23/VERDICT.md  [read in full]
7addc5911fdda10724a222558d26421dc05e8b016b12eb650e9d9f38ddfb1b87  [deliveries]/ib-blind_hd-s_2026-10-23/PREREG.md  [read l. 40-70, grep]
23f926e19f289b371346de2428faac68920a9d00ebbfa5b1d720ca6557c0ee80  [deliveries]/ib-blind_hd-s_2026-10-23/TRANSCRIPTION.md  [read l. 110-122, grep]
5a3d5aa62096aa59b9c96a7fa54378b06734ac2c99619cc3bc0ce4d444dccfc7  [deliveries]/ib-blind_hd-s_2026-10-23/SHA256SUMS  [verified, 152 OK (C1)]
ada053a6301eac703f5b21edf3c558edad973c484f167c17b080cc7016a1a691  [deliveries]/ib-lead_a1_reading_2026-10-23/READING.md  [read l. 1-40, 85-125]
```

Records and logs read programmatically are listed in D.

## C. Computations (command, then output, verbatim)

**C1. Seals.** `STAGE_REPORT.md` = `a4426f34c407f9a1…` and `TARGET_A2.md` = `d8207fbfa6b8cd15…` (B). Then:
```
$ grep -v "^#" SEALED.sha256 | sha256sum -c | count
    346 OK
$ (cd [deliveries]/ib-blind_hd-s_2026-10-23 && sha256sum -c SHA256SUMS | count)
    152 OK
```

**C2. HD-S intervals and coverage, exact** (`scripts/check_intervals.py`; Fractions). For each band: q(μ)² = 1 − (Bμ/A)² from
μ_a, μ_b, compared with the record; inward test of the JSON and RESULT.md decimals; q(μ_a)² ≥ (99/100)²; onset bands q(μ_b)² ≤
q_split² and HD-E's μ_lo ≤ μ_b; contiguity; every box verified.
`$ /usr/bin/python3 -I check_intervals.py [repository]`
```
D l | exact q_lo..q_hi (float) | JSON inward | RESULT.md | inward ok | cover ok | mu_lo(HD-E) <= mu_b
7 2 | 0.947978590..0.990000611 | ['0.94798', '0.99000'] | [0.94798, 0.99000] | json True res True | recomp True claim True qmax True lo True contig True (9 boxes) verified True | 176/625 <= 2817/10000: True
7 3 | 0.976986909..0.990002738 | ['0.97699', '0.99000'] | [0.97699, 0.99000] | json True res True | recomp True claim True qmax True lo True contig True (5 boxes) verified True | 859/5000 <= 1719/10000: True
8 2 | 0.000000000..0.990006474 | ['0.00000', '0.99000'] | [0, 0.99000] | json True res True | recomp True claim True qmax True lo True contig True (22 boxes) verified True | n/a (from 0+)
8 3 | 0.943989763..0.990010779 | ['0.94399', '0.99001'] | [0.94399, 0.99001] | json True res True | recomp True claim True qmax True lo True contig True (10 boxes) verified True | 343/1250 <= 549/2000: True
8 4 | 0.982997733..0.990018212 | ['0.98300', '0.99001'] | [0.98300, 0.99001] | json True res True | recomp True claim True qmax True lo True contig True (3 boxes) verified True | 71/500 <= 1421/10000: True
9 2 | 0.000000000..0.990013983 | ['0.00000', '0.99001'] | [0, 0.99001] | json True res True | recomp True claim True qmax True lo True contig True (22 boxes) verified True | n/a (from 0+)
9 3 | 0.920991748..0.990014045 | ['0.92100', '0.99001'] | [0.92100, 0.99001] | json True res True | recomp True claim True qmax True lo True contig True (11 boxes) verified True | 3317/10000 <= 1659/5000: True
9 4 | 0.951970489..0.990002247 | ['0.95198', '0.99000'] | [0.95198, 0.99000] | json True res True | recomp True claim True qmax True lo True contig True (9 boxes) verified True | 611/2500 <= 489/2000: True
9 5 | 0.986984961..0.990018451 | ['0.98699', '0.99001'] | [0.98699, 0.99001] | json True res True | recomp True claim True qmax True lo True contig True (2 boxes) verified True | 1211/10000 <= 303/2500: True
10 2 | 0.000000000..0.990008524 | ['0.00000', '0.99000'] | [0, 0.99000] | json True res True | recomp True claim True qmax True lo True contig True (22 boxes) verified True | n/a (from 0+)
10 3 | 0.489855582..0.990012615 | ['0.48986', '0.99001'] | [0.48986, 0.99001] | json True res True | recomp True claim True qmax True lo True contig True (21 boxes) verified True | 83/100 <= 8301/10000: True
10 4 | 0.919972322..0.990002738 | ['0.91998', '0.99000'] | [0.91998, 0.99000] | json True res True | recomp True claim True qmax True lo True contig True (11 boxes) verified True | 201/625 <= 3217/10000: True
10 5 | 0.960989632..0.990011811 | ['0.96099', '0.99001'] | [0.96099, 0.99001] | json True res True | recomp True claim True qmax True lo True contig True (8 boxes) verified True | 134/625 <= 429/2000: True
11 2 | 0.000000000..0.990001380 | ['0.00000', '0.99000'] | [0, 0.99000] | json True res True | recomp True claim True qmax True lo True contig True (22 boxes) verified True | n/a (from 0+)
11 3 | 0.000000000..0.990001809 | ['0.00000', '0.99000'] | [0, 0.99000] | json True res True | recomp True claim True qmax True lo True contig True (23 boxes) verified True | n/a (from 0+)
11 4 | 0.896960617..0.990011610 | ['0.89697', '0.99001'] | [0.89697, 0.99001] | json True res True | recomp True claim True qmax True lo True contig True (13 boxes) verified True | 741/2000 <= 1853/5000: True
11 5 | 0.928998358..0.990017952 | ['0.92900', '0.99001'] | [0.92900, 0.99001] | json True res True | recomp True claim True qmax True lo True contig True (11 boxes) verified True | 2949/10000 <= 59/200: True
11 6 | 0.967996382..0.990018451 | ['0.96800', '0.99001'] | [0.96800, 0.99001] | json True res True | recomp True claim True qmax True lo True contig True (7 boxes) verified True | 119/625 <= 381/2000: True
ALL OK
```

**C3. HD-E bounds and coverage** (`scripts/check_hde.py`; Fractions). Quoted E3 bounds (stage report l. 31; HD-E RESULT l. 51-55)
against the record's exact rationals; E1/E2 coverage recomputed.
`$ /usr/bin/python3 -I check_hde.py [repository]`
```
== E3: quoted bounds vs exact
D = 7: exact 399917/10368 = 38.572242; stage report '>= 38.6' inward: False; HD-E RESULT '>= 38.57' inward: True
D = 8: exact 1481614528/62748517 = 23.611945; stage report '>= 23.6' inward: True; HD-E RESULT '>= 23.61' inward: True
D = 9: exact 17257/2401 = 7.187422; stage report '>= 7.19' inward: False; HD-E RESULT '>= 7.187' inward: True
D = 10: exact 79325/16384 = 4.841614; stage report '>= 4.84' inward: True; HD-E RESULT '>= 4.842' inward: False
D = 11: exact 19870/6561 = 3.028502; stage report '>= 3.03' inward: False; HD-E RESULT '>= 3.029' inward: False

== E1 coverage (q <= 99/100) and E2 coverage (q <= q_split)
E2 D = 7 l = 2: mu_lo 176/625, q(mu_lo) = 0.948016 >= q_hi 237/250: True; U lower bound 345.024; leaves 7
E2 D = 7 l = 3: mu_lo 859/5000, q(mu_lo) = 0.977014 >= q_hi 977/1000: True; U lower bound 2843.4; leaves 1
E2 D = 8 l = 3: mu_lo 343/1250, q(mu_lo) = 0.944030 >= q_hi 118/125: True; U lower bound 1793.41; leaves 1
E2 D = 8 l = 4: mu_lo 71/500, q(mu_lo) = 0.983022 >= q_hi 983/1000: True; U lower bound 10519.4; leaves 1
E2 D = 9 l = 3: mu_lo 3317/10000, q(mu_lo) = 0.921039 >= q_hi 921/1000: True; U lower bound 3593.2; leaves 3
E2 D = 9 l = 4: mu_lo 611/2500, q(mu_lo) = 0.952009 >= q_hi 119/125: True; U lower bound 7442.31; leaves 1
E2 D = 9 l = 5: mu_lo 1211/10000, q(mu_lo) = 0.987006 >= q_hi 987/1000: True; U lower bound 35853.8; leaves 1
E2 D = 10 l = 3: mu_lo 83/100, q(mu_lo) = 0.490001 >= q_hi 49/100: True; U lower bound 135.96; leaves 3
E2 D = 10 l = 4: mu_lo 201/625, q(mu_lo) = 0.920022 >= q_hi 23/25: True; U lower bound 11674.2; leaves 1
E2 D = 10 l = 5: mu_lo 134/625, q(mu_lo) = 0.961026 >= q_hi 961/1000: True; U lower bound 27162.7; leaves 1
E2 D = 11 l = 4: mu_lo 741/2000, q(mu_lo) = 0.897016 >= q_hi 897/1000: True; U lower bound 23142.6; leaves 7
E2 D = 11 l = 5: mu_lo 2949/10000, q(mu_lo) = 0.929046 >= q_hi 929/1000: True; U lower bound 44357.9; leaves 1
E2 D = 11 l = 6: mu_lo 119/625, q(mu_lo) = 0.968030 >= q_hi 121/125: True; U lower bound 101871; leaves 1
E1 entries: 35; E2 entries: 13; failures: 0
verdict: VERIFIED
```

E2's "≈" column against the exact bounds (inline, Fractions): 6 of 13 quoted values exceed the exact bound — 9-5 (3.59·10⁴ >
35853.84…), 10-3 (136 > 135.9596…; exact 1380839923/10156250), 10-4 (1.17·10⁴ > 11674.20…), 10-5 (2.72·10⁴ > 27162.68…), 11-5
(4.44·10⁴ > 44357.87…), 11-6 (1.02·10⁵ > 101870.59…). The other seven are below.

**C4. Möbius bracket and the HD-S records** (`scripts/check_mobius_and_records.py`; sympy). (1) s^{2e}·[(1−z)f_zP + f(−P +
(1−z)P_z + P²)] with P = g/s^e, s = z + δ, minus `scert.py` l. 176-179's `br`, for arbitrary g, f, f_z. (2) Scan of the 34 records.
`$ [python-2]/bin/python -I check_mobius_and_records.py [repository]`
(the `repro-equal False` entries mask only `timing`/`provenance`; C5 shows they are equal under `compare_runs.py`'s keys)
```
== (1) zeta-design bracket
e = 1: s^(2e)*bracket - code_br = 0
e = 2: s^(2e)*bracket - code_br = 0
e = 20: s^(2e)*bracket - code_br = 0
e = 24: s^(2e)*bracket - code_br = 0

== (2) HD-S records
records: 34
10-2             none         VERIFIED                                                     repro-equal False log-equal True plan-equal True | boxes 22, attempts 22, all verified True, degrees [32], G-S6 (the box with Q = 0): True
10-2-nc-bound    nc-bound     REJECT: nc-bound (b)                                         repro-equal True log-equal True plan-equal None | K 266104, Q [-1.765967528e-6 +/- 2.95e-16], (a) True, rejected True
10-2-td-coeff    td-coeff     REJECT: E0n                                                  repro-equal True log-equal True plan-equal None | 
10-2-td-horizon  td-horizon   REJECT: td-horizon                                           repro-equal True log-equal True plan-equal None | 
10-3             none         VERIFIED                                                     repro-equal False log-equal True plan-equal True | boxes 21, attempts 21, all verified True, degrees [28]
10-4             none         VERIFIED                                                     repro-equal False log-equal True plan-equal True | boxes 11, attempts 11, all verified True, degrees [24]
10-5             none         VERIFIED                                                     repro-equal False log-equal True plan-equal True | boxes 8, attempts 8, all verified True, degrees [24], delta_b in [188/729, 278/645] (min 0.2579)
11-2             none         VERIFIED                                                     repro-equal False log-equal True plan-equal True | boxes 22, attempts 22, all verified True, degrees [32], G-S6 (the box with Q = 0): True
11-2-nc-bound    nc-bound     REJECT: nc-bound (b)                                         repro-equal True log-equal True plan-equal None | K 304036, Q [-2.017701931e-6 +/- 4.23e-16], (a) True, rejected True
11-2-td-coeff    td-coeff     REJECT: E0n                                                  repro-equal True log-equal True plan-equal None | 
11-2-td-horizon  td-horizon   REJECT: td-horizon                                           repro-equal True log-equal True plan-equal None | 
11-3             none         VERIFIED                                                     repro-equal False log-equal True plan-equal True | boxes 23, attempts 23, all verified True, degrees [32], G-S6 (the box with Q = 0): True
11-4             none         VERIFIED                                                     repro-equal False log-equal True plan-equal True | boxes 13, attempts 13, all verified True, degrees [28]
11-5             none         VERIFIED                                                     repro-equal False log-equal True plan-equal True | boxes 11, attempts 11, all verified True, degrees [28]
11-6             none         VERIFIED                                                     repro-equal False log-equal True plan-equal True | boxes 7, attempts 7, all verified True, degrees [24], delta_b in [239/927, 324/811] (min 0.2578)
7-2              none         VERIFIED                                                     repro-equal False log-equal True plan-equal True | boxes 9, attempts 9, all verified True, degrees [20]
7-2-nc-bound     nc-bound     REJECT: nc-bound (b)                                         repro-equal True log-equal True plan-equal None | K 174912, Q [-1.160787096e-6 +/- 5.05e-17], (a) True, rejected True
7-2-td-coeff     td-coeff     REJECT: E0n                                                  repro-equal True log-equal True plan-equal None | 
7-2-td-horizon   td-horizon   REJECT: td-horizon                                           repro-equal True log-equal True plan-equal None | 
7-2-td-verifier  td-verifier  REJECT: KAT                                                  repro-equal True log-equal True plan-equal None | 
7-3              none         VERIFIED                                                     repro-equal False log-equal True plan-equal True | boxes 5, attempts 5, all verified True, degrees [16]
8-2              none         VERIFIED                                                     repro-equal False log-equal True plan-equal True | boxes 22, attempts 22, all verified True, degrees [24], G-S6 (the box with Q = 0): True
8-2-nc-bound     nc-bound     REJECT: nc-bound (b)                                         repro-equal True log-equal True plan-equal None | K 201776, Q [-1.339062413e-6 +/- 2.51e-16], (a) True, rejected True
8-2-td-coeff     td-coeff     REJECT: E0n                                                  repro-equal True log-equal True plan-equal None | 
8-2-td-horizon   td-horizon   REJECT: td-horizon                                           repro-equal True log-equal True plan-equal None | 
8-3              none         VERIFIED                                                     repro-equal False log-equal True plan-equal True | boxes 10, attempts 10, all verified True, degrees [20]
8-4              none         VERIFIED                                                     repro-equal False log-equal True plan-equal True | boxes 3, attempts 3, all verified True, degrees [20]
9-2              none         VERIFIED                                                     repro-equal False log-equal True plan-equal True | boxes 22, attempts 22, all verified True, degrees [28], G-S6 (the box with Q = 0): True
9-2-nc-bound     nc-bound     REJECT: nc-bound (b)                                         repro-equal True log-equal True plan-equal None | K 231801, Q [-1.538323313e-6 +/- 2.52e-16], (a) True, rejected True
9-2-td-coeff     td-coeff     REJECT: E0n                                                  repro-equal True log-equal True plan-equal None | 
9-2-td-horizon   td-horizon   REJECT: td-horizon                                           repro-equal True log-equal True plan-equal None | 
9-3              none         VERIFIED                                                     repro-equal False log-equal True plan-equal True | boxes 11, attempts 11, all verified True, degrees [24]
9-4              none         VERIFIED                                                     repro-equal False log-equal True plan-equal True | boxes 9, attempts 9, all verified True, degrees [24]
9-5              none         VERIFIED                                                     repro-equal False log-equal True plan-equal True | boxes 2, attempts 2, all verified True, degrees [20], delta_b in [239/927, 3/11] (min 0.2578)
```

**C5. Record = reproduction under `compare_runs.py`'s MASK_KEYS** (`scripts/jsondiff.py`, masking timing, host, platform,
git_commit, t_backward_s, t_total_s, t_design_s, t_verify_s).
```
$ for each of the 34 HD-S records: python3 -I jsondiff.py record repro-host-2 <compare_runs.py MASK_KEYS>
10-2: differing leaves: 0
10-2-nc-bound: differing leaves: 0
10-2-td-coeff: differing leaves: 0
10-2-td-horizon: differing leaves: 0
10-3: differing leaves: 0
10-4: differing leaves: 0
10-5: differing leaves: 0
11-2: differing leaves: 0
11-2-nc-bound: differing leaves: 0
11-2-td-coeff: differing leaves: 0
11-2-td-horizon: differing leaves: 0
11-3: differing leaves: 0
11-4: differing leaves: 0
11-5: differing leaves: 0
11-6: differing leaves: 0
7-2: differing leaves: 0
7-2-nc-bound: differing leaves: 0
7-2-td-coeff: differing leaves: 0
7-2-td-horizon: differing leaves: 0
7-2-td-verifier: differing leaves: 0
7-3: differing leaves: 0
8-2: differing leaves: 0
8-2-nc-bound: differing leaves: 0
8-2-td-coeff: differing leaves: 0
8-2-td-horizon: differing leaves: 0
8-3: differing leaves: 0
8-4: differing leaves: 0
9-2: differing leaves: 0
9-2-nc-bound: differing leaves: 0
9-2-td-coeff: differing leaves: 0
9-2-td-horizon: differing leaves: 0
9-3: differing leaves: 0
9-4: differing leaves: 0
9-5: differing leaves: 0
$ same for the pilot VALID record vs repro
differing leaves: 0
```

**C6. TD-S2's counterexamples sit at (0, μ_a)** (rationals elided).
```
$ TD-S2 counterexample points vs each l = 2 band mu_a
7-2 mu_a = 1237/10000
td-horizon: FAIL  td-horizon: N > 0: sign*p = <negative rational> <= 0 at (t, mu) = (0, 1237/10000)  (a counterexample)
8-2 mu_a = 157/1250
td-horizon: FAIL  td-horizon: N > 0: sign*p = <negative rational> <= 0 at (t, mu) = (0, 157/1250)  (a counterexample)
9-2 mu_a = 1271/10000
td-horizon: FAIL  td-horizon: N > 0: sign*p = <negative rational> <= 0 at (t, mu) = (0, 1271/10000)  (a counterexample)
10-2 mu_a = 321/2500
td-horizon: FAIL  td-horizon: N > 0: sign*p = <negative rational> <= 0 at (t, mu) = (0, 321/2500)  (a counterexample)
11-2 mu_a = 259/2000
td-horizon: FAIL  td-horizon: N > 0: sign*p = <negative rational> <= 0 at (t, mu) = (0, 259/2000)  (a counterexample)
```

**C7. The pilot: VOID against VALID** (`scripts/jsondiff.py`; `diff`), and the code diff and commit order (`git`).
```
$ python3 -I jsondiff.py <VOID record> <VALID record> timing
masked keys: ['timing']
differing leaves: 5
provenance/git_commit | '8c2d6d2' | '710488b'
result/gates/NC-H/ok | False | True
result/gates/NC-H/sigma | None | -0.9964382002917467
result/gates/NC-H/z_min | None | 0.682
verdict | 'VOID: a gate or control is not as registered' | 'VALID'

$ python3 -I jsondiff.py <VOID repro-host-2> <VALID repro-host-2> timing
masked keys: ['timing']
differing leaves: 5
provenance/git_commit | '8c2d6d2' | '710488b'
result/gates/NC-H/ok | False | True
result/gates/NC-H/sigma | None | -0.9964382002917467
result/gates/NC-H/z_min | None | 0.682
verdict | 'VOID: a gate or control is not as registered' | 'VALID'

$ diff <VOID record run.log> <VALID record run.log>
5c5
< NC-H: ok = False, sigma = None
---
> NC-H: ok = True, sigma = -0.9964382002917467
52c52
< VOID: a gate or control is not as registered
---
> VALID
(diff exit 1)
```
```
$ git -C [repository] diff 8c2d6d2 710488b -- code/hd/pilot.py kit/
diff --git a/code/hd/pilot.py b/code/hd/pilot.py
index f229a3b..b96cdf9 100644
--- a/code/hd/pilot.py
+++ b/code/hd/pilot.py
@@ -21,7 +21,8 @@ band of D active there qualifies (a rung with no active band qualifies); if none
 Gates and controls (all in the same run; VALID only if all are as registered):
     PG1   the recorded rule-2 certificates T1 and G1 (BHM-025; N > 0 proved exactly): sigma > 0 under this evaluator
     PG2   the pilot's own design at T1 and G1 (z, degree 28, eps = 1/50): sigma >= THETA
-    NC-H  T1's pilot design with P(0) raised 1/10 above the horizon bound W(0)/f_z(0): sigma < 0
+    NC-H  T1's pilot design plus c (1 - z), which raises P(0) to 1/10 above the horizon bound W(0)/f_z(0) and leaves
+          P(1) unchanged (PREREG_ADDENDUM_1.md): sigma < 0
     NC-B  a planted bound state at G1's setting, W - K b on [3/10, 3/5], b = ((z - 3/10)(3/5 - z))^2, K = 2 I1/I2
           (the trial function b then has energy -I1 < 0): no qualifying design at all, and G1's design gives sigma < 0
 """
@@ -358,8 +359,8 @@ def gates(root):
         sg, zm = slack(tab, own[name][2])
         g[f"PG2 {name}"] = {"sigma": sg, "z_min": zm, "ok": sg is not None and sg >= THETA}
     S, tab, fit = own["T1"]
-    shift = S.W(0.0) / S.fz(0.0) - fit(0.0)[0] + 0.1
-    sg, zm = slack(tab, lambda z: (fit(z)[0] + shift, fit(z)[1]))
+    shift = S.W(0.0) / S.fz(0.0) - fit(0.0)[0] + 0.1          # addendum 1: + shift (1 - z) keeps P(1)
+    sg, zm = slack(tab, lambda z: (fit(z)[0] + shift * (1 - z), fit(z)[1] - shift))
     g["NC-H"] = {"shift": shift, "sigma": sg, "z_min": zm, "ok": sg is not None and sg < 0}
     S0 = own["G1"][0]
     K, I1 = bound_K(S0)

$ git -C [repository] log --format="%h %ad %s" --date=iso-strict 8c2d6d2^..b22c087 (subjects cut to 120 chars)
b22c087 2026-10-23T12:29:59-04:00 REGISTRY: commit of BHM-083 filled in
cf129f2 2026-10-23T12:29:57-04:00 The blind replication of HD-S's first band, D = 7 l = 2: holds (certified), agreeing with S(7, 2) (BHM-083)
a6e621f 2026-10-23T11:49:23-04:00 REGISTRY: commits of BHM-081 and BHM-082 filled in
e35d88e 2026-10-23T11:49:21-04:00 Session-L's [another line of this project] literature screen archived (BHM-081; SOURCES S19-S24, six anchors read by the lead); the note's a
8862d7c 2026-10-23T11:22:16-04:00 Outbox status: the session-R lead's acknowledgement of messages 6 and 7
7452f40 2026-10-23T11:21:55-04:00 Outbox: the prompt for the session-R lead's reading of the D = 7-11 stage report, sequenced after the blin
00a69f9 2026-10-23T11:21:08-04:00 REGISTRY: commits of BHM-078 to BHM-080 filled in
8ddbef0 2026-10-23T11:21:06-04:00 HD-S VERIFIED: all 18 bands of D = 7-11, so Theorem HD is certified for q <= 99/100 (BHM-078); the D = 7-11 stage re
0aa2673 2026-10-23T11:14:34-04:00 HD-S registered (BHM-076): S-certificates on the 18 bands of D = 7-11, before any run on claim data; the blind brief
e9f59ab 2026-10-23T11:11:09-04:00 Development code for HD-S (S-certificates on the D = 7-11 bands); not run on claim data
e89c65e 2026-10-23T11:10:02-04:00 HD-PILOT VALID: q_max(D) = 99/100 for D = 7-11 (BHM-074); TARGET_HD addendum 1 fixes q_max and the band designs befo
710488b 2026-10-23T11:02:53-04:00 HD-PILOT attempt at 8c2d6d2 VOID as registered: NC-H's constant shift made sigma undefined (BHM-072); addendum 1 fix
d224f28 2026-10-23T11:01:15-04:00 [another line of this project]: the lead's answer documented (BHM-070, Lemma R); literature screen requested from session-L (BHM-071); TODO 
8c2d6d2 2026-10-23T10:54:38-04:00 HD-PILOT registered (BHM-069): the untrusted design pilot that fixes q_max(D) for D = 7-11, before any run on claim 
```

Pilot table at rung 99/100 (against `pilot/RESULT.md` l. 35-52; all match to the digits quoted; note min ψ₁ 0.48694… at
D = 11 ℓ = 2 and min δ_t 0.2472… at q = 99/100):
```
$ pilot VALID record, rung 99/100: design, least degree, min sigma of the design, min psi1, min sigma_design, min delta_t
7 2 onset 948/1000 z 20 least {'z': 20, 'zeta': 32} minsig 0.05058374017729794 minpsi 0.8911741850035451 sig_design 0.07185607560669995 min delta_t 0.24725509600379306
7 3 onset 977/1000 z 16 least {'z': 16, 'zeta': 24} minsig 0.0062686162843935715 minpsi 0.9860842983439801 sig_design 0.021761644320662334 min delta_t 0.24725509600379292
8 2 from 0+ 0 z 24 least {'z': 24, 'zeta': 40} minsig 0.04537430537112794 minpsi 0.7418206121106594 sig_design 0.04492539520395131 min delta_t 0.24725509600378745
8 3 onset 944/1000 z 20 least {'z': 20, 'zeta': 24} minsig 0.015120753450588185 minpsi 0.9007414252029569 sig_design 0.02356052466953789 min delta_t 0.24725509600379342
8 4 onset 983/1000 z 20 least {'z': 20, 'zeta': 24} minsig 0.003025829011120742 minpsi 0.9959840305268439 sig_design 0.0097012953076004 min delta_t 0.24725509600379555
9 2 from 0+ 0 z 28 least {'z': 28, 'zeta': 40} minsig 0.04025465790553941 minpsi 0.6255846982566835 sig_design 0.044409141361740026 min delta_t 0.2472550960037964
9 3 onset 921/1000 z 24 least {'z': 24, 'zeta': 28} minsig 0.017975414254079506 minpsi 0.7994664594189863 sig_design 0.023715120919845182 min delta_t 0.2472550960037975
9 4 onset 952/1000 z 24 least {'z': 24, 'zeta': 24} minsig 0.009473084336967509 minpsi 0.9302900329291697 sig_design 0.01009925225392971 min delta_t 0.24725509600379286
9 5 onset 987/1000 zeta 20 least {'z': 24, 'zeta': 20} minsig 0.0015173136325574007 minpsi 0.9996475659854207 sig_design 0.004971668812596921 min delta_t 0.247255096003794
10 2 from 0+ 0 z 32 least {'z': 32, 'zeta': 48} minsig 0.040864796977760555 minpsi 0.5448490801754184 sig_design 0.04202450816405522 min delta_t 0.24725509600379827
10 3 onset 490/1000 z 28 least {'z': 28, 'zeta': 32} minsig 0.014945374983577718 minpsi 0.6987054443077109 sig_design 0.015407412402879935 min delta_t 0.24725509600379306
10 4 onset 920/1000 z 24 least {'z': 24, 'zeta': 28} minsig 0.0028053293521619355 minpsi 0.8472028261441943 sig_design 0.009832370987071617 min delta_t 0.24725509600379297
10 5 onset 961/1000 zeta 24 least {'z': 28, 'zeta': 24} minsig 0.003990883439180802 minpsi 0.9540896157128536 sig_design 0.005096457161064354 min delta_t 0.2472550960037964
11 2 from 0+ 0 z 32 least {'z': 32, 'zeta': 48} minsig 0.001355791027044502 minpsi 0.48694055384768814 sig_design 0.03868342754528644 min delta_t 0.24725509600379364
11 3 from 0+ 0 z 32 least {'z': 32, 'zeta': 40} minsig 0.013347570661694425 minpsi 0.617802169258597 sig_design 0.013410358568702783 min delta_t 0.24725509600379222
11 4 onset 897/1000 z 28 least {'z': 28, 'zeta': 32} minsig 0.007709810056077505 minpsi 0.7620992533708602 sig_design 0.009406908380311056 min delta_t 0.24725509600379145
11 5 onset 929/1000 z 28 least {'z': 28, 'zeta': 28} minsig 0.0018918404116410239 minpsi 0.8841491917725817 sig_design 0.004903553191076424 min delta_t 0.24725509600379594
11 6 onset 968/1000 zeta 24 least {'z': 32, 'zeta': 24} minsig 0.002211554957122115 minpsi 0.9709441172126595 sig_design 0.002853115950256982 min delta_t 0.2472550960037933
```

δ_t at q = 99/100 to 20 digits and the E3 rationals, from an inline `[python-2]/bin/python -I -c` (mpmath, 30 digits;
the min ψ₁ value is the record's float):
`D=11 l=2 min psi1 (float repr): 0.48694055384768814`; `delta_t at q=99/100: 2w/(1+w) = 0.24725509600379317264`;
`19870/6561 = 3.0285017527815881725 ; 17257/2401 = 7.1874219075385256143 ; 399917/10368 = 38.572241512345679012`.

**C8. Blind-seat and bh-modes decimals for D = 7 ℓ = 2** (`scripts/blind_decimals.py`; Fractions, integer square roots, floor).
`$ /usr/bin/python3 -I blind_decimals.py`
```
mu=1237/10000 (q top) q^2 = 482351496417168561/492144578017168561  q = 0.990000611118724 (floor)
mu=2780/10000 (blind split) q^2 = 2821360801041/3130496801041  q = 0.949341971366875 (floor)
mu=2817/10000 (q bottom) q^2 = 450385526985669121/501172656585669121  q = 0.947978589867229 (floor)
blind E2 lower 0.94797859 (lower end: inward iff >= exact): inward True
blind E2 upper 0.99000061: inward True
blind E0 lower 0.947979: inward True
blind E0 upper 0.949342: inward False
blind C lower 0.949342: inward True
blind C upper 0.990001: inward False
bh-modes S(7,2) lower 0.94798: inward True
bh-modes S(7,2) upper 0.99000: inward True
```

**C9. A2: METHOD's N at the degenerate horizon, q = 1** (`scripts/a2_throat.py`; sympy). P = a/z + b₀ + b₁z + b₂z² (n = 4) or
a/z + b₀ + b₁z (general n); N = U − 64H²[(1−z)f_zP + f(−P + (1−z)P_z + P²)], f = (1 − (1−z)^{n−1})², x = 2(1−z)^{n−1},
δ = 1/((ℓ+n)(n+1)), m = (ℓ−1)(ℓ+n). The D = 6 run uses `TARGET.md` §1's U₋, H₋; the n = 4…9 runs use `potentials.U_minus`.
`$ [python-2]/bin/python -I a2_throat.py`
```
== D = 6 (n = 4), q = 1, TARGET.md's U_-, H_-
denominator of N (after together): (ell + 4)**10
H_-(x_H = 2) = (ell + 3)*(ell + 4)
N(0) - 576 H(2)^2 (c - a(a+1)), c = l(l-3)/9: 0
N(0)/(576 H(2)^2) at a = -1/2: (2*ell - 3)**2/36  vs (2l-3)^2/36: 0
bounded P (a = 0): N(0) = U(x_H) = 64*ell*(ell - 3)*(ell + 3)**2*(ell + 4)**2 ; at l = 2: -115200
l = 2: H(2) = 30 ; N(0) at a = -1/2: 14400 ; window: N(0) > 0 iff a in [-2/3, -1/3]
l = 3: N(0) at a = 0: 0 ; at a = -1/2: 254016

== general n at q = 1 (potentials.U_minus), n = 4..9, l symbolic
n = 4 (D = 6): N has z in denominator: False; c_n(l) = ell*(ell - 3)/9 (= l(l-n+1)/(n-1)^2: True); N(0) = 64(n-1)^2 H(2)^2 (c_n - a(a+1)): True; c_n + 1/4 = (2*ell - 3)**2/36; at l = 2: 1/36
n = 5 (D = 7): N has z in denominator: False; c_n(l) = ell*(ell - 4)/16 (= l(l-n+1)/(n-1)^2: True); N(0) = 64(n-1)^2 H(2)^2 (c_n - a(a+1)): True; c_n + 1/4 = (ell - 2)**2/16; at l = 2: 0
n = 6 (D = 8): N has z in denominator: False; c_n(l) = ell*(ell - 5)/25 (= l(l-n+1)/(n-1)^2: True); N(0) = 64(n-1)^2 H(2)^2 (c_n - a(a+1)): True; c_n + 1/4 = (2*ell - 5)**2/100; at l = 2: 1/100
n = 7 (D = 9): N has z in denominator: False; c_n(l) = ell*(ell - 6)/36 (= l(l-n+1)/(n-1)^2: True); N(0) = 64(n-1)^2 H(2)^2 (c_n - a(a+1)): True; c_n + 1/4 = (ell - 3)**2/36; at l = 2: 1/36
n = 8 (D = 10): N has z in denominator: False; c_n(l) = ell*(ell - 7)/49 (= l(l-n+1)/(n-1)^2: True); N(0) = 64(n-1)^2 H(2)^2 (c_n - a(a+1)): True; c_n + 1/4 = (2*ell - 7)**2/196; at l = 2: 9/196
n = 9 (D = 11): N has z in denominator: False; c_n(l) = ell*(ell - 8)/64 (= l(l-n+1)/(n-1)^2: True); N(0) = 64(n-1)^2 H(2)^2 (c_n - a(a+1)): True; c_n + 1/4 = (ell - 4)**2/64; at l = 2: 1/16
```

**C10. A2: the horizon bound as q → 1 at D = 6, ℓ = 2, and the q = 1 identity at n = 2, 3** (`scripts/a2_horizon_bound.py`,
`scripts/hb_exact.py`, `scripts/hb_digits.py`; sympy; floats printed by `%g` are rounded, the exact values follow).
`$ [python-2]/bin/python -I a2_horizon_bound.py`
```
mu | q (decimal) | 1 - q | delta_t | z_- (inner horizon, float) | W(0) | horizon bound W(0)/f_z(0)
3/25 | 0.9901988398 | 9.801e-03 | 0.245098 | -0.0982549 | -0.686275 | -0.933333
1/10 | 0.9931939116 | 6.806e-03 | 0.208644 | -0.0811252 | -0.88037 | -1.4065
1/100 | 0.9999319444 | 6.806e-05 | 0.0230639 | -0.00780833 | -1.87554 | -27.1064
1/1000 | 0.9999993194 | 6.806e-07 | 0.00233061 | -0.000778081 | -1.98742 | -284.248
1/10000 | 0.9999999932 | 6.806e-09 | 0.000233306 | -7.77808e-05 | -1.99874 | -2855.68

== q = 1, n = 2, 3: c_n(l) and N(0) for P = a/z + b0 + b1 z
n = 2 (D = 4): z in denominator: False; c_n = ell*(ell - 1); identity: True; c_n + 1/4 = (2*ell - 1)**2/4; c_n at l = 2: 2
n = 3 (D = 5): z in denominator: False; c_n = ell*(ell - 2)/4; identity: True; c_n + 1/4 = (ell - 1)**2/4; c_n at l = 2: 0
```
`$ [python-2]/bin/python -I hb_exact.py`
```
3/25 W(0) = -35/51 | W(0)/f_z(0) = -14/15
1/100 W(0) = -1.87553761323360 | W(0)/f_z(0) = -27.1064306335459
1/10000 W(0) = -1.99874015538345 | W(0)/f_z(0) = -2855.67620723735
```
`$ [python-2]/bin/python -I hb_digits.py`
```
3/25 q = 0.990198839825901 delta_t = 0.245098039216 W(0) = -0.686274509804 W(0)/f_z(0) = -0.933333333333 W0 + 3/2 = 0.81372549 W0 + 9/2 = 3.8137255
1/100 q = 0.999931944397124 delta_t = 0.0230638704469 W(0) = -1.87553761323 W(0)/f_z(0) = -27.1064306335 W0 + 3/2 = -0.37553761 W0 + 9/2 = 2.6244624
1/10000 q = 0.999999993194444 delta_t = 0.000233306113898 W(0) = -1.99874015538 W(0)/f_z(0) = -2855.67620724 W0 + 3/2 = -0.49874016 W0 + 9/2 = 2.5012598
```

## D. Records and logs read programmatically (SHA-256)

HD-E and the pilot:
```
bb06c9023b0f7ad0b30b18b66221ebfe5095866caa4c426d406725d41da96da5  results/hd/elementary/runs/record/main/result.json
d9454332450335d9e5488936b7c426b77087ddc2cbb8d3621c507e69ac911d01  results/hd/elementary/runs/record/main/run.log
696746ab187f6af425b9b265fcaddf509da47b5e1b4593fcc346bc732998a771  results/hd/pilot/attempt-8c2d6d2/record/kit.log
8c9a520d8a532b1bb3a78d29f4f352c344feec669cf5733b731054f1c3125d4b  results/hd/pilot/attempt-8c2d6d2/record/main/result.json
9a729b46340a04f78f1939ea75d66b0e2311a23f01a831af8dc644b97966d426  results/hd/pilot/attempt-8c2d6d2/record/main/run.log
696746ab187f6af425b9b265fcaddf509da47b5e1b4593fcc346bc732998a771  results/hd/pilot/attempt-8c2d6d2/repro-host-2/kit.log
3eb0b3b2faf147a95acb1eaf824fbeec8cfa21c07a39132756f07537b40f1d73  results/hd/pilot/attempt-8c2d6d2/repro-host-2/main/result.json
9a729b46340a04f78f1939ea75d66b0e2311a23f01a831af8dc644b97966d426  results/hd/pilot/attempt-8c2d6d2/repro-host-2/main/run.log
f6213cd8c6ac37bb823ce42c6616e25c27675aae07ce5c41eca9b7ccc5689606  results/hd/pilot/runs/record/kit.log
10e04bf69e70c5798c472a54c643bccbad646bac0b1c2129de1779ded6601486  results/hd/pilot/runs/record/main/result.json
b59c0ab2ce26562d881caf0ace7631bc1fc1700dc5a13f8c1f18af5178d25dfb  results/hd/pilot/runs/record/main/run.log
f6213cd8c6ac37bb823ce42c6616e25c27675aae07ce5c41eca9b7ccc5689606  results/hd/pilot/runs/repro-host-2/kit.log
11a86e3c378cf9978dc96221a0c63f0d00ca08d12a8de95457108f11e10c4c76  results/hd/pilot/runs/repro-host-2/main/result.json
b59c0ab2ce26562d881caf0ace7631bc1fc1700dc5a13f8c1f18af5178d25dfb  results/hd/pilot/runs/repro-host-2/main/run.log
```
HD-S (`results/hd/s/runs/`, record and repro-host-2; 34 result.json, 34 run.log, 18 planning.jsonl each):
```
e2230bfc31f70115b9a676291c124f68d8dbaa3309976b8441c82fdbe6a3cda4  results/hd/s/runs/record/10-2-nc-bound/result.json
35d03c9af782b5762d9214d1e533151846783f3c197122aa2c8645a1f6fb2cd6  results/hd/s/runs/record/10-2-nc-bound/run.log
172a0a82b37ad8631273e3a8c0d1338667719f680dd26b3900f0e130272a373e  results/hd/s/runs/record/10-2/planning.jsonl
c86fcc8fab3d6a3f4b185f937473d2d15faab141180390e2595da469defe29f6  results/hd/s/runs/record/10-2/result.json
d556444f5e8ee28c183a25973805b5e87f072c3a5da7ac540c5aa9c0d6a3ec6b  results/hd/s/runs/record/10-2/run.log
bb76d41e7edb4ecf4b685a7e9a42cbbed23884d1060db029c9cd67953d2681f0  results/hd/s/runs/record/10-2-td-coeff/result.json
f11dc290a31e08d7e6cf7a7042a769480132f5ff83535ba93708749d22345fc8  results/hd/s/runs/record/10-2-td-coeff/run.log
dd9cbfd4ed656b7f5e8feaa97ad16d9d71f04e0babc905d13b45dc887cf123f2  results/hd/s/runs/record/10-2-td-horizon/result.json
d8e9211221a6ddc0dc2d33e103892b7ee62aae46ba962162595161e4582d0da1  results/hd/s/runs/record/10-2-td-horizon/run.log
60f31922d5a1e15718dad86d59455f55c01cdace1e92920012d100bdb42bba43  results/hd/s/runs/record/10-3/planning.jsonl
16768210a712af0b134df297adb45627673d2f2e7c82809cdd4b90293e76d937  results/hd/s/runs/record/10-3/result.json
7594f0b9dedc85fc6d4155e8cc5129bc1e48b49d11d87dc68978c3dddfb55bb9  results/hd/s/runs/record/10-3/run.log
bd66832de686164e97a20ff2a9bf19b8427cf3eae12d72936cb2f60d8cea8df6  results/hd/s/runs/record/10-4/planning.jsonl
bdb259293da694d505df2d9236f0fb75c17755e94924182555efafc9e994b058  results/hd/s/runs/record/10-4/result.json
5cb9226c101f78d68855e984ab23f46789560f6df8a7b62bb0444aeefa013401  results/hd/s/runs/record/10-4/run.log
adb8756efb350adf0907eb18eb6c8a94f61bcb6329b190a6a87b9e44cb0e6e40  results/hd/s/runs/record/10-5/planning.jsonl
654db7fd076295ae128f8f5cd38ec8c6dc46c694a02e78dd977c80cafed2b097  results/hd/s/runs/record/10-5/result.json
c8274377a9cc980627a8fe8f41b8485d31400271da1c9d721343f593dc1f2f19  results/hd/s/runs/record/10-5/run.log
81e063504fd60ddc0b434cd5ba74f120eed9fcf17117e5366199aa689869a144  results/hd/s/runs/record/11-2-nc-bound/result.json
47c514f6f17261e9667feac4edd98ec257aa09657bab8ee9c92c3e90e935c5b9  results/hd/s/runs/record/11-2-nc-bound/run.log
f2b11ad0118d1a0d6d8fc7bcc0ed0f7fbac9d45c8fe2d8f7e2a7b0847af419ea  results/hd/s/runs/record/11-2/planning.jsonl
7ffc29d76015f3651465447ed825ad6422018623cc7f1e8426a0e9d2fd64b183  results/hd/s/runs/record/11-2/result.json
f485c088f224208da06efafde623c0ceacfe6caf04073e7ef1347515d1e5ca12  results/hd/s/runs/record/11-2/run.log
0d0ef35d56df40b5e5aa4d4c5dfbb4ff14abd2b661466f60ae1e40a4bb0714dd  results/hd/s/runs/record/11-2-td-coeff/result.json
64e5da78c57197e492b27ef8f8d26acc636cfa02ff58b0f820f11573f98cca5c  results/hd/s/runs/record/11-2-td-coeff/run.log
1e02f87b3fc874c42fcfc816aa5eca489f813b44d5d465561db07bae121a5bc0  results/hd/s/runs/record/11-2-td-horizon/result.json
7f18169adba3ca3c363b33e4341e475730231f140b932af77beec137c4beb8fa  results/hd/s/runs/record/11-2-td-horizon/run.log
6aa2d1b40995b269f8e9a0193cc1ad29bf981564d5008b91c8a26a10458ee0b2  results/hd/s/runs/record/11-3/planning.jsonl
dbe16db068bdd49fce86dca50f104a195bab08d7e9ea86f0e7b34bae82326b3d  results/hd/s/runs/record/11-3/result.json
746b2854419c1fbde3bfd2ddf35e3b3000864be69b4d01dc79644ed76eb0a855  results/hd/s/runs/record/11-3/run.log
c1ea97675317e5a97581cbe875861701d2955ce8d43c736f80282cbfe86d59b6  results/hd/s/runs/record/11-4/planning.jsonl
2ea1cd8b8e1188f2f71b3ef9b4652abab52a04e0497e492c38df84f35f5d1266  results/hd/s/runs/record/11-4/result.json
6d0a85a28f687bf89bb1920bdd6a6280b2e58945c8d52d58ac02fe0771f1a3df  results/hd/s/runs/record/11-4/run.log
ab6a1c256d3eeb44874f560efa4b4c0d97dd776f37160e165874ba14feb21fa4  results/hd/s/runs/record/11-5/planning.jsonl
03aea70d9d0a4c0017d142c9c3a9cf5af0dd2adf6f30f4762771fce7ff0014ad  results/hd/s/runs/record/11-5/result.json
f87c34b6af9c42b8c4f18e54a312c568670eb0b5541885afb2380f93365b2f1d  results/hd/s/runs/record/11-5/run.log
d2820aec9b7aa8f45fc768334ff45764a55a0b724e230d78c6b9255eef86da99  results/hd/s/runs/record/11-6/planning.jsonl
94b7c0920c6d59c796612015f6e9410d445898c04fca6813fddfabf0c269cdb4  results/hd/s/runs/record/11-6/result.json
d3626c14d0aadf50f51001f298d70e2a560a33022183c670b8cd53de48bc1fc0  results/hd/s/runs/record/11-6/run.log
5ec8c71e24eca586456464c40ee98851d511645854cb8bc9069880afe117631a  results/hd/s/runs/record/7-2-nc-bound/result.json
1c824726990167c23df6c6e98e0e69f32145957ab80411a22953fbfdf05d8a83  results/hd/s/runs/record/7-2-nc-bound/run.log
9a7118a3883f96d8c7417b2f2bc2abd8108f63e22e6544f5cad2bd3aedee4fe1  results/hd/s/runs/record/7-2/planning.jsonl
8a16a42b8d12a963614c5f722bca77d376aedffd2bb367d42ca508eee166c272  results/hd/s/runs/record/7-2/result.json
ec40ed46a36646e629cb8455759d0013f055be6b27699d3232ffef5eeadb22f1  results/hd/s/runs/record/7-2/run.log
f7abe352da6c5456d7fa1b54bc9546ee69ae3b6bbfaefdab41d4d6180c0de4a4  results/hd/s/runs/record/7-2-td-coeff/result.json
ad96c8de3254f5f14bfe66e0bbad59f70a3dbc386860665c595a4afa5b9c271b  results/hd/s/runs/record/7-2-td-coeff/run.log
5547214ba7fd0e9559c7bbdf9fdea90984e6bc5757f291f2a094db0a8285b30e  results/hd/s/runs/record/7-2-td-horizon/result.json
bc4662d5bfdc2c7c886aaca51536b2527b8c16e5a9543002953381a67aaf825c  results/hd/s/runs/record/7-2-td-horizon/run.log
2dee395db3b6fbd2397092f4df14847d1474172590e2119a12d8db40dbbd53eb  results/hd/s/runs/record/7-2-td-verifier/result.json
7eb4f89c93d958d93501b8e923befb722db34a0b069ea22d57f6788707397972  results/hd/s/runs/record/7-2-td-verifier/run.log
7933c95d3cced08408618e6e73ea5880c265e3519f89001d5345e1169de60e76  results/hd/s/runs/record/7-3/planning.jsonl
8d23fd1562b88ae6c90be75c1568ff0ada794a26bdd9a4b2cd4ae3d7b9937746  results/hd/s/runs/record/7-3/result.json
28868302aceceb9024796079165bc111bff74dcd9b33d1aa44f3549738680fd8  results/hd/s/runs/record/7-3/run.log
dfa88d7b837d4115719990b4a6c66fc5660fb417ff2a321dbd2ee0fa57a51afe  results/hd/s/runs/record/8-2-nc-bound/result.json
7b6d61082329195b61bd0017ad498c5436fe525b719c4e6166085b93eddf1d18  results/hd/s/runs/record/8-2-nc-bound/run.log
756085c0e9b1bd96a18214612083ed44627ba254104a0236d1d66723dffee743  results/hd/s/runs/record/8-2/planning.jsonl
749c6075fe087424e4f60adf28c66e235b87154a4d1f3ca205a4ea5d79adee17  results/hd/s/runs/record/8-2/result.json
3159daf1c8d519dd17ba41a25a81b58e6bc678794e1b44e602cf8260f773c4ef  results/hd/s/runs/record/8-2/run.log
ea5ae97cc18608c6b73f340abcbb5f1e4071bc1f98a74d99f2f87255b459eeb1  results/hd/s/runs/record/8-2-td-coeff/result.json
a79c34001fdf8046a6b20c411d43b0c5032aa9b6b690b3c8c50c7726cef054fa  results/hd/s/runs/record/8-2-td-coeff/run.log
ea55225636fe6ad5d97361b8e84a5c087f9f1fe44ea1a0b5bc01463877181e80  results/hd/s/runs/record/8-2-td-horizon/result.json
64bd01047a7098c2e4da01309782f40f7f79b9f39fca7e053aa967c28257582a  results/hd/s/runs/record/8-2-td-horizon/run.log
bb03579dd98c62b6955e18fe5197a8034c4f0cc7845a65483e8e792f77447af1  results/hd/s/runs/record/8-3/planning.jsonl
8c57c4cb326ab7b28c9b7b1f3bae124964635fe293d9f852fb31f4bf0f7b94b7  results/hd/s/runs/record/8-3/result.json
0e5c8d9750d54684ca701cab234569efd4a224dbedc1340f258fc36af802caaa  results/hd/s/runs/record/8-3/run.log
fd969c3749d174b4ae7635b176e52634d5e43e4a4269f11ce789787052a1a45b  results/hd/s/runs/record/8-4/planning.jsonl
e1e5d94d8a282790641a17221324d3a3411e3e0e13aa1b3fc1a868cb64c60552  results/hd/s/runs/record/8-4/result.json
81524635461a61fdcbbfba462e7cd2988fd95cbde020bc2adc202e947129e3b4  results/hd/s/runs/record/8-4/run.log
943978eaf8e9b4c09e4719c54ce118ad2051017adcb4c0f5e7a865247cd43960  results/hd/s/runs/record/9-2-nc-bound/result.json
66d29e9ef2624d14af1171b84f613100ba9389b4573b1d18994e11c26b588df7  results/hd/s/runs/record/9-2-nc-bound/run.log
ae0a3083404da5eda350c57f6caf5f749b2f334f5c763a989f5906de2ffa04d2  results/hd/s/runs/record/9-2/planning.jsonl
feb934e83ab08536b402b73a80b49271f57b43f8957576f8b09c0646371965b4  results/hd/s/runs/record/9-2/result.json
0ebcce4562e6cf5149167418b67b6236d6629faf53bf71a6e4d9d13fb8658561  results/hd/s/runs/record/9-2/run.log
5a055936c9caa1249342242f92db945278eb660c88d39007fe252a396050d07f  results/hd/s/runs/record/9-2-td-coeff/result.json
8e9218d1f1960ff4b238fb4957e59490524f74db2f92639a2286b04ed2adfcd2  results/hd/s/runs/record/9-2-td-coeff/run.log
528f4358db4e57bd7183a2c262535316aa36c07c8d37445ece91cc6f53f966bc  results/hd/s/runs/record/9-2-td-horizon/result.json
265a41735a3cd4d54fe1ffe9beaa9a8d2c929b5d73ce6cfbec9189441729f6a9  results/hd/s/runs/record/9-2-td-horizon/run.log
3dc3b005d1d8c13ac09a80f93464310072c49790f95715676a6ca1dc77a489ed  results/hd/s/runs/record/9-3/planning.jsonl
4140d738203e41a11080a36cbf57f01a7a212477fbf538ae452d9596dd8e31e6  results/hd/s/runs/record/9-3/result.json
3dda9b3ab6985595aa8f785b4ccc74aad5053090e24c5c11688f6e853effbfdc  results/hd/s/runs/record/9-3/run.log
4794bbf8a73e4e2728a16822a7391c54a89ee47651192e4aa3829fe6ea3519b4  results/hd/s/runs/record/9-4/planning.jsonl
6e389529b19c3a6cc912f14c2dd4eaaad95a2b725d5fbade8065fa356d4a828f  results/hd/s/runs/record/9-4/result.json
687f028d5e0c8f777844e45c2214e6c2ad89eb811553aaac56f353781fd3ff21  results/hd/s/runs/record/9-4/run.log
ff90dbf73c16488a1d109edf0151c134de2b064be21eee59872d265b0010e1d2  results/hd/s/runs/record/9-5/planning.jsonl
c556aede04f168d424aa3fff5fb78056bb1168bfc704f164373dcedf1e012264  results/hd/s/runs/record/9-5/result.json
46b989bcc44df58eb34b9159192969fbb4c8bdff7a03bbe98271f6ec158c95a3  results/hd/s/runs/record/9-5/run.log
b20e5bf27f88fa433d4b9b5077d976f3b83c6708133ff4bb3958acdc64780700  results/hd/s/runs/repro-host-2/10-2-nc-bound/result.json
35d03c9af782b5762d9214d1e533151846783f3c197122aa2c8645a1f6fb2cd6  results/hd/s/runs/repro-host-2/10-2-nc-bound/run.log
172a0a82b37ad8631273e3a8c0d1338667719f680dd26b3900f0e130272a373e  results/hd/s/runs/repro-host-2/10-2/planning.jsonl
3d4698d7eb8958cf4fc3aff8ea0548155dcebd07a9424dc92031d29e835aa7bd  results/hd/s/runs/repro-host-2/10-2/result.json
d556444f5e8ee28c183a25973805b5e87f072c3a5da7ac540c5aa9c0d6a3ec6b  results/hd/s/runs/repro-host-2/10-2/run.log
5bd86f5e689d80952d7cc3d0f71926a02b6579fa27de1299ed8ef7b58adccc9e  results/hd/s/runs/repro-host-2/10-2-td-coeff/result.json
f11dc290a31e08d7e6cf7a7042a769480132f5ff83535ba93708749d22345fc8  results/hd/s/runs/repro-host-2/10-2-td-coeff/run.log
d6a67b8b8a2ba6035ebf741a3854d5812877956e0a80d30e6ce9a4afe6542892  results/hd/s/runs/repro-host-2/10-2-td-horizon/result.json
d8e9211221a6ddc0dc2d33e103892b7ee62aae46ba962162595161e4582d0da1  results/hd/s/runs/repro-host-2/10-2-td-horizon/run.log
60f31922d5a1e15718dad86d59455f55c01cdace1e92920012d100bdb42bba43  results/hd/s/runs/repro-host-2/10-3/planning.jsonl
8ebae1ea9c68afe697fca1be887896ab561231e779cc88e0b73d533c80bc501b  results/hd/s/runs/repro-host-2/10-3/result.json
7594f0b9dedc85fc6d4155e8cc5129bc1e48b49d11d87dc68978c3dddfb55bb9  results/hd/s/runs/repro-host-2/10-3/run.log
bd66832de686164e97a20ff2a9bf19b8427cf3eae12d72936cb2f60d8cea8df6  results/hd/s/runs/repro-host-2/10-4/planning.jsonl
d4ddb6a50bbdb091ac6e36eaa507fe71d40b1afdd06ebe16ed9f2c1cbc01fc8c  results/hd/s/runs/repro-host-2/10-4/result.json
5cb9226c101f78d68855e984ab23f46789560f6df8a7b62bb0444aeefa013401  results/hd/s/runs/repro-host-2/10-4/run.log
adb8756efb350adf0907eb18eb6c8a94f61bcb6329b190a6a87b9e44cb0e6e40  results/hd/s/runs/repro-host-2/10-5/planning.jsonl
e5bdd9901370e15f8b1774dba8df43cbe5a30d9f37a6a332a296f45780aec477  results/hd/s/runs/repro-host-2/10-5/result.json
c8274377a9cc980627a8fe8f41b8485d31400271da1c9d721343f593dc1f2f19  results/hd/s/runs/repro-host-2/10-5/run.log
1d2338493551e1cfe0c90b28458a3ae075923e7ad309b915c08767bcef3f4e2c  results/hd/s/runs/repro-host-2/11-2-nc-bound/result.json
47c514f6f17261e9667feac4edd98ec257aa09657bab8ee9c92c3e90e935c5b9  results/hd/s/runs/repro-host-2/11-2-nc-bound/run.log
f2b11ad0118d1a0d6d8fc7bcc0ed0f7fbac9d45c8fe2d8f7e2a7b0847af419ea  results/hd/s/runs/repro-host-2/11-2/planning.jsonl
3417c193afa54d79df3c61ead0d5cfa67016c1b7644c3a35e6803e5a5e80b881  results/hd/s/runs/repro-host-2/11-2/result.json
f485c088f224208da06efafde623c0ceacfe6caf04073e7ef1347515d1e5ca12  results/hd/s/runs/repro-host-2/11-2/run.log
b2329fc25cca785bae2869de8931db42544f9dd83eaa52410fa36c8e77339afa  results/hd/s/runs/repro-host-2/11-2-td-coeff/result.json
64e5da78c57197e492b27ef8f8d26acc636cfa02ff58b0f820f11573f98cca5c  results/hd/s/runs/repro-host-2/11-2-td-coeff/run.log
1dbe5937ff4053f63ddcde7165ea3728fa514c7d99239a1dcb151dea59b20abc  results/hd/s/runs/repro-host-2/11-2-td-horizon/result.json
7f18169adba3ca3c363b33e4341e475730231f140b932af77beec137c4beb8fa  results/hd/s/runs/repro-host-2/11-2-td-horizon/run.log
6aa2d1b40995b269f8e9a0193cc1ad29bf981564d5008b91c8a26a10458ee0b2  results/hd/s/runs/repro-host-2/11-3/planning.jsonl
24624ea527c86517ae1ea092e96ec26799889cc72e19e0c688a1b6ad95bbff4b  results/hd/s/runs/repro-host-2/11-3/result.json
746b2854419c1fbde3bfd2ddf35e3b3000864be69b4d01dc79644ed76eb0a855  results/hd/s/runs/repro-host-2/11-3/run.log
c1ea97675317e5a97581cbe875861701d2955ce8d43c736f80282cbfe86d59b6  results/hd/s/runs/repro-host-2/11-4/planning.jsonl
dbc012dbe918917fdb08524f483ffe2202b24e8734be966522aa1c770021c629  results/hd/s/runs/repro-host-2/11-4/result.json
6d0a85a28f687bf89bb1920bdd6a6280b2e58945c8d52d58ac02fe0771f1a3df  results/hd/s/runs/repro-host-2/11-4/run.log
ab6a1c256d3eeb44874f560efa4b4c0d97dd776f37160e165874ba14feb21fa4  results/hd/s/runs/repro-host-2/11-5/planning.jsonl
becbb61a3f9299d8ab79bacb8f34601ff3e1e6ff0e0290a5bd1247066d32e50a  results/hd/s/runs/repro-host-2/11-5/result.json
f87c34b6af9c42b8c4f18e54a312c568670eb0b5541885afb2380f93365b2f1d  results/hd/s/runs/repro-host-2/11-5/run.log
d2820aec9b7aa8f45fc768334ff45764a55a0b724e230d78c6b9255eef86da99  results/hd/s/runs/repro-host-2/11-6/planning.jsonl
befef2dd65b53cafa436b1b3c220ee50de644373e6a53f11d52b63085a69fb3a  results/hd/s/runs/repro-host-2/11-6/result.json
d3626c14d0aadf50f51001f298d70e2a560a33022183c670b8cd53de48bc1fc0  results/hd/s/runs/repro-host-2/11-6/run.log
e8318053db6f2946aeccd0e7f349febebe1ee69c51ac9aabf9c8dcfe26409f97  results/hd/s/runs/repro-host-2/7-2-nc-bound/result.json
1c824726990167c23df6c6e98e0e69f32145957ab80411a22953fbfdf05d8a83  results/hd/s/runs/repro-host-2/7-2-nc-bound/run.log
9a7118a3883f96d8c7417b2f2bc2abd8108f63e22e6544f5cad2bd3aedee4fe1  results/hd/s/runs/repro-host-2/7-2/planning.jsonl
e781fe9dae4a37b9a2cbf0e1f426120e22c345aebb78b6e2fea40a384f22e88a  results/hd/s/runs/repro-host-2/7-2/result.json
ec40ed46a36646e629cb8455759d0013f055be6b27699d3232ffef5eeadb22f1  results/hd/s/runs/repro-host-2/7-2/run.log
5ec8fc8fc7121dcad090f6be0470ee5459f4eda2b63001a26853c10cfbab8bc9  results/hd/s/runs/repro-host-2/7-2-td-coeff/result.json
ad96c8de3254f5f14bfe66e0bbad59f70a3dbc386860665c595a4afa5b9c271b  results/hd/s/runs/repro-host-2/7-2-td-coeff/run.log
71f832fd9bcfe98dd2e098205476f80dd5886c22c25c6bf002ab50c07ebff478  results/hd/s/runs/repro-host-2/7-2-td-horizon/result.json
bc4662d5bfdc2c7c886aaca51536b2527b8c16e5a9543002953381a67aaf825c  results/hd/s/runs/repro-host-2/7-2-td-horizon/run.log
637a80f863e13f3779482cf6fe244ac0448c366be5068e0b6f1c96cf30dcfd7c  results/hd/s/runs/repro-host-2/7-2-td-verifier/result.json
7eb4f89c93d958d93501b8e923befb722db34a0b069ea22d57f6788707397972  results/hd/s/runs/repro-host-2/7-2-td-verifier/run.log
7933c95d3cced08408618e6e73ea5880c265e3519f89001d5345e1169de60e76  results/hd/s/runs/repro-host-2/7-3/planning.jsonl
2c943448e98e8c1a6cff5d530b0a7c31578e12bc1125110aba7dab9286586248  results/hd/s/runs/repro-host-2/7-3/result.json
28868302aceceb9024796079165bc111bff74dcd9b33d1aa44f3549738680fd8  results/hd/s/runs/repro-host-2/7-3/run.log
8ae7fe74923a39f8e053e48532553c57c0d3e1b85d97494399d3b490a0c97228  results/hd/s/runs/repro-host-2/8-2-nc-bound/result.json
7b6d61082329195b61bd0017ad498c5436fe525b719c4e6166085b93eddf1d18  results/hd/s/runs/repro-host-2/8-2-nc-bound/run.log
756085c0e9b1bd96a18214612083ed44627ba254104a0236d1d66723dffee743  results/hd/s/runs/repro-host-2/8-2/planning.jsonl
13a0c1d7e784a062d04871529d230e62d697394371791b16806818ecc0091283  results/hd/s/runs/repro-host-2/8-2/result.json
3159daf1c8d519dd17ba41a25a81b58e6bc678794e1b44e602cf8260f773c4ef  results/hd/s/runs/repro-host-2/8-2/run.log
182921b5c3b3aafee4c8e55397989df080585b41ae37ef899997e54841147ff3  results/hd/s/runs/repro-host-2/8-2-td-coeff/result.json
a79c34001fdf8046a6b20c411d43b0c5032aa9b6b690b3c8c50c7726cef054fa  results/hd/s/runs/repro-host-2/8-2-td-coeff/run.log
7c5a37e762cce142245b324ace858dbb6b0012d54abd8f19f45294b39cc1aaae  results/hd/s/runs/repro-host-2/8-2-td-horizon/result.json
64bd01047a7098c2e4da01309782f40f7f79b9f39fca7e053aa967c28257582a  results/hd/s/runs/repro-host-2/8-2-td-horizon/run.log
bb03579dd98c62b6955e18fe5197a8034c4f0cc7845a65483e8e792f77447af1  results/hd/s/runs/repro-host-2/8-3/planning.jsonl
b40caffcdff164bb37e2e941ff9e3a3dcf4f8f1f96cf736a14a6c9a8f98d3731  results/hd/s/runs/repro-host-2/8-3/result.json
0e5c8d9750d54684ca701cab234569efd4a224dbedc1340f258fc36af802caaa  results/hd/s/runs/repro-host-2/8-3/run.log
fd969c3749d174b4ae7635b176e52634d5e43e4a4269f11ce789787052a1a45b  results/hd/s/runs/repro-host-2/8-4/planning.jsonl
a48ab182c8666f3c64d2a26a2f15027edd7ac57795a8c3759a2cf4dd082d920f  results/hd/s/runs/repro-host-2/8-4/result.json
81524635461a61fdcbbfba462e7cd2988fd95cbde020bc2adc202e947129e3b4  results/hd/s/runs/repro-host-2/8-4/run.log
84ef8edab21b82ce39aac6568c43e4bf3a77ffba4a1bccfcc5232a5b51a30288  results/hd/s/runs/repro-host-2/9-2-nc-bound/result.json
66d29e9ef2624d14af1171b84f613100ba9389b4573b1d18994e11c26b588df7  results/hd/s/runs/repro-host-2/9-2-nc-bound/run.log
ae0a3083404da5eda350c57f6caf5f749b2f334f5c763a989f5906de2ffa04d2  results/hd/s/runs/repro-host-2/9-2/planning.jsonl
f293b86538fa09c078e15bb3c4bbcbef2215b869f04cc013bd15fba690a68800  results/hd/s/runs/repro-host-2/9-2/result.json
0ebcce4562e6cf5149167418b67b6236d6629faf53bf71a6e4d9d13fb8658561  results/hd/s/runs/repro-host-2/9-2/run.log
5fa4943c3c8b0226e6aa6301c899921050122a666dbbc134e46bbfcba09737dd  results/hd/s/runs/repro-host-2/9-2-td-coeff/result.json
8e9218d1f1960ff4b238fb4957e59490524f74db2f92639a2286b04ed2adfcd2  results/hd/s/runs/repro-host-2/9-2-td-coeff/run.log
3c16a2019301f9bb33ad24227492d58ee1de423ff974ff59e0a71d14ea77b3ea  results/hd/s/runs/repro-host-2/9-2-td-horizon/result.json
265a41735a3cd4d54fe1ffe9beaa9a8d2c929b5d73ce6cfbec9189441729f6a9  results/hd/s/runs/repro-host-2/9-2-td-horizon/run.log
3dc3b005d1d8c13ac09a80f93464310072c49790f95715676a6ca1dc77a489ed  results/hd/s/runs/repro-host-2/9-3/planning.jsonl
ed60c8758bdc7754f5bf14c442cd4f2a2e396f9802175332b06ce63da46d4d4d  results/hd/s/runs/repro-host-2/9-3/result.json
3dda9b3ab6985595aa8f785b4ccc74aad5053090e24c5c11688f6e853effbfdc  results/hd/s/runs/repro-host-2/9-3/run.log
4794bbf8a73e4e2728a16822a7391c54a89ee47651192e4aa3829fe6ea3519b4  results/hd/s/runs/repro-host-2/9-4/planning.jsonl
f67715d3a47c24611b8bb0b835d06499e031ad8cf996974879e69ef7a5180649  results/hd/s/runs/repro-host-2/9-4/result.json
687f028d5e0c8f777844e45c2214e6c2ad89eb811553aaac56f353781fd3ff21  results/hd/s/runs/repro-host-2/9-4/run.log
ff90dbf73c16488a1d109edf0151c134de2b064be21eee59872d265b0010e1d2  results/hd/s/runs/repro-host-2/9-5/planning.jsonl
993b59ff3d41d656952a2381f0f956bc51b3a72e6b1544bd7b4ecb259e1c20c7  results/hd/s/runs/repro-host-2/9-5/result.json
46b989bcc44df58eb34b9159192969fbb4c8bdff7a03bbe98271f6ec158c95a3  results/hd/s/runs/repro-host-2/9-5/run.log
```

## E. My scripts and outputs (SHA-256; paths relative to the working folder)

```
dbcb3e0f5f568ffebee7a7fd19f136a58fd4d49d087a8d24b3e9dc656326e25e  scripts/a2_horizon_bound.py
03dcd3f193daca32d8286900422db9faac9c11c1f2c5ee349084a889ceab1fc5  scripts/a2_throat.py
eece7484ffcbb4fa5d013eeaf7a8febab0e07494f426a407e54a5edbf453aba6  scripts/assemble_checks.py
795117f780f6f38ab004eec381358f73ecbf0a2087f0c0218bca3c568d228551  scripts/blind_decimals.py
65a8eb36a9aebb32b7c93564f80d582d9a066657ceb9eb4ccf1526341d597f3a  scripts/check_hde.py
6f4ef149ee7a769f070740a2347ef2539131b58a3767deca8a254268e5e68e38  scripts/check_intervals.py
a3f72a3902ccdc3f7b4f63189935617253bdd13069a165b666c7d7f7f24b5278  scripts/check_mobius_and_records.py
dd1472a0b6298bf83ae37c353ad55347dad5ea455b45abe207df072ac38011b5  scripts/hb_digits.py
1eb7e369791a28c95d06072887264d1fa24c4a1bbea4922fca34e3382047adb0  scripts/hb_exact.py
aed9944aef71dab1a7572fe1885404fb6190d417b6cde2f3ccf531903469e26c  scripts/jsondiff.py
c52d35fab80b2aab7836e0e696508c201b3a06e9adf05aa40d6b130c248d937c  a2_horizon_bound.out
8c26c2f477584526c7112894f045b27b956cdc2c7d91ca0e6a3b3f1e7ef59ee0  a2_throat.out
541a52e7ef9b1a7a686b624e3ea93965c71f1f0d20c411777cef35cefbbfa7cc  blind_decimals.out
84ff8f6f4d61f2110a9abb3d0874161a140957c843b9fc60eac2c45f7cab24bc  check_hde.out
99423039e83f8abe57fe5576b1a6937f612044cdc9874abdabced0c26e2d24c9  check_intervals.out
70801b936fe33e2211793c219935cb3cfd2dfa473b6d5a2d46731d9e27cbd350  check_mobius_and_records.out
eb84760425fa06c54787cf79b39b6e914c3e54745f8c06dd374b822c1cd385f1  hb_digits.out
c15725da8ec84f30c7281ddd84a54429c324598c353c15b6a1fd60e10b6a4610  hb_exact.out
892de6698f100c5db6a1ca78dd7fe905166a2b80354b40d2757b9d1244b76f93  hd_reading_draft/outputs/pilot_git.out
90044d478a022a8981711a4c2f12e616afb5337ab5196f6f98b3fc032a45a93d  hd_reading_draft/outputs/pilot_table.out
0207ffdf65f2c7b4e2d94eb44e35754c57e90a17715e45e79ef1fef70bdc7921  hd_reading_draft/outputs/pilot_void_vs_valid.out
e432b7370f3a73dd5f0fb3b13455f8c3b0079260b8b2f477034affbe7b486097  hd_reading_draft/outputs/repro_equality.out
c450a7ac7b43bf0db72f2ff427e698fac4019fd765831c40565fbd7ef26346da  hd_reading_draft/outputs/seals.out
d4a5a1bb48b125cd17fdde9cc7bbb73cf00d8feb52c2ef237967913127381050  hd_reading_draft/outputs/tds2.out
3261b7443a370f87f8962cf56982e798e896f11395816d4871f3207e30cdb655  hashes_docs_code.txt
c56bba6c8428e6a2969ff70d4cea92e6d086bd050a9d67023ab5975e95dac571  hashes_reviews.txt
8b2c45cc4b0131ff3ad4fc2c46ed7b1076bef619f71aead3af158c5b1fe2d652  hashes_hde_pilot_records.txt
095174d823288834b86b1933e0fe72f5b1518a2911ed675aad6c1895896ea288  hashes_hds_records.txt
589e5310c160b78d48e371fe2d60915f3ecbe1b6bd743c95ff9193ad92747527  sealed_subset.txt
ae237ae4347f7a7748b8a6be0bc27d295f942babb10189b71c17620dfc3e8bb0  blind_sha256sums_check.txt
```
The files `my_mem3_test.out`, `tx_scan.out` and the many other files in the working folder are not mine (the folder is
shared with the parent session); nothing here depends on them.
