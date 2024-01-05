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

class PORTAL_DESTINATION(enum.Enum):
    TO_NORMAL_WORLD = 1
    TO_REWE_WOLRD = 2

def map_str_destination(destination: str)-> PORTAL_DESTINATION:
    if destination == "to_main_world":
        return PORTAL_DESTINATION.TO_NORMAL_WORLD
    elif destination == "to_rewe_world":
        return PORTAL_DESTINATION.TO_REWE_WOLRD

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
            "bottle" : 0,
            "can" : 0,
            "trash": 0,
            "money" : 0
        }

        self.time = 0
        self.renew_time = random.randint(TRASH_BIN_CONTENT_UPDATE_MIN, TRASH_BIN_CONTENT_UPDATE_MAX)
    
    def _reset(self):
        self.content = {
            "bottle" : 0,
            "can" : 0,
            "trash": 0,
            "money" : 0
        }

    def _generate_msg(self):
        if self.content['bottle'] == 0 and self.content['can'] == 0 and self.content['trash'] == 0 and self.content['money'] == 0:
            return "Der Mülleimer ist leer"
        else:
            bottle_msg = ""
            can_msg = ""
            trash_msg = ""
            money_msg = ""
            if self.content['bottle'] > 0:
                bottle_msg = f"{self.content['bottle']} Pfandflaschen"
            if self.content['can'] > 0:
                can_msg = f"{self.content['can']} Pfanddosen"
            if self.content['trash'] > 0:
                trash_msg = f"{self.content['trash']} Stücke Müll"
            if self.content['money'] > 0:
                money_msg = f"{self.content['money']:.2f} € an Geld"


            msg = f"Du hast folgende Gegenstände gefunden:        {bottle_msg} {can_msg} {trash_msg} {money_msg}"
            return msg

    def interact(self):
        msg = self._generate_msg()
        content = copy.deepcopy(self.content)
        self._reset()
        return content, msg

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
                    self.content["can"] += num_bottles_cans
                    self.content["can"] = min(self.content["can"], TRASH_BIN_MAX_CANS_BOTTLES)
                else:
                    self.content["bottle"] += num_bottles_cans
                    self.content["bottle"] = min(self.content["bottle"], TRASH_BIN_MAX_CANS_BOTTLES)
            else:
                num_trash = random.randint(0, 1)
                self.content["trash"] += num_trash
                self.content["trash"] = min(self.content["trash"], 2)

        else:
            money = random.uniform(0, TRASH_BIN_MAX_MONEY)
            self.content["money"] += money

    def update(self, dt):
        self.time += dt
        if self.time > self.renew_time:
            self.time = 0
            self.renew_time = random.randint(TRASH_BIN_CONTENT_UPDATE_MIN, TRASH_BIN_CONTENT_UPDATE_MAX)
            self._update_content()

class Portal(pygame.sprite.Sprite):
    def __init__(self, pos, size, group, destination: str):
        super().__init__(group)

        self.destination = map_str_destination(destination)

        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.image.fill('red')
        self.rect = self.image.get_rect()
        self.rect.topleft = pos