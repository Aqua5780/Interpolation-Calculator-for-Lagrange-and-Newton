#!/usr/bin/env python3
"""
Interpolation Calculator — Entry Point

Usage:
    python -m Interpolation
      or
    python Interpolation/main.py
"""

import tkinter as tk
from .app import InterpolationApp


def main():
    root = tk.Tk()
    InterpolationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
