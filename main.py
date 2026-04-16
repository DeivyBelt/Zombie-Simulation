# ============================================================
#  main.py — Loop principal y control de estados del programa
# ============================================================

import sys
import pygame

from config import CELL_SIZE, PANEL_WIDTH, FPS
from simulation import ZombieSimulation
from renderer import Renderer
from ui import MenuScreen

# ──────────────────────────────────────────────────────────────
#  Estados del programa
# ──────────────────────────────────────────────────────────────
MENU       = "menu"
SIMULACION = "simulacion"


def main():
    pygame.init()
    pygame.display.set_caption("Zombie Simulation")

    while True:  # Loop principal para volver al menú
        estado = MENU
        sim    = None
        rend   = None

        # ── Menú de configuración ──────────────────────────────────
        menu = MenuScreen()
        params = menu.run()

        if params is None:
            # El usuario cerró la ventana en el menú
            break

        estado = SIMULACION

        # ── Crear ventana de simulación ────────────────────────────
        grid_size = params["size"]
        grid_px   = grid_size * CELL_SIZE            # píxeles del grid
        win_w     = grid_px + PANEL_WIDTH
        win_h     = grid_px

        screen = pygame.display.set_mode((win_w, win_h))
        pygame.display.set_caption("Zombie Simulation ☣")

        sim  = ZombieSimulation(
            size           = params["size"],
            prob_infeccion = params["prob_infeccion"],
            tiempo_muerte  = params["tiempo_muerte"],
            porc_zombies   = params["porc_zombies"],
        )
        rend  = Renderer(screen, CELL_SIZE)
        clock = pygame.time.Clock()

        paused = False  # espacio para pausar

        # ── Loop de simulación ──────────────────────────────────────
        volver_menu = False
        while not volver_menu:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    volver_menu = True

                if event.type == pygame.KEYDOWN:
                    # ESPACIO → pausa/reanuda
                    if event.key == pygame.K_SPACE:
                        paused = not paused

                    # R → reiniciar con los mismos parámetros
                    if event.key == pygame.K_r:
                        sim = ZombieSimulation(
                            size           = params["size"],
                            prob_infeccion = params["prob_infeccion"],
                            tiempo_muerte  = params["tiempo_muerte"],
                            porc_zombies   = params["porc_zombies"],
                        )
                        paused = False

                    # ESCAPE → volver al menú
                    if event.key == pygame.K_ESCAPE:
                        volver_menu = True

            # ── Lógica ────────────────────────────────────────────
            if not paused and not sim.terminada:
                sim.step()

            # ── Renderizado ───────────────────────────────────────
            rend.draw_simulation(sim, grid_offset_x=0)

            # Indicador de pausa
            if paused:
                fnt = pygame.font.SysFont("monospace", 20, bold=True)
                txt = fnt.render("⏸  PAUSADO  [ESPACIO]", True, (255, 200, 0))
                screen.blit(txt, txt.get_rect(centerx=grid_px // 2, y=8))

            # Hint teclas (esquina inferior del grid)
            hint_fnt = pygame.font.SysFont("monospace", 10)
            hints = "[ESPACIO] pausa   [R] reiniciar   [ESC] menú"
            h_surf = hint_fnt.render(hints, True, (60, 65, 75))
            screen.blit(h_surf, (6, win_h - 14))

            pygame.display.flip()
            clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
