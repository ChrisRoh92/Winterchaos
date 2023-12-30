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
import pygame, copy
from typing import List
from ..utils.params import *
from .base_level import BaseLevel
from ..entities.bierdurstmann_entity import Bierdurstmann
from ..entities.map_entity import MapEntity


class CameraGroup:
    def __init__(self):
        self.offset = pygame.Vector2()

    def custom_drawing(self, player_group: pygame.sprite.GroupSingle, screen: pygame.Surface, *sprite_groups):
        self.offset.x = (player_group.sprite.rect.centerx) - WIDTH_H
        self.offset.y = (player_group.sprite.rect.centery) - HEIGHT_H


        # player_group.sprite.rect = offset_rect
        # player_group.sprite.pos = offset_rect.center

        

        

        

        for group in sprite_groups:
            for sprite in group:
                offset_rect = copy.deepcopy(sprite.rect)
                offset_rect.center -= self.offset
                screen.blit(sprite.image, offset_rect)


        
        offset_rect = copy.deepcopy(player_group.sprite.rect)
        offset_rect.center -= self.offset
        screen.blit(player_group.sprite.image, offset_rect)
        # player_group.draw(screen)


class GameLevel(BaseLevel):
    def __init__(self):
        self.player_group = pygame.sprite.GroupSingle()
        self.map_group = pygame.sprite.GroupSingle()

        self.camera = CameraGroup()

        self._init()

    # ------------------------- #
    # 'Public Methods'          #
    # ------------------------- #

    def update(self, dt:float, events: List[pygame.event.Event]):
        self.map_group.update()
        self.player_group.update(dt, events)

    def render(self, screen: pygame.Surface):
        screen.fill('gray')
        self.camera.custom_drawing(self.player_group, screen, self.map_group)
        # self.map_group.draw(screen)
        # self.player_group.draw(screen)

    def reset(self):
        pass

    def shutdown(self):
        pass

    # ------------------------- #
    # 'Private Methods'         #
    # ------------------------- #

    def _init(self):
        self.player = Bierdurstmann(pygame.Vector2(WIDTH_H, HEIGHT_H), self.player_group)
        self.map = MapEntity(self.map_group)