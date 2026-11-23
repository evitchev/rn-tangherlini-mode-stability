# TRANSCRIPTION — V_S− of Kodama–Ishibashi (S5) at n = 5, ℓ = 2

*ib-blind seat (Claude agent working for the session-R lead), phase 1, 2026-10-23.
Brief: `[repository]/results/hd/s/briefs/BRIEF_ib-blind_2026-10-23.md`,
sha256 `1339b7fbd0c0761e055e375501bbb857485fc728c40c5c2b2bf2e0e19a8703dd` (checked before reading).
This is my own transcription. No bh-modes code, Kimi transcription or session-L transcription was opened.*

## 1. Sources and how they were read

| Source | Version used | sha256 of the PDF | Pages |
|---|---|---|---|
| S5 = hep-th/0308128, Kodama–Ishibashi, *Master equations for perturbations of generalised static black holes with charge in higher dimensions*, PTP 111 (2004) 29 | **v4** (2 Mar 2004), the latest | `317219dcee4b2195b0a4c06c9d984daeb5f594f403235b653c6771a5beedcaf6` | 46 |
| S5 v1 (20 Aug 2003), for comparison | v1 | `3d9783f86f2ecf384b332d330d40b29158f64d0a2cb0c7e2a696ffb7de6fff78` | 46 |
| S5 v2 (30 Sep 2003), for comparison | v2 | `b3a8915f6ee854cbbc589e18d2b647038986b46b063df2782664df3648cb0687` | 46 |
| S5 v3 (18 Dec 2003), for comparison | v3 | `c7e04b39658a164f0e95eaa9eff97e8a73cd7c209c1d867480ee92860e62dcc7` | 46 |
| Paper I = hep-th/0305147, Kodama–Ishibashi, PTP 110 (2003) 701 (the Q = 0 potential) | v3 (30 Sep 2003), the latest | `e1f58faac2dcad3759d9aa092eccc1ba9d0fc857b44bc4025fb5b62af5706c6e` | — |

- All were downloaded from arxiv.org into `lit/` on 2026-10-23 (`logs/lit_sha256_download.txt`).
- They were treated as untrusted data and read with **pdftotext 0.86.1 only**: `-layout`, `-raw`, and `-bbox`
  (word bounding boxes, used to place the large delimiters). Nothing from them was executed.
- **Placement.** In v4 the PDF page index equals the printed page number. (5.56)–(5.61) are on page 24 and
  (5.62a)–(5.66) on page 25, as the brief says ("rendered pages 24–25").
- **Versions.**
  - The `-layout` text of (5.56)–(5.66) is identical in v3 and v4.
  - v2 differs from v4 only in where pdftotext places one exponent line.
  - v1's text layer drops Greek letters and minus signs (an older font encoding). Its terms match v4 term by term
    in the same order, but it cannot be compared character by character.
  - I found no sign of an erratum between versions in (5.62)–(5.63).

## 2. The large delimiters (the only non-trivial part of reading (5.63))

pdftotext loses TeX's large delimiters. The `-bbox` output gives the opening ones as cmex glyph codes, with their
x-positions on the line: `0x02` = big `[`, `0x03` = big `]`, `0x08` = big `{`, `0x01` = big `)`. The closing `}`
glyphs (code `0x09`) are not emitted as words. Each one sits in a measured 8–9 pt gap before the power of x that it
precedes.

**(5.63b), page 25. Line y-positions are pt from the top of the page.**

| Line | Delimiters (x in pt) and neighbouring words | Reading |
|---|---|---|
| y≈302 | `[` at 130.92, before `−4n³` (135.48) | opens the y-bracket |
| y≈319 | `]` at 233.52, after `m²` (exponent at 228.72), before `y` (239.88) | `[ … −16(n−2)(n−4)m² ] y` |
| y≈337 | `{` at 243.36, after `(1+mδ)²`, before `(n+1)(3n−2)mδ`; gap 361.8→370.4 before `x³` | `−4n²(n+1)²(1+mδ)²{(n+1)(3n−2)mδ − n²}x³` |
| y≈355 / 372 | `{` at 222.48, after `+4(n+1)(1+mδ)`; next line indented (starts at 143.04); gap 377.7→386.8 before `x²` | the brace spans both lines |
| y≈389 / 407 | `{` at 161.64, after `−16m`; inner big `(` in the gap 211.4→218.3; `)` at 315.72, before `δ`; next line, gap 302.9→312.0 before `x` | `−16m{(n+1)m(−4m+3n²(n−2)K)δ + 3n(n−4)m + 3n²(n+1)(n−2)K}x` |

The reading of every bracket is confirmed by checks C1, C3, C4 and C10 below. For example, closing the x-brace at
the end of its first line would put the δ-free x-term outside the −16m factor, which fails C1.

- **(5.63a)** is read in the same way: a normal-size `]` in the word `4)]`; braces at 206.52, 185.64 and 141.24;
  a big `)` at 296.52.
- **Paper I (3.7)**, PDF page 8: the leading `−` (128.76) stands *outside* the big `[` (139.08). So the y-term is
  −[n³(n+2)(n+1)²x² − 12n²(n+1)(n−2)mx + 4(n−2)(n−4)m²]y.

## 3. Transcribed equations (general n, K, λ)

**Definitions.**
- f = K − λr² − 2M/r^{n−1} + Q²/r^{2n−2} (2.19). With x = 2M/r^{n−1}, y = λr² and z = Q²/r^{2n−2} (5.40),
  this is f = K − x + z − y.
- m = k² − nK (5.39); for K = 1, k² = ℓ(ℓ+n−1) (2.3), so m = (ℓ−1)(ℓ+n).
- µ_S5² = M² + 4mQ²/(n+1)², with µ_S5 > 0 (5.58), and µ_S5 = (1 + 2mδ)M (5.60).
- Q² = (n+1)²M²δ(1+mδ) (5.65).
- H = m + n(n+1)x/2 − n²z (5.38), and H = H₊H₋ (5.66).

**The potentials.**
- V_S± = f U± / (64 r² H±²) (5.61).
- H₊ = 1 − ½n(n+1)δx (5.62a).
- **H₋ = m + ½n(n+1)(1+mδ)x (5.62b).**
- **U₋ (5.63b)** =

      [ −4n³(n+2)(n+1)²(1+mδ)²x² + 48n²(n+1)(n−2)m(1+mδ)x − 16(n−2)(n−4)m² ] y
      − n³(3n−2)(n+1)⁴ δ(1+mδ)³ x⁴
      − 4n²(n+1)²(1+mδ)² { (n+1)(3n−2)mδ − n² } x³
      + 4(n+1)(1+mδ) { m(n−2)(n−4)(n+1)(m+n²K)δ + 4n(2n²−3n+4)m + n²(n−2)(n−4)(n+1)K } x²
      − 16m { (n+1)m(−4m + 3n²(n−2)K)δ + 3n(n−4)m + 3n²(n+1)(n−2)K } x
      + 64m³ + 16n(n+2)m²K

- **U₊ (5.63a)**, used only for check C4 =

      [ −4n³(n+2)(n+1)²δ²x² − 48n²(n+1)(n−2)δx − 16(n−2)(n−4) ] y
      − δ³n³(3n−2)(n+1)⁴(1+mδ)x⁴
      + 4δ²n²(n+1)² { (n+1)(3n−2)mδ + 4n² + n − 2 } x³
      + 4δ(n+1) { (n−2)(n−4)(n+1)(m+n²K)δ − 7n³ + 7n² − 14n + 8 } x²
      + { 16(n+1)(−4m + 3n²(n−2)K)δ − 16(3n−2)(n−2) } x
      + 64m + 16n(n+2)K

**Paper I** (Q = 0):
- V_S = fQ_I/(16r²H_I²) (3.6), with H_I = m + ½n(n+1)x (3.2).
- Q_I = −[n³(n+2)(n+1)²x² − 12n²(n+1)(n−2)mx + 4(n−2)(n−4)m²]y + n⁴(n+1)²x³
  + n(n+1)[4(2n²−3n+4)m + n(n−2)(n−4)(n+1)K]x² − 12n[(n−4)m + n(n+1)(n−2)K]mx + 16m³ + 4Kn(n+2)m² (3.7).

**Code.** These formulas are coded once, in `code/ki_s5.py` (sha256 `b2585fb00ba70a3bbe50e55ce1ca22dc8811799252d521b5fbebfc934b6d311b`).

**Notation collisions.**
- S5 writes q for the electric charge (2.14). The brief's q is |Q|/M.
- S5's µ (here µ_S5) is not TARGET_HD's rational parameter µ. In this workspace that parameter is called **µ_T**.

## 4. The brief's setting: n = 5 (D = 7), ℓ = 2, K = 1, λ = 0

**Parameters.**
- m = 7. In units r_H = 1, ρ = r/r_H and x = x_H ρ^{−4}.
- f = 1 − x + q²x²/4. Its roots are x = 2/(1 ± w), with w = √(1−q²); the outer horizon is x_H = 2/(1+w).
- δ = (s − 1)/14, with s = 1 + 2mδ = √(1 + 7q²/9). Taking s > 0 is the condition µ_S5 > 0.

**The potential.**
- **H₋ = 7 + 15(1 + 7δ)x.**
- **U₋ (y = 0)** = −2106000 δ(1+7δ)³ x⁴ − 3600(1+7δ)²(546δ − 25) x³ + 144(1+7δ)(672δ + 985) x²
  − 336(2758δ + 485) x + 49392.
- **V = f U₋ / (64 r² H₋²).**

**The rational parametrisation (TARGET_HD §1)**, with µ_T ∈ [0, 1]:
- w = 8µ_T/(7+µ_T²);
- s = 8(7−µ_T²)/(6(7+µ_T²));
- δ = (1−µ_T²)/(6(7+µ_T²));
- q² = (7−µ_T)(1−µ_T)(1+µ_T)(7+µ_T)/(7+µ_T²)²;
- x_H = 2(7+µ_T²)/((1+µ_T)(7+µ_T)).
- µ_T = 1 is q = 0, and µ_T = 0 is q = 1. q decreases strictly as µ_T increases.
- The band q ∈ [0.948, 0.99] is µ_T ∈ [0.1237038, 0.2816423] (to 7 digits).
- The exact rational cover, fixed in PREREG.md, is µ_T ∈ [1237/10000, 2817/10000], i.e. q from 0.990000611
  down to 0.947978590. It was checked with exact q² comparisons in `logs/band_edges_host-0_*.log`.
- The horizon sign change (C8) is at µ_T = 0.2770435.

## 5. Checks (all can fail; all passed)

Script: `code/check_transcription.py` (sha256 `30333817d35e4bea9a6f548e09624c62679d34f7fa8bac42947d87738c587cd4`).
- Run on **host-2**, 2026-10-23T15:36:12Z, with `[venv]` as it is (Python 3.12.8, sympy 1.14.0),
  `ulimit -v 8000000`, `timeout 1200`, `nice -n 19`.
- Full log: `logs/check_transcription_20261023T153612Z.log` (sha256 `12b0ef81b1149621845b285b2f4c57831762ff2467a2e7f5adf689dc940745f4`).
- All identities are tested exactly: the numerator of the difference must expand to 0.

| # | Check | Result |
|---|---|---|
| C1 | **Q = 0 limit vs Paper I**, general n, m, x, y, K: H₋(δ=0) = H_I and U₋(δ=0) = 4Q_I, so V_S−(δ=0) = fQ_I/(16r²H_I²) | PASS |
| C2 | n = 2, Q = 0 vs the **Zerilli** potential | PASS |
| C3 | n = 2, Q ≠ 0 vs **Chandrasekhar's polar RN potentials**. V_S− = V₂⁽⁺⁾ and V_S+ = V₁⁽⁺⁾, with V_i⁽⁺⁾ = q_j dF_j/dr* + q_j²F_j² + κF_j, F_j = Δ/(r³(µ²r+q_j)), q₁ = 6M(1+mδ), q₂ = −6Mmδ. The formula is from my memory of MTBH ch. 5; S5 itself states this identification for n = 2. | PASS |
| C4 | **Involution** µ_S5 → −µ_S5, i.e. δ → −(1+mδ)/m, which fixes Q²: H₋(δ') = mH₊(δ) and U₋(δ') = m²U₊(δ), general n, m, x, y, K. This ties together the two separately typeset formulas. | PASS |
| C5 | (5.66): H₊H₋ = m + ½n(n+1)x − n²z, with z = (n+1)²δ(1+mδ)x²/4 | PASS |
| C6 | **x → 0**: r²V → U₋(0)/(64H₋(0)²) = ((2ℓ+n−1)²−1)/4, the free (n+2)-dimensional centrifugal term, for every δ. n = 5, ℓ = 2 gives 63/4. | PASS |
| C7 | TARGET_HD §1 items: m; z = q²x²/4; the roots of f; (1+2mδ)² = 1+4mq²/(n+1)²; B² = (n+1)²+4m; s² identity; endpoints; for n = 5, ℓ = 2, w increasing and δ ≥ 0 on [0, 1] | PASS |
| C8 | The brief's background: **U₋(x_H) changes sign once**, at q = 0.949691435450… (brief: ≈ 0.9497); at q = 1, f ≈ 16(ρ−1)² and (V/f)_H = −4, so **V ≈ −(1/4)/r*²** (brief: exactly −1/4) | PASS |
| C9 | METHOD.md Lemma 2 identity, symbolically and in a concrete instance; at n = 5, ℓ = 2, N(1) = −784(2P(1)−9)(2P(1)+7), so the admissible window is −7/2 < P(1) < 9/2 | PASS |
| C10 | **Extremal structure**, general n, ℓ: κ(n,ℓ) = ℓ(ℓ−n+1)/(n−1)², and κ + 1/4 = (2ℓ−n+1)²/(4(n−1)²) is a perfect square. This is the AdS₂ form κ = Δ(Δ−1) with Δ = ℓ/(n−1). D = 7, ℓ = 2 is exactly the critical case 2ℓ = n−1. | PASS |

**Negative drills.** Each check was rerun against a deliberately corrupted U₋, and every corruption must be caught.

| Tamper | C1 | C2 | C3 | C4 | C6 | C8 | C10 | Caught |
|---|---|---|---|---|---|---|---|---|
| T1: x³ bracket, −n² → +n² (δ-free) | FAIL | FAIL | FAIL | FAIL | pass | FAIL | FAIL | yes |
| T2: (n+1)⁴ → (n+1)³ in the x⁴ term (δ only) | pass | pass | FAIL | FAIL | pass | FAIL | FAIL | yes |
| T3: 64m³ → 64m² | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL | yes |
| T4: δ → δ² in the (n−2)(n−4) x² term | pass | pass | pass | FAIL | pass | FAIL | FAIL | yes |

**Coverage.**
- C1–C3 do not see δ-dependent terms that carry (n−2) factors (T4).
- Those terms are tested by C4 (internal consistency of S5), C10 (structure) and C8 (agreement with the
  brief's numbers).
- C6 tests only the x⁰ terms.

## 6. TARGET_HD.md §1: what I used and checked

- I read lines 1–24 only, after checking that its sha256 begins `b895ecba9a23c34a`. I stopped at the §2 heading.
- Every item I use agrees with S5 and passes C7:
  - the setting f, x, q and x_H;
  - m = (ℓ−1)(ℓ+n) via S5 (2.3) and (5.39);
  - δ via (5.58) and (5.60) (and (5.65));
  - H₋ = (5.62b);
  - U₋ = (5.63b) at y = 0;
  - V = fU₋/(64r²H₋²) = (5.61);
  - the operator, from (5.59): f(fΦ′)′ = d²Φ/dr*²;
  - the rational parametrisation (identically s² = 1 + 4mq²/(n+1)²; µ_T = 1 is q = 0 and µ_T = 0 is q = 1).
- I found **no mistake in §1**.
- One remark: TARGET_HD's µ collides with S5's µ (see §3).

## 7. Blindness statement

I opened exactly one file under bh-modes `results/hd/`: the brief. I also read TARGET_HD.md lines 1–24 and
`results/p3/METHOD.md`, as allowed.

I did not open or list anything else in bh-modes:
- no addenda, no REGISTRY;
- no `code/`, `kit/`, `outbox/` or `notes/`;
- no audits;
- no git history.

On the nodes:
- **host-2:** I touched only my own `[session-R-runs]/` folder and ran `[venv]/bin/python3`.
- **host-1:** I ran one environment probe (hostname, uptime, nproc, free, df of ~, venv versions) and nothing else.
- I listed no processes on either node and never looked at `[run-folder]/`.

Nothing in phase 1 computed the spectral question. C8 and C10 evaluate the potential only at the horizon and at
q = 1 (outside the band), and both values were already given in the brief.
