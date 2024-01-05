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
import pygame, copy, os, enum, time
from pytmx.util_pygame import load_pygame
from typing import List
from ..utils.params import *
from .base_level import BaseLevel
from ..entities.bierdurstmann_entity import Bierdurstmann
from ..entities.boxes_entity import CollisionBox, TrashBin, PORTAL_DESTINATION
from ..entities.map_entity import MapEntity
from .game_level_stuff.info_boxes import GameMenu, GameInfoPanel, InteractionTextBox, InventoryMenu
from .game_level_stuff.main_world_scene import GAME_SCENE_STATE
from .game_level_stuff.main_world_scene import MainWorldScene
from .game_level_stuff.grocery_world_scene import GroceryWorldScene


class GAME_WORLDS(enum.Enum):
    UNDEFINED = 0
    NORMAL_WORLD = 1
    ROSSKNECHT_WORLD = 2
    REWE_WORLD = 3
    AUSNUECHTERUNGSZELLE_WORLD = 4
    HOME_BIERDURSTMANN_WORLD = 5
    WERSTOFFHOF_WORLD = 6

class LEVEL_STATE(enum.Enum):
    RUNNING = 1
    TRANSITION = 2

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

        # start_time = time.time_ns()

        self.camera = CameraGroup()
        self.current_world = GAME_WORLDS.NORMAL_WORLD
        self.level_state = LEVEL_STATE.RUNNING
        self.scenes = {
            GAME_WORLDS.NORMAL_WORLD : None,
            GAME_WORLDS.REWE_WORLD : None
        }

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

        
        self.transition_alpha = 0
        
        self._init()

        # end_time = time.time_ns()
        # duration = (end_time - start_time) / (1000**2)
        # print(f"duration loading: {duration}")

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
        else:
            if self.level_state == LEVEL_STATE.RUNNING:
                self.scenes[self.current_world].update(dt, events)           
                self._update_panel()
            elif self.level_state == LEVEL_STATE.TRANSITION:
                self.transition_alpha += 10

            self._run_state_machine()

    def _draw_transition(self, screen):
        color = (0, 0, 0, self.transition_alpha)
        background = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        background.fill(color)


        screen.blit(background, (0, 0))

    def _foo_testing(self, screen):

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


        self.scenes[self.current_world].render(screen)
        if self.level_state == LEVEL_STATE.TRANSITION:
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

        self.player = Bierdurstmann(pygame.Vector2(), None, self.show_interaction_box)

        self.scenes[GAME_WORLDS.NORMAL_WORLD] = MainWorldScene(self.camera, None, MAIN_WORLD_MAP_FILE)
        self.scenes[GAME_WORLDS.REWE_WORLD] = GroceryWorldScene(self.camera, None, GROCERY_MAP_FILE)

        self._init_state_machine()


    # ------------------------- #
    # 'State Machine'           #
    # ------------------------- #
    def _init_state_machine(self):
        self.scenes[self.current_world].init_scene(self.player)

    def _transition_to_new_state(self, new_state: GAME_WORLDS):
        self.scenes[self.current_world].teardown()
        self.current_world = new_state
        self.scenes[self.current_world].init_scene(self.player)

    def _run_state_machine(self):
        # print(f"self.level_state: {self.level_state}")
        if self.level_state == LEVEL_STATE.RUNNING:
            if self.scenes[self.current_world].state == GAME_SCENE_STATE.TRANSITION_TO:
                self.level_state = LEVEL_STATE.TRANSITION
        elif self.level_state == LEVEL_STATE.TRANSITION:
            if self.transition_alpha > 255:
                self.level_state = LEVEL_STATE.RUNNING
                self.transition_alpha = 0
                destination = self.scenes[self.current_world].destination
                print(destination)
                if destination == PORTAL_DESTINATION.TO_NORMAL_WORLD:
                    self._transition_to_new_state(GAME_WORLDS.NORMAL_WORLD)
                elif destination == PORTAL_DESTINATION.TO_REWE_WOLRD:
                    self._transition_to_new_state(GAME_WORLDS.REWE_WORLD)
                

