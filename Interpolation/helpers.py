"""
Interpolation Calculator — Number & Symbol Formatting Helpers
"""

_SUB = "₀₁₂₃₄₅₆₇₈₉"


def sub(i):
    """Return subscript digits for index *i*."""
    return "".join(_SUB[int(d)] for d in str(i))


def fmt(v, dp=6):
    """Format a number: integer when exact, else up to *dp* decimals (trailing zeros stripped)."""
    if v is None:
        return ""
    if abs(v) < 1e-14:
        return "0"
    if abs(v - round(v)) < 1e-10:
        return str(int(round(v)))
    s = f"{v:.{dp}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s


def signed(v, dp=6):
    """Return ``'+ 0.95'`` or ``'- 0.6167'`` with the appropriate sign."""
    if v >= 0:
        return f"+ {fmt(v, dp)}"
    return f"- {fmt(abs(v), dp)}"


def xdiff_sym(var, b):
    """Symbolic ``(var - b)`` handling negative *b*: ``(x - 3)`` or ``(x + 1)``."""
    if b >= 0:
        return f"({var} - {fmt(b)})"
    return f"({var} + {fmt(abs(b))})"


def xdiff_num(a, b):
    """Numeric ``(a - b)`` handling negative *b*."""
    if b >= 0:
        return f"({fmt(a)} - {fmt(b)})"
    return f"({fmt(a)} + {fmt(abs(b))})"
