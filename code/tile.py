'''
This is the Tile script, this is where the tile class is initialized
This sets the size and hitboxs for all the objects in the game
'''

import pygame # Import pygame
from settings import * # Import everythin form settings

# Main Tile class
class Tile(pygame.sprite.Sprite):
	# Initialize Function (This is called when the class "Tile" is created)
	def __init__(self,pos,groups,sprite_type,surface = pygame.Surface((TILESIZE, TILESIZE))):
		super().__init__(groups) # init (Initialize) groups
		
		# Sets some variables
		self.sprite_type = sprite_type
		self.image = surface

		if sprite_type == 'object': # If an object
			self.rect = self.image.get_rect(topleft = (pos[0],pos[1] - TILESIZE)) # Set the hight 2 time bigger
		else: # Every other sprite
			self.rect = self.image.get_rect(topleft = pos) # Set the position
		self.hitbox = self.rect.inflate(0, -10) # Set the hitbox