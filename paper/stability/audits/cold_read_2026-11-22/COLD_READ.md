# Cold read of the stability paper: language and notation

*2026-11-22 (EST). Registry BHM-199. Written by the session that received the brief
`outbox/2026-11-22-to-cold-reader.md` (SHA-256 `5ef47e85925fe81f6beb1f159f1785e4605dd085c2e9d4df255792b1210d700d`,
checked) from the lead session.*

## 0. What was read, and how cold this read is

- **Read:** only `stability_2026-11-22.pdf` in this folder, 15 pages. Its SHA-256 was checked before reading:
  `bc5d550ee4a86d1f76177750f3214bef384a786b3226d260a5ae1512da4e48fb`, as the brief gives it.
- **How:** one `pdftotext -layout` extraction, and pages 1–14 viewed as rendered pages with the Read tool, so that
  the formulae were read as typeset. Page 15 (references only) was read as text.
- **Not opened:** the LaTeX source, results, registry, rules, notes, any memory file. No web, no code. The only
  commands run were `sha256sum` (PDF, brief, this report), `pdftotext`, `ls` of this folder and `date`; and,
  after the list was written, `wc`, `grep` and `awk` on this report and one `git status --short`, which showed
  file names only (among them the lead's staged `paper/stability/tex/LANGUAGE_PASS.md`). Nothing was opened.
- **Reader:** an outside referee's role, gr-qc or math.AP. Page numbers are the PDF's. Reference numbers such as [1]
  are the PDF's own. Formulae in quotations are transcribed from the typeset page into plain text.
- **Limits on "cold".** This session was not empty when the brief arrived, and the lead should weigh three things:
  1. The harness had loaded the project's memory **index** (eleven one-line entries). One line says that the
     operator wants standard terms and every symbol defined at first use. Others contain project words such as
     "kit", "registration", "controls", "seat".
  2. The harness had shown five recent commit titles. They told me that the operator had already asked about
     "a gate of the step named", that the labels of the paper and the letters of Table 1 were under discussion, and
     that Λ, λ and the integrals had just been fixed. Items below that overlap with these are marked **†**: they are
     not independent findings.
  3. The session cannot see its own name, so it cannot confirm that it is the `bh-modes-4e` the brief addresses.
     The message was delivered to it.
- **Model.** The session started on Claude Opus 5.5; the operator switched it to Claude Fable 5.2 with `/model`
  before the brief arrived, and to effort `xhigh` during the reading. The whole list was compiled after both
  switches. The evidence is the two command outputs in this session's transcript, not this sentence.
- **Kinds**, as in the brief: **1** a term that is not standard (a coinage, or software or lab vocabulary);
  **2** used before defined, or never defined; **3** two meanings; **4** an unclear sentence, or one that refers
  to something it does not explain; **5** a label or annotation that a mathematics paper would not carry.
- **Out of scope and not judged:** whether the mathematics is correct, the citations, the typesetting, the draft
  banner and the red [OPEN: …] items. A few suggestions below rest on my own reading of a formula; each says so.

## 1. The list, in page order

### Title and abstract (p. 1)

**1.** p. 1 (title) · kind 3 · "the scalar gravitational sector". The same object has five names: "the scalar
gravitational sector" (title), "the scalar-type sector of Kodama and Ishibashi, whose master variable Φ−"
(abstract), "the scalar-type gravitational sector" (p. 1), "the charged scalar-type sector" (p. 4), "the Φ− sector"
(p. 12). The scalar-type sector has two master variables, Φ+ and Φ− (p. 5 mentions Φ+), so "the scalar-type sector
…, whose master variable Φ−" is inexact. And the perturbations of a charged black hole are coupled gravitational
and electromagnetic ones, so "linear gravitational perturbations" (abstract) wants a word. *Suggest:* one name,
defined once: "the Φ− equation of the scalar-type sector, the one that reduces to the gravitational scalar-type
master equation as Q → 0". Unsure: I believe that this is how [1] distinguishes Φ− from Φ+, but I did not check.

**2.** p. 1 · kind 4 · "S-deformations with explicit rational deformation functions, whose positivity is verified
by Bernstein bounds on boxes". "Whose" points at the deformation functions. What is positive is the deformed
potential (the N of Lemma 2). Same on p. 4: "an S-deformation whose positivity was checked in exact or interval
arithmetic". *Suggest:* "…, for which the deformed potential is shown to be non-negative by …".

**3.** p. 1, 6 · kind 2 · "Bernstein bounds on boxes"; "certified by exact Bernstein bounds with subdivision".
The criterion is stated only on p. 8 ("A box is accepted when all its Bernstein coefficients are positive").
The usual words are "Bernstein expansion", "Bernstein coefficients" and their range-enclosure property. A PDE
referee may not know them. *Suggest:* at first use in §4.2, one sentence: a polynomial is positive on a box
(a product of intervals) if all its coefficients in the Bernstein basis of that box are positive; otherwise the
box is bisected. "Subdivision" (p. 6) and "adaptive bisection" (p. 8) are the same thing; one word.

**4.** p. 1 · kind 3 · "The reduction and the extremal step are machine-checked in Lean." Nothing has been called
a reduction yet. A reader takes it for Kodama and Ishibashi's reduction of the perturbation equations to master
equations, since the paper uses the word that way ("reduced the linear perturbations … to master equations",
p. 1; "Kodama and Ishibashi's reduction to master equations", p. 5), and that one is cited, not machine-checked.
It turns out to mean Proposition 3 (pp. 6, 12: "for Z and for the reduction, a Lean formalisation"). There is a
third use on p. 7: "This step's reduction and cover". *Suggest:* "Proposition 3 (the implication from the
polynomial inequality N ≥ 0 to A ≥ 0) and Theorem 2 are formalised in Lean."

**5.** p. 1, 2 · kind 2 · "the extremal step"; "Our extremal step follows that route". Not defined. It means the
case q = 1 (Theorem 2 with §4.6). On "step" see item 91.

**6.** p. 1 · kind 4 · "At D = 4 it reduces to a known Zerilli–Moncrief function." The Zerilli–Moncrief function
is the master variable. A particular static solution for it is meant, as p. 5 says. *Suggest:* "a known static
solution of the Zerilli–Moncrief equation".

**7.** p. 1, 3, 4 · kind 4 (small) · "an explicit zero-energy solution"; then "the zero-energy solution" (pp. 3, 4).
The equation has a two-dimensional solution space; the definite article needs "that decays at infinity".

### Introduction (pp. 1–4)

**8.** p. 1 · kind 2 · "[1, Table I: “d ≥ 6?”]". The quotation uses d, Kodama and Ishibashi's letter for the
spacetime dimension, where the paper uses D. *Suggest:* "(their d is our D)".

**9.** p. 1 · kind 4 · "That sector's potential V_{S−} has negative regions, so its sign does not decide the
question." "Its sign" is not one sign. *Suggest:* "V_{S−} is negative somewhere for some parameters, so
non-negativity of the potential cannot be used directly."

**10.** p. 1 onward · kind 2 · "S-deformation". Used about twenty times and never defined as a term, even in
§4.1: Lemma 1 gives the identity without naming Ṽ or S. It is standard in the papers that follow [3], so a
gr-qc referee will know it. A PDE referee knows the device as the ground-state (Jacobi, Riccati) substitution.
*Suggest:* in the introduction and at Lemma 1: "Ṽ := V + S′ − S² is called the S-deformation of V, and S the
deformation function."

**11.** p. 2 · kind 4 · "The S-deformation of [4, eqs. (76)–(77)] proves D = 4 and D = 5 [5, p. 40]. For n > 2 it
leaves a negative region near the horizon “in general”". Two stops. (a) "proves D = 4" for "proves stability for
D = 4". The same ellipsis recurs: "Theorem 1 settles D = 6–11" (p. 4), "The last kind is what reaches q = 1"
(p. 6), "q = 1 is Theorem 2's" (p. 7). (b) The bullet changes from D to n in the middle, and n > 2 includes
n = 3, that is D = 5, which the sentence before says is proved.

**12.** p. 2 · kinds 1, 4 · "A horizon-regular S-deformation cannot remove V_{S−}'s negative region near
extremality [1, p. 32]." "Horizon-regular" is a coinage; say "an S that is regular at the horizon". More
important: as written this is a no-go statement, and the paper's own method then seems to do what it forbids
(its S has its pole "outside the exterior", p. 6, so it is regular at the horizon). A referee will stop here.
Say exactly what [1] shows: for which class of S, and in which sense "remove".

**13.** p. 2 · kind 2 · "up to q = 0.98 (0.9 for D = 9–11)". q is used two pages before its definition (p. 4).
Unsure whether the charge variable of [6] has the same normalisation; if not, say whose q this is.

**14.** p. 2 · kind 4 (small) · "the ℓ = 2 quasinormal modes of V_{S−}". Modes of a potential. *Suggest:* "of the
master equation with potential V_{S−}".

**15.** p. 2, 12 · unsure · "the light quasinormal modes …, those the large-D effective theory describes". I am not
sure that "light" is the common word. In much of the large-D literature these are the "decoupled" modes
(frequencies of order D⁰ in units of 1/r_H), against the "non-decoupled" ones. If [9] says "light", keep it and
add "(decoupled)".

**16.** p. 2 · kinds 4, 5 · "(see also [Hin25b] for the small mass regime)", inside a quotation of [17]. It carries
the citation key of another paper's bibliography, which resolves to nothing here. Cut it with an ellipsis, or
resolve it. Also "As of that paper": *suggest* "At the time of [17]".

**17.** p. 2 · kind 3 (small) · "no outgoing modes with Im σ ≥ 0". σ, a frequency in [20], is not introduced, and
on p. 7 σ is a chart variable.

**18.** p. 3 · kind 1 · "with a Lean layer, for computed water waves"; "the eight Lean layers" (pp. 12, 13).
"Layer" is not a word for a formal development. *Suggest:* "a Lean formalisation"; "eight Lean developments" (or
libraries, or files, whichever is true). "Computed water waves": "numerically computed water-wave solutions".

**19.** p. 3, 6, 10 · kinds 1, 2 · "Each certificate is a fail-closed computation in exact rational arithmetic."
"Fail-closed" is a term of security and safety engineering. It is used on p. 3 (twice) and explained on p. 6.
*Suggest:* say it in words once and drop the term: "a computation that reports success only if every inequality
is verified in exact rational arithmetic; any error, time-out or resource limit counts as a failure".

**20.** p. 3 onward · kind 3 · "certificate". In computer-assisted proofs a certificate is a piece of data that
can be checked (a witness). Here it is (i) a computation that runs ("Each certificate is a … computation",
"registered before it ran", "fixed before each certificate ran", p. 6); (ii) a polynomial ("the certificates are
M = NL/µ on O and O′, …", p. 7); (iii) what a piece has ("T3's certificate", p. 10); (iv) a unit of counting
("the 54 certificates", p. 12). *Suggest:* fix one sense. The certificate is the data (the function P and the
list of boxes); "verifying the certificate" is the computation.

**21.** p. 3 onward · kind 1 · "Each was registered before it ran"; "registration"; "as registered"; "PREREG".
Pre-registration is a practice of the empirical sciences. A mathematics reader does not know what is registered
where, nor why it bears on a proof. The explanation is on p. 11. *Suggest:* keep the fact in §6 only, in plain
words: "the statement to be verified, the boxes and the acceptance criterion were fixed in a hashed file before
each computation ran".

**22.** p. 3, 6, 10, 12 · kind 1 · "carries negative controls"; "negative controls (false inputs that must be
rejected) and tamper drills (deliberate corruptions that must be detected)" (p. 6); "the run's soundness
controls" (p. 10); "Every control ended in its registered form" (p. 12). "Negative control" is laboratory
vocabulary and "tamper drill" is a coinage. There are three names for the controls. The software words are
"negative tests" and "fault injection" (or "mutation testing"). *Suggest:* one sentence in §6: "The verifier was
run on deliberately false statements and on corrupted input files, and rejected all of them."

**23.** p. 3, 9–13 · kind 1 · "re-derived by a second party with independently written code"; "second
party/parties" (six pages). An audit or legal word; and a computation is not "derived". The abstract already has
the plain version: "an independent second check". *Suggest:* "independently re-verified with a separate
implementation".

**24. †** p. 3 · kind 5 · "Labels. Each of our statements carries the kind of evidence behind it: certified, …;
proved (pencil; audited k×), …; machine-checked, …; numerical, …; and cited, …". A mathematics paper does not
label statements by class of evidence. A statement is a theorem (proved in the paper, or cited), a
computer-assisted lemma (with what was computed), or a numerical observation. The scheme produces the theorem
headers of item 43, and annotations such as "Physical reading (cited)" (p. 5), "(numerical, information only)"
(p. 12), "(pencil; motivation only, not used in the proof)" (p. 7; this one is outside the five labels), and
"(from Fable's audit)" (p. 7). *Suggest:* a paragraph "Structure and status of the proof", with one table that
says, for each step, whether it is a pen-and-paper argument, an exact computation or a Lean proof. Then plain
theorem, lemma and proof environments. Inside the scheme:
- kind 1 · "pencil" ("pencil steps", "pencil audit", eight pages): *suggest* "pen-and-paper" or "by hand".
- kind 1 · "audited k×", "audited 2×", "audited twice": *suggest* "checked independently k times". Until p. 13
  the paper does not say that the auditors are AI models; a referee reads "audited" as "checked by a person".
- kind 3 · "certified" is a defined label, and it is also used in its ordinary sense for other people's work
  ("certify a count", "a certified spectral gap", "a certified linear instability", pp. 3, 12, 13). Near-synonyms
  in use: "verified", "VERIFIED", "confirmed", "checked", "accepted", "machine-checked".
- "numerical, information only": *suggest* "numerical evidence, not used in any proof".

**25.** p. 3–4 · kinds 4, 1, 5 · "Relative to the sources read." The heading is unclear; *suggest* "Relation to
the literature". The paragraph is a search protocol in the vocabulary of systematic reviews: "the screen for
this paper", "an earlier screen on the extremal case", "ten seed papers", "Every seed was found again by other
queries", "4,099 unique records", "each read by title", "Not searched", "Not found in these sources"; later
"the literature screens and the watch" (p. 13). "Screen", "seed" and "watch" are not explained, and a reader
cannot tell what "Every seed was found again by other queries" shows. A mathematics paper says "To our
knowledge …" and cites. If the protocol is to stay, an appendix is the place.

### §2 Setting (pp. 4–5)

**26.** p. 4 · kind 2 · "The metric function f = K − λr² − 2M/r^{n−1} + Q²/r^{2(n−1)}". The metric is never
written, so "metric function" refers to nothing, and t (used in e^{κt}, p. 5) and r are never introduced. M and
Q are never described in words. *Suggest:* the line element, ds² = −f dt² + f⁻¹ dr² + r² dΩ_n², and one sentence:
M and Q are the mass and charge parameters in the normalisation of [1], in which extremality is |Q| = M.

**27.** p. 4, 5 · kind 2 · "The horizon is at x_H"; "(r_H, ∞)"; "Units r_H = 1". r_H is never defined.
*Suggest:* "r_H is the largest root of f, and x_H = 2M/r_H^{n−1}".

**28.** p. 4–11 · kind 1 (small) · "the exterior" as a noun: "on the exterior", "outside the exterior", "the closed
exterior", "the interior of the exterior" (p. 10). *Suggest:* define once, "the exterior region r > r_H", and
write the last as "at an interior point r > r_H".

**29.** p. 4 · kind 3 · "we set q := |Q|/M ∈ (0, 1]". But q = 0 is used: "every q ∈ [0, 1]" (pp. 6, 10),
"q ∈ [0, q(µ_lo(ℓ))]" (p. 10), "µ = 1 is q = 0" (p. 5), "negative from q = 0⁺" (pp. 7, 10). *Suggest:* say once
that the computations include q = 0, though Theorem 1 does not need it. For "q = 0⁺" write "for every q > 0"
(or "≥ 0"; the text does not let me tell which).

**30.** p. 4 · kind 2 · "U− is [1, eq. (5.63b)] at λ = 0". The central object of the paper is not written
anywhere: every certificate is about U−, or about N built from it. A reader cannot follow §4 without [1] open.
*Suggest:* write it out, in an appendix if it is long.

**31.** p. 4 · kind 3 · "V_{ℓ,q} := V_{S−} = f U−/(64r²H−²)", then "V is real, continuous and bounded". One
potential has three names (V_{S−}, V_{ℓ,q}, V), the operator two (A_{ℓ,q}, A), and the dependence on n is silent.
On p. 7 H− becomes "H".

**32.** p. 4 · kind 4 · "A_{ℓ,q} := −d²/dr∗² + V_{ℓ,q} on L²(ℝ, dr∗) is the self-adjoint operator of its quadratic
form on C0∞(ℝ). Since V is bounded and r∗ ranges over all of ℝ, it is the only self-adjoint extension from
C0∞(ℝ), so A ≥ 0 there gives A ≥ 0". A PDE referee forms an opinion of the paper at this sentence, and stops
at each clause. "The self-adjoint operator of its quadratic form" and "the only self-adjoint extension from"
are not the usual phrases; "A ≥ 0 there gives A ≥ 0" reads as a tautology; and "A ≥ 0" is never defined.
*Suggest:* "Since V is bounded, −d²/dr∗² + V_{ℓ,q} is essentially self-adjoint on C0∞(ℝ). Let A_{ℓ,q} be its
closure, with domain H²(ℝ). We write A_{ℓ,q} ≥ 0 if ⟨ϕ, A_{ℓ,q}ϕ⟩ ≥ 0 for every ϕ in the domain. Since C0∞(ℝ) is
a core, this holds if and only if the quadratic form is non-negative on C0∞(ℝ)."

**33.** p. 5 · kinds 3, 2 · "A mode is a solution e^{κt}ϕ(r∗) of the master equation with κ > 0 and
0 ≠ ϕ ∈ L²(ℝ, dr∗)". (a) This defines "mode" as an exponentially growing L² mode. Everywhere else the word has
its ordinary senses: "quasinormal modes", "every computed mode damped", "outgoing modes", "the zero mode",
"light … modes". *Suggest:* "a growing mode" or "an unstable mode", and use that in Theorem 1. (b) The master
equation is never written. *Suggest:* ∂_t²Φ− − ∂_{r∗}²Φ− + V_{S−}Φ− = 0. (c) κ is used again on p. 6 with
another meaning (item 53).

**34.** p. 5 · kind 4 (small) · "Such a ϕ lies in A's domain H²(ℝ), since V is bounded, so ϕ″ = (V + κ²)ϕ is in L²
too." The order of the argument is inverted: ϕ″ ∈ L² is the reason why ϕ ∈ H².

**35.** p. 5 · kinds 5, 1, 4 · "Physical reading (cited). With Kodama and Ishibashi's reduction to master
equations, and their results for the tensor and vector types and for Φ+ [1], Theorem 1 says that these black
holes have no exponentially growing linear gravito-electromagnetic mode." The heading carries a label. "Physical
reading": *suggest* "Physical interpretation", or better a Corollary stated as conditional on [1]. The sentence
refers to "their results" without saying what they are, and it says nothing about ℓ = 0 and ℓ = 1 while
concluding for all modes.

**36.** p. 5 · kind 4 · "Units r_H = 1. The form's sign does not depend on the scale." "The form" is the quadratic
form of Theorem 1, which has not been stated yet.

**37.** p. 5 · kind 4 · "The charge is parametrised rationally by µ ∈ [0, 1]: q(µ) := √(1 − w(µ)²)". q(µ) is not
rational in µ; w(µ) and 1 + 2mδ are. And q(µ) depends on n and ℓ through w. That matters later: "q(1/8)",
"q(µ_lo)" and "q(MU1)" are different numbers for each (D, ℓ), which the notation hides. *Suggest:* "µ
parametrises the charge so that δ and q² are rational functions of µ", and q_{n,ℓ}(µ), or a sentence. "µ = 1 is
q = 0": *suggest* "corresponds to".

### §3 Results (p. 5)

**38. †** p. 5 · kind 5 · "Theorem 1 (certified; its pencil steps proved, each audited twice or machine-checked
and audited once; Proposition 3 and Theorem 2 machine-checked, Lean)." and "Theorem 2 (certified;
machine-checked, Lean)." The parenthesis of a theorem carries a name or an attribution. This one carries a
status report, with a forward reference to Proposition 3. *Suggest:* "Theorem 1." and after the statement one
sentence: "The proof is computer-assisted; §… says which steps are computations, which are formalised in Lean,
and which are pen-and-paper."

**39.** p. 5 · kind 2 · "solves the zero-energy master equation of V_{S−}". Write the equation: −u″ + V_{S−}u = 0.
"Zero-energy solution" is standard in physics; a PDE reader says "a positive solution of Au = 0".

**40.** p. 5, 10 · kind 3 · "Y = ρ^{−(n−1)}" (Theorem 2). Y is used again on p. 10 as the variable of the cubic
"3025Y³ − 31521Y² + 99792Y − 68796".

**41.** p. 5 · kind 4 (small) · "What the theorems do not say: anything about decay, about other sectors beyond
the cited results, or about Λ ≠ 0." Clear in content. A paper would write a sentence: "Theorems 1 and 2 give no
decay statement and do not address …".

### §4.1 The S-deformation (p. 6)

**42.** p. 6, 8–12 · kind 5 · "Lemma 1 ([3, eqs. (2.18)–(2.20)]; results/p3/METHOD.md)." A file path of the
repository as a lemma's attribution. Paths, line numbers and JSON field paths recur in the body: the "Source:"
lines of Table 1 ("results/p3/RESULT.md l. 18", "the record's .result.boxes_mu[].P", ".bernstein_leaves"), and
"results/p3/PREREG.md", "results/p3/RESULT_ADDENDUM_1.md l. 16", "results/a2/STAGE_REPORT_ADDENDUM_1.md
l. 32–39", "AUDITS.md", "code/compare_runs.py" on pp. 9–12. *Suggest:* cite the archived repository once, as a
reference with its DOI, and leave the map from statements to files to its README, or to an appendix.

**43.** p. 6 · kind 3 (small) · "So if Ṽ := V + S′ − S² ≥ 0, then A ≥ 0." In Lemma 1 V is any continuous function,
and A was defined for V_{ℓ,q} only.

**44.** p. 6, 7 · kind 2 · "Take S := −fβ with β = (1 − z)P, for a function P of z." β is introduced and never used
again. The subscripts in "f_z", "P_z", and on p. 7 "(log u0)_{r∗}" and "(log u0)_z", are derivatives, which is
not said: p. 4 says only that a prime is d/dr∗. The lemma does not say how regular P is.

**45.** p. 5–6 · kind 5 (numbering) · "Theorem 1", "Theorem 2", "Lemma 1", "Lemma 2", "Proposition 3",
"Lemma U(n)". Three numbering schemes: there is a Theorem 2 and a Lemma 2, Proposition 3 continues the lemmas'
counter, and one lemma has a letter.

**46.** p. 6 · kind 4 · "It is machine-checked in Lean at every n, with the inverse tortoise map's existence as a
hypothesis. That existence is proved (pencil; audited 2×) for q < 1, and machine-checked at q = 1." "The inverse
tortoise map": *suggest* "the inverse r(r∗) of the tortoise coordinate", that is, the statement that r∗ is a
C¹ bijection of (r_H, ∞) onto ℝ. "At every n": "for every n". And the sentence reports that a proof exists. The
proof is not in the paper; nor are those of Lemma 2, Proposition 3, Lemma U and the cover of §4.6. "Proved
(pencil; audited 2×)" therefore points to something the reader cannot see. (This is at the edge of the brief's
scope. I list it because the label refers to something the paper does not contain.)

**47.** p. 6–10 · kind 1 · "The designs P."; "stored designs", "singular designs", "ζ-designs", "u0's own design",
"a closed-form design", "that design rule". "Design" is the project's word for the choice of the function P.
The abstract calls the same objects "deformation functions", which in the literature is S. *Suggest:* "the
function P", "the choice of P"; for "design rule", "the procedure by which P was chosen".

**48.** p. 6 · kind 4 · "We use three kinds, fixed before each certificate ran". When P was fixed has no bearing on
the proof. The paper says so itself on p. 10: "a certificate's validity does not depend on its design".

**49.** p. 6, 8 · kind 2 · "“ζ-designs” P̂/(z + δ_b)^d". There is no ζ in the formula. P̂, δ_b and d are not
defined, and δ_b is not the δ of p. 4. On p. 7 ζ is a chart coordinate (z = µζ), and Table 1 has "designs of
degree 16–32 in z or ζ" (p. 8): which ζ?

**50.** p. 6 · kinds 1, 4 · "singular designs, with a pole at z = −ε < 0 outside the exterior"; "The last kind is
what reaches q = 1. It is admissible because Proposition 3 needs P only on the open interval (0, 1)." (a) A
function that is regular on the whole domain is not "singular" there. *Suggest:* "rational P with a pole at
z = −ε, outside [0, 1]". (b) ε is not defined (how small? does it depend on µ?), and §4.3 uses ε for m^{−1/2}.
(c) If the pole is at z = −ε < 0, then P is regular on the closed interval [0, 1]. Why then does it matter that
Proposition 3 needs only the open interval? Something is left unsaid.

### §4.2–§4.3 (p. 6)

**51.** p. 6, 7 · kind 4 (small) · "positive on a closed box in (z, µ), or in blown-up coordinates". "Blown-up
coordinates" is acceptable (the blow-up of the corner z = µ = 0), but they appear only in §4.5, as "charts", and
the sets covered there are not closed: "(0, 1) × [0, µ1]".

**52.** p. 6, 10, 12 · kind 1 · "No floating point enters a verdict."; "Its verdict as registered is FAIL";
"their recorded verdicts". "Verdict": *suggest* "outcome". "No floating-point arithmetic is used in any
verification." And in "any failed inequality, error or limit gives a rejection" (kind 4): a limit of what?

**53.** p. 6, 8, 10 · kinds 5, 2, 4, 3 · "Large ℓ: Lemma U(n)"; "Write ε = m^{−1/2} and κ = m^{1/2}δ. Then
m^{−3}U− = Pos_n − Neg_n, with nonnegative coefficients and Pos_n(0) = 64. A corner bound gives U− > 0, hence
V > 0, for every ℓ > ℓ0(n) and every q ∈ [0, 1]".
- (a) The name "U(n)" reads as the unitary group, and collides with U−.
- (b) The lemma is never stated: there is no sentence with hypothesis and conclusion, only this description.
- (c) Pos_n and Neg_n are not defined: polynomials in which variables? "Pos_n(0)" is the value at zero of what?
- (d) "A corner bound" is not explained. My guess: Neg_n has non-negative coefficients, so on the parameter box
  it is largest at one corner.
- (e) ε was the position of the pole (§4.1), and κ the growth rate of a mode (§2).
- (f) "the bound" for n = 5–9 (Table 1: "m^{−3}U− ≥ the bound") is not given in the paper.
- (g) "It is certified; its steps are proved (pencil; audited 2×), and at n = 4 the whole lemma is in Lean":
  "is in Lean" for "is formalised in Lean".
*Suggest:* "Lemma 4 (large ℓ). For n = 4, …, 9, every ℓ > ℓ0(n) and every q ∈ [0, 1], U− > 0 on the exterior
region, where ℓ0 = 10, 10, 10, 11, 13, 14", followed by its proof or by a precise statement of what is computed.

**54.** whole paper · kind 3 · D and n. The paper states results in D and computes in n = D − 2, and moves between
them inside one paragraph: §4.3 has "ℓ0 = 10 at D = 6" and "at n = 4 the whole lemma is in Lean" for the same
case; "ℓ0(n)" (p. 6) is "ℓ0(D)" on pp. 10–11; Table 1 has "Lemma U(4) (ℓ ≥ 11)" in the rows of D = 6, "n = 5–9"
for D = 7–11, and "n = 4–9" beside "D = 7–11". *Suggest:* one letter in every statement, or always both
("n = 4 (D = 6)").

### §4.4–§4.5 (p. 7)

**55.** p. 7 · kind 2 · "For the remaining ℓ above the bands". "The bands" comes before §4.5 introduces them, and
"remaining" has nothing before it to refer to.

**56.** p. 7 · kind 3 · "certified on boxes in (t, µ) with x = t x_H". t is the time coordinate on p. 5 (e^{κt}).

**57.** p. 7–12 · kinds 1, 2 · "The bands."; "one band at D = 6"; "the critical bands"; about thirty uses. "Band"
is a coinage, and it is never defined. From its use it is a pair (D, ℓ) for which V_{S−} is negative somewhere
for some charge; but "from q∗", "Some open at an onset" and "open only above 99/100" treat it as an interval of
charges. In spectral theory a band is a spectral band, and a PDE referee may read it so. *Suggest:* "We call
(n, ℓ) exceptional if V_{ℓ,q} takes a negative value for some q ∈ [0, 1]; this is the case exactly for
2 ≤ ℓ ≤ n − 2", and "the onset charge q_on(n, ℓ) := inf{q : V_{ℓ,q} takes a negative value}".

**58.** p. 7 · kind 4 · "one band at D = 6 (…), and the bands ℓ = 2, …, n − 2 at D = 7–11, twenty in all". Is the
band at D = 6 one of the twenty? From §§5.2–5.3 it is not (twenty at D = 7–11, so twenty-one). And D = 6 follows
the same rule (ℓ = 2 = n − 2), so the sentence need not split it off.

**59.** p. 7, 9, 10 · kinds 1, 2 · "from q∗ ≈ 0.97306; its inward upper end in §5.1 is 0.97305". "Inward" is
defined two pages later ("Decimals are inward: lower ends rounded up, upper ends rounded down", p. 9). "Inward
rounding" exists in interval arithmetic, but "its inward upper end" is opaque, and two decimals for one number
make the reader stop. q∗ itself is used here before p. 10 defines it, and its star is not the star of r∗. Later:
"(inward: 0.97305)", "inward: [0.97277, 0.99019]", "the outward decimal or bare digits". *Suggest:* exact
endpoints, one "≈" value each, and one sentence: "Decimal values are for orientation only; every comparison is
between exact numbers."

**60.** p. 7, 10, 11 · kind 1 · "Some open at an onset q > 0; others are negative from q = 0⁺."; "opens in the
interior"; "open only above 99/100". "A band opens" for "V first takes negative values". See items 29, 57.

**61.** p. 7, 10 · kinds 1, 4 · "Each band is certified by stored designs P and N > 0 on boxes of (z, µ)."
"Stored" (also "stored polynomials", "stored polynomial designs", p. 10) means saved in the repository's files;
a reader wants "explicit". And what is certified is A ≥ 0 for these (n, ℓ, q), by N > 0.

**62.** p. 7–9 · kinds 3, 2 · "Near q = 1 we use four charts: O and O′ in (z, µ); T, with z = µζ; C, with µ = zσ."
(a) The same letters name pieces: "O1, O2" and "T3" in Table 1, "T1, T2" on p. 10, are not charts. (b) T is then
also a polynomial ("T = NL(µζ, µ)/µ²"), while the polynomial on chart C is called K and the one on O and O′ is
called M. (c) The domains of the charts are not given. The constants of p. 7 (item 74) are presumably their
bounds; this is not said. What distinguishes O from O′?

**63.** p. 7 · kind 4 · "Each chart's polynomial comes after an exact division."; "O and O′ use NL undivided, T
divides by µ² and C by z²"; "every chart divides, by µ, µ² or z²σ". Charts do not divide. *Suggest:* "In each
chart the polynomial tested is NL, written in the chart's variables and divided by the monomial indicated; the
division leaves no remainder."

**64.** p. 7–9 · kinds 2, 3 · "NL". It is used in §4.5 before §4.6 introduces it, and §4.6 defines it only
implicitly ("Then NL = N · S_ε²R²L is an algebraic identity"). A two-letter name for one polynomial reads as the
product of N and L, and it is not that product. Table 1 has "N · L" in the HD-S row and "NL" in the others: are
they the same? *Suggest:* one letter, for instance 𝒩 or N̂, defined by a displayed formula.

**65.** p. 7 · kind 2 · "For the singular designs of A2-S and HD-X-S, whose claims include q = 1"; "the critical
bands (HD-X-2, §4.6)". Names of pieces are used before Table 1 and §5 introduce them, and "critical bands"
before §4.6.

**66.** p. 7 · kinds 2, 3 · "Their union covers (0, 1) × [0, µ1]." µ1 is not defined. It is presumably the
typewriter MU1 of the same page: one constant in two typographies.

**67.** p. 7 · kind 4 · "and q = 1 is Theorem 2's". *Suggest:* "and the case q = 1 is covered by Theorem 2".

### §4.6 Extremality (p. 7)

**68.** p. 7, 13 · kind 3 · "Extremality and the zero mode" (heading); "The zero mode." (p. 13). Elsewhere u0 is
"the zero-energy solution". "Zero mode" suggests a normalisable eigenfunction and clashes with the definition of
"mode" on p. 5. From its formula u0 does not look square-integrable at the horizon (my reading, not checked).

**69.** p. 7 · kind 1 · "u0 is throat-principal". A coinage. I take it to mean that u0 is the principal (recessive,
minimal-growth) solution at the horizon end r∗ → −∞, "throat" being physicists' word for the near-horizon region
of an extremal black hole. *Suggest:* "u0 is the principal solution at r∗ → −∞". If u0 is also principal at
+∞, the standard statement is: "u0 is a ground state and A_{ℓ,1} is critical in the sense of Murata and
Pinchover, so there is no W ≥ 0, W ≢ 0, with A_{ℓ,1} − W ≥ 0". That is what "no design can give N > 0 at q = 1"
says, and it would explain the word "critical". Unsure that this is the meaning intended; it is my inference
from the formula of Theorem 2.

**70.** p. 7, 11 · kinds 2, 3 · "The critical bands."; "the critical set 𝒦" (p. 11). "Critical" is not explained
(see item 69). The set 𝒦 is introduced four pages after the term, and never used again.

**71.** p. 7 · kind 4 · "Near q = 1 we use u0's own design, (1 − z)(log u0)_z, with its pole moved to z = −ε and a
term cµ added." Terse at each step: "u0's own design" (the P for which S = −W); "its pole" (which one: at
z = 0?); c and ε are not defined.

**72.** p. 4, 7–9, 11 · kind 3 · "the certificates are M = NL/µ on O and O′, T = NL(µζ, µ)/µ², and
K = NL(z, zσ)/(z²σ)". M is the mass (p. 4). K is the curvature constant of [1] (p. 4), a polynomial in the A2-E
row of Table 1 ("F = µK + sG"), this polynomial, and, in calligraphic, the critical set (p. 11). T: item 62.

**73.** p. 7 · kinds 1, 2, 3 · "Write P = Π/𝒟 with 𝒟 = S_ε · R · Hn, where S_ε = ε_d z + ε_n is the pole factor (not
the deformation S of §4.1), R = (1 − (1 − z)^{n−1})/z, and Hn is H's numerator. Then NL = N · S_ε²R²L is an
algebraic identity, with L = Ud · Hd² · fd, valid wherever H ≠ 0." Identifiers of a program used as symbols:
Hn, Ud, Hd, fd. The last three are never defined (denominators of U−, H− and f as rational functions of z and µ,
I suppose). ε_d and ε_n are not defined, and their n is not the dimension. S_ε needs a disclaimer in the text
itself, which says that it should have another letter. 𝒟 stands beside D, R beside ℝ, H for H−, and L is the
number of accepted boxes on p. 8.

**74.** p. 7, 11 · kinds 1, 2, 5 · "The constants are Z1 = 1/4, ZT = 8, SIG1 = 1/8, MUT = 1/32 and
MU1 ∈ {1/8, 13/100, 3/25}. The case split needs 0 < Z1 < 1, 0 < MUT ≤ MU1 and ZT · SIG1 ≥ 1. … keep the images of
T and C inside the rectangle. The code checks all five." Program identifiers in typewriter as mathematical
constants. None is defined: which one bounds which chart? "The case split" and "the rectangle" are not
explained. *Suggest:* z₁, ζ₁, σ₁, µ_T, µ₁; the four chart domains written as sets; and the cover stated as a
lemma: "the images of the four charts cover (0, 1) × (0, µ₁]".

**75.** p. 7, 11 · kinds 5, 2 · "(pencil; audited 2×, by Kimi and by Fable)"; "(from Fable's audit)" twice; "(a
remark in Fable's audit of HD-X-2)" (p. 11). Names of AI models as auditors inside the mathematics, six pages
before §9 says what Kimi and Fable are. Who made a remark belongs in §9 or the acknowledgements.

**76.** p. 7 · small · "w = w(µ) of §2 rises from w(0) = 0 to w(1) = 1". *Suggest:* "increases".

### §4.7 and Table 1 (pp. 7–9)

**77.** p. 7–8, 11 · kinds 1, 2 · "Box counts are the records' counts"; "Each entry is taken from its step's
RESULT or from that RESULT's sealed JSON record". "Record", "RESULT", "sealed" and "step" are the project's
workflow words and are not defined. "Sealed" (also p. 11, twice) seems to mean hashed and not changed after.

**78. †** p. 8–9 · kinds 2, 5 · the "Piece" column of Table 1: "O1, O2", "T3", "P1 Part I", "Lemma U(4)", "A2-E",
"A2-S", "HD-E E1", "HD-E E2", "HD-E E3", "HD-S", "HD-X-E", "HD-X-S", "HD-X-2", "Z". Internal labels. No letter is
expanded: E, S, X, HD, P1, Z, and the 2 of HD-X-2. "T3" implies a T1 and a T2, and "P1 Part I" a Part II, which
do not appear. The forms vary: "HD-E E1", "(HD-E, E1)", "E1's range"; "P1 Part I" and "P1"; "A1" and "a1";
"P1" and "p3". *Suggest:* descriptive names (each row's range of D, ℓ and q is enough), or one table that
defines the labels, in the repository's documentation.

**79.** p. 8–9 · kind 2 · undefined symbols in the entries of Table 1: "F(t, µ)" (the polynomial tested in the
rows on U−; never defined); "F = µK + sG" (s, K and G); "p0"; "µ_lo(ℓ)" (defined on p. 10); "q_split" (never
defined; p. 10 gives one value); "the bound"; "O2: three regions"; "33 parts (5 split, 28 strict)"; "symbolic n"
(*suggest* "for general n, symbolically").

**80.** p. 8–9 · kind 3 · "8 parts"; "33 parts". "Part" is also A1, A2, HD and HD-X ("The parts of the proof",
p. 9). Also "accepted at once" beside "accepted at the first box".

### §5 Proof of Theorem 1 (pp. 9–11)

**81.** p. 9, 12 · kinds 5, 3 · "The parts of the proof are named as registered: A1 and A2 at D = 6, and HD
(q ≤ 99/100) and HD-X (q ∈ [99/100, 1]) at D = 7–11." The names come from the project's registry. The hierarchy
of units is never explained: four parts, fifteen rows of Table 1 ("pieces"), "the 54 certificates" (p. 12),
"428 of 428" jobs' records (p. 12), and "By step: onset 6, p3 7 …" (p. 12).

**82. †** p. 9 · kinds 1, 4 · "Range ends are exact, and compared exactly by a gate of the step named." "Range
ends": *suggest* "the endpoints of the charge intervals". "Gate" (also "the must-pass known-answer gate G1",
"A gate checks", "gate MEET", "the gate 1") is quality-control jargon for a check that must pass. "Of the step
named": named where? *Suggest:* "Every comparison of endpoints used below is an inequality between exact
numbers, verified in exact arithmetic by the computation cited."

**83.** p. 9 · kinds 5, 1 · "They are the ones recorded in each step's RESULT, except at two ends where the RESULT
gives the outward decimal or bare digits: T3's upper end, 0.99019 (…), and A2-S's lower end, 0.98937 (…)".
Bookkeeping about which file holds which rounding. "Bare digits" is not clear (truncated?). See item 59.

**84.** p. 10 · kind 4 · "where q∗² is the real root of 3025Y³ − 31521Y² + 99792Y − 68796 (inward: 0.97305)". The
decimal is that of q∗; the root is q∗². For Y see item 40.

**85.** p. 10, 11 · kinds 1, 2, 4, 5 · "T3's record. T3's certificate comes from the p3 registration (…). Its
verdict as registered is FAIL, because the must-pass known-answer gate G1 failed for that design rule"; "A
second design rule was registered afterwards … and passed G1"; "The T1, T2 and T3 certificates of […] stand";
"the run's soundness controls rejected as registered"; "Rule 2 passed G1 without re-running T3"; "fail-closed
and VERIFIED, with its second parties". A referee stops at "FAIL": what failed, and does it touch the theorem?
The bullet is the project's history in the project's words. G1 is never described (which known answer?), "that
design rule" has no antecedent, T1 and T2 appear only here, and the paper quotes its own repository as a source.
"Known-answer test" is a term from the testing of cryptographic modules. The mathematical content is one
sentence. *Suggest:* "Remark. The eight functions P used here were produced by a search procedure that failed a
separate test fixed in advance. The verification of N > 0 for these explicit P does not depend on how they were
found. The repository records the history." (The wording must be checked against what G1 was; I cannot tell
from the paper.)

**86.** p. 10, 11 · kinds 3, 4 · "The two meet exactly"; "§5.3 meets it at q(µ_lo)"; "It meets HD-X-S's
[q(1/8), 1]"; "gate MEET". "Meet" is "share an endpoint" in the first two and "overlap" in the third, and a
section does not meet an interval. *Suggest:* "the two intervals share the endpoint q(µ_lo)"; "overlap".

**87.** p. 6–12 · kind 3 · "exactly", "exact". "with q(µ_lo(ℓ))² ≥ (99/100)² exactly" (the checking is exact, not
the inequality); "compared exactly"; "an exact division" (no remainder); "meet exactly" (share an endpoint);
"re-ran T3's certificate exactly" (p. 13); "matched its registered record exactly" (p. 12: identical files).
*Suggest:* "verified in exact arithmetic" for the first two, and other words for the others.

**88.** p. 10 · kind 5 · "(results/a2/elementary/PREREG.md l. 13, whose inequality for q(µ_lo) is corrected in
results/a2/STAGE_REPORT_ADDENDUM_1.md l. 43). A gate checks q(µ_lo)² ≥ (99/100)² (that PREREG, l. 26)." The
trail of an internal correction, inside a proof.

**89.** p. 10 · kind 2 · "ℓ_el(D) ≤ ℓ ≤ ℓ0(D), with ℓ_el = 4, 5, 6, 6, 7". ℓ_el is given by its values only. "el"
is not explained (elementary? compare the paths "results/hd/elementary" and the suffix "-E"), nor what makes a
piece elementary; my guess is U− ≥ 0, so that no S-deformation is needed. Also "a µ-box [µ_lo, 1]" for an
interval, and three forms: "µ_lo(D, ℓ)", "µ_lo(ℓ)", "µ_lo".

**90.** p. 10 · kinds 2, 4 · "U− > 0 on [0, q_split] … N > 0 on [q(µ_b), q(µ_a)] (HD-S), with q(µ_b)² ≤ q_split²";
"HD-S's coverage check". q_split, µ_a and µ_b are never defined. In "One of them opens in the interior of the
exterior rather than at the horizon: D = 10, ℓ = 3, at q ≈ 0.4913" the meaning has to be guessed (the negative
region first appears at an interior point), and the text does not say why this case needs a separate mention.
"The box that ends at µ = 1, i.e. q = 0, is verified" stands alone: verified to give what?

**91.** p. 1–12 · kind 3 · "step". (i) A step of a proof: "pencil steps", "the steps of Lemma U". (ii) "the
extremal step". (iii) A unit of the project's workflow: "a gate of the step named", "each step's RESULT", "By
step: onset 6, p3 7", "a step whose verdict as registered is FAIL".

**92.** p. 11 · kinds 1, 5 · "Each µ_lo equals HD-E's sealed E1 end (gate MEET)".

**93.** p. 11 · kinds 5, 3, 4 · §5.4 "What is audited". A report on the process, inside the proof: "audited by
Kimi", "Fable's pencil audit of an earlier draft of this section: all five items sound", "which had earlier only
been read", "a reading by a separate Claude Opus 5.5 session (§9), which found no gap". Which five items? How do
"read", "audited" and "pencil audit" differ? And "composition(s)" has three synonyms: "the assembly" (pp. 12,
13), "The routes from the pieces to A ≥ 0" (p. 9), "cover" and "coverage" (pp. 7, 10). *Suggest:* move it to §6
or §9, and use one word, for instance "the covering argument".

### §6 Verification (pp. 11–12)

**94.** p. 11–12 · kinds 1, 2 · "Failed and void runs stay on the record."; "Each record was re-run from a clean
archive of the recorded commit"; "every job's record and its reproduction are identical in that masked form, 428
of 428. By step: onset 6, p3 7 (and rule 2's 4), a1 8, … A2-S 9 (and its check runs 12), … HD-X-S 198 (and the
gate 1), HD-X-2 35 (and its addendum 47)". "Void", "record", "job", "check runs", "the gate", "its addendum" and
"rule 2" are not defined, and a record is not re-run; a computation is. A section on reproducibility may use
software words (commit, archive, lock file), but it must define its units once, and this breakdown uses names
the reader has not been given (onset, p3, a1).

**95.** p. 12, 13 · kinds 1, 4 · "The verification kit"; "The kit."; "In its dry run"; "the pinned lock file"; "a
canonical form that drops only run-dependent fields"; "Every control ended in its registered form"; "the eight
Lean layers rebuilt with their recorded verdicts". *Suggest:* "reproducibility package" for "kit", "a trial run
of the package" for "dry run". "Every control ended in its registered form" is unclear: each test on false
input was rejected, as specified in advance?

**96.** p. 12 · kinds 2, 1 · "re-derived by a different agent with independently written code"; "a blind
replication with its own transcription of [1]"; "the first band of D = 7". "Agent" comes before §9 says that the
agents are AI models. "Blind replication" is laboratory vocabulary. *Suggest:* "an independent
re-implementation that took its formulae from [1] directly, without access to our code", if that is what
"blind" means here.

### §7–§9 (pp. 12–13)

**97.** p. 12 · kind 3 · "A numerical screen (numerical, information only)". "Screen" was literature screening on
p. 3. *Suggest:* "a numerical scan". The label: item 24.

**98.** p. 12 · kind 1 (a standard name exists) · "the instability at a degenerate horizon, studied for extremal
black branes in [34]". *Suggest:* "the Aretakis instability", as the title of [34] has it. "Degenerate horizon"
here and "extremal horizon" elsewhere: one of the two.

**99.** p. 13 · kind 4 (small) · "That repository is a curated snapshot of the project's own."; "with 8 jobs on
one machine" (parallel processes here; a "job" in §6 is a run).

**100.** p. 13 · kind 1 · "The author chose the problem, set the targets and the kill criteria, and made every
ruling"; "ran the literature screens and the watch. The watch uses a library that makes no model calls"; "A
Claude Opus 5.5 agent of that session". "Kill criteria", "ruling" and "watch" are management words, and "the
watch" is not explained. *Suggest:* "decided in advance when a line of attack would be abandoned, and made
every decision"; "a periodic search for new preprints".

**101.** p. 1, 6 · small · "non-negative" (p. 1) and "nonnegative" (p. 6).

## 2. Symbols with more than one meaning

Collected from the items above, with a few more. "Tt" marks typewriter.

| Symbol | Meanings, with page |
|---|---|
| S | deformation function (p. 6); S_ε "the pole factor" (p. 7); the sphere S^n and the subscript of V_{S−} (p. 4); suffix of pieces "A2-S", "HD-S" (p. 8); SIG1 (Tt, p. 7) |
| K, 𝒦 | curvature constant of [1] (p. 4); polynomial in "F = µK + sG" (p. 8); polynomial on chart C (p. 7); "the critical set 𝒦" (p. 11) |
| M | mass parameter (p. 4); polynomial "M = NL/µ" (p. 7); MU1, MUT (Tt, p. 7) |
| T, t | chart T (p. 7); polynomial T (p. 7); pieces T1–T3 (pp. 8, 10); t time (p. 5); t = x/x_H (p. 7) |
| O | charts O, O′ (p. 7); pieces O1, O2 (p. 8) |
| C | chart C (p. 7); beside C¹, C0∞ |
| N, NL, L | N of Lemma 2 (p. 6); NL, which is not N·L (p. 7); "N · L" (p. 8); L a polynomial (p. 7); L a number of boxes (p. 8); Neg_n (p. 6) |
| P, p | the function P (p. 6); P̂ (p. 6); Π (p. 7); p0 (p. 8); piece "P1" (p. 8); step "p3" (pp. 10, 12); Pos_n (p. 6) |
| U | U− (p. 4); Ud (p. 7); "Lemma U(n)" (p. 6) |
| H | H− (p. 4); H, Hn, Hd (p. 7); r_H, x_H; part "HD" |
| D, 𝒟, d | dimension D; denominator 𝒟 (p. 7); d of [1] in a quotation (p. 1); exponent d (p. 6); ε_d, Ud, Hd, fd (p. 7) |
| ε | pole position z = −ε (pp. 6, 7); ε = m^{−1/2} (p. 6); ε_d, ε_n (p. 7) |
| κ | growth rate (p. 5); κ = m^{1/2}δ (p. 6) |
| δ | δ of [1] (p. 4); δ_b (p. 6) |
| ζ | "ζ-designs" (p. 6); chart variable z = µζ (p. 7); "degree … in z or ζ" (p. 8) |
| σ | frequency in a paraphrase of [20] (p. 2); chart variable µ = zσ (p. 7) |
| Y | ρ^{−(n−1)} (p. 5); variable of the cubic (p. 10) |
| k | k² eigenvalue (p. 4); "k independent audits" (p. 3); "the largest k/1000" (p. 10) |
| µ | charge parameter (p. 5); µ1 and MU1 (p. 7); µ_lo, µ_a, µ_b (pp. 8, 10); MUT (p. 7) |
| R | R = (1 − (1 − z)^{n−1})/z (p. 7); beside ℝ |
| ∗ | r∗ tortoise coordinate (p. 4); q∗ onset charge (pp. 7, 10) |
| Z, z | piece "Z (q = 1)" (p. 9); Z1, ZT (Tt, p. 7); coordinate z (p. 5) |
| E | suffix "-E" of pieces; sub-pieces E1–E3 (p. 8) |

## 3. The project's vocabulary, with the usual words

| In the paper | What a referee expects |
|---|---|
| pencil (step, audit) | pen-and-paper; by hand |
| audited k×; audit | checked independently (say by whom) |
| certified (as a label); certificate (as a computation) | "verified by an exact computation"; certificate = the data checked |
| fail-closed | "any error or limit counts as failure", said once |
| registered; registration; PREREG | fixed in advance (in a hashed file) |
| negative controls; soundness controls; tamper drills | tests on false inputs; fault injection |
| second party | an independent implementation; an independent check |
| re-derived (of a computation) | reproduced; re-verified |
| design; design rule; stored design | the function P; how P was chosen; explicit P |
| singular design | rational P with a pole outside [0, 1] |
| band; opens; onset | (n, ℓ) for which V is somewhere negative; onset charge, defined |
| critical band; throat-principal | critical operator; principal solution at the horizon end (if meant) |
| corner bound | the bound, stated |
| piece; part; step; job; run; record; RESULT | defined once, or dropped |
| gate; verdict; FAIL; VERIFIED; void | check; outcome; and prose |
| sealed | hashed, unchanged since |
| inward, outward (decimals); bare digits; range ends | exact endpoints with one "≈" each |
| meet (of intervals) | share an endpoint; overlap |
| composition; assembly; routes | the covering argument |
| kit; dry run; Lean layers | reproducibility package; trial run; Lean developments |
| screen; seed; watch (literature) | literature search; and "to our knowledge" |
| numerical screen | numerical scan |
| blind replication; transcription | independent re-implementation from [1] |
| mode (for a growing mode); zero mode | growing mode; zero-energy solution |
| the exterior | the exterior region r > r_H |
| Physical reading | Physical interpretation; or a Corollary |
| the reduction; the extremal step | Proposition 3; the case q = 1 (Theorem 2) |
| kill criteria; ruling | conditions for abandoning an approach; decision |
| the instability at a degenerate horizon | the Aretakis instability |

**Terms I checked and would leave**, so that the pass does not over-correct: "master equation", "master
variable", "tortoise coordinate", "mode stability", "S-deformation" (once defined), "nodeless", "zero-energy
solution", "Zerilli–Moncrief", "isolating interval", "Bernstein coefficients", "box", "subdivision", "blow-up"
and "chart", "exact rational arithmetic", "computer-assisted proof", "machine-checked" ("formalised in Lean" is
as good), "Reissner–Nordström–Tangherlini", "extremal", "subextremal".

## 4. Judgement

**How a referee would receive the language.** The paper is in two registers. The abstract, the statements of
Theorems 1 and 2, Lemma 1, the first bullet of §4.6 and the remarks after the theorems read as mathematics;
they are short and exact, and the statement "No mathematician besides the author has checked the argument" is
the kind of candour a referee respects. From "The designs P" in §4.1 through §6 the paper changes to the
project's working language. A referee without the repository cannot follow it: it reads as the log of a
verification, with labels, file paths, registry names and reports of audits where a mathematics paper has
definitions, statements and proofs. I expect the first report to say "I cannot check Theorem 1 from the
manuscript", and to give the notation and the vocabulary as the reason before any question of correctness.

**What matters most**, in order:

1. **The paper is not self-contained in its objects** (items 30, 26, 33, 53, 62, 73, 74, 79, 90). U−, the master
   equation and the metric are not written. Lemma U, the chart cover and the polynomial NL are described, not
   stated. Table 1 and §5 use symbols that are defined nowhere (F, q_split, µ_a, µ_b, ℓ_el, the chart constants).
   This comes first: a term can be translated by a patient reader, an absent definition cannot.
2. **The labels and the process reports stand where the mathematics should** (items 24, 38, 42, 46, 75, 85, 88,
   93). "Proved (pencil; audited 2×)" tells the reader that a proof exists elsewhere. A referee wants the proof,
   or a precise statement of what was computed, and is not moved by the number of audits. One "status" table,
   and §6 for everything about registration, controls, audits and T3's history, would let §§3–5 be plain
   theorem, lemma and proof.
3. **The coinages** (table of §3): above all "band", "design", "piece/part/step", "gate", "inward",
   "throat-principal", "critical", "second party" and "pencil". Most have a standard word. "Band" and
   "critical" need a definition; "throat-principal" may hide a standard and stronger statement (item 69).
4. **The collisions of symbols** (table of §2): NL (not a product), M, K, T, S_ε, ε, κ, Y, t, the typewriter
   constants, and D against n (item 54).
5. **Three sentences of analysis in §2** (items 32–34): self-adjointness, the meaning of A ≥ 0, and "mode". They
   are a few lines, but a PDE referee judges the author by them.

**A count.** 101 items. By the first kind listed in each: 25 of kind 1, 21 of kind 2, 19 of kind 3, 22 of
kind 4, 11 of kind 5, and three without a kind (15, 76, 101). The items of kind 5 are the fewest, but each
stands for many occurrences (the labels, the file paths, the registry names). Four items are marked † as not
independent of what this session had seen before the brief (24, 38, 78, 82).
