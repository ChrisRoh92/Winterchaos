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
from .boxes_entity import TrashBin, Portal, Pfandautomat
from ..utils.sprite_utils import load_sprite, load_sprite_with_sprite_size
from ..utils.params import *
from ..utils.utils import interpolate

class INTERACTION_TYPES(enum.Enum):
    UNDEFINED = 0
    TRASH_BIN_INTERACTION = 1
    OTHER_PLAYER_INTERACTION = 2
    PORTAL_INTERACTION = 3
    PFAND_AUTOMAT_INTERACTION = 4


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
                content, msg = obj.interact()
                return {"type": INTERACTION_TYPES.TRASH_BIN_INTERACTION, "msg": msg, "content": content}
            elif isinstance(obj, Portal):
                content = {"destination": obj.destination}
                msg = None
                return {"type": INTERACTION_TYPES.PORTAL_INTERACTION, "msg": msg, "content": content}
            elif isinstance(obj, Pfandautomat):
                obj.interact()
                return {"type": INTERACTION_TYPES.PFAND_AUTOMAT_INTERACTION, "msg": None, "content": None}

        return {"type": INTERACTION_TYPES.UNDEFINED, "msg": None, "content": None}
        

class BierdurstmannInventory:
    def __init__(self):
        self.content = {
            'money' : 0.0,
            "beer" : 12,
            "bottle": 0,
            "can" : 0,
            "trash" : 0
        }


    def add_trash_bin_content(self, content:dict):
        self.content['money'] += content['money']
        self.content['bottle'] += content['bottle']
        self.content['can'] += content['can']
        self.content['trash'] += content['trash']

STATE_TIME = 10
class BierdurstmannState:
    def __init__(self):

        self.health = 100
        self.bierdurst = 0
        self.suff = 0

        self.time = 0

        self.sound_files = [
            "game/assets/sounds/durscht_bierdurscht.mp3",
            "game/assets/sounds/dann_sauf_i_mi_voll.mp3"
        ]

        self.index = 1
        self.sound = pygame.mixer.Sound(self.sound_files[self.index])

    def _play_beer_sound(self):
        self.index = random.randint(0, (len(self.sound_files) - 1))
        if pygame.mixer.get_busy():
            self.sound.stop()
            self.sound = pygame.mixer.Sound(self.sound_files[self.index])
            self.sound.play()
        else:
            self.sound = pygame.mixer.Sound(self.sound_files[self.index])
            self.sound.play()


    def drink_beer(self):
        self.suff += 1
        self.time = 0
        self._play_beer_sound()

    def update(self, dt):
        self.time += dt
        if self.time > STATE_TIME:
            self.time = 0
            self.suff -= 1
            self.suff = max(0, self.suff)

class EmoteBox(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill("white")
        self.rect = self.image.get_rect()
        self.rect.midbottom = (pos.x, pos.y + PLAYER_SIZE)

class Bierdurstmann(pygame.sprite.Sprite):
    def __init__(
            self, 
            pos: pygame.Vector2, 
            group: pygame.sprite.GroupSingle,
            show_message: callable):
        if group:
            super().__init__(group)
        else:
            super().__init__()


        # self.draw_group = draw_group
        
        self.pos = copy.deepcopy(pos)
        self.show_message = show_message
        self.interaction_box_group = pygame.sprite.GroupSingle()
        self.interaction_box = InteractionBox(self.pos, self.interaction_box_group)
        self.emote_box_group = pygame.sprite.GroupSingle()
        self.emote_box = EmoteBox(self.pos, self.emote_box_group)

        self.inventory = BierdurstmannInventory()
        self.state = BierdurstmannState()
        self.portal_destination = None
        
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.direction = pygame.Vector2()

        self.collision_box = pygame.rect.Rect(5, 5, PLAYER_SIZE - 20, PLAYER_SIZE - 20)
        self.collision_box.center = self.rect.center
        
        self.dir = "left"
        self.interact = False

        self.default_frame = 0
        self.current_frame = 0
        self.time = 0
        self.timstamp = 0
        self.speed_factor = 1.0
        self._load_sprite()
                                 
    def _load_sprite(self):
        filename = "player.png"
        total_path = os.path.join("game", "assets", "sprites", filename)
        sprite_w = 64
        sprite_h = 64
        self.sprites = {
            "up" :      load_sprite_with_sprite_size(total_path, 0, 8, 9, 1, sprite_w, sprite_h, (PLAYER_SIZE, PLAYER_SIZE)),
            "left" :      load_sprite_with_sprite_size(total_path, 0, 9, 9, 1, sprite_w, sprite_h, (PLAYER_SIZE, PLAYER_SIZE)),
            "down" :      load_sprite_with_sprite_size(total_path, 0, 10, 9, 1, sprite_w, sprite_h, (PLAYER_SIZE, PLAYER_SIZE)),
            "right" :      load_sprite_with_sprite_size(total_path, 0, 11, 9, 1, sprite_w, sprite_h, (PLAYER_SIZE, PLAYER_SIZE))
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
                    if self.inventory.content['beer'] > 0:
                        self.state.drink_beer()
                        self.inventory.content['beer'] -= 1
                        if random.randint(0, 1) == 0:
                            self.inventory.content['bottle'] += 1
                        else:
                            self.inventory.content['can'] += 1
                    else:
                        self.show_message("Du hast kein Bier mehr!")



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
        self.reduce_speed_factor = interpolate(self.state.suff, 0, 10, 1.0, 0.4)
        self.pos += self.direction * PLAYER_SPEED * dt * self.speed_factor * self.reduce_speed_factor
        ## Handle Suff Level
        if self.state.suff > 0:
            sin_value = math.sin(self.timstamp * 1.0 * self.state.suff) * 1 + math.cos(self.timstamp * 1.0/self.state.suff) * 0.2
            amplitude = interpolate(self.state.suff, 0, 10, 0, 2)
            if self.direction.magnitude() > 0:
                self.pos.y += sin_value * amplitude * self.reduce_speed_factor
                self.pos.x += sin_value * amplitude * self.reduce_speed_factor
            # if abs(self.direction.x) > 0:
            #     self.pos.y += sin_value * amplitude * self.reduce_speed_factor
            #     self.pos.x += sin_value * amplitude * self.reduce_speed_factor
            # elif abs(self.direction.y) > 0:
            #     self.pos.y += sin_value * amplitude * self.reduce_speed_factor
            #     self.pos.x += sin_value * amplitude * self.reduce_speed_factor

    def _animate(self, dt):
        self.time += dt * PLAYER_FRAME_FACTOR * self.speed_factor * self.reduce_speed_factor
        self.current_frame = math.floor(self.time)
        if self.current_frame > len(self.sprites[self.dir])-1:
            self.time = 0
            self.current_frame = 0

        self.image = self.sprites[self.dir][self.current_frame]  
        self.rect = self.image.get_rect()
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        self.collision_box.center = self.rect.center

    def _custom_collisioncheck(self, collision):

        if not self.collision_box.colliderect(collision):
            return None

        delta_links = self.collision_box.right - collision.rect.left
        delta_rechts = collision.rect.right - self.collision_box.left
        delta_oben = self.collision_box.bottom - collision.rect.top
        delta_unten = collision.rect.bottom - self.collision_box.top

        min_delta = min(delta_links, delta_rechts, delta_oben, delta_unten)

        if min_delta == delta_links:
            self.pos.x = collision.rect.left - (PLAYER_SIZE_H - 10)
            return "rechts von ego"
        elif min_delta == delta_rechts:
            self.pos.x = collision.rect.right + (PLAYER_SIZE_H - 10)
            return "links von ego"
        elif min_delta == delta_oben:
            self.pos.y = collision.rect.top - (PLAYER_SIZE_H - 10)
            return "unten von ego"
        else:
            self.pos.y = collision.rect.bottom + (PLAYER_SIZE_H - 10)
            return "oben von ego"


    def _check_collision(self, collisionbox_groups: List[pygame.sprite.Group]):
            for group in collisionbox_groups:
                collisions = pygame.sprite.spritecollide(self, group, False)
                for col in collisions:
                    if self._custom_collisioncheck(col):
                        self.rect.center = (int(self.pos.x), int(self.pos.y))
                        self.collision_box.center = self.rect.center
                        return





                

            
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

    def _check_interaction(self, collisionbox_groups: pygame.sprite.Group):
        data = self.interaction_box.check(collisionbox_groups)
        return data
    
    def _handle_post_interaction(self, interaction_data: dict, portal_data:dict):
        if interaction_data['type'] == INTERACTION_TYPES.TRASH_BIN_INTERACTION:
            self.inventory.add_trash_bin_content(interaction_data['content'])
            self.show_message(interaction_data['msg'])
        elif interaction_data['type'] == INTERACTION_TYPES.OTHER_PLAYER_INTERACTION:
            pass
        else:
            pass

        if portal_data['type'] == INTERACTION_TYPES.PORTAL_INTERACTION:
            self.portal_destination = portal_data['content']['destination']
        else:
            pass

    def update(self, dt, events: List[pygame.event.Event], collisionbox_groups: List[pygame.sprite.Group], interaction_group: pygame.sprite.Group, portal_group: pygame.sprite.Group):
        self.timstamp += dt
        self._handle_inputs(events)
        self._move(dt)
        self._animate(dt)
        self._check_collision(collisionbox_groups)
        self._move_interaction_box()
        self.state.update(dt)
        if self.interact:
            interaction_data = self._check_interaction(interaction_group)
            portal_data = self._check_interaction(portal_group)
            self._handle_post_interaction(interaction_data, portal_data)

    def get_portal_destination(self):
        destination = self.portal_destination
        self.portal_destination = None
        return destination

    def update_pos(self, pos: pygame.Vector2):
        self.pos = pos
        self.rect.center = self.pos

    def get_data(self):
        return self.inventory.content['money'],  self.state.bierdurst, self.state.suff