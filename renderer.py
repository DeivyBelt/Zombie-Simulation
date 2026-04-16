# ============================================================
#  renderer.py — Renderizado del grid y panel de estadísticas
# ============================================================

import pygame
from config import (
    HUMANO, ZOMBIE, MUERTO,
    CELL_SIZE, PANEL_WIDTH,
    COLOR_BG, COLOR_PANEL, COLOR_GRID_LINE,
    COLOR_HUMANO, COLOR_ZOMBIE, COLOR_MUERTO,
    COLOR_TEXT, COLOR_TEXT_DIM, COLOR_ACCENT,
    ASSET_HUMANO, ASSET_ZOMBIE, ASSET_MUERTO,
)


class Renderer:
    """
    Encargado de todo el renderizado visual del simulador.

    Carga los sprites UNA sola vez al construirse y los
    escala al tamaño de celda definido en config.py.
    """

    def __init__(self, screen: pygame.Surface, cell_size: int = CELL_SIZE):
        self.screen    = screen
        self.cell_size = cell_size
        self.font_big  = pygame.font.SysFont("monospace", 18, bold=True)
        self.font_med  = pygame.font.SysFont("monospace", 14)
        self.font_sm   = pygame.font.SysFont("monospace", 11)

        # --- Cargar y escalar sprites una sola vez ---
        cs = cell_size
        try:
            self.sprites = {
                HUMANO: pygame.transform.scale(
                    pygame.image.load(ASSET_HUMANO).convert_alpha(), (cs, cs)),
                ZOMBIE: pygame.transform.scale(
                    pygame.image.load(ASSET_ZOMBIE).convert_alpha(), (cs, cs)),
                MUERTO: pygame.transform.scale(
                    pygame.image.load(ASSET_MUERTO).convert_alpha(), (cs, cs)),
            }
        except Exception as e:
            print(f"Error cargando sprites: {e}")
            # Fallback a colores sólidos
            self.sprites = {
                HUMANO: pygame.Surface((cs, cs)),
                ZOMBIE: pygame.Surface((cs, cs)),
                MUERTO: pygame.Surface((cs, cs)),
            }
            self.sprites[HUMANO].fill(COLOR_HUMANO)
            self.sprites[ZOMBIE].fill(COLOR_ZOMBIE)
            self.sprites[MUERTO].fill(COLOR_MUERTO)

        # Colores para la mini-gráfica
        self.plot_colors = {
            "humanos": COLOR_HUMANO,
            "zombies": COLOR_ZOMBIE,
            "muertos": COLOR_MUERTO,
        }

    # ----------------------------------------------------------
    # Renderizado principal
    # ----------------------------------------------------------

    def draw_simulation(self, sim, grid_offset_x: int = 0):
        """Dibuja grid + panel lateral completo."""
        self.screen.fill(COLOR_BG)
        self._draw_grid(sim, grid_offset_x)
        self._draw_panel(sim, grid_offset_x)

    # ----------------------------------------------------------
    # Grid
    # ----------------------------------------------------------

    def _draw_grid(self, sim, offset_x: int):
        cs   = self.cell_size
        size = sim.size

        for i in range(size):
            for j in range(size):
                estado = sim.grid[i, j]
                x = offset_x + j * cs
                y = i * cs
                
                # Dibujar fondo de celda con color sólido
                color_fondo = {
                    HUMANO: COLOR_HUMANO,
                    ZOMBIE: COLOR_ZOMBIE,
                    MUERTO: COLOR_MUERTO,
                }.get(estado, COLOR_BG)
                pygame.draw.rect(self.screen, color_fondo, (x, y, cs, cs))
                
                # Blitear sprite encima
                sprite = self.sprites[estado]
                self.screen.blit(sprite, (x, y))

        # Líneas del grid (sutiles)
        grid_w = size * cs
        grid_h = size * cs
        for col in range(size + 1):
            x = offset_x + col * cs
            pygame.draw.line(self.screen, COLOR_GRID_LINE, (x, 0), (x, grid_h))
        for row in range(size + 1):
            y = row * cs
            pygame.draw.line(self.screen, COLOR_GRID_LINE, (offset_x, y), (offset_x + grid_w, y))

    # ----------------------------------------------------------
    # Panel lateral
    # ----------------------------------------------------------

    def _draw_panel(self, sim, grid_offset_x: int):
        screen_w = self.screen.get_width()
        panel_x  = screen_w - PANEL_WIDTH
        panel_h  = self.screen.get_height()

        # Fondo del panel
        pygame.draw.rect(self.screen, COLOR_PANEL,
                         (panel_x, 0, PANEL_WIDTH, panel_h))
        pygame.draw.line(self.screen, (40, 45, 55),
                         (panel_x, 0), (panel_x, panel_h))

        h, z, m = sim.contar_estados()
        total    = max(h + z + m, 1)
        paso     = sim.step_count

        y = 18
        # Título panel
        self._text("☣  ZOMBIE SIM", panel_x + 14, y,
                   self.font_big, COLOR_ZOMBIE)
        y += 32

        # Paso actual
        self._text(f"Paso: {paso}", panel_x + 14, y,
                   self.font_med, COLOR_TEXT_DIM)
        y += 28

        # Separador
        pygame.draw.line(self.screen, (40, 45, 55),
                         (panel_x + 10, y), (panel_x + PANEL_WIDTH - 10, y))
        y += 12

        # Contadores con barra de progreso
        entries = [
            ("Humanos", h, total, COLOR_HUMANO),
            ("Zombies", z, total, COLOR_ZOMBIE),
            ("Muertos", m, total, COLOR_MUERTO),
        ]
        for label, count, tot, color in entries:
            self._text(label, panel_x + 14, y, self.font_med, color)
            self._text(str(count), panel_x + PANEL_WIDTH - 60, y,
                       self.font_med, COLOR_TEXT)
            y += 18
            # Barra
            bar_w  = PANEL_WIDTH - 28
            filled = int(bar_w * count / tot)
            pygame.draw.rect(self.screen, (40, 45, 55),
                             (panel_x + 14, y, bar_w, 7), border_radius=3)
            if filled > 0:
                pygame.draw.rect(self.screen, color,
                                 (panel_x + 14, y, filled, 7), border_radius=3)
            y += 18

        y += 8
        pygame.draw.line(self.screen, (40, 45, 55),
                         (panel_x + 10, y), (panel_x + PANEL_WIDTH - 10, y))
        y += 12

        # Mini-gráfica de historia
        self._text("Evolución", panel_x + 14, y, self.font_med, COLOR_TEXT_DIM)
        y += 20
        plot_h = 100
        plot_w = PANEL_WIDTH - 28
        self._draw_plot(sim, panel_x + 14, y, plot_w, plot_h)
        y += plot_h + 16

        pygame.draw.line(self.screen, (40, 45, 55),
                         (panel_x + 10, y), (panel_x + PANEL_WIDTH - 10, y))
        y += 12

        # Parámetros activos
        self._text("Parámetros", panel_x + 14, y, self.font_med, COLOR_TEXT_DIM)
        y += 20
        params = [
            ("Infección",   f"{sim.prob_infeccion:.0%}"),
            ("T. muerte",   str(sim.tiempo_muerte)),
            ("Grid",        f"{sim.size}×{sim.size}"),
        ]
        for k, v in params:
            self._text(f"{k}:", panel_x + 16, y, self.font_sm, COLOR_TEXT_DIM)
            self._text(v, panel_x + 130, y, self.font_sm, COLOR_ACCENT)
            y += 18

        # Indicador de fin
        if sim.terminada:
            y += 10
            self._text("■ Sin zombies activos", panel_x + 14, y,
                       self.font_sm, COLOR_HUMANO)

    # ----------------------------------------------------------
    # Mini-gráfica de evolución
    # ----------------------------------------------------------

    def _draw_plot(self, sim, x: int, y: int, w: int, h: int):
        """Dibuja líneas de historia de población dentro de un rectángulo."""
        pygame.draw.rect(self.screen, (25, 28, 36), (x, y, w, h), border_radius=4)
        pygame.draw.rect(self.screen, (40, 45, 55), (x, y, w, h), 1, border_radius=4)

        series = [
            (sim.hist_humanos, COLOR_HUMANO),
            (sim.hist_zombies, COLOR_ZOMBIE),
            (sim.hist_muertos, COLOR_MUERTO),
        ]
        total_cells = sim.size * sim.size

        for data, color in series:
            n = len(data)
            if n < 2:
                continue
            points = []
            for idx, val in enumerate(data):
                px = x + int(idx / max(n - 1, 1) * (w - 4)) + 2
                py = y + h - 4 - int(val / total_cells * (h - 8))
                points.append((px, py))
            pygame.draw.lines(self.screen, color, False, points, 2)

    # ----------------------------------------------------------
    # Utilidad texto
    # ----------------------------------------------------------

    def _text(self, msg: str, x: int, y: int,
              font: pygame.font.Font, color):
        surf = font.render(msg, True, color)
        self.screen.blit(surf, (x, y))
