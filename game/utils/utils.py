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

def clamp(value, lower, upper):
    if value > upper:
        return upper
    elif value < lower:
        return lower
    else:
        return value
    

def interpolate(x, x1, x2, y1, y2):
    if (x2-x1) > 0:
        return y1 + x * ((y2 - y1)/(x2-x1))
    else:
        return None # Error Case
    
