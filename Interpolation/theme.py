"""
Interpolation Calculator — Theme & Font Constants
"""
import platform

IS_MAC = platform.system() == "Darwin"

# Fonts
FF = "Helvetica Neue" if IS_MAC else "Segoe UI"   # UI font family
MF = "Menlo" if IS_MAC else "Consolas"             # Monospace font family

# Colors
BG        = "#F4F6F9"
CARD      = "#FFFFFF"
ACCENT    = "#1565C0"
ACCENT_LT = "#E3F2FD"
ORANGE    = "#E65100"
ORANGE_LT = "#FFF3E0"
GREEN     = "#2E7D32"
GREEN_LT  = "#E8F5E9"
RED       = "#C62828"
RED_LT    = "#FFEBEE"
FG        = "#212121"
FG2       = "#757575"
BORDER    = "#CFD8DC"
