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

## General params
WIDTH, HEIGHT = 800, 600
WIDTH_H, HEIGHT_H = WIDTH // 2, HEIGHT // 2
FPS = 60

## Sprite Params
PLAYER_SIZE = 48
PLAYER_SIZE_H = PLAYER_SIZE // 2
PLAYER_SPEED = 200
PLAYER_FRAME_FACTOR = 10

## Fonts:
FONT_PATH = "game/assets/fonts/Ubuntu-Regular.ttf"

TRASH_BIN_CONTENT_UPDATE_MIN = 5
TRASH_BIN_CONTENT_UPDATE_MAX = 20
TRASH_BIN_MAX_MONEY = 1.0
TRASH_BIN_MAX_CANS_BOTTLES_RANDOM = 2
TRASH_BIN_MAX_CANS_BOTTLES = 10
TRASH_BIN_MAX_TRASH = 10