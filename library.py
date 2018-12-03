"""STORAGE."""
import pygame
from pygame.locals import *

# assign variables or names to used keys
PAUSE = K_ESCAPE
MOVE = {"left": K_a, "right": K_d, "forwards": K_w, "backwards": K_s}

# directions
LEFT = 0
RIGHT = 1
FORWARDS = 2
BACKWARDS = 3

# boolean values for key pressed states
KEY_PRESSED = {"left": False, "right": False, "forwards": False,
               "backwards": False, "mouse": False, "space": False}

HAD_FIRST_RUN = False
RESET = False


# set Colors (r, g, b, a)
BLUE = (0, 0, 255, 255)
GREEN = (0, 255, 0, 255)
GREY = (100, 100, 100, 255)
DARK_GREY = (75, 75, 75, 255)
LIGHT_GREY = (200, 200, 200, 255)
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 255)
RED = (255, 0, 0, 255)

MUD = (139, 69, 19)
MOSS = (61, 142, 31)

# set images
scaleNum = 90
buttonSize = (600, 100)

#   UI Buttons
buttonOneHover = pygame.transform.scale(
    pygame.image.load("UI/Button_000_hover.png"), buttonSize)
buttonTwoHover = pygame.transform.scale(
    pygame.image.load("UI/Button_001_hover.png"), buttonSize)
buttonOneClick = pygame.transform.scale(
    pygame.image.load("UI/Button_000_pressed.png"), buttonSize)
buttonTwoClick = pygame.transform.scale(
    pygame.image.load("UI/Button_001_pressed.png"), buttonSize)
buttonOne = pygame.transform.scale(
    pygame.image.load("UI/Button_000_normal.png"), buttonSize)
buttonTwo = pygame.transform.scale(
    pygame.image.load("UI/Button_001_normal.png"), buttonSize)

# Background
background = pygame.image.load("UI/WellEscape_Background.png")

loading_bar_font_face = None    # gets set in main.

scaleNum = 90
# load the player image
playerImg = pygame.transform.scale(
    pygame.image.load("Characters/Player.png"),
    (int(scaleNum * 0.75), int(scaleNum * 0.75)))

debug_mode = False

SOUND_HAS_INITIALIZED = None

def clamp(min, max, value):
    """
    Clamp value between min and max.

    :return:    Clamped value
    """
    if value < min:
        value = min
    elif value > max:
        value = max

    return value


def text_objects(text, font):
    """Create a text object."""
    text_surface = font.render(text, True, BLACK)
    return text_surface, text_surface.get_rect()


def lerp(start_value, end_value, percentage):
    """
    Lerp a value from start to end.

    :param start_value:         start value ->int/float
    :param end_value:           end value ->int/float
    :param percentage:          time percentage (clamped 0-1)
    :return:                    lerped value -> float
    """
    percentage = clamp(0, 1, percentage)
    return start_value + ((end_value - start_value) * percentage)


def lerp_vector2(start_position, end_position, percentage):
    """
    Lerp a value from start to end.

    :param start_position:          start value ->(x, y)
    :param end_position:            end value ->(x, y)
    :param percentage:              time percentage  (clamped 0-1)
    :return:                        lerped value -> (x, y)
    """
    pos_x = lerp(start_position[0], end_position[0], percentage)
    pos_y = lerp(start_position[1], end_position[1], percentage)

    return pos_x, pos_y


def abs(value):
    """Force number to positive."""
    if value < 0:
        return -value
    else:
        return value


def loading_bar(surface, rect, percent):
    """
    Display a loading bar on surface and update display.

    :param surface: surface to display loading bar on.
    :param rect:    the position and size of the loading bar
    (x, y, width, height).
    :param percent: the loading percentage.
    :return:        None.
    """
    text_surface = loading_bar_font_face.render("Loading", True, BLACK)
    pygame.draw.rect(surface, GREY, rect)
    pygame.draw.rect(
        surface, WHITE,
        (rect[0] + 5, rect[1] + 5, (rect[2] - 10) * percent, rect[3] - 8)
    )
    surface.blit(text_surface, (50, 10))
    pygame.display.flip()
