"""
Allow running as:
    python -m Interpolation          (from parent directory)
    python Interpolation/__main__.py (direct script)
"""
import sys, os

# When executed directly, the package isn't on sys.path yet.
if __package__ is None or __package__ == "":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    __package__ = "Interpolation"

from .main import main

main()
