import pygame # Import pygame
from settings import * # Import all from settings
from entity import Entity # Import the class entity from entity
from end_screen import End_Screen
import os # Import os (Operating system)

# Get the absolute path for this directory
sourceFileDir = os.path.dirname(os.path.abspath(__file__))

class Girl(Entity):
    def __init__(self, pos, groups, obstacle_sprites):
        # General Setup
        super().__init__(groups) # Initialize groups
        self.sprite_type = 'girl' # Set the sprite type to enemy
        
        # Set up player (Image, Position)
        self.image = pygame.image.load(os.path.join(sourceFileDir, '../graphics/test/player.png')).convert_alpha() # Set the image
        self.rect = self.image.get_rect(topleft = pos) # Set the position
    
    # Get player distance / direction Function (Returns the distance and direction of the player)
    def get_player_distance_direction(self,player):
        enemy_vec = pygame.math.Vector2(self.rect.center) # Changes the enemys position to a vector2 (float, float)
        player_vec = pygame.math.Vector2(player.rect.center) # Changes the players position to a vector2 (float, float)
        distance = (player_vec - enemy_vec).magnitude() # Subtract the player and enemy position and then get the magnitude to get the distance

        if distance > 0: # So if distance is 0 it doesn't give an error
            direction = (player_vec - enemy_vec).normalize() # Subtract the player and enemy position and then get the normalize value to get the direction
        else:
            direction = pygame.math.Vector2() # If it is 0 set it back to 0

        return (distance,direction) # Return distance and direction
    
    def run(self, player):
        if self.get_player_distance_direction(player)[0] <= 70:
            keys = pygame.key.get_pressed() # Get all tthe key from pygame
            if keys[pygame.K_e]:
                player.health = 0
                