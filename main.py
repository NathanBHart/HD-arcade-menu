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
while main_loop:

    CLOCK.tick(FPS)
    console_control.update()

    # process inputs (events)
    for event in pygame.event.get():
        # close the window
        if event.type == pygame.QUIT:
            main_loop = False

    menu.control(console_control)
