# locals.py
# This file contains important data values and initializes pygame in the main
# ---------------------------------------------------------------------------------------------------------------------

import pygame
from pygame.locals import *

# Initialize fonts
pygame.font.init()

# Initialize music mixer
pygame.mixer.init()

# Set up display constants based on screen size...
DISPLAYSURF = pygame.display.set_mode((0, 0), FULLSCREEN)
DISPLAY_WIDTH = DISPLAYSURF.get_width()
DISPLAY_HEIGHT = DISPLAYSURF.get_height()
IDEAL_PIXEL_COUNT = (1280 * 720) ** (1/2)
IDEAL_PIXEL_RATIO = (DISPLAY_WIDTH * DISPLAY_HEIGHT) ** (1/2) / IDEAL_PIXEL_COUNT
DEFAULT_PADDING = 60 * IDEAL_PIXEL_RATIO

# Set up card constants based on the display constants
CARD_HEIGHT = DISPLAY_HEIGHT / 1.25
CARD_WIDTH = DISPLAY_WIDTH / 2
CARD_TOP_MARGIN = (DISPLAY_HEIGHT - CARD_HEIGHT) / 2
CARD_SIDE_MARGIN = (DISPLAY_WIDTH - CARD_WIDTH) / 2
DEPTH_SCALE = 5


# Set up fonts (These are imported from "resources/menu_ui/fonts")
text_huge = pygame.font.Font('resources/menu_ui/fonts/silkscreen/slkscrb.ttf', int(70 * IDEAL_PIXEL_RATIO))
text_h1 = pygame.font.Font('resources/menu_ui/fonts/silkscreen/slkscrb.ttf', int(60 * IDEAL_PIXEL_RATIO))
text_h2 = pygame.font.Font('resources/menu_ui/fonts/silkscreen/slkscr.ttf', int(30 * IDEAL_PIXEL_RATIO))
text_h3 = pygame.font.Font('resources/menu_ui/fonts/silkscreen/slkscr.ttf', int(20 * IDEAL_PIXEL_RATIO))
text_p = pygame.font.Font('resources/menu_ui/fonts/open_sans/OpenSans-Bold.ttf', int(25 * IDEAL_PIXEL_RATIO))

# Set up timing constants
CLOCK = pygame.time.Clock()
FPS = 30

# Set Color Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 100, 100)

# Animation constants
SLIDE_LEFT = -1
SLIDE_RIGHT = 1
ANIMATION_LERP = 2
ANIMATION_TIME = 0.4