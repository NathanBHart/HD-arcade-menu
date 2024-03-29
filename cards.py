# --------- IMPORT CUSTOM MODULES: ------------------------------------------------------------------------------------
from file_reader import *  # File Reader Module
from locals import *  # Note that pygame and the controller is imported through the locals module!
from assistant_functions import *

# --------- SYSTEM MODULES:
from subprocess import Popen
import random


# ---------------------------------------------------------------------------------------------------------------------


# --------- CLASSES/OBJECTS: ------------------------------------------------------------------------------------------
# ----- MenuGroup:
# A MenuGroup holds all of the cards, and the functions that creates card behaviors. The cards essentially contain all
# of the information relevant to each menu option (such as the information to display, the background, the color,
# the links to game/hi score files, etc., and some card-specific functions. The MenuGroup holds all of these cards in
# a list, and can cycle through them/enable functionality.
class MenuGroup:

    # When the MenuGroup is initialized, you can specify any number of card objects to be added to the list at first.
    # This functionality is not used in practice, but is still an option, meaning that unique menus composed of specific
    # cards can be created.
    def __init__(self, *args):

        # A MenuGroup has a background, which is always displayed behind the cards. To start, a default background is
        # generated and set to be the background, but this will change when the menu is loaded.
        self.background = get_default_background()

        # Items is important, it is a 1D list that contains all of the card objects that will be in the menu. Cards
        # Are displayed depending on their position in the list, and this list is rearranged to suit that purpose.
        self.items = []

        # For each of the items specified as arguments (when MenuGroup is initialized), add it to the list, but only
        # if it is of Card type. (Can't add bad data to the list!)
        for each in args:

            if isinstance(each, Card):
                self.add_to_group(each)

        # Then present the display to the user.
        # NOTE: This is important, because in order for this menu system to be super lightweight, it only
        # renders and displays when animations are occuring, otherwise the screen doesn't update, but isn't cleared.
        self.load_display()

    # A function (used internally) to add a new card object to the list.
    def add_to_group(self, item):

        # First, check if it is of Card type before proceeding
        if isinstance(item, Card):

            # If so, set up a temporary variable to be the passed in object.
            temp = item
            # Adjust the relative position of the card so that it sits at the end of the MenuGroup
            temp.position = len(self.items)
            # Prepare the new card to be displayed
            temp.prepare_display()

            # Add the prepared object (via the temp variable) to the end of the items list.
            self.items.append(temp)

            # If its the first item in the list, set the background to be the background for that card.
            if len(self.items) == 1:
                self.background = temp.background

    # This function is called to display the current list position. It will render the current list item, as well as
    # the one before and behind it in the list (only three are on the screen at a time anyways, so it is memory
    # efficient to do it this way.)
    def display_items(self):

        # First, the current background is blitted onto the main screen.
        location = (
            DISPLAY_WIDTH / 2 - self.background.get_width() / 2,
            DISPLAY_HEIGHT / 2 - self.background.get_height() / 2
        )
        DISPLAYSURF.blit(self.background, location)

        # Then, if the list is not empty, items will be displayed in the list.
        if self.items != []:

            # We start with the last item in the list, this will be rendered to the left of the current item (position
            # -1). The current item is at position 0, and the item following at position 1.

            # For -1, 0, and 1
            for j in range(-1, 2):
                # Display the item specified by j at the ith position (from -1, to 0, to 1.)
                self.items[j % len(self.items)].display_card(j)
                # Modulo is used to loop the counting back around if the list length is exceeded by the index.

            # TODO: Fix this

            # Color is pulled from currently selected cards
            color = self.items[0].color

            # Contrast is checked and text is either white or black depending on which is more readable.
            if (color[0] * color[1] * color[2]) < (256 ** 3 / 2):
                if color[0] > 230 or color[1] > 190:
                    text_color = BLACK
                else:
                    text_color = WHITE
            else:
                text_color = BLACK

            text = "Press (A) to Select"
            padding = 10 * IDEAL_PIXEL_RATIO

            rect = (
                DISPLAY_WIDTH / 2 - text_p.size(text)[0] / 2,
                DISPLAY_HEIGHT / 2 + CARD_HEIGHT / 2,
                text_p.size(text)[0],
                text_p.size("Tg")[1],
            )

            pygame.draw.rect(
                DISPLAYSURF,
                color,
                (rect[0] - padding, rect[1] - padding, rect[2] + padding * 2, rect[3] + padding * 2)
            )

            display_text_box(text, rect, text_color, text_p, True, centered=True)

            if type(self.items[0]) == GameMenuCard:
                text = "Press (B) to Return to Main Menu"
                padding = 10 * IDEAL_PIXEL_RATIO

                rect = (
                    25 * IDEAL_PIXEL_RATIO,
                    25 * IDEAL_PIXEL_RATIO,
                    text_p.size(text)[0],
                    text_p.size("Tg")[1],
                )

                pygame.draw.rect(
                    DISPLAYSURF,
                    text_color,
                    (rect[0] - padding, rect[1] - padding, rect[2] + padding * 2, rect[3] + padding * 2)
                )

                display_text_box(text, rect, color, text_p, True, centered=True)

    # A function to animate the cards moving in a direction (use the direction constants given!)
    def animate_cards(self, direction_const: int):

        # direction is set to be a normalized integer version of the specified direction.
        # This is in case a value with a magnitude greater than 1 is specified, so the
        # animation still behaves as expected.
        direction = int(direction_const / abs(direction_const))

        # Import the main_loop global variable. This is so that if the X is hit when the animation is running, it still
        # can cause the program to close.
        global main_loop

        # Set up variables for new background and music.
        # A background is necessary, so a default one is loaded, but music isn't.
        new_background = get_default_background()
        new_music = None

        # If there is more than 1 item,
        if len(self.items) > 1:

            # Set the new background and music to the next item (indicated by the item next along the list... opposite
            # of direction).
            new_background = self.items[-direction].background
            # Not all cards have music, so don't try to reference it if it doesn't exist!
            if hasattr(self.items[-direction], 'music'):
                new_music = self.items[-direction].music

        # If only one list item, then reference the one list item's attributes as the new background and music...
        elif self.items != []:

            new_background = self.items[0].background
            if hasattr(self.items[0], 'music'):
                new_music = self.items[0].music

        # Shift is initialized
        shift = 0
        # Reps indicates the amount of repetitions that the animation will need to do, and this is a product of the
        # Animation time and the frames per second (from the constants module).
        reps = round(FPS * ANIMATION_TIME)

        for i in range(reps):

            # Tick
            DISPLAYSURF.fill(WHITE)
            CLOCK.tick(FPS)

            # process inputs(events)
            for event in pygame.event.get():
                # close the window
                if event.type == pygame.QUIT:
                    main_loop = False

            # If exit was hit, main_loop will be false, and so break out of this function and let the main loop close.
            if not main_loop:
                break

            # If a third of the animation is completed,
            if i > reps / 3:

                # Update the background and music.
                self.background = new_background
                if new_music != None:
                    # Use the music playing function to play the music link.
                    self.play_music(new_music)

            # Add the background to the display at a fixed point before displaying the moved cards.
            location = (
                DISPLAY_WIDTH / 2 - self.background.get_width() / 2,
                DISPLAY_HEIGHT / 2 - self.background.get_height() / 2
            )
            DISPLAYSURF.blit(self.background, location)

            # Shift changes each time to lerp towards the direction value. This is used to display each of the cards,
            # But shifted over somewhat.
            shift += (direction - shift) / ANIMATION_LERP

            # If there are items in the list,
            if self.items != []:

                # Using a modified technique from the "display_items" method:
                # We want to render 5 instead of just 3 cards. This is because as we move the three main cards
                # over, more cards are revealed during the animation cycle on either end, depending.
                # Otherwise, the principle is the exact same for the list.
                for i in range(-2, 3):
                    self.items[i % len(self.items)].display_card(i + shift)

            pygame.display.update()

        # If animating to the left, then we want to move the first item to the last. This makes the 2nd item be the
        # new focused item... Essentially, we are moving UP the list.
        if direction < 0 and self.items != []:
            temp = self.items.pop(0)
            self.items.append(temp)

        # If animating to the right, the opposite is done. The last item is put as the new focus item.
        if direction > 0 and self.items != []:
            temp = self.items.pop(-1)
            self.items.insert(0, temp)

        # The display is now loaded with everything in it's new position.
        self.load_display()

    # Function to play music within the menu system. Takes a link.
    def play_music(self, music_link: str = ""):

        # Try is used to catch errors and prevent crashing. This could be the result of a typo in a read file, a
        # misplaced or deleted file, or a programming error in which the wrong type is passed into the music player.
        try:
            # Load the music from the link provided, and play it!
            pygame.mixer.music.load(music_link)
            pygame.mixer.music.play()

        # Error catching: Either the file is misplaced or a wrong link was used...
        except FileNotFoundError:
            print("Could not find correct music  file")
        # Or the wrong type was passed in.
        except TypeError:
            print("Cannot play music (link was not passed in)")

    # A function to render the current menu display to the screen as it based on the list.
    def load_display(self):

        DISPLAYSURF.fill(WHITE)
        self.display_items()
        pygame.display.update()

    # A function to reset the items and load in a new set of cards based on the file provided. This will be used mostly
    # For the ORIGINALS, CLASSICS, and MINIGAMES files.
    def load_menu_from_file(self, file=ORIGINALS):

        # Fill with black loading screen while menu loads (Indicates something is changing, so user does not press
        # Button again
        DISPLAYSURF.fill(BLACK)
        display_text_box("Loading...", (DEFAULT_PADDING, DEFAULT_PADDING, DISPLAY_HEIGHT, DISPLAY_WIDTH), WHITE,
                         text_huge, aa=True)
        pygame.display.update()

        # Stop any currently playing music
        pygame.mixer.music.stop()

        # The imported read_file command is used to return a 2D array with the parameters for each card.
        f = read_file(file)

        # Reset the current items
        self.items = []

        # For each of the cards read, create a GameMenuCard with all of the correct properties.
        # Most of the parameters are taken as strings, such as titles, descriptions, and links,
        # But color is converted to a tuple by essentially breaking it down, and then
        # number_of_players and completion time is converted to an integer.
        for ref in f:

            try:
                add_item = GameMenuCard(
                    title=ref["title"],
                    description=ref["description"],
                    background_image=ref["background_image"],
                    music=ref["music"],
                    color=tuple(map(int, ref["color"].split(', '))),
                    game_file=ref["game_file"],
                    hi_score_file=ref["hi_score_file"],
                    number_of_players=int(ref["number_of_players"]),
                    completion_time=int(ref["completion_time"]),
                )

                # For each of the cards added, prepare a display for it.
                add_item.prepare_display()

                # Add the card to the MenuGroup as a card object.
                self.add_to_group(add_item)

            except ValueError:  # For now, if the file item is not configured properly and it throws an error,
                pass  # Do not load the card.

        # As long as some cards loaded, play the music of the first card.
        # (These are game cards, so they have music properties... no need to check)
        if self.items != []:
            self.play_music(self.items[0].music)

        # Load the display!
        self.load_display()

    # A function to load in the three top-level menu options (HD Originals, Classics, and Minigames).
    def load_primary_menu(self):

        # Fill with black loading screen while menu loads (Indicates something is changing, so user does not press
        # Button again
        DISPLAYSURF.fill(BLACK)
        display_text_box("Loading...", (DEFAULT_PADDING, DEFAULT_PADDING, DISPLAY_HEIGHT, DISPLAY_WIDTH), WHITE,
                         text_huge, aa=True)
        pygame.display.update()

        # Stop any music that is playing
        pygame.mixer.music.stop()

        # Reset the menu list.
        self.items = []

        # Add three cards.
        #   Type 0 is HD Originals
        #   Type 1 is Classics
        #   Type 2 is Minigames
        self.add_to_group(PrimaryMenuCard(color=(255, 160, 100), type=0))
        self.add_to_group(PrimaryMenuCard(color=(100, 160, 255), type=1))
        self.add_to_group(PrimaryMenuCard(color=(100, 255, 160), type=2))

        # Load the display!
        self.load_display()

    # Method to perform actions based on current selected card and controller input
    # Pass in the controller object from the controller module.
    def control(self, controller_object: Controller):

        # Get the x_axis input from the controller
        x_input = controller_object.get_x_axis()

        keys = pygame.key.get_pressed()
        key_x_input = int(keys[K_RIGHT]) - int(keys[K_LEFT])

        if key_x_input != 0:
            x_input = key_x_input

        # If the x_input is not nothing (it will either be -1 or 1)
        if x_input != 0:
            # Animate the card in the inverse direction of the controller
            self.animate_cards(-x_input)

        # If there are items in the menu, set "card" to be the first item in the list.
        if len(self.items) > 0:
            card = self.items[0]
        else:
            # If there is no cards, then card is None
            card = None

            # If there are no cards, escape back to the main menu by pressing "b"
            if controller_object.is_button_just_pressed("b") or keys[K_b]:
                self.load_primary_menu()

        # If the card is a primary menu card, then do this
        if type(card) == PrimaryMenuCard:

            if controller_object.is_button_just_pressed("a") or keys[K_a]:

                if card.type == 0:

                    self.load_menu_from_file(ORIGINALS)

                elif card.type == 1:

                    self.load_menu_from_file(CLASSICS)

                elif card.type == 2:

                    self.load_menu_from_file(MINIGAMES)

        # If the card is a game menu card, then do this
        elif type(card) == GameMenuCard:

            if controller_object.is_button_just_pressed("b") or keys[K_b]:
                self.load_primary_menu()

            if controller_object.is_button_just_pressed("a") or keys[K_a]:

                try:
                    Popen(card.game_file)
                    # holding_state() # TODO: Permit holding state when foreground game is running
                except FileNotFoundError:
                    print("Could not open associated file!")

    def pause_screen_slides(self):

        # Fill with black loading screen while menu loads (Indicates something is changing, so user does not press
        # Button again
        DISPLAYSURF.fill(BLACK)
        display_text_box("Loading...", (DEFAULT_PADDING, DEFAULT_PADDING, DISPLAY_HEIGHT, DISPLAY_WIDTH), WHITE,
                         text_huge, aa=True)

        # This is probably not efficient, or anything, but frankly it's easy so here we are.
        slides = []
        i = 0

        for file in (ORIGINALS, CLASSICS, MINIGAMES):

            self.load_menu_from_file(file)

            for each in self.items:

                if type(each) == GameMenuCard:

                    text = each.title

                    slides.append(each.background)

                    color = each.color

                    # Contrast is checked and text is either white or black depending on which is more readable.
                    if (color[0] * color[1] * color[2]) < (256 ** 3 / 2):
                        if color[0] > 230 or color[1] > 190:
                            text_color = BLACK
                        else:
                            text_color = WHITE
                    else:
                        text_color = BLACK

                    rect = (
                        DEFAULT_PADDING,
                        DEFAULT_PADDING,
                        DISPLAY_WIDTH - DEFAULT_PADDING * 2,
                        DISPLAY_HEIGHT - DEFAULT_PADDING * 2
                    )

                    display_text_box(text, rect, text_color, text_huge, True, surface=slides[i], background=color)

                    i += 1

        random.seed()

        # Shuffle slides in random order
        random.shuffle(slides)

        self.load_primary_menu()

        return slides



# ----- Card:
# Base class for any card object.
# Cards are a menu item, and they work with the MenuGroup objects. The base class (Card) has an image, as well as
# A few other parameters that govern how the card is structured.
# Cards have certain properties and methods which allow them to work in the MenuGroup
class Card:

    # When a base card is initialized (either directly, or indirectly), all it really needs is a color parameter. All
    # the rest will be configured and displayed automatically through code.
    def __init__(self, color: tuple = WHITE):

        # Position is the relative position of the card in respect to the screen (0 is middle, -1 is to the left, and
        # 1 is to the right). It is set to 0 for now, but it's position is changed through code later.
        self.position = 0
        # Color is the color tint of the card
        self.color = color

        # Size of the card (#s have to be ints)
        self.size = (round(CARD_WIDTH), round(CARD_HEIGHT))

        # Absolute location of card (top corner)
        self.location = (
            (DISPLAY_WIDTH - CARD_WIDTH) / 2,
            (DISPLAY_HEIGHT - CARD_HEIGHT) / 2,
        )

        # Set up a rectangle to represent the shape of the card as a box.
        # **NOTE: This is currently an unused feature.**
        self.rect = (
            self.location[0],
            self.location[1],
            self.size[0],
            self.size[1]
        )
        # A text rectangle is used to represent the size of the area text can be placed. This is not relative to the
        # DISPLAYSURF, and is only relative to the card surface itself, so it doesn't have to be absolute.
        self.text_rect = (
            DEFAULT_PADDING,
            DEFAULT_PADDING,
            CARD_WIDTH - DEFAULT_PADDING * 2,
            CARD_HEIGHT - DEFAULT_PADDING * 2,
        )

        # The original display is configured. This is the card at it's max (default CARD) resolution. When the card is
        # scaled down or up, it does so from this as a base resolution, otherwise distortion would occur.
        self.original_display = pygame.image.load("resources/menu_ui/menu_card.png")
        self.original_display.fill(
            (self.color[0], self.color[1], self.color[2], 100),
            special_flags=pygame.BLEND_MULT
        )
        self.original_display = pygame.transform.scale(self.original_display, (round(CARD_WIDTH), round(CARD_HEIGHT)))

        # display property is what is actually shown. This can be scaled down or up freely, but will always be
        # updated based on the base resolution.
        self.display = self.original_display

        # Each card has an associated background property. This gets the default background, and colorizes it to
        # match the card. (So unless otherwise set, the background will be this.)
        self.background = get_default_background()
        self.background.fill(
            (self.color[0], self.color[1], self.color[2], 255),
            special_flags=pygame.BLEND_MULT
        )
        ratio = self.background.get_width() / self.background.get_height()
        screen_ratio = DISPLAY_WIDTH / DISPLAY_HEIGHT

        if screen_ratio >= ratio:
            img_width = int(DISPLAY_WIDTH)
            img_height = int(float(img_width / ratio))
        else:
            img_height = int(DISPLAY_HEIGHT)
            img_width = int(img_height * ratio)

        self.background = pygame.transform.scale(self.background, (img_width, img_height))

    # A function to blit the card to the screen at a particular location. First, if the specified position is different
    # then the internal position is updated to match, the card is prepared (another method) and it is blitted.
    def display_card(self, relative_position: int = 0):

        if self.position != relative_position:
            self.position = relative_position
            self.prepare_display()

        DISPLAYSURF.blit(self.display, self.location)

    # A function to update parameters and prepare the display for the card
    def prepare_display(self):

        # Update the actual dimensions of the card
        self.size = (
            round(CARD_WIDTH / (abs(self.position / DEPTH_SCALE) + 1)),
            round(CARD_HEIGHT / (abs(self.position / DEPTH_SCALE) + 1))
        )

        # Absolute location of card (top corner)
        self.location = (
            (DISPLAY_WIDTH - self.size[0]) / 2 + (CARD_WIDTH + DEFAULT_PADDING) * self.position,
            (DISPLAY_HEIGHT - self.size[1]) / 2,
        )

        # Creates a rectangle of the card (unused)
        self.rect = (
            self.size[0],
            self.size[1],
            self.location[0],
            self.location[1]
        )

        # Change the display to the scaled image based on the original card display.
        self.display = pygame.transform.scale(self.original_display, self.size)

    # A function to change the internal background of the card to something else
    def change_background(self, link: str = "resources/menu_ui/background_default.png"):

        try:

            self.background = pygame.image.load(link)

            ratio = self.background.get_width() / self.background.get_height()
            screen_ratio = DISPLAY_WIDTH / DISPLAY_HEIGHT

            if screen_ratio >= ratio:
                img_width = int(DISPLAY_WIDTH)
                img_height = int(float(img_width / ratio))
            else:
                img_height = int(DISPLAY_HEIGHT)
                img_width = int(img_height * ratio)

            self.background = pygame.transform.scale(self.background, (img_width, img_height))

        except FileNotFoundError:

            print("Background.change: Error, file (" + link + ") not found.")

        except TypeError:

            print("Background.change: Error, invalid type entered!")


# A class for the main menu cards.
class PrimaryMenuCard(Card):

    # Primary menu card has a unique property called type, which just indicates what the card is
    def __init__(self, color, type):
        super().__init__(color)
        self.type = type

        # For each type, load in certain properties
        if self.type == 0:

            title_image = pygame.image.load("resources/menu_ui/hd_originals_card.png")
            title_image = pygame.transform.scale(title_image, (round(CARD_WIDTH), round(CARD_WIDTH)))

            location = (
                CARD_WIDTH / 2 - title_image.get_width() / 2 + 30 * IDEAL_PIXEL_RATIO,
                CARD_HEIGHT / 2 - title_image.get_height() / 2 + 20 * IDEAL_PIXEL_RATIO
            )

            self.original_display.blit(title_image, location)

        elif self.type == 1:

            title_image = pygame.image.load("resources/menu_ui/classic_games_card.png")
            title_image = pygame.transform.scale(title_image, (round(CARD_WIDTH), round(CARD_WIDTH)))

            location = (
                CARD_WIDTH / 2 - title_image.get_width() / 2 + 30 * IDEAL_PIXEL_RATIO,
                CARD_HEIGHT / 2 - title_image.get_height() / 2 + 20 * IDEAL_PIXEL_RATIO
            )

            self.original_display.blit(title_image, location)

        elif self.type == 2:

            title_image = pygame.image.load("resources/menu_ui/minigames_card.png")
            title_image = pygame.transform.scale(title_image, (round(CARD_WIDTH), round(CARD_WIDTH)))

            location = (
                CARD_WIDTH / 2 - title_image.get_width() / 2 + 30 * IDEAL_PIXEL_RATIO,
                CARD_HEIGHT / 2 - title_image.get_height() / 2 + 20 * IDEAL_PIXEL_RATIO
            )

            self.original_display.blit(title_image, location)

        self.prepare_display()


# Also a class for game menu cards. These cards can hold additional content such as titles, descriptions, music
# Game file location, etc.
class GameMenuCard(Card):

    def __init__(self, **kwargs):
        super().__init__(kwargs["color"])

        self.title = kwargs["title"]
        if len(self.title) < 15:
            text_type = text_huge
        else:
            text_type = text_h1
        next_line = display_text_box(self.title, self.text_rect, WHITE, text_type, centered=True,
                                     surface=self.original_display)
        x = self.text_rect
        self.text_rect = (x[0] + 10, x[1] + next_line, x[2] - 20, x[3] - next_line)

        self.description = kwargs["description"]
        display_text_box(self.description, self.text_rect, WHITE, text_p, centered=True, aa=True,
                         surface=self.original_display)

        self.background_image = kwargs["background_image"]
        self.change_background(self.background_image)
        self.music = kwargs["music"]

        self.number_of_players = kwargs["number_of_players"]
        self.completion_time = kwargs["completion_time"]

        self.game_file = kwargs["game_file"]
        self.hi_score_file = kwargs["hi_score_file"]

        # LOAD IN THE UI ELEMENTS (This is too complex, if you are reading this, I am so sorry I did it this way.)

        # A quick function to make a ui box. Two will be made, one for number of players, and one for time
        def ui_box(text):
            graphic = pygame.image.load("resources/menu_ui/small_card.png")
            graphic = pygame.transform.scale(
                graphic,
                (round(150 * IDEAL_PIXEL_RATIO),
                 round(150 * IDEAL_PIXEL_RATIO))
            )
            display_text_box(
                text,
                (
                    0,
                    round(15 * IDEAL_PIXEL_RATIO),
                    graphic.get_width(),
                    graphic.get_height()
                ),
                WHITE,
                text_h3,
                centered=True,
                aa=True,
                restrict=False,
                surface=graphic
            )

            return graphic

        # Set up player graphic (It's tedious)
        self.players_graphic = ui_box("# Players")

        player_icon = pygame.image.load("resources/menu_ui/player_icon.png")
        player_icon = pygame.transform.scale(player_icon, (
            round(50 * IDEAL_PIXEL_RATIO),
            round(50 * IDEAL_PIXEL_RATIO),
        ))

        blit_y = self.players_graphic.get_height() / 2 - player_icon.get_height() / 2

        spacing = 25 * IDEAL_PIXEL_RATIO

        if self.number_of_players == 1:
            self.players_graphic.blit(player_icon, (spacing, blit_y))
            player_icon.fill(BLACK, special_flags=pygame.BLEND_MULT)
            self.players_graphic.blit(player_icon, (spacing * 3, blit_y))
        elif self.number_of_players == 2:
            self.players_graphic.blit(player_icon, (spacing, blit_y))
            self.players_graphic.blit(player_icon, (spacing * 3, blit_y))

        self.players_graphic.fill(
            (self.color[0], self.color[1], self.color[2], 255),
            special_flags=pygame.BLEND_MULT
        )

        self.time_graphic = ui_box("Duration")

        time_icon = pygame.image.load("resources/menu_ui/timer_icon.png")
        time_icon = pygame.transform.scale(time_icon, (
            round(35 * IDEAL_PIXEL_RATIO),
            round(35 * IDEAL_PIXEL_RATIO),
        ))

        blit_y = self.time_graphic.get_height() / 2 - time_icon.get_height() / 2

        spacing = 20 * IDEAL_PIXEL_RATIO

        self.time_graphic.blit(time_icon, (spacing, blit_y))

        display_text_box(str(self.completion_time),
                         (0, 50 * IDEAL_PIXEL_RATIO, 180 * IDEAL_PIXEL_RATIO, 50 * IDEAL_PIXEL_RATIO), WHITE, text_h2,
                         True, True, False, self.time_graphic)
        display_text_box("min", (0, 80 * IDEAL_PIXEL_RATIO, 180 * IDEAL_PIXEL_RATIO, 80 * IDEAL_PIXEL_RATIO), WHITE,
                         text_h3, True, True, False, self.time_graphic)

        self.time_graphic.fill(
            (self.color[0], self.color[1], self.color[2], 255),
            special_flags=pygame.BLEND_MULT
        )

    def display_card(self, relative_position: int = 0):
        super().display_card(relative_position)

        graphic_x = self.location[0] + self.size[0] / 3 - self.players_graphic.get_width() / 2
        graphic_y = self.location[1] + self.size[1] - self.players_graphic.get_height() - 15 * IDEAL_PIXEL_RATIO

        DISPLAYSURF.blit(self.players_graphic, (graphic_x, graphic_y))
        graphic_x = self.location[0] + 2 * self.size[0] / 3 - self.players_graphic.get_width() / 2
        DISPLAYSURF.blit(self.time_graphic, (graphic_x, graphic_y))
