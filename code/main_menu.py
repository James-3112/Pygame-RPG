import pygame
from settings import *
from support import import_folder
import os # Import os (Operating system)

# Get the absolute path for this directory
sourceFileDir = os.path.dirname(os.path.abspath(__file__))

class Main_Menu:
    def __init__(self):
        # Set up Menu (Image, Position)
        self.image = pygame.image.load(os.path.join(sourceFileDir, '../graphics/main_menu/MainMenu1.png')).convert_alpha() # Set the image
        self.rect = self.image.get_rect(topleft = (0,0)) # Set the position

        self.animation = import_folder(os.path.join(sourceFileDir, '../graphics/main_menu'))
        self.frame_index = 0
        self.animation_speed = 0.15
        
        self.display_surface = pygame.display.get_surface() # Get the screen
        self.font = pygame.font.Font(FONT, 30) # Set the font size

    def run(self):
        self.frame_index += self.animation_speed # Frame index = frame index + animation speed
        if self.frame_index >= len(self.animation): # If the fram index is longer then the len of the animations
            self.frame_index = 0 # Then set the frame index back to 0

        self.image = self.animation[int(self.frame_index)] # Set the animation

        text = self.font.render('Press Space To Play',True,'White') # Render the text
        pos = text.get_rect(center = (WIDTH / 2, HEIGTH / 2 + 200)) # Get the position of the text
        self.display_surface.blit(self.image, (0,0))
        self.display_surface.blit(text, pos) # Darw the text on the screen