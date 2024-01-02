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
import pygame, copy, os
from ...utils.params import *
from ...utils.utils import drawText
from ..base_level import BaseLevel
from ...entities.bierdurstmann_entity import Bierdurstmann, BierdurstmannInventory
from ...entities.boxes_entity import CollisionBox, TrashBin
from ...entities.map_entity import MapEntity

class GameMenu(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.image = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

        self.background = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.background.fill("gray")
        self.background.set_alpha(150)
        self.background_rect = self.image.get_rect()
        self.background_rect.topleft = (0, 0)

        self.w = WIDTH * 0.5
        self.h = HEIGHT * 0.8
        self.menu_image = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        self.menu_image.fill('white')
        self.menu_rect = self.menu_image.get_rect(center = (WIDTH_H, HEIGHT_H))

        self.image.blit(self.background, self.background_rect)
        self.image.blit(self.menu_image, self.menu_rect)

class GameInfoPanel(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

        self.image = pygame.Surface((WIDTH, 40), pygame.SRCALPHA)
        self.image.fill('white')
        self.image.set_alpha(255)
        self.rect = self.image.get_rect(topleft = (0, 0))

        self.money = 0
        self.suff_level = 0
        self.bierdurst = 0

        self.font = pygame.font.Font(None, 32)

        self._draw_content()

    def _draw_content(self):
        self.image.fill('white')

        money_text = self.font.render(f"Geld: {self.money:.2f} €", True, (0, 0, 0))
        sufflevel_text = self.font.render(f"Suff: {self.suff_level}", True, (0, 0, 0))
        bierdurst_text = self.font.render(f"Bierdurst: {self.bierdurst}", True, (0, 0, 0))


        money_rect = money_text.get_rect()
        money_rect.midleft = (20, 20)
        sufflevel_rect = sufflevel_text.get_rect()
        sufflevel_rect.midright = (WIDTH - 20, 20)
        bierdurst_rect = bierdurst_text.get_rect()
        bierdurst_rect.center = (WIDTH_H, 20)

        self.image.blit(money_text, money_rect)
        self.image.blit(sufflevel_text, sufflevel_rect)
        self.image.blit(bierdurst_text, bierdurst_rect)


    def update(self, money, bierdurst, suff):
        self.money = money
        self.bierdurst = bierdurst
        self.suff_level = suff
        self._draw_content()

class InteractionTextBox(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.GroupSingle):
        super().__init__(group)

        self.w = 0.5 * WIDTH
        self.h = 0.2 * HEIGHT

        self.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (WIDTH_H, HEIGHT - 20)

        self.font = pygame.font.Font(None, 24)
        self.hintfont = pygame.font.Font(None, 18)
        self.msg = ""

    def _draw_message(self):
        self.image.fill(pygame.SRCALPHA)

        pygame.draw.rect(self.image, 'white', pygame.rect.Rect(0, 0, self.w, self.h), 0, 20)

        drawText(self.image, self.msg, (0, 0, 0), self.font, True)

        # show disappear hints:

        text = self.hintfont.render("Drücke Enter zum Fortfahren...", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.midbottom = (self.w // 2, self.h - 20)

        self.image.blit(text, text_rect)

    def set_msg(self, msg):
        self.msg = msg

    def update(self):
        self._draw_message()

class InventoryMenu(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.GroupSingle):
        super().__init__(group)

        self.w = 0.8 * WIDTH
        self.h = 0.8 * HEIGHT

        self.w_h = self.w // 2
        self.h_h = self.h // 2

        self.image = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft = (0, 0))

        self.background = pygame.Surface((WIDTH, HEIGHT))
        self.background.fill('white')
        self.background.set_alpha(150)
        self.background_rect = self.background.get_rect(topleft = (0, 0))

        self.image.blit(self.background, self.background_rect)

        self.content = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        self.content_rect = self.content.get_rect(center = (WIDTH_H, HEIGHT_H))

        self.inventory = None

        self.title_font = pygame.font.Font(None, 36)
        self.content_font = pygame.font.Font(None, 24)
        self.hint_font = pygame.font.Font(None, 18)

    def _generate_item(self, text_str, subtext_str, image_path):
        width = 150
        width_h = width // 2
        height = 2*96
        surf = pygame.Surface((width, height), pygame.SRCALPHA)


        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (96, 96))
        image_rect = image.get_rect()
        image_rect.midtop = (width_h, 0)
        y = 100
        text = self.content_font.render(text_str, True, 'black')
        text_rect = text.get_rect()
        text_rect.midtop = (width_h, y)
        y += (5 + text.get_height())

        subtext = self.hint_font.render(subtext_str, True, 'black')
        subtext_rect = subtext.get_rect()
        subtext_rect.midtop = (width_h, y)


        surf.blit(image, image_rect)
        surf.blit(text, text_rect)
        surf.blit(subtext, subtext_rect)

        return surf


    def _render_text(self):
        padding = 20
        y_start = padding
        title_text = self.title_font.render("Inventar vom Bierdurstmann", True, 'black')
        title_rect = title_text.get_rect()
        title_rect.midtop = (self.w_h, y_start)

        total_width = self.w - 2*padding

        y_start += (padding + title_text.get_height())

        money_surf = self._generate_item(f"{self.inventory.content['money']:.2f} €", "Geld", "game/assets/raw_images/money_coins.webp")
        beer_surf = self._generate_item(f"{self.inventory.content['beer']}", "Bier", "game/assets/raw_images/beer_icon.webp")
        ## compute stuff
        content_width = money_surf.get_width() + beer_surf.get_width()
        empty_width = total_width - content_width
        distance_width = empty_width // 3
        x_start = padding + distance_width
        ## create rects
        money_rect = money_surf.get_rect()
        money_rect.topleft = (x_start, y_start)
        x_start += (distance_width + money_surf.get_width())
        beer_rect = beer_surf.get_rect(topleft = (x_start, y_start))
        

        y_start += (money_surf.get_height())

        bottle_surf = self._generate_item(f"{self.inventory.content['bottle']}", "Pfand Flaschen", "game/assets/raw_images/Pfandflaschen.webp")
        can_surf = self._generate_item(f"{self.inventory.content['can']}", "Pfand Dosen", "game/assets/raw_images/pfand_dosen.webp")
        trash_surf = self._generate_item(f"{self.inventory.content['trash']}", "Müll", "game/assets/raw_images/trash.webp")
        ## compute stuff
        content_width = bottle_surf.get_width() + can_surf.get_width() + trash_surf.get_width()
        empty_width = total_width - content_width
        distance_width = empty_width // 4
        x_start = padding + distance_width

        bottle_rect = bottle_surf.get_rect(topleft = (x_start, y_start))
        x_start += (distance_width + bottle_surf.get_width())

        can_rect = can_surf.get_rect(topleft = (x_start, y_start))
        x_start += (distance_width + can_surf.get_width())

        trash_rect = trash_surf.get_rect(topleft = (x_start, y_start))


        hint_text = self.hint_font.render("Drücke Escape um fortzufahren...", True, 'black')
        hint_rect = hint_text.get_rect()
        hint_rect.midbottom = (self.w_h, self.h - padding)

        self.content.blit(title_text, title_rect)
        self.content.blit(money_surf, money_rect)
        self.content.blit(beer_surf, beer_rect)
        self.content.blit(bottle_surf, bottle_rect)
        self.content.blit(can_surf, can_rect)
        self.content.blit(trash_surf, trash_rect)
        self.content.blit(hint_text, hint_rect)

    def _draw_content(self):
        self.image.fill(pygame.SRCALPHA)
        self.image.blit(self.background, self.background_rect)

        self.content.fill(pygame.SRCALPHA)
        ## draw Rect

        pygame.draw.rect(self.content, 'white', pygame.rect.Rect(0, 0, self.w, self.h), 0, 10)
        ## Draw Text:
        if self.inventory:
            self._render_text()

        self.image.blit(self.content, self.content_rect)

    def update(self, inventory: BierdurstmannInventory):
        self.inventory = inventory
        self._draw_content()
