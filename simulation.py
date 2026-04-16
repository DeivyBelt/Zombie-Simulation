# ============================================================
#  simulation.py — Lógica central de la simulación
# ============================================================

import numpy as np
import random
from config import HUMANO, ZOMBIE, MUERTO


class ZombieSimulation:
    """
    Autómata celular que modela la propagación de zombies.

    Estados:
        HUMANO (0) — celda viva, puede infectarse
        ZOMBIE (1) — celda infectada, contagia vecinos
        MUERTO (2) — celda inerte (zombie que expiró)

    Reglas (vecindad Moore 3×3):
        - Un HUMANO con al menos un ZOMBIE adyacente se infecta
          con probabilidad `prob_infeccion`.
        - Un ZOMBIE incrementa su contador cada paso; cuando
          supera `tiempo_muerte` se convierte en MUERTO.
    """

    def __init__(self, size: int, prob_infeccion: float,
                 tiempo_muerte: int, porc_zombies: float):
        self.size            = size
        self.prob_infeccion  = prob_infeccion
        self.tiempo_muerte   = tiempo_muerte

        # Inicializar grid con distribución aleatoria
        p_zombie = porc_zombies / 100.0
        p_humano = 1.0 - p_zombie
        self.grid = np.random.choice(
            [HUMANO, ZOMBIE],
            size=(size, size),
            p=[p_humano, p_zombie]
        )

        # Temporizadores de vida para cada zombie
        self.timers = np.zeros((size, size), dtype=np.int32)

        # Historial para la gráfica de población
        self.hist_humanos = []
        self.hist_zombies = []
        self.hist_muertos = []

        self.step_count = 0
        self._record()

    # ----------------------------------------------------------
    # Paso de simulación
    # ----------------------------------------------------------

    def step(self):
        """Avanza un paso de tiempo en la simulación."""
        nuevo   = self.grid.copy()
        nuevo_t = self.timers.copy()
        size    = self.size

        for i in range(size):
            for j in range(size):
                estado = self.grid[i, j]

                if estado == HUMANO:
                    if self._hay_zombie_cerca(i, j):
                        if random.random() < self.prob_infeccion:
                            nuevo[i, j]   = ZOMBIE
                            nuevo_t[i, j] = 0

                elif estado == ZOMBIE:
                    nuevo_t[i, j] += 1
                    if nuevo_t[i, j] > self.tiempo_muerte:
                        nuevo[i, j] = MUERTO

        self.grid   = nuevo
        self.timers = nuevo_t
        self.step_count += 1
        self._record()

    # ----------------------------------------------------------
    # Vecindad Moore
    # ----------------------------------------------------------

    def _hay_zombie_cerca(self, i: int, j: int) -> bool:
        """Retorna True si existe al menos un ZOMBIE en la vecindad 3×3."""
        size = self.size
        for x in range(max(0, i - 1), min(size, i + 2)):
            for y in range(max(0, j - 1), min(size, j + 2)):
                if (x != i or y != j) and self.grid[x, y] == ZOMBIE:
                    return True
        return False

    # ----------------------------------------------------------
    # Conteos y estadísticas
    # ----------------------------------------------------------

    def contar_estados(self) -> tuple[int, int, int]:
        """Retorna (humanos, zombies, muertos) del frame actual."""
        h = int(np.sum(self.grid == HUMANO))
        z = int(np.sum(self.grid == ZOMBIE))
        m = int(np.sum(self.grid == MUERTO))
        return h, z, m

    def _record(self):
        h, z, m = self.contar_estados()
        self.hist_humanos.append(h)
        self.hist_zombies.append(z)
        self.hist_muertos.append(m)

    @property
    def terminada(self) -> bool:
        """True cuando no quedan zombies activos."""
        return int(np.sum(self.grid == ZOMBIE)) == 0
