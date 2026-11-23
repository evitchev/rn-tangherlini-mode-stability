# PREREG — my audit of the bh-modes extremal checks E0–E5 (BHM-010)

*Auditor: Kimi. 2026-10-22.*

Brief: `results/a2/extremal/briefs/BRIEF_kimi_2026-10-22.md`, SHA-256
`6591db1e5f6a4e85df418224f06c8bef9cb24deb7f74cbd9a87d81b3ba9852b4` (verified against
`SEALED.sha256`).

## Anti-anchoring

Before opening `results/a2/extremal/RESULT.md`, anything under
`results/a2/extremal/runs/`, `REGISTRY.md` rows >= BHM-010, `lean/`, or `outbox/`, I will have
on disk:

1. E0: my own transcription of KI hep-th-0308128 (5.62b)/(5.63b) from the rendered PDF (page
   25; done in my p3 audit, same source) checked symbolically against TARGET.md;
2. E1-E5 as exact identities in ell with my own CAS, the limits in E2/E5 by exhibiting the
   rational functions whose value at r = 1 gives them;
3. controls: (a) the negative branch of KI (5.58) at q = 1 must make E3 fail in my code;
   (b) a perturbed U_- coefficient must make E3 fail;
4. the reproduction run of `kit/a2/extremal.sh` at `8a19e06`, exit code and log hash.

## Pre-committed verdict rule

Each of E0-E5 passes only on my own exact computation. Overall PASS requires E0-E5 all PASS
and the reproduction green.
