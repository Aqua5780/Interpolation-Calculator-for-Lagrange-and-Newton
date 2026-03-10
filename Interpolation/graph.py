"""
Interpolation Calculator — Graph (matplotlib popup)
"""

import tkinter as tk
import numpy as np

from .theme import CARD, ACCENT, ORANGE, RED
from .helpers import fmt

try:
    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


def show(master, x, y, xv):
    """
    Open a Toplevel window showing the interpolating polynomial, data points,
    and the evaluated point ``P(xv)``.
    """
    if not HAS_MATPLOTLIB:
        from tkinter import messagebox
        messagebox.showwarning("Missing Library", "matplotlib is required for graphing.")
        return

    n = len(x)

    # Build DD table for polynomial evaluation
    dd = np.zeros((n, n))
    dd[:, 0] = y.copy()
    for j in range(1, n):
        for i in range(n - j):
            dd[i][j] = (dd[i + 1][j - 1] - dd[i][j - 1]) / (x[i + j] - x[i])

    def poly_eval(xp):
        r = dd[0][0]
        prod = 1.0
        for j in range(1, n):
            prod *= (xp - x[j - 1])
            r += dd[0][j] * prod
        return r

    # Plot range
    margin = (max(x) - min(x)) * 0.35 + 0.5
    xp = np.linspace(min(x) - margin, max(x) + margin, 400)
    yp = np.array([poly_eval(xi) for xi in xp])
    yv_eval = poly_eval(xv)

    # Create popup window
    win = tk.Toplevel(master)
    win.title("Interpolation Graph")
    win.geometry("780x540")
    win.configure(bg=CARD)

    fig = Figure(figsize=(7.8, 5.2), dpi=100, facecolor=CARD)
    ax = fig.add_subplot(111)

    ax.plot(xp, yp, "-", color=ACCENT, linewidth=2.2, label="P(x)", zorder=3)
    ax.plot(x, y, "o", color=ORANGE, markersize=9, zorder=5,
            markeredgecolor="white", markeredgewidth=1.5, label="Data points")
    ax.plot(xv, yv_eval, "s", color=RED, markersize=11, zorder=6,
            markeredgecolor="white", markeredgewidth=1.5,
            label=f"P({fmt(xv)}) = {fmt(yv_eval)}")

    ax.set_xlabel("x", fontsize=11)
    ax.set_ylabel("P(x)", fontsize=11)
    ax.set_title(f"Interpolating Polynomial (degree {n - 1})",
                 fontsize=13, fontweight="bold")
    ax.legend(fontsize=10, loc="best")
    ax.grid(True, alpha=0.25, linestyle="--")
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
