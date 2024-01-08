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
import pygame, copy, enum, random
from typing import List
from .game_scene_base import *
from ...entities.map_entity import MapEntity
from ...entities.boxes_entity import CollisionBox, TrashBin, Portal




class MainWorldScene(GameScene):
    def __init__(self, camera, bg_music_file: str, map_file: str):
        super().__init__(camera, bg_music_file, map_file)

        self.trash_bins_group = pygame.sprite.Group()

        self.create_world()


    def create_world(self):
        self.tmx_data = load_pygame(self.map_file)
        self.tmx_layers = self.tmx_data.layers
        self.tmx_objectgroups = self.tmx_data.objectgroups
        self.tmx_w = self.tmx_data.width
        self.tmx_h = self.tmx_data.height

        self.map = MapEntity(self.tmx_layers, self.tmx_w, self.tmx_h, self.map_group)

        for group in self.tmx_objectgroups:
            if group.name == "collision_boxes":
                for obj in group:
                    pos = (obj.x, obj.y)
                    size = (obj.width, obj.height)
                    CollisionBox(pos, size, self.collision_box_group)
            elif group.name == "trash_buckets":
                for obj in group:
                    pos = (obj.x, obj.y)
                    surf = obj.image
                    TrashBin(pos, surf, self.interaction_object_groups)
            elif group.name == "portals":
                    for obj in group:
                        pos = (obj.x, obj.y)
                        size = (obj.width, obj.height)
                        Portal(pos, size, self.portals_group, obj.name)
            elif group.name == "player":
                if self.last_player_pos == None:
                    obj = group[0]
                    pos = pygame.Vector2(obj.x, obj.y)
                    self.last_player_pos = pos

    def init_scene(self, player: Bierdurstmann):
        super().init_scene(player)

        if self.last_player_pos:
            self.player.update_pos(self.last_player_pos)

    def update(self, dt: float, events: List[pygame.event.Event]):
        self.map_group.update()
        self.interaction_object_groups.update(dt)
        self.player.update(dt, events, [self.collision_box_group, self.interaction_object_groups], self.interaction_object_groups, self.portals_group)
        destination = self.player.get_portal_destination()
        if destination:
            self.state = GAME_SCENE_STATE.TRANSITION_TO
            self.destination = destination

    def render(self, screen: pygame.Surface):
        self.camera.custom_drawing(self.player_group, screen, self.map_group, self.interaction_object_groups)

    def teardown(self):
        self.last_player_pos = self.player.pos
        super().teardown()
        self.destination = None
        self.state = GAME_SCENE_STATE.SHUTDOWN