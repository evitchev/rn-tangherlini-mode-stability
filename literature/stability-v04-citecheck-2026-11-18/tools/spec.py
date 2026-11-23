"""The verdicts of the citation check, by hand. build.py extracts the passages, checks the draft's quotes and writes the
ledger. Fields: S, draft line(s), section, anchor as given, verdict, lines the passage is taken from (";" separates
ranges), a manual passage where the layout cannot be read line by line (else ""), the draft's quoted words (to be found
verbatim in the passage, "" if none), note."""

CITATIONS = [
    ("S28", "50", "§1", "Table 1", "OK", "740-745", "Table 1: Stability of static black holes. [Columns: Tensor, Vector, "
     "Scalar, each split Q = 0 | Q ≠ 0. Row K = 1, λ = 0, column Scalar, Q ≠ 0:] D = 4, 5 OK [/] D ≥ 6 ?", "",
     "Outside the listed scope (message 18 names S28's eqs. (76)–(77) and l.762–767); checked because it is an anchored S28 "
     "citation in §1. The text layer renders ≠ as \"6=\"; the table cell was read from the layout and the PDF."),
    ("S48", "52", "§1", "l.2275–2276", "OK", "2275-2276", "",
     "for scalar type perturbation, we were not able to prove even the stability of asymptotically flat black holes with "
     "charge in generic dimensions",
     "Quote verbatim. S48 is a review chapter (l.20–21: \"In this chapter ... We first review\"), so \"In their review\" "
     "holds. The source sentence goes on: \"due to the existence of a negative region in the effective potential around "
     "the horizon in the extremal and near extremal cases\" (l.2277–2278), which the draft's next sentence paraphrases."),
    ("S28", "57", "§1", "eqs. (76)–(77)", "OK", "705-712;762",
     "By the similar S-deformation S = (f/h) dh/dr ; h = r^{n/2−1} H− , (76) the effective potential VS− for Φ− is "
     "transformed to ṼS− = k²f/(2r²H−) [2m − (n + 1)(n − 2)(1 + mδ)x] . (77) [...] Hence, the gravitational mode is "
     "also stable for n = 2.", "",
     "Fractions reassembled from the display layout of l.705–712. At n = 2 the bracket in (77) is 2m, and l.762 draws "
     "the conclusion for n = 2 (D = 4). So \"the S-deformation that proves D = 4\" is (76)–(77)."),
    ("S28", "58-59", "§1", "l.762–767", "SAYS MORE", "762-767", "", "except for some special cases",
     "Quote verbatim. But the draft's \"leaves a negative region near the horizon for n > 2\" drops the source's \"in "
     "general\" (l.763: \"for n > 2, ṼS− becomes negative near the horizon in general\"). n = 3 (D = 5) is one of the "
     "special cases: S28's summary establishes the charged case \"for D = 4 and D = 5\" (l.774–776), and S48 l.2263–2265 "
     "says ṼS− > 0 for K = 1, λ ≥ 0, n = 3. As written, the sentence conflicts with the draft's own l.49 (stability for "
     "D = 4 and 5). Fix: restore \"in general\", or say the negative region appears for n ≥ 4 in general, D = 5 being "
     "one of the special cases."),
    ("S48", "61-62", "§1", "l.2406–2408", "SAYS MORE", "2404-2408", "",
     "there does not seem to be a systematic method to find such a desirable function S",
     "Quote verbatim, but it stops before the restrictive clause that ends the source's sentence: \"... such a desirable "
     "function S that could apply to generic cases\" (l.2407–2408). Without it the quote reads as no systematic method at "
     "all. Fix: quote through \"that could apply to generic cases\"."),
    ("S52", "69-70", "§1", "l.2476–2479", "SAYS MORE", "2477-2479", "", "",
     "l.2476 is the page number (\"– 43 –\"); the passage is l.2477–2479. The modes are the light quasinormal modes of "
     "the charged membrane: section 5 is \"Light quasinormal spectrum o[f] the RN black hole\" (contents, l.77), and "
     "(5.22) is \"our final result for the light quasinormal mode frequencies associated with shape fluctuations\" "
     "(l.2438–2439), at leading order in large D (l.2425–2426, l.2431), in flat space. The draft's \"the quasinormal "
     "modes of the charged black hole with Λ = 0 decay\" covers all quasinormal modes; heavy (O(D)) modes are not in "
     "the membrane description. Fix: \"the light quasinormal modes\" (one word)."),
    ("S51", "69-70", "§1", "l.326–330", "SAYS MORE", "326-330", "", "",
     "Passage l.327–330 (l.326 finishes the previous sentence). The ω± of (3.8) are modes of the leading-order large-D "
     "effective equations (l.93, l.296–319), and at L → ∞ they \"reproduce the quasinormal modes of Reissner-Nordstrom "
     "black hole obtained in [12]\", where [12] is S52 (l.482). So the same scope note as the S52 row applies; the "
     "same one-word fix covers both."),
    ("S53", "74", "§1", "l.524–531", "OK", "525-530", "", "",
     "l.524 is blank and l.531 starts the next sentence; the passage is l.525–530. The two coupled systems are the "
     "Schwarzschild black hole in dynamical Chern–Simons gravity and a charged Kaluza–Klein black hole (l.528–529)."),
    ("S49", "77", "§1", "l.20–30", "OK", "20-30", "", "",
     "\"settle the problem of linear stability to gravitational and electromagnetic perturbations of "
     "Reissner-Nordström ... in the full subextremal range |Q| < M\" (l.28–30). Linear stability with boundedness and "
     "decay (l.26–27) is beyond mode stability, as the draft says."),
    ("S50", "79", "§1", "l.26–29", "OK", "26-29", "", "to a uniform boundedness estimate in all dimensions",
     "Quote verbatim (across l.27–28). \"decay for D ≤ 6\" is \"decay estimates in the case of six or fewer spacetime "
     "dimensions\" (l.28–29)."),
    ("S40", "81", "§1", "l.7–12", "SAYS MORE", "7-12", "", "",
     "Supported except for one qualifier: the source is about \"the subextremal Kerr–Newman black hole\" (l.7). The "
     "draft says \"For Kerr–Newman\", which reads as including extremal Kerr–Newman, a case the draft treats as "
     "distinct elsewhere (§7, Extremality). Fix: \"For subextremal Kerr–Newman\"."),
    ("S41", "83", "§1", "l.444–445", "OK", "444-445", "", "as a black box",
     "Quote verbatim. The result used as a black box is Andersson–Häfner–Whiting's mode stability for linearized "
     "gravity [AHW24] (l.444), if the draft wants to credit it."),
    ("S41", "84", "§1", "l.539–541", "SAYS MORE", "538-541", "",
     "remains an open problem except in the slow-rotation regime",
     "Quote verbatim, but the source's sentence continues \"(see also [Hin25b] for the small mass regime)\" (l.541), a "
     "second regime where Kerr–de Sitter mode stability is known; [Hin25b] is Hintz, \"Mode stability and shallow "
     "quasinormal modes of Kerr–de Sitter black holes away from extremality\" (l.24885). Fix: add the small-mass regime "
     "after the quote. \"As of that paper\" correctly dates the statement (v2, 3 Aug 2026; S37 is later)."),
    ("S43", "86", "§1", "l.11–26", "OK", "11-16;22-27", "", "",
     "The separation is for five-dimensional asymptotically flat Myers–Perry \"with two unequal spins\" and arbitrary "
     "azimuthal numbers (l.11–13). The source itself names an earlier special case: \"In the singly spinning limit, we "
     "recover Santos's angular operators and radial equation for perturbations with mψ = 0 and even parity\" "
     "(l.24–25). So \"separated only recently\" holds for the general case. If precision is wanted: \"separated in "
     "general only recently\". (l.17–21 are the arXiv margin stamp and blank lines.)"),
    ("S42", "87", "§1", "l.163–164, l.446–447", "OK", "163-164;446-447", "", "has not been shown to hold yet",
     "Quote verbatim (l.446). What has not been shown is mode stability \"down to the real axis Im σ = 0\" (l.446–447), "
     "as the draft says; the main theorem is \"still condition[al] on the assumption of real mode stability for the "
     "wave equation\" (l.163–164)."),
    ("S37", "91", "§1", "l.10–15", "SAYS MORE", "8-15", "", "",
     "The claim is for Kerr–de Sitter \"in the full subextremal range\" (l.8–10) and is that there are \"no nontrivial "
     "outgoing modes with Im σ ≥ 0\" (l.12). The draft drops \"subextremal\" (\"mode stability for Kerr–de Sitter\"). "
     "Dropping \"nontrivial\" is harmless. Fix: \"for subextremal Kerr–de Sitter\". The anchor could start at l.8, "
     "where the subextremal range is stated."),
    ("S37", "91-92", "§1", "l.126–128", "OK", "126-128", "", "",
     "\"All are exact except C9, which uses floating-point arithmetic with rigorous error bounds\" (the text layer "
     "drops the fl ligature: \"oating\"). The source says \"computer-assisted steps\"; the draft's \"certificates\" is "
     "a fair paraphrase."),
    ("S37", "93", "§1", "l.1338", "OK", "1338", "", "No human expert has yet checked the argument",
     "Quote verbatim, in the author's first-person statement on AI use (l.1330–1339). \"Unrefereed preprint\": the "
     "Zenodo record's resource type is publication/preprint."),
    ("S39", "95", "§1", "l.139–141, l.1845–1848", "SAYS MORE", "138-141;1844-1848",
     "[left column, l.138–141:] these families; it is not a damping threshold or a claim to ex- haust all Riemann sheets. "
     "A certified contour establishes ex- actly one simple DM in the stated (3, 3) domain, while critical [...] [right "
     "column, l.1844–1848:] with angular isolation and the absence of normalization poles, this proves that D33 "
     "contains exactly the one simple QNM shown in Fig. 10a. The statement applies to this domain, an- gular branch, and "
     "Riemann sheet.", "",
     "Two-column layout; columns separated by hand. The anchors are right. The draft keeps \"one bounded frequency "
     "domain\" but drops the other two qualifiers: \"The statement applies to this domain, angular branch, and Riemann "
     "sheet\" (l.1846–1848; also the abstract, l.36–37). Fix: \"in one bounded frequency domain, on one angular branch "
     "and Riemann sheet\". \"within a numerical survey\" is supported by the abstract (\"the survey extending through "
     "the 41st overtone\", l.28)."),
    ("S38", "97", "§1", "l.19–33", "OK", "19-33", "", "",
     "\"We give a computer assisted existence proof for a non-Schwarzschild solution\" (l.21–22): static, asymptotically "
     "flat, at one horizon radius and nearby (l.19, l.22–23, l.31–32); existence, not uniqueness (l.33)."),
    ("S58", "99", "§1", "l.8–22", "OK", "8-22", "", "",
     "Massless scalar wave equation (a test field) on one subextremal Reissner–Nordström–de Sitter black hole with "
     "rational horizon radii (l.8–11); interval-arithmetic certificates (l.17–22). The text layer renders the bound as "
     "\"− 35 κ−\", i.e. −(3/5)κ− (l.11)."),
    ("S59", "100", "§1", "l.8–22", "OK", "8-22", "", "",
     "Singly spinning, D = 7, a/r+ = 8, linear instability in the sense of Prabhu and Wald (l.8–10), by a "
     "computer-assisted certificate (l.18–20). The author states that the sign \"relies on the exactness of the "
     "symbolic derivation\" (l.20–21)."),
    ("S57", "102", "§1", "l.9–18", "OK", "9-18", "", "",
     "\"The proof is computer assisted\" (l.15). The source proves existence of \"a real analytic solution, that we "
     "interpret as the solution observed by Choptuik\", on \"an open neighborhood of the past light cone of the "
     "singularity\" (l.12–15). The draft's sentence matches the paper's title, \"Choptuik's critical spacetime "
     "exists\"; the two qualifiers could be added if wanted."),
    ("S56", "103", "§1", "l.6–14", "ANCHOR OFF", "6-7;100-103", "", "",
     "The abstract (l.6–14) gives \"a rigorous proof for its mode stability\" (l.7) but says nothing about computer "
     "assistance. That is at l.100–103: all computations are in rational numbers, free of rounding errors, and \"it "
     "seems unrealistic to perform all our computations without the aid of some computer algebra system\". Right "
     "lines: l.6–7 and l.100–103."),
    ("S44", "104", "§1", "l.16–21", "OK", "16-21", "", "",
     "\"the proof of mode-stability for the non self-adjoint spectral problem ... use rigorous computer-assisted "
     "techniques in the intermediate regime\" (l.16–21). It is mode stability of the Larson–Penston solution of the "
     "isothermal Euler–Poisson system (l.11–12)."),
    ("S46", "105", "§1", "(none)", "OK", "14-19", "", "",
     "No anchor in the draft. Supported at l.14–19: a rigorous, constructive existence proof of a Ricci-flat Kähler "
     "metric on the Fermat quartic, with \"verified numerics to get the bounds used by the fixed point theorem\" "
     "(math.DG)."),
    ("S47", "105", "§1", "(none)", "OK", "32-44", "", "",
     "No anchor in the draft. Supported at l.32–44: an interval-arithmetic residual certificate for a machine-learned "
     "water-wave candidate, and a Lean formalisation of \"the deductions connecting the certified numerical bounds to "
     "the final residual theorem\" (l.38–40). The certificate bounds a residual; it is not an existence proof."),
    ("S37", "132", "§1", "(none)", "OK", "10-15", "", "",
     "No anchor in the draft. The disclaimer rests on S37's claim of computer-assisted mode stability (l.10–15). As a "
     "disclaimer it says nothing beyond the source."),
    ("S52", "404", "§7", "l.2476–2479", "SAYS MORE", "2477-2479", "", "",
     "Same passage and same point as the §1 S52 row: these are the light quasinormal modes (l.2438–2439) at leading "
     "order in large D. The draft's \"the modes at Λ = 0 decay\" needs \"light\". l.2476 is the page number."),
    ("S51", "404", "§7", "l.326–330", "SAYS MORE", "326-330", "", "",
     "Same as the §1 S51 row: the modes of the leading-order effective theory, which at L → ∞ reproduce S52's."),
    ("S51", "409", "§7", "l.26–30", "OK", "26-30", "", "",
     "\"the de Sitter Reissner-Nordstrom black hole becomes unstable against gravitational perturbations at larger "
     "charge than a critical charge in a higher dimension\" (l.27–28). l.29–30 concern the zero mode at the critical "
     "charge; the anchor could be l.27–28."),
    ("S45", "410", "§7", "l.18–27", "OK", "18-27", "", "",
     "Massless scalar field on higher-dimensional Reissner–Nordström–de Sitter black holes, quasinormal modes of the "
     "near-ultracold family at leading WKB order (l.18–22). \"Semiclassical\" is the paper's own word (title)."),
    ("S58", "411", "§7", "(none)", "OK", "8-12;16-17", "", "",
     "No anchor in the draft. \"at one parameter point\": the black hole is a single explicit one (l.8–9), and the "
     "paper says \"at this parameter point\" (l.16–17). Suggested anchor: l.8–12, l.16–17."),
    ("S54", "415", "§7", "l.8–24", "OK", "8-18;23-24", "", "",
     "\"QNMs can be interpreted as honest eigenfunctions of generators of time translations\" on Hilbert spaces of "
     "functions \"additionally Gevrey regular at infinity and at the event horizon\" (l.10–15), for extremal "
     "Reissner–Nordström (l.9–10). (l.18–22 are the arXiv margin stamp and blank lines.)"),
    ("S55", "416", "§7", "l.15–26", "OK", "15-26", "", "",
     "\"no exponentially growing modes nor modes on the real axis for the Teukolsky equation on Kerr ... both in the "
     "extremal and subextremal case\" (l.15–17). The anchor could be l.15–17 (and l.22–23 for \"the extremal case ... "
     "has remained an open problem\")."),
    ("S43", "421", "§7", "(none)", "OK", "11-13", "", "",
     "No anchor in the draft. As in the §1 S43 row; suggested anchor l.11–13 (two unequal spins; earlier special case "
     "at l.24–25)."),
    ("S42", "422", "§7", "(none)", "OK", "163-164;446-447", "", "",
     "No anchor in the draft. As in the §1 S42 row; suggested anchor l.163–164, l.446–447."),
    ("S59", "423", "§7", "(none)", "OK", "8-10;17-20", "", "",
     "No anchor in the draft. \"Ultraspinning\" is in the title; a/r+ = 8 (l.9). Suggested anchor l.8–10, l.17–20."),
]

# Reference entries: verdict and note; the record data are filled in from ledger/records_parsed.tsv and bibcheck.tsv.
REFERENCES = {
    "S37": ("BIBLIOGRAPHY",
            "Authors and title match the Zenodo record. The DOI is the concept DOI: 10.5281/zenodo.24146363 resolves to "
            "the latest version (fetching record 24146363 returned record 24146364). Version v1's own DOI is "
            "10.5281/zenodo.24146364 (record 24146364, published 2026-11-11, file kerr_de_sitter_stability.pdf). "
            "\"doi:...24146363 (v1, ...)\" mixes the two. Fix: \"doi:10.5281/zenodo.24146364 (v1, 11 Nov 2026)\", or "
            "keep the concept DOI and drop \"v1\". The two resolve to the same file today, since v1 is the only "
            "version. My own S36 screen gave 24146363 the same way."),
    "S49": ("OK",
            "The draft's title ends \"... the full subextremal range |Q| < M\", as on the paper's title page (l.7–8 "
            "of the text layer). arXiv's metadata title stops at \"range\". Either is defensible; the paper's own is "
            "used."),
    "S51": ("OK",
            "Title, arXiv and paper: \"Reissner-Nordstrom\" without the umlaut. The draft writes \"Reissner–Nordström\", "
            "a silent correction; keep it or restore the original when formatting."),
    "S44": ("OK", "\"Hadžić\" as on the paper's title block (l.2); arXiv's metadata has \"Hadzic\"."),
    "S55": ("OK", "arXiv's metadata lists the author as \"da Costa, Rita Teixeira\"; \"R. Teixeira da Costa\" is right."),
    "S45": ("OK", "arXiv's title is in title case (\"Geometrically Induced Semiclassical Limit ...\"); case only."),
    "S47": ("OK", "arXiv's title is in title case; case only."),
    "S58": ("OK", "The DOI is the version DOI (concept DOI 10.5281/zenodo.24285820). No version label on the record."),
    "S59": ("OK", "The DOI is the version DOI (concept DOI 10.5281/zenodo.24288753). No version label on the record."),
}
