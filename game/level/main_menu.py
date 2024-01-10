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
import pygame, random, enum
from typing import List
from .base_level import BaseLevel
from ..utils.params import *

class BackgroundBubbles(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, pos: pygame.Vector2 = None):
        super().__init__(group)

        self.radius = random.randint(BUBBLE_MIN_RADIUS, BUBBLE_MAX_RADIUS)
        self.diameter = self.radius * 2
        if pos:
            self.pos = pos
        else:
         self.pos = pygame.Vector2(random.randint(0, WIDTH), HEIGHT + 10)
        self.image = pygame.Surface((self.diameter, self.diameter), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center = self.pos)
        alpha_value = min(255, 255 * (1 - (self.radius/BUBBLE_MAX_RADIUS)) + 100)
        white = (255, 255, 255, alpha_value)

        pygame.draw.circle(self.image, white, (self.radius, self.radius), self.radius)

    def update(self, dt):
        self.pos.y -= BASE_BUBBLE_SPEED * (1.0/self.radius) * dt
        if self.pos.y < -self.radius:
            self.kill()

        self.rect.center = self.pos
        
class MainMenuBackground:
    def __init__(self):

        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image.fill(BEER_YELLOW)
        self.rect = self.image.get_rect(topleft = (0, 0))

        self.bubbles = pygame.sprite.Group()

        margin = 20
        for _ in range(MAX_BUBBLES):
            pos = pygame.Vector2(random.randint(20, WIDTH-margin), random.randint(margin, HEIGHT - margin))
            BackgroundBubbles(self.bubbles, pos)
    def update(self, dt):
        self.bubbles.update(dt)
        
        if len(self.bubbles) < MAX_BUBBLES:
            BackgroundBubbles(self.bubbles)


    def render(self, screen: pygame.Surface):
        self.image.fill(BEER_YELLOW)
        self.bubbles.draw(self.image)
        screen.blit(self.image, self.rect)
        
class MAIN_MENU_BUTTON(enum.Enum):
    START_GAME = 0
    LOAD_GAME = 1
    SETTINGS = 2
    HELP = 3
    QUIT = 4
    NONE = 5



class MainMenuButton():
    def __init__(self, pos: pygame.Vector2, text:str, font: pygame.font.Font):

        self.font = font
        self.text = text
        self.selected = False
        self.image = pygame.Surface((MENU_BTN_WIDTH, MENU_BTN_HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center = pos)


    def draw(self, surface: pygame.Surface):

        self.image.fill(pygame.SRCALPHA)
        pygame.draw.rect(self.image, BTN_BACKGROUND_COLOR[self.selected], pygame.rect.Rect(0, 0, MENU_BTN_WIDTH, MENU_BTN_HEIGHT), 0, 20)
        self.text_surf = self.font.render(self.text, True, BTN_TEXT_COLOR[self.selected])
        self.text_rect = self.text_surf.get_rect(center = (MENU_BTN_WIDTH_H, MENU_BTN_HEIGHT_H))
        self.image.blit(self.text_surf, self.text_rect)
        surface.blit(self.image, self.rect)

    def update(self, selected: bool):
        self.selected = selected

class MainMenu:
    def __init__(self, callback: callable):
        
        self.callback = callback
        self.selected_btn = MAIN_MENU_BUTTON.NONE

        self.image = pygame.Surface((MENU_WIDTH, MENU_HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH_H, HEIGHT_H)

        self.font = pygame.font.Font(FONT_PATH, 30)
        self.selected_btn = MAIN_MENU_BUTTON.START_GAME.value
        self.buttons = []

        current_y = MENU_MARGIN + MENU_BTN_HEIGHT_H
        btn_offset = BTN_MARGIN + MENU_BTN_HEIGHT
        self.buttons.append(MainMenuButton(pygame.Vector2(MENU_WIDTH_H, current_y), "Spiel Starten", self.font))
        current_y += btn_offset
        self.buttons.append(MainMenuButton(pygame.Vector2(MENU_WIDTH_H, current_y), "Spiel Laden", self.font))
        current_y += btn_offset
        self.buttons.append(MainMenuButton(pygame.Vector2(MENU_WIDTH_H, current_y), "Einstellungen", self.font))
        current_y += btn_offset
        self.buttons.append(MainMenuButton(pygame.Vector2(MENU_WIDTH_H, current_y), "Hilfe", self.font))
        current_y += btn_offset
        self.buttons.append(MainMenuButton(pygame.Vector2(MENU_WIDTH_H, current_y), "Spiel Beenden", self.font))


        

    def update(self, dt: float, events: List[pygame.event.Event]):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    self.selected_btn = max(self.selected_btn - 1, MAIN_MENU_BUTTON.START_GAME.value)
                elif e.key == pygame.K_DOWN:
                    self.selected_btn = min(self.selected_btn + 1, MAIN_MENU_BUTTON.QUIT.value)
                elif e.key == pygame.K_RETURN:
                    if self.selected_btn in range(MAIN_MENU_BUTTON.START_GAME.value, MAIN_MENU_BUTTON.QUIT.value + 1):
                        self.callback(self.selected_btn)

        for index, btn in enumerate(self.buttons):
            btn.update(index == self.selected_btn)

    
    def draw(self, screen):
        self.image.lock

        menu_rect = pygame.rect.Rect(0, 0, MENU_WIDTH, MENU_HEIGHT)
        pygame.draw.rect(self.image, 'white', menu_rect,0, 10)

        for btn in self.buttons:
            btn.draw(self.image)

        screen.blit(self.image, self.rect)
            
class InterruptTextBox:
    def __init__(self):
        self.image = pygame.Surface((500, 100), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center = (WIDTH_H, HEIGHT_H))

        self.text = ""
        self.font = pygame.font.Font(FONT_PATH, 20)

    def update_text(self, new_text: str):
        self.text = new_text

    def render(self, screen):
        self.image.fill('white')

        text = self.font.render(self.text, True, 'black')
        text_rect = text.get_rect(center = (250, 50))

        self.image.blit(text, text_rect)
        screen.blit(self.image, self.rect)


class MainMenuLevel(BaseLevel):
    def __init__(self, start_game: callable, stop_game: callable):
        self.background = MainMenuBackground()
        self.start_game = start_game
        self.stop_game = stop_game

        self.font = pygame.font.Font(FONT_PATH, 24)
        self.menu = MainMenu(self.menu_callback)
        self.interrupt_box = InterruptTextBox()
        self.interrupt = False

    # ------------------------- #
    # 'Public Methods'          #
    # ------------------------- #

    def menu_callback(self, clicked_btn: MAIN_MENU_BUTTON):
        if clicked_btn == MAIN_MENU_BUTTON.START_GAME.value:
            self.start_game()
        elif clicked_btn == MAIN_MENU_BUTTON.QUIT.value:
            self.stop_game()
        else:
            self.interrupt_box.update_text("Not Implemented Yet")
            self.interrupt = True


    def _handle_events(self, events: List[pygame.event.Event]):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    if self.interrupt:
                        self.interrupt = False


    def update(self, dt:float, events: List[pygame.event.Event]):
        self._handle_events(events)
        self.background.update(dt)
        if self.interrupt:
            pass
        else:
            self.menu.update(dt, events)

        
            


    def render(self, screen: pygame.Surface):
        self.background.render(screen)
        self.menu.draw(screen)
        if self.interrupt:
            self.interrupt_box.render(screen)



    def reset(self):
        pass

    def shutdown(self):
        pass

    # ------------------------- #
    # 'Private Methods'         #
    # ------------------------- #