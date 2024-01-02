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
import pygame, copy

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
    
def drawText(surface: pygame.Surface, text, color, font, aa=False, bkg=None):
    PADDING = 20
    width = surface.get_width() - 2 * PADDING
    height = surface.get_height() - 3 * PADDING
    width_h, height_h = width // 2, height // 2
    rect = pygame.rect.Rect(PADDING, PADDING, width, height)
    y = rect.top
    lineSpacing = 5

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        image_rect = image.get_rect(midtop = (width_h + PADDING, y))
        surface.blit(image, image_rect)
        # surface.blit(image, (rect.centerx, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text