"""
Interpolation Calculator — Desmos-style Graph (matplotlib popup)
"""

import tkinter as tk
import numpy as np

from .theme import CARD
from .helpers import fmt

try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
    from matplotlib.figure import Figure
    import matplotlib.ticker as mticker
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


# ── Desmos-inspired palette ──────────────────────────────────
_BG        = "#FFFFFF"
_GRID      = "#E0E0E0"
_GRID_FINE = "#F0F0F0"
_AXIS      = "#999999"
_CURVE     = "#2D70B3"     # Desmos blue
_POINT     = "#FA7E19"     # Desmos orange
_EVAL      = "#C74440"     # Desmos red
_LABEL_FG  = "#333333"
_FONT      = "sans-serif"


def _poly_str_latex(coeffs):
    """Build a LaTeX string from coefficient list [const, x, x², …]."""
    deg = len(coeffs) - 1
    parts = []
    for k in range(deg, -1, -1):
        c = coeffs[k]
        if abs(c) < 1e-14:
            continue
        cv = fmt(abs(c))
        is_leading = not parts
        sign = "" if (is_leading and c >= 0) else ("+" if c >= 0 else "-")
        if not is_leading:
            sign = f" {sign} "
        if k == 0:
            parts.append(f"{sign}{cv}")
        elif k == 1:
            parts.append(f"{sign}{cv if cv != '1' else ''}x")
        else:
            parts.append(f"{sign}{cv if cv != '1' else ''}x^{{{k}}}")
    return "".join(parts) if parts else "0"


def show(master, x, y, xv):
    """Open a Toplevel window with a Desmos-style interactive graph."""
    if not HAS_MATPLOTLIB:
        from tkinter import messagebox
        messagebox.showwarning("Missing Library", "matplotlib is required for graphing.")
        return

    n = len(x)

    # ── Build DD table & polynomial evaluator ──
    dd = np.zeros((n, n))
    dd[:, 0] = y.copy()
    for j in range(1, n):
        for i in range(n - j):
            dd[i][j] = (dd[i + 1][j - 1] - dd[i][j - 1]) / (x[i + j] - x[i])

    # Collect full polynomial coefficients for display
    poly_coeffs = [0.0] * n
    # Term 0: constant
    term = [dd[0][0]]
    for i in range(len(term)):
        if i < n:
            poly_coeffs[i] += term[i]
    basis = [1.0]
    for j in range(1, n):
        basis = _poly_mul(basis, [-x[j - 1], 1.0])
        scaled = [c * dd[0][j] for c in basis]
        for i in range(len(scaled)):
            if i < n:
                poly_coeffs[i] += scaled[i]

    def poly_eval(xp):
        r = dd[0][0]
        prod = 1.0
        for j in range(1, n):
            prod *= (xp - x[j - 1])
            r += dd[0][j] * prod
        return r

    # ── Plot range ──
    x_span = max(x) - min(x) if max(x) != min(x) else 2.0
    margin_x = x_span * 0.5
    x_lo, x_hi = min(x) - margin_x, max(x) + margin_x

    xp = np.linspace(x_lo, x_hi, 800)
    yp = np.array([poly_eval(xi) for xi in xp])
    yv_eval = poly_eval(xv)

    all_y = np.concatenate([yp, y, [yv_eval]])
    y_span = max(all_y) - min(all_y) if max(all_y) != min(all_y) else 2.0
    margin_y = y_span * 0.15
    y_lo, y_hi = min(all_y) - margin_y, max(all_y) + margin_y

    # ── Create window ──
    win = tk.Toplevel(master)
    win.title("Interpolation Graph")
    win.geometry("920x640")
    win.configure(bg=_BG)

    fig = Figure(figsize=(9.2, 6.0), dpi=100, facecolor=_BG)
    ax = fig.add_subplot(111)
    ax.set_facecolor(_BG)

    # ── Grid (Desmos style: light minor + slightly darker major) ──
    ax.grid(True, which="major", color=_GRID, linewidth=0.7, zorder=0)
    ax.grid(True, which="minor", color=_GRID_FINE, linewidth=0.4, zorder=0)
    ax.minorticks_on()

    # ── Axes through origin ──
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.axhline(0, color=_AXIS, linewidth=1.0, zorder=1)
    ax.axvline(0, color=_AXIS, linewidth=1.0, zorder=1)

    # ── Tick styling ──
    ax.tick_params(axis="both", which="major", labelsize=9, colors=_AXIS,
                   direction="in", length=0)
    ax.tick_params(axis="both", which="minor", length=0)

    # ── Polynomial curve ──
    ax.plot(xp, yp, color=_CURVE, linewidth=2.8, solid_capstyle="round",
            zorder=3, label=f"$P(x)$")

    # ── Data points ──
    for i in range(n):
        ax.plot(x[i], y[i], "o", color=_POINT, markersize=10, zorder=5,
                markeredgecolor="white", markeredgewidth=2.0)
        ax.annotate(f"({fmt(x[i])}, {fmt(y[i])})",
                    xy=(x[i], y[i]), xytext=(8, 10),
                    textcoords="offset points",
                    fontsize=9, fontfamily=_FONT, color=_POINT, fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                              edgecolor=_POINT, alpha=0.9, linewidth=0.8),
                    zorder=7)

    # ── Evaluated point ──
    ax.plot(xv, yv_eval, "o", color=_EVAL, markersize=12, zorder=6,
            markeredgecolor="white", markeredgewidth=2.5)
    ax.annotate(f"P({fmt(xv)}) = {fmt(yv_eval)}",
                xy=(xv, yv_eval), xytext=(10, -18),
                textcoords="offset points",
                fontsize=10, fontfamily=_FONT, color=_EVAL, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFF0EF",
                          edgecolor=_EVAL, alpha=0.95, linewidth=1.0),
                arrowprops=dict(arrowstyle="-", color=_EVAL, lw=0.8),
                zorder=8)

    # ── Dashed lines from eval point to axes ──
    ax.plot([xv, xv], [0, yv_eval], "--", color=_EVAL, linewidth=0.8,
            alpha=0.5, zorder=2)
    ax.plot([0, xv], [yv_eval, yv_eval], "--", color=_EVAL, linewidth=0.8,
            alpha=0.5, zorder=2)

    # ── Special points (Desmos-style) ─────────────────────────

    _SPECIAL  = "#388E3C"   # green for special points
    _SP_BG    = "#E8F5E9"

    # Helper: check if a special point overlaps an existing data/eval point
    existing = set()
    for i in range(n):
        existing.add((round(x[i], 8), round(y[i], 8)))
    existing.add((round(xv, 8), round(yv_eval, 8)))

    def _is_new(px, py):
        return (round(px, 8), round(py, 8)) not in existing

    def _mark(px, py, label, offset=(8, -14)):
        ax.plot(px, py, "o", color=_SPECIAL, markersize=7, zorder=5,
                markeredgecolor="white", markeredgewidth=1.5)
        ax.annotate(label, xy=(px, py), xytext=offset,
                    textcoords="offset points",
                    fontsize=8, fontfamily=_FONT, color=_SPECIAL, fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.2", facecolor=_SP_BG,
                              edgecolor=_SPECIAL, alpha=0.9, linewidth=0.6),
                    zorder=7)

    # Y-intercept: P(0)
    if x_lo <= 0 <= x_hi:
        y_int = poly_eval(0)
        if y_lo <= y_int <= y_hi and _is_new(0, y_int):
            _mark(0, y_int, f"(0, {fmt(y_int)})", offset=(8, 8))

    # X-intercepts (roots): find sign changes in the dense curve
    roots_found = []
    for k in range(len(xp) - 1):
        if yp[k] * yp[k + 1] < 0:
            # Linear interpolation to approximate root
            rx = xp[k] - yp[k] * (xp[k + 1] - xp[k]) / (yp[k + 1] - yp[k])
            # Newton refinement (a few iterations)
            for _ in range(20):
                fv = poly_eval(rx)
                # Numerical derivative
                h = 1e-8
                fp = (poly_eval(rx + h) - fv) / h
                if abs(fp) < 1e-15:
                    break
                rx -= fv / fp
            if x_lo <= rx <= x_hi and abs(poly_eval(rx)) < 1e-6:
                # Avoid duplicates
                if all(abs(rx - prev) > 0.05 for prev in roots_found):
                    roots_found.append(rx)
                    if _is_new(rx, 0):
                        _mark(rx, 0, f"({fmt(rx)}, 0)")

    # Local maxima & minima: find where derivative changes sign
    dy = np.diff(yp)
    for k in range(len(dy) - 1):
        if dy[k] * dy[k + 1] < 0:
            # Approximate extremum x
            ex = xp[k + 1]
            ey = yp[k + 1]
            # Refine with neighbours
            if k + 2 < len(xp):
                # Parabolic fit around the 3 points
                x0, x1, x2 = xp[k], xp[k + 1], xp[k + 2]
                y0, y1, y2 = yp[k], yp[k + 1], yp[k + 2]
                denom = (x0 - x1) * (x0 - x2) * (x1 - x2)
                if abs(denom) > 1e-15:
                    a_coef = (x2 * (y1 - y0) + x1 * (y0 - y2) + x0 * (y2 - y1)) / denom
                    b_coef = (x2**2 * (y0 - y1) + x1**2 * (y2 - y0) + x0**2 * (y1 - y2)) / denom
                    if abs(a_coef) > 1e-15:
                        ex = -b_coef / (2 * a_coef)
                        ey = poly_eval(ex)
            if x_lo <= ex <= x_hi and y_lo <= ey <= y_hi and _is_new(ex, ey):
                kind = "max" if dy[k] > 0 else "min"
                _mark(ex, ey, f"({fmt(ex)}, {fmt(ey)})", offset=(8, 10 if kind == "max" else -14))

    # ── Polynomial expression in top-left ──
    latex_eq = _poly_str_latex(poly_coeffs)
    ax.text(0.03, 0.96, f"$P(x) = {latex_eq}$",
            transform=ax.transAxes, fontsize=11, fontfamily=_FONT,
            verticalalignment="top",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="white",
                      edgecolor=_GRID, alpha=0.92, linewidth=0.8),
            color=_CURVE, zorder=9)

    # ── Degree label ──
    ax.text(0.03, 0.88, f"Degree {n - 1} polynomial  ·  {n} data points",
            transform=ax.transAxes, fontsize=8.5, fontfamily=_FONT,
            color="#999999", zorder=9)

    # ── Limits ──
    ax.set_xlim(x_lo, x_hi)
    ax.set_ylim(y_lo, y_hi)

    fig.tight_layout(pad=0.8)

    # ── Embed in Tk ──
    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # Navigation toolbar (zoom/pan like Desmos)
    toolbar_frame = tk.Frame(win, bg=_BG)
    toolbar_frame.pack(fill="x")
    toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
    toolbar.update()


def _poly_mul(a, b):
    """Local poly multiply (avoids circular import)."""
    n = len(a) + len(b) - 1
    c = [0.0] * n
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            c[i + j] += ai * bj
    return c
