'''
This is the Player script, this is where everything to do with the player is done
Such as Movement, Collisions, Weapons, and animations
'''

import pygame # Import pygame
from settings import * # Import all from settings
from support import import_folder # Import "import_folder" form support
from entity import Entity # Import the class entity from entity
import os # Import os (Operating system)

# Get the absolute path for this directory
sourceFileDir = os.path.dirname(os.path.abspath(__file__))

# Main Player class
class Player(Entity):
    # Initialize Function (This is called when the class "Player" is created)
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack):
        # Run the init Function for groups
        super().__init__(groups)
        
        # Set up player (Image, Position, Hitbox)
        self.image = pygame.image.load(os.path.join(sourceFileDir, '../graphics/test/player.png')).convert_alpha() # Set the image
        self.rect = self.image.get_rect(topleft = pos) # Set the position
        self.hitbox = self.rect.inflate(0, -26) # Set the hitbox size

        # Graphics Settings
        self.import_player_assets() # Import assets
        self.status = 'down' # Set the status to down

        # Attacking Settings
        self.attacking = False # Set attacking to false
        self.attack_cooldown = 400 # Set attack cool down to 400
        self.attack_time = None # Set attack time to none
        
        self.obstacle_sprites = obstacle_sprites # Set the obstacle sprites

        # Weapon Settings
        self.create_attack = create_attack # Set the create attack Function
        self.destroy_attack = destroy_attack # Set the destroy attack Function
        self.weapon_index = 0 # Set the weapon index to 0
        self.weapon = list(weapon_data.keys())[self.weapon_index] # Set the weapons
        self.can_switch_weapon = True # Set can switch weapon to true
        self.weapon_switch_time = None # Set weapon switch time to none
        self.switch_duration_cooldown = 200 # Set switch duration cooldown to 200

        # Stats
        self.stats = {'health': 100, 'energy': 60, 'attack': 10, 'speed': 5} # Set base stats
        self.health = self.stats['health'] # Set health to stats health
        self.energy = self.stats['energy'] # Set energy to stats energy
        self.speed = self.stats['speed'] # Set speed to stats speed

    # Import Player Assets Funtion (This import the all the players animations)
    def import_player_assets(self):
        character_path = os.path.join(sourceFileDir, '../graphics/player/') # Get all the player animations
        self.animations = {'up': [],'down': [],'left': [],'right': [], # Initialize animations
			'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
			'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}
        
        for animation in self.animations.keys(): # go through all the animations and set them
            self.animations[animation] = import_folder(character_path + animation)

    # Inputs Funtion (Handles all the input for the player)
    def input(self):
        if self.attacking: # If attacking return (Don't do anything)
            return

        # Get all tthe key from pygame
        keys = pygame.key.get_pressed()

        # Movement Input (Sets direction and status)
        # Up and Down
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0

        # Left and Right
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0

        # Attack Input
        # Creates attacks
        if keys[pygame.K_SPACE]:
            self.attack_time = pygame.time.get_ticks()
            self.attacking = True
            self.create_attack()

        # Switching Weapon
        if keys[pygame.K_q] and self.can_switch_weapon:
            self.can_switch_weapon = False
            self.weapon_switch_time = pygame.time.get_ticks()

            # Goes through all the weapon if there are not weapons go back to the begining
            if self.weapon_index < len(list(weapon_data.keys())) - 1:
                self.weapon_index += 1
            else:
                self.weapon_index = 0

            # Then set the weapon
            self.weapon = list(weapon_data.keys())[self.weapon_index]

    # Get Status Funtion (Handles the status for animations)
    def get_status(self):
        # Idle (If we aren't move and not attacking then set idle)
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        # Attacking (If we are attacking set movement to 0)
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0

            if not 'attack' in self.status: # if Attack is not in status
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle','_attack') # replace idle with attacking
                else:
                    self.status = self.status + '_attack' # if we are not idel then just add attacking
        elif 'attack' in self.status: # If we are not attacking then remove attacking from status
            self.status = self.status.replace('_attack','')

    # Cool Downs Funtion (Handles cool downs)
    def cooldowns(self):
        current_time = pygame.time.get_ticks() # Set the current time

        if self.attacking: # If attacking
            if current_time - self.attack_time >= self.attack_cooldown: # If attack cool down has passed
                self.attacking = False # Set attacking to False and destroy the attack
                self.destroy_attack()

        if not self.can_switch_weapon: # If can switch weapon = false
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown: # If switch weaon cool down has passed
                self.can_switch_weapon = True # Set the can switch weapon to true

    # Animate Funtion (Animates the player)
    def animate(self):
        animation = self.animations[self.status] # Set the animation to the status of the player

        self.frame_index += self.animation_speed # Frame index = frame index + animation speed
        if self.frame_index >= len(animation): # If the fram index is longer then the len of the animations
            self.frame_index = 0 # Then set the frame index back to 0

        self.image = animation[int(self.frame_index)] # Set the animation
        self.rect = self.image.get_rect(center = self.hitbox.center) # Recenter the rectangle

    # Update (This runs every time the game updates)
    def update(self): # Run all the Funtions
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)