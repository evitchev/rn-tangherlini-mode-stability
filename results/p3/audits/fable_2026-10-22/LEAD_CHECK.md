# The session-R lead's check of Fable's p3 pencil audit (2026-10-22 20:15 EDT)

- **Filing:** AUDIT.md sha256 `2b26da61…`, as Fable reported. SHA256SUMS: 6/6 OK, and nothing is unlisted. Brief `5f59fdbe…` is
  quoted. Fable's own SHA256SUMS is untouched; this note is covered by SHA256SUMS_LEAD.
- **Spot check of the code observation (GAP-MINOR, sec. 5).**
  - At `094591c`, `code/onset/bernstein.py` l.17-19 defines Q(v) = Fraction(str(v)) for any non-Fraction. So a float would
    enter through its decimal string, not its binary value.
  - In `code/p3/scert.py`, the calls on the proof side apply Q to polynomial coefficients, the μ-box ends and the constants
    ZA and ZB (l.205, 210, 258, 271, 275, 278).
  - The explicit float conversions (l.119, 248-249) are in the Riccati diagnostic and in the NC-P1 quadrature, which is a
    negative control.
  - So this is consistent with Fable's "not exercised in the trust path". It was a grep of the call sites, not a full trace of
    the argument types. A type assertion in Q (reject float) would close the point at no cost.
- **Scope:** Fable's audit covers METHOD.md, the code's trust base and the Lean statement fidelity, without having read
  RESULT.md (anti-anchoring). The lead's own reading of p3 (METHOD and RESULT) is still to come and will focus on RESULT.md's
  claims against the audited method.
