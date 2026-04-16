# ============================================================
#  ui.py — Pantalla de menú / configuración inicial
# ============================================================

import pygame
from config import (
    GRID_SIZE_DEFAULT, PROB_INFECCION_DEFAULT,
    TIEMPO_MUERTE_DEFAULT, PORC_ZOMBIES_DEFAULT,
    COLOR_BG, COLOR_PANEL, COLOR_TEXT, COLOR_TEXT_DIM,
    COLOR_ACCENT, COLOR_ZOMBIE, COLOR_HUMANO,
    COLOR_INPUT_BG, COLOR_INPUT_BORDER, COLOR_INPUT_ACTIVE,
)


# ──────────────────────────────────────────────────────────────
#  Widget: campo de texto numérico
# ──────────────────────────────────────────────────────────────

class InputField:
    """Campo de texto numérico simple hecho con pygame."""

    def __init__(self, rect: pygame.Rect, label: str,
                 default: str, hint: str = ""):
        self.rect    = rect
        self.label   = label
        self.text    = default
        self.hint    = hint
        self.active  = False
        self.font    = pygame.font.SysFont("monospace", 15)
        self.lbl_fnt = pygame.font.SysFont("monospace", 13)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Retorna True si el campo capturó el evento."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            return self.active

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isdigit() or (
                    event.unicode == "." and "." not in self.text):
                if len(self.text) < 8:
                    self.text += event.unicode
            return True
        return False

    def draw(self, surface: pygame.Surface):
        # Etiqueta
        lbl = self.lbl_fnt.render(self.label, True, COLOR_TEXT_DIM)
        surface.blit(lbl, (self.rect.x, self.rect.y - 20))

        # Caja
        border_color = COLOR_INPUT_ACTIVE if self.active else COLOR_INPUT_BORDER
        pygame.draw.rect(surface, COLOR_INPUT_BG, self.rect, border_radius=6)
        pygame.draw.rect(surface, border_color, self.rect, 1, border_radius=6)

        # Texto interior
        display = self.text if self.text else self.hint
        color   = COLOR_TEXT if self.text else COLOR_TEXT_DIM
        txt_surf = self.font.render(display, True, color)
        surface.blit(txt_surf, (self.rect.x + 10,
                                self.rect.y + (self.rect.h - txt_surf.get_height()) // 2))

        # Cursor parpadeante
        if self.active and pygame.time.get_ticks() % 1000 < 500:
            cx = self.rect.x + 10 + txt_surf.get_width() + 2
            cy = self.rect.y + 6
            pygame.draw.line(surface, COLOR_ACCENT,
                             (cx, cy), (cx, self.rect.y + self.rect.h - 6), 1)

    @property
    def value(self) -> str:
        return self.text


# ──────────────────────────────────────────────────────────────
#  Widget: botón
# ──────────────────────────────────────────────────────────────

class Button:
    def __init__(self, rect: pygame.Rect, label: str, color=None):
        self.rect   = rect
        self.label  = label
        self.color  = color or COLOR_ACCENT
        self.hover  = False
        self.font   = pygame.font.SysFont("monospace", 16, bold=True)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.rect.collidepoint(event.pos)
        return False

    def draw(self, surface: pygame.Surface):
        color = tuple(min(c + 30, 255) for c in self.color) if self.hover else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        lbl = self.font.render(self.label, True, (255, 255, 255))
        surface.blit(lbl, lbl.get_rect(center=self.rect.center))


# ──────────────────────────────────────────────────────────────
#  Pantalla de menú
# ──────────────────────────────────────────────────────────────

class MenuScreen:
    """
    Pantalla inicial con inputs configurables y botón de inicio.
    Retorna un dict con los parámetros cuando el usuario pulsa Iniciar.
    """

    WIDTH  = 520
    HEIGHT = 560

    def __init__(self):
        self.surface = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Zombie Simulation — Configuración")

        self.font_title = pygame.font.SysFont("monospace", 28, bold=True)
        self.font_sub   = pygame.font.SysFont("monospace", 12)

        cx = self.WIDTH // 2
        fw, fh = 300, 38     # campo ancho / alto

        self.fields = [
            InputField(pygame.Rect(cx - fw // 2, 190, fw, fh),
                       "Tamaño del grid (celdas por lado)",
                       str(GRID_SIZE_DEFAULT), "ej: 40"),
            InputField(pygame.Rect(cx - fw // 2, 270, fw, fh),
                       "Probabilidad de infección  (0.0 – 1.0)",
                       str(PROB_INFECCION_DEFAULT), "ej: 0.3"),
            InputField(pygame.Rect(cx - fw // 2, 350, fw, fh),
                       "Tiempo de muerte (pasos)",
                       str(TIEMPO_MUERTE_DEFAULT), "ej: 6"),
            InputField(pygame.Rect(cx - fw // 2, 430, fw, fh),
                       "Zombies iniciales  (%)",
                       str(PORC_ZOMBIES_DEFAULT), "ej: 10"),
        ]

        self.btn_start = Button(
            pygame.Rect(cx - 100, 498, 200, 42),
            "▶  Iniciar simulación",
            COLOR_ZOMBIE,
        )
        self.error_msg = ""

    # ----------------------------------------------------------

    def run(self) -> dict | None:
        """
        Bloquea hasta que el usuario pulsa Iniciar o cierra la ventana.
        Retorna un dict con los parámetros o None si cerró.
        """
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None

                for field in self.fields:
                    field.handle_event(event)

                if self.btn_start.handle_event(event):
                    params = self._parse()
                    if params:
                        return params

            self._draw()
            pygame.display.flip()
            clock.tick(60)

    # ----------------------------------------------------------

    def _parse(self) -> dict | None:
        """Valida y convierte los valores de los campos."""
        try:
            size   = int(self.fields[0].value)
            prob   = float(self.fields[1].value)
            tdeath = int(self.fields[2].value)
            porc   = float(self.fields[3].value)

            assert 5 <= size <= 100,      "Grid: entre 5 y 100"
            assert 0.0 < prob <= 1.0,     "Infección: entre 0.01 y 1.0"
            assert 1 <= tdeath <= 50,     "T. muerte: entre 1 y 50"
            assert 1.0 <= porc <= 90.0,   "Zombies: entre 1% y 90%"

            self.error_msg = ""
            return {
                "size":            size,
                "prob_infeccion":  prob,
                "tiempo_muerte":   tdeath,
                "porc_zombies":    porc,
            }
        except (ValueError, AssertionError) as e:
            self.error_msg = f"⚠  {e}"
            return None

    # ----------------------------------------------------------

    def _draw(self):
        self.surface.fill(COLOR_BG)

        cx = self.WIDTH // 2

        # Franja superior decorativa
        pygame.draw.rect(self.surface, (25, 10, 10), (0, 0, self.WIDTH, 130))

        # Título
        title = self.font_title.render("☣  ZOMBIE SIMULATION", True, COLOR_ZOMBIE)
        self.surface.blit(title, title.get_rect(centerx=cx, y=30))

        sub = self.font_sub.render(
            "Sistema autónomo de propagación — Autómata Celular",
            True, COLOR_TEXT_DIM)
        self.surface.blit(sub, sub.get_rect(centerx=cx, y=75))

        # Íconos decorativos
        icons_font = pygame.font.SysFont("monospace", 22)
        for i, (icon, col) in enumerate([
            ("H", COLOR_HUMANO), ("→", COLOR_TEXT_DIM),
            ("Z", COLOR_ZOMBIE), ("→", COLOR_TEXT_DIM), ("†", (150,150,160))
        ]):
            s = icons_font.render(icon, True, col)
            self.surface.blit(s, s.get_rect(centerx=cx - 80 + i * 40, y=100))

        # Campos
        for field in self.fields:
            field.draw(self.surface)

        # Error
        if self.error_msg:
            err = self.font_sub.render(self.error_msg, True, COLOR_ZOMBIE)
            self.surface.blit(err, err.get_rect(centerx=cx, y=478))

        # Botón
        self.btn_start.draw(self.surface)
