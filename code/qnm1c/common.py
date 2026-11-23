"""Shared helpers for the 1c certificate: errors, exact boxes, ball conversions, provenance."""
import hashlib
import json
import os
import platform
import socket
import subprocess
import sys
from fractions import Fraction

from flint import acb, arb, fmpq


class CertificateError(Exception):
    """Raised whenever a check cannot be verified.  Callers turn it into REJECT."""


def q(fr):
    """Fraction -> fmpq (exact)."""
    fr = Fraction(fr)
    return fmpq(fr.numerator, fr.denominator)


def arb_q(fr):
    """Exact rational as an arb ball (radius from rounding only)."""
    return arb(q(fr))


def acb_q(re, im):
    return acb(arb_q(re), arb_q(im))


class Box:
    """Closed rectangle [re0, re1] x [im0, im1] with exact rational corners, in omega_L = 2 M omega."""

    def __init__(self, re0, re1, im0, im1):
        self.re0, self.re1, self.im0, self.im1 = (Fraction(v) for v in (re0, re1, im0, im1))
        if not (self.re0 < self.re1 and self.im0 < self.im1):
            raise CertificateError("degenerate box")

    @classmethod
    def from_Momega(cls, re0, re1, im0, im1):
        return cls(*(2 * Fraction(v) for v in (re0, re1, im0, im1)))

    def to_Momega(self):
        return [str(v / 2) for v in (self.re0, self.re1, self.im0, self.im1)]

    def center(self):
        return (self.re0 + self.re1) / 2, (self.im0 + self.im1) / 2

    def corners_ccw(self):
        return [(self.re0, self.im0), (self.re1, self.im0), (self.re1, self.im1), (self.re0, self.im1)]

    def contains_box(self, other, strict=False):
        if strict:
            return (self.re0 < other.re0 and other.re1 < self.re1
                    and self.im0 < other.im0 and other.im1 < self.im1)
        return (self.re0 <= other.re0 and other.re1 <= self.re1
                and self.im0 <= other.im0 and other.im1 <= self.im1)

    def as_acb(self):
        """The whole box as one complex ball."""
        return acb(interval(self.re0, self.re1), interval(self.im0, self.im1))

    def grid(self, nre, nim):
        out = []
        dr, di = (self.re1 - self.re0) / nre, (self.im1 - self.im0) / nim
        for i in range(nre):
            for j in range(nim):
                out.append(Box(self.re0 + i * dr, self.re0 + (i + 1) * dr,
                               self.im0 + j * di, self.im0 + (j + 1) * di))
        return out

    def json(self):
        return {"omega_L": [str(v) for v in (self.re0, self.re1, self.im0, self.im1)],
                "Momega": self.to_Momega()}


def interval(lo, hi):
    """arb enclosing the real interval [lo, hi] (exact rationals)."""
    return arb_q(lo).union(arb_q(hi))


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def provenance():
    import flint
    import mpmath
    import sympy
    try:
        import gmpy2
        gv = gmpy2.version()
    except Exception:  # noqa: BLE001
        gv = None
    commit = os.environ.get("BHM_COMMIT")
    if commit is None:
        try:
            commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                                    text=True, check=True).stdout.strip()
        except Exception:  # noqa: BLE001
            commit = "unknown"
    return {
        "git_commit": commit,
        "host": socket.gethostname(),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "python_flint": flint.__version__,
        "FLINT": flint.__FLINT_VERSION__,
        "sympy": sympy.__version__,
        "mpmath": mpmath.__version__,
        "gmpy2": gv,
    }


def dump_json(obj, path):
    with open(path, "w") as fh:
        json.dump(obj, fh, indent=1, sort_keys=True)
        fh.write("\n")
