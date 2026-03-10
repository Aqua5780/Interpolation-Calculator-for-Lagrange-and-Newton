"""
Interpolation Calculator — Lagrange Interpolation (step-by-step output)
"""

import tkinter as tk

from .helpers import sub, fmt, signed, xdiff_sym, xdiff_num
from .polynomial import poly_from_roots, poly_scale, poly_add, poly_str


def render(txt_widget, x, y, xv, denoms=None):
    """
    Write the full Lagrange step-by-step solution into *txt_widget*.

    Returns ``(result_value, denoms_list)`` so the caller can cache them.
    """
    n = len(x)
    t = txt_widget
    t.config(state=tk.NORMAL)
    t.delete("1.0", tk.END)
    w = lambda s, tg="fm": t.insert(tk.END, s, tg)

    w("LAGRANGE INTERPOLATION\n", "title")
    w("=" * 52 + "\n\n", "dim")

    # ── Given Data ──
    w("Given Data Points:\n", "section")
    for i in range(n):
        w(f"  x{sub(i)} = {fmt(x[i])},   f(x{sub(i)}) = ", "fm")
        w(f"{fmt(y[i])}\n", "val")
    w(f"\nDegree of polynomial: {n - 1}\n\n")

    w("Formula:\n", "section")
    w("  Li(x) = PROD (x - xj)/(xi - xj),  j != i\n", "fm")
    w("  P(x)  = SUM  f(xi) * Li(x)\n\n", "fm")

    # ══════════════════════════════════════
    # Step 1: Compute Basis Polynomials
    # ══════════════════════════════════════
    w("--- Step 1: Compute Basis Polynomials ---\n\n", "step")

    if denoms is None:
        denoms = []
        for i in range(n):
            d = 1.0
            for j in range(n):
                if j != i:
                    d *= (x[i] - x[j])
            denoms.append(d)

    for i in range(n):
        w(f"L{sub(i)}(x)", "hl")

        num_parts = [xdiff_sym("x", x[j]) for j in range(n) if j != i]
        den_sym   = [xdiff_num(x[i], x[j]) for j in range(n) if j != i]
        den_diffs = [x[i] - x[j] for j in range(n) if j != i]

        w(f" = {''.join(num_parts)} / {''.join(den_sym)}\n", "fm")

        den_nums = [f"({fmt(d)})" for d in den_diffs]
        pad = " " * len(f"L{sub(i)}(x)")
        w(f"{pad} = {''.join(num_parts)} / {''.join(den_nums)}\n", "fm")

        w(f"{pad} = ", "fm")
        w(f"{''.join(num_parts)} / {fmt(denoms[i])}\n\n", "val")

    # ══════════════════════════════════════
    # Step 2: Interpolating Polynomial
    # ══════════════════════════════════════
    w("--- Step 2: Interpolating Polynomial ---\n\n", "step")

    parts = [f"{fmt(y[i])} * L{sub(i)}(x)" for i in range(n)]
    w(f"P(x) = {' + '.join(parts)}\n\n", "fm")

    # Substitute basis polynomials
    w("Substituting basis polynomials:\n\n", "section")

    w("P(x) = ", "fm")
    for i in range(n):
        num_parts = [xdiff_sym("x", x[j]) for j in range(n) if j != i]
        term_str = f"{fmt(y[i])} * {''.join(num_parts)} / {fmt(denoms[i])}"
        if i == 0:
            w(term_str, "fm")
        else:
            w(f"\n       + {term_str}", "fm")
    w("\n\n")

    # Expand each term
    w("Expanding each term:\n\n", "section")

    term_polys = []
    for i in range(n):
        roots_i = [x[j] for j in range(n) if j != i]
        num_poly = poly_from_roots(roots_i)

        scalar = y[i] / denoms[i]
        scaled = poly_scale(num_poly, scalar)
        term_polys.append(scaled)

        w(f"  {fmt(y[i])}/{fmt(denoms[i])}", "hl")
        w(f" * {poly_str(num_poly)}", "fm")
        w(f"\n    = ", "fm")
        w(f"{fmt(scalar)}", "val")
        w(f" * ({poly_str(num_poly)})\n", "fm")
        w(f"    = ", "fm")
        w(f"{poly_str(scaled)}\n\n", "val")

    # Collect
    total_poly = [0.0] * n
    for tp in term_polys:
        total_poly = poly_add(total_poly, tp)

    w("Collecting all terms:\n\n", "section")
    w("P(x) = ", "fm")
    for i, tp in enumerate(term_polys):
        if i == 0:
            w(f"({poly_str(tp)})", "fm")
        else:
            w(f"\n       + ({poly_str(tp)})", "fm")
    w("\n\n")

    w("P(x) = ", "hl")
    w(f"{poly_str(total_poly)}\n\n", "result")

    # ══════════════════════════════════════
    # Step 3: Evaluate at x = xv
    # ══════════════════════════════════════
    w(f"--- Step 3: Evaluate at x = {fmt(xv)} ---\n\n", "step")

    L_vals = []
    total = 0.0

    for i in range(n):
        num = 1.0
        fac_sub  = [xdiff_num(xv, x[j]) for j in range(n) if j != i]
        fac_diffs = []
        for j in range(n):
            if j != i:
                d = xv - x[j]
                num *= d
                fac_diffs.append(d)

        Li = num / denoms[i]
        L_vals.append(Li)
        total += y[i] * Li

        w(f"L{sub(i)}({fmt(xv)})", "hl")
        w(f" = {''.join(fac_sub)} / {fmt(denoms[i])}\n", "fm")

        fac_vals = [f"({fmt(d)})" for d in fac_diffs]
        pad = " " * len(f"L{sub(i)}({fmt(xv)})")
        w(f"{pad} = {''.join(fac_vals)} / {fmt(denoms[i])}\n", "fm")
        w(f"{pad} = ", "fm")
        w(f"{fmt(Li)}\n\n", "val")

    # Final summation
    w(f"P({fmt(xv)})", "hl")
    parts = [f"{fmt(y[i])}({fmt(L_vals[i])})" for i in range(n)]
    w(f" = {' + '.join(parts)}\n", "fm")

    prods = [y[i] * L_vals[i] for i in range(n)]
    pad = " " * len(f"P({fmt(xv)})")
    w(f"{pad} = ", "fm")
    for i, p in enumerate(prods):
        if i == 0:
            w(f"{fmt(p)}", "fm")
        else:
            w(f" {signed(p)}", "fm")
    w("\n\n")

    # Result
    w("=" * 42 + "\n", "dim")
    w(f"  P({fmt(xv)}) = {fmt(total)}\n", "result")
    w("=" * 42 + "\n", "dim")

    t.config(state=tk.DISABLED)
    return total, denoms
