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
from .boxes_entity import TrashBin
from ..utils.sprite_utils import load_sprite
from ..utils.params import *


class InteractionBox(pygame.sprite.Sprite):
    def __init__(self, pos, group: pygame.sprite.GroupSingle):
        super().__init__(group)

        self.pos = copy.deepcopy(pos)
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def check(self, group: pygame.sprite.Group):
        collisions = pygame.sprite.spritecollide(self, group, False)
        if len(collisions) > 0:
            obj = collisions[0]
            if isinstance(obj, TrashBin):
                obj.show_content()

class BierdurstmannInventory:
    def __init__(self):
        self.content = {
            'money' : 15,
            "bier" : 10
        }

STATE_TIME = 10
class BierdurstmannState:
    def __init__(self):

        self.health = 100
        self.bierdurst = 0
        self.suff = 0

        self.time = 0

    def drink_beer(self):
        self.suff += 1
        self.time = 0

    def update(self, dt):
        self.time += dt
        if self.time > STATE_TIME:
            self.time = 0
            self.suff -= 1
            self.suff = max(0, self.suff)

class Bierdurstmann(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2, group: pygame.sprite.GroupSingle, interaction_box_group: pygame.sprite.GroupSingle):
        super().__init__(group)

        self.pos = copy.deepcopy(pos)
        self.interaction_box = InteractionBox(self.pos, interaction_box_group)

        self.inventory = BierdurstmannInventory()
        self.state = BierdurstmannState()
        
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.direction = pygame.Vector2()
        
        self.dir = "left"
        self.interact = False

        self.default_frame = 0
        self.current_frame = 0
        self.time = 0
        self.speed_factor = 1.0
        self._load_sprite()
                                 
    def _load_sprite(self):
        filename = "bierdurstmann.png"
        total_path = os.path.join("game", "assets", "sprites", filename)
        self.sprites = {
            "up" :      load_sprite(total_path, 0, 0, 4, 1, 4, 4, (PLAYER_SIZE, PLAYER_SIZE)),
            "down" :    load_sprite(total_path, 0, 1, 4, 1, 4, 4, (PLAYER_SIZE, PLAYER_SIZE)),
            "left" :    load_sprite(total_path, 0, 2, 4, 1, 4, 4, (PLAYER_SIZE, PLAYER_SIZE)),
            "right" :   load_sprite(total_path, 0, 3, 4, 1, 4, 4, (PLAYER_SIZE, PLAYER_SIZE)),
        }           

        self.image = self.sprites[self.dir][self.default_frame]  
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def _handle_inputs(self, events: List[pygame.event.Event]):
        self.interact = False
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    self.interact = True
                if e.key == pygame.K_b:
                    if self.inventory.content['bier'] > 0:
                        self.state.drink_beer()
                        self.inventory.content['bier'] -= 1



        keys = pygame.key.get_pressed()
        self.direction = pygame.Vector2()
        if keys[pygame.K_LSHIFT]:
            self.speed_factor = 2.0
        else:
            self.speed_factor = 1.0
        if keys[pygame.K_w]:
            if self.dir != 'up':
                self.time = 0
            self.dir = 'up'
            self.direction.y = -1
        elif keys[pygame.K_s]:
            if self.dir != 'down':
                self.time = 0
            self.dir = 'down'
            self.direction.y = 1
        elif keys[pygame.K_a]:
            if self.dir != 'left':
                self.time = 0
            self.dir = 'left'
            self.direction.x = -1
        elif keys[pygame.K_d]:
            if self.dir != 'right':
                self.time = 0
            self.dir = 'right'
            self.direction.x = 1
        else:
            self.time = 0
            
    def _move(self, dt):
        self.pos += self.direction * PLAYER_SPEED * dt * self.speed_factor

    def _animate(self, dt):
        self.time += dt * PLAYER_FRAME_FACTOR
        self.current_frame = math.floor(self.time)
        if self.current_frame > len(self.sprites[self.dir])-1:
            self.time = 0
            self.current_frame = 0

        self.image = self.sprites[self.dir][self.current_frame]  
        self.rect = self.image.get_rect()
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def _check_collision(self, collisionbox_groups: List[pygame.sprite.Group]):
        for group in collisionbox_groups:
            collisions = pygame.sprite.spritecollide(self, group, False)
            if len(collisions) > 0:
                ## Always only use the first detected collision for now!
                
                collision = collisions[0]
                if self.direction.x > 0:
                    self.pos.x = collision.rect.left - PLAYER_SIZE_H
                elif self.direction.x < 0:
                    self.pos.x = collision.rect.right + PLAYER_SIZE_H
                elif self.direction.y > 0:
                    self.pos.y = collision.rect.top - PLAYER_SIZE_H
                elif self.direction.y < 0:
                    self.pos.y = collision.rect.bottom + PLAYER_SIZE_H

                self.rect.center = (int(self.pos.x), int(self.pos.y))
                break
    
    def _move_interaction_box(self):
        new_rect = copy.deepcopy(self.interaction_box.rect)
        if self.direction.x > 0:
            new_rect.bottomleft = self.rect.bottomright
        elif self.direction.x < 0:
            new_rect.bottomright = self.rect.bottomleft
        elif self.direction.y > 0:
            new_rect.topleft = self.rect.bottomleft
        elif self.direction.y < 0:
            new_rect.bottomleft = self.rect.topleft
        self.interaction_box.rect = new_rect

    def _check_interaction(self, collisionbox_groups: List[pygame.sprite.Group]):
        self.interaction_box.check(collisionbox_groups[1])

    def update(self, dt, events: List[pygame.event.Event], collisionbox_groups: List[pygame.sprite.Group]):
        self._handle_inputs(events)
        self._move(dt)
        self._animate(dt)
        self._check_collision(collisionbox_groups)
        self._move_interaction_box()
        self.state.update(dt)
        if self.interact:
            self._check_interaction(collisionbox_groups)


    def get_data(self):
        return self.inventory.content['money'],  self.state.bierdurst, self.state.suff