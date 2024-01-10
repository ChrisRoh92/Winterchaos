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
FPS = 120

## Sprite Params
PLAYER_SIZE = 48
PLAYER_SIZE_H = PLAYER_SIZE // 2
PLAYER_SPEED = 200
PLAYER_FRAME_FACTOR = 20

## Fonts:
FONT_PATH = "game/assets/fonts/Ubuntu-Regular.ttf"


## Map 
MAIN_WORLD_MAP_FILE = "game/assets/tiled_map/map_tiled.tmx" ## TODO(chrohne): rename
GROCERY_MAP_FILE = "game/assets/tiled_map/rewe_map.tmx" ## TODO(chrohne): rename

TRASH_BIN_CONTENT_UPDATE_MIN = 5
TRASH_BIN_CONTENT_UPDATE_MAX = 20
TRASH_BIN_MAX_MONEY = 1.0
TRASH_BIN_MAX_CANS_BOTTLES_RANDOM = 2
TRASH_BIN_MAX_CANS_BOTTLES = 10
TRASH_BIN_MAX_TRASH = 10



## Main Menu
BUBBLE_MAX_RADIUS, BUBBLE_MIN_RADIUS = 10, 5
BASE_BUBBLE_SPEED = 1000
MAX_BUBBLES = 20
BEER_YELLOW = (252, 173, 3)
MENU_MARGIN = 10
BTN_MARGIN = 10


MENU_BTN_WIDTH, MENU_BTN_HEIGHT = 400, 40
MENU_BTN_WIDTH_H, MENU_BTN_HEIGHT_H = MENU_BTN_WIDTH // 2, MENU_BTN_HEIGHT // 2
BTN_BACKGROUND_ACTIVE, BTN_BACKGROUND_INACTIVE = (210, 105, 30), (250, 166, 26)
BTN_TEXT_ACTIVE, BTN_TEXT_INACTIVE = (255, 255, 255), (0, 0, 0)
BTN_BACKGROUND_COLOR = {False: BTN_BACKGROUND_ACTIVE, True: BTN_BACKGROUND_INACTIVE}
BTN_TEXT_COLOR = {False: BTN_TEXT_ACTIVE, True: BTN_TEXT_INACTIVE}
MENU_WIDTH, MENU_HEIGHT = MENU_BTN_WIDTH + 2 * MENU_MARGIN, 5 * MENU_BTN_HEIGHT + 2 * MENU_MARGIN + 4 * BTN_MARGIN
MENU_WIDTH_H, MENU_HEIGHT_H = MENU_WIDTH // 2, MENU_HEIGHT // 2