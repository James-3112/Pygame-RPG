import pygame # Import pygame
from settings import * # Import all from settings
from entity import Entity # Import the Entity class from entity
from support import * # Import all from support
import os # Import os (Operating system)

# Get the absolute path for this directory
sourceFileDir = os.path.dirname(os.path.abspath(__file__))

# Main Enemy class
class Enemy(Entity):
    # Initialize Function (This is called when the class "Enemy" is created)
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles):
        # General Setup
        super().__init__(groups) # Initialize groups
        self.sprite_type = 'enemy' # Set the sprite type to enemy

        # Graphics setup
        self.import_graphics(monster_name) # Import all the graphics for the monster
        self.status = 'idle' # Set the status to idle
        self.image = self.animations[self.status][self.frame_index] # Set the image

        # Movement
        self.rect = self.image.get_rect(topleft = pos) # Get the rect (Rectangle) from the image
        self.hitbox = self.rect.inflate(0, -10) # Set the hitbox size
        self.obstacle_sprites = obstacle_sprites # Set the obstacle sprites

        # Stats
        self.monster_name = monster_name # Get the monster name
        monster_info = monster_data[self.monster_name] # Get the monster info
        self.health = monster_info['health'] # Set monster health
        self.speed = monster_info['speed'] # Set monster speed
        self.attack_damage = monster_info['damage'] # Set monster damage
        self.resistance = monster_info['resistance'] # Set monster resistance
        self.attack_radius = monster_info['attack_radius'] # Set monster attack radius
        self.notice_radius = monster_info['notice_radius'] # Set monster notice radius
        self.attack_type = monster_info['attack_type'] # Set monster attack type

        # Player Interaction
        self.can_attack = True # If the monster can attack
        self.attack_time = None # Time of the attack
        self.attack_cooldown = 400 # Attack cool down
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles

        # Invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincivility_duration = 300

        # Sounds
        self.death_sound = pygame.mixer.Sound(os.path.join(sourceFileDir, '../audio/death.wav'))
        self.hit_sound = pygame.mixer.Sound(os.path.join(sourceFileDir, '../audio/hit.wav'))
        self.attack_sound = pygame.mixer.Sound(monster_info['attack_sound'])

        self.death_sound.set_volume(0.2)
        self.hit_sound.set_volume(0.2)
        self.attack_sound.set_volume(0.3)
    
    # Import graphics Function (Import all the monster graphics)
    def import_graphics(self, name):
        self.animations = {'idle': [], 'move': [], 'attack': []} # Define animations
        main_path = os.path.join(sourceFileDir, f'../graphics/monsters/{name}/') # Get the path

        for animation in self.animations.keys(): # For ever animations get the animation and set it
            self.animations[animation] = import_folder(main_path + animation)

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
    
    # Get status Function (Gets the status of the enemy)
    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0] # Get the distance from the player

        if distance <= self.attack_radius and self.can_attack: # If the distance is less then the attack radius then attack
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius: # If the distance is less then the notice radius move towards the player
            self.status = 'move'
        else: # Else set the status to idle
            self.status = 'idle'

    # Action Function (Tell the enemy what to do with the status)
    def actions(self, player):
        if self.status == 'attack': # If attacking then set the attack time to now
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
            self.attack_sound.play()
        elif self.status == 'move': # If moving then set the direction to the direction of the player
            self.direction = self.get_player_distance_direction(player)[1]
        else: # Else set the direction to 0
            self.direction = pygame.math.Vector2()

    # Animate Function (Animate the enemy)
    def animate(self):
        animation = self.animations[self.status] # Set the animation to the status of the enemy

        self.frame_index += self.animation_speed # Frame index = frame index + animation speed
        if self.frame_index >= len(animation): # If the fram index is longer then the len of the animations
            if self.status == 'attack': # At the end of the animation if attacking set can attack to false
                self.can_attack = False
            self.frame_index = 0 # Then set the frame index back to 0

        self.image = animation[int(self.frame_index)] # Set the animation
        self.rect = self.image.get_rect(center = self.hitbox.center) # Recenter the rectangle

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
    
    # Cool down Function (Handles the cool down for the attacks)
    def cooldowns(self):
        current_time = pygame.time.get_ticks() # Get the current time (The time at the end of the animate)
        
        if not self.can_attack: # If can't attack
            if current_time - self.attack_time >= self.attack_cooldown: # If the cool down has passed the set can attack to true
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincivility_duration:
                self.vulnerable = True

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.hit_sound.play()
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()

            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.trigger_death_particles(self.rect.center, self.monster_name)
            self.death_sound.play()

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    # Update (Updates the enemy)
    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()

    # Enemy update (Update only enemy with the player)
    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)