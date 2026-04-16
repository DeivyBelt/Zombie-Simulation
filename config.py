# ============================================================
#  config.py — Constantes globales de la simulación
# ============================================================

HUMANO = 0
ZOMBIE = 1
MUERTO = 2

GRID_SIZE_DEFAULT        = 40
CELL_SIZE                = 16
PANEL_WIDTH              = 260
FPS                      = 12

PROB_INFECCION_DEFAULT   = 0.3
TIEMPO_MUERTE_DEFAULT    = 6
PORC_ZOMBIES_DEFAULT     = 10

COLOR_BG           = (15, 15, 20)
COLOR_PANEL        = (20, 22, 28)
COLOR_GRID_LINE    = (30, 35, 40)
COLOR_HUMANO       = (46, 204, 113)
COLOR_ZOMBIE       = (231, 76, 60)
COLOR_MUERTO       = (80, 85, 95)
COLOR_TEXT         = (220, 220, 220)
COLOR_TEXT_DIM     = (120, 120, 130)
COLOR_ACCENT       = (52, 152, 219)
COLOR_INPUT_BG     = (30, 33, 42)
COLOR_INPUT_BORDER = (60, 65, 80)
COLOR_INPUT_ACTIVE = (52, 152, 219)

import os as _os
_BASE_DIR = _os.path.dirname(_os.path.abspath(__file__))
ASSET_ZOMBIE = _os.path.join(_BASE_DIR, "assets", "zombie.png")
ASSET_HUMANO = _os.path.join(_BASE_DIR, "assets", "humano.png")
ASSET_MUERTO = _os.path.join(_BASE_DIR, "assets", "muerto.png")
