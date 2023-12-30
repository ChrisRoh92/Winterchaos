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
import pygame
from typing import List
from ..utils.params import *
from .base_level import BaseLevel
from ..entities.bierdurstmann_entity import Bierdurstmann


class GameLevel(BaseLevel):
    def __init__(self):
        self.player_group = pygame.sprite.GroupSingle()

        self._init()

    # ------------------------- #
    # 'Public Methods'          #
    # ------------------------- #

    def update(self, dt:float, events: List[pygame.event.Event]):
        self.player_group.update(dt, events)

    def render(self, screen: pygame.Surface):
        screen.fill('gray')
        self.player_group.draw(screen)

    def reset(self):
        pass

    def shutdown(self):
        pass

    # ------------------------- #
    # 'Private Methods'         #
    # ------------------------- #

    def _init(self):
        self.player = Bierdurstmann(pygame.Vector2(WIDTH_H, HEIGHT_H), self.player_group)