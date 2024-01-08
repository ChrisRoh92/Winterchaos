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
import pygame, random
from typing import List
from .base_level import BaseLevel
from ..utils.params import *

BUBBLE_MAX_RADIUS, BUBBLE_MIN_RADIUS = 10, 5
BASE_BUBBLE_SPEED = 1000
MAX_BUBBLES = 100
BEER_YELLOW = (252, 173, 3)

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
        



class MainMenuLevel(BaseLevel):
    def __init__(self, start_game: callable):
        self.background = MainMenuBackground()
        self.start_game = start_game

        self.font = pygame.font.Font(FONT_PATH, 24)

    # ------------------------- #
    # 'Public Methods'          #
    # ------------------------- #

    def _handle_events(self, events: List[pygame.event.Event]):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    self.start_game()


    def update(self, dt:float, events: List[pygame.event.Event]):
        self.background.update(dt)
        self._handle_events(events)

        

    def render(self, screen: pygame.Surface):
        screen.fill("black")

        self.background.render(screen)

        ## Move out to new class, just here for testing
        menu_rect = pygame.rect.Rect(0, 0, 500, 200)
        menu_rect.center = (WIDTH_H, HEIGHT_H + HEIGHT_H//2)
        pygame.draw.rect(screen, 'white', menu_rect,0, 10)

        text = "Press Enter to Start"
        text_image = self.font.render(text, True, 'black')
        text_image_rect = text_image.get_rect(center = menu_rect.center)

        screen.blit(text_image, text_image_rect)



    def reset(self):
        pass

    def shutdown(self):
        pass

    # ------------------------- #
    # 'Private Methods'         #
    # ------------------------- #