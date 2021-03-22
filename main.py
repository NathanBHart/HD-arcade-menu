# main.py
# This is the main program which runs the menu system.
# ---------------------------------------------------------------------------------------------------------------------


# --------- IMPORT CUSTOM MODULES: ------------------------------------------------------------------------------------
# from locals import * # Note that pygame and the controller is imported through the locals module!
from cards import *
# ---------------------------------------------------------------------------------------------------------------------


# --------- MAIN PROGRAM: ---------------------------------------------------------------------------------------------

menu = MenuGroup()
menu.load_primary_menu()

# Ensure main_loop is active
main_loop = True

while main_loop:

    CLOCK.tick(FPS)
    console_control.update()

    # process inputs (events)
    for event in pygame.event.get():
        # close the window
        if event.type == pygame.QUIT:
            main_loop = False

    menu.control(console_control)
