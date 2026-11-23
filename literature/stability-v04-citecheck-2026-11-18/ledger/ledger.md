# Ledger: citation check of DRAFT_v0.4.md (sha256 28af203a...8864)

One entry per citation (C01-C38) and per reference entry (R01-R23). Passages are from the text layers named in message 18 (pdftotext -layout, poppler 0.86.1). Line numbers count as grep -n does. Runs of spaces are collapsed and lines are joined with a space; "[...]" joins separate ranges. Otherwise the text is as in paper.txt, line-end hyphens included. Bracketed words in a passage are mine.

## C01 S28, draft l.50 (§1), Table 1: **OK**

- Passage (l.740-745): Table 1: Stability of static black holes. [Columns: Tensor, Vector, Scalar, each split Q = 0 | Q ≠ 0. Row K = 1, λ = 0, column Scalar, Q ≠ 0:] D = 4, 5 OK [/] D ≥ 6 ?
- Note: Outside the listed scope (message 18 names S28's eqs. (76)–(77) and l.762–767); checked because it is an anchored S28 citation in §1. The text layer renders ≠ as "6="; the table cell was read from the layout and the PDF.

## C02 S48, draft l.52 (§1), l.2275–2276: **OK**

- Passage (l.2275-2276): parameter range. In contrast, for scalar type perturbation, we were not able to prove even the stability of asymptotically flat black holes with charge in generic dimensions,
- Check: quote found verbatim in draft and source
- Note: Quote verbatim. S48 is a review chapter (l.20–21: "In this chapter ... We first review"), so "In their review" holds. The source sentence goes on: "due to the existence of a negative region in the effective potential around the horizon in the extremal and near extremal cases" (l.2277–2278), which the draft's next sentence paraphrases.

## C03 S28, draft l.57 (§1), eqs. (76)–(77): **OK**

- Passage (l.705-712, 762): By the similar S-deformation S = (f/h) dh/dr ; h = r^{n/2−1} H− , (76) the effective potential VS− for Φ− is transformed to ṼS− = k²f/(2r²H−) [2m − (n + 1)(n − 2)(1 + mδ)x] . (77) [...] Hence, the gravitational mode is also stable for n = 2.
- Note: Fractions reassembled from the display layout of l.705–712. At n = 2 the bracket in (77) is 2m, and l.762 draws the conclusion for n = 2 (D = 4). So "the S-deformation that proves D = 4" is (76)–(77).

## C04 S28, draft l.58-59 (§1), l.762–767: **SAYS MORE**

- Passage (l.762-767): Hence, the gravitational mode is also stable for n = 2. However, for n > 2, ṼS− becomes negative near the horizon in general (See Fig.3). The S-deformation used in the neutral case does not work either, because it cannot remove a negative ditch of VS− produced by the charge near the horizon. We have not been able to prove the stability for n > 2 by this method, except for some special cases.
- Check: quote found verbatim in draft and source
- Note: Quote verbatim. But the draft's "leaves a negative region near the horizon for n > 2" drops the source's "in general" (l.763: "for n > 2, ṼS− becomes negative near the horizon in general"). n = 3 (D = 5) is one of the special cases: S28's summary establishes the charged case "for D = 4 and D = 5" (l.774–776), and S48 l.2263–2265 says ṼS− > 0 for K = 1, λ ≥ 0, n = 3. As written, the sentence conflicts with the draft's own l.49 (stability for D = 4 and 5). Fix: restore "in general", or say the negative region appears for n ≥ 4 in general, D = 5 being one of the special cases.

## C05 S48, draft l.61-62 (§1), l.2406–2408: **SAYS MORE**

- Passage (l.2404-2408): For some cases, in particular, when electric charge and cosmological constant are involved, we have not yet been able to draw definite conclusions for the stability problem with respect to scalar type perturbations. This is in part because there does not seem to be a systematic method to find such a desirable function S that could apply to generic cases. In particular, for the charged black hole case, the potential
- Check: quote found verbatim in draft and source
- Note: Quote verbatim, but it stops before the restrictive clause that ends the source's sentence: "... such a desirable function S that could apply to generic cases" (l.2407–2408). Without it the quote reads as no systematic method at all. Fix: quote through "that could apply to generic cases".

## C06 S52, draft l.69-70 (§1), l.2476–2479: **SAYS MORE**

- Passage (l.2477-2479): As we have mentioned above, (5.22) is correct as stated for l ≥ 2. It is easily verified 38 that all quasinormal modes with l ≥ 2 have negative imaginary components (and so represent decaying fluctuations).
- Note: l.2476 is the page number ("– 43 –"); the passage is l.2477–2479. The modes are the light quasinormal modes of the charged membrane: section 5 is "Light quasinormal spectrum o[f] the RN black hole" (contents, l.77), and (5.22) is "our final result for the light quasinormal mode frequencies associated with shape fluctuations" (l.2438–2439), at leading order in large D (l.2425–2426, l.2431), in flat space. The draft's "the quasinormal modes of the charged black hole with Λ = 0 decay" covers all quasinormal modes; heavy (O(D)) modes are not in the membrane description. Fix: "the light quasinormal modes" (one word).

## C07 S51, draft l.69-70 (§1), l.326–330: **SAYS MORE**

- Passage (l.326-330): perturbations). So we consider the gravitational perturbations with ℓ > 1 and gauge field perturbations with ℓ > 0. At the zero cosmological constant limit L → ∞, these results reproduce the quasinormal modes of Reissner-Nordstrom black hole obtained in [12]. At Q = 0, ω± reduces to quasinormal modes of scalar type perturbation of (Anti) de Sitter Schwarzschild black hole [15]. At the both limits, the perturbations are stable. On the other
- Note: Passage l.327–330 (l.326 finishes the previous sentence). The ω± of (3.8) are modes of the leading-order large-D effective equations (l.93, l.296–319), and at L → ∞ they "reproduce the quasinormal modes of Reissner-Nordstrom black hole obtained in [12]", where [12] is S52 (l.482). So the same scope note as the S52 row applies; the same one-word fix covers both.

## C08 S53, draft l.74 (§1), l.524–531: **OK**

- Passage (l.525-530): In this paper, we extended the formalism in [16, 17] to coupled systems where the per- turbative field equations take the form of systems of coupled Schrödinger equations. Similar to [16, 17], the existence of S-deformation implies the linear mode stability of the system. Also, we applied our formalism to the case of the Schwarzschild black hole in dynamical Chern-Simons gravity and a charged Kaluza-Klein black hole [22, 30], and we showed the stability of the spacetime by finding a regular S-deformation function numerically. While
- Note: l.524 is blank and l.531 starts the next sentence; the passage is l.525–530. The two coupled systems are the Schwarzschild black hole in dynamical Chern–Simons gravity and a charged Kaluza–Klein black hole (l.528–529).

## C09 S49, draft l.77 (§1), l.20–30: **OK**

- Passage (l.20-30): Abstract We prove the linear stability of subextremal Reissner-Nordström spacetimes as solutions to the Einstein–Maxwell equation. We make use of a novel representation of gauge-invariant quanti- ties which satisfy a symmetric system of coupled wave equations. This system is composed of two of the three equations derived in our previous works [20], [21], where the estimates required arbitrary smallness of the charge. Here, the estimates are obtained by defining a combined energy-momentum tensor for the system in terms of the symmetric structure of the right hand sides of the equations. We obtain boundedness of the energy, Morawetz estimates and decay for the full subextremal range |Q| < M , completely in physical space. Such decay estimates, together with the estimates for the gauge-dependent quantities of the perturbations obtained in [22], settle the problem of linear sta- bility to gravitational and electromagnetic perturbations of Reissner-Nordström solution in the full subextremal range |Q| < M .
- Note: "settle the problem of linear stability to gravitational and electromagnetic perturbations of Reissner-Nordström ... in the full subextremal range |Q| < M" (l.28–30). Linear stability with boundedness and decay (l.26–27) is beyond mode stability, as the draft says.

## C10 S50, draft l.79 (§1), l.26–29: **OK**

- Passage (l.26-29): tion. In the analysis of the master quantities, we strengthen the mode stability result of Kodama-Ishibashi to a uniform boundedness estimate in all dimensions; further, we prove decay estimates in the case of six or fewer spacetime dimensions. Finally, we provide a rigorous argument
- Check: quote found verbatim in draft and source
- Note: Quote verbatim (across l.27–28). "decay for D ≤ 6" is "decay estimates in the case of six or fewer spacetime dimensions" (l.28–29).

## C11 S40, draft l.81 (§1), l.7–12: **SAYS MORE**

- Passage (l.7-12): We study linearized perturbations of the subextremal Kerr–Newman black hole solution of the Einstein–Maxwell equations. We show how to overcome what Chandrasekhar called the “apparent indissolubility of the coupling between the spin-1 and spin-2 fields” by using a matrix integrating factor for suitably transformed first-order systems that describe the radiative degrees of freedom. For the radial ODEs obtained after angular separation, we prove mode stability on the real axis, i.e., the absence of quasinormal modes with real frequencies, using a Whiting-type transform.
- Note: Supported except for one qualifier: the source is about "the subextremal Kerr–Newman black hole" (l.7). The draft says "For Kerr–Newman", which reads as including extremal Kerr–Newman, a case the draft treats as distinct elsewhere (§7, Extremality). Fix: "For subextremal Kerr–Newman".

## C12 S41, draft l.83 (§1), l.444–445: **OK**

- Passage (l.444-445): (2) The mode stability result of Andersson–Häfner–Whiting [AHW24] for linearized gravity holds in the full subextremal range and is used here as a black box.
- Check: quote found verbatim in draft and source
- Note: Quote verbatim. The result used as a black box is Andersson–Häfner–Whiting's mode stability for linearized gravity [AHW24] (l.444), if the draft wants to credit it.

## C13 S41, draft l.84 (§1), l.539–541: **SAYS MORE**

- Passage (l.538-541): (15) Hintz–Petersen–Vasy [HPV25] proved the nonlinear stability of Kerr–de Sitter black holes in the full subextremal range, conditional on the validity of mode stability for the linearized Einstein equation—which, unlike in the Kerr case, remains an open problem except in the slow-rotation regime (see also [Hin25b] for the small mass regime). The basic strategy is
- Check: quote found verbatim in draft and source
- Note: Quote verbatim, but the source's sentence continues "(see also [Hin25b] for the small mass regime)" (l.541), a second regime where Kerr–de Sitter mode stability is known; [Hin25b] is Hintz, "Mode stability and shallow quasinormal modes of Kerr–de Sitter black holes away from extremality" (l.24885). Fix: add the small-mass regime after the quote. "As of that paper" correctly dates the statement (v2, 3 Aug 2026; S37 is later).

## C14 S43, draft l.86 (§1), l.11–26: **OK**

- Passage (l.11-16, 22-27): We study linearized gravitational perturbations of five-dimensional asymptotically flat Myers– Perry black holes with two unequal spins. We construct separated solutions for the five coupled gauge-invariant polarizations for arbitrary azimuthal mode numbers. The key observation is that the Killing–Yano symmetry induces a first-order angular operator that, together with a commuting second-order operator, determines the angular profiles of all five gravitational polarizations. The Carter interchange relates the scalar angular and radial equations, and the five tidal components [...] of each separated solution share a single radial amplitude. We prove completeness of the angular harmonics at real frequencies and show that the resulting physical perturbations admit local metric reconstruction. In the singly spinning limit, we recover Santos’s angular operators and radial equation for perturbations with mψ = 0 and even parity under ψ → −ψ. These results provide a framework for studying quasinormal modes and gravitational stability of five-dimensional rotating black holes with two independent spins.
- Note: The separation is for five-dimensional asymptotically flat Myers–Perry "with two unequal spins" and arbitrary azimuthal numbers (l.11–13). The source itself names an earlier special case: "In the singly spinning limit, we recover Santos's angular operators and radial equation for perturbations with mψ = 0 and even parity" (l.24–25). So "separated only recently" holds for the general case. If precision is wanted: "separated in general only recently". (l.17–21 are the arXiv margin stamp and blank lines.)

## C15 S42, draft l.87 (§1), l.163–164, l.446–447: **OK**

- Passage (l.163-164, 446-447): case to a and b and also renormalize G such that µ = 2m. The theorem is as of writing still condition on the assumption of real mode stability for the wave equation. [...] this is exactly the content of [CPWZ22], however it has not been shown to hold yet down to the real axis Im σ = 0. For the purposes of this paper we will take the latter as a mild conditional assumption,
- Check: quote found verbatim in draft and source
- Note: Quote verbatim (l.446). What has not been shown is mode stability "down to the real axis Im σ = 0" (l.446–447), as the draft says; the main theorem is "still condition[al] on the assumption of real mode stability for the wave equation" (l.163–164).

## C16 S37, draft l.91 (§1), l.10–15: **SAYS MORE**

- Passage (l.8-15): Abstract. We prove that subextremal Kerrde Sitter black holes are nonlinearly stable as solutions of the Einstein vacuum equations with positive cosmological constant, in the full subextremal range. Hintz, Petersen and Vasy reduced this to mode stability of the ungauged linearized Einstein equation; we prove that statement. The main step is mode stability of the Teukolsky equations of spin ±2: there are no nontrivial outgoing modes with Im σ ≥ 0. From it we deduce that every generalized mode of the linearized Einstein equation with Im σ ≥ 0 is pure gauge, up to a linearized Kerrde Sitter metric when σ = 0. Part of the proof is computer-assisted.
- Note: The claim is for Kerr–de Sitter "in the full subextremal range" (l.8–10) and is that there are "no nontrivial outgoing modes with Im σ ≥ 0" (l.12). The draft drops "subextremal" ("mode stability for Kerr–de Sitter"). Dropping "nontrivial" is harmless. Fix: "for subextremal Kerr–de Sitter". The anchor could start at l.8, where the subextremal range is stated.

## C17 S37, draft l.91-92 (§1), l.126–128: **OK**

- Passage (l.126-128): Computer assistance. The computer-assisted steps are listed in Appendix A. All are exact except C9, which uses oating-point arithmetic with rigorous error bounds. The code is available on request.
- Note: "All are exact except C9, which uses floating-point arithmetic with rigorous error bounds" (the text layer drops the fl ligature: "oating"). The source says "computer-assisted steps"; the draft's "certificates" is a fair paraphrase.

## C18 S37, draft l.93 (§1), l.1338: **OK**

- Passage (l.1338): them. No human expert has yet checked the argument. I have reviewed and edited the content
- Check: quote found verbatim in draft and source
- Note: Quote verbatim, in the author's first-person statement on AI use (l.1330–1339). "Unrefereed preprint": the Zenodo record's resource type is publication/preprint.

## C19 S39, draft l.95 (§1), l.139–141, l.1845–1848: **SAYS MORE**

- Passage (l.138-141, 1844-1848): [left column, l.138–141:] these families; it is not a damping threshold or a claim to ex- haust all Riemann sheets. A certified contour establishes ex- actly one simple DM in the stated (3, 3) domain, while critical [...] [right column, l.1844–1848:] with angular isolation and the absence of normalization poles, this proves that D33 contains exactly the one simple QNM shown in Fig. 10a. The statement applies to this domain, an- gular branch, and Riemann sheet.
- Note: Two-column layout; columns separated by hand. The anchors are right. The draft keeps "one bounded frequency domain" but drops the other two qualifiers: "The statement applies to this domain, angular branch, and Riemann sheet" (l.1846–1848; also the abstract, l.36–37). Fix: "in one bounded frequency domain, on one angular branch and Riemann sheet". "within a numerical survey" is supported by the abstract ("the survey extending through the 41st overtone", l.28).

## C20 S38, draft l.97 (§1), l.19–33: **OK**

- Passage (l.19-33): Abstract: Static, asymptotically flat, non-Schwarzschild black holes in four-dimensional Einstein–Weyl gravity have previously been constructed by numerical shooting, while the local field equations admit horizon and asymptotic expansions to all orders. We give a computer assisted existence proof for a non-Schwarzschild solution whose dimensionless horizon radius is one in units of the massive spin-two scale, with parameters close to the previously reported numerical branch. The exterior is divided into a convergent horizon series domain, a compact core enclosed by a parameter dependent Taylor model with directed rounding, and an infinite asymptotic domain treated as a centered stable manifold fixed point problem. The resulting five-dimensional matching map between the core and tail is continuous on a rigorously specified box. After exact rational preconditioning, the signs on opposite faces satisfy the hypotheses of the Poincaré–Miranda theorem and therefore certify a matching zero. The solution has a regular nondegenerate horizon, no additional exterior horizon, vanishing Ricci scalar, and nonvanishing Ricci tensor. The strict bounds also imply existence at every sufficiently nearby horizon radius and a local continuous family at fixed coupling. The proof establishes existence, but not uniqueness of the matching zero.
- Note: "We give a computer assisted existence proof for a non-Schwarzschild solution" (l.21–22): static, asymptotically flat, at one horizon radius and nearby (l.19, l.22–23, l.31–32); existence, not uniqueness (l.33).

## C21 S58, draft l.99 (§1), l.8–22: **OK**

- Passage (l.8-22): Abstract. We consider the subextremal Reissner–Nordström–de Sitter black hole whose horizons are at r− = 19/20, r+ = 1 and rc = 2, with cosmological constant Λ = 1200/4301. We prove that every nonzero quasinormal mode of the massless scalar wave equation on its exterior, for every angular momentum ℓ, satisfies Im ω < − 35 κ− , where κ− is the surface gravity of the Cauchy horizon. The frequency ω = 0 occurs only for ℓ = 0, with a constant mode, and is a simple zero. By a theorem of Hintz and Vasy, solutions with smooth initial 1 data then extend across the Cauchy horizon in Hloc and are continuous up to it, so the Christodoulou formulation of strong cosmic censorship fails for this linear model at this parameter point. Bounded frequencies and low angular momenta are handled by interval- arithmetic certificates for the radial Wronskian. All remaining frequencies are excluded by a Hermite-type monotone quantity integrated along complex contours in the tortoise coordinate. This quantity gives certificates that hold uniformly in ℓ ≥ 10, so the infinitely many angular momenta are covered by finitely many interval computations. The certificates and the programs that check them are in the supplement.
- Note: Massless scalar wave equation (a test field) on one subextremal Reissner–Nordström–de Sitter black hole with rational horizon radii (l.8–11); interval-arithmetic certificates (l.17–22). The text layer renders the bound as "− 35 κ−", i.e. −(3/5)κ− (l.11).

## C22 S59, draft l.100 (§1), l.8–22: **OK**

- Passage (l.8-22): Abstract. We prove that the singly spinning Myers–Perry black hole in seven spacetime dimensions with rotation parameter a/r+ = 8 is linearly unstable in the sense of Prabhu and Wald. We construct smooth, compactly supported, constraint-satisfying initial data that are invariant under U (1) × SO(4) and odd under the (t-ϕ) reflection. For their gauge-fixed repre- sentative P ′ we establish that the potential energy of KP ′ , the initial time derivative of the corresponding solution, is negative. Positivity of the kinetic energy makes the Rayleigh–Ritz quotient ω 2 of Prabhu and Wald negative, and their variational principle gives exponential growth of the kinetic energy of the time derivative of the solution. We identify this potential energy with the local canonical energy of the evolved compactly supported data, by an ar- gument that uses only identities from the Prabhu–Wald framework. The trial is explicit; the negativity is established by a computer-assisted certificate: a rigorous adaptive quadrature in which the integrand is bounded on complex polydiscs by bivariate Taylor models with inter- val remainders. The certified value is a small residue of large contributions of both signs, and its sign relies on the exactness of the symbolic derivation; we state this dependence explicitly. The certificate, its records and the programs that check them are in the supplement.
- Note: Singly spinning, D = 7, a/r+ = 8, linear instability in the sense of Prabhu and Wald (l.8–10), by a computer-assisted certificate (l.18–20). The author states that the sign "relies on the exactness of the symbolic derivation" (l.20–21).

## C23 S57, draft l.102 (§1), l.9–18: **OK**

- Passage (l.9-18): Abstract: About twenty years ago, Choptuik studied numerically the gravi- tational collapse (Einstein field equations) of a massless scalar field in spheri- cal symmetry, and found strong evidence for a universal, self-similar solution at the threshold of black hole formation. We prove rigorously the existence of a real analytic solution, that we interpret as the solution observed by Chop- tuik. Our construction covers an open neighborhood of the past light cone of the singularity. The proof is computer assisted. Starting from an explicit ap- proximate solution, we show that nearby there is a true solution. The source code and a high precision data file (about 80 significant decimal digits, with rigorous error bounds) are included. We do not study perturbations.
- Note: "The proof is computer assisted" (l.15). The source proves existence of "a real analytic solution, that we interpret as the solution observed by Choptuik", on "an open neighborhood of the past light cone of the singularity" (l.12–15). The draft's sentence matches the paper's title, "Choptuik's critical spacetime exists"; the two qualifiers could be added if wanted.

## C24 S56, draft l.103 (§1), l.6–14: **ANCHOR OFF**

- Passage (l.6-7, 100-103): Abstract. We study the fundamental self-similar solution to the SU(2) sigma model, found by Shatah and Turok-Spergel. We give a rigorous proof for its mode stability. Based on earlier results by the second [...] convergence of a certain continued fraction. We provide rigorous error estimates for all our approximations. Furthermore, we emphasize that all computations are free of rounding errors since we work exclusively with rational numbers. As a consequence, our result is completely rigorous although we have to admit that it seems unrealistic to perform all our computations without the aid of some computer algebra system.
- Note: The abstract (l.6–14) gives "a rigorous proof for its mode stability" (l.7) but says nothing about computer assistance. That is at l.100–103: all computations are in rational numbers, free of rounding errors, and "it seems unrealistic to perform all our computations without the aid of some computer algebra system". Right lines: l.6–7 and l.100–103.

## C25 S44, draft l.104 (§1), l.16–21: **OK**

- Passage (l.16-21): One of the key challenges is the proof of mode-stability for the non self-adjoint spectral prob- lem which arises when linearising the dynamics around the Larson-Penston collapsing solution. To exclude the presence of complex growing modes other than the trivial one associated with time trans- lation symmetry, we use a high-order energy method in low and high frequency regimes, for which the monotonicity properties are crucially exploited, and use rigorous computer-assisted techniques in the intermediate regime. In addition, the maximal dissipativity of the linearised operator is proven on
- Note: "the proof of mode-stability for the non self-adjoint spectral problem ... use rigorous computer-assisted techniques in the intermediate regime" (l.16–21). It is mode stability of the Larson–Penston solution of the isothermal Euler–Poisson system (l.11–12).

## C26 S46, draft l.105 (§1), (none): **OK**

- Passage (l.14-19): We give a rigorous, constructive proof that there exists a Ricci-flat Kähler metric on the Fermat quartic hypersurface, independently of Yau’s famous theorem, along with an explicit and accurate analytic approximation to the metric. The proof combines numerical techniques to obtain the approximately Ricci flat metric, a fixed point theorem to prove existence, and verified numerics to get the bounds used by the fixed point theorem. The method is general and we discuss the computational issues in applying it to other manifolds.
- Note: No anchor in the draft. Supported at l.14–19: a rigorous, constructive existence proof of a Ricci-flat Kähler metric on the Fermat quartic, with "verified numerics to get the bounds used by the fixed point theorem" (math.DG).

## C27 S47, draft l.105 (§1), (none): **OK**

- Passage (l.32-44): high-amplitude candidate solutions. We freeze one such machine-learned candi- date as an explicit finite representation and certify its residual using interval arithmetic, rigorously accounting for floating-point roundoff, Fourier truncation, aliasing and grid-to-continuum errors. The resulting computation establishes a rigorous uniform bound on the governing-equation residual, independently val- idating the accuracy achieved through neural-network computation. We then formalize the mathematical structure of the certification argument in Lean, which machine-checks the deductions connecting the certified numerical bounds to the final residual theorem. Both the interval certification and formalization were developed with substantial assistance from a large language model, while the validity of the result remains independent of the language model: the numer- ical bounds are rigorously enclosed by interval arithmetic and the subsequent mathematical deductions are checked by the Lean kernel. Together, these steps
- Note: No anchor in the draft. Supported at l.32–44: an interval-arithmetic residual certificate for a machine-learned water-wave candidate, and a Lean formalisation of "the deductions connecting the certified numerical bounds to the final residual theorem" (l.38–40). The certificate bounds a residual; it is not an existence proof.

## C28 S37, draft l.132 (§1), (none): **OK**

- Passage (l.10-15): subextremal range. Hintz, Petersen and Vasy reduced this to mode stability of the ungauged linearized Einstein equation; we prove that statement. The main step is mode stability of the Teukolsky equations of spin ±2: there are no nontrivial outgoing modes with Im σ ≥ 0. From it we deduce that every generalized mode of the linearized Einstein equation with Im σ ≥ 0 is pure gauge, up to a linearized Kerrde Sitter metric when σ = 0. Part of the proof is computer-assisted.
- Note: No anchor in the draft. The disclaimer rests on S37's claim of computer-assisted mode stability (l.10–15). As a disclaimer it says nothing beyond the source.

## C29 S52, draft l.404 (§7), l.2476–2479: **SAYS MORE**

- Passage (l.2477-2479): As we have mentioned above, (5.22) is correct as stated for l ≥ 2. It is easily verified 38 that all quasinormal modes with l ≥ 2 have negative imaginary components (and so represent decaying fluctuations).
- Note: Same passage and same point as the §1 S52 row: these are the light quasinormal modes (l.2438–2439) at leading order in large D. The draft's "the modes at Λ = 0 decay" needs "light". l.2476 is the page number.

## C30 S51, draft l.404 (§7), l.326–330: **SAYS MORE**

- Passage (l.326-330): perturbations). So we consider the gravitational perturbations with ℓ > 1 and gauge field perturbations with ℓ > 0. At the zero cosmological constant limit L → ∞, these results reproduce the quasinormal modes of Reissner-Nordstrom black hole obtained in [12]. At Q = 0, ω± reduces to quasinormal modes of scalar type perturbation of (Anti) de Sitter Schwarzschild black hole [15]. At the both limits, the perturbations are stable. On the other
- Note: Same as the §1 S51 row: the modes of the leading-order effective theory, which at L → ∞ reproduce S52's.

## C31 S51, draft l.409 (§7), l.26–30: **OK**

- Passage (l.26-30): We study the large D effective theory for D dimensional charged (Anti) de Sitter black holes. Then we show that the de Sitter Reissner-Nordstrom black hole becomes unstable against gravitational perturbations at larger charge than a critical charge in a higher dimension. Furthermore we find that there is a non-trivial zero-mode static perturbation at the critical charge. The existence of static perturbations suggests the appearance of non-spherical sym-
- Note: "the de Sitter Reissner-Nordstrom black hole becomes unstable against gravitational perturbations at larger charge than a critical charge in a higher dimension" (l.27–28). l.29–30 concern the zero mode at the critical charge; the anchor could be l.27–28.

## C32 S45, draft l.410 (§7), l.18–27: **OK**

- Passage (l.18-27): In this work, we investigate the correspondence between quasinormal modes (QNMs) and greybody factors (GBFs) in higher-dimensional Reissner–Nordstöm–de Sitter black holes based on the massless scalar field. Our analysis focuses on the QNMs in the near-ultracold family where the inner, outer, and cosmological horizons are close together. Under the geometric limit condition, the leading-order Wentzel–Kramers–Brillouin term of the QNM is dominant for fixed angular quantum numbers and dimensionality without imposing the eikonal limit. Particularly, the corresponding GBFs also retain the explicit form of both parameters. Furthermore, we demonstrate that the half-transmission frequency of the GBF and its derivative are related to null geodesics, in terms of aspects such as the angular frequency and Lyapunov exponent, with the use of both parameters. We provide their relationships in arbitrary dimensionality. Furthermore, the higher-order corrections to the QNMs are investigated at the Nariai limit and in the near-ultracold geometry with separated horizons.
- Note: Massless scalar field on higher-dimensional Reissner–Nordström–de Sitter black holes, quasinormal modes of the near-ultracold family at leading WKB order (l.18–22). "Semiclassical" is the paper's own word (title).

## C33 S58, draft l.411 (§7), (none): **OK**

- Passage (l.8-12, 16-17): Abstract. We consider the subextremal Reissner–Nordström–de Sitter black hole whose horizons are at r− = 19/20, r+ = 1 and rc = 2, with cosmological constant Λ = 1200/4301. We prove that every nonzero quasinormal mode of the massless scalar wave equation on its exterior, for every angular momentum ℓ, satisfies Im ω < − 35 κ− , where κ− is the surface gravity of the Cauchy horizon. The frequency ω = 0 occurs only for ℓ = 0, with a constant [...] Christodoulou formulation of strong cosmic censorship fails for this linear model at this parameter point. Bounded frequencies and low angular momenta are handled by interval-
- Note: No anchor in the draft. "at one parameter point": the black hole is a single explicit one (l.8–9), and the paper says "at this parameter point" (l.16–17). Suggested anchor: l.8–12, l.16–17.

## C34 S54, draft l.415 (§7), l.8–24: **OK**

- Passage (l.8-18, 23-24): Abstract. We present a new framework for characterizing quasinormal modes (QNMs) or resonant states for the wave equation on asymptotically flat spacetimes, applied to the setting of extremal Reissner–Nordström black holes. We show that QNMs can be interpreted as honest eigenfunctions of generators of time translations acting on Hilbert spaces of initial data, corresponding to a suitable time slicing. The main difficulty that is present in the asymptotically flat setting, but is absent in the previously studied asymptotically de Sitter or anti de Sitter sub-extremal black hole spacetimes, is that L2 -based Sobolev spaces are not suitable Hilbert space choices. Instead, we consider Hilbert spaces of functions that are additionally Gevrey regular at infinity and at the event horizon. We introduce L2 -based Gevrey estimates for the wave equation that are intimately connected to the existence of conserved quantities along null infinity and the event horizon. We relate this new framework to the arXiv:1910.08479v2 [gr-qc] 7 Jun 2021 [...] traditional interpretation of quasinormal frequencies as poles of the meromorphic continuation of a resolvent operator and obtain new quantitative results in this setting.
- Note: "QNMs can be interpreted as honest eigenfunctions of generators of time translations" on Hilbert spaces of functions "additionally Gevrey regular at infinity and at the event horizon" (l.10–15), for extremal Reissner–Nordström (l.9–10). (l.18–22 are the arXiv margin stamp and blank lines.)

## C35 S55, draft l.416 (§7), l.15–26: **OK**

- Passage (l.15-26): We prove that there are no exponentially growing modes nor modes on the real axis for the Teukolsky equation on Kerr black hole spacetimes, both in the extremal and subextremal case. We also give a quantitative refinement of mode stability. As an immediate application, we show that the transmission and reflection coefficients of the scattering problem are bounded, independently of the specific angular momentum of the black hole, in any compact set of real frequencies excluding zero frequency and the superradiant threshold. While in the subextremal setting these results were known previously, the extremal case is more involved and has remained an open problem. Ours are the first results outside axisymmetry and could serve as a preliminary step towards understanding boundedness, scattering and decay properties of general solutions to the Teukolsky equation on extremal Kerr black holes.
- Note: "no exponentially growing modes nor modes on the real axis for the Teukolsky equation on Kerr ... both in the extremal and subextremal case" (l.15–17). The anchor could be l.15–17 (and l.22–23 for "the extremal case ... has remained an open problem").

## C36 S43, draft l.421 (§7), (none): **OK**

- Passage (l.11-13): We study linearized gravitational perturbations of five-dimensional asymptotically flat Myers– Perry black holes with two unequal spins. We construct separated solutions for the five coupled gauge-invariant polarizations for arbitrary azimuthal mode numbers. The key observation is that
- Note: No anchor in the draft. As in the §1 S43 row; suggested anchor l.11–13 (two unequal spins; earlier special case at l.24–25).

## C37 S42, draft l.422 (§7), (none): **OK**

- Passage (l.163-164, 446-447): case to a and b and also renormalize G such that µ = 2m. The theorem is as of writing still condition on the assumption of real mode stability for the wave equation. [...] this is exactly the content of [CPWZ22], however it has not been shown to hold yet down to the real axis Im σ = 0. For the purposes of this paper we will take the latter as a mild conditional assumption,
- Note: No anchor in the draft. As in the §1 S42 row; suggested anchor l.163–164, l.446–447.

## C38 S59, draft l.423 (§7), (none): **OK**

- Passage (l.8-10, 17-20): Abstract. We prove that the singly spinning Myers–Perry black hole in seven spacetime dimensions with rotation parameter a/r+ = 8 is linearly unstable in the sense of Prabhu and Wald. We construct smooth, compactly supported, constraint-satisfying initial data that are [...] gument that uses only identities from the Prabhu–Wald framework. The trial is explicit; the negativity is established by a computer-assisted certificate: a rigorous adaptive quadrature in which the integrand is bounded on complex polydiscs by bivariate Taylor models with inter- val remainders. The certified value is a small residue of large contributions of both signs, and
- Note: No anchor in the draft. "Ultraspinning" is in the title; a/r+ = 8 (l.9). Suggested anchor l.8–10, l.17–20.

## R01 S37, draft l.459 (References), reference entry: **BIBLIOGRAPHY**

- Draft entry: - [S37] J. S. Padhi, Gravitational mode stability and the nonlinear stability of Kerr–de Sitter black holes in the full subextremal range, Zenodo, doi:10.5281/zenodo.24146363 (v1, 2026; unrefereed preprint).
- Passage: Zenodo record: title "Gravitational mode stability and the nonlinear stability of Kerr–de Sitter black holes in the full subextremal range"; creators Padhi, Jaideep Sai [Purdue University West Lafayette]; doi 10.5281/zenodo.24146364, conceptdoi 10.5281/zenodo.24146363, id 24146364, version v1, publication_date 2026-11-11, created 2026-11-11, updated 2026-11-11; draft doi 10.5281/zenodo.24146363 = CONCEPT DOI (version DOI is 10.5281/zenodo.24146364)
- Check: authors match: yes; title match (normalised): yes
- Note: Authors and title match the Zenodo record. The DOI is the concept DOI: 10.5281/zenodo.24146363 resolves to the latest version (fetching record 24146363 returned record 24146364). Version v1's own DOI is 10.5281/zenodo.24146364 (record 24146364, published 2026-11-11, file kerr_de_sitter_stability.pdf). "doi:...24146363 (v1, ...)" mixes the two. Fix: "doi:10.5281/zenodo.24146364 (v1, 11 Nov 2026)", or keep the concept DOI and drop "v1". The two resolve to the same file today, since v1 is the only version. My own S36 screen gave 24146363 the same way.

## R02 S38, draft l.461 (References), reference entry: **OK**

- Draft entry: - [S38] K. Goldstein, V. Jejjala, A computer assisted existence proof for a non-Schwarzschild black hole in Einstein–Weyl gravity, arXiv:2609.21797v2.
- Passage: arXiv abstract page of the cited version: title "A computer assisted existence proof for a non-Schwarzschild black hole in Einstein--Weyl gravity"; authors Goldstein, Kevin; Jejjala, Vishnu; versions v1 Fri, 18 Sep 2026 | v2 Mon, 19 Oct 2026; cited v2 = latest v2; SOURCES date 19 Oct 2026 = v2 date: yes
- Check: authors match: yes; title match (normalised): yes
- Note: Authors, title and version match the record; SOURCES.md's date is the cited version's date.

## R03 S39, draft l.463 (References), reference entry: **OK**

- Draft entry: - [S39] C. Chen, X. Zhang, Z. Cao, J. Jing, Complete quasinormal modes of Type-D black holes. II. Extremal Kerr black holes, arXiv:2610.39095v3.
- Passage: arXiv abstract page of the cited version: title "Complete quasinormal modes of Type-D black holes. II. Extremal Kerr black holes"; authors Chen, Changkai; Zhang, Xiaohua; Cao, Zhoujian; Jing, Jiliang; versions v1 Thu, 29 Oct 2026 | v2 Mon, 2 Nov 2026 | v3 Tue, 3 Nov 2026; cited v3 = latest v3; SOURCES date 3 Nov 2026 = v3 date: yes
- Check: authors match: yes; title match (normalised): yes
- Note: Authors, title and version match the record; SOURCES.md's date is the cited version's date.

## R04 S40, draft l.465 (References), reference entry: **OK**

- Draft entry: - [S40] P. Hintz, Perturbations of Kerr–Newman black holes: separation and mode stability, arXiv:2609.33661v1. - [S41] P. Hintz, Nonlinear stability of subextremal Kerr black holes, arXiv:2606.28253v2.
- Passage: arXiv abstract page of the cited version: title "Perturbations of Kerr-Newman black holes: separation and mode stability"; authors Hintz, Peter; versions v1 Sun, 27 Sep 2026; cited v1 = latest v1; SOURCES date 27 Sep 2026 = v1 date: yes
- Check: authors match: yes; title match (normalised): yes
- Note: Authors, title and version match the record; SOURCES.md's date is the cited version's date.

## R05 S41, draft l.466 (References), reference entry: **OK**

- Draft entry: - [S41] P. Hintz, Nonlinear stability of subextremal Kerr black holes, arXiv:2606.28253v2. - [S42] P.-B. Peters, Price's law for scalar waves on 1+4 dimensional subextremal Myers–Perry spacetimes,
- Passage: arXiv abstract page of the cited version: title "Nonlinear stability of subextremal Kerr black holes"; authors Hintz, Peter; versions v1 Fri, 26 Jun 2026 | v2 Mon, 3 Aug 2026; cited v2 = latest v2; SOURCES date 3 Aug 2026 = v2 date: yes
- Check: authors match: yes; title match (normalised): yes
- Note: Authors, title and version match the record; SOURCES.md's date is the cited version's date.

## R06 S42, draft l.467 (References), reference entry: **OK**

- Draft entry: - [S42] P.-B. Peters, Price's law for scalar waves on 1+4 dimensional subextremal Myers–Perry spacetimes, arXiv:2610.33812v1.
- Passage: arXiv abstract page of the cited version: title "Price's law for scalar waves on 1+4 dimensional subextremal Myers-Perry spacetimes"; authors Peters, Pieter-Bart; versions v1 Sat, 24 Oct 2026; cited v1 = latest v1; SOURCES date 24 Oct 2026 = v1 date: yes
- Check: authors match: yes; title match (normalised): yes
- Note: Authors, title and version match the record; SOURCES.md's date is the cited version's date.

## R07 S43, draft l.469 (References), reference entry: **OK**

- Draft entry: - [S43] J.-K. Zhao, H.-D. Lyu, Separation of gravitational perturbations of Myers–Perry black holes, arXiv:2611.21591v1.
- Passage: arXiv abstract page of the cited version: title "Separation of gravitational perturbations of Myers-Perry black holes"; authors Zhao, Jun-Kun; Lyu, Hong-Da; versions v1 Mon, 16 Nov 2026; cited v1 = latest v1; SOURCES date 16 Nov 2026 = v1 date: yes
- Check: authors match: yes; title match (normalised): yes
- Note: Authors, title and version match the record; SOURCES.md's date is the cited version's date.

## R08 S44, draft l.471 (References), reference entry: **OK**

- Draft entry: - [S44] Y. Guo, M. Hadžić, J. Jang, M. Schrecker, Nonlinear stability of the Larson–Penston collapse, arXiv:2509.12435v1.
- Passage: arXiv abstract page of the cited version: title "Nonlinear stability of the Larson-Penston collapse"; authors Guo, Yan; Hadzic, Mahir; Jang, Juhi; Schrecker, Matthew; versions v1 Mon, 15 Sep 2025; cited v1 = latest v1; SOURCES date 15 Sep 2025 = v1 date: yes
- Check: authors match: yes; title match (normalised): yes
- Note: "Hadžić" as on the paper's title block (l.2); arXiv's metadata has "Hadzic".

## R09 S45, draft l.473 (References), reference entry: **OK**

- Draft entry: - [S45] B. Gwak, Geometrically induced semiclassical limit for quasinormal modes and greybody factors in higher-dimensional near-ultracold spacetimes, arXiv:2610.28367v1.
- Passage: arXiv abstract page of the cited version: title "Geometrically Induced Semiclassical Limit for Quasinormal Modes and Greybody Factors in Higher-Dimensional Near-Ultracold spacetimes"; authors Gwak, Bogeun; versions v1 Tue, 20 Oct 2026; cited v1 = latest v1; SOURCES date 20 Oct 2026 = v1 date: yes
- Check: authors match: yes; title match (normalised): yes
- Note: arXiv's title is in title case ("Geometrically Induced Semiclassical Limit ..."); case only.

## R10 S46, draft l.475 (References), reference entry: **OK**

- Draft entry: - [S46] M. R. Douglas, J. Gómez-Serrano, F. Lehmann, D. Platt, Y. Qi, A constructive computer-assisted existence proof for a Calabi–Yau metric, arXiv:2611.16908v1.
- Passage: arXiv abstract page of the cited version: title "A constructive computer-assisted existence proof for a Calabi--Yau metric"; authors Douglas, Michael R.; Gómez-Serrano, Javier; Lehmann, Fabian; Platt, Daniel; Qi, Yidi; versions v1 Thu, 12 Nov 2026; cited v1 = latest v1; SOURCES date 12 Nov 2026 = v1 date: yes
- Check: authors match: yes; title match (normalised): yes
- Note: Authors, title and version match the record; SOURCES.md's date is the cited version's date.

## R11 S47, draft l.477 (References), reference entry: **OK**

- Draft entry: - [S47] M. Shavit, Y. Wang, T. Buckmaster, Rigorously certified neural-network computation of nonlinear water waves at near-machine precision, arXiv:2611.07395v1.
- Passage: arXiv abstract page of the cited version: title "Rigorously Certified Neural-Network Computation of Nonlinear Water Waves at Near-Machine Precision"; authors Shavit, Michal; Wang, Yongji; Buckmaster, Tristan; versions v1 Thu, 5 Nov 2026; cited v1 = latest v1; SOURCES date 5 Nov 2026 = v1 date: yes
- Check: authors match: yes; title match (normalised): yes
- Note: arXiv's title is in title case; case only.

## R12 S48, draft l.479 (References), reference entry: **OK**

- Draft entry: - [S48] A. Ishibashi, H. Kodama, Perturbations and stability of static black holes in higher dimensions, arXiv:1103.6148v2.
- Passage: arXiv abstract page of the cited version: title "Perturbations and Stability of Static Black Holes in Higher Dimensions"; authors Ishibashi, Akihiro; Kodama, Hideo; versions v1 Thu, 31 Mar 2011 | v2 Wed, 18 May 2011; cited v2 = latest v2; SOURCES date 18 May 2011 = v2 date: yes
- Check: authors match: yes; title match (normalised): yes
- Note: Authors, title and version match the record; SOURCES.md's date is the cited version's date.

## R13 S49, draft l.481 (References), reference entry: **OK**

- Draft entry: - [S49] E. Giorgi, The linear stability of Reissner–Nordström spacetime: the full subextremal range |Q| < M, arXiv:1910.05630v2.
- Passage: arXiv abstract page of the cited version: title "The linear stability of Reissner-Nordström spacetime: the full subextremal range"; authors Giorgi, Elena; versions v1 Sat, 12 Oct 2019 | v2 Thu, 25 Nov 2021; cited v2 = latest v2; SOURCES date 25 Nov 2021 = v2 date: yes
- Check: authors match: yes; title match (normalised): NO
- Note: The draft's title ends "... the full subextremal range |Q| < M", as on the paper's title page (l.7–8 of the text layer). arXiv's metadata title stops at "range". Either is defensible; the paper's own is used.

## R14 S50, draft l.483 (References), reference entry: **OK**

- Draft entry: - [S50] P.-K. Hung, J. Keller, M.-T. Wang, Linear stability of higher dimensional Schwarzschild spacetimes: decay of master quantities, arXiv:1809.05144v1.
- Passage: arXiv abstract page of the cited version: title "Linear Stability of Higher Dimensional Schwarzschild Spacetimes: Decay of Master Quantities"; authors Hung, Pei-Ken; Keller, Jordan; Wang, Mu-Tao; versions v1 Thu, 13 Sep 2018; cited v1 = latest v1; SOURCES date 13 Sep 2018 = v1 date: yes
- Check: authors match: yes; title match (normalised): yes
- Note: Authors, title and version match the record; SOURCES.md's date is the cited version's date.

## R15 S51, draft l.485 (References), reference entry: **OK**

- Draft entry: - [S51] K. Tanabe, Instability of de Sitter Reissner–Nordström black hole in the 1/D expansion, arXiv:1511.06059v2. - [S52] S. Bhattacharyya, M. Mandlik, S. Minwalla, S. Thakur, A charged membrane paradigm at large D,
- Passage: arXiv abstract page of the cited version: title "Instability of de Sitter Reissner-Nordstrom black hole in the 1/D expansion"; authors Tanabe, Kentaro; versions v1 Thu, 19 Nov 2015 | v2 Tue, 17 May 2016; cited v2 = latest v2; SOURCES date 17 May 2016 = v2 date: yes
- Check: authors match: yes; title match (normalised): yes
- Note: Title, arXiv and paper: "Reissner-Nordstrom" without the umlaut. The draft writes "Reissner–Nordström", a silent correction; keep it or restore the original when formatting.

## R16 S52, draft l.486 (References), reference entry: **OK**

- Draft entry: - [S52] S. Bhattacharyya, M. Mandlik, S. Minwalla, S. Thakur, A charged membrane paradigm at large D, arXiv:1511.03432v2.
- Passage: arXiv abstract page of the cited version: title "A Charged Membrane Paradigm at Large D"; authors Bhattacharyya, Sayantani; Mandlik, Mangesh; Minwalla, Shiraz; Thakur, Somyadip; versions v1 Wed, 11 Nov 2015 | v2 Thu, 10 Mar 2016; cited v2 = latest v2; SOURCES date 10 Mar 2016 = v2 date: yes
- Check: authors match: yes; title match (normalised): yes
- Note: Authors, title and version match the record; SOURCES.md's date is the cited version's date.

## R17 S53, draft l.488 (References), reference entry: **OK**

- Draft entry: - [S53] M. Kimura, T. Tanaka, Stability analysis of black holes by the S-deformation method for coupled systems, arXiv:1809.00795v3.
- Passage: arXiv abstract page of the cited version: title "Stability analysis of black holes by the $S$-deformation method for coupled systems"; authors Kimura, Masashi; Tanaka, Takahiro; versions v1 Tue, 4 Sep 2018 | v2 Wed, 12 Sep 2018 | v3 Fri, 25 Jan 2019; cited v3 = latest v3; SOURCES date 25 Jan 2019 = v3 date: yes
- Check: authors match: yes; title match (normalised): yes
- Note: Authors, title and version match the record; SOURCES.md's date is the cited version's date.

## R18 S54, draft l.490 (References), reference entry: **OK**

- Draft entry: - [S54] D. Gajic, C. Warnick, Quasinormal modes in extremal Reissner–Nordström spacetimes, arXiv:1910.08479v2. - [S55] R. Teixeira da Costa, Mode stability for the Teukolsky equation on extremal and subextremal Kerr spacetimes,
- Passage: arXiv abstract page of the cited version: title "Quasinormal modes in extremal Reissner-Nordström spacetimes"; authors Gajic, Dejan; Warnick, Claude; versions v1 Fri, 18 Oct 2019 | v2 Mon, 7 Jun 2021; cited v2 = latest v2; SOURCES date 7 Jun 2021 = v2 date: yes
- Check: authors match: yes; title match (normalised): yes
- Note: Authors, title and version match the record; SOURCES.md's date is the cited version's date.

## R19 S55, draft l.491 (References), reference entry: **OK**

- Draft entry: - [S55] R. Teixeira da Costa, Mode stability for the Teukolsky equation on extremal and subextremal Kerr spacetimes, arXiv:1910.02854v1.
- Passage: arXiv abstract page of the cited version: title "Mode stability for the Teukolsky equation on extremal and subextremal Kerr spacetimes"; authors da Costa, Rita Teixeira; versions v1 Mon, 7 Oct 2019; cited v1 = latest v1; SOURCES date 7 Oct 2019 = v1 date: yes
- Check: authors match: yes; title match (normalised): yes
- Note: arXiv's metadata lists the author as "da Costa, Rita Teixeira"; "R. Teixeira da Costa" is right.

## R20 S56, draft l.493 (References), reference entry: **OK**

- Draft entry: - [S56] O. Costin, R. Donninger, X. Xia, A proof for the mode stability of a self-similar wave map, arXiv:1411.2947v3.
- Passage: arXiv abstract page of the cited version: title "A Proof for the Mode Stability of a Self-similar Wave Map"; authors Costin, Ovidiu; Donninger, Roland; Xia, Xiaoyue; versions v1 Tue, 11 Nov 2014 | v2 Mon, 24 Nov 2014 | v3 Thu, 18 Dec 2014; cited v3 = latest v3; SOURCES date 18 Dec 2014 = v3 date: yes
- Check: authors match: yes; title match (normalised): yes
- Note: Authors, title and version match the record; SOURCES.md's date is the cited version's date.

## R21 S57, draft l.495 (References), reference entry: **OK**

- Draft entry: - [S57] M. Reiterer, E. Trubowitz, Choptuik's critical spacetime exists, arXiv:1203.3766v1. - [S58] Neko2333OWO, A certified spectral gap and the failure of strong cosmic censorship for linear waves on an
- Passage: arXiv abstract page of the cited version: title "Choptuik's critical spacetime exists"; authors Reiterer, Michael; Trubowitz, Eugene; versions v1 Fri, 16 Mar 2012; cited v1 = latest v1; SOURCES date 16 Mar 2012 = v1 date: yes
- Check: authors match: yes; title match (normalised): yes
- Note: Authors, title and version match the record; SOURCES.md's date is the cited version's date.

## R22 S58, draft l.496 (References), reference entry: **OK**

- Draft entry: - [S58] Neko2333OWO, A certified spectral gap and the failure of strong cosmic censorship for linear waves on an explicit Reissner–Nordström–de Sitter black hole, Zenodo, doi:10.5281/zenodo.24285821 (2026; unrefereed).
- Passage: Zenodo record: title "A certified spectral gap and the failure of strong cosmic censorship for linear waves on an explicit Reissner–Nordström–de Sitter black hole"; creators Neko2333OWO; doi 10.5281/zenodo.24285821, conceptdoi 10.5281/zenodo.24285820, id 24285821, version None, publication_date 2026-11-16, created 2026-11-16, updated 2026-11-16; draft doi 10.5281/zenodo.24285821 = version DOI
- Check: authors match: yes; title match (normalised): yes
- Note: The DOI is the version DOI (concept DOI 10.5281/zenodo.24285820). No version label on the record.

## R23 S59, draft l.498 (References), reference entry: **OK**

- Draft entry: - [S59] Neko2333OWO, Linear instability of an ultraspinning Myers–Perry black hole in seven dimensions: a certified negative canonical energy, Zenodo, doi:10.5281/zenodo.24288754 (2026; unrefereed).
- Passage: Zenodo record: title "Linear instability of an ultraspinning Myers–Perry black hole in seven dimensions: a certified negative canonical energy"; creators Neko2333OWO; doi 10.5281/zenodo.24288754, conceptdoi 10.5281/zenodo.24288753, id 24288754, version None, publication_date 2026-11-16, created 2026-11-16, updated 2026-11-16; draft doi 10.5281/zenodo.24288754 = version DOI
- Check: authors match: yes; title match (normalised): yes
- Note: The DOI is the version DOI (concept DOI 10.5281/zenodo.24288753). No version label on the record.

