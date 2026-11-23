# PREREG — my audit of bh-modes HD-X-E / HD-X-S / HD-X-2 (BHM-127, BHM-131, BHM-143)

*Auditor: Kimi. 2026-10-27.*

Brief: `results/stage3/briefs/BRIEF_kimi_2026-10-26.md`, SHA-256
`efdfd025595b04290c15933929be39199781d689332d4004fe092d28065765ef` (the value carried by the
cover message; per the brief's own instruction, `SEALED.sha256` is NOT opened to check it).

## Anti-anchoring (allow-list regime)

Until my own checks are on disk, I read only: the brief; the files in its first table
(TARGET_HD.md, TARGET_HD_ADDENDUM_2.md, results/hd/elementary/PREREG.md,
results/hdx/{elementary,pilot,s,critical}/PREREG.md, the pilot record's `designs` field only,
results/extremal/PREREG.md, results/p3/METHOD.md, METHOD_ADDENDUM_1.md,
METHOD_ADDENDUM_2.md, RULES.md); and my own earlier workspaces. Everything else is barred,
including `code/` (until task 7) and `SEALED.sha256`.

## What I will produce before opening anything barred

Order: HD-X-2 first (no known answer), then HD-X-S, then HD-X-E.

1. **HD-X-2** (9 bands: D = 7 ℓ = 2; D = 8 ℓ = 2; D = 9 ℓ = 2, 3; D = 10 ℓ = 2, 3; D = 11
   ℓ = 2, 3, 4): my own N from my own transcription and the registered design
   P = -nu - l y/((z+eps) R) - (1-z) H_z/H + c mu; my exact check of the zero-mode identity
   N(z, 0) == 0; my own exact proof that N > 0 on (0,1) x (0, MU1] per band, with my own
   handling of the mu -> 0 division and the corner (0, 0), and a proof that my regions cover
   the rectangle.
2. **HD-X-S** (11 bands): the same, with the A2-S-type design P = a(1+eps)/(z+eps) + p0,
   eps = w/((n-1)(1+w)), a and p0 from the pilot record's `designs` field, and the corner
   (0, 0) handled by charts.
3. **HD-X-E** (33 cases, n-1 <= ell <= l0(n)): strict positivity for ell >= n; the splitting
   at ell = n - 1 with the only zero at (x, q) = (2, 1); exact coverage.
4. Pencil verdicts: (a) the reductions for both singular designs at general n; (b) the
   tortoise map for 0 < q < 1 at general n; (c) the composition of Theorem HD-X.
5. Controls (a)-(f) as the brief lists them, each rejected, with the point and value, and a
   note on whether each could have passed.
6. The three kit reproductions on host-1/005.

## Hosts

Every run beyond a sub-minute spot check goes to host-1 or host-2 under `nice -n 19` with the
pinned venv; a copy of every run's outputs stays on its node under `[kimi-folder]/`; any
imported earlier workspace's files will be hashed on the node too (my code imports
`build.py`/`rfg.py`/`verify.py`/`part1.py` from my p3/a1/hd workspaces). The host of every run
is recorded.

## Verdict rule

Each claim passes only on my own exact computation; a failure is reported with the (D, ell),
the region, and an exact point and value. A certified Q[phi] < 0 at any D = 7-11, ell >= 2,
q in (99/100, 1] would be reported at once.
