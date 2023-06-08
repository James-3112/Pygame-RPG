import pygame
from settings import *
from support import import_folder
import os # Import os (Operating system)

# Get the absolute path for this directory
sourceFileDir = os.path.dirname(os.path.abspath(__file__))

class How_To_Play:
    def __init__(self):
        # Set up Menu (Image, Position)
        self.image = pygame.image.load(os.path.join(sourceFileDir, '../graphics/how_to_play_screen/how_to_play.png')).convert_alpha() # Set the image
        self.rect = self.image.get_rect(topleft = (0,0)) # Set the position
        
        self.display_surface = pygame.display.get_surface() # Get the screen

    def run(self):
        self.display_surface.blit(self.image, (0,0))