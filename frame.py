# --------------------------------------------------------------------
# Program: Frame Class
# Author: Alex Hyde
# Date: Oct 25 2019
# Description: Class for storing and processing all drawable and
#   button of a current screen. Used for storing different screens
#   such as menus and game screens.
# --------------------------------------------------------------------

import button
import pygame


# frame class for storing and processing current drawables and buttons
class Frame:
    def __init__(self, drawables, button_list=None, fill=(255, 255, 255)):
        self.drawables = drawables
        if button_list is None:
            button_list = []
        self.button_lists = button_list
        self.fill = fill

    def draw(self, win):
        win.fill(self.fill)
        for d in self.drawables:
            d.draw(win)

    # process buttons
    def process_events(self, click_bool, release_bool, mousepos):
        for button_list in self.button_lists:
            button_list.process_events(click_bool, release_bool, mousepos)

    def add(self, drawable):
        self.drawables.append(drawable)

    # return surface object with the current screen of the frame
    def get_screen(self, w, h):
        surf = pygame.Surface((w, h))
        self.draw(surf)
        return surf

    def __add__(self, other):
        return Frame(self.drawables + other.drawables, self.button_list + other.button_list, self.fill)
