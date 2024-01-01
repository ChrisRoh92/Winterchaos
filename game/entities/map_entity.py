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
from pytmx.util_pygame import load_pygame
from typing import List
from ..utils.sprite_utils import load_sprite
from ..utils.params import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

class MapEntity(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        filename = "map_tiled.tmx"
        total_path = os.path.join("game", "assets", "tiled_map", filename)
        # self.image = pygame.image.load(total_path)
        # self.image = pygame.transform.scale_by(self.image, 0.5)
        self.tiles = pygame.sprite.Group()
        self.tmx_data = load_pygame(total_path)
        self.width = self.tmx_data.width * 16
        self.height = self.tmx_data.height * 16
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                for x,y,surf in layer.tiles():
                    pos = (x * 16, y * 16)
                    Tile(pos, surf, self.tiles)
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.tiles.draw(self.image)

    def update(self):
        pass