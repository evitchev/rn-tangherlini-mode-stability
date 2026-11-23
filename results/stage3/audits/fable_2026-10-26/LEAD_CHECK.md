# The session-R lead's check of Fable's stage-2/3 pencil audit (2026-10-26, about 22:20 EDT)

- **Filing:**
  - AUDIT.md sha256 `79673b75…`, as Fable reported. SHA256SUMS `83188748…`: 5/5 OK. Nothing is unlisted except STATE.md,
    STATE_LOG.md and MESSAGES.md, which Fable declares as evolving.
  - The brief copy in this folder equals the sealed brief `e45fdde0…` (cmp), and AUDIT.md quotes that hash.
  - Fable reports no process run, the allow-list kept and SEALED.sha256 not opened. The folder holds no code, logs or outputs that
    would say otherwise.
  - Fable's SHA256SUMS is untouched; this note is covered by SHA256SUMS_LEAD.
- **Spot check of A3's GAP-MINOR (the μ = 0 design and the pencil Proposition's hypothesis).**
  - `results/p3/METHOD_ADDENDUM_2.md` l.19 states the pencil Proposition for "P C¹ on an open interval containing [0, 1]".
  - `TARGET_A2_ADDENDUM_1.md` l.58 puts the design's pole at z = −ε ≤ 0. At ε = 0 the pole is at z = 0, which lies in [0, 1].
  - Lean's `prop3_Ioo` (`lean/lean_p3_sdeformation_v4_2026-10-24/lean/BHModesP3.lean` l.403-405) assumes P differentiable only for
    0 < z < 1, with P′ continuous on `Set.Ioo 0 1`.
  - So Fable's reading holds: the Lean statement covers the μ = 0 design and the pencil wording does not. The proposed addendum
    (the (0, 1) form, and "outside (0, 1)" where the μ = 0 design is meant) closes it. No result changes.
- **Spot check of B1's GAP-MINOR (the intertwiner at the extremal, irregular horizon).**
  - `results/extremal/PREREG.md` l.78-84 argues that w → 0 at both ends along r* (like −ν/ρ at infinity, like −α/s at the
    throat). It flags the quasinormal-mode condition at the irregular point itself as "the part to audit".
  - Fable's fix: w = O(ρ − 1) in every direction, so L preserves each sector's recessive solution, and
    W[Lψ₁, Lψ₂] = ω² W[ψ₁, ψ₂]. I have read this pencil argument but not re-derived it. It changes no claim.
- **Scope:** a pencil audit, with no computation. Its limits are Fable's list of hypotheses: S5's reduction as the trust base, the
  machine gates not re-run, Lean statements read but proofs not re-checked, and standard asymptotics at rank-1 irregular points.
