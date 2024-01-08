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
import pygame, copy, os, enum
from abc import ABC, abstractclassmethod
from pytmx.util_pygame import load_pygame
from typing import List
from ...utils.params import *
from ...entities.bierdurstmann_entity import Bierdurstmann


class GAME_SCENE_STATE(enum.Enum):
    UNDEFINED = 0
    INIT = 1
    RUNNING = 2
    SHUTDOWN = 3
    TRANSITION_TO = 4


class GameScene(ABC):
    def __init__(self, camera, bg_music_file: str, map_file: str):

        self.camera = camera
        self.sound = None
        self.state = GAME_SCENE_STATE.UNDEFINED


        self.music_file = bg_music_file
        self.map_file = map_file

        ## sprite groups:
        self.groups = []
        self.last_player_pos = None ## should be pygame.Vector2

        self.collision_box_group = pygame.sprite.Group()
        self.portals_group = pygame.sprite.Group()
        self.npc_group = pygame.sprite.Group()
        self.interaction_object_groups = pygame.sprite.Group()

        self.map_group = pygame.sprite.GroupSingle()

    @abstractclassmethod
    def init_scene(self, player: Bierdurstmann):
        self.player = player
        self.player_group = pygame.sprite.GroupSingle()
        self.player_group.add(self.player)

    @abstractclassmethod 
    def update(self, dt: float, events: List[pygame.event.Event]):
        pass

    @abstractclassmethod 
    def render(self, screen: pygame.Surface):
        pass

    @abstractclassmethod 
    def teardown(self):
        self.player_group.remove(self.player)