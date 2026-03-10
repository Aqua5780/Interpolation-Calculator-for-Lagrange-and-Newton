"""
Interpolation Calculator — Polynomial Arithmetic Helpers

Polynomials are stored as coefficient lists:  [const, x, x², x³, …]
"""

from .helpers import fmt


# ── core operations ──────────────────────────────────────────

def poly_mul(a, b):
    """Multiply two polynomials."""
    n = len(a) + len(b) - 1
    c = [0.0] * n
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            c[i + j] += ai * bj
    return c


def poly_from_roots(roots):
    """Build ``(x - r₀)(x - r₁)…`` from a list of roots."""
    p = [1.0]
    for r in roots:
        p = poly_mul(p, [-r, 1.0])
    return p


def poly_scale(p, s):
    """Multiply every coefficient by scalar *s*."""
    return [c * s for c in p]


def poly_add(a, b):
    """Add two polynomials."""
    n = max(len(a), len(b))
    r = [0.0] * n
    for i in range(len(a)):
        r[i] += a[i]
    for i in range(len(b)):
        r[i] += b[i]
    return r


# ── pretty-printing ──────────────────────────────────────────

def _pow_str(k):
    """Return the exponent decoration for power *k*."""
    if k == 0:
        return ""
    if k == 1:
        return ""
    if k == 2:
        return "²"
    if k == 3:
        return "³"
    return f"^{k}"


def poly_str(coeffs):
    """Pretty-print a polynomial from its coefficient list."""
    deg = len(coeffs) - 1
    parts = []
    for k in range(deg, -1, -1):
        c = coeffs[k]
        if abs(c) < 1e-14:
            continue
        cv = fmt(abs(c))
        is_leading = not parts

        if is_leading:
            sign = "" if c >= 0 else "-"
        else:
            sign = " + " if c >= 0 else " - "

        if k == 0:
            parts.append(f"{sign}{cv}")
        elif cv == "1":
            parts.append(f"{sign}x{_pow_str(k)}")
        else:
            parts.append(f"{sign}{cv}x{_pow_str(k)}")
    return "".join(parts) if parts else "0"


def poly_term_str(coeffs):
    """Return ``[(value, power), …]`` for nonzero terms, highest power first."""
    return [(coeffs[k], k) for k in range(len(coeffs) - 1, -1, -1) if abs(coeffs[k]) > 1e-14]
