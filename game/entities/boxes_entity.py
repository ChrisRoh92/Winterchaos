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

import pygame, copy, math, os, enum, random
from typing import List
from ..utils.sprite_utils import load_sprite
from ..utils.params import *

class CollisionBox(pygame.sprite.Sprite):
    def __init__(self, pos, size, group):
        super().__init__(group)

        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.image.fill('red')
        self.rect = self.image.get_rect()
        self.rect.topleft = pos


class TrashBin(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        ## TODO(chrohne): Max size of trash bin, so the bierdurstmann should collect the trash
        ## and bring it to the recycling center, so there is more space for bottles/cans
        self.content = {
            "Flasche" : 0,
            "Dosen" : 0,
            "Müll": 0,
            "Geld" : 0
        }

        self.time = 0
        self.renew_time = random.randint(TRASH_BIN_CONTENT_UPDATE_MIN, TRASH_BIN_CONTENT_UPDATE_MAX)

    def show_content(self):
        print(f"content: {self.content}, time: {self.time}, renew_time: {self.renew_time}")

    def _update_content(self):
        value = random.uniform(0, 1)
        if value < 0.95:
            ## generate "Flaschen", "Dosen", Müll"
            if random.uniform(0, 1) > 0.6:
                ## generate Flaschen/Dosen
                num_bottles_cans = random.randint(0, TRASH_BIN_MAX_CANS_BOTTLES_RANDOM)
                foo = random.randint(0, 1)
                if foo == 0:
                    self.content["Dosen"] += num_bottles_cans
                    self.content["Dosen"] = min(self.content["Dosen"], TRASH_BIN_MAX_CANS_BOTTLES)
                else:
                    self.content["Flasche"] += num_bottles_cans
                    self.content["Flasche"] = min(self.content["Flasche"], TRASH_BIN_MAX_CANS_BOTTLES)
            else:
                num_trash = random.randint(0, 1)
                self.content["Müll"] += num_trash
                self.content["Müll"] = min(self.content["Müll"], 2)

        else:
            money = random.uniform(0, TRASH_BIN_MAX_MONEY)
            self.content["Geld"] += money

    def update(self, dt):
        self.time += dt
        if self.time > self.renew_time:
            self.time = 0
            self.renew_time = random.randint(TRASH_BIN_CONTENT_UPDATE_MIN, TRASH_BIN_CONTENT_UPDATE_MAX)
            self._update_content()

