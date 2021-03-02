# Nathan Hart
# March 2021
# Game Console Input -- Module

import pygame

pygame.init()
pygame.joystick.init()

# Set up a class for controllers (up to two may be present in a game)
class ArcadeController:

    def __init__(self, id):

        self.controller = pygame.joystick.Joystick(id)
        self.axis = (self.controller.get_axis(0), self.controller.get_axis(1))
        self.button_0 = self.controller.get_button(0)
        self.button_1 = self.controller.get_button(1)
        self.button_2 = self.controller.get_button(2)
        self.button_3 = self.controller.get_button(3)


    def get_button(self, button_id):

        return self.controller.get_button(button_id)

    def is_button_tapped(self, button_id):

        pass

    def is_button_just_pressed(self, button_id):

        pass

    def is_joystick_tapped(self):

        pass
