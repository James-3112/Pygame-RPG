'''
This is the Weapon script, this is where the weapons class is initialized
This sets the position and graphics for all the weapons in the game
'''

import pygame # Import pygame
import os # Import os (Operating system)

# Get the absolute path for this directory
sourceFileDir = os.path.dirname(os.path.abspath(__file__))

# Main Weapon class
class Weapon(pygame.sprite.Sprite):
    # Initialize Function (This is called when the class "Tile" is created)
    def __init__(self, player, groups):
        super().__init__(groups) # Sets the groups
        self.sprite_type = 'weapon'
        direction = player.status.split('_')[0] # Get the players direction

        # Get the weapon image
        self.image = pygame.image.load(os.path.join(sourceFileDir, f'../graphics/weapons/{player.weapon}/{direction}.png')).convert_alpha()

        # Set the position of the weapon
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16)) # Right
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16)) # Left
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10,0)) # Down
        else:
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10,0)) # Up