from locals import *
#import win32gui
#import win32con


def display_text_box(text, rect, color=BLACK, font=text_h1, aa=False, centered=False, restrict=False,
                     surface=DISPLAYSURF, background = None):
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
        if background is pygame.color:
            image = font.render(text[:i], aa, color)
        else:
            image = font.render(text[:i], aa, color, background)

        if centered:
            surface.blit(image, (rect.left + (rect.width - image.get_width()) / 2, y))
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


# Currently this does not get called
# TODO: Fix holding_state() function
def holding_state():
    window = win32gui.GetForegroundWindow()

    DISPLAYSURF.fill(BLACK)
    pygame.display.update()

    pygame.display.iconify()

    hold = True

    while hold:

        console_control.update()

        # TODO: This doesn't work?
        # process inputs (events)
        for event in pygame.event.get():
            # close the window
            if event.type == QUIT:

                # Import the global main_loop from the locals.py file
                # There may be a better way to do this
                global main_loop

                hold = False
                main_loop = False

        # TODO: Test this using an actual controller!
        if console_control.is_button_just_pressed("menu"):
            # Bring back the menu display

            win32gui.ShowWindow(window, win32con.SW_SHOWNOACTIVATE)
            win32gui.BringWindowToTop(window)

            DISPLAYSURF.fill(BLACK)

            text = "Are you sure you want to return to main menu?"

            rect = (
                100 * IDEAL_PIXEL_RATIO,
                100 * IDEAL_PIXEL_RATIO,
                DISPLAY_WIDTH - 200 * IDEAL_PIXEL_RATIO,
                DISPLAY_HEIGHT - 200 * IDEAL_PIXEL_RATIO,
            )

            next_line = display_text_box(text, rect, WHITE, text_h1, centered=True)

            text = "Press (A) to Confirm, Press (B) to Cancel"

            rect = (
                100 * IDEAL_PIXEL_RATIO,
                next_line + 100 * IDEAL_PIXEL_RATIO,
                DISPLAY_WIDTH - 200 * IDEAL_PIXEL_RATIO,
                DISPLAY_HEIGHT - 200 * IDEAL_PIXEL_RATIO,
            )

            display_text_box(text, rect, WHITE, text_p, centered=True, aa=True)

            pygame.display.update()

            check_for_input = True

            while check_for_input:

                console_control.update()

                if console_control.is_button_just_pressed("a"):
                    # CLOSE PROGRAM CODE HERE
                    pass
                    check_for_input = False
                    hold = False

                elif console_control.is_button_just_pressed("b"):
                    # Return to holding state
                    # Essentially hide display, (1,1) is so small that Windows essentially will not render it.
                    pygame.display.set_mode((1, 1), RESIZABLE)
                    check_for_input = False

                CLOCK.tick(FPS)

        CLOCK.tick(FPS)