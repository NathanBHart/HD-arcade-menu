import pygame # TODO document everything
from pygame.locals import *
import math

pygame.init()
pygame.font.init()



DISPLAYSURF = pygame.display.set_mode((0,0), FULLSCREEN)

# Set up fonts
text_h1 = pygame.font.SysFont('Silkscreen', 75, True)
text_h2 = pygame.font.SysFont('Silkscreen', 40)
text_h3 = pygame.font.SysFont('Silkscreen', 30)
text_p = pygame.font.SysFont('Open Sans', 25, True)

# Declare Constants
CARD_HEIGHT = DISPLAYSURF.get_height() / 1.25
CARD_WIDTH = DISPLAYSURF.get_width() / 2
CARD_TOP_MARGIN = (DISPLAYSURF.get_height() - CARD_HEIGHT) / 2
CARD_SIDE_MARGIN = (DISPLAYSURF.get_width() - CARD_WIDTH) / 2

CLOCK = pygame.time.Clock()
NUMBER_OF_PARAMS_GAME_FILE = 9
ORIGINALS = "Resources/originals/original_games.txt"

# Declare variables
background = None
scaled_backgound_image = None

# Set Color Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 100, 100)

def read_file(file):

    temp = open(file, "r")

    f = temp.read().splitlines()

    list_item_count = 0

    i = 0

    for stuff in f:

        if str(f[i]) == "-li":
            list_item_count += 1

        i += 1


    x = [[0 for i in range(NUMBER_OF_PARAMS_GAME_FILE)] for j in range(list_item_count)]

    item = 0
    i = 0

    for stuff in f:

        if str(f[i]) == "-li":

            scan = True
            j = 1
            c_type = 0

            while c_type < NUMBER_OF_PARAMS_GAME_FILE:

                if str(f[i + j])[0] != "#" or str(f[i + j]) != "NONE":

                    x[item][c_type] = f[i + j]

                    c_type += 1

                j += 1

            item += 1

        i += 1

    temp.close()

    return x


def display_text(text, location, level = 1, color = BLACK, character_max = 50):

    text_level = text_p
    new_line = 30

    if level == 1:
        text_level = text_h1
        new_line = 70
    elif level == 2:
        text_level = text_h2
        new_line = 40
    elif level == 3:
        text_level = text_h3
        new_line = 30

    if len(text) < character_max or character_max == 0:
        textsurface = text_level.render(text, False, color)
        DISPLAYSURF.blit(textsurface, location)
    else:
        for i in range(int(math.ceil(len(text)/character_max))):
            textsurface = text_level.render(text[i*character_max:(i+1)*character_max], False, color) # TODO Add feature to break line at end of word
            DISPLAYSURF.blit(textsurface, (location[0], location[1] + new_line * i))

    return int(math.ceil(len(text)/character_max))

def card_display(location, width, height, color = WHITE):

    fill_color = (color[0], color[1], color[2], 150)

    s = pygame.Surface((width, height), pygame.SRCALPHA)  # per-pixel alpha
    s.fill(fill_color)  # notice the alpha value in the color
    DISPLAYSURF.blit(s, location)

def image_display(image, location = (0,0), alpha = 255):
    edit = image
    edit.set_alpha(alpha)
    DISPLAYSURF.blit(edit, location)


def menu_card(type = "Blank", position = 0, id = 0, color = WHITE):

    global background

    side = CARD_WIDTH  # / (abs(position) + 1)
    top = CARD_HEIGHT  # / (abs(position) + 1)
    top_corner = (CARD_SIDE_MARGIN + (side + 60) * (position), CARD_TOP_MARGIN)

    if position >= -2 and position <= 2:

        try:

            if type == "Original_Game":
                file = read_file(ORIGINALS)
            else:
                file = read_file("Resources/card_exception")

            if type == "Original_Game":

                #print(file[id])

                card_display(top_corner, side, top, tuple(map(int, file[id][4].split(', '))))

                bg_img = "Resources/originals/game_images/" + file[id][2]

                next_line = display_text(file[id][0], (top_corner[0] + 80, top_corner[1] + 80), 1, WHITE, int(CARD_WIDTH/70)) # TODO Fix text to screen ratio
                display_text(file[id][1], (top_corner[0] + 80, top_corner[1] + 80 + 80 * next_line), 4, WHITE, int(CARD_WIDTH/18))

            else:

                card_display(top_corner, side, top, (255, 100, 100))

                bg_img = None

                next_line = display_text("Error - Unspecified", (top_corner[0] + 60, top_corner[1] + 60), 2, WHITE, int(CARD_WIDTH / 45))  # TODO Fix text to screen ratio
                display_text("Card type not specified. Please check code to ensure correct type is specified without typo.", (top_corner[0] + 60, top_corner[1] + 130 * next_line), 4, WHITE, int(CARD_WIDTH / 11))


        except:

            card_display(top_corner, side, top, (255, 50, 50))

            bg_img = None

            next_line = display_text("Error", (top_corner[0] + 60, top_corner[1] + 60), 1, (255, 200, 200), int(CARD_WIDTH / 45))
            display_text("Error with displaying card. Check code and source file. Type argument was: " + str(type)
                        + " and an id of: " + str(id) + ". Check file and code.", (top_corner[0] + 60, top_corner[1] + 130 * next_line), 4, (255, 200, 200), int(CARD_WIDTH / 11))

        if round(position * 2) == 0:

            background = bg_img



main_loop = True

i = 0

while main_loop:

    DISPLAYSURF.fill(BLACK)

    if background != None:

        try:

            if scaled_backgound_image == None:

                background_image = pygame.image.load(background)

                ratio = background_image.get_width()/background_image.get_height()
                img_width = int(DISPLAYSURF.get_width())
                img_height = int(float(img_width / ratio))

                scaled_background_image = pygame.transform.scale(background_image, (img_width, img_height))
                scaled_background_image.set_alpha(100)


            DISPLAYSURF.blit(scaled_background_image, (0,0))
            #image_display(scaled_background_image, 1, (0,0), 100)

        except:

            display_text("Error Loading Background Image", (0,0), 3, RED)
            display_text("Check code for typo or check for missing or changed file", (0, 30), 4, RED)

    CLOCK.tick(30)

    for event in pygame.event.get():
        if event.type == QUIT:
            main_loop = False

    menu_card("Original_Game", 0 + i, 0)
    menu_card("Original_Game", 2 + i, 0)
    menu_card("Original_Game", 1 + i, 1)

    i -= 0.01

    pygame.display.update()