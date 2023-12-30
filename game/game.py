# Copyright 2023-2024 Christoph Rohnert
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import pygame, sys, math, random, copy
from .utils.params import *
from .level.base_level import LEVELS
from .level.main_menu import MainMenuLevel
from .level.game_level import GameLevel

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Winterchaos")

        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(FPS) / 1000.0

        self.events = pygame.event.get()

        self.current_level = GameLevel()
        self.running = True

    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events = pygame.event.get()
            self._handle_events()
            self._update()
            self._render()

        self._shutdown()

    # ------------------------- #
    # 'Private Methods'         #
    # ------------------------- #
    def _handle_events(self):
        for e in self.events:
            if e.type == pygame.QUIT:
                self.running = False

    def _update(self):
        self.current_level.update(self.dt, self.events)

    def _render(self):
        self.current_level.render(self.screen)
        pygame.display.flip()

    def _shutdown(self):
        pygame.quit()
        sys.exit()