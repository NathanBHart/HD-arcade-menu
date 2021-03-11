import pygame
from pygame.locals import *
import math
import controller
import file_reader
from file_reader import *

#TODO: refactor, document, and organize code.
#TODO: Display only the relavant cards on the screen at a time
#TODO: Fix positioning system, and animation system
#TODO: Fix background system

pygame.init()
pygame.font.init()

# Display Constants
DISPLAYSURF = pygame.display.set_mode((0, 0), FULLSCREEN)
DISPLAY_WIDTH = DISPLAYSURF.get_width()
DISPLAY_HEIGHT = DISPLAYSURF.get_height()
IDEAL_PIXEL_COUNT = (1280 * 720) ** (1/2)
IDEAL_PIXEL_RATIO = (DISPLAY_WIDTH * DISPLAY_HEIGHT) ** (1/2) / IDEAL_PIXEL_COUNT
DEFAULT_PADDING = 60 * IDEAL_PIXEL_RATIO

# Set up fonts
text_huge = pygame.font.SysFont('Silkscreen', int(70 * IDEAL_PIXEL_RATIO), True)
text_h1 = pygame.font.SysFont('Silkscreen', int(60 * IDEAL_PIXEL_RATIO), True)
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

# Set Color Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 100, 100)

SLIDE_LEFT = -1
SLIDE_RIGHT = 1
ANIMATION_LERP = 2
ANIMATION_TIME = 0.4

class MenuGroup:

    def __init__(self, *args):

        self.background = get_default_background()
        self.items = []

        for each in args:

            self.add_to_group(each)

    def add_to_group(self, item):

        temp = item

        temp.position = len(self.items)

        temp.prepare_display()

        self.items.append(item)

        if len(self.items) == 1:

            self.background = self.items[0].background

    def display_items(self):

        DISPLAYSURF.blit(self.background, (0, 0))

        if self.items != []:
            j = len(self.items) - 1

            for i in range(-1, 2):
                self.items[j].display_card(i)

                j += 1

                if j == len(self.items):
                    j = 0

    def animate_cards(self, direction: int):

        global main_loop
        new_background = get_default_background()
        new_music = None

        if len(self.items) > 1:

            new_background = self.items[direction].background
            if hasattr(self.items[direction], 'music'):
                new_music = self.items[direction].music

            if direction < 0:
                new_background = self.items[1].background
                if hasattr(self.items[1], 'music'):
                    new_music = self.items[1].music

            if direction > 0:
                new_background = self.items[len(self.items)-1].background
                if hasattr(self.items[len(self.items)-1], 'music'):
                    new_music = self.items[len(self.items)-1].music

        elif self.items != []:

            new_background = self.items[0].background
            if hasattr(self.items[0], 'music'):
                new_music = self.items[0].music

        shift = 0
        reps = round(FPS * ANIMATION_TIME)

        for i in range(reps):

            DISPLAYSURF.fill(WHITE)
            CLOCK.tick(FPS)

            # process inputs(events)
            for event in pygame.event.get():
                # close the window
                if event.type == pygame.QUIT:
                    main_loop = False
                    break

            if not main_loop:
                break

            if i > reps/3:

                self.background = new_background
                if new_music != None:
                    self.play_music(new_music)

            DISPLAYSURF.blit(self.background, (0, 0))

            shift += (direction - shift) / ANIMATION_LERP

            if self.items != []:

                j = len(self.items) - 1
                self.items[j].display_card(-1 + shift)
                j -= 1
                if j < 0: j = 0
                self.items[j].display_card(-2 + shift)

                j = 0
                for i in range(3):
                    self.items[j].display_card(i + shift)

                    j += 1

                    if j == len(self.items):
                        j = 0

            pygame.display.update()

        self.background = new_background

        if direction < 0:
            temp = self.items.pop(0)
            self.items.append(temp)

        if direction > 0:
            temp = self.items.pop(len(self.items) - 1)
            self.items.insert(0, temp)

        self.display_items()
        pygame.display.update()

    def play_music(self, music_link: str = ""):

        try:
            pygame.mixer.music.load(music_link)
            pygame.mixer.music.play()
        except FileNotFoundError:
            print("Could not find correct music  file")
        except TypeError:
            print("Cannot play music (link was not passed in)")

    def load_menu_from_file(self, file = ORIGINALS):
        read_file = file_reader.read_file(file)

        self.items = []

        for each in read_file:

            ref = each

            add_item = GameMenuCard(title=ref["title"], description=ref["description"], background_image=ref["background_image"],
                                    music=ref["music"], color=tuple(map(int, ref["color"].split(', '))), game_file=ref["game_file"], hi_score_file=ref["hi_score_file"],
                                    number_of_players=int(ref["number_of_players"]), completion_time=int(ref["completion_time"]))

            add_item.prepare_display()

            self.add_to_group(add_item)

        if self.items != []:
            self.play_music(self.items[0].music)

    def load_primary_menu(self):

        self.items = []

        self.add_to_group(PrimaryMenuCard(color=(255, 160, 100), type = 0))
        self.add_to_group(PrimaryMenuCard(color=(100, 160, 255), type=1))
        self.add_to_group(PrimaryMenuCard(color=(100, 255, 160), type=2))


class Card:

    def __init__(self, position: int = 0, **kwargs):
        self.position = position
        self.color = kwargs["color"]
        self.size = (round(CARD_WIDTH / (abs(self.position / DEPTH_SCALE) + 1)), round(CARD_HEIGHT/ (abs(self.position / DEPTH_SCALE) + 1)))
        self.location = ((DISPLAY_WIDTH - self.size[0]) / 2 + (CARD_WIDTH + DEFAULT_PADDING) * self.position,
                         (DISPLAY_HEIGHT - self.size[1]) / 2)
        #self.rect = (self.location[0], self.location[1], self.size[0], self.size[1])

        self.text_rect = (DEFAULT_PADDING, DEFAULT_PADDING, CARD_WIDTH - DEFAULT_PADDING*2, CARD_HEIGHT - DEFAULT_PADDING*2)

        self.original_display = pygame.image.load("resources/menu_ui/menu_card.png")
        self.original_display.fill((self.color[0], self.color[1], self.color[2], 100), special_flags=pygame.BLEND_MULT)
        self.original_display = pygame.transform.scale(self.original_display, (round(CARD_WIDTH),round(CARD_HEIGHT)))

        self.display = pygame.transform.scale(self.original_display, self.size)

        self.background = get_default_background()
        self.background.fill((self.color[0], self.color[1], self.color[2], 255), special_flags=pygame.BLEND_MULT)

    def display_card(self, relative_position: int = 0):

        if self.position != relative_position:
            self.position = relative_position
            self.prepare_display()

        DISPLAYSURF.blit(self.display, self.location)

    def prepare_display(self):

        self.size = (round(CARD_WIDTH / (abs(self.position / DEPTH_SCALE) + 1)),
                     round(CARD_HEIGHT / (abs(self.position / DEPTH_SCALE) + 1)))
        self.location = ((DISPLAY_WIDTH - self.size[0]) / 2 + (CARD_WIDTH + DEFAULT_PADDING) * self.position,
                         (DISPLAY_HEIGHT - self.size[1]) / 2)
        #self.rect = (self.size[0], self.size[1], self.location[0], self.location[1])
        self.display = pygame.transform.scale(self.original_display, self.size)

    def change_background(self, link: str = "resources/menu_ui/background_default.png"):

        try:

            self.background = pygame.image.load(link)

            ratio = self.background.get_width() / self.background.get_height()
            img_width = int(DISPLAY_WIDTH)
            img_height = int(float(img_width / ratio))

            self.background = pygame.transform.scale(self.background, (img_width, img_height))

        except FileNotFoundError:

            print("Background.change: Error, file (" + link + ") not found.")

        except TypeError:

            print("Background.change: Error, invalid type entered!")


class PrimaryMenuCard(Card):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = kwargs["type"]

        if self.type == 0:

            title_image = pygame.image.load("resources/menu_ui/hd_originals_card.png")
            title_image = pygame.transform.scale(title_image, (round(CARD_WIDTH), round(CARD_WIDTH)))

            location = (30 * IDEAL_PIXEL_RATIO, 20 * IDEAL_PIXEL_RATIO)

            self.original_display.blit(title_image, location)

        elif self.type == 1:

            title_image = pygame.image.load("resources/menu_ui/classic_games_card.png")
            title_image = pygame.transform.scale(title_image, (round(CARD_WIDTH), round(CARD_WIDTH)))

            location = (30 * IDEAL_PIXEL_RATIO, 20 * IDEAL_PIXEL_RATIO)

            self.original_display.blit(title_image, location)

        elif self.type == 2:

            title_image = pygame.image.load("resources/menu_ui/minigames_card.png")
            title_image = pygame.transform.scale(title_image, (round(CARD_WIDTH), round(CARD_WIDTH)))

            location = (30 * IDEAL_PIXEL_RATIO, 20 * IDEAL_PIXEL_RATIO)

            self.original_display.blit(title_image, location)


        self.prepare_display()


class GameMenuCard(Card):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = kwargs["title"]
        next_line = display_text_box(self.title, self.text_rect, WHITE, text_huge, centered= True, surface=self.original_display)
        x = self.text_rect
        self.text_rect = (x[0] + 10, x[1] + next_line + DEFAULT_PADDING/2, x[2] - 20, x[3] - next_line)

        self.description = kwargs["description"]
        display_text_box(self.description, self.text_rect, WHITE, text_p, centered = True, aa=True, surface=self.original_display)

        self.background_image = kwargs["background_image"]
        self.change_background(self.background_image)
        self.music = kwargs["music"]

        self.number_of_players = kwargs["number_of_players"]
        self.completion_time = kwargs["completion_time"]

        self.game_file = kwargs["game_file"]
        self.hi_score_file = kwargs["hi_score_file"]


def display_text_box(text, rect, color = BLACK, font = text_h1, aa=False, centered = False, restrict = False, surface = DISPLAYSURF):
    # Used and updated from PyGame documentation
    # draw some text into an area of a surface
    # automatically wraps words
    # returns bottom of text as a pixel value

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

def get_default_background():

    background = pygame.image.load("resources/menu_ui/background_default.png")

    ratio = background.get_width() / background.get_height()
    img_width = int(DISPLAY_WIDTH)
    img_height = int(float(img_width / ratio))

    background = pygame.transform.scale(background, (img_width, img_height))

    return background

menu = MenuGroup()
menu.load_primary_menu()
#menu.load_menu_from_file(ORIGINALS)

main_loop = True

console_control = controller.Controller(0)

while main_loop:

    DISPLAYSURF.fill(WHITE)
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

    if pygame.key.get_pressed()[K_DOWN]:
        menu.load_menu_from_file(ORIGINALS)

    pygame.display.update()