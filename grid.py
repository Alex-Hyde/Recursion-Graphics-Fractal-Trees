# --------------------------------------------------------------------
# Program: Grid Classes
# Author: Alex Hyde
# Date: Oct 25 2019
# Description: Abstract grid class, inherited by a concrete word grid
#   sub class and concrete menu sub class.
# Input: Menu class allows button click processing through button
#   class
# --------------------------------------------------------------------

import pygame
import label
import button

pygame.init()

# colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# alignment constants
LEFT = 0
RIGHT = 1
CENTER = 0.5
TOP = 0
BOTTOM = 1


# abstract grid class
class Grid:
    def __init__(self, rect, r, c, gap=0, visible_lines=True, color=BLACK):
        self.rect = rect
        self.x, self.y, self.w, self.h = rect
        self.r = r
        self.c = c
        self.gap = gap
        self.cWidth = (self.w - gap * (c + 1)) / c  # column width
        self.cHeight = (self.h - gap * (r + 1)) / r  # column height
        self.points = self.create_points()  # creates list of cell points
        self.current = -1  # used for iterating through points
        self.visible_lines = visible_lines  # visiblity boolean
        self.color = color

    # creates evenly spaced cell points with gap
    def create_points(self):
        points = []
        for y in range(self.r):
            for x in range(self.c):
                points.append((self.x + self.gap * (x + 1) + self.cWidth * x,
                               self.y + self.gap * (y + 1) + self.cHeight * y))
        return points

    def draw(self, win):
        if self.visible_lines:  # if visible
            pygame.draw.rect(win, color, self.rect, 1)

            for p in self.points:
                pygame.draw.rect(win, self.color, (p[0], p[1], self.cWidth, self.cHeight), 1)

    # return cell index, given the position of the cell in the grid
    def get_cell_index(self, x, y):
        if x < 0 or x >= self.c:
            return
        if y < 0 or y >= self.y:
            return
        return y*self.c + x

    # retrun x and y position (column, row) of cell, given the index of the cell
    def get_cell_pos(self, ind):
        if ind < len(self):
            return ind % self.c, ind // self.c

    # return coordinates of a cell, given its index
    def get_cell_coords(self, ind):
        return self.points[ind]

    # return if two cells (represented by index) are adjacent
    def is_adjacent(self, a, b, diagonals=True):
        ax, ay = self.get_cell_pos(a)
        bx, by = self.get_cell_pos(b)
        if diagonals:
            return abs(ax - bx) <= 1 and abs(ay - by) <= 1
        else:
            return (abs(ax - bx) == 1 and (ay - by) == 0) or ((ax - bx) == 0 and abs(ay - by) == 1)

    def set_visible(self, b):
        self.visible_lines = b

    def is_visible(self, b):
        return self.visible_lines

    def set_color(self, color):
        self.color = color

    def __str__(self):
        return ", ".join(list(map(lambda a: "(" + str(a[0]) + ", " + str(a[1]) + ")", self.points)))

    # return number of cells
    def __len__(self):
        return self.r*self.c

    # used for iterating through points
    def __iter__(self):
        return self

    # used for iterating through points
    def __next__(self):
        self.current += 1
        if self.current < len(self.points):
            return self.points[self.current]
        self.current = -1
        raise StopIteration


# concrete menu sub class of Grid
class Menu(Grid):
    def __init__(self, rect, r, c, button_text_list, gap=0, button_on_click=None, color=BLACK, visible_lines=True,
                 active=True, visible=True):
        super().__init__(rect, r, c, gap, color=color, visible_lines=visible_lines)
        # button_on_click = is the function run when a button is clicked
        self.button_text_list = button_text_list
        self.button_list = self.create_buttons(button_on_click)
        self.active = active
        self.visible = visible
        self.button_list.actve = active

    # create a list of buttons
    def create_buttons(self, b_on_click):
        b_list = button.ButtonList()

        t_list = self.button_text_list.copy()
        for p in self.points:
            b = button.Button((p[0], p[1], self.cWidth, self.cHeight), text=t_list[0])
            if b_on_click is not None:
                b.on_click = b_on_click
            b_list.add(b)
            del t_list[0]
        return b_list

    def draw(self, win):
        if self.visible_lines:
            pygame.draw.rect(win, self.color, self.rect, 1)
        if self.visible:
            self.button_list.draw(win)

    # return button position (column, row) given the button
    def get_button_pos(self, b):
        ind = self.get_button_ind(b)
        x = ind % self.c
        y = ind // self.c
        return x, y

    # returns list of all clicked buttons
    def get_clicked(self):
        return [self.get_button_ind(b) for b in self.button_list.clicked]

    # returns list of all released buttons
    def get_released(self):
        return [self.get_button_ind(b) for b in self.button_list.released]

    # returns list of all hovered buttons
    def get_hovered(self):
        return [self.get_button_ind(b) for b in self.button_list.hovered]

    # return index of button, given the button
    def get_button_ind(self, b):
        return self.button_list.find(b)

    def set_active(self, b):
        self.active = b
        self.button_list.set_active(b)

    def set_visible(self, b):
        self.visible = b
        self.button_list.set_visible(b)

    # return button, given the position of the button in the grid
    def get_button_by_pos(self, x, y):
        return self.button_list.get(y*self.c + x)

    # return button, given the index of the button
    def get_button(self, ind):
        return self.button_list.get(ind)

    def __str__(self):
        return 


# concrete word grid sub class of Grid
class WordGrid(Grid):
    def __init__(self, rect, r, c, text_list, gap=0, visible_lines=True, text_hAlign=CENTER, text_vAlign=CENTER):
        super().__init__(rect, r, c, gap, visible_lines)
        # text alignment in cell
        self.text_hAlign = text_hAlign
        self.text_vAlign = text_vAlign

        self.text_list = text_list
        self.labels = self.create_labels()  # create list of drawable text labels

    # return a list of drawable text labels
    def create_labels(self):
        labels = []
        for i, p in enumerate(self.points):
            l = label.Label(self.text_list[i])
            l.set_x(p[0] + (self.cWidth - l.get_width()) * self.text_hAlign)
            l.set_y(p[1] + (self.cHeight - l.get_height()) * self.text_vAlign)
            labels.append(l)
        return labels

    # return label given its text
    def get_label(self, text):
        if self.text_list is not None and text in self.text_list:
            return self.labels[self.text_list.index(text)]
        return -1

    def get_label_by_index(self, ind):
        return self.labels[ind]

    # update position of text in cell (alignment)
    # used when changing font size of changing alignment
    def update_labels_pos(self):
        for i, l in enumerate(self.labels):
            l.set_x(self.points[i][0] + (self.cWidth - l.get_width()) * self.text_hAlign)
            l.set_y(self.points[i][1] + (self.cHeight - l.get_height()) * self.text_vAlign)

    # return index of label, given its text
    def find_label_index(self, text):
        if self.text_list is not None and text in self.text_list:
            return self.text_list.index(text)
        return -1

    def draw(self, win):
        super().draw(win)
        for l in self.labels:
            l.draw(win)
