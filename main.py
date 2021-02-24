import pygame # TODO document everything
from pygame.locals import *
import math

pygame.init()
pygame.font.init()

# Display Constants
DISPLAYSURF = pygame.display.set_mode((0,0), FULLSCREEN)
DISPLAY_WIDTH = DISPLAYSURF.get_width()
DISPLAY_HEIGHT = DISPLAYSURF.get_height()
IDEAL_PIXEL_COUNT = (1280 * 720) ** (1/2)
IDEAL_PIXEL_RATIO = (DISPLAY_WIDTH * DISPLAY_HEIGHT) ** (1/2) / IDEAL_PIXEL_COUNT
DEFAULT_PADDING = 60 * IDEAL_PIXEL_RATIO

# Set up fonts
text_h1 = pygame.font.SysFont('Silkscreen', int(60 * IDEAL_PIXEL_RATIO), True)
text_h2 = pygame.font.SysFont('Silkscreen', int(40 * IDEAL_PIXEL_RATIO))
text_h3 = pygame.font.SysFont('Silkscreen', int(30 * IDEAL_PIXEL_RATIO))
text_p = pygame.font.SysFont('Open Sans', int(25 * IDEAL_PIXEL_RATIO), True)

# Card Constants
CARD_HEIGHT = DISPLAY_HEIGHT / 1.25
CARD_WIDTH = DISPLAY_WIDTH / 2
CARD_TOP_MARGIN = (DISPLAY_HEIGHT - CARD_HEIGHT) / 2
CARD_SIDE_MARGIN = (DISPLAY_WIDTH - CARD_WIDTH) / 2

CLOCK = pygame.time.Clock()
NUMBER_OF_PARAMS_GAME_FILE = 9
ORIGINALS = "Resources/originals/original_games.txt"

# Declare variables
background_link = None
previous_background_link = None
scaled_background_image = None

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

def display_text(text, location, level = 1, color = BLACK, character_max = 100):

    text_level = text_p

    if level == 1:
        text_level = text_h1
    elif level == 2:
        text_level = text_h2
    elif level == 3:
        text_level = text_h3

    new_line = text_level.size("Tg")[1]

    if len(text) < character_max or character_max == 0:
        textsurface = text_level.render(text, False, color)
        DISPLAYSURF.blit(textsurface, location)
    else:
        for i in range(int(math.ceil(len(text)/character_max))):
            textsurface = text_level.render(text[i*character_max:(i+1)*character_max], False, color) # TODO Add feature to break line at end of word
            DISPLAYSURF.blit(textsurface, (location[0], location[1] + new_line * i))

    return int(math.ceil(len(text)/character_max))

# Used and updated from PyGame documentation
# draw some text into an area of a surface
# automatically wraps words
# returns bottom of text as a pixel value
def display_text_box(text, rect, color = BLACK, font = text_h1, aa=False, bkg=None, restrict = False, surface = DISPLAYSURF):
    rect = Rect(rect)
    y = rect.top
    line_spacing = -2

    # get the height of the font
    font_height = font.size("Tg")[1]

    while text:

        i = 1

        # determine if the row of text will be outside our area
        # Restrict allows this option to be disabled
        if y + font_height > rect.bottom and restrict:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):

            for j in range(i):
                if text[j] == " ":
                    i = j + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += font_height + line_spacing

        # remove the text we just blitted
        text = text[i:]

    return y

def card_display(location, width, height, color = WHITE):

    fill_color = (color[0], color[1], color[2], 150)

    s = pygame.Surface((width, height), pygame.SRCALPHA)  # per-pixel alpha
    s.fill(fill_color)  # notice the alpha value in the color
    DISPLAYSURF.blit(s, location)

def image_display(image, location = (0,0), alpha = 255):
    edit = image
    edit.set_alpha(alpha)
    DISPLAYSURF.blit(edit, location)

def background_update(image = True):

    global background_link, previous_background_link, scaled_background_image

    if image:

        if background_link != None:

            if previous_background_link != background_link:

                try:

                    temp = pygame.image.load(background_link)

                    ratio = temp.get_width() / temp.get_height()
                    img_width = int(DISPLAY_WIDTH)
                    img_height = int(float(img_width / ratio))

                    temp = pygame.transform.scale(temp, (img_width, img_height))
                    temp.set_alpha(100)

                    scaled_background_image = temp

                    DISPLAYSURF.blit(temp, (0, 0))

                    previous_background_link = background_link

                except:

                    display_text("Error Loading Background Image", (0, 0), 3, RED)
                    display_text("Check code for typo or check for missing or changed file", (0, 30), 4, RED)

            else:

                DISPLAYSURF.blit(scaled_background_image, (0,0))

def menu_card(type = "Blank", position = 0, id = 0, color = WHITE):

    global background_link

    depth_scale = 10

    side = CARD_WIDTH / ((abs(position)/depth_scale) + 1)  # / (abs(position) + 1)
    top = CARD_HEIGHT / ((abs(position)/depth_scale) + 1)  # / (abs(position) + 1)
    top_corner = (CARD_SIDE_MARGIN + (CARD_WIDTH + DEFAULT_PADDING) * (position), (DISPLAY_HEIGHT-top)/2)

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

                next_line = display_text_box(file[id][0], (top_corner[0] + DEFAULT_PADDING, top_corner[1] + DEFAULT_PADDING, CARD_WIDTH - DEFAULT_PADDING*2, CARD_HEIGHT - DEFAULT_PADDING*2), WHITE, text_h1)
                display_text_box(file[id][1], (top_corner[0] + DEFAULT_PADDING, next_line + DEFAULT_PADDING/2, CARD_WIDTH - DEFAULT_PADDING*2, CARD_HEIGHT - DEFAULT_PADDING*2), WHITE, text_p, aa = True)

            else:

                card_display(top_corner, side, top, (255, 100, 100))

                bg_img = None

                next_line = display_text("Error - Unspecified", (top_corner[0] + DEFAULT_PADDING, top_corner[1] + DEFAULT_PADDING), 2, WHITE, int(CARD_WIDTH / 45))
                display_text("Card type not specified. Please check code to ensure correct type is specified without typo.", (top_corner[0] + 60, top_corner[1] + 130 * next_line), 4, WHITE, int(CARD_WIDTH / 11))


        except:

            card_display(top_corner, side, top, (255, 50, 50))

            bg_img = None

            next_line = display_text("Error", (top_corner[0] + 60, top_corner[1] + 60), 1, (255, 200, 200), int(CARD_WIDTH / 45))
            display_text("Error with displaying card. Check code and source file. Type argument was: " + str(type)
                        + " and an id of: " + str(id) + ". Check file and code.", (top_corner[0] + 60, top_corner[1] + 130 * next_line), 4, (255, 200, 200), int(CARD_WIDTH / 11))

        if round(position * 2) == 0:

            background_link = bg_img



main_loop = True

i = 0

while main_loop:

    DISPLAYSURF.fill(BLACK)

    background_update()

    CLOCK.tick(30)

    for event in pygame.event.get():
        if event.type == QUIT:
            main_loop = False

    menu_card("Original_Game", 0, 0)
    menu_card("Original_Game", 2, 0)
    menu_card("Original_Game", 1, 1)

    pygame.display.update()