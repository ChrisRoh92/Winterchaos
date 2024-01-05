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
from pytmx.util_pygame import load_pygame
from typing import List
from ..utils.params import *
from .base_level import BaseLevel
from ..entities.bierdurstmann_entity import Bierdurstmann
from ..entities.boxes_entity import CollisionBox, TrashBin
from ..entities.map_entity import MapEntity
from .game_level_stuff.info_boxes import GameMenu, GameInfoPanel, InteractionTextBox, InventoryMenu

class GAME_WORLDS(enum.Enum):
    UNDEFINED = 0
    NORMAL_WORLD = 1
    ROSSKNECHT_WORLD = 2
    REWE_WORLD = 3
    AUSNUECHTERUNGSZELLE_WORLD = 4
    HOME_BIERDURSTMANN_WORLD = 5
    WERSTOFFHOF_WORLD = 6

class CameraGroup:
    def __init__(self):
        self.offset = pygame.Vector2()

    def custom_drawing(self, player_group: pygame.sprite.GroupSingle, screen: pygame.Surface, *sprite_groups):
        self.offset.x = int(player_group.sprite.pos.x) - WIDTH_H
        self.offset.y = int(player_group.sprite.pos.y) - HEIGHT_H
        
        for group in sprite_groups:
            for sprite in group:
                offset_rect = copy.deepcopy(sprite.rect)
                offset_rect.center -= self.offset
                screen.blit(sprite.image, offset_rect)

        offset_rect = copy.deepcopy(player_group.sprite.rect)
        offset_rect.center -= self.offset
        screen.blit(player_group.sprite.image, offset_rect)


class GameLevel(BaseLevel):
    def __init__(self):
        self.player_group = pygame.sprite.GroupSingle()
        ## TODO: could the next GroupSingle live in Bierdurstmann class?
        self.interaction_box_group = pygame.sprite.GroupSingle()

        self.current_world = GAME_WORLDS.NORMAL_WORLD 
        self.sound = pygame.mixer.Sound("game/assets/sounds/background_music.wav")
        self.sound.set_volume(0.5)
        self.sound.play(-1)

        self.map_group = pygame.sprite.GroupSingle()
        self.collisionbox_groups = pygame.sprite.Group()
        self.trash_bins_group = pygame.sprite.Group()

        ## Text and Menus
        self.menu_group = pygame.sprite.GroupSingle()
        self.info_panel_group = pygame.sprite.GroupSingle()
        self.interaction_text_group = pygame.sprite.GroupSingle()
        self.inventory_menu_group = pygame.sprite.GroupSingle()
        ## Panel, Menu and TextBox states
        self.show_menu = False
        self.show_message = False
        self.show_inventory = False
        ## Init Panels and TextBoxes:
        self.menu = GameMenu(self.menu_group)
        self.info_panel = GameInfoPanel(self.info_panel_group)
        self.inventory = InventoryMenu(self.inventory_menu_group)
        self.interaction_textbox = InteractionTextBox(self.interaction_text_group)

        ## Transition:
        self.start_transition = False
        self.transition_timer = 0

        self.camera = CameraGroup()
        self._init()

    # ------------------------- #
    # 'Public Methods'          #
    # ------------------------- #

    def show_interaction_box(self, msg):
        self.show_message = True
        self.interaction_textbox.set_msg(msg)
        self.interaction_textbox._draw_message()

    def update(self, dt:float, events: List[pygame.event.Event]):
        self._handle_events(events)
        if self.show_message:
            pass
        elif self.show_menu:
            pass
        elif self.show_inventory:
            self.inventory_menu_group.update(self.player.inventory)
        # elif self.start_transition:
        #     self.transition_timer += 10
        #     if self.transition_timer > 255:
        #         pass
        #         # self.start_transition = False
        else:

            ## Depended on the current map, only the relevant sprites needs to be updated:
            if self.current_world == GAME_WORLDS.NORMAL_WORLD:
                self.map_group.update()
                self.trash_bins_group.update(dt)
                self.player_group.update(dt, events, [self.collisionbox_groups, self.trash_bins_group])
            
            
            self._update_panel()

    def _draw_transition(self, screen):

        # Farben definieren
        transparent = (0, 0, 0, 0)
        semi_transparent_black = (0, 0, 0, 240)

        # Rechteck erstellen, um den gesamten Bildschirm zu füllen
        rect = pygame.Rect(0, 0, WIDTH, HEIGHT)

        # Kreis erstellen (Position, Radius)
        
        circle_radius = 100
        circle_pos = (WIDTH_H -circle_radius, HEIGHT_H- circle_radius)


        background = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        background.fill(semi_transparent_black)

        circle_surface = pygame.Surface((circle_radius * 2, circle_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(circle_surface, 'white', (circle_radius, circle_radius), circle_radius)

        circle_mask = pygame.mask.from_surface(circle_surface)
        # for i in circle_mask:
        #     print(i)
        # print(circle_mask)
        # background.set_at()

        # Maske auf die Hintergrund-Surface anwenden, um den Kreis freizugeben
        background.blit(circle_surface, circle_pos)
        background.set_colorkey('white')

        screen.blit(background, (0, 0))


        # transition_image = pygame.Surface((WIDTH, HEIGHT))
        # transition_image.fill('black')
        # transition_image.set_alpha(self.transition_timer)
        # transition_image_rect = transition_image.get_rect(topleft = (0, 0))

        # circle_radius = 50
        # circle_surface = pygame.Surface((50 * 2, 50 * 2), pygame.SRCALPHA)
        # pygame.draw.circle(circle_surface, 'white', (WIDTH_H, HEIGHT_H), circle_radius)

        # circle_mask = pygame.mask.from_surface(circle_surface)


        # transition_image.blit(circle_surface, self.player.rect.center)

        
        # screen.blit(transition_image, transition_image_rect)
        

    def render(self, screen: pygame.Surface):
        ## Delete content
        screen.fill('black')
        

        self.camera.custom_drawing(self.player_group, screen, self.map_group, self.trash_bins_group, self.interaction_box_group)
        
        if self.start_transition:
            self._draw_transition(screen)
        
        ## Drawing Menus and Panels
        self.info_panel_group.draw(screen)
        if self.show_menu:
            self.menu_group.draw(screen)
        elif self.show_message:
            self.interaction_text_group.draw(screen)
        elif self.show_inventory:
            self.inventory_menu_group.draw(screen)


    def reset(self):
        pass

    def shutdown(self):
        pass

    # ------------------------- #
    # 'Private Methods'         #
    # ------------------------- #
    def _update_panel(self):
        money, bierdurst, suff = self.player.get_data()
        self.info_panel_group.update(money, bierdurst, suff)

    def _handle_events(self, events: List[pygame.event.Event]):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_t:
                    if not self.start_transition:
                        self.start_transition = True
                        self.transition_timer = 0
                    else:
                        self.start_transition = False
                        self.transition_timer = 0
                if e.key == pygame.K_q:
                    self.show_menu = True
                elif e.key == pygame.K_ESCAPE:
                    if self.show_menu:
                        self.show_menu = False
                    elif self.show_inventory:
                        self.show_inventory = False
                elif e.key == pygame.K_RETURN:
                    if self.show_message:
                        self.show_message = False
                elif e.key == pygame.K_i:
                    if not self.show_inventory:
                        self.show_inventory = True

    def _init(self):
        filename = "rewe_map.tmx"
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
                self.player = Bierdurstmann(pos, self.player_group, self.interaction_box_group, self.show_interaction_box)