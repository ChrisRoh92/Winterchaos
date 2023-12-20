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
from typing import List
from .base_level import BaseLevel


class GameLevel(BaseLevel):
    def __init__(self):
        pass

    # ------------------------- #
    # 'Public Methods'          #
    # ------------------------- #

    def update(self, dt:float, events: List[pygame.event.Event]):
        pass

    def render(self, screen: pygame.Surface):
        pass

    def reset(self):
        pass

    def shutdown(self):
        pass

    # ------------------------- #
    # 'Private Methods'         #
    # ------------------------- #