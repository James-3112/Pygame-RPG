import pygame
from math import sin

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0 # Set the frame index (For animations) to 0
        self.animation_speed = 0.15 # Set the animation speed to 0.15
        self.direction = pygame.math.Vector2() # Create the direction and make it a vector2

    # Move Funtion (Moves the player with the ditection)
    def move(self, speed):
        # Normalize the direction so you don't go faster going  
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed # Move the hitbox horizontally then cheek for collision
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical') # Move the hitbox vertically then cheek for collision
        self.rect.center = self.hitbox.center # Moves the entity hitbox

    # Collision Funtion (Cheeks for collisions)
    def collision(self, direction):
        # Horizontal
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites: # Go through all obstacles sprites
                if sprite.hitbox.colliderect(self.hitbox): # If colliding
                    if self.direction.x > 0: # Moving Right
                        self.hitbox.right = sprite.hitbox.left # Move left
                    if self.direction.x < 0: # Moving Left
                        self.hitbox.left = sprite.hitbox.right # Move right

        # Vertical       
        if direction == 'vertical':
            for sprite in self.obstacle_sprites: # Go through all obstacles sprites
                if sprite.hitbox.colliderect(self.hitbox): # If colliding
                    if self.direction.y > 0: # Moving Down
                        self.hitbox.bottom = sprite.hitbox.top # Move down
                    if self.direction.y < 0: # Moving Up
                        self.hitbox.top = sprite.hitbox.bottom # Move Up

    def wave_value(self):
        value = sin(pygame.time.get_ticks())

        # Step funtion
        if value >= 0:
            return 255
        else:
            return 0