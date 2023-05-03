'''
This is the Debug script, this is whate i can use to degub my code
It add a black box and some text on whatever your trying to debug
'''

import pygame # Import pygame
pygame.init() # Initialize pygame
font = pygame.font.Font(None,30) # Set the font size

# Debug Function (This is used to debug thing)
def debug(info, y = 10, x = 10):
    display_surface = pygame.display.get_surface() # Get the screen
    debug_surf = font.render(str(info),True,'White') # Render the text
    debug_rect = debug_surf.get_rect(topleft = (x,y)) # Get the position of the text
    pygame.draw.rect(display_surface,'Black',debug_rect) # Darw a black box on the screen
    display_surface.blit(debug_surf,debug_rect) # Darw the text on the screen