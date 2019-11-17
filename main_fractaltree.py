# --------------------------------------------------------------------
# Program: Fractal Trees - Recusion implementaion
# Author: Alex Hyde
# Date: Nov 06 2019
# Description: Program implementing recursion algorithms to generate
#   trees, mountains, and other aspects of nature that are created
#   using recursion. The program can generate a scene or individual
#   objects whose characteristics can be modified by the user.
# Input: The program takes input from the user through button actions.
# --------------------------------------------------------------------

import pygame
import math
import color as c
import vector
import frame
import random
import label
import button
import grid

pygame.init()

# window screen constants
WIN_WIDTH = 1000
WIN_HEIGHT = 800
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))


# class for easy accessing and storing of all settings variables in program
#   with methods to be applied to buttons to easily change settings
class Settings:
    def __init__(self):
        # Scene
        # Mountain
        self.mountain_start = WIN_HEIGHT//2 + 50
        self.mountain_end = WIN_HEIGHT//2 + 100
        self.mountain_frequency = 1

        # Foreground
        self.foreground_start = self.mountain_end
        self.foreground_end = WIN_HEIGHT
        self.secondary_foreground_start = self.foreground_end - 100
        self.bush_chance = 3  # chance of getting a bush spawn
        self.flower_chance = 2  # chance of getting a flower
        self.tree_chance = 3  # chance of getting a tree

    @staticmethod
    def set_mountain_start(b):
        settings.mountain_start = int(b.value())

    @staticmethod
    def set_mountain_end(b):
        settings.mountain_end = int(b.value())
        settings.foreground_start = int(b.value())

    @staticmethod
    def set_mountain_frequency(b):
        settings.mountain_frequency = int(b.value())

    @staticmethod
    def set_foreground_end(b):
        settings.foreground_end = int(b.value())

    @staticmethod
    def set_secondary_foreground_start(b):
        settings.secondary_foreground_start = int(b.value())

    @staticmethod
    def set_bush_chance(b):
        settings.bush_chance = int(b.value())

    @staticmethod
    def set_flower_chance(b):
        settings.bush_chance = int(b.value())

    @staticmethod
    def set_tree_chance(b):
        settings.tree_chance = int(b.value())


# abstract line class
class Line:
    def __init__(self, a, b):
        self.a = a
        self.b = b


# surface extension to make it drawable in a draw loop
class Surface_Drawable(pygame.Surface):
    def draw(self, win):
        win.blit(self, (0, 0))


# flower class for storing and creating a flower
class Flower:
    def __init__(self, start_pos, stem_len, radius, sColor=c.GREEN, pColor=c.WHITE, cColor=c.BLACK, stem_width=1,
                 tilt_angle=0,
                 tilt_count=0):
        self.stem_points = [start_pos.get(True)]
        self.petals_center = None
        self.radius = radius
        self.create_stem(start_pos, stem_len, random_if_range(tilt_angle), tilt_count)
        self.sColor = sColor
        self.pColor = pColor
        self.cColor = cColor
        self.stem_width = stem_width

    def create_stem(self, start_pos, stem_len, tilt_angle, tilt_count):
        sec_len = stem_len / tilt_count
        last_pos = start_pos
        for i in range(tilt_count):
            new_pos = last_pos.get_point_on_line(270 - tilt_angle * i, sec_len)
            self.stem_points.append(new_pos.get(True))
            last_pos = new_pos
        self.petals_center = new_pos.get(True)

    def draw(self, win):
        pygame.draw.lines(win, self.sColor, False, self.stem_points, self.stem_width)
        pygame.draw.circle(win, self.pColor, self.petals_center, self.radius)
        pygame.draw.circle(win, self.cColor, self.petals_center, self.radius//2)


# mountain class for storing and creating a mountain
class Mountain:
    def __init__(self, start_pos, end_pos, height, height_change, start_height, iters, color=c.GREY):
        self.points = [start_pos, end_pos]
        self.iters = iters
        self.create_mountain(start_pos, end_pos, height, height_change, start_height, True)
        self.points = [p.get(True) for p in self.points]
        self.color = color

    def create_mountain(self, start_pos, end_pos, height, height_change, start_height=None, first=False, count=0):
        if count < self.iters:

            new_x = (start_pos.x + end_pos.x) / 2

            if not first:
                sign = random.choice([-1, 1])
                # create new point
                new_pos = vector.Vec2(new_x,
                                      vector.Vec2.poi(start_pos, end_pos, vector.Vec2(new_x, 0),
                                                      vector.Vec2(new_x, 1)).y + random_if_range(height) * sign)
                new_h = height[0] * height_change, height[1] * height_change
            else:
                # create new point
                new_pos = vector.Vec2(new_x,
                                      vector.Vec2.poi(start_pos, end_pos, vector.Vec2(new_x, 0),
                                                      vector.Vec2(new_x, 1)).y - random_if_range(start_height))
                new_h = height

            # prevents points from going below the base of the mountain
            if new_pos.y > self.points[0].y:
                new_pos.y = self.points[0].y

            # insert point in correct location for polygon drawing
            self.points.insert(self.points.index(end_pos), new_pos)

            # create left side
            self.create_mountain(start_pos, new_pos, new_h, height_change, count=count+1)
            # create right side
            self.create_mountain(new_pos, end_pos, new_h, height_change, count=count+1)

    def draw(self, win):
        pygame.draw.polygon(win, self.color, self.points)


# tree class for storing and creating a tree
class Tree:
    def __init__(self, start_pos, heading, current_length, end_length, current_line_list=None, angle_change=45,
                 len_dec=0.5, width=1, width_dec=1, sColor=c.BROWN, eColor=c.DARK_GREEN, lColor="g",
                 lCRange=(100, 255), two=False, trunk_size=None):
        self.branches = []  # list of branches
        self.leaves = []  # list of leaves
        self.max_level = 0  # what is the farthest branch up the tree
        self.sColor = sColor  # start colour (trunk)
        self.eColor = eColor  # end colour (branches at the end)
        self.lColor = lColor  # colour code for random leaf colour
        self.lCRange = lCRange  # colour range for darkness of leaves
        self.trunk_size = trunk_size
        if two:
            self.branches = self.create_tree2(start_pos, heading, current_length, current_line_list,
                                              angle_change, len_dec, width, health_split=140, first=True)
        else:
            self.branches = self.create_tree(start_pos, heading, current_length, end_length, current_line_list,
                                             angle_change, len_dec, width, width_dec)
        self.set_branch_colors()

    def draw(self, win):
        for branch in self.branches:
            branch.draw(win)
        for leaf in self.leaves:
            leaf.draw(win)

    # set branch colour depending on how far up the tree they are
    def set_branch_colors(self):
        for branch in self.branches:
            grad_strength = branch.level / self.max_level
            r = self.sColor[0] - (self.sColor[0] - self.eColor[0]) * grad_strength
            g = self.sColor[1] - (self.sColor[1] - self.eColor[1]) * grad_strength
            b = self.sColor[2] - (self.sColor[2] - self.eColor[2]) * grad_strength
            branch.set_color([r, g, b])

    # create the branches and leaves for the tree using fractal recursion
    def create_tree(self, start_pos, heading, current_length, end_length, current_line_list=None, angle_change=45,
                    len_dec=50, width=1, width_dec=100, level=0):
        if current_line_list is None:
            current_line_list = []
        if current_length > end_length:
            p = start_pos.get_point_on_line(heading, current_length)
            current_line_list.append(Branch((p.x, p.y), (start_pos.x, start_pos.y), width=width, level=level))

            level += 1

            if level > self.max_level:
                self.max_level = level

            # create left branch
            current_line_list = self.create_tree(p, heading - random_if_range(angle_change),
                                                 current_length * random_if_range(len_dec) / 100, end_length,
                                                 current_line_list, angle_change, len_dec,
                                                 width * random_if_range(width_dec)/100, width_dec, level)
            # create right branch
            current_line_list = self.create_tree(p, heading + random_if_range(angle_change),
                                                 current_length * random_if_range(len_dec) / 100, end_length,
                                                 current_line_list, angle_change, len_dec,
                                                 width * random_if_range(width_dec)/100, width_dec, level)

        else:  # when branch ends(minimum size reached) add leaf
            if random.randrange(4) == 0:  # 1 in 4 chance of having a leaf on the end of a branch
                self.leaves.append(Leaf(start_pos.get(True), c.random_color(self.lCRange[0], self.lCRange[1],
                                                                            self.lColor, random.randrange(50, 100)),
                                        random.randrange(6)))
                if random.randrange(5) == 0:
                    self.leaves[-1].color = c.random_color(self.lCRange[0], self.lCRange[1],
                                                           "b", random.randrange(10, 100))
        return current_line_list

    # second version
    def create_tree2(self, start_pos, heading, length, current_line_list=None,
                     angle_change=45, len_dec=50, width=1, level=0, health_split=140, health=100, health_limit=3,
                     main_branch=True, first=False):
        if current_line_list is None:
            current_line_list = []
        if health > health_limit:
            if first and self.trunk_size is not None:
                temp_len = self.trunk_size
            else:
                temp_len = length
            p = start_pos.get_point_on_line(heading, temp_len * health/100)
            current_line_list.append(Branch((p.x, p.y), (start_pos.x, start_pos.y), width=width, level=level,
                                            health=health/100))

            level += 1

            if level > self.max_level:
                self.max_level = level

            h_left = random_if_range(health_split)  # how much health is passed onto next branches
            h1 = random.randrange(h_left - 100, 100)
            h2 = h_left - h1

            if main_branch:
                m1 = h1 > h2
                m2 = not m1
            else:
                m1, m2 = False, False

            if main_branch:
                if heading < 270 and h1 > h2:
                    h1, h2 = h2, h1
                elif heading > 270 and h2 > h1:
                    h1, h2 = h2, h1

            # create left branch
            current_line_list = self.create_tree2(p, heading - random_if_range(angle_change),
                                                  length,
                                                  current_line_list, angle_change, len_dec,
                                                  width, level, health_split,
                                                  health * h1/100, health_limit, m1)
            # create right branch
            current_line_list = self.create_tree2(p, heading + random_if_range(angle_change),
                                                  length,
                                                  current_line_list, angle_change, len_dec,
                                                  width, level, health_split,
                                                  health * h2/100, health_limit, m2)

        else:  # when branch ends(minimum size reached) add leaf
            if random.randrange(1) == 0:  # 1 in 4 chance of having a leaf on the end of a branch
                self.leaves.append(Leaf(start_pos.get(True), c.random_color(self.lCRange[0], self.lCRange[1],
                                                                            self.lColor, random.randrange(50, 100)),
                                        random.randrange(4)))
        return current_line_list

    def tint_depth(self, strength):
        for branch in self.branches:
            branch.color = add_depth_tint(branch.color, strength)
        for leaf in self.leaves:
            leaf.color = add_depth_tint(leaf.color, strength)


# leaf class for storing and drawing leaves
class Leaf:
    def __init__(self, pos, color, size):
        self.pos = pos
        self.color = color
        self.size = size

    def draw(self, win):
        pygame.draw.circle(win, self.color, self.pos, self.size)


# branch class for storing and drawing branches
class Branch(Line):
    def __init__(self, a, b, color=c.WHITE, width=0, level=0, health=1):
        super().__init__(list(map(int, a)), list(map(int, b)))
        self.color = color
        self.width = int(width * health)
        self.health = health
        if self.width < 1:
            self.width = 1
        self.level = level

    def draw(self, win):
        pygame.draw.line(win, self.color, self.a, self.b, self.width)

    def set_color(self, color):
        self.color = color


# ------------------ Fractal Presets ------------------

# creates and return a recursive mountain
def create_mountain(center, y, width=100):
    half_width = width//2
    height = random.randrange(50, 150)/100 * half_width
    variation = random.randrange(5, 20), random.randrange(20, 40)
    return Mountain(vector.Vec2(center - half_width, y), vector.Vec2(center + half_width, y), variation, 0.8, height,
                    5, c.grey(random.randrange(50, 200)))


# creates and return a recursive tree
def create_tree(x, y, final_y):
    ratio = (y-200) / (final_y-200)
    width = 10 * ratio
    start_len = 40 * ratio
    trunk_len = random.randrange(40, 70) * ratio
    t = Tree(vector.Vec2(x, y), 270, start_len, 5, len_dec=(70, 80), angle_change=(10, 40), width=width,
             width_dec=(80, 90), two=True, lColor=random.choice(["r", "g", "rg"]), trunk_size=trunk_len)
    t.tint_depth(1 - (y-350) / (final_y-350))
    return t


# creates and returns a recursive bush
def create_bush(x, y, final_y):
    ratio = (y - 400) / (final_y - 400)
    width = 10 * ratio
    start_len = 20 * ratio
    b = Tree(vector.Vec2(x, y), 270, start_len, 2, len_dec=(70, 80), angle_change=(40, 80), width=width, width_dec=90,
             sColor=c.DARKER_GREEN, eColor=c.DARK_GREEN, lColor="g", lCRange=(50, 100))
    return b


# creates and returns a flower
def create_flower(x, y, final_y):
    ratio = (y - 400) / (final_y - 400)
    stem_len = 40 * ratio
    radius = int(15 * ratio)
    f = Flower(vector.Vec2(x, y), stem_len, radius, pColor=c.random_any_color(100), cColor=c.random_any_color(100),
               stem_width=3, tilt_angle=(-15, 15), tilt_count=5)
    return f


# ------------------ Button Click Functions ------------------

# function to create the forest and mountain range scene to be assigned to a button
def create_scene_on_click(b):
    global current_frame
    loading_screen()
    scene_buttons.get_button(1).on_release = create_scene_on_click
    current_frame = frame.Frame([create_still_surface(create_scene()), scene_buttons], [scene_buttons.button_list])


# function to create the tree scene to be assigned to a button
def create_fractal_screen_on_click(b):
    global current_frame
    loading_screen()
    scene_buttons.get_button(1).on_release = create_fractal_screen_on_click
    current_frame = frame.Frame([create_still_surface(create_fractal_screen()), scene_buttons],
                                [scene_buttons.button_list])


# function to reset all of the settings for the scene to defaults
def reset_scene_settings(b=None):
    settings_list = [450, 500, 1, 700, 800, 3, 3, 2]
    for i, b in enumerate(scene_settings.button_list):
        if i < 8:
            b.set_value(settings_list[i])
            b.action(b)


# functions run when clicking first settings buttons
# Switches visible menu to settings menu
def settings1_on_click(b):
    mainMenu.set_active(False)
    mainMenu.set_visible(False)
    scene_settings.set_active(True)
    scene_settings.set_visible(True)


# return to main menu. Optional b parameter so the function can be assigned to a button
def return_to_main_menu(b=None):
    global current_frame
    current_frame = menu_frame
    scene_settings.set_active(False)
    scene_settings.set_visible(False)
    mainMenu.set_visible(True)
    mainMenu.set_active(True)


# ------------------ Surface Rendering Functions ------------------

# create the forest and mountain range scene
def create_scene():
    # mountains
    mList = []
    for d in range(settings.mountain_start, settings.mountain_end, settings.mountain_frequency):
        mList.append(create_mountain(random.randrange(WIN_WIDTH), d, random.randrange(100, 800)))

    # trees, bushes, flowers
    tList = []
    for t in range(settings.foreground_start, settings.foreground_end):  # t is the y coordinate/depth

        if t > settings.secondary_foreground_start:
            if random.randrange(settings.bush_chance) == 0:  # bushes
                tList.append(create_bush(random.randrange(WIN_WIDTH), t, WIN_HEIGHT))
            if random.randrange(settings.flower_chance) == 0:  # flowers
                tList.append(create_flower(random.randrange(WIN_WIDTH), t, WIN_HEIGHT))

        if random.randrange(settings.tree_chance) == 0:  # trees
            tList.append(create_tree(random.randrange(WIN_WIDTH), t, WIN_HEIGHT))

    bg = Surface_Drawable((WIN_WIDTH, WIN_HEIGHT))
    bg.fill(c.SKY)
    pygame.draw.rect(bg, c.DARK_GREEN, (0, settings.mountain_start, WIN_WIDTH, WIN_HEIGHT - settings.mountain_start))

    return frame.Frame([bg] + mList + tList)


# create the tree scene associated
def create_fractal_screen():
    tree = create_tree(550, 600, 600)
    tree2 = create_bush(800, 600, 600)
    mountain = create_mountain(250, 600, random.randrange(200, 500))
    return frame.Frame([mountain, tree, tree2])  # frame for showing a few trees


# returns all the drawables of a frame drawn on a single surface
def create_still_surface(f):
    scene = Surface_Drawable((WIN_WIDTH, WIN_HEIGHT))
    scene.blit(f.get_screen(WIN_WIDTH, WIN_HEIGHT), (0, 0))
    return scene


# return a frame with a copy of a passed frame's screen. All drawables are combined into one surface.
# Makes the surface (such as tree fractals) unchangable but far more efficient for displaying every frame
def create_still_scene(f):
    scene = create_still_surface(f)
    scene_frame = frame.Frame([scene], [f.button_list])
    return scene_frame


# draws the loading screen
def loading_screen():
    WIN.blit(ls, (0, 0))
    pygame.display.update()


# function to redraw the screen
def redraw():
    current_frame.draw(WIN)
    pygame.display.update()


# ------------------ Other Functions ------------------

# gradients the color towards the color of the sky depending on its depth (strength)
def add_depth_tint(color, strength):
    sky = c.SKY
    r = color[0] - (color[0] - sky[0]) * strength
    g = color[1] - (color[1] - sky[1]) * strength
    b = color[2] - (color[2] - sky[2]) * strength
    return r, g, b


# passed an integer or list/tuple of 2 intergers.
# Will either return an integer or a random value from range of list/tuple
def random_if_range(a):
    if type(a) == tuple or type(a) == list:
        if int(a[0]) < int(a[1]):
            return random.randrange(int(a[0]), int(a[1]))
        return a[0]
    return a


# ------------------ Main Program ------------------

# settings class to store all settings
settings = Settings()

# ------------------ Loading Screen ------------------
ls = Surface_Drawable((WIN_WIDTH, WIN_HEIGHT))
ls.fill(c.WHITE)
l = label.Label("Loading: please wait")
l.set_x((WIN_WIDTH - l.get_width())/2)
l.set_y((WIN_HEIGHT - l.get_height())/2)
l.draw(ls)

# ------------------ Redraw and Menu Buttons for Scenes ------------------
scene_buttons = grid.Menu((10, 10, 120, 110), 2, 1, ["Menu", "Redraw"], 10, visible_lines=False)
for b in scene_buttons.button_list:
    b.color_scheme("black")
scene_buttons.get_button(0).on_release = return_to_main_menu

# ------------------ Main Menu ------------------
# background
bg = Surface_Drawable((WIN_WIDTH, WIN_HEIGHT))
bg.blit(pygame.image.load("fractalbg.jpg"), (0, 0))
# title text
title = label.Label("Fractal Scene Generator", color=c.WHITE)
title.set_y(100)
title.set_size(60)
title.set_x((WIN_WIDTH - title.get_width()) / 2)
# buttons for menu
mainMenu = grid.Menu((WIN_WIDTH / 2 - 300, 250, 600, 250), 2, 2,
                     ["Scene", "  > Settings", "Fractals", "  > Settings"], 20, visible_lines=False)
# menu button attributes
for i, b in enumerate(mainMenu.button_list):
    if i < 4:
        b.set_text_size(40)
        b.color_scheme("black")
        b.set_fColor(None)
        b.b = 10
        if i % 2 == 1:
            b.tAlignx = button.LEFT
            b.reset_text_pos()
        if i == 3:
            b.set_visible(False)
            b.set_active(False)
# button functions
mainMenu.button_list.get(0).on_release = create_scene_on_click
mainMenu.button_list.get(1).on_release = settings1_on_click
mainMenu.button_list.get(2).on_release = create_fractal_screen_on_click

# ------------------ Scene Settings Menu ------------------
scene_settings = grid.Menu((WIN_WIDTH/2 - 300, 250, 600, 400), 5, 2, ["Mountain range start coordinate: @",
                                                                      "Mountain range end coordinate: @",
                                                                      "Mountain frequency: @",
                                                                      "Secondary foreground start: @",
                                                                      "Foreground end coordinate: @",
                                                                      "Tree chance: 1/@",
                                                                      "Bush chance: 1/@",
                                                                      "Flower chance: 1/@",
                                                                      "<-- Back", "Reset"], 20,
                           visible_lines=False, visible=False, active=False)
start_end_values = [(WIN_HEIGHT//2 - 200, WIN_HEIGHT//2 + 50), (WIN_HEIGHT//2 + 51, WIN_HEIGHT//2 + 200),
                    (1, 30), (WIN_HEIGHT - 300, WIN_HEIGHT-10), (WIN_HEIGHT - 100, WIN_HEIGHT), (1, 100), (1, 10),
                    (1, 10)]
functions = [settings.set_mountain_start, settings.set_mountain_end, settings.set_mountain_frequency,
             settings.set_secondary_foreground_start, settings.set_foreground_end, settings.set_tree_chance,
             settings.set_bush_chance, settings.set_flower_chance]
start_values = [settings.mountain_start, settings.mountain_end, settings.mountain_frequency,
                settings.secondary_foreground_start, settings.foreground_end, settings.tree_chance,
                settings.bush_chance, settings.flower_chance]
for i, b in enumerate(scene_settings.button_list):
    if i < 8:
        b.set_fColor(c.BLUE)
        b.tAligny = 0.8
        scene_settings.button_list.set(i, b.convert_to_slider((20, 20), slide_color=c.DARK_BLUE,
                                                              start_value=start_end_values[i][0],
                                                              end_value=start_end_values[i][1],
                                                              slide_value=start_values[i],
                                                              slider_border=20, border=3))
        scene_settings.button_list.get(i).action = functions[i]
        scene_settings.button_list.get(i).set_text_size(12)
    elif i == 8:
        b.on_release = return_to_main_menu
    elif i == 9:
        b.on_release = reset_scene_settings


# ------------------ Frames ------------------
menu_frame = frame.Frame([bg, title, mainMenu, scene_settings], [mainMenu.button_list, scene_settings.button_list])
# current frame starts with the menu (menu is shown first when program is run)
current_frame = menu_frame


# ------------------ Main Loop ------------------

inPlay = True
while inPlay:
    pygame.time.delay(10)
    redraw()

    # used for button click processing
    m_click = False
    m_release = False

    # Events iteration
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                m_click = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                m_release = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return_to_main_menu()

    # process button events on current screen
    current_frame.process_events(m_click, m_release, pygame.mouse.get_pos())


# always quit pygame :)
pygame.quit()
