"""The verdicts, by hand. One row per \\cite command of v0.8 (K01-K83, in the order of ledger/citations.tsv).
Each row: (row, verdict, basis, {key: line ranges read in that key's text layer}, note).
- verdict: OK, SAYS MORE, ANCHOR OFF or MISQUOTED (the classes of BHM-189).
- basis: READ (read at the source and anchor) or COMPARED (an earlier check of mine covered the same claim at the same
  passage: the wording of v0.8 was compared with the wording checked then, and the anchor was mapped to that passage).
- Line ranges: "a-b;c-d", lines as grep -n counts them in the source's paper.txt.
Page anchors in v0.8 are printed page numbers. For S41 (PDF p.9 = printed 5), S51 (PDF 7 = 6) and S52 (PDF 45-46 =
43-44) they differ from the PDF page index; in every other anchored source they coincide.
REFERENCES: entry notes by key (verdict, note); the rest are OK with the standard note."""

C04 = "BHM-189 C%s"

CITATIONS = [
    ("K01", "SAYS MORE", "READ", {"S5": "1407-1409;1892-1896", "S23": "21-27"},
     "S5 is the reduction for the charged case: two decoupled second-order ODEs for the vector and scalar types "
     "(l.1892-1896), in the canonical Schrödinger form (5.59) (l.1407-1409). S23 is the vacuum case: \"maximally "
     "symmetric vacuum black holes\" (l.21-22). Cited jointly for \"static charged black holes\", [2] says more than "
     "S23 does. Fix: \"... sector by sector [1], extending their reduction for vacuum black holes [2]\"."),
    ("K02", "OK", "READ", {"S6": "21-31;644-647"},
     "\"The higher-dimensional Schwarzschild black holes are therefore stable with respect to scalar perturbations. "
     "This completes the stability analysis\" (l.645-647), at general n; tensor and vector earlier in §2. No anchor in "
     "v0.8; suggested: abstract and p.13."),
    ("K03", "OK", "READ", {"S5": "1878-1881;1903-1907", "S28": "774-776"},
     "S5: for n = 2 the deformed potential is positive; \"When K = 1, λ ≥ 0 and n = 3 ... ṼS− > 0. Hence, in these "
     "special cases, the black hole is stable with respect to any type of perturbation\" (l.1878-1881, p.32); Table I "
     "(p.33). S28: \"the stability ... of a spherically symmetric black hole with charge for D = 4 and D = 5\" "
     "(l.774-776, p.13)."),
    ("K04", "OK", "READ", {"S5": "1899-1907"},
     "Table I (p.33), K = 1, λ = 0, scalar, Q ≠ 0: \"d = 4, 5 OK\" and \"d≥6?\". \"d\" is the spacetime dimension "
     "n + 2 (l.1899-1900)."),
    ("K05", "OK", "COMPARED", {"S28": "740-745"}, "As " + C04 % "01" + ": Table 1 (p.13), \"D ≥ 6 ?\"."),
    ("K06", "OK", "COMPARED", {"S48": "2273-2276"},
     "As " + C04 % "02" + ": quote verbatim (l.2275-2276, p.40); S48 is the authors' review chapter."),
    ("K07", "OK", "COMPARED", {"S28": "705-712;762"},
     "As " + C04 % "03" + ": eqs. (76)-(77) (pp.12-13); at n = 2 the bracket is 2m and l.762 concludes stability for "
     "n = 2. The D = 5 part is cited to S48 p.40 (K08)."),
    ("K08", "OK", "READ", {"S48": "2253-2265"},
     "S48's S-deformation (8.21)-(8.22) (the same Ṽ as S28's (76)-(77)): \"For n = 2, this is positive definite for "
     "m > 0. When K = 1, λ ≥ 0 and n = 3 ... we can show that ṼS− > 0\" (l.2263-2264, p.40). Spherical horizon "
     "(K = 1), λ ≥ 0, D = 5, as v0.8 says."),
    ("K09", "OK", "COMPARED", {"S28": "762-767"},
     "As " + C04 % "04" + ", with its fix taken: both fragments verbatim, \"in general\" kept (l.763, l.767, p.13)."),
    ("K10", "OK", "COMPARED", {"S48": "2263-2265"},
     "The D = 5 special case named in " + C04 % "04" + "'s note (S48 l.2263-2265, p.40)."),
    ("K11", "OK", "READ", {"S5": "1882-1888"},
     "Quote verbatim (l.1886-1887, p.32). The source's sentence: VS− \"has a negative region around the horizon for "
     "the extremal and near extremal cases\" (l.1884-1885), as v0.8 says."),
    ("K12", "OK", "COMPARED", {"S48": "2404-2408"},
     "As " + C04 % "05" + ", with its fix taken: the quote now runs to \"that could apply to generic cases\" "
     "(l.2406-2408, p.43), verbatim."),
    ("K13", "SAYS MORE", "READ", {"S14": "135-138;142-154"},
     "Table I (p.3) is \"l = 2 fundamental frequencies of gravitational perturbations of scalar type V−\" (l.142): one "
     "mode per entry, the fundamental. v0.8 says they \"computed the ℓ = 2 quasinormal modes\" and \"found every computed "
     "mode damped\". The rest holds: D = 5-11, q = Q/Qext up to 0.98 (D = 5-8) and 0.9 (D = 9-11), every Im ω < 0, and the "
     "values are for pure RN, ρ = 0 (l.135-137; the caption says RNdS). Fix: \"computed the fundamental ℓ = 2 "
     "quasinormal mode ... and found it damped at every computed point\"."),
    ("K14", "OK", "COMPARED", {"S26": "18-23"},
     "As my check of 2026-10-22 (target_A.md, 1309.7667, abstract l.22-23): \"numerical evidence that ... "
     "asymptotically flat extremally charged Reissner-Nordstrøm black holes are stable for all D\" (l.21-23). No anchor "
     "in v0.8; suggested: abstract."),
    ("K15", "OK", "READ", {"S32": "867-878;968-975", "S14": "142-154"},
     "Compared at every point both tables give (ℓ = 2, fundamental): D = 7, q = 0, 0.1, ..., 0.9 (S32 Table 5) and 0.98, "
     "and D = 6, 0.98 (S32 Table 7). S32's values, rounded to S14's three decimals, equal S14's at 7 of the 12 points; at "
     "the other 5 they differ by one unit in the third decimal (largest difference 0.0015, D = 7, q = 0.98: S14 1.107 − "
     "0.380i, S32 1.105518 − 0.379003i). \"Match\" holds to about 0.1%; \"agree to within 0.002\" would be exact. Note: "
     "my check of 2026-11-10 (zmode_litcheck, Q5) found S32 disagreeing with Konoplya–Zhidenko hep-th/0703231 (S8) at "
     "Q > 0; S14 is a different paper and agrees with S32. No anchor in v0.8; suggested: S32 Tables 5 and 7."),
    ("K16", "OK", "READ", {"S14": "142-154"}, "As K15."),
    ("K17", "OK", "COMPARED", {"S52": "77;2438-2439"},
     "\"light quasinormal modes\" is S52's term (section 5, \"Light quasinormal spectrum\", l.77), as in "
     + C04 % "06" + "'s note."),
    ("K18", "OK", "COMPARED", {"S52": "2466-2479"},
     "As " + C04 % "06" + ", with its fix taken (light modes, at leading order). pp.43-44 are printed numbers: printed "
     "43 ends at l.2476, and the passage l.2477-2479 opens printed 44 (PDF 46)."),
    ("K19", "OK", "COMPARED", {"S51": "324-330"},
     "As " + C04 % "07" + ", with its fix taken. p.6 is printed (PDF p.7)."),
    ("K20", "OK", "READ", {"S9": "15-21;447-458"},
     "S9 finds S by solving numerically the equation for which the deformed potential vanishes (abstract l.18-21), "
     "i.e. S = −Φ′/Φ for a zero-energy solution Φ; l.447-458 tie it to the nodeless ground state at the onset. The "
     "explicit \"zero-energy solution without zeros\" form is S27's (K21)."),
    ("K21", "OK", "READ", {"S27": "86-95;154-158"},
     "S = −Φ′E=0/ΦE=0 (eq. 6), and \"the existence of ΦE=0 which does not have zero anywhere implies the existence of a "
     "regular solution\" (l.86-94, pp.2-3)."),
    ("K22", "OK", "COMPARED", {"S53": "525-530"}, "As " + C04 % "08" + "; wording unchanged; p.11 = l.525-530."),
    ("K23", "OK", "COMPARED", {"S49": "20-30"}, "As " + C04 % "09" + "."),
    ("K24", "OK", "COMPARED", {"S50": "26-29"}, "As " + C04 % "10" + ": quote verbatim."),
    ("K25", "OK", "COMPARED", {"S40": "7-12"},
     "As " + C04 % "11" + ", with its fix taken (\"subextremal\"); \"for the radial ODEs obtained after angular "
     "separation, we prove mode stability on the real axis, i.e., the absence of quasinormal modes with real "
     "frequencies\" (l.11-12)."),
    ("K26", "OK", "COMPARED", {"S41": "444-445"},
     "As " + C04 % "12" + ": quote verbatim. p.5 is printed (PDF p.9)."),
    ("K27", "OK", "READ", {"S41": "1-12"}, "A date reference (\"At the time of\"); S41 v2 is of 3 Aug 2026."),
    ("K28", "OK", "COMPARED", {"S41": "538-541"},
     "As " + C04 % "13" + ", with its fix taken (\"with a further result for small mass cited there\"): quote "
     "verbatim. p.7 is printed (PDF p.11)."),
    ("K29", "SAYS MORE", "READ", {"S43": "11-13;22-27"},
     "\"two independent spins\" holds (l.11-12, l.27). But \"after the singly spinning case\": the abstract says the "
     "earlier separation (Santos) is \"for perturbations with mψ = 0 and even parity under ψ → −ψ\" (l.24-25), one "
     "symmetry sector; v2 of 19 Nov says the same in its introduction: singly spinning MP \"were separated for modes "
     "preserving the transverse-sphere symmetry\" (v2 p.1). Fix: \"after a symmetry sector of the singly spinning "
     "case\". Santos (arXiv:2610.18956) is S43's [12] and is not in v0.8's references."),
    ("K30", "OK", "COMPARED", {"S42": "163-164;446-447"}, "As " + C04 % "15" + ": quote verbatim."),
    ("K31", "OK", "COMPARED", {"S37": "8-15"},
     "As " + C04 % "16" + ", with its fix taken (\"in the full subextremal range\"); the source says \"no nontrivial "
     "outgoing modes with Im σ ≥ 0\" (l.12) and \"Part of the proof is computer-assisted\" (l.14-15)."),
    ("K32", "OK", "COMPARED", {"S37": "126-128"}, "As " + C04 % "17" + "."),
    ("K33", "OK", "COMPARED", {"S37": "1338"}, "As " + C04 % "18" + ": quote verbatim."),
    ("K34", "OK", "COMPARED", {"S39": "138-141;1844-1848"},
     "As " + C04 % "19" + ", with its fix taken: domain, angular branch and Riemann sheet (l.1846-1848)."),
    ("K35", "OK", "COMPARED", {"S38": "19-33"}, "As " + C04 % "20" + "."),
    ("K36", "OK", "COMPARED", {"S58": "8-22"}, "As " + C04 % "21" + "."),
    ("K37", "OK", "COMPARED", {"S59": "8-22"}, "As " + C04 % "22" + "."),
    ("K38", "OK", "COMPARED", {"S57": "9-18"}, "As " + C04 % "23" + "."),
    ("K39", "OK", "COMPARED", {"S56": "6-7;96-103"},
     "As " + C04 % "24" + ", with its fix taken (abstract and p.2). \"with computer algebra\": all computations in "
     "rational numbers, \"without the aid of some computer algebra system\" unrealistic (l.101-103)."),
    ("K40", "OK", "COMPARED", {"S44": "16-21"}, "As " + C04 % "25" + "."),
    ("K41", "OK", "COMPARED", {"S46": "14-19"},
     "As " + C04 % "26" + ". v0.8 now says \"computer-assisted proofs\" (v0.4: \"certified computation\"): S46 is \"a "
     "constructive computer-assisted existence proof\" (title; l.14-19), so this holds."),
    ("K42", "SAYS MORE", "READ", {"S47": "98-108;736-742;840-844"},
     "v0.8 now says \"Computer-assisted proofs are also in use ... with formal verification in Lean, for nonlinear "
     "water waves computed by neural networks\" (v0.4: \"certified computation\"). S47 certifies a uniform bound on the "
     "residual of one machine-learned candidate (p.3, l.100-108), and says: \"This is a uniform residual theorem for a "
     "supplied finite series. It is not an existence or uniqueness theorem for an exact nearby water wave\" (l.738-739, "
     "p.12; also l.840-844, p.14). Fix: keep \"proofs\" for S46 only, e.g. \"... in geometric analysis [28] and, with "
     "formal verification in Lean, to certify the residual of a neural-network approximation of a nonlinear water wave "
     "[29, p. 3]\"."),
    ("K43", "OK", "READ", {"S33": "395-399"},
     "Read on the rendered page (PDF p.8, printed 7). Ψ2 = 2Bℓ(ℓ+1)√((2ℓ+1)(ℓ−1)) r^(1−ℓ)(1 − M/r)^(−ℓ)/((ℓ−1)r + 2M). "
     "With r_H = M at q = 1, v0.8's D = 4 form of u_0 equals Ψ2 times a constant, and Ψ2 ~ r^(−ℓ) decays "
     "(tools/zm_check.py). Ψ2 solves Kodama–Ishibashi's −f(fΨ′)′ + V_S−Ψ = 0 exactly at D = 4, q = 1. Note: S33's own "
     "printed V2 (eq. 4.18) is the negative of that potential (it would tend to −ℓ(ℓ+1)/r² at large r): a sign slip in "
     "S33's (4.18), not in v0.8, which cites only (4.14)."),
    ("K44", "OK", "READ", {"S5": "1903-1907"}, "As K04."),
    ("K45", "OK", "COMPARED", {"S28": "740-745"}, "As " + C04 % "01" + "."),
    ("K46", "OK", "COMPARED", {"S48": "2273-2276"}, "As " + C04 % "02" + "."),
    ("K47", "OK", "COMPARED", {"S37": "8-15"}, "As " + C04 % "28" + "."),
    ("K48", "OK", "READ", {"S5": "248-255"}, "The background (2.18)-(2.19), p.5."),
    ("K49", "OK", "READ", {"S5": "207;219-221"},
     "(2.12) is the Einstein equation with Λ; (2.14) defines λ := 2Λ/(n(n + 1)) (p.4)."),
    ("K50", "OK", "READ", {"S5": "119;125-131"},
     "K is the sectional curvature of the horizon's Einstein space Kn, normalised to 0, ±1 (l.125-131, p.3)."),
    ("K51", "OK", "READ", {"S5": "248-251"},
     "(2.18), p.5. In S5, dσn² is the metric of an Einstein space Kn (l.119); for K = 1 and the maximally symmetric case "
     "it is the round S^n, as v0.8 says."),
    ("K52", "OK", "READ", {"S5": "253-255"}, "(2.19) as written, p.5."),
    ("K53", "OK", "READ", {"S5": "253-255"},
     "M and Q are (2.19)'s parameters. |Q| = M as extremality at λ = 0, K = 1 follows from (2.19) (a double root of f)."),
    ("K54", "OK", "READ", {"S5": "1205"}, "m = k² − nK (5.39), p.21; at K = 1 and k² = ℓ(ℓ + n − 1), m = (ℓ − 1)(ℓ + n)."),
    ("K55", "OK", "READ", {"S5": "1402-1406;1412-1414"},
     "(5.58) µ² = M² + 4mQ²/(n + 1)² and (5.60) µ = (1 + 2mδ)M, µ > 0 (p.24); so (1 + 2mδ)² = 1 + 4mq²/(n + 1)² and "
     "δ ≥ 0."),
    ("K56", "OK", "READ", {"S5": "1426-1428"}, "(5.62b) as written, p.25."),
    ("K57", "OK", "READ", {"S5": "1445-1462"},
     "(5.63b), p.25, read on the rendered page: the first two lines form [ ... ] y, which vanishes at λ = 0 (y = λr²); "
     "the rest, at K = 1, is Appendix A's display term by term (K81)."),
    ("K58", "OK", "READ", {"S6": "226-239;644-645"},
     "S6: on C0∞(r*), A is symmetric and semi-bounded; for λ ≥ 0 the self-adjoint extension is unique, so positivity "
     "on C0∞ gives positivity of the extension (l.226-239, p.5; used at l.644-645, p.13). That is the direction v0.8 "
     "uses. The H² domain and \"if and only if\" are standard facts, not stated in S6."),
    ("K59", "OK", "READ", {"S6": "205-209;217-219"},
     "A positive self-adjoint ⇒ \"no negative mode solutions that are normalisable\" (l.208-209, 217; pp.4-5)."),
    ("K60", "OK", "READ", {"S5": "1838;1903-1907"},
     "Table I: tensor and vector OK at K = 1, λ = 0, Q ≠ 0 (p.33); \"the electromagnetic mode Φ+ is always stable\" "
     "(l.1838, p.31)."),
    ("K61", "OK", "READ", {"S5": "818-822"},
     "\"A perturbation corresponding to such a constant mode represents a variation of the parameters λ, M, and Q of "
     "the background\" (l.819-821, p.15): k² = 0 is ℓ = 0."),
    ("K62", "OK", "READ", {"S5": "2509;2518-2523"},
     "For k² = n and K = 1 (ℓ = 1): \"Φ+ is gauge-invariant. In contrast ... Φ− is not gauge-invariant\" "
     "(l.2518-2523, p.42). The source adds that the master equation for Φ− is gauge-invariant."),
    ("K63", "OK", "READ", {"S33": "395-399"}, "As K43."),
    ("K64", "OK", "READ", {"S6": "478-492"},
     "(2.18)-(2.20), p.10: (Φ, AΦ) = −[Φ* D̃Φ]boundary + ∫(|D̃Φ|² + Ṽ|Φ|²) with D̃ = d/dr* + S and Ṽ = V + f dS/dr − S²; "
     "the boundary term vanishes on C0∞. Lemma 1 is this identity (f dS/dr = dS/dr*)."),
    ("K65", "OK", "READ", {"S6": "620-627;644-647"},
     "Stable at every n (l.644-647). The negative region at D = 10 is v0.8's own statement; S6 notes VS is not positive "
     "definite in general (l.622, l.625)."),
    ("K66", "OK", "READ", {}, "Names the source of a transcription; no claim about S5's content."),
    ("K67", "OK", "READ", {}, "Refers back to §2's use of S5 (K60)."),
    ("K68", "OK", "COMPARED", {"S52": "2466-2479"}, "As " + C04 % "29" + ", with its fix taken; as K18."),
    ("K69", "OK", "COMPARED", {"S51": "324-330"}, "As " + C04 % "30" + ", with its fix taken; as K19."),
    ("K70", "OK", "READ", {"S14": "8-12"},
     "\"gravitationally unstable for large values of the electric charge and cosmological constant in D ≥ 7\" "
     "(abstract)."),
    ("K71", "OK", "COMPARED", {"S51": "26-30"}, "As " + C04 % "31" + "."),
    ("K72", "OK", "COMPARED", {"S45": "18-27"}, "As " + C04 % "32" + "."),
    ("K73", "OK", "COMPARED", {"S58": "8-12;16-17"}, "As " + C04 % "33" + "."),
    ("K74", "OK", "COMPARED", {"S54": "8-18;23-24"}, "As " + C04 % "34" + "."),
    ("K75", "OK", "COMPARED", {"S55": "15-26"}, "As " + C04 % "35" + "."),
    ("K76", "OK", "READ", {"S31": "22-29"},
     "The Aretakis instability of non-dilatonic extremal black p-branes, via the near-horizon geometry (abstract). No "
     "anchor in v0.8; suggested: abstract."),
    ("K77", "SAYS MORE", "READ", {"S43": "22-27"}, "As K29 (the same sentence in §8)."),
    ("K78", "OK", "COMPARED", {"S42": "163-164;446-447"}, "As " + C04 % "37" + "."),
    ("K79", "OK", "COMPARED", {"S59": "8-10;17-20"}, "As " + C04 % "38" + "."),
    ("K80", "OK", "READ", {"S5": "1407-1419"},
     "(5.59)-(5.61): f(fΦ′±)′ + (ω² − VS±)Φ± = SS±, with VS± = fU±/(64r²H±²) real (pp.24-25)."),
    ("K81", "OK", "READ", {"S5": "1445-1462"},
     "Appendix A's U− equals (5.63b) at y = 0, K = 1, term by term, read on the rendered page (see K57)."),
    ("K82", "OK", "READ", {"S5": "1426-1428"}, "As K56."),
    ("K83", "OK", "READ", {}, "About the code's transcription of S5; no claim about S5's content beyond K81."),
]

REFERENCES = {
    "S31": ("OK", "The v3 PDF's title page reads \"On the Aretakis Instability of Extremal Black Branes\" (l.6), as the "
                  "entry does; arXiv's metadata for v3 gives \"You've got a Freund--Rubin in Me: The Aretakis Instability "
                  "of Extremal Black Branes\", which is what arXiv and INSPIRE listings show."),
    "S43": ("OK", "v1 as cited is right, but a v2 was posted on 19 Nov 2026 (arXiv API: updated 2026-11-19T18:59:27Z), "
                  "with a new abstract that no longer mentions the singly spinning limit; it is in v2's introduction "
                  "(p.1). Keep v1 deliberately, or cite v2 and move the anchor."),
    "S49": ("OK", "As BHM-189 R13: \"|Q| < M\" is on the paper's title page but not in arXiv's metadata title."),
    "S51": ("OK", "As BHM-189 R15: the original title has no umlaut (\"Reissner-Nordstrom\")."),
    "S26": ("OK", "The original title spells \"Reissner-Nordstrøm(-de Sitter)\" (SOURCES.md too); v0.8 normalises to "
                  "\"Nordström\"."),
    "S37": ("OK", "BHM-189 R01's fix is taken: version DOI 10.5281/zenodo.24146364 (v1), with the concept DOI named; the "
                  "record is still the latest version (is_last)."),
}
