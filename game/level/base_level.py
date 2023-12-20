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
from abc import ABC, abstractmethod
import enum, pygame
from typing import List

class LEVELS(enum.Enum):
    UNDEFINED       = 0
    MAIN_MENU_LEVEL = 1
    GAME_LEVEL      = 2

class BaseLevel(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def update(self, dt:float, events: List[pygame.event.Event]):
        pass

    @abstractmethod
    def render(self, screen: pygame.Surface):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def shutdown(self):
        pass