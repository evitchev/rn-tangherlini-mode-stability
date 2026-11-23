# Ledger: citation check of stability_v0.8.tex (sha256 975aa46e...02a4) and its PDF (23eae9d6...b1fe)

One entry per \cite command (K01-K83, in the order of the text) and per reference entry (R01-R34, by the PDF's number). Keys are the S-labels; [n] is the PDF's number. Passages are from the text layers named in SOURCES.md (pdftotext -layout), lines counted as grep -n does; runs of spaces are collapsed, lines joined with a space, and "[...]" joins separate ranges. Basis: READ = read at the source for this check; COMPARED = an earlier check of mine covered the same claim at the same passage, and v0.8's wording was compared with the wording checked then; RECORD = checked against the record fetched on 2026-11-23.

## K01 S5,S23 [1],[2], tex l.86 (sec:intro), anchor (none): **SAYS MORE** (READ)

- Lines read: S5 l.1407-1409, 1892-1896; S23 l.21-27
- Passage: S5: The reduced master equations have the canonical forms f (f Φ′± )′ + ω 2 − VS± Φ± = SS± . (5.59) [...] In the present paper, we have extended the formulation for perturbations of a generalised static black hole given in Paper I to an Einstein-Maxwell system in a generalised static spacetime with a static electric field, and we have shown that the perturbation equations for vector and scalar perturbations can be reduced to two decoupled second-order ODEs for the gravitational mode and the electromagnetic || S23: We show that in four or more spacetime dimensions, the Einstein equations for gravita- tional perturbations of maximally symmetric vacuum black holes can be reduced to a single second-order wave equation in a two-dimensional static spacetime, irrespective of the mode of perturbations. Our starting point is the gauge-invariant formalism for perturbations in an arbitrary number of dimensions developed by the present authors, and the variable for the final second-order master equation is given by a simple combination of gauge-invariant variables in this formalism. Our formulation applies to the case of non-vanishing as well as
- Note: S5 is the reduction for the charged case: two decoupled second-order ODEs for the vector and scalar types (l.1892-1896), in the canonical Schrödinger form (5.59) (l.1407-1409). S23 is the vacuum case: "maximally symmetric vacuum black holes" (l.21-22). Cited jointly for "static charged black holes", [2] says more than S23 does. Fix: "... sector by sector [1], extending their reduction for vacuum black holes [2]".

## K02 S6 [3], tex l.87 (sec:intro), anchor (none): **OK** (READ)

- Lines read: S6 l.21-31, 644-647
- Passage: S6: We investigate the classical stability of higher-dimensional Schwarzschild black holes with respect to linear perturbations in the framework of a gauge-invariant formalism for gravi- tational perturbations of maximally symmetric black holes. This formalism was recently developed by the present authors. The perturbations are classified into three types, those of tensor, vector, and scalar modes, according to their tensorial behaviour on the spherical section of the background metric. The vector- and scalar-type modes correspond, respec- tively, to the axial and polar modes in the four-dimensional case. We show that for each mode of the perturbations, the spatial derivative part of the master equation is a positive, self-adjoint operator in the L2 -Hilbert space, and hence that the master equation for each type of perturbation has no normalisable negative modes that would correspond to unstable solutions. [...] Clearly Ṽ > 0, and thus A with domain C0∞ (r∗ ) is strictly positive, so is the self- adjoint extension. The higher-dimensional Schwarzschild black holes are therefore stable with respect to scalar perturbations. This completes the stability analysis for higher-dimensional Schwarzschild black holes.
- Note: "The higher-dimensional Schwarzschild black holes are therefore stable with respect to scalar perturbations. This completes the stability analysis" (l.645-647), at general n; tensor and vector earlier in §2. No anchor in v0.8; suggested: abstract and p.13.

## K03 S5,S28 [1],[4], tex l.88 (sec:intro), anchor (none): **OK** (READ)

- Lines read: S5 l.1878-1881, 1903-1907; S28 l.774-776
- Passage: S5: For n = 2, this is positive definite for m > 0. When K = 1, λ ≥ 0 and n = 3 or when λ ≥ 0, Q = 0 and the horizon is S 4 , from m ≥ n + 2 (l ≥ 2) and the behaviour of xh (see Fig. 2), we can show that ṼS− > 0. Hence, in these special cases, the black hole is stable with respect to any type of perturbation. [...] Tensor Vector Scalar Q = 0 Q 6= 0 Q = 0 Q 6= 0 Q=0 Q 6= 0 d = 4, 5 OK K=1 λ=0 OK OK OK OK OK d≥6? || S28: In particular for the case of Λ = 0, we have established the stability of a spherically symmetric black hole for arbitrary dimensions, and that of of a spherically symmetric black hole with charge for D = 4 and D = 5.
- Note: S5: for n = 2 the deformed potential is positive; "When K = 1, λ ≥ 0 and n = 3 ... ṼS− > 0. Hence, in these special cases, the black hole is stable with respect to any type of perturbation" (l.1878-1881, p.32); Table I (p.33). S28: "the stability ... of a spherically symmetric black hole with charge for D = 4 and D = 5" (l.774-776, p.13).

## K04 S5 [1], tex l.89 (sec:intro), anchor Table~I: ``$d \ge 6$?'': **OK** (READ)

- Lines read: S5 l.1899-1907
- Passage: S5: Table I. Stabilities of generalised static black holes. In this table, “d” represents the spacetime dimension, n + 2. The results for tensor perturbations apply only for maximally symmetric black holes, while those for vector and scalar perturbations are valid for black holes with generic Einstein horizons, except in the case with K = 1, Q = 0, λ > 0 and d = 6. Tensor Vector Scalar Q = 0 Q 6= 0 Q = 0 Q 6= 0 Q=0 Q 6= 0 d = 4, 5 OK K=1 λ=0 OK OK OK OK OK d≥6?
- Check: "$d \ge 6$?": verbatim
- Note: Table I (p.33), K = 1, λ = 0, scalar, Q ≠ 0: "d = 4, 5 OK" and "d≥6?". "d" is the spacetime dimension n + 2 (l.1899-1900).

## K05 S28 [4], tex l.89 (sec:intro), anchor Table~1: **OK** (COMPARED)

- Lines read: S28 l.740-745
- Passage: S28: Table 1: Stability of static black holes. Tensor Vector Scalar Q = 0 Q 6= 0 Q = 0 Q 6= 0 Q = 0 Q 6= 0 D = 4, 5 OK K = 1 λ =0 OK OK OK OK OK D ≥ 6 ?
- Note: As BHM-189 C01: Table 1 (p.13), "D ≥ 6 ?".

## K06 S48 [5], tex l.91 (sec:intro), anchor p.~40: **OK** (COMPARED)

- Lines read: S48 l.2273-2276
- Passage: S48: Our results are summarized in Table I. As shown there, maximally symmetric black holes are stable with respect to tensor and vector perturbations over the entire parameter range. In contrast, for scalar type perturbation, we were not able to prove even the stability of asymptotically flat black holes with charge in generic dimensions,
- Check: "for scalar type perturbation, we were not able to prove even the stability of asymptotically flat black holes with charge in generic dimensions": verbatim
- Note: As BHM-189 C02: quote verbatim (l.2275-2276, p.40); S48 is the authors' review chapter.

## K07 S28 [4], tex l.99 (sec:intro), anchor eqs.~(76)--(77): **OK** (COMPARED)

- Lines read: S28 l.705-712, 762
- Passage: S28: By the similar S-deformation f dh S= ; h = r n/2−1 H− , (76) h dr the effective potential VS− for Φ− is transformed to k2 f ṼS− = [2m − (n + 1)(n − 2)(1 + mδ)x] . (77) 2r 2 H− [...] Hence, the gravitational mode is also stable for n = 2.
- Note: As BHM-189 C03: eqs. (76)-(77) (pp.12-13); at n = 2 the bracket is 2m and l.762 concludes stability for n = 2. The D = 5 part is cited to S48 p.40 (K08).

## K08 S48 [5], tex l.100 (sec:intro), anchor p.~40: **OK** (READ)

- Lines read: S48 l.2253-2265
- Passage: S48: Using a similar transformation, we can also prove the stability with respect to the gravitational mode Φ− for some special cases. For example, the S-deformation of VS− with f dh− S= , h− = r n/2−1 H− (8.21) h− dr leads to k2 f ṼS− = [2m − (n + 1)(n − 2)(1 + mδ)x] . (8.22) 2r 2 H− For n = 2, this is positive definite for m > 0. When K = 1, λ ≥ 0 and n = 3 or when λ ≥ 0, Q = 0 and the horizon is S 4 , we can show that ṼS− > 0. Hence, in these special cases, the black hole is stable with respect to any type of perturbation.
- Note: S48's S-deformation (8.21)-(8.22) (the same Ṽ as S28's (76)-(77)): "For n = 2, this is positive definite for m > 0. When K = 1, λ ≥ 0 and n = 3 ... we can show that ṼS− > 0" (l.2263-2264, p.40). Spherical horizon (K = 1), λ ≥ 0, D = 5, as v0.8 says.

## K09 S28 [4], tex l.102 (sec:intro), anchor p.~13: **OK** (COMPARED)

- Lines read: S28 l.762-767
- Passage: S28: Hence, the gravitational mode is also stable for n = 2. However, for n > 2, ṼS− becomes negative near the horizon in general (See Fig.3). The S-deformation used in the neutral case does not work either, because it cannot remove a negative ditch of VS− produced by the charge near the horizon. We have not been able to prove the stability for n > 2 by this method, except for some special cases.
- Check: "becomes negative near the horizon in general": verbatim; "except for some special cases": verbatim
- Note: As BHM-189 C04, with its fix taken: both fragments verbatim, "in general" kept (l.763, l.767, p.13).

## K10 S48 [5], tex l.102 (sec:intro), anchor p.~40: **OK** (COMPARED)

- Lines read: S48 l.2263-2265
- Passage: S48: For n = 2, this is positive definite for m > 0. When K = 1, λ ≥ 0 and n = 3 or when λ ≥ 0, Q = 0 and the horizon is S 4 , we can show that ṼS− > 0. Hence, in these special cases, the black hole is stable with respect to any type of perturbation.
- Note: The D = 5 special case named in BHM-189 C04's note (S48 l.2263-2265, p.40).

## K11 S5 [1], tex l.105 (sec:intro), anchor p.~32: **OK** (READ)

- Lines read: S5 l.1882-1888
- Passage: S5: However, for the other cases, ṼS− is not positive definite for generic values of the parameters. The S-deformation used to prove the stability of neutral black holes in Paper II is not effective either. This is because VS− has a negative region around the horizon for the extremal and near extremal cases, as shown in Fig. 4, and the S-deformation cannot remove this negative region if S is a regular function at the horizon. Hence, determination of the stability for these generic cases with n ≥ 3 is left as an open problem.
- Check: "the S-deformation cannot remove this negative region if $S$ is a regular function at the horizon": verbatim
- Note: Quote verbatim (l.1886-1887, p.32). The source's sentence: VS− "has a negative region around the horizon for the extremal and near extremal cases" (l.1884-1885), as v0.8 says.

## K12 S48 [5], tex l.108 (sec:intro), anchor p.~43: **OK** (COMPARED)

- Lines read: S48 l.2404-2408
- Passage: S48: For some cases, in particular, when electric charge and cosmological constant are involved, we have not yet been able to draw definite conclusions for the stability problem with respect to scalar type perturbations. This is in part because there does not seem to be a systematic method to find such a desirable function S that could apply to generic cases. In particular, for the charged black hole case, the potential
- Check: "there does not seem to be a systematic method to find such a desirable function $S$ that could apply to generic cases": verbatim
- Note: As BHM-189 C05, with its fix taken: the quote now runs to "that could apply to generic cases" (l.2406-2408, p.43), verbatim.

## K13 S14 [6], tex l.114 (sec:intro), anchor Table~I: **SAYS MORE** (READ)

- Lines read: S14 l.135-138, 142-154
- Passage: S14: propagating on the D-dimensional Schwarzschild back- pure Reissner-Nordström (RN) black holes (ρ = 0). From ground in the limit of vanishing charge. the Table I one can see that quasinormal modes of non- We shall imply that Ψ ∼ e−iωt , ω = ωRe − iωIm , so extremal pure RN holes are damped for D = 6, 7, ..11. that ωIm > 0 corresponds to a stable (decayed) mode, For the near extremal values of charge Q, a power-law [...] TABLE I: l = 2 fundamental frequencies of gravitational perturbations of scalar type V− of D-dimensional RNdS black holes. q D=5 D=6 D=7 D=8 D=9 D = 10 D = 11 0 0.948 − 0.256i 1.137 − 0.304i 1.339 − 0.401i 1.564 − 0.603i 1.997 − 0.863i 2.460 − 0.987i 2.902 − 1.087i 0.1 0.941 − 0.254i 1.130 − 0.302i 1.332 − 0.401i 1.558 − 0.608i 1.998 − 0.862i 2.459 − 0.983i 2.900 − 1.083i 0.2 0.922 − 0.247i 1.110 − 0.296i 1.311 − 0.400i 1.545 − 0.623i 2.001 − 0.856i 2.456 − 0.973i 2.895 − 1.072i 0.3 0.894 − 0.237i 1.080 − 0.289i 1.282 − 0.402i 1.537 − 0.646i 2.002 − 0.844i 2.449 − 0.956i 2.884 − 1.053i 0.4 0.859 − 0.225i 1.045 − 0.282i 1.248 − 0.406i 1.545 − 0.660i 1.997 − 0.822i 2.435 − 0.932i 2.866 − 1.029i 0.5 0.821 − 0.213i 1.007 − 0.276i 1.219 − 0.414i 1.552 − 0.649i 1.984 − 0.794i 2.412 − 0.903i 2.840 − 1.001i 0.6 0.782 − 0.201i 0.970 − 0.271i 1.198 − 0.419i 1.545 − 0.624i 1.959 − 0.764i 2.380 − 0.875i 2.805 − 0.974i 0.7 0.742 − 0.190i 0.938 − 0.267i 1.180 − 0.412i 1.522 − 0.596i 1.925 − 0.737i 2.342 − 0.851i 2.764 − 0.953i 0.8 0.705 − 0.181i 0.908 − 0.260i 1.156 − 0.399i 1.490 − 0.575i 1.888 − 0.720i 2.303 − 0.836i 2.725 − 0.938i 0.9 0.670 − 0.172i 0.878 − 0.252i 1.128 − 0.387i 1.459 − 0.562i 1.855 − 0.707i 2.268 − 0.823i 2.689 − 0.926i 0.98 0.643 − 0.165i 0.854 − 0.245i 1.107 − 0.380i 1.435 − 0.552i − − −
- Note: Table I (p.3) is "l = 2 fundamental frequencies of gravitational perturbations of scalar type V−" (l.142): one mode per entry, the fundamental. v0.8 says they "computed the ℓ = 2 quasinormal modes" and "found every computed mode damped". The rest holds: D = 5-11, q = Q/Qext up to 0.98 (D = 5-8) and 0.9 (D = 9-11), every Im ω < 0, and the values are for pure RN, ρ = 0 (l.135-137; the caption says RNdS). Fix: "computed the fundamental ℓ = 2 quasinormal mode ... and found it damped at every computed point".

## K14 S26 [7], tex l.116 (sec:intro), anchor (none): **OK** (COMPARED)

- Lines read: S26 l.18-23
- Passage: S26: charged black holes starts. The larger D is, the smaller is the threshold value of Λ. We have shown that the ratio ρ = rh /rcos (where rcos and rh are the cosmological and event horizons) is proportional to e−(D−4)/2 at the onset of instability for D = 7, 8, . . . 11, implying that the same law should fulfill for arbitrary D. This is numerical evidence that extremally charged Reissner-Nordstrøm-de Sitter black holes are gravitationally unstable for D > 6, while asymptotically flat extremally charged Reissner-Nordstrøm black holes are stable for all D. The instability is not connected to the horizon
- Note: As my check of 2026-10-22 (target_A.md, 1309.7667, abstract l.22-23): "numerical evidence that ... asymptotically flat extremally charged Reissner-Nordstrøm black holes are stable for all D" (l.21-23). No anchor in v0.8; suggested: abstract.

## K15 S32 [8], tex l.117 (sec:intro), anchor (none): **OK** (READ)

- Lines read: S32 l.867-878, 968-975
- Passage: S32: D = 7, l = 2 Q n=0 n=1 0 1.339158 − 0.400860i 1.185695 − 1.100378i 0.1 1.331837 − 0.400562i 1.179698 − 1.090348i 0.2 1.311363 − 0.400306i 1.161451 − 1.061660i 0.3 1.281662 − 0.401696i 1.129749 − 1.018067i 0.4 1.248303 − 0.406452i 1.081359 − 0.965418i 0.5 1.218338 − 0.414393i 1.010141 − 0.914494i 0.6 1.197456 − 0.419240i 0.912490 − 0.891908i 0.7 1.180123 − 0.412358i 0.842223 − 0.947155i 0.8 1.156032 − 0.398594i 0.865678 − 0.946362i 0.9 1.127843 − 0.387023i 0.845565 − 0.919864i [...] Q = 0.98, l = 2 D n=0 n=1 5 0.643626 − 0.165328i 0.578828 − 0.530191i 6 0.854710 − 0.244925i 0.733131 − 0.757077i 7 1.105518 − 0.379003i 0.829412 − 0.901894i 8 1.435632 − 0.552161i 0.841175 − 0.969673i Table 7: QN frequency for scalar(−) perturbation for Q = 0.98.
- Note: Compared at every point both tables give (ℓ = 2, fundamental): D = 7, q = 0, 0.1, ..., 0.9 (S32 Table 5) and 0.98, and D = 6, 0.98 (S32 Table 7). S32's values, rounded to S14's three decimals, equal S14's at 7 of the 12 points; at the other 5 they differ by one unit in the third decimal (largest difference 0.0015, D = 7, q = 0.98: S14 1.107 − 0.380i, S32 1.105518 − 0.379003i). "Match" holds to about 0.1%; "agree to within 0.002" would be exact. Note: my check of 2026-11-10 (zmode_litcheck, Q5) found S32 disagreeing with Konoplya–Zhidenko hep-th/0703231 (S8) at Q > 0; S14 is a different paper and agrees with S32. No anchor in v0.8; suggested: S32 Tables 5 and 7.

## K16 S14 [6], tex l.117 (sec:intro), anchor (none): **OK** (READ)

- Lines read: S14 l.142-154
- Passage: S14: TABLE I: l = 2 fundamental frequencies of gravitational perturbations of scalar type V− of D-dimensional RNdS black holes. q D=5 D=6 D=7 D=8 D=9 D = 10 D = 11 0 0.948 − 0.256i 1.137 − 0.304i 1.339 − 0.401i 1.564 − 0.603i 1.997 − 0.863i 2.460 − 0.987i 2.902 − 1.087i 0.1 0.941 − 0.254i 1.130 − 0.302i 1.332 − 0.401i 1.558 − 0.608i 1.998 − 0.862i 2.459 − 0.983i 2.900 − 1.083i 0.2 0.922 − 0.247i 1.110 − 0.296i 1.311 − 0.400i 1.545 − 0.623i 2.001 − 0.856i 2.456 − 0.973i 2.895 − 1.072i 0.3 0.894 − 0.237i 1.080 − 0.289i 1.282 − 0.402i 1.537 − 0.646i 2.002 − 0.844i 2.449 − 0.956i 2.884 − 1.053i 0.4 0.859 − 0.225i 1.045 − 0.282i 1.248 − 0.406i 1.545 − 0.660i 1.997 − 0.822i 2.435 − 0.932i 2.866 − 1.029i 0.5 0.821 − 0.213i 1.007 − 0.276i 1.219 − 0.414i 1.552 − 0.649i 1.984 − 0.794i 2.412 − 0.903i 2.840 − 1.001i 0.6 0.782 − 0.201i 0.970 − 0.271i 1.198 − 0.419i 1.545 − 0.624i 1.959 − 0.764i 2.380 − 0.875i 2.805 − 0.974i 0.7 0.742 − 0.190i 0.938 − 0.267i 1.180 − 0.412i 1.522 − 0.596i 1.925 − 0.737i 2.342 − 0.851i 2.764 − 0.953i 0.8 0.705 − 0.181i 0.908 − 0.260i 1.156 − 0.399i 1.490 − 0.575i 1.888 − 0.720i 2.303 − 0.836i 2.725 − 0.938i 0.9 0.670 − 0.172i 0.878 − 0.252i 1.128 − 0.387i 1.459 − 0.562i 1.855 − 0.707i 2.268 − 0.823i 2.689 − 0.926i 0.98 0.643 − 0.165i 0.854 − 0.245i 1.107 − 0.380i 1.435 − 0.552i − − −
- Note: As K15.

## K17 S52 [9], tex l.119 (sec:intro), anchor (none): **OK** (COMPARED)

- Lines read: S52 l.77, 2438-2439
- Passage: S52: 5 Light quasinormal spectrum or the RN black hole 39 [...] (5.22), our final result for the light quasinormal mode frequencies associated with shape fluctuations, is correct as stated for l > 1, but requires clarification for
- Note: "light quasinormal modes" is S52's term (section 5, "Light quasinormal spectrum", l.77), as in BHM-189 C06's note.

## K18 S52 [9], tex l.121 (sec:intro), anchor pp.~43--44: **OK** (COMPARED)

- Lines read: S52 l.2466-2479
- Passage: S52: large D and has independently obtained the result (5.22). 37 2i Had the mode with ωr0 = 1+Q 2 been physical, it would have represented an instability, con- 0 tradicting the well known stability of Reissner Nordstrom black holes (atleast of sufficiently small charge) in arbitrary dimensions. – 43 – As we have mentioned above, (5.22) is correct as stated for l ≥ 2. It is easily verified 38 that all quasinormal modes with l ≥ 2 have negative imaginary components (and so represent decaying fluctuations).
- Note: As BHM-189 C06, with its fix taken (light modes, at leading order). pp.43-44 are printed numbers: printed 43 ends at l.2476, and the passage l.2477-2479 opens printed 44 (PDF 46).

## K19 S51 [10], tex l.121 (sec:intro), anchor p.~6: **OK** (COMPARED)

- Lines read: S51 l.324-330
- Passage: S51: S n+1 . As boundary condition we demanded Fm (z) ∝ (cos z)ℓ at z = π/2 5 . The modes with ℓ > 1 (ℓ > 0) describe dynamical perturbation of gravitational perturbations (gauge field perturbations). So we consider the gravitational perturbations with ℓ > 1 and gauge field perturbations with ℓ > 0. At the zero cosmological constant limit L → ∞, these results reproduce the quasinormal modes of Reissner-Nordstrom black hole obtained in [12]. At Q = 0, ω± reduces to quasinormal modes of scalar type perturbation of (Anti) de Sitter Schwarzschild black hole [15]. At the both limits, the perturbations are stable. On the other
- Note: As BHM-189 C07, with its fix taken. p.6 is printed (PDF p.7).

## K20 S9 [11], tex l.126 (sec:intro), anchor (none): **OK** (READ)

- Lines read: S9 l.15-21, 447-458
- Passage: S9: If the potential contains a small negative region, usually, the S-deformation method was used to show the non-existence of unstable mode. However, in some cases, it is hard to find an appropriate deformation function analytically because the only way known so far to find it is a try-and-error approach. In this paper, we show that it is easy to find a regular deformation function by numerically solving the differential equation such that the deformed potential vanishes everywhere, when the spacetime is stable. Even if the spacetime is almost marginally stable, our method still works. [...] finite values at the boundary x → ±∞. Since it is known that the ground state for the one-dimensional Schödinger equation has no nodes (for example, see [25, 26]), Φ0 cannot becomes zero except at the boundary. So, we can define a function 1 dΦ0 (x; ω(α)) S := − , (29) Φ0 (x; ω(α)) dx and this is regular in −∞ < x < ∞. We can show that S satisfies dS V + − S 2 = ω2. (30) dx If we assume the function S has a smooth limit in α → αcr + 0, this becomes a regular solution of Eq.(9) since ω 2 → 0 in this limit.
- Note: S9 finds S by solving numerically the equation for which the deformed potential vanishes (abstract l.18-21), i.e. S = −Φ′/Φ for a zero-energy solution Φ; l.447-458 tie it to the nodeless ground state at the onset. The explicit "zero-energy solution without zeros" form is S27's (K21).

## K21 S27 [12], tex l.126 (sec:intro), anchor (none): **OK** (READ)

- Lines read: S27 l.86-95, 154-158
- Passage: S27: Eq. (5) is satisfied by 1dΦE=0 S=− , (6) ΦE=0 dx 2 with a solution of the Schrödinger equation with zero energy ΦE=0 .1 Thus, the existence of ΦE=0 which does not have zero anywhere implies the existence of a regular solution of Eq. (5). In this paper, we show the existence of such a wave function when the spacetime is stable (under some assumptions). This result is an almost immediate consequence of the [...] If the energy of the ground state is larger than zero, from Lemma 1, we can construct a solution of the Schrödinger equation with zero energy which does not have zero anywhere when the potential is in a finite box, i.e., V is bounded and piecewise continuous in −L < x < L with a positive constant L, but V = ∞ in |x| ≥ L. Using such a solution ΦE=0 , we can construct a regular S-deformation as
- Note: S = −Φ′E=0/ΦE=0 (eq. 6), and "the existence of ΦE=0 which does not have zero anywhere implies the existence of a regular solution" (l.86-94, pp.2-3).

## K22 S53 [13], tex l.128 (sec:intro), anchor p.~11: **OK** (COMPARED)

- Lines read: S53 l.525-530
- Passage: S53: In this paper, we extended the formalism in [16, 17] to coupled systems where the per- turbative field equations take the form of systems of coupled Schrödinger equations. Similar to [16, 17], the existence of S-deformation implies the linear mode stability of the system. Also, we applied our formalism to the case of the Schwarzschild black hole in dynamical Chern-Simons gravity and a charged Kaluza-Klein black hole [22, 30], and we showed the stability of the spacetime by finding a regular S-deformation function numerically. While
- Note: As BHM-189 C08; wording unchanged; p.11 = l.525-530.

## K23 S49 [14], tex l.133 (sec:intro), anchor abstract: **OK** (COMPARED)

- Lines read: S49 l.20-30
- Passage: S49: Abstract We prove the linear stability of subextremal Reissner-Nordström spacetimes as solutions to the Einstein–Maxwell equation. We make use of a novel representation of gauge-invariant quanti- ties which satisfy a symmetric system of coupled wave equations. This system is composed of two of the three equations derived in our previous works [20], [21], where the estimates required arbitrary smallness of the charge. Here, the estimates are obtained by defining a combined energy-momentum tensor for the system in terms of the symmetric structure of the right hand sides of the equations. We obtain boundedness of the energy, Morawetz estimates and decay for the full subextremal range |Q| < M , completely in physical space. Such decay estimates, together with the estimates for the gauge-dependent quantities of the perturbations obtained in [22], settle the problem of linear sta- bility to gravitational and electromagnetic perturbations of Reissner-Nordström solution in the full subextremal range |Q| < M .
- Note: As BHM-189 C09.

## K24 S50 [15], tex l.136 (sec:intro), anchor abstract: **OK** (COMPARED)

- Lines read: S50 l.26-29
- Passage: S50: tion. In the analysis of the master quantities, we strengthen the mode stability result of Kodama-Ishibashi to a uniform boundedness estimate in all dimensions; further, we prove decay estimates in the case of six or fewer spacetime dimensions. Finally, we provide a rigorous argument
- Check: "to a uniform boundedness estimate in all dimensions": verbatim
- Note: As BHM-189 C10: quote verbatim.

## K25 S40 [16], tex l.139 (sec:intro), anchor abstract: **OK** (COMPARED)

- Lines read: S40 l.7-12
- Passage: S40: We study linearized perturbations of the subextremal Kerr–Newman black hole solution of the Einstein–Maxwell equations. We show how to overcome what Chandrasekhar called the “apparent indissolubility of the coupling between the spin-1 and spin-2 fields” by using a matrix integrating factor for suitably transformed first-order systems that describe the radiative degrees of freedom. For the radial ODEs obtained after angular separation, we prove mode stability on the real axis, i.e., the absence of quasinormal modes with real frequencies, using a Whiting-type transform.
- Note: As BHM-189 C11, with its fix taken ("subextremal"); "for the radial ODEs obtained after angular separation, we prove mode stability on the real axis, i.e., the absence of quasinormal modes with real frequencies" (l.11-12).

## K26 S41 [17], tex l.141 (sec:intro), anchor p.~5: **OK** (COMPARED)

- Lines read: S41 l.444-445
- Passage: S41: (2) The mode stability result of Andersson–Häfner–Whiting [AHW24] for linearized gravity holds in the full subextremal range and is used here as a black box.
- Check: "as a black box": verbatim
- Note: As BHM-189 C12: quote verbatim. p.5 is printed (PDF p.9).

## K27 S41 [17], tex l.141 (sec:intro), anchor (none): **OK** (READ)

- Lines read: S41 l.1-12
- Passage: S41: NONLINEAR STABILITY OF SUBEXTREMAL KERR BLACK HOLES PETER HINTZ Abstract. We settle the global nonlinear stability problem for the family of Kerr black holes in the full subextremal range: spacetimes evolving from initial data close to those of a subextremal Kerr black hole as solutions of the Einstein vacuum equation Ric(g) = 0 settle down to a nearby −2−ϵK member of the Kerr family at the rate O(t∗ ) in spatially compact regions. For the initial data, we require O(r −1−ϵ0 )-decay for ϵ
- Note: A date reference ("At the time of"); S41 v2 is of 3 Aug 2026.

## K28 S41 [17], tex l.142 (sec:intro), anchor p.~7: **OK** (COMPARED)

- Lines read: S41 l.538-541
- Passage: S41: (15) Hintz–Petersen–Vasy [HPV25] proved the nonlinear stability of Kerr–de Sitter black holes in the full subextremal range, conditional on the validity of mode stability for the linearized Einstein equation—which, unlike in the Kerr case, remains an open problem except in the slow-rotation regime (see also [Hin25b] for the small mass regime). The basic strategy is
- Check: "remains an open problem except in the slow-rotation regime": verbatim
- Note: As BHM-189 C13, with its fix taken ("with a further result for small mass cited there"): quote verbatim. p.7 is printed (PDF p.11).

## K29 S43 [18], tex l.144 (sec:intro), anchor abstract: **SAYS MORE** (READ)

- Lines read: S43 l.11-13, 22-27
- Passage: S43: We study linearized gravitational perturbations of five-dimensional asymptotically flat Myers– Perry black holes with two unequal spins. We construct separated solutions for the five coupled gauge-invariant polarizations for arbitrary azimuthal mode numbers. The key observation is that [...] of each separated solution share a single radial amplitude. We prove completeness of the angular harmonics at real frequencies and show that the resulting physical perturbations admit local metric reconstruction. In the singly spinning limit, we recover Santos’s angular operators and radial equation for perturbations with mψ = 0 and even parity under ψ → −ψ. These results provide a framework for studying quasinormal modes and gravitational stability of five-dimensional rotating black holes with two independent spins.
- Note: "two independent spins" holds (l.11-12, l.27). But "after the singly spinning case": the abstract says the earlier separation (Santos) is "for perturbations with mψ = 0 and even parity under ψ → −ψ" (l.24-25), one symmetry sector; v2 of 19 Nov says the same in its introduction: singly spinning MP "were separated for modes preserving the transverse-sphere symmetry" (v2 p.1). Fix: "after a symmetry sector of the singly spinning case". Santos (arXiv:2610.18956) is S43's [12] and is not in v0.8's references.

## K30 S42 [19], tex l.146 (sec:intro), anchor pp.~3, 7: **OK** (COMPARED)

- Lines read: S42 l.163-164, 446-447
- Passage: S42: case to a and b and also renormalize G such that µ = 2m. The theorem is as of writing still condition on the assumption of real mode stability for the wave equation. [...] this is exactly the content of [CPWZ22], however it has not been shown to hold yet down to the real axis Im σ = 0. For the purposes of this paper we will take the latter as a mild conditional assumption,
- Check: "has not been shown to hold yet": verbatim
- Note: As BHM-189 C15: quote verbatim.

## K31 S37 [20], tex l.154 (sec:intro), anchor abstract: **OK** (COMPARED)

- Lines read: S37 l.8-15
- Passage: S37: Abstract. We prove that subextremal Kerrde Sitter black holes are nonlinearly stable as solutions of the Einstein vacuum equations with positive cosmological constant, in the full subextremal range. Hintz, Petersen and Vasy reduced this to mode stability of the ungauged linearized Einstein equation; we prove that statement. The main step is mode stability of the Teukolsky equations of spin ±2: there are no nontrivial outgoing modes with Im σ ≥ 0. From it we deduce that every generalized mode of the linearized Einstein equation with Im σ ≥ 0 is pure gauge, up to a linearized Kerrde Sitter metric when σ = 0. Part of the proof is computer-assisted.
- Note: As BHM-189 C16, with its fix taken ("in the full subextremal range"); the source says "no nontrivial outgoing modes with Im σ ≥ 0" (l.12) and "Part of the proof is computer-assisted" (l.14-15).

## K32 S37 [20], tex l.155 (sec:intro), anchor p.~3: **OK** (COMPARED)

- Lines read: S37 l.126-128
- Passage: S37: Computer assistance. The computer-assisted steps are listed in Appendix A. All are exact except C9, which uses oating-point arithmetic with rigorous error bounds. The code is available on request.
- Note: As BHM-189 C17.

## K33 S37 [20], tex l.157 (sec:intro), anchor p.~21: **OK** (COMPARED)

- Lines read: S37 l.1338
- Passage: S37: them. No human expert has yet checked the argument. I have reviewed and edited the content
- Check: "No human expert has yet checked the argument": verbatim
- Note: As BHM-189 C18: quote verbatim.

## K34 S39 [21], tex l.159 (sec:intro), anchor pp.~3, 23: **OK** (COMPARED)

- Lines read: S39 l.138-141, 1844-1848
- Passage: S39: these families; it is not a damping threshold or a claim to ex- 2(s + 1) dRℓm 2 + + ω + haust all Riemann sheets. A certified contour establishes ex- dr2 r − M dr r−M actly one simple DM in the stated (3, 3) domain, while critical 7M 2 ω 2 − s Aℓm (M ω) M (4M ω − 2is)(2M ω − m) [...] ρi centered at ωi , approximate the connection by a degree-Ji with angular isolation and the absence of normalization poles, polynomial Pi in the scaled frequency, with coefficients ci,q : this proves that D33 contains exactly the one simple QNM shown in Fig. 10a. The statement applies to this domain, an- Ji  q X ω − ωi gular branch, and Riemann sheet.
- Note: As BHM-189 C19, with its fix taken: domain, angular branch and Riemann sheet (l.1846-1848).

## K35 S38 [22], tex l.161 (sec:intro), anchor abstract: **OK** (COMPARED)

- Lines read: S38 l.19-33
- Passage: S38: Abstract: Static, asymptotically flat, non-Schwarzschild black holes in four-dimensional Einstein–Weyl gravity have previously been constructed by numerical shooting, while the local field equations admit horizon and asymptotic expansions to all orders. We give a computer assisted existence proof for a non-Schwarzschild solution whose dimensionless horizon radius is one in units of the massive spin-two scale, with parameters close to the previously reported numerical branch. The exterior is divided into a convergent horizon series domain, a compact core enclosed by a parameter dependent Taylor model with directed rounding, and an infinite asymptotic domain treated as a centered stable manifold fixed point problem. The resulting five-dimensional matching map between the core and tail is continuous on a rigorously specified box. After exact rational preconditioning, the signs on opposite faces satisfy the hypotheses of the Poincaré–Miranda theorem and therefore certify a matching zero. The solution has a regular nondegenerate horizon, no additional exterior horizon, vanishing Ricci scalar, and nonvanishing Ricci tensor. The strict bounds also imply existence at every sufficiently nearby horizon radius and a local continuous family at fixed coupling. The proof establishes existence, but not uniqueness of the matching zero.
- Note: As BHM-189 C20.

## K36 S58 [23], tex l.163 (sec:intro), anchor abstract: **OK** (COMPARED)

- Lines read: S58 l.8-22
- Passage: S58: Abstract. We consider the subextremal Reissner–Nordström–de Sitter black hole whose horizons are at r− = 19/20, r+ = 1 and rc = 2, with cosmological constant Λ = 1200/4301. We prove that every nonzero quasinormal mode of the massless scalar wave equation on its exterior, for every angular momentum ℓ, satisfies Im ω < − 35 κ− , where κ− is the surface gravity of the Cauchy horizon. The frequency ω = 0 occurs only for ℓ = 0, with a constant mode, and is a simple zero. By a theorem of Hintz and Vasy, solutions with smooth initial 1 data then extend across the Cauchy horizon in Hloc and are continuous up to it, so the Christodoulou formulation of strong cosmic censorship fails for this linear model at this parameter point. Bounded frequencies and low angular momenta are handled by interval- arithmetic certificates for the radial Wronskian. All remaining frequencies are excluded by a Hermite-type monotone quantity integrated along complex contours in the tortoise coordinate. This quantity gives certificates that hold uniformly in ℓ ≥ 10, so the infinitely many angular momenta are covered by finitely many interval computations. The certificates and the programs that check them are in the supplement.
- Note: As BHM-189 C21.

## K37 S59 [24], tex l.164 (sec:intro), anchor abstract: **OK** (COMPARED)

- Lines read: S59 l.8-22
- Passage: S59: Abstract. We prove that the singly spinning Myers–Perry black hole in seven spacetime dimensions with rotation parameter a/r+ = 8 is linearly unstable in the sense of Prabhu and Wald. We construct smooth, compactly supported, constraint-satisfying initial data that are invariant under U (1) × SO(4) and odd under the (t-ϕ) reflection. For their gauge-fixed repre- sentative P ′ we establish that the potential energy of KP ′ , the initial time derivative of the corresponding solution, is negative. Positivity of the kinetic energy makes the Rayleigh–Ritz quotient ω 2 of Prabhu and Wald negative, and their variational principle gives exponential growth of the kinetic energy of the time derivative of the solution. We identify this potential energy with the local canonical energy of the evolved compactly supported data, by an ar- gument that uses only identities from the Prabhu–Wald framework. The trial is explicit; the negativity is established by a computer-assisted certificate: a rigorous adaptive quadrature in which the integrand is bounded on complex polydiscs by bivariate Taylor models with inter- val remainders. The certified value is a small residue of large contributions of both signs, and its sign relies on the exactness of the symbolic derivation; we state this dependence explicitly. The certificate, its records and the programs that check them are in the supplement.
- Note: As BHM-189 C22.

## K38 S57 [25], tex l.168 (sec:intro), anchor abstract: **OK** (COMPARED)

- Lines read: S57 l.9-18
- Passage: S57: Abstract: About twenty years ago, Choptuik studied numerically the gravi- tational collapse (Einstein field equations) of a massless scalar field in spheri- cal symmetry, and found strong evidence for a universal, self-similar solution at the threshold of black hole formation. We prove rigorously the existence of a real analytic solution, that we interpret as the solution observed by Chop- tuik. Our construction covers an open neighborhood of the past light cone of the singularity. The proof is computer assisted. Starting from an explicit ap- proximate solution, we show that nearby there is a true solution. The source code and a high precision data file (about 80 significant decimal digits, with rigorous error bounds) are included. We do not study perturbations.
- Note: As BHM-189 C23.

## K39 S56 [26], tex l.170 (sec:intro), anchor abstract and p.~2: **OK** (COMPARED)

- Lines read: S56 l.6-7, 96-103
- Passage: S56: Abstract. We study the fundamental self-similar solution to the SU(2) sigma model, found by Shatah and Turok-Spergel. We give a rigorous proof for its mode stability. Based on earlier results by the second [...] 1 2 , |Imλ| ≤ 380} is then studied by a new approach which is in some sense “brute force”. This means that we work with suitable approximations to solutions of the equation, e.g. truncated Chebyshev expansions, and a rigorous version of a method used by Bizoń [1] which relates the existence of eigenvalues to the convergence of a certain continued fraction. We provide rigorous error estimates for all our approximations. Furthermore, we emphasize that all computations are free of rounding errors since we work exclusively with rational numbers. As a consequence, our result is completely rigorous although we have to admit that it seems unrealistic to perform all our computations without the aid of some computer algebra system.
- Note: As BHM-189 C24, with its fix taken (abstract and p.2). "with computer algebra": all computations in rational numbers, "without the aid of some computer algebra system" unrealistic (l.101-103).

## K40 S44 [27], tex l.170 (sec:intro), anchor abstract: **OK** (COMPARED)

- Lines read: S44 l.16-21
- Passage: S44: One of the key challenges is the proof of mode-stability for the non self-adjoint spectral prob- lem which arises when linearising the dynamics around the Larson-Penston collapsing solution. To exclude the presence of complex growing modes other than the trivial one associated with time trans- lation symmetry, we use a high-order energy method in low and high frequency regimes, for which the monotonicity properties are crucially exploited, and use rigorous computer-assisted techniques in the intermediate regime. In addition, the maximal dissipativity of the linearised operator is proven on
- Note: As BHM-189 C25.

## K41 S46 [28], tex l.171 (sec:intro), anchor abstract: **OK** (COMPARED)

- Lines read: S46 l.14-19
- Passage: S46: We give a rigorous, constructive proof that there exists a Ricci-flat Kähler metric on the Fermat quartic hypersurface, independently of Yau’s famous theorem, along with an explicit and accurate analytic approximation to the metric. The proof combines numerical techniques to obtain the approximately Ricci flat metric, a fixed point theorem to prove existence, and verified numerics to get the bounds used by the fixed point theorem. The method is general and we discuss the computational issues in applying it to other manifolds.
- Note: As BHM-189 C26. v0.8 now says "computer-assisted proofs" (v0.4: "certified computation"): S46 is "a constructive computer-assisted existence proof" (title; l.14-19), so this holds.

## K42 S47 [29], tex l.172 (sec:intro), anchor p.~3: **SAYS MORE** (READ)

- Lines read: S47 l.98-108, 736-742, 840-844
- Passage: S47: However, a small sampled residual alone does not provide a rigorous bound on the continuous residual or on the error relative to an exact solution [3, 4]. Here we address continuous-residual certification by combining machine-learning- based discovery with rigorous numerical certification and formal verification. We demonstrate the approach for strongly nonlinear, high-amplitude water waves, where physics-informed neural networks discover candidate solutions with residuals approaching the limits of double-precision arithmetic. We then convert a selected candidate into a rigorous uniform residual certificate using interval arithmetic and formally verify the mathematical deductions underlying the certificate in Lean. The resulting pipeline provides a route from machine-learned numerical discovery to certified, machine-checkable scientific computation. [...] N = 150, ε= = 1.78 × 10−13 . (10) 1015 This is a uniform residual theorem for a supplied finite series. It is not an existence or uniqueness theorem for an exact nearby water wave. Such a result would additionally require a rigorous inverse bound for the appropriately constrained linearized Babenko operator and control of the nonlinear remainder [20]; these ingredients are not part of the present certificate. [...] A second distinction concerns numerical accuracy and mathematical existence. The certificate established here is a rigorous uniform bound on the residual of an explicit approximate solution. It shows that the reported near-machine-precision residual is not an artifact of floating-point roundoff, Fourier truncation, aliasing or finite sam- pling. It does not, by itself, prove the existence of an exact water-wave solution nearby.
- Note: v0.8 now says "Computer-assisted proofs are also in use ... with formal verification in Lean, for nonlinear water waves computed by neural networks" (v0.4: "certified computation"). S47 certifies a uniform bound on the residual of one machine-learned candidate (p.3, l.100-108), and says: "This is a uniform residual theorem for a supplied finite series. It is not an existence or uniqueness theorem for an exact nearby water wave" (l.738-739, p.12; also l.840-844, p.14). Fix: keep "proofs" for S46 only, e.g. "... in geometric analysis [28] and, with formal verification in Lean, to certify the residual of a neural-network approximation of a nonlinear water wave [29, p. 3]".

## K43 S33 [30], tex l.220 (sec:intro), anchor eq.~(4.14): **OK** (READ)

- Lines read: S33 l.395-399
- Passage: S33: M −ℓ p   2Bℓ (ℓ + 1) (2ℓ + 1)(ℓ − 1) −ℓ+1 Ψ2 = r 1− . (4.14) (ℓ − 1)r + 2M r
- Note: Read on the rendered page (PDF p.8, printed 7). Ψ2 = 2Bℓ(ℓ+1)√((2ℓ+1)(ℓ−1)) r^(1−ℓ)(1 − M/r)^(−ℓ)/((ℓ−1)r + 2M). With r_H = M at q = 1, v0.8's D = 4 form of u_0 equals Ψ2 times a constant, and Ψ2 ~ r^(−ℓ) decays (tools/zm_check.py). Ψ2 solves Kodama–Ishibashi's −f(fΨ′)′ + V_S−Ψ = 0 exactly at D = 4, q = 1. Note: S33's own printed V2 (eq. 4.18) is the negative of that potential (it would tend to −ℓ(ℓ+1)/r² at large r): a sign slip in S33's (4.18), not in v0.8, which cites only (4.14).

## K44 S5 [1], tex l.222 (sec:intro), anchor Table~I: **OK** (READ)

- Lines read: S5 l.1903-1907
- Passage: S5: Tensor Vector Scalar Q = 0 Q 6= 0 Q = 0 Q 6= 0 Q=0 Q 6= 0 d = 4, 5 OK K=1 λ=0 OK OK OK OK OK d≥6?
- Note: As K04.

## K45 S28 [4], tex l.223 (sec:intro), anchor Table~1: **OK** (COMPARED)

- Lines read: S28 l.740-745
- Passage: S28: Table 1: Stability of static black holes. Tensor Vector Scalar Q = 0 Q 6= 0 Q = 0 Q 6= 0 Q = 0 Q 6= 0 D = 4, 5 OK K = 1 λ =0 OK OK OK OK OK D ≥ 6 ?
- Note: As BHM-189 C01.

## K46 S48 [5], tex l.223 (sec:intro), anchor p.~40: **OK** (COMPARED)

- Lines read: S48 l.2273-2276
- Passage: S48: Our results are summarized in Table I. As shown there, maximally symmetric black holes are stable with respect to tensor and vector perturbations over the entire parameter range. In contrast, for scalar type perturbation, we were not able to prove even the stability of asymptotically flat black holes with charge in generic dimensions,
- Note: As BHM-189 C02.

## K47 S37 [20], tex l.226 (sec:intro), anchor (none): **OK** (COMPARED)

- Lines read: S37 l.8-15
- Passage: S37: Abstract. We prove that subextremal Kerrde Sitter black holes are nonlinearly stable as solutions of the Einstein vacuum equations with positive cosmological constant, in the full subextremal range. Hintz, Petersen and Vasy reduced this to mode stability of the ungauged linearized Einstein equation; we prove that statement. The main step is mode stability of the Teukolsky equations of spin ±2: there are no nontrivial outgoing modes with Im σ ≥ 0. From it we deduce that every generalized mode of the linearized Einstein equation with Im σ ≥ 0 is pure gauge, up to a linearized Kerrde Sitter metric when σ = 0. Part of the proof is computer-assisted.
- Note: As BHM-189 C28.

## K48 S5 [1], tex l.232 (sec:setting), anchor (none): **OK** (READ)

- Lines read: S5 l.248-255
- Passage: S5: When ∇r 6= 0, these equations give the black hole type solution dr 2 ds2 = −f (r)dt2 + + r 2 dσn2 , (2.18) f (r) with 2M Q2 f (r) = K − λr 2 − + . (2.19) r n−1 r 2n−2
- Note: The background (2.18)-(2.19), p.5.

## K49 S5 [1], tex l.235 (sec:setting), anchor eqs.~(2.12), (2.14): **OK** (READ)

- Lines read: S5 l.207, 219-221
- Passage: S5: Rµν = Λgµν + κ Tµν − T gµν , (2.12) [...] 2Λ κ2 q 2 λ := , Q2 := . (2.14) n(n + 1) n(n − 1)
- Note: (2.12) is the Einstein equation with Λ; (2.14) defines λ := 2Λ/(n(n + 1)) (p.4).

## K50 S5 [1], tex l.236 (sec:setting), anchor p.~3: **OK** (READ)

- Lines read: S5 l.119, 125-131
- Passage: S5: Here, dσn2 = γij (z)dz i dz j is the metric of the n-dimensional Einstein space Kn with [...] of its horizon. In the case in which Kn is a constant curvature space, K denotes its sectional curvature, while in a generic case, K is just a constant representing a local average of the sectional curvature. Because an Einstein space of dimension smaller than four always has a constant curvature and is maximally symmetric, this difference arises only for n ≥ 4, or, equivalently, when the spacetime dimension d = n + 2 is greater than or equal to 6. In the present paper, we assume that Kn is complete with respect to the Einstein metric, and we normalise K so that K = 0, ±1.
- Note: K is the sectional curvature of the horizon's Einstein space Kn, normalised to 0, ±1 (l.125-131, p.3).

## K51 S5 [1], tex l.238 (sec:setting), anchor eq.~(2.18): **OK** (READ)

- Lines read: S5 l.248-251
- Passage: S5: When ∇r 6= 0, these equations give the black hole type solution dr 2 ds2 = −f (r)dt2 + + r 2 dσn2 , (2.18) f (r)
- Note: (2.18), p.5. In S5, dσn² is the metric of an Einstein space Kn (l.119); for K = 1 and the maximally symmetric case it is the round S^n, as v0.8 says.

## K52 S5 [1], tex l.239 (sec:setting), anchor eq.~(2.19): **OK** (READ)

- Lines read: S5 l.253-255
- Passage: S5: 2M Q2 f (r) = K − λr 2 − + . (2.19) r n−1 r 2n−2
- Note: (2.19) as written, p.5.

## K53 S5 [1], tex l.240 (sec:setting), anchor (none): **OK** (READ)

- Lines read: S5 l.253-255
- Passage: S5: 2M Q2 f (r) = K − λr 2 − + . (2.19) r n−1 r 2n−2
- Note: M and Q are (2.19)'s parameters. |Q| = M as extremality at λ = 0, K = 1 follows from (2.19) (a double root of f).

## K54 S5 [1], tex l.249 (sec:setting), anchor eq.~(5.39): **OK** (READ)

- Lines read: S5 l.1205
- Passage: S5: m = k2 − nK, (5.39)
- Note: m = k² − nK (5.39), p.21; at K = 1 and k² = ℓ(ℓ + n − 1), m = (ℓ − 1)(ℓ + n).

## K55 S5 [1], tex l.250 (sec:setting), anchor eqs.~(5.58), (5.60): **OK** (READ)

- Lines read: S5 l.1402-1406, 1412-1414
- Passage: S5: where µ is a positive constant satisfying 4mQ2 µ2 = M 2 + . (5.58) (n + 1)2 [...] Here, if we define the parameter δ by µ = (1 + 2mδ)M, (5.60)
- Note: (5.58) µ² = M² + 4mQ²/(n + 1)² and (5.60) µ = (1 + 2mδ)M, µ > 0 (p.24); so (1 + 2mδ)² = 1 + 4mq²/(n + 1)² and δ ≥ 0.

## K56 S5 [1], tex l.251 (sec:setting), anchor eq.~(5.62b): **OK** (READ)

- Lines read: S5 l.1426-1428
- Passage: S5: n(n + 1) H− = m + (1 + mδ)x, (5.62b) 2
- Note: (5.62b) as written, p.25.

## K57 S5 [1], tex l.251 (sec:setting), anchor eq.~(5.63b): **OK** (READ)

- Lines read: S5 l.1445-1462
- Passage: S5: U− = −4n3 (n + 2)(n + 1)2 (1 + mδ)2 x2 + 48n2 (n + 1)(n − 2)m(1 + mδ)x  −16(n − 2)(n − 4)m2 y − n3 (3n − 2)(n + 1)4 δ(1 + mδ)3 x4  −4n2 (n + 1)2 (1 + mδ)2 (n + 1)(3n − 2)mδ − n2 x3  +4(n + 1)(1 + mδ) m(n − 2)(n − 4)(n + 1)(m + n2 K)δ  +4n(2n2 − 3n + 4)m + n2 (n − 2)(n − 4)(n + 1)K x2 −16m (n + 1)m −4m + 3n2 (n − 2)K δ   +3n(n − 4)m + 3n2 (n + 1)(n − 2)K x +64m3 + 16n(n + 2)m2 K. (5.63b)
- Note: (5.63b), p.25, read on the rendered page: the first two lines form [ ... ] y, which vanishes at λ = 0 (y = λr²); the rest, at K = 1, is Appendix A's display term by term (K81).

## K58 S6 [3], tex l.265 (sec:setting), anchor pp.~5, 13: **OK** (READ)

- Lines read: S6 l.226-239, 644-645
- Passage: S6: positive self-adjoint operator. However, because V is bounded from below in most cases, in the domain C0∞ (r∗ )—the set of smooth functions with compact support in r∗ —A is a symmetric, semi-bounded operator and hence can be extended to a semi- bounded self-adjoint operator in such a way that the lower bound of the spectrum of the extension is the same as that of A. In fact, a natural extension, called the Friedrichs extension,30) is such a self-adjoint operator. Furthermore, when λ ≥ 0, there is a unique self-adjoint extension because in this case, the Schwarzschild wedge is globally hyperbolic, and the range of r∗ is complete, i.e., (−∞, ∞). Therefore the time evolution of Φ—which is defined by a self-adjoint extension of A—must be uniquely determined by its initial data, by virtue of this global hyperbolicity. (If there were different self-adjoint extensions, then each of them would describe a different time evolution of Φ from the same initial data.) Therefore, if the symmetric operator A with domain C0∞ (r∗ ) is shown to be positive definite, then the self-adjoint extension must also be positive definite. We show that this is indeed the case. [...] Clearly Ṽ > 0, and thus A with domain C0∞ (r∗ ) is strictly positive, so is the self- adjoint extension. The higher-dimensional Schwarzschild black holes are therefore
- Note: S6: on C0∞(r*), A is symmetric and semi-bounded; for λ ≥ 0 the self-adjoint extension is unique, so positivity on C0∞ gives positivity of the extension (l.226-239, p.5; used at l.644-645, p.13). That is the direction v0.8 uses. The H² domain and "if and only if" are standard facts, not stated in S6.

## K59 S6 [3], tex l.272 (sec:setting), anchor pp.~4--5: **OK** (READ)

- Lines read: S6 l.205-209, 217-219
- Passage: S6: A=− +V (2.5) dr∗2 is a positive self-adjoint operator in L2 (r∗ , dr∗ ), the Hilbert space of square integrable functions of r∗ , so that Eq. (2.4) possesses no negative mode solutions that are [...] normalisable. In other words, the positivity of the self-adjoint operator ensures that, given well-behaved initial data—for instance, smooth data of compact support in r∗ —Φ remains bounded for all time. A rigorous proof of the stability of the system
- Note: A positive self-adjoint ⇒ "no negative mode solutions that are normalisable" (l.208-209, 217; pp.4-5).

## K60 S5 [1], tex l.277 (sec:setting), anchor (none): **OK** (READ)

- Lines read: S5 l.1838, 1903-1907
- Passage: S5: Since this is positive definite, the electromagnetic mode Φ+ is always stable for any [...] Tensor Vector Scalar Q = 0 Q 6= 0 Q = 0 Q 6= 0 Q=0 Q 6= 0 d = 4, 5 OK K=1 λ=0 OK OK OK OK OK d≥6?
- Note: Table I: tensor and vector OK at K = 1, λ = 0, Q ≠ 0 (p.33); "the electromagnetic mode Φ+ is always stable" (l.1838, p.31).

## K61 S5 [1], tex l.279 (sec:setting), anchor p.~15: **OK** (READ)

- Lines read: S5 l.818-822
- Passage: S5: of △ˆ is completely discrete, each eigenvalue has a finite multiplicity, and the lowest eigenvalue is k2 =0, whose eigenfunction is a constant. A perturbation corresponding to such a constant mode represents a variation of the parameters λ, M , and Q of the background, as seen from the argument in §2.1. For this reason, we do not consider the modes with k2 = 0, although there may be a non-trivial eigenfunction with
- Note: "A perturbation corresponding to such a constant mode represents a variation of the parameters λ, M, and Q of the background" (l.819-821, p.15): k² = 0 is ℓ = 0.

## K62 S5 [1], tex l.280 (sec:setting), anchor p.~42: **OK** (READ)

- Lines read: S5 l.2509, 2518-2523
- Passage: S5: For k2 = n and K = 1, µ = M and Φ± are written [...] From this, we find that Φ+ is gauge-invariant. In contrast, as is seen from the relation √ Φ− n δ Φ= + Φ+ , (D.11) 2(n + 1)M (n + 1)M Φ− is not gauge-invariant. Nevertheless, the master equation for Φ− is gauge-
- Note: For k² = n and K = 1 (ℓ = 1): "Φ+ is gauge-invariant. In contrast ... Φ− is not gauge-invariant" (l.2518-2523, p.42). The source adds that the master equation for Φ− is gauge-invariant.

## K63 S33 [30], tex l.321 (sec:results), anchor eq.~(4.14): **OK** (READ)

- Lines read: S33 l.395-399
- Passage: S33: M −ℓ p   2Bℓ (ℓ + 1) (2ℓ + 1)(ℓ − 1) −ℓ+1 Ψ2 = r 1− . (4.14) (ℓ − 1)r + 2M r
- Note: As K43.

## K64 S6 [3], tex l.331 (sec:sdef), anchor eqs.~(2.18)--(2.20): **OK** (READ)

- Lines read: S6 l.478-492
- Passage: S6: Now, to show the positivity of A, let us introduce the differential operator d D̃ ≡ +S, (2.18) dr∗ with S being some function of r. Then, we have h i Z   ∗ (Φ, AΦ)L2 = − Φ D̃Φ + dr∗ |D̃Φ|2 + Ṽ |Φ|2 , (2.19) boundary where dS Ṽ ≡ V + f − S2 . (2.20) dr For Φ ∈ C0∞ (r∗ ), the boundary term vanishes. Inspecting the form of (2.17), we find
- Note: (2.18)-(2.20), p.10: (Φ, AΦ) = −[Φ* D̃Φ]boundary + ∫(|D̃Φ|² + Ṽ|Φ|²) with D̃ = d/dr* + S and Ṽ = V + f dS/dr − S²; the boundary term vanishes on C0∞. Lemma 1 is this identity (f dS/dr = dS/dr*).

## K65 S6 [3], tex l.672 (sec:verification), anchor (none): **OK** (READ)

- Lines read: S6 l.620-627, 644-647
- Passage: S6: Fig. 7. The potential barriers VS surrounding (n + 2)-dimensional Schwarzschild black holes for scalar perturbations of the mode l = 2. The horizontal axis is normalised with respect to the black hole horizon radius rh . In 8-dimensional spacetimes, VS is not positive definite. the potential VS is not positive definite in general, as shown in Fig. 7. (For further reference, we also plot the potential VS for the Schwarzschild-de Sitter case in Fig. 8 and the Schwarzschild-anti-de Sitter case in Fig. 9.) [...] Clearly Ṽ > 0, and thus A with domain C0∞ (r∗ ) is strictly positive, so is the self- adjoint extension. The higher-dimensional Schwarzschild black holes are therefore stable with respect to scalar perturbations. This completes the stability analysis for higher-dimensional Schwarzschild black holes.
- Note: Stable at every n (l.644-647). The negative region at D = 10 is v0.8's own statement; S6 notes VS is not positive definite in general (l.622, l.625).

## K66 S5 [1], tex l.708 (sec:verification), anchor (none): **OK** (READ)

- Note: Names the source of a transcription; no claim about S5's content.

## K67 S5 [1], tex l.738 (sec:discussion), anchor (none): **OK** (READ)

- Note: Refers back to §2's use of S5 (K60).

## K68 S52 [9], tex l.744 (sec:discussion), anchor pp.~43--44: **OK** (COMPARED)

- Lines read: S52 l.2466-2479
- Passage: S52: large D and has independently obtained the result (5.22). 37 2i Had the mode with ωr0 = 1+Q 2 been physical, it would have represented an instability, con- 0 tradicting the well known stability of Reissner Nordstrom black holes (atleast of sufficiently small charge) in arbitrary dimensions. – 43 – As we have mentioned above, (5.22) is correct as stated for l ≥ 2. It is easily verified 38 that all quasinormal modes with l ≥ 2 have negative imaginary components (and so represent decaying fluctuations).
- Note: As BHM-189 C29, with its fix taken; as K18.

## K69 S51 [10], tex l.745 (sec:discussion), anchor p.~6: **OK** (COMPARED)

- Lines read: S51 l.324-330
- Passage: S51: S n+1 . As boundary condition we demanded Fm (z) ∝ (cos z)ℓ at z = π/2 5 . The modes with ℓ > 1 (ℓ > 0) describe dynamical perturbation of gravitational perturbations (gauge field perturbations). So we consider the gravitational perturbations with ℓ > 1 and gauge field perturbations with ℓ > 0. At the zero cosmological constant limit L → ∞, these results reproduce the quasinormal modes of Reissner-Nordstrom black hole obtained in [12]. At Q = 0, ω± reduces to quasinormal modes of scalar type perturbation of (Anti) de Sitter Schwarzschild black hole [15]. At the both limits, the perturbations are stable. On the other
- Note: As BHM-189 C30, with its fix taken; as K19.

## K70 S14 [6], tex l.749 (sec:discussion), anchor (none): **OK** (READ)

- Lines read: S14 l.8-12
- Passage: S14: We have shown that higher dimensional Reissner-Nordström-de Sitter black holes are gravitation- ally unstable for large values of the electric charge and cosmological constant in D ≥ 7 space-time dimensions. We have found the shape of the slightly perturbed black hole at the threshold point of instability. Why only D = 4, 5 and 6 dimensional worlds are favorable as to the black stability remains unknown.
- Note: "gravitationally unstable for large values of the electric charge and cosmological constant in D ≥ 7" (abstract).

## K71 S51 [10], tex l.751 (sec:discussion), anchor abstract: **OK** (COMPARED)

- Lines read: S51 l.26-30
- Passage: S51: We study the large D effective theory for D dimensional charged (Anti) de Sitter black holes. Then we show that the de Sitter Reissner-Nordstrom black hole becomes unstable against gravitational perturbations at larger charge than a critical charge in a higher dimension. Furthermore we find that there is a non-trivial zero-mode static perturbation at the critical charge. The existence of static perturbations suggests the appearance of non-spherical sym-
- Note: As BHM-189 C31.

## K72 S45 [31], tex l.753 (sec:discussion), anchor abstract: **OK** (COMPARED)

- Lines read: S45 l.18-27
- Passage: S45: In this work, we investigate the correspondence between quasinormal modes (QNMs) and greybody factors (GBFs) in higher-dimensional Reissner–Nordstöm–de Sitter black holes based on the massless scalar field. Our analysis focuses on the QNMs in the near-ultracold family where the inner, outer, and cosmological horizons are close together. Under the geometric limit condition, the leading-order Wentzel–Kramers–Brillouin term of the QNM is dominant for fixed angular quantum numbers and dimensionality without imposing the eikonal limit. Particularly, the corresponding GBFs also retain the explicit form of both parameters. Furthermore, we demonstrate that the half-transmission frequency of the GBF and its derivative are related to null geodesics, in terms of aspects such as the angular frequency and Lyapunov exponent, with the use of both parameters. We provide their relationships in arbitrary dimensionality. Furthermore, the higher-order corrections to the QNMs are investigated at the Nariai limit and in the near-ultracold geometry with separated horizons.
- Note: As BHM-189 C32.

## K73 S58 [23], tex l.753 (sec:discussion), anchor (none): **OK** (COMPARED)

- Lines read: S58 l.8-12, 16-17
- Passage: S58: Abstract. We consider the subextremal Reissner–Nordström–de Sitter black hole whose horizons are at r− = 19/20, r+ = 1 and rc = 2, with cosmological constant Λ = 1200/4301. We prove that every nonzero quasinormal mode of the massless scalar wave equation on its exterior, for every angular momentum ℓ, satisfies Im ω < − 35 κ− , where κ− is the surface gravity of the Cauchy horizon. The frequency ω = 0 occurs only for ℓ = 0, with a constant [...] Christodoulou formulation of strong cosmic censorship fails for this linear model at this parameter point. Bounded frequencies and low angular momenta are handled by interval-
- Note: As BHM-189 C33.

## K74 S54 [32], tex l.759 (sec:discussion), anchor abstract: **OK** (COMPARED)

- Lines read: S54 l.8-18, 23-24
- Passage: S54: Abstract. We present a new framework for characterizing quasinormal modes (QNMs) or resonant states for the wave equation on asymptotically flat spacetimes, applied to the setting of extremal Reissner–Nordström black holes. We show that QNMs can be interpreted as honest eigenfunctions of generators of time translations acting on Hilbert spaces of initial data, corresponding to a suitable time slicing. The main difficulty that is present in the asymptotically flat setting, but is absent in the previously studied asymptotically de Sitter or anti de Sitter sub-extremal black hole spacetimes, is that L2 -based Sobolev spaces are not suitable Hilbert space choices. Instead, we consider Hilbert spaces of functions that are additionally Gevrey regular at infinity and at the event horizon. We introduce L2 -based Gevrey estimates for the wave equation that are intimately connected to the existence of conserved quantities along null infinity and the event horizon. We relate this new framework to the arXiv:1910.08479v2 [gr-qc] 7 Jun 2021 [...] traditional interpretation of quasinormal frequencies as poles of the meromorphic continuation of a resolvent operator and obtain new quantitative results in this setting.
- Note: As BHM-189 C34.

## K75 S55 [33], tex l.761 (sec:discussion), anchor abstract: **OK** (COMPARED)

- Lines read: S55 l.15-26
- Passage: S55: We prove that there are no exponentially growing modes nor modes on the real axis for the Teukolsky equation on Kerr black hole spacetimes, both in the extremal and subextremal case. We also give a quantitative refinement of mode stability. As an immediate application, we show that the transmission and reflection coefficients of the scattering problem are bounded, independently of the specific angular momentum of the black hole, in any compact set of real frequencies excluding zero frequency and the superradiant threshold. While in the subextremal setting these results were known previously, the extremal case is more involved and has remained an open problem. Ours are the first results outside axisymmetry and could serve as a preliminary step towards understanding boundedness, scattering and decay properties of general solutions to the Teukolsky equation on extremal Kerr black holes.
- Note: As BHM-189 C35.

## K76 S31 [34], tex l.762 (sec:discussion), anchor (none): **OK** (READ)

- Lines read: S31 l.22-29
- Passage: S31: Abstract: We investigate how the Aretakis instability affects non-dilatonic extremal black p-branes by focusing on their near-horizon geometry. Crucially, the strength of the instability, i.e. the number of transverse derivatives needed to see non-decay/blow-up of fields on the horizon at late null time, is given by the scaling dimensions with respect to the near-horizon AdSp+2 -factor. This renders the problem of determining the severity of the Aretakis instability equivalent to computing the Kaluza– Klein spectrum of fields on Freund–Rubin spaces. We use this to argue that non-dilatonic extremal black branes suffer from the Aretakis instability even in the absence of additional fields — we find that this is weaker than for extremal black holes. We also argue that the scaling dimensions determine the
- Note: The Aretakis instability of non-dilatonic extremal black p-branes, via the near-horizon geometry (abstract). No anchor in v0.8; suggested: abstract.

## K77 S43 [18], tex l.768 (sec:discussion), anchor (none): **SAYS MORE** (READ)

- Lines read: S43 l.22-27
- Passage: S43: of each separated solution share a single radial amplitude. We prove completeness of the angular harmonics at real frequencies and show that the resulting physical perturbations admit local metric reconstruction. In the singly spinning limit, we recover Santos’s angular operators and radial equation for perturbations with mψ = 0 and even parity under ψ → −ψ. These results provide a framework for studying quasinormal modes and gravitational stability of five-dimensional rotating black holes with two independent spins.
- Note: As K29 (the same sentence in §8).

## K78 S42 [19], tex l.769 (sec:discussion), anchor (none): **OK** (COMPARED)

- Lines read: S42 l.163-164, 446-447
- Passage: S42: case to a and b and also renormalize G such that µ = 2m. The theorem is as of writing still condition on the assumption of real mode stability for the wave equation. [...] this is exactly the content of [CPWZ22], however it has not been shown to hold yet down to the real axis Im σ = 0. For the purposes of this paper we will take the latter as a mild conditional assumption,
- Note: As BHM-189 C37.

## K79 S59 [24], tex l.771 (sec:discussion), anchor (none): **OK** (COMPARED)

- Lines read: S59 l.8-10, 17-20
- Passage: S59: Abstract. We prove that the singly spinning Myers–Perry black hole in seven spacetime dimensions with rotation parameter a/r+ = 8 is linearly unstable in the sense of Prabhu and Wald. We construct smooth, compactly supported, constraint-satisfying initial data that are [...] gument that uses only identities from the Prabhu–Wald framework. The trial is explicit; the negativity is established by a computer-assisted certificate: a rigorous adaptive quadrature in which the integrand is bounded on complex polydiscs by bivariate Taylor models with inter- val remainders. The certified value is a small residue of large contributions of both signs, and
- Note: As BHM-189 C38.

## K80 S5 [1], tex l.773 (sec:discussion), anchor (none): **OK** (READ)

- Lines read: S5 l.1407-1419
- Passage: S5: The reduced master equations have the canonical forms f (f Φ′± )′ + ω 2 − VS± Φ± = SS± . (5.59)  Here, if we define the parameter δ by µ = (1 + 2mδ)M, (5.60) the effective potentials VS± are expressed as f U± VS± = 2 , (5.61) 64r 2 H±
- Note: (5.59)-(5.61): f(fΦ′±)′ + (ω² − VS±)Φ± = SS±, with VS± = fU±/(64r²H±²) real (pp.24-25).

## K81 S5 [1], tex l.830 (app:U), anchor eq.~(5.63b): **OK** (READ)

- Lines read: S5 l.1445-1462
- Passage: S5: U− = −4n3 (n + 2)(n + 1)2 (1 + mδ)2 x2 + 48n2 (n + 1)(n − 2)m(1 + mδ)x  −16(n − 2)(n − 4)m2 y − n3 (3n − 2)(n + 1)4 δ(1 + mδ)3 x4  −4n2 (n + 1)2 (1 + mδ)2 (n + 1)(3n − 2)mδ − n2 x3  +4(n + 1)(1 + mδ) m(n − 2)(n − 4)(n + 1)(m + n2 K)δ  +4n(2n2 − 3n + 4)m + n2 (n − 2)(n − 4)(n + 1)K x2 −16m (n + 1)m −4m + 3n2 (n − 2)K δ   +3n(n − 4)m + 3n2 (n + 1)(n − 2)K x +64m3 + 16n(n + 2)m2 K. (5.63b)
- Note: Appendix A's U− equals (5.63b) at y = 0, K = 1, term by term, read on the rendered page (see K57).

## K82 S5 [1], tex l.840 (app:U), anchor eq.~(5.62b): **OK** (READ)

- Lines read: S5 l.1426-1428
- Passage: S5: n(n + 1) H− = m + (1 + mδ)x, (5.62b) 2
- Note: As K56.

## K83 S5 [1], tex l.841 (app:U), anchor (none): **OK** (READ)

- Note: About the code's transcription of S5; no claim about S5's content beyond K81.

## R01 S5 [1], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "Master equations for perturbations of generalised static black holes with charge in higher dimensions"; Hideo Kodama; Akihiro Ishibashi
- Check: record: title match yes, authors match yes; cited v4, latest v4
- Note: Authors, title and identifier match the record; the cited version is the latest. Journal version: Prog.Theor.Phys.111:29-73,2004.

## R02 S23 [2], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "A master equation for gravitational perturbations of maximally symmetric black holes in higher dimensions"; Hideo Kodama; Akihiro Ishibashi
- Check: record: title match yes, authors match yes; cited v3, latest v3
- Note: Authors, title and identifier match the record; the cited version is the latest. Journal version: Prog.Theor.Phys. 110 (2003) 701-722.

## R03 S6 [3], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "Stability of Higher-Dimensional Schwarzschild Black Holes"; Akihiro Ishibashi; Hideo Kodama
- Check: record: title match yes, authors match yes; cited v3, latest v3
- Note: Authors, title and identifier match the record; the cited version is the latest. Journal version: Prog.Theor.Phys. 110 (2003) 901-919.

## R04 S28 [4], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "Stability of Generalised Static Black Holes in Higher Dimensions"; Hideo Kodama; Akihiro Ishibashi
- Check: record: title match yes, authors match yes; cited v1, latest v1
- Note: Authors, title and identifier match the record; the cited version is the latest.

## R05 S48 [5], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "Perturbations and Stability of Static Black Holes in Higher Dimensions"; Akihiro Ishibashi; Hideo Kodama
- Check: record: title match yes, authors match yes; cited v2, latest v2
- Note: Authors, title and identifier match the record; the cited version is the latest.

## R06 S14 [6], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "Instability of higher dimensional charged black holes in the de-Sitter world"; R. A. Konoplya; A. Zhidenko
- Check: record: title match yes, authors match yes; cited v3, latest v3
- Note: Authors, title and identifier match the record; the cited version is the latest. Journal version: Phys.Rev.Lett.103:161101,2009.

## R07 S26 [7], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "Instability of D-dimensional extremally charged Reissner-Nordstrom(-de Sitter) black holes: Extrapolation to arbitrary D"; R. A. Konoplya; A. Zhidenko
- Check: record: title match yes, authors match yes; cited v3, latest v3
- Note: The original title spells "Reissner-Nordstrøm(-de Sitter)" (SOURCES.md too); v0.8 normalises to "Nordström". Journal version: Phys. Rev. D 89 (2014) 024011.

## R08 S32 [8], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "Grey-body factor from correspondence with quasinormal mode for gravitational perturbation of higher-dimensional Reissner-Nordström black hole"; Hyewon Han; Bogeun Gwak
- Check: record: title match yes, authors match yes; cited v2, latest v2
- Note: Authors, title and identifier match the record; the cited version is the latest.

## R09 S52 [9], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "A Charged Membrane Paradigm at Large D"; Sayantani Bhattacharyya; Mangesh Mandlik; Shiraz Minwalla; Somyadip Thakur
- Check: record: title match yes, authors match yes; cited v2, latest v2
- Note: Authors, title and identifier match the record; the cited version is the latest.

## R10 S51 [10], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "Instability of de Sitter Reissner-Nordstrom black hole in the 1/D expansion"; Kentaro Tanabe
- Check: record: title match yes, authors match yes; cited v2, latest v2
- Note: As BHM-189 R15: the original title has no umlaut ("Reissner-Nordstrom").

## R11 S9 [11], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "A simple test for stability of black hole by $S$-deformation"; Masashi Kimura
- Check: record: title match yes, authors match yes; cited v3, latest v3
- Note: Authors, title and identifier match the record; the cited version is the latest.

## R12 S27 [12], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "Robustness of the $S$-deformation method for black hole stability analysis"; Masashi Kimura; Takahiro Tanaka
- Check: record: title match yes, authors match yes; cited v3, latest v3
- Note: Authors, title and identifier match the record; the cited version is the latest.

## R13 S53 [13], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "Stability analysis of black holes by the $S$-deformation method for coupled systems"; Masashi Kimura; Takahiro Tanaka
- Check: record: title match yes, authors match yes; cited v3, latest v3
- Note: Authors, title and identifier match the record; the cited version is the latest.

## R14 S49 [14], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "The linear stability of Reissner-Nordström spacetime: the full subextremal range"; Elena Giorgi
- Check: record: title match NO, authors match yes; cited v2, latest v2
- Note: As BHM-189 R13: "|Q| < M" is on the paper's title page but not in arXiv's metadata title. Journal version: Commun. Math. Phys. 380, 1313-1360 (2020).

## R15 S50 [15], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "Linear Stability of Higher Dimensional Schwarzschild Spacetimes: Decay of Master Quantities"; Pei-Ken Hung; Jordan Keller; Mu-Tao Wang
- Check: record: title match yes, authors match yes; cited v1, latest v1
- Note: Authors, title and identifier match the record; the cited version is the latest.

## R16 S40 [16], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "Perturbations of Kerr-Newman black holes: separation and mode stability"; Peter Hintz
- Check: record: title match yes, authors match yes; cited v1, latest v1
- Note: Authors, title and identifier match the record; the cited version is the latest.

## R17 S41 [17], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "Nonlinear stability of subextremal Kerr black holes"; Peter Hintz
- Check: record: title match yes, authors match yes; cited v2, latest v2
- Note: Authors, title and identifier match the record; the cited version is the latest.

## R18 S43 [18], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "Separation of gravitational perturbations of Myers--Perry black holes"; Jun-Kun Zhao; Hong-Da Lyu
- Check: record: title match yes, authors match yes; cited v1, latest v2
- Note: v1 as cited is right, but a v2 was posted on 19 Nov 2026 (arXiv API: updated 2026-11-19T18:59:27Z), with a new abstract that no longer mentions the singly spinning limit; it is in v2's introduction (p.1). Keep v1 deliberately, or cite v2 and move the anchor.

## R19 S42 [19], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "Price's law for scalar waves on 1+4 dimensional subextremal Myers-Perry spacetimes"; Pieter-Bart Peters
- Check: record: title match yes, authors match yes; cited v1, latest v1
- Note: Authors, title and identifier match the record; the cited version is the latest.

## R20 S37 [20], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "Gravitational mode stability and the nonlinear stability of Kerr–de Sitter black holes in the full subextremal range"; Padhi, Jaideep Sai
- Check: record: title match yes, authors match yes; cited v1, latest is_last=True; concept 24146363
- Note: BHM-189 R01's fix is taken: version DOI 10.5281/zenodo.24146364 (v1), with the concept DOI named; the record is still the latest version (is_last).

## R21 S39 [21], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "Complete quasinormal modes of Type-D black holes. II. Extremal Kerr black holes"; Changkai Chen; Xiaohua Zhang; Zhoujian Cao; Jiliang Jing
- Check: record: title match yes, authors match yes; cited v3, latest v3
- Note: Authors, title and identifier match the record; the cited version is the latest.

## R22 S38 [22], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "A computer assisted existence proof for a non-Schwarzschild black hole in Einstein--Weyl gravity"; Kevin Goldstein; Vishnu Jejjala
- Check: record: title match yes, authors match yes; cited v2, latest v2
- Note: Authors, title and identifier match the record; the cited version is the latest.

## R23 S58 [23], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "A certified spectral gap and the failure of strong cosmic censorship for linear waves on an explicit Reissner–Nordström–de Sitter black hole"; Neko2333OWO
- Check: record: title match yes, authors match yes; cited index 0, latest is_last=True; concept 24285820
- Note: Authors, title and identifier match the record; the cited version is the latest.

## R24 S59 [24], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "Linear instability of an ultraspinning Myers–Perry black hole in seven dimensions: a certified negative canonical energy"; Neko2333OWO
- Check: record: title match yes, authors match yes; cited index 0, latest is_last=True; concept 24288753
- Note: Authors, title and identifier match the record; the cited version is the latest.

## R25 S57 [25], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "Choptuik's critical spacetime exists"; Michael Reiterer; Eugene Trubowitz
- Check: record: title match yes, authors match yes; cited v1, latest v1
- Note: Authors, title and identifier match the record; the cited version is the latest. Journal version: Commun. Math. Phys. 368, 143-186 (2019).

## R26 S56 [26], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "A Proof for the Mode Stability of a Self-similar Wave Map"; Ovidiu Costin; Roland Donninger; Xiaoyue Xia
- Check: record: title match yes, authors match yes; cited v3, latest v3
- Note: Authors, title and identifier match the record; the cited version is the latest.

## R27 S44 [27], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "Nonlinear stability of the Larson-Penston collapse"; Yan Guo; Mahir Hadzic; Juhi Jang; Matthew Schrecker
- Check: record: title match yes, authors match yes; cited v1, latest v1
- Note: Authors, title and identifier match the record; the cited version is the latest.

## R28 S46 [28], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "A constructive computer-assisted existence proof for a Calabi--Yau metric"; Michael R. Douglas; Javier Gómez-Serrano; Fabian Lehmann; Daniel Platt; Yidi Qi
- Check: record: title match yes, authors match yes; cited v1, latest v1
- Note: Authors, title and identifier match the record; the cited version is the latest.

## R29 S47 [29], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "Rigorously Certified Neural-Network Computation of Nonlinear Water Waves at Near-Machine Precision"; Michal Shavit; Yongji Wang; Tristan Buckmaster
- Check: record: title match yes, authors match yes; cited v1, latest v1
- Note: Authors, title and identifier match the record; the cited version is the latest.

## R30 S33 [30], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "Non-vanishing non-linear Static Love Number of a Class of Extremal Reissner-Nordstrom Black Holes"; L. R. Gounis; A. Kehagias; G. Panagopoulos; A. Riotto
- Check: record: title match yes, authors match yes; cited v1, latest v1
- Note: Authors, title and identifier match the record; the cited version is the latest.

## R31 S45 [31], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "Geometrically Induced Semiclassical Limit for Quasinormal Modes and Greybody Factors in Higher-Dimensional Near-Ultracold spacetimes"; Bogeun Gwak
- Check: record: title match yes, authors match yes; cited v1, latest v1
- Note: Authors, title and identifier match the record; the cited version is the latest.

## R32 S54 [32], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "Quasinormal modes in extremal Reissner-Nordström spacetimes"; Dejan Gajic; Claude Warnick
- Check: record: title match yes, authors match yes; cited v2, latest v2
- Note: Authors, title and identifier match the record; the cited version is the latest. Journal version: Comm. Math. Phys. 385, p1395-1498 (2021).

## R33 S55 [33], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "Mode stability for the Teukolsky equation on extremal and subextremal Kerr spacetimes"; Rita Teixeira da Costa
- Check: record: title match yes, authors match yes; cited v1, latest v1
- Note: Authors, title and identifier match the record; the cited version is the latest. Journal version: Communications in Mathematical Physics, 378(1), 705-781 (2020).

## R34 S31 [34], reference entry, anchor reference entry: **OK** (RECORD)

- Passage: Record: "You've got a Freund--Rubin in Me: The Aretakis Instability of Extremal Black Branes"; Calvin Y. -R. Chen; Áron D. Kovács
- Check: record: title match NO, authors match yes; cited v3, latest v3
- Note: The v3 PDF's title page reads "On the Aretakis Instability of Extremal Black Branes" (l.6), as the entry does; arXiv's metadata for v3 gives "You've got a Freund--Rubin in Me: The Aretakis Instability of Extremal Black Branes", which is what arXiv and INSPIRE listings show.

