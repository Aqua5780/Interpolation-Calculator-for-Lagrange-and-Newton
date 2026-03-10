"""
Interpolation Calculator — Main Application Window
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

from .theme import (
    IS_MAC, FF, MF, BG, CARD, ACCENT, ACCENT_LT,
    ORANGE, ORANGE_LT, GREEN, GREEN_LT,
    RED, RED_LT, FG, FG2, BORDER,
)
from . import lagrange, newton, graph
from .graph import HAS_MATPLOTLIB


class InterpolationApp:
    """Top-level GUI controller."""

    def __init__(self, master):
        self.master = master
        master.title("Interpolation Calculator")
        master.geometry("1520x920")
        master.configure(bg=BG)
        master.minsize(1100, 700)

        self.entries = []            # [(x_entry, y_entry, row_frame), …]
        self._result_lagrange = None
        self._result_newton = None
        self._data_cache = None

        self._build()
        self._load_example1()

    # ══════════════════════════════════════
    # UI Construction
    # ══════════════════════════════════════
    def _build(self):
        # ── Title Bar ──
        bar = tk.Frame(self.master, bg=ACCENT, height=44)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        tk.Label(bar, text="   Interpolation Calculator",
                 font=(FF, 14, "bold"), bg=ACCENT, fg="white").pack(side="left", padx=4)
        tk.Label(bar, text="Lagrange  &  Newton Divided Difference",
                 font=(FF, 10), bg=ACCENT, fg="#BBDEFB").pack(side="left", padx=10)

        # ── Input Card ──
        inp_wrap = tk.Frame(self.master, bg=BG, padx=12, pady=8)
        inp_wrap.pack(fill="x")

        card = tk.Frame(inp_wrap, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        card.pack(fill="x")

        inner = tk.Frame(card, bg=CARD, padx=16, pady=10)
        inner.pack(fill="x")

        # Left — data points
        left = tk.Frame(inner, bg=CARD)
        left.pack(side="left", fill="both", expand=True)

        tk.Label(left, text="Data Points", font=(FF, 12, "bold"),
                 bg=CARD, fg=FG).pack(anchor="w")

        hdr = tk.Frame(left, bg=CARD)
        hdr.pack(fill="x", pady=(4, 0))
        tk.Label(hdr, text="#", font=(FF, 9, "bold"), bg=CARD,
                 fg=FG2, width=4, anchor="center").pack(side="left")
        tk.Label(hdr, text="x", font=(FF, 10, "bold"), bg=CARD,
                 fg=ACCENT, width=14, anchor="center").pack(side="left", padx=2)
        tk.Label(hdr, text="f(x)", font=(FF, 10, "bold"), bg=CARD,
                 fg=ACCENT, width=14, anchor="center").pack(side="left", padx=2)

        # Scrollable frame for data points
        pts_outer = tk.Frame(left, bg=CARD, height=120)
        pts_outer.pack(fill="x")
        pts_outer.pack_propagate(False)

        pts_canvas = tk.Canvas(pts_outer, bg=CARD, highlightthickness=0)
        pts_scroll = ttk.Scrollbar(pts_outer, orient="vertical", command=pts_canvas.yview)
        pts_canvas.configure(yscrollcommand=pts_scroll.set)
        pts_canvas.pack(side="left", fill="both", expand=True)
        pts_scroll.pack(side="right", fill="y")

        self.pts_frame = tk.Frame(pts_canvas, bg=CARD)
        self._pts_window = pts_canvas.create_window((0, 0), window=self.pts_frame, anchor="nw")
        self._pts_canvas = pts_canvas

        self.pts_frame.bind(
            "<Configure>",
            lambda e: pts_canvas.config(scrollregion=pts_canvas.bbox("all")),
        )

        # Right — controls
        right = tk.Frame(inner, bg=CARD, padx=24)
        right.pack(side="right", fill="y")

        tk.Label(right, text="Evaluate P(x) at:", font=(FF, 10, "bold"),
                 bg=CARD, fg=FG).pack(anchor="w")

        ev = tk.Frame(right, bg=CARD)
        ev.pack(anchor="w", pady=(2, 10))
        tk.Label(ev, text="x =", font=(FF, 11, "bold"), bg=CARD, fg=ACCENT).pack(side="left")
        self.x_eval_entry = tk.Entry(ev, width=10, font=(FF, 11), relief="solid", bd=1,
                                     bg="white", fg=FG, insertbackground=FG)
        self.x_eval_entry.pack(side="left", padx=4)
        self.x_eval_entry.bind("<Return>", lambda e: self._compute())

        # Compute button (label-based so colours work on macOS)
        comp_frame = tk.Frame(right, bg="#1B5E20", cursor="hand2")
        comp_frame.pack(fill="x", pady=(0, 8))
        comp_label = tk.Label(comp_frame, text="   Compute   ", font=(FF, 11, "bold"),
                              bg="#1B5E20", fg="white", padx=16, pady=6)
        comp_label.pack(fill="x")
        for w in (comp_frame, comp_label):
            w.bind("<Enter>", lambda e: comp_label.config(bg="#2E7D32") or comp_frame.config(bg="#2E7D32"))
            w.bind("<Leave>", lambda e: comp_label.config(bg="#1B5E20") or comp_frame.config(bg="#1B5E20"))
            w.bind("<Button-1>", lambda e: self._compute())

        # Small buttons row 1
        r1 = tk.Frame(right, bg=CARD)
        r1.pack(fill="x", pady=2)
        self._btn(r1, "+ Add Point", ACCENT_LT, ACCENT, self._add_point).pack(side="left", padx=2)
        self._btn(r1, "- Remove", RED_LT, RED, self._rm_point).pack(side="left", padx=2)
        self._btn(r1, "Clear All", "#ECEFF1", FG2, self._clear_all).pack(side="left", padx=2)

        # Small buttons row 2
        r2 = tk.Frame(right, bg=CARD)
        r2.pack(fill="x", pady=2)
        self._btn(r2, "Example 1", ORANGE_LT, ORANGE, self._load_example1).pack(side="left", padx=2)
        self._btn(r2, "Example 2", ORANGE_LT, ORANGE, self._load_example2).pack(side="left", padx=2)
        if HAS_MATPLOTLIB:
            self._btn(r2, "Show Graph", GREEN_LT, GREEN, self._graph).pack(side="left", padx=2)

        # ── Results Section (side-by-side) ──
        res_wrap = tk.Frame(self.master, bg=BG, padx=12)
        res_wrap.pack(fill="both", expand=True, pady=(0, 12))

        paned = tk.PanedWindow(res_wrap, orient="horizontal", bg=BORDER, sashwidth=3)
        paned.pack(fill="both", expand=True)

        self.lag_txt = self._make_panel(paned, "LAGRANGE INTERPOLATION", ACCENT_LT, ACCENT)
        self.new_txt = self._make_panel(paned, "NEWTON'S DIVIDED DIFFERENCE", ORANGE_LT, ORANGE)

        # Place sash at 50 / 50 after the window is drawn
        self.master.update_idletasks()
        total_w = paned.winfo_width() or 1496
        paned.sash_place(0, int(total_w * 0.5), 0)

    # ── widget helpers ───────────────────────────────────────

    def _btn(self, parent, text, bg_c, fg_c, cmd):
        return tk.Button(parent, text=text, font=(FF, 9), bg=bg_c, fg=fg_c,
                         activebackground=bg_c, relief="flat", padx=8, pady=3,
                         command=cmd, cursor="hand2")

    def _make_panel(self, paned, title, hdr_bg, hdr_fg):
        """Create a result panel with header + scrollable text area."""
        frame = tk.Frame(paned, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        paned.add(frame, minsize=450)

        h = tk.Frame(frame, bg=hdr_bg, padx=12, pady=6)
        h.pack(fill="x")
        tk.Label(h, text=title, font=(FF, 11, "bold"), bg=hdr_bg, fg=hdr_fg).pack(anchor="w")

        tf = tk.Frame(frame, bg=CARD)
        tf.pack(fill="both", expand=True)

        txt = tk.Text(tf, font=(MF, 10), bg=CARD, fg=FG, wrap="none",
                      relief="flat", padx=12, pady=8, insertbackground=FG,
                      spacing1=1, spacing3=1)
        txt.pack(fill="both", expand=True)

        # Mouse-wheel scrolling on hover (vertical + horizontal with Shift)
        def _on_enter(e):
            if IS_MAC:
                txt.bind_all("<MouseWheel>", lambda ev: txt.yview_scroll(-1 * ev.delta, "units"))
                txt.bind_all("<Shift-MouseWheel>", lambda ev: txt.xview_scroll(-1 * ev.delta, "units"))
            else:
                txt.bind_all("<MouseWheel>", lambda ev: txt.yview_scroll(int(-1 * (ev.delta / 120)), "units"))
                txt.bind_all("<Shift-MouseWheel>", lambda ev: txt.xview_scroll(int(-1 * (ev.delta / 120)), "units"))

        def _on_leave(e):
            txt.unbind_all("<MouseWheel>")
            txt.unbind_all("<Shift-MouseWheel>")

        txt.bind("<Enter>", _on_enter)
        txt.bind("<Leave>", _on_leave)

        # Formatting tags
        txt.tag_configure("title",   font=(MF, 12, "bold"), foreground=hdr_fg)
        txt.tag_configure("section", font=(MF, 10, "bold"), foreground="#37474F")
        txt.tag_configure("step",    font=(MF, 10, "bold"), foreground="#00695C")
        txt.tag_configure("fm",      font=(MF, 10),         foreground="#263238")
        txt.tag_configure("hl",      font=(MF, 10, "bold"), foreground=ACCENT)
        txt.tag_configure("val",     font=(MF, 10, "bold"), foreground="#6A1B9A")
        txt.tag_configure("result",  font=(MF, 12, "bold"), foreground=RED,
                          background="#FFF8E1", spacing1=4, spacing3=4)
        txt.tag_configure("thdr",    font=(MF, 9, "bold"),  foreground="#37474F")
        txt.tag_configure("tcell",   font=(MF, 9),          foreground="#455A64")
        txt.tag_configure("dim",     font=(MF, 9),          foreground="#9E9E9E")
        txt.tag_configure("ok",      font=(MF, 10, "bold"), foreground=GREEN)
        txt.config(state=tk.DISABLED)
        return txt

    # ══════════════════════════════════════
    # Data Point Management
    # ══════════════════════════════════════
    def _add_point(self, xv="", yv=""):
        i = len(self.entries)
        row = tk.Frame(self.pts_frame, bg=CARD)
        row.pack(fill="x", pady=1)

        tk.Label(row, text=str(i), font=(FF, 9), bg=CARD, fg=FG2,
                 width=4, anchor="center").pack(side="left")

        xe = tk.Entry(row, width=14, font=(FF, 10), relief="solid", bd=1,
                      bg="white", fg=FG, insertbackground=FG)
        xe.pack(side="left", padx=2)
        if xv != "":
            xe.insert(0, str(xv))
        xe.bind("<Return>", lambda e: self._compute())

        ye = tk.Entry(row, width=14, font=(FF, 10), relief="solid", bd=1,
                      bg="white", fg=FG, insertbackground=FG)
        ye.pack(side="left", padx=2)
        if yv != "":
            ye.insert(0, str(yv))
        ye.bind("<Return>", lambda e: self._compute())

        self.entries.append((xe, ye, row))

    def _rm_point(self):
        if len(self.entries) <= 2:
            messagebox.showwarning("Minimum Points", "At least 2 data points are required.")
            return
        _, _, row = self.entries.pop()
        row.destroy()

    def _clear_quiet(self):
        for _, _, row in self.entries:
            row.destroy()
        self.entries.clear()
        self.x_eval_entry.delete(0, tk.END)

    def _clear_all(self):
        self._clear_quiet()
        for t in (self.lag_txt, self.new_txt):
            t.config(state=tk.NORMAL)
            t.delete("1.0", tk.END)
            t.config(state=tk.DISABLED)
        for _ in range(3):
            self._add_point()

    def _load_example1(self):
        """Paper problem 3: (1,2.3), (3,4.2), (4,3.3)  eval x=2.5"""
        self._clear_quiet()
        for xv, yv in [(1, 2.3), (3, 4.2), (4, 3.3)]:
            self._add_point(xv, yv)
        self.x_eval_entry.insert(0, "2.5")

    def _load_example2(self):
        """Paper left side: (1,2.5), (3,5.7), (6,4.1)"""
        self._clear_quiet()
        for xv, yv in [(1, 2.5), (3, 5.7), (6, 4.1)]:
            self._add_point(xv, yv)
        self.x_eval_entry.insert(0, "2.5")

    # ══════════════════════════════════════
    # Read & Validate Input
    # ══════════════════════════════════════
    def _read(self):
        xs, ys = [], []
        for i, (xe, ye, _) in enumerate(self.entries):
            try:
                xs.append(float(xe.get()))
                ys.append(float(ye.get()))
            except ValueError:
                messagebox.showerror("Input Error",
                                     f"Point {i}: please enter valid numbers for x and f(x).")
                return None, None
        if len(xs) < 2:
            messagebox.showerror("Input Error", "Need at least 2 data points.")
            return None, None
        if len(set(xs)) != len(xs):
            messagebox.showerror("Input Error", "All x-values must be distinct.")
            return None, None
        return np.array(xs), np.array(ys)

    # ══════════════════════════════════════
    # Compute
    # ══════════════════════════════════════
    def _compute(self):
        x, y = self._read()
        if x is None:
            return
        try:
            xv = float(self.x_eval_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Enter a valid number for 'Evaluate at x'.")
            return

        self._data_cache = (x, y, xv)

        # Run Lagrange
        self._result_lagrange, _ = lagrange.render(self.lag_txt, x, y, xv)

        # Run Newton (pass Lagrange result for cross-check)
        self._result_newton = newton.render(self.new_txt, x, y, xv,
                                            lagrange_result=self._result_lagrange)

    # ══════════════════════════════════════
    # Graph
    # ══════════════════════════════════════
    def _graph(self):
        if self._data_cache is None:
            messagebox.showinfo("Graph", "Click 'Compute' first, then open the graph.")
            return
        x, y, xv = self._data_cache
        graph.show(self.master, x, y, xv)
