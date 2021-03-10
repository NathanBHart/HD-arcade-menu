import pygame

pygame.joystick.init()

class Controller():

    # A controller object should be set up at the start of each program with
    # an ID value. One should be made for each controller used.
    def __init__(self, id):

        if pygame.joystick.get_count() > id + 1:
            self.Object = pygame.joystick.Joystick(id)
        else:
            self.Object = None
            print("!!Error: Controller ID invalid (out of range, or not initialized.)")

        self.current_buttons = []
        self.buttons_last_frame = []

    def is_controller_active(self):
        return self.Object != None

    # Call this every frame so that is_button_just_pressed function works
    def update(self):

        if self.is_controller_active() == False: return

        self.buttons_last_frame = self.current_buttons

        self.current_buttons = []

        for i in range(5):

            if self.Object.get_button(i) == True: self.current_buttons.append(i)

    # Return the axis as a tuple
    def get_axis(self):
        if self.is_controller_active() == False: return (0, 0)
        return (round(self.Object.get_axis(0)), round(self.Object.get_axis(1)))

    # Return just x axis
    def get_x_axis(self):
        if self.is_controller_active() == False: return 0
        return round(self.Object.get_axis(0))

    # Return just y axis
    def get_y_axis(self):
        if self.is_controller_active() == False: return 0
        return round(self.Object.get_axis(0))

    # Translate input to button id. This supports strings or numbers (so people can code with whatever
    # Is easiest
    def to_button_id(self, input):

        if input in range(0, 5):
            return input

        elif type(input) is str:

            if input == "a":

                return 0

            elif input == "b":

                return 1

            elif input == "x":

                return 2

            elif input == "y":

                return 3

            elif input == "player":

                return 4

            elif input == "menu":

                return 5

            else:

                print("Input controller value must be between 0-3, or \"a\", \"b\", \"x\", \"y\", \"player\", or \"menu\".")
                return None

        else:

            print("Invalid input. Input controller value must be between 0-3, or \"a\", \"b\", \"x\", \"y\", \"player\", or \"menu\".")
            return None

    # Check if a button is pressed. Returns integer/boolean
    def is_button_pressed(self, button):

        if self.is_controller_active() == False: return 0

        id = self.to_button_id(button)

        if not id == None: return self.Object.get_button(id)

    # Checks if a button has JUST been pressed, but does not return true continuously if button is held.
    def is_button_just_pressed(self, button):

        id = self.to_button_id(button)

        if id in self.current_buttons and id not in self.buttons_last_frame:

            return True

        else:

            return False