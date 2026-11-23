# Working notes: the comparisons behind AUDIT.md (Fable, 2026-11-13; written before AUDIT.md)

Parametrisation used to turn mu-ends into q-ends (every piece, at its own (n, l)): A = (l + n) + (l - 1) mu^2,
B = 2l + n - 1, w = B mu/A = sqrt(1 - q^2), so q(mu)^2 = 1 - w^2; w increases on [0, 1] (gates O5/PARAM; pencil:
w' = B((l + n) - (l - 1)mu^2)/A^2 > 0), so a mu-box [a, b] is the q-interval [q(b), q(a)]. At n = 4 this is onset.param
(A = (l + 4) + (l - 1)mu^2, B = 2l + 3), and gate PARAM4 (HD-E, HD-X-E) checks param_n(4, l) = onset.param(l).
(99/100)^2 = 0.9801 exactly.

## N1. D = 6, l = 2: the three pieces and their two overlaps
- q(1/5)^2 at l = 2: w = (7/5)/(6 + 1/25) = 35/151, w^2 = 1225/22801, q^2 = 21576/22801 (= 0.9462742...).
- q(3/25)^2: w = (21/25)/(6 + 9/625) = 525/3759 = 175/1253, w^2 = 30625/1570009, q^2 = 1539384/1570009 = 31416/32041
  (both divided by 49) (= 0.9801988...).
- q(1/8)^2: w = (7/8)/(6 + 1/64) = 56/385 = 8/55, w^2 = 64/3025, q^2 = 2961/3025 (= 0.9788430...).
- T3's eight boxes (R-T3 result.boxes_mu[i].mu): [3/25, 13/100], [13/100, 7/50], [7/50, 3/20], [3/20, 4/25],
  [4/25, 17/100], [17/100, 9/50], [9/50, 19/100], [19/100, 1/5]: contiguous (0.12, 0.13, ..., 0.20), union [3/25, 1/5],
  so T3 certifies q in [q(1/5), q(3/25)] = [sqrt(21576/22801), sqrt(31416/32041)].
- Overlap 1, O2 with T3: 21576/22801 = 0.94627428... against q_*^2 in the record's isolating interval
  [0.94683882904927334931..., same to 45 digits] (R-O2 q_star_squared_interval; mu_* = 0.198932... < 1/5). The gap
  5.6e-4 is 41 orders above the interval's width, so q(1/5) < q_* exactly. Overlap width q_* - q(1/5) = 0.973056 - 0.972766
  = 2.9e-4.
- Overlap 2, T3 with A2-S: 2961 * 32041 = 94,873,401 and 3025 * 31416 = 95,033,400; 94,873,401 < 95,033,400, so
  2961/3025 < 31416/32041 and q(1/8) < q(3/25) (exact, integers). Width 0.990199 - 0.989365 = 8.3e-4.
- Union: (0, q_*] u [q(1/5), q(3/25)] u [q(1/8), 1] = (0, 1].

## N2. D = 6, l = 3..10: P1 and A2-E meet at the same mu_lo
R-P1 part1[].mu_lo / q_at_mu_lo_squared and R-A2E parts[].mu_lo / q_at_mu_lo_squared, entry by entry:
  l=3: 11/100, 134331349/137053849 (0.980136); l=4: 103/1000, 63226555957929/64510244957929 (0.9801006);
  l=5: 49/500, 312772999176/319113139801 (0.980132); l=6: 47/500, 27471514409/28023764409 (0.980294);
  l=7: 91/1000, 29925587924649/30523890174649 (0.980399); l=8: 89/1000, 142474321369809/145333802369809 (0.980325);
  l=9: 87/1000, 2613126399136/2665281539761 (0.980432); l=10: 43/500, 12122233672881/12366763922881 (0.980227).
Identical in both records. covers_q_max true for all eight (P1), i.e. q(mu_lo)^2 >= 0.9801 exactly; the tightest, l = 4:
64510244957929 * 0.9801 = 63,226,491,103,266 < 63,226,555,957,929. So [0, q(mu_lo)] u [q(mu_lo), 1] = [0, 1] per l.
A2-E's PREREG l.13 says "q(mu_lo(l)) <= 99/100", a known misprint for ">=" (results/a2/STAGE_REPORT_ADDENDUM_1.md section 4);
the record gates the right direction.

## N3. D = 7..11, q <= 99/100: the 18 bands against E2 and against 99/100 (R-HDS coverage fields; decimals mine)
band | q_split (= HD-S q_lo) | q_split^2 | q(mu_b)^2 (exact, record) | decimal | q(mu_a)^2 (exact, record) | decimal
7-2 | 237/250 = 0.948 | 0.898704 | 450385526985669121/501172656585669121 | 0.898665 | 482351496417168561/492144578017168561 | 0.9801012
7-3 | 977/1000 | 0.954529 | 154985298094511521/162372700594511521 | 0.954503 | 616496957997921/629010864247921 | 0.9801054
8-2 | 0 (mu_b = 1) | 0 | 0 | 0 | 17083021501189/17429648063689 | 0.9801128
8-3 | 118/125 = 0.944 | 0.891136 | 3684836513121/4135077513121 | 0.891116 | 199657162856145201/203706576081145201 | 0.9801213
8-4 | 983/1000 | 0.966289 | 978026969107944729/1012152142007944729 | 0.966284 | 3765525061221/3841839123721 | 0.980136
9-2 | 0 | 0 | 0 | 0 | 796755993449624481/812910403449624481 | 0.9801277
9-3 | 921/1000 | 0.848241 | 13843592400702961/16320645300702961 | 0.848225 | 1711069078242249/1745761178242249 | 0.9801278
9-4 | 119/125 = 0.952 | 0.906304 | 1812171689673769/1999642553673769 | 0.906248 | 291488937834369/297405994084369 | 0.9801044
9-5 | 987/1000 | 0.974169 | 38425874043609/39445974043609 | 0.974139 | 88875546247769841/90676699847769841 | 0.9801365
10-2 | 0 | 0 | 0 | 0 | 3841215986197681/3919140742447681 | 0.9801169
10-3 | 49/100 = 0.490 | 0.2401 | 91914991536373201/383045380761373201 | 0.239959 | 1164187484726301/1187794936288801 | 0.980125
10-4 | 23/25 = 0.92 | 0.8464 | 142513652343129921/168386374843129921 | 0.846350 | 616496957997921/629010864247921 | 0.9801054
10-5 | 961/1000 | 0.923521 | 949834170649/1028514420649 | 0.9235011 | 6517045060605261/6649208824667761 | 0.9801234
11-2 | 0 | 0 | 0 | 0 | 211474330206729/215767514206729 | 0.9801027
11-3 | 0 | 0 | 0 | 0 | 153891955293609/157016011543609 | 0.9801036
11-4 | 897/1000 | 0.804609 | 90451546986883929/112426644586883929 | 0.804539 | 1666516108576123609/1700313254176123609 | 0.980123
11-5 | 929/1000 | 0.863041 | 1974131929/2287421929 | 0.8630380 | 134331349/137053849 | 0.980136
11-6 | 121/125 = 0.968 | 0.937024 | 15357181301769/16389437301769 | 0.9370170 | 88875546247769841/90676699847769841 | 0.9801365
Every q(mu_b)^2 <= q_split^2 and every q(mu_a)^2 >= 0.9801 (gate fields "q(mu_b) <= q_lo or mu_b = 1": true and
"q(mu_a) >= q_max": true in all 18 records; verdict VERIFIED in all 18). The four tightest meetings, by integer
cross-multiplication (mine):
- 10-5: 949834170649 * 10^6 = 949,834,170,649,000,000 < 1028514420649 * 923521 = 949,854,666,272,185,129.
- 11-5: 1974131929 * 10^6 = 1,974,131,929,000,000 < 2287421929 * 863041 = 1,974,138,909,026,089.
- 11-6: 15357181301769 * 10^6 = 15,357,181,301,769,000,000 < 16389437301769 * 937024 = 15,357,296,098,252,795,456.
- 8-4: 978026969107944729 * 10^6 = 978,026,969,107,944,729,000,000 < 1012152142007944729 * 966289
  = 978,031,481,148,714,904,240,681.
E2's own coverage, q(mu_lo)^2 >= q_split^2: covers true for all 13 (R-HDE E2[].covers); e.g. 7-2: 6872766153201/7647166153201
= 0.898734 >= 0.898704. The q_hi fields equal the PREREG's q_split table (237/250, 977/1000, 118/125, 983/1000, 921/1000,
119/125, 987/1000, 49/100, 23/25, 961/1000, 897/1000, 929/1000, 121/125) and HD-S's q_lo fields.
Coincidences, checked, not errors: 7-3 and 10-4 share mu_a = 283/2500 and q(mu_a)^2 because w = 5mu/(4 + mu^2) in both
((A, B) = (8 + 2mu^2, 10) and (12 + 3mu^2, 15) are proportional); 11-5's mu_a = 11/100 gives A1's l = 3 value
134331349/137053849 because (14 + 4mu^2, 18) is proportional to (7 + 2mu^2, 9); 9-5 and 11-6 share 1061/10000.

## N4. D = 7..11, l_el <= l <= l0: E1 covers [0, 99/100]
R-HDE E1: 35 entries, q_hi 99/100, covers true in each; L_EL = {5: 4, 6: 5, 7: 6, 8: 6, 9: 7}; E3 l0 = 10, 10, 11, 13, 14.
Entries per D: 7: l = 4..10 (7); 8: 5..10 (6); 9: 6..11 (6); 10: 6..13 (8); 11: 7..14 (8). Tightest: D = 11 l = 7,
63226555957929/64510244957929 = 0.9801006 (the l = 4, n = 4 value again, by proportionality).

## N5. D = 7..11, q in [99/100, 1]
- HD-X-E (R-HDXE): verdict VERIFIED; MEET: all 33 entries equal: true, meets: true, with HD-E mu_lo = HD-X-E mu_lo; the
  33 (D, l) are exactly E1's 35 minus (10, 6) and (11, 7) (which are HD-X-S bands). The q_at_mu_lo_squared values of
  the 33 parts equal E1's for the same (D, l), entry by entry. Each part claims q in [q(mu_lo), 1] with q(mu_lo)^2 >= 0.9801.
  So E1 u HD-X-E = [0, 1] at each of the 33 (D, l); the point q(mu_lo) is the same number in both because both use
  param_n with the same mu_lo.
- HD-X-S (R-HDXS, 11 bands, all VERIFIED): q(1/8)^2 from PARAM: 7-3: 64449/66049 (0.975776); 8-3: 81585/83521 (0.976821);
  8-4: 402633/413449 (0.973839); 9-4: 9945/10201 (0.974904); 9-5: 36225/37249 (0.972509); 10-4: 64449/66049 (0.975776);
  10-5: 42525/43681 (0.973535); 10-6: 788697/811801 (0.971540); 11-5: 609/625 (0.9744); 11-6: 36225/37249 (0.972509);
  11-7: 257481/265225 (0.970802). Each <= 0.9801 (gate true), and each < the matching HD-S q(mu_a)^2 or E1 q(mu_lo)^2
  (all >= 0.9801), so the ranges overlap. Upper end 1 (claim "q in [q(1/8), 1]").
- HD-X-2 (R-HDX2, 9 bands, all VERIFIED): MU1 and q(MU1)^2: 7-2: 1/8, 197505/201601 (0.979683); 8-2: 13/100,
  698908729/714118729 (0.978701); 9-2: 13/100, 7961448561/8130448561 (0.979214); 9-3: 3/25, 2404864/2455489 (0.979383);
  10-2: 13/100, 9829338561/10033828561 (0.979620); 10-3: 3/25, 46562824/47513449 (0.979992); 11-2: 13/100,
  1321538729/1348578729 (0.979950); 11-3: 1/8, 2961/3025 (0.978843); 11-4: 3/25, 1015861/1038361 (0.978332). Each <= 0.9801
  (PARAM true; the largest, 10-3: 47513449 * 0.9801 = 46,567,931.4 > 46,562,824). Claim q in [q(MU1), 1); each HD-X-2
  band is an HD-S band with q(mu_a)^2 >= 0.9801 > q(MU1)^2, so the ranges overlap; q = 1 is Z's.
- Z (R-Z): VERIFIED at n = 2, 3 (information), 4..9 (claim) and N (symbolic): claim A_{l,1} >= 0 for every l >= 2.
- E3 (R-HDE E3): q in [0, 1] for l > l0.
- Partition of l >= 2 at each D (n = D - 2; l_el, n - 1, l0): D = 7: bands 2, 3 | n - 1 = 4 .. 10 | > 10;
  D = 8: 2, 3, 4 | 5..10 | > 10; D = 9: 2..5 | 6..11 | > 11; D = 10: 2..6 | 7..13 | > 13; D = 11: 2..7 | 8..14 | > 14.
  Below 99/100 the split is at l_el instead (4, 5, 6, 6, 7), so (10, 6) and (11, 7) are E1 below and HD-X-S above.
  Bands: 20 = 2 + 3 + 4 + 5 + 6; HD-X-S 11 (2l > n - 1), HD-X-2 9 (2l <= n - 1); HD-S 18 = 20 minus (10, 6), (11, 7).

## N6. The routes (item 4): what each claim must say
- U_- >= 0 route: the claim must give U_- >= 0 for every x in the open exterior (0, x_H(q)) at every q of the range;
  then V = f U_-/(64 r^2 H_-^2) >= 0 because f > 0 (exterior; at q = 1 f = (1 - Y)^2 > 0 for rho > 1), r > 0 and
  H_- = m + n(n + 1)(1 + m delta)x/2 >= m > 0 (m > 0, delta >= 0, x >= 0); then the form is >= 0 term by term. The
  records claim it on the closed set [0, x_H] (O2, P1, E1, E2, A2-E, HD-X-E), on [0, 2] (Lemma U, E3), with strictness
  where it holds. Zeros at the extremal horizon (A2-E l = 3; HD-X-E l = n - 1; O2 at (q_*, x_H)) are outside the open
  exterior and harmless.
- N > 0 route: the claim must give, for each q of the range, a P that is C^1 on (0, 1) with N >= 0 on (0, 1), plus
  q^2 <= 1, m > 0, delta >= 0 (prop3_Dn's hypotheses), and the inverse tortoise map R (pencil for q < 1; tortoise_q1 at
  q = 1). T3: P polynomial in (z, mu), N > 0 on [0, 1] x box, L > 0 (R-T3; METHOD.md Prop. 3 at n = 4; Lean prop3_D6).
  HD-S: P polynomial (z) or Phat/(z + delta_b)^d with delta_b > 0 (zeta), N L s^{2e} > 0 and L > 0 on [0, 1] x box
  (METHOD_ADDENDUM_2; prop3_Dn, prop3_Dn_zeta); q(mu_a) < 1 so the q < 1 map suffices. A2-S, HD-X-S: singular P with a
  pole at -eps <= 0, N > 0 on (0, 1) for mu in [0, 1/8] (METHOD_ADDENDUM_3 at mu = 0; prop3_Ioo/prop3_Dn; tortoise_q1).
  HD-X-2: mu in (0, MU1], pole at -eps < 0 (METHOD_ADDENDUM_2 applies; prop3_Dn).
- q = 1, Theorem 2: Z-id (u0 solves the zero-energy equation), Z-pos (u0 > 0), the tortoise map at q = 1, Lemma 1 with
  S = -(log u0)_{r*}: V + S' - S^2 = 0 (Lean A_nonneg, every n >= 2 and l >= 2).

## N7. The corollary (item 5)
V is bounded and continuous on R (H_- >= m > 0; U_- bounded on [0, x_H]; f <= 1; V -> 0 at both ends, like c/r*^2 at an
extremal throat). A = -d^2/dr*^2 + V is self-adjoint on H^2(R) (a bounded perturbation of -d^2/dx^2), its form domain is
H^1, and the form is >= 0 on C_0^infty, hence on H^1 by density, so A >= 0. A mode e^{kappa t}phi with 0 != phi in L^2
solves phi'' = (V + kappa^2)phi, so phi'' in L^2 and phi in H^2 = dom(A); then <phi, A phi> = -kappa^2 ||phi||^2 < 0,
a contradiction. The draft's section 2 defines a mode as an eigenfunction of A, which skips the H^2 step (one clause).

## N8. Draft numbers checked against the records (sections 3-5, and section 4 as the brief's range covers it)
Agree: the cubic for q_*^2 and q_* = 0.97305... (prefix of 0.9730564...); T3's and A2-S's exact ends; l = 3..10 and
l >= 11 at D = 6; l_el = 4, 5, 6, 6, 7; l0 = 10, 10, 11, 13, 14; the 18 / 13 / 5 band counts and their (D, l);
q_split values; the interior band's q(mu_b) < 0.490; the 20 / 11 / 9 split; MEET; q(1/8)^2 and q(MU1)^2 <= (99/100)^2;
the largest q(MU1)^2 = 46562824/47513449 at D = 10 l = 3; Theorem 2's statement and the n range; MU1 in {1/8, 13/100,
3/25}; the cover constants.
Differ:
- l.154 "959747/17496 ≈ 54.86": results/a1/RESULT_ADDENDUM_1.md (BHM-119) l.14-19, 27: the inward quote is 54.85 (or
  54.855); 54.86 is the rounded-up value that addendum corrects in five places.
- l.213 "[0.97277…, 0.99019…]": the digits of sqrt(21576/22801) are 0.9727663... (results/p3/RESULT_ADDENDUM_1.md l.16);
  0.97277 is the inward (rounded-up) value, so the ellipsis is misleading; write [0.97277, 0.99019] (inward) or
  [0.97276…, 0.99019…].
- l.214 "[0.98936…, 1]": the digits are right (0.989365...), but section 5's convention says inward; the inward lower
  end is 0.98937 (results/a2/s/RESULT_ADDENDUM_1.md l.33; results/a2/STAGE_REPORT_ADDENDUM_1.md section 3).
- l.230 "q(mu_b) = 0.48986…": the digits are 0.489856...; 0.48986 is inward; same ellipsis point (HD-S RESULT l.50 has it too).
- l.175-176 (section 4.5): "Their union covers (0, 1) × (0, mu_1]": A2-S and HD-X-S claim q = 1, so their cover must and
  does include mu = 0: (0, 1) x [0, 1/8] (results/a2/s/PREREG.md l.45; results/hdx/s/PREREG.md l.39); and "each chart's
  polynomial comes after an exact division" holds for all four charts only in HD-X-2 (A2-S/HD-X-S use NL itself on O, O').
- l.202 (convention): "square roots of rationals" does not cover q_*, a cubic irrational compared through O1's isolating
  interval.
