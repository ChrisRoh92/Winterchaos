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
import pygame, copy, os
from pytmx.util_pygame import load_pygame
from typing import List
from ..utils.params import *
from .base_level import BaseLevel
from ..entities.bierdurstmann_entity import Bierdurstmann
from ..entities.boxes_entity import CollisionBox, TrashBin
from ..entities.map_entity import MapEntity


class CameraGroup:
    def __init__(self):
        self.offset = pygame.Vector2()

    def custom_drawing(self, player_group: pygame.sprite.GroupSingle, screen: pygame.Surface, *sprite_groups):
        self.offset.x = (player_group.sprite.rect.centerx) - WIDTH_H
        self.offset.y = (player_group.sprite.rect.centery) - HEIGHT_H
        
        for group in sprite_groups:
            for sprite in group:
                offset_rect = copy.deepcopy(sprite.rect)
                offset_rect.center -= self.offset
                screen.blit(sprite.image, offset_rect)

        offset_rect = copy.deepcopy(player_group.sprite.rect)
        offset_rect.center -= self.offset
        screen.blit(player_group.sprite.image, offset_rect)

class GameMenu(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.image = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

        self.background = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.background.fill("gray")
        self.background.set_alpha(150)
        self.background_rect = self.image.get_rect()
        self.background_rect.topleft = (0, 0)

        self.w = WIDTH * 0.5
        self.h = HEIGHT * 0.8
        self.menu_image = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        self.menu_image.fill('white')
        self.menu_rect = self.menu_image.get_rect(center = (WIDTH_H, HEIGHT_H))

        self.image.blit(self.background, self.background_rect)
        self.image.blit(self.menu_image, self.menu_rect)

class GameInfoPanel(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.image = pygame.Surface((WIDTH, 40), pygame.SRCALPHA)
        self.image.fill('white')
        self.image.set_alpha(255)
        self.rect = self.image.get_rect(topleft = (0, 0))

        self.money = 0
        self.suff_level = 0
        self.bierdurst = 0

        self.font = pygame.font.Font(None, 32)

        self._draw_content()

    def _draw_content(self):
        self.image.fill('white')

        money_text = self.font.render(f"Geld: {self.money}", True, (0, 0, 0))
        sufflevel_text = self.font.render(f"Suff: {self.suff_level}", True, (0, 0, 0))
        bierdurst_text = self.font.render(f"Bierdurst: {self.bierdurst}", True, (0, 0, 0))


        money_rect = money_text.get_rect()
        money_rect.midleft = (20, 20)
        sufflevel_rect = sufflevel_text.get_rect()
        sufflevel_rect.midright = (WIDTH - 20, 20)
        bierdurst_rect = bierdurst_text.get_rect()
        bierdurst_rect.center = (WIDTH_H, 20)

        self.image.blit(money_text, money_rect)
        self.image.blit(sufflevel_text, sufflevel_rect)
        self.image.blit(bierdurst_text, bierdurst_rect)


    def update(self, money, bierdurst, suff):
        self.money = money
        self.bierdurst = bierdurst
        self.suff_level = suff
        self._draw_content()


class GameLevel(BaseLevel):
    def __init__(self):
        self.player_group = pygame.sprite.GroupSingle()
        self.interaction_box_group = pygame.sprite.GroupSingle()
        self.menu_group = pygame.sprite.GroupSingle()
        self.info_panel_group = pygame.sprite.GroupSingle()
        self.map_group = pygame.sprite.GroupSingle()
        self.collisionbox_groups = pygame.sprite.Group()
        self.trash_bins_group = pygame.sprite.Group()

        self.camera = CameraGroup()
        self.show_menu = False
        self.menu = GameMenu(self.menu_group)
        self.info_panel = GameInfoPanel(self.info_panel_group)

        self._init()

    # ------------------------- #
    # 'Public Methods'          #
    # ------------------------- #
    def _update_panel(self):
        money, bierdurst, suff = self.player.get_data()
        self.info_panel_group.update(money, bierdurst, suff)

    def update(self, dt:float, events: List[pygame.event.Event]):
        self._handle_events(events)
        if not self.show_menu:
            self.map_group.update()
            self.trash_bins_group.update(dt)
            self.player_group.update(dt, events, [self.collisionbox_groups, self.trash_bins_group])
            self._update_panel()
        

    def render(self, screen: pygame.Surface):
        screen.fill('gray')
        self.camera.custom_drawing(self.player_group, screen, self.map_group, self.trash_bins_group, self.interaction_box_group)
        self.info_panel_group.draw(screen)
        if self.show_menu:
            self.menu_group.draw(screen)

        # self.collisionbox_groups.draw(screen)
        # self.map_group.draw(screen)
        # self.player_group.draw(screen)

    def reset(self):
        pass

    def shutdown(self):
        pass

    # ------------------------- #
    # 'Private Methods'         #
    # ------------------------- #

    def _handle_events(self, events: List[pygame.event.Event]):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    self.show_menu = True
                if e.key == pygame.K_ESCAPE:
                    if self.show_menu:
                        self.show_menu = False

    def _init(self):
        filename = "map_tiled.tmx"
        total_path = os.path.join("game", "assets", "tiled_map", filename)

        self.tmx_data = load_pygame(total_path)
        self.tmx_layers = self.tmx_data.layers
        self.tmx_objectgroups = self.tmx_data.objectgroups
        self.tmx_w = self.tmx_data.width
        self.tmx_h = self.tmx_data.height


        
        self.map = MapEntity(self.tmx_layers, self.tmx_w, self.tmx_h, self.map_group)

        self._load_and_init_objects()

    def _load_and_init_objects(self):
        for group in self.tmx_objectgroups:
            if group.name == "collision_boxes":
                for obj in group:
                    pos = (obj.x, obj.y)
                    size = (obj.width, obj.height)
                    CollisionBox(pos, size, self.collisionbox_groups)
            elif group.name == "trash_buckets":
                for obj in group:
                    pos = (obj.x, obj.y)
                    surf = obj.image
                    TrashBin(pos, surf, self.trash_bins_group)
            elif group.name == "player":
                obj = group[0]
                pos = pygame.Vector2(obj.x, obj.y)
                self.player = Bierdurstmann(pos, self.player_group, self.interaction_box_group)