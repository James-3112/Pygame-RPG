import pygame
from settings import *
import os # Import os (Operating system)

# Get the absolute path for this directory
sourceFileDir = os.path.dirname(os.path.abspath(__file__))

deltaTime = 1 / 60

class Timer:
    def __init__(self):
        self.display_surface = pygame.display.get_surface() # Get the screen
        self.font = pygame.font.Font(FONT, 30) # Set the font size
        
        self.isRunning = True
        self.timer_text = 0

    def run(self):
        if self.isRunning == True:
            self.timer_text += deltaTime
            text = self.font.render(str(round(self.timer_text, 0)).replace(".0", ""), True, "White")
            
            pos = text.get_rect(center = (WIDTH / 2, 50))
            self.display_surface.blit(text, pos)
        else:
            self.font = pygame.font.Font(FONT, 60)
            text = self.font.render(str(round(self.timer_text, 2)), True, "White")
            
            pos = text.get_rect(center = (WIDTH / 2, 50))
            self.display_surface.blit(text, pos)