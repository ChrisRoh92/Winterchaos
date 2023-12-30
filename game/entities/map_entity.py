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

import pygame, copy, math, os, enum
from typing import List
from ..utils.sprite_utils import load_sprite
from ..utils.params import *


class MapEntity(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        filename = "map.png"
        total_path = os.path.join("game", "assets", "sprites", filename)
        self.image = pygame.image.load(total_path)
        self.image = pygame.transform.scale_by(self.image, 0.5)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

    def update(self):
        pass