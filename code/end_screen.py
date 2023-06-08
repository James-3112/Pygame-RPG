import pygame
from settings import *
from support import import_folder
import os # Import os (Operating system)

# Get the absolute path for this directory
sourceFileDir = os.path.dirname(os.path.abspath(__file__))

class End_Screen:
    def __init__(self):
        # Set up Menu (Image, Position)
        self.image = pygame.image.load(os.path.join(sourceFileDir, '../graphics/end_screen/EndScreen_NoText.png')).convert_alpha() # Set the image
        self.rect = self.image.get_rect(topleft = (0,0)) # Set the position
        
        self.display_surface = pygame.display.get_surface() # Get the screen
        self.font = pygame.font.Font(FONT, 30) # Set the font size

    def run(self):
        text = self.font.render('Press Space To Quit',True,'White') # Render the text
        pos = text.get_rect(center = (WIDTH / 2, HEIGTH / 2 + 200)) # Get the position of the text
        self.display_surface.blit(self.image, (0,0))
        self.display_surface.blit(text, pos) # Darw the text on the screen
        
        # Quiting
        keys = pygame.key.get_pressed() # Get all tthe key from pygame
        if keys[pygame.K_SPACE]:
            pygame.Quit()
