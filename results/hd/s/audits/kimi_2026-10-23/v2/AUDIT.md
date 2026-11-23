# AUDIT — bh-modes HD-S, the S-certificates of D = 7–11 (BHM-078)

*Auditor: Kimi (second auditor for machine results), 2026-10-23.
Brief: `results/hd/s/briefs/BRIEF_kimi_2026-10-23.md`, SHA-256
`e5e9c7df35402576e80c2ac45ec63a36faa3535d3a48352c795a0c827cba416d` (verified against
`SEALED.sha256`; the artifact and code hashes listed in the brief verified).
Workspace: `[kimi-folder]/bhm-hd-s-audit-2026-10-23/`.
Runs of record: own suite on **host-1**, kit reproduction on **host-2**, both `nice -n 19` with
the pinned venv. The bh-modes tree was never modified.*

**Anti-anchoring.** All own checks were complete and on disk before any result/log/registry
files were opened. Only the `boxes[]` fields (`mu`, `variable`, `degree`, `delta_b`, `P`) of
the certificate JSONs were read — never a verdict field; the slimmed copies I worked on are in
`data/` (boxed fields only).

## Task 1 — transcription

My own general-n KI (5.62b)/(5.63b) transcription (p3 audit, BHM-036 — the same `build.py` the
kit's E0n gate uses as its oracle), validated there against the rendered PDF.

## Task 2 — own exact check of every stored certificate: PASS

My own N-builder at general n (`own/buildN.py`), in Y = 1−z, on my own QQ(μ) arithmetic:

- z-design: N = U₋ − 64H₋²[(1−z)f_z P + f(−P + (1−z)P_z + P²)], x = x_H(1−z)^{n−1},
  f = 1 − x + q²x²/4;
- ζ-design: P = P̂/(z+δ_b)^d, checked through Ñ = N·(z+δ_b)^{2d} (polynomial; positivity
  equivalent since δ_b > 0).

Cross-checked against an independent sympy build of N: every z-coefficient of the 7-2 first
box at μ = 13/100 (z-design) and the 9-5 first box at μ = 11/100 (ζ-design) — exact agreement
(`own/crosscheck_s.py` and log).

Every box of every band: Den = A^a B^b (μ+1)^c > 0 on the μ-box (factorwise, my verifier) and
Ñ > 0 on [0,1] × the box (my exact Bernstein verifier, the fixed version — see the HD-E
audit). Results (`own/verify_all.host-1.log`, host host-1):

- **all 231 boxes POSITIVE; all 18 bands VERIFIED**;
- coverage exact per band: boxes contiguous, q(μ_a)² ≥ (99/100)², and q(μ_b)² ≤ q_split² for
  the 13 onset bands resp. μ_b = 1 (q = 0) for the 5 bands from 0⁺;
- in particular the interior band D = 10 ℓ = 3: the first box starts below the onset
  (q²(μ_b) = 91914991536373201/383045380761373201 ≈ 0.23995849 ≤ (49/100)²).

## Task 3 — pencil verdicts on the two extensions of Proposition 3

- **(a) general n: SOUND.** My p3-audit proof of the identity Ṽ = fN/(64ρ²H₋²) was derived
  for *abstract* f(z) and P(z), so it carries over verbatim; what remains is f > 0 on the
  exterior — with f = (1−y)(1−ky), y = (1−z)^{n−1} ∈ (0, 1), k = (1−w)/(1+w) ∈ (0, 1), that is
  manifest — and H₋ ≥ m > 0 (all coefficients positive). Endpoints are inside the certified
  closed interval, as at n = 4.
- **(b) the ζ-design: SOUND.** δ_b > 0 ⇒ z + δ_b > 0 on [0, 1], so P = P̂/(z+δ_b)^d is smooth
  there (its poles lie at z = −δ_b < 0, off the exterior), S = −f(1−z)P stays C¹, Lemma 1 of
  `results/p3/METHOD.md` applies, and N·(z+δ_b)^{2d} > 0 ⇔ N > 0 because the factor is
  strictly positive on the closed interval.

## Task 4 — controls: all REJECT as required

- **(a) planted bound state** (band 7-2, box 0, at the box midpoint μ_c = 1299/10000;
  W = −K f b/ρ², b = ((z−3/10)(3/5−z))², K = 174913): (i) Q[b] = A − K·C < 0 rigorously
  (acb integration over the full support r ∈ [10/7, 5/2]: A = [1.16077654521e-6 ± 6.0e-18],
  C = ∫ b³r⁻² = [1.3273e-11 ± 3.5e-16], Q's upper bound < 0), so the bound state is real;
  (ii) the same certificate P checked against V + W REJECTs in exact arithmetic,
  counterexample at z = 1/2.
  *(Corrected 2026-10-24 on the lead's note: the first version integrated over
  [10/7, 5/3] — only part of the support — and carried an extra 1/f in the W-integral, so
  "Q[b] < 0 rigorously" was not established as printed. The redone (i) uses the full support
  and the right weight, with K recomputed. Part (ii) was unaffected.)*
- **(b) one stored certificate, one coefficient changed** (7-2 box 0, P's constant term
  +1/10): REJECT, counterexample at (z, μ) = (1/2, 1299/10000).
- **(c) verifier tamper:** caught by the KAT suite (KAT1–KAT8, including the
  tampered-verifier drill and the substitution identities).

## Task 5 — reproduction

`kit/hd/run_s.sh` at `0aa2673` on **host-2** (`runs/kit-run-host-2/`): exit 0, **KIT PASS** —
all 18 bands VERIFIED, and every registered control and drill (per-D td-coeff, td-horizon,
nc-bound, and td-verifier) REJECTed exactly as registered. Every band's reproduced
`result.json` is identical to the run of record in every substantive field (timings/host
masked).

## Overall verdict

**HD-S stands: all 18 bands verified by my own exact route, with exact coverage; the pencil
extensions are SOUND; my controls reject; the kit reproduces the record bit-for-bit at the
substantive level.** With HD-E (BHM-063, my audit of it), Theorem HD (D = 7–11, every ℓ ≥ 2,
0 < q ≤ 99/100) now has both its parts second-party checked.

Pointer for the operator: audit workspace `[kimi-folder]/bhm-hd-s-audit-2026-10-23/`
(AUDIT.md, audit_record.json, SHA256SUMS).
