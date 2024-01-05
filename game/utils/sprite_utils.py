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
import pygame

def load_sprite(file, start_col, start_row, num_cols, num_rows, total_rows, total_cols, size = None):
    sheet = pygame.image.load(file).convert()
    sheet.set_colorkey((255, 255, 255))

    sheet_w, sheet_h = sheet.get_size()
    sprite_w = sheet_w // total_cols
    sprite_h = sheet_h // total_rows

    sprites = []

    for row in range(num_rows):
        current_h = sprite_h * (row + start_row)
        for col in range(num_cols):
            current_w = sprite_w * (col + start_col)
            image = sheet.subsurface(pygame.rect.Rect(current_w, current_h, sprite_w, sprite_h))
            if size:
                image = pygame.transform.scale(image, size).convert()
                image.set_colorkey((255, 255, 255))
            sprites.append(image)

    return sprites


def load_sprite_with_sprite_size(file, start_col, start_row, num_cols, num_rows, sprite_w, sprite_h, size = None):
    sheet = pygame.image.load(file).convert_alpha()

    sprites = []

    current_h = 0
    current_w = 0
    for row in range(num_rows):
        current_h = sprite_h * (row + start_row)
        for col in range(num_cols):
            current_w = sprite_w * (col + start_col)
            image = sheet.subsurface(pygame.rect.Rect(current_w, current_h, sprite_w, sprite_h))
            if size:
                image = pygame.transform.scale(image, size).convert_alpha()
            sprites.append(image)

    return sprites