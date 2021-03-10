import pygame
from pygame.locals import *
#import math
import controller
import file_reader
from file_reader import *

pygame.init()
pygame.font.init()

# Display Constants
DISPLAYSURF = pygame.display.set_mode((0,0), FULLSCREEN)
DISPLAY_WIDTH = DISPLAYSURF.get_width()
DISPLAY_HEIGHT = DISPLAYSURF.get_height()
IDEAL_PIXEL_COUNT = (1280 * 720) ** (1/2)
IDEAL_PIXEL_RATIO = 1#(DISPLAY_WIDTH * DISPLAY_HEIGHT) ** (1/2) / IDEAL_PIXEL_COUNT
DEFAULT_PADDING = 60 * IDEAL_PIXEL_RATIO

# Set up fonts
text_huge = pygame.font.SysFont('Silkscreen', int(110 * IDEAL_PIXEL_RATIO), True)
text_h1 = pygame.font.SysFont('Silkscreen', 60, True)
text_h2 = pygame.font.SysFont('Silkscreen', int(30 * IDEAL_PIXEL_RATIO))
text_h3 = pygame.font.SysFont('Silkscreen', int(20 * IDEAL_PIXEL_RATIO))
text_p = pygame.font.SysFont('Open Sans', int(25 * IDEAL_PIXEL_RATIO), True)

# Card Constants
CARD_HEIGHT = DISPLAY_HEIGHT / 1.25
CARD_WIDTH = DISPLAY_WIDTH / 2
CARD_TOP_MARGIN = (DISPLAY_HEIGHT - CARD_HEIGHT) / 2
CARD_SIDE_MARGIN = (DISPLAY_WIDTH - CARD_WIDTH) / 2
DEPTH_SCALE = 5

CLOCK = pygame.time.Clock()
FPS = 30
# Declare variables
background_link = None
previous_background_link = None
scaled_background_image = None

# Set Color Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 100, 100)

SLIDE_LEFT = -1
SLIDE_RIGHT = 1
ANIMATION_LERP = 2
ANIMATION_TIME = 0.3

class MenuGroup:

    def __init__(self, *args):

        self.items = [*args]

    def add_to_group(self, item):

        self.items.append(item)

    def display_items(self):

        for each in self.items:

            each.display_card()

    def animate_cards(self, direction: int = SLIDE_LEFT):

        destinations = {}

        for each in self.items:

            destinations[each] = each.position + direction

        reps = round(FPS * ANIMATION_TIME)
        for i in range(reps):

            DISPLAYSURF.fill(BLACK)
            CLOCK.tick(FPS)

            for each in self.items:

                each.position += (destinations[each] - each.position) / ANIMATION_LERP
                each.prepare_display()

            # process inputs(events)
            for event in pygame.event.get():
                # close the window
                if event.type == pygame.QUIT:
                    main_loop = False
                    break

            menu.display_items()

            pygame.display.update()

        for each in self.items:

            each.position = destinations[each]
            each.prepare_display()

    def load_menu_from_file(self, file = ORIGINALS):
        read_file = file_reader.read_file(file)




class Card:

    def __init__(self, **kwargs):
        self.position = kwargs["position"]
        self.color = kwargs["color"]
        self.size = (round(CARD_WIDTH / (abs(self.position / DEPTH_SCALE) + 1)), round(CARD_HEIGHT/ (abs(self.position / DEPTH_SCALE) + 1)))
        self.location = ((DISPLAY_WIDTH - self.size[0]) / 2 + (CARD_WIDTH + DEFAULT_PADDING) * self.position,
                         (DISPLAY_HEIGHT - self.size[1]) / 2)
        #self.rect = (self.location[0], self.location[1], self.size[0], self.size[1])

        self.text_rect = (DEFAULT_PADDING, DEFAULT_PADDING*1.5, CARD_WIDTH - DEFAULT_PADDING*2, CARD_HEIGHT - DEFAULT_PADDING*2)

        self.original_display = pygame.image.load("resources/menu_ui/menu_card.png")
        self.original_display.fill((self.color[0], self.color[1], self.color[2], 100), special_flags=pygame.BLEND_MULT)
        self.original_display = pygame.transform.scale(self.original_display, (round(CARD_WIDTH),round(CARD_HEIGHT)))

        self.display = pygame.transform.scale(self.original_display, self.size)

    def display_card(self):

        DISPLAYSURF.blit(self.display, self.location)

    def prepare_display(self):

        self.size = (round(CARD_WIDTH / (abs(self.position / DEPTH_SCALE) + 1)),
                     round(CARD_HEIGHT / (abs(self.position / DEPTH_SCALE) + 1)))
        self.location = ((DISPLAY_WIDTH - self.size[0]) / 2 + (CARD_WIDTH + DEFAULT_PADDING) * self.position,
                         (DISPLAY_HEIGHT - self.size[1]) / 2)
        #self.rect = (self.size[0], self.size[1], self.location[0], self.location[1])
        #self.text_rect = (DEFAULT_PADDING, DEFAULT_PADDING, self.size[0] - DEFAULT_PADDING * 2, self.size[1] - DEFAULT_PADDING * 2)
        self.display = pygame.transform.scale(self.original_display, self.size)

class PrimaryMenuCard(Card):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = kwargs["title"]
        display_text_box(self.title, self.text_rect, WHITE, text_huge, centered=True, surface=self.original_display)
        self.prepare_display()

class GameMenuCard(Card):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = kwargs["title"]
        next_line = display_text_box(self.title, self.text_rect, WHITE, text_huge, centered= True, surface=self.original_display)
        x = self.text_rect
        self.text_rect = (x[0] + 10, x[1] + next_line + DEFAULT_PADDING, x[2] - 20, x[3] - next_line)

        self.description = kwargs["description"]
        display_text_box(self.description, self.text_rect, WHITE, text_p, centered = True, aa=True, surface=self.original_display)

'''        self.background_image = kwargs["background image"]
        self.music = kwargs["music"]
        self.color = kwargs["color"]
        self.number_of_players = kwargs["number of players"]
        self.completion_time = kwargs["completion time"]
        self.game_file = kwargs["game file"]
        self.hi_score_file = kwargs["hi score file"]'''

# Used and updated from PyGame documentation
# draw some text into an area of a surface
# automatically wraps words
# returns bottom of text as a pixel value
def display_text_box(text, rect, color = BLACK, font = text_h1, aa=False, centered = False, restrict = False, surface = DISPLAYSURF):
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
        image = font.render(text[:i], aa, color)

        if centered:
            surface.blit(image, (rect.left + (rect.width - image.get_width())/2, y))
        else:
            surface.blit(image, (rect.left, y))
        y += font_height + line_spacing

        # remove the text we just blitted
        text = text[i:]

    y -= font_height + line_spacing

    return y

menu_item = PrimaryMenuCard(position=0, color= RED, title="HD Originals")
menu_item2 = PrimaryMenuCard(position=1, color= (200, 235, 255), title="Minigames")
menu_item3 = PrimaryMenuCard(position=-1, color= (200, 255, 235), title="Classics")
menu_item4 = GameMenuCard(position=2, color=WHITE, title = "HD Game Lab", description="Welcome to the HD Game Lab, the game development community for HDCH. This discord server is designed to be a resource to you, so feel free to participate and contribute as much as you want.")

menu = MenuGroup(menu_item, menu_item2, menu_item3, menu_item4)

main_loop = True

console_control = controller.Controller(0)

while main_loop:

    DISPLAYSURF.fill(BLACK)
    CLOCK.tick(FPS)

    # process inputs(events)
    for event in pygame.event.get():
        # close the window
        if event.type == pygame.QUIT:
            main_loop = False

    menu.display_items()

    if console_control.get_x_axis() == 1 or pygame.key.get_pressed()[K_RIGHT]:
        menu.animate_cards(SLIDE_LEFT)

    if console_control.get_x_axis() == -1 or pygame.key.get_pressed()[K_LEFT]:
        menu.animate_cards(SLIDE_RIGHT)

    pygame.display.update()