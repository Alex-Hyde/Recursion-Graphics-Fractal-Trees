# --------------------------------------------------------------------
# Program: Button Classes
# Author: Alex Hyde
# Date: Oct 25 2019
# Description: Button classes for creating buttons and processing
#   button clicks. Fully customizable with custom on click and release
#   functions.
# Input: Allows easy processing of user clicks.
# --------------------------------------------------------------------

import pygame
import label
import color as c

pygame.init()

# alignment constants
LEFT = 0
RIGHT = 1
TOP = 0
BOTTOM = 1
CENTER = 0.5


# button list class for easily processing multiple buttons on one screen
class ButtonList:
    def __init__(self, buttonList=None):
        if buttonList is None:
            buttonList = []
        self.buttonList = list(buttonList)  # if passed a tuple
        self.current = -1  # used for iteration
        self.clicked = []
        self.released = []
        self.hovered = []
        self.visible = True
        self.active = True

    # return button index, given the button
    def find(self, item):
        if item in self.buttonList:
            return self.buttonList.index(item)
        else:
            return -1

    # returns button given its index
    def get(self, ind):
        return self.buttonList[ind]

    def set(self, ind, new):
        self.buttonList[ind] = new

    # return button at a set of coordinates, -1 if the is no button at those coordinates
    def get_button_at(self, pos):
        for b in self.buttonList:
            if b.is_hover(pos):
                return b
        return -1

    def draw(self, win):
        if self.visible:  # if button list is visible
            for b in self.buttonList:
                b.draw(win)

    def add(self, button):
        self.buttonList.append(button)

    # process button clicks, releases and hovers
    def process_events(self, click_bool, release_bool, mousepos):
        self.released = []
        self.clicked = []
        self.hovered = []
        if self.active:  # if the button list is active
            for b in self.buttonList:
                if type(b) == Slider:
                    b.process(click_bool, release_bool, mousepos)
                elif (b.is_hover(mousepos) or b.is_clicked) and b.is_active():
                    if click_bool:
                        b.on_click_default()
                        b.on_click(b)
                        self.clicked.append(b)
                    elif release_bool and b.is_clicked:
                        b.on_release_default()
                        b.on_release(b)
                        self.released.append(b)
                    else:
                        b.on_hover()
                        self.hovered.append(b)
                else:
                    b.reset_color()
        else:
            for b in self.buttonList:
                if type(b) == Slider:
                    b.slide_button.reset_color()
                else:
                    b.reset_color()

    # return all clicked buttons
    def get_clicked(self):
        return self.clicked

    # return all released buttons
    def get_released(self):
        return self.released

    # return all hovered buttons
    def get_hovered(self):
        return self.hovered

    def set_visible(self, b):
        self.visible = b

    def set_active(self, b):
        self.active = b

    # add two button lists
    def __add__(self, other):
        return ButtonList(self.buttonList + other.buttonList)

    # used for iteration
    def __iter__(self):
        return self

    # used for iteration
    def __next__(self):
        self.current += 1
        if self.current < len(self.buttonList):
            return self.buttonList[self.current]
        self.current = -1
        raise StopIteration


class Button:
    def __init__(self, rect, fColor=(255, 255, 255), bColor=(0, 0, 0), onHoldColor=(100, 100, 100),
                 onHoverColor=(200, 200, 200), tColor=(0, 0, 0), border=1, text="", visible=True, active=True,
                 tAlignx=CENTER, tAligny=CENTER, text_size=18):
        self.x, self.y, self.w, self.h = rect
        self.b = border

        self.text = text
        self.text_size = text_size
        # text alignment
        self.tAlignx = tAlignx
        self.tAligny = tAligny
        # colors
        self.fColor = fColor
        self.onHoldColor = onHoldColor
        self.currentFillColor = fColor
        self.onHoverColor = onHoverColor
        self.bColor = bColor
        self.tColor = tColor
        # rendering text drawable
        self.rendered_text = None
        self.render_text()

        self.visible = visible
        self.active = active
        self.is_clicked = False
        self.is_hovered = False
        self.on_click = self.blank_func  # on click function (to be replaced in an instantiated button)
        self.on_release = self.blank_func  # on release function (to be replaced in an instantiated button)
        self.values = {}  # can be used to store custom values

    def draw(self, win):
        if self.visible:
            if self.currentFillColor is not None:
                pygame.draw.rect(win, self.currentFillColor, self.rect())
            if self.bColor is not None:
                self.draw_border(win)
            self.rendered_text.draw(win)

    def draw_border(self, win):
        x, y, w, h = self.rect()
        pygame.draw.rect(win, self.bColor, (x, y, w, self.b))
        pygame.draw.rect(win, self.bColor, (x, y + self.b, self.b, h - self.b))
        pygame.draw.rect(win, self.bColor, (x + self.b, y + h - self.b, w - self.b, self.b))
        pygame.draw.rect(win, self.bColor, (x + w - self.b, y + self.b, self.b, h - self.b))

    # renders text drawable
    def render_text(self):
        self.rendered_text = label.Label(self.text, color=self.tColor, size=self.text_size)
        self.reset_text_pos()

    # sets text drawable position (based on alignment)
    def reset_text_pos(self):
        self.rendered_text.set_x(self.x + (self.w-self.rendered_text.get_width())*self.tAlignx)
        self.rendered_text.set_y(self.y + (self.h-self.rendered_text.get_height())*self.tAligny)

    # empty function (to be replaced by custom functions in instantiated button objects)
    def blank_func(self, blank):
        pass

    # return boolean if the mouse position collides with the button
    def is_hover(self, mousepos):
        x, y = mousepos
        return self.x < x < self.x + self.w and self.y < y < self.y + self.h

    # default function when button if clicked (change color)
    def on_click_default(self):
        self.currentFillColor = self.onHoldColor
        self.is_clicked = True

    # default function when button if released (change color)
    def on_release_default(self):
        self.currentFillColor = self.fColor
        self.is_clicked = False

    # default function when button if hovered (change color)
    def on_hover(self):
        if not self.is_clicked:
            self.currentFillColor = self.onHoverColor

    def convert_to_slider(self, slide_wh, change=False, text_slider_percent=50, color=c.WHITE, bColor=c.BLACK, border=1,
                          start_value=0, end_value=100, slide_value=None, slide_color=c.BLACK, text_size=18,
                          tColor=c.BLACK, slider_border=5):
        return Slider(self.rect(), slide_wh, text_slider_percent, color, bColor, border, start_value, end_value,
                      slide_value, slide_color, self.text, self.text_size, self.tAlignx, self.tAligny, tColor,
                      slider_border, self.fColor, self.bColor, self.onHoldColor, self.onHoverColor,
                      visible=self.visible, active=self.active)

    # --------------------SETTER AND GETTER METHODS--------------------

    def set_text(self, text):
        self.text = text
        self.render_text()

    def rect(self):
        return self.x, self.y, self.w, self.h

    def set_x(self, x):
        xdif = x - self.x
        self.x += xdif
        self.rendered_text.set_x(self.rendered_text.x + xdif)

    def set_y(self, y):
        ydif = y - self.y
        self.y += ydif
        self.rendered_text.set_y(self.rendered_text.y + ydif)

    def get_text(self):
        return self.text

    def get_label(self):
        return self.rendered_text

    def set_text_size(self, size):
        self.text_size = size
        self.render_text()

    def set_fColor(self, color):
        self.fColor = color
        if not self.is_clicked and not self.is_hovered:
            self.currentFillColor = self.fColor

    def set_hoverColor(self, color):
        self.onHoverColor = color
        if self.is_hovered and not self.is_clicked:
            self.currentFillColor = self.onHoverColor

    def set_holdColor(self, color):
        self.onHoldColor = color
        if not self.is_hovered and self.is_clicked:
            self.currentFillColor = self.onHoldColor

    def set_bColor(self, color):
        self.bColor = color

    def reset_color(self):
        self.currentFillColor = self.fColor

    def set_active(self, torf):
        self.active = torf

    def is_active(self):
        return self.active

    def set_visible(self, torf):
        self.visible = torf

    def is_visible(self):
        return self.visible

    def color_scheme(self, color):
        if color == "black":
            self.fColor = c.BLACK
            self.tColor = c.WHITE
            self.bColor = c.WHITE
            self.onHoverColor = c.grey(100)
            self.onHoldColor = c.grey(150)
        elif color == "white":
            self.fColor = c.WHITE
            self.tColor = c.BLACK
            self.bColor = c.BLACK
            self.onHoverColor = c.grey(200)
            self.onHoldColor = c.grey(100)
        elif color == "red":
            self.fColor = c.RED
            self.tColor = c.BLACK
            self.bColor = c.BLACK
            self.onHoverColor = c.basic_color(180, "r", 80)
            self.onHoldColor = c.basic_color(120, "r", 70)
        elif color == "green":
            self.fColor = c.GREEN
            self.tColor = c.BLACK
            self.bColor = c.BLACK
            self.onHoverColor = c.basic_color(180, "g", 80)
            self.onHoldColor = c.basic_color(120, "g", 70)
        elif color == "blue":
            self.fColor = c.BLUE
            self.tColor = c.BLACK
            self.bColor = c.BLACK
            self.onHoverColor = c.basic_color(180, "b", 80)
            self.onHoldColor = c.basic_color(120, "b", 70)
        self.render_text()
        self.reset_color()


class Slider:
    def __init__(self, rect, slide_wh, text_slider_percent=50, color=c.WHITE, bColor=c.BLACK, border=1, start_value=0,
                 end_value=100, slide_value=None, slide_color=c.BLACK, text="", text_size=18, tAlignx=CENTER,
                 tAligny=CENTER, tColor=c.BLACK, slider_border=5,
                 butfColor=(255, 255, 255), butbColor=(0, 0, 0), butonHoldColor=(100, 100, 100),
                 butonHoverColor=(200, 200, 200), buttColor=(0, 0, 0), butborder=1, buttext="", visible=True,
                 active=True, buttext_size=10):
        self.x, self.y, self.w, self.h = rect
        self.b = border
        self.text_h = (self.h - self.b * 2) * text_slider_percent/100
        self.slider_h = (self.h - self.b * 2) - self.text_h
        self.slide_x1 = self.x + self.b + slider_border
        self.slide_x2 = self.x + self.w - self.b - slider_border
        self.slide_y = self.y + self.h - self.b - self.slider_h/2
        self.slide_button = Button((self.slide_x1 - slide_wh[0]/2, self.slide_y - slide_wh[1]/2, slide_wh[0],
                                    slide_wh[1]),
                                   butfColor, butbColor, butonHoldColor, butonHoverColor, buttColor,
                                   butborder, buttext, visible, active, CENTER, CENTER, buttext_size)
        self.slide_color = slide_color
        self.color = color
        self.bColor = bColor
        self.tColor = tColor
        self.text = text
        self.is_dynamic_text = "@" in text
        self.text_size = text_size
        self.tAlignx = tAlignx
        self.tAligny = tAligny
        self.start_value = start_value
        self.end_value = end_value
        self.visible = visible
        if slide_value is None:
            slide_value = start_value
        elif slide_value < start_value or slide_value > end_value:
            raise Exception("Slider value outside of slider range")
        self.slide_value = slide_value
        self.buttonx = self.slide_x1 + (self.slide_x2 - self.slide_x1) * self.convert_slider_value_to_percent()
        self.slide_button.set_x(self.buttonx - self.slide_button.w/2)

        self.action = self.blank_func

        self.rendered_text = None
        self.render_text()

    def draw(self, win):
        if self.is_visible():
            pygame.draw.rect(win, self.color, self.rect())
            self.draw_border(win)
            self.draw_slider(win)
            self.rendered_text.draw(win)

    def draw_slider(self, win):
        pygame.draw.line(win, self.slide_color, (self.slide_x1, self.slide_y), (self.slide_x2, self.slide_y), 3)
        self.slide_button.draw(win)

    def draw_border(self, win):
        x, y, w, h = self.rect()
        pygame.draw.rect(win, self.bColor, (x, y, w, self.b))
        pygame.draw.rect(win, self.bColor, (x, y + self.b, self.b, h - self.b))
        pygame.draw.rect(win, self.bColor, (x + self.b, y + h - self.b, w - self.b, self.b))
        pygame.draw.rect(win, self.bColor, (x + w - self.b, y + self.b, self.b, h - 2 * self.b))

    def dynamic_text(self):
        return self.text.replace("@", str(int(self.slide_value)))

    # returns the slider's value
    def value(self):
        return self.slide_value

    # empty function (to be replaced by custom functions in instantiated button objects)
    def blank_func(self, blank):
        pass

    # renders text drawable
    def render_text(self):
        self.rendered_text = label.Label(self.dynamic_text(), color=self.tColor, size=self.text_size)
        self.reset_text_pos()

    # sets text drawable position (based on alignment)
    def reset_text_pos(self):
        self.rendered_text.set_x(self.x + (self.w - self.rendered_text.get_width()) * self.tAlignx)
        self.rendered_text.set_y(self.y + self.b + (self.text_h - self.rendered_text.get_height()) * self.tAligny)

    def convert_slider_pos_to_percent(self):
        return (self.buttonx - self.slide_x1) / (self.slide_x2 - self.slide_x1)

    def convert_slider_value_to_percent(self):
        return (self.slide_value - self.start_value) / (self.end_value - self.start_value)

    def rect(self):
        return self.x, self.y, self.w, self.h

    def process(self, click_bool, release_bool, mousepos):
        if (self.slide_button.is_hover(mousepos) or self.slide_button.is_clicked) and self.slide_button.is_active():
            if click_bool:
                self.slide_button.on_click_default()
            elif release_bool and self.slide_button.is_clicked:
                self.slide_button.on_release_default()
            else:
                self.slide_button.on_hover()
        else:
            self.slide_button.reset_color()

        if self.slide_button.is_clicked:
            x = mousepos[0]
            if x < self.slide_x1:
                x = self.slide_x1
            elif x > self.slide_x2:
                x = self.slide_x2
            self.slide_button.set_x(int(x - self.slide_button.w/2))
            self.buttonx = x

        self.slide_value = self.start_value + (self.end_value - self.start_value) * self.convert_slider_pos_to_percent()

        if self.is_dynamic_text:
            self.render_text()

        self.action(self)

    def is_visible(self):
        return self.visible

    def get_label(self):
        return self.rendered_text

    def set_text_size(self, size):
        self.text_size = size
        self.render_text()

    def set_value(self, v):
        self.slide_value = v
        if self.slide_value < self.start_value or self.slide_value > self.end_value:
            raise Exception("Slider value outside of slider range")
        self.buttonx = self.slide_x1 + (self.slide_x2 - self.slide_x1) * self.convert_slider_value_to_percent()
        self.slide_button.set_x(self.buttonx - self.slide_button.w / 2)
