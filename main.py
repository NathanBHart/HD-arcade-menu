# main.py
# This is the main program which runs the menu system.


# --------- IMPORT CARDS MODULE: --------------------------------------------------------------------------------------
# Import chain: 'cards' imports 'locals' > 'locals' imports pygame, pygame.locals, and 'controller'
from cards import *

# --------- MAIN PROGRAM: ---------------------------------------------------------------------------------------------
# Create an empty menu group, and then load in the primary menu in that menu group.
menu = MenuGroup()
menu.load_primary_menu()

# Ensure main_loop is active
main_loop = True

# Run while main_loop is true

timer = 0.0
pause_screen = False

while main_loop:

    CLOCK.tick(FPS)
    timer += 1 / FPS
    console_control.update()

    # process inputs (events)
    for event in pygame.event.get():
        # close the window
        if event.type == QUIT:
            main_loop = False

    menu.control(console_control)

    if timer > 2:
        pause_screen = True

    if pause_screen:
        timer = 0

        slides = menu.pause_screen_slides()
        if not len(slides) > 0:
            slides.append(get_default_background())

        DISPLAYSURF.blit(slides[0], (0, 0))
        pygame.display.update()

        while pause_screen:

            CLOCK.tick(FPS)
            timer += 1 / FPS
            console_control.update()

            # process inputs (events)
            for event in pygame.event.get():
                # close the window
                if event.type == QUIT:
                    pause_screen = False
                    main_loop = False

            if timer > 4:

                if len(slides) > 0:
                    # Cycle first item to last item
                    slides.append(slides.pop(0))

                    DISPLAYSURF.fill(BLACK)
                    DISPLAYSURF.blit(slides[0], (0, 0))
                    pygame.display.update()

                timer = 0
