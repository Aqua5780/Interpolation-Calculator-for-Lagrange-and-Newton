"""
Interpolation Calculator — Newton's Divided Difference (step-by-step output)
"""

import tkinter as tk
import numpy as np

from .helpers import sub, fmt, signed, xdiff_sym, xdiff_num


def render(txt_widget, x, y, xv, lagrange_result=None):
    """
    Write the full Newton DD step-by-step solution into *txt_widget*.

    Returns the evaluated result ``P(xv)``.
    """
    n = len(x)
    t = txt_widget
    t.config(state=tk.NORMAL)
    t.delete("1.0", tk.END)
    w = lambda s, tg="fm": t.insert(tk.END, s, tg)

    w("NEWTON'S DIVIDED DIFFERENCE\n", "title")
    w("=" * 52 + "\n\n", "dim")

    # ── Given Data ──
    w("Given Data Points:\n", "section")
    for i in range(n):
        w(f"  x{sub(i)} = {fmt(x[i])},   f(x{sub(i)}) = ", "fm")
        w(f"{fmt(y[i])}\n", "val")
    w(f"\nDegree of polynomial: {n - 1}\n\n")

    # ── Build Divided Difference Table ──
    dd = np.zeros((n, n))
    dd[:, 0] = y.copy()
    for j in range(1, n):
        for i in range(n - j):
            dd[i][j] = (dd[i + 1][j - 1] - dd[i][j - 1]) / (x[i + j] - x[i])

    # ══════════════════════════════════════
    # Step 1: Divided Difference Table
    # ══════════════════════════════════════
    w("--- Step 1: Divided Difference Table ---\n\n", "step")

    cw = 14
    hdrs = ["xi", "f[xi]"]
    ords = ["1st", "2nd", "3rd"]
    for j in range(1, n):
        label = ords[j - 1] if j <= 3 else f"{j}th"
        hdrs.append(f"{label} DD")

    hdr_line = " | ".join(h.center(cw) for h in hdrs)
    w(hdr_line + "\n", "thdr")
    w("-" * len(hdr_line) + "\n", "dim")

    for i in range(n):
        cells = [fmt(x[i]).center(cw), fmt(dd[i][0]).center(cw)]
        for j in range(1, n):
            if i <= n - j - 1:
                cells.append(fmt(dd[i][j]).center(cw))
            else:
                cells.append(" " * cw)
        w(" | ".join(cells) + "\n", "tcell")

    w("\n")

    # ── Detailed Calculations ──
    w("Detailed Calculations:\n\n", "section")

    for j in range(1, n):
        for i in range(n - j):
            ids = ", ".join(f"x{sub(k)}" for k in range(i, i + j + 1))
            top = ", ".join(f"x{sub(k)}" for k in range(i + 1, i + j + 1))
            bot = ", ".join(f"x{sub(k)}" for k in range(i, i + j))

            w(f"  f[{ids}]", "hl")
            w(f" = ( f[{top}] - f[{bot}] ) / ( x{sub(i + j)} - x{sub(i)} )\n", "fm")

            numer = dd[i + 1][j - 1] - dd[i][j - 1]
            denom_val = x[i + j] - x[i]
            indent = " " * (len(f"  f[{ids}]") + 3)

            w(f"{indent}= ( {fmt(dd[i + 1][j - 1])} - {fmt(dd[i][j - 1])} )"
              f" / ( {fmt(x[i + j])} - {fmt(x[i])} )\n", "fm")
            w(f"{indent}= {fmt(numer)} / {fmt(denom_val)}\n", "fm")
            w(f"{indent}= ", "fm")
            w(f"{fmt(dd[i][j])}\n\n", "val")

    # ══════════════════════════════════════
    # Step 2: Newton's Polynomial
    # ══════════════════════════════════════
    w("--- Step 2: Newton's Polynomial ---\n\n", "step")

    # Symbolic form
    w(f"P(x) = f[x{sub(0)}]", "fm")
    for j in range(1, n):
        ids = ", ".join(f"x{sub(k)}" for k in range(j + 1))
        facs = "".join(f"(x - x{sub(k)})" for k in range(j))
        w(f"\n       + f[{ids}] * {facs}", "fm")
    w("\n\n")

    # With numerical values
    w(f"P(x) = {fmt(dd[0][0])}", "val")
    for j in range(1, n):
        c = dd[0][j]
        s = "+" if c >= 0 else "-"
        facs = "".join(xdiff_sym("x", x[k]) for k in range(j))
        w(f" {s} {fmt(abs(c))}{facs}", "val")
    w("\n\n")

    # ══════════════════════════════════════
    # Step 3: Evaluate at x = xv
    # ══════════════════════════════════════
    w(f"--- Step 3: Evaluate at x = {fmt(xv)} ---\n\n", "step")

    # Symbolic substitution
    w(f"P({fmt(xv)}) = {fmt(dd[0][0])}", "fm")
    for j in range(1, n):
        c = dd[0][j]
        s = "+" if c >= 0 else "-"
        facs = "".join(xdiff_num(xv, x[k]) for k in range(j))
        w(f"\n         {s} {fmt(abs(c))} * {facs}", "fm")
    w("\n\n")

    # Computed factor values
    w(f"       = {fmt(dd[0][0])}", "fm")
    for j in range(1, n):
        c = dd[0][j]
        s = "+" if c >= 0 else "-"
        fac_vals = "".join(f"({fmt(xv - x[k])})" for k in range(j))
        w(f"\n         {s} {fmt(abs(c))} * {fac_vals}", "fm")
    w("\n\n")

    # Individual term values
    cum = 1.0
    result = dd[0][0]
    terms = [dd[0][0]]
    for j in range(1, n):
        cum *= (xv - x[j - 1])
        tv = dd[0][j] * cum
        terms.append(tv)
        result += tv

    w("       = ", "fm")
    for i, tv in enumerate(terms):
        if i == 0:
            w(f"{fmt(tv)}", "fm")
        else:
            w(f" {signed(tv)}", "fm")
    w("\n\n")

    # ── Result ──
    w("=" * 42 + "\n", "dim")
    w(f"  P({fmt(xv)}) = {fmt(result)}\n", "result")
    w("=" * 42 + "\n", "dim")

    # Cross-verification against Lagrange
    if lagrange_result is not None:
        if abs(result - lagrange_result) < 1e-8:
            w(f"\n  [check] Both methods agree: P({fmt(xv)}) = {fmt(result)}\n", "ok")
        else:
            diff = abs(result - lagrange_result)
            w(f"\n  Note: Lagrange={fmt(lagrange_result)}, "
              f"Newton={fmt(result)}, diff={fmt(diff)}\n", "fm")

    t.config(state=tk.DISABLED)
    return result
