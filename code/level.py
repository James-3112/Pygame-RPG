'''
This is the Level script, this is where the game level get made
This where all other file get drawn
'''

import pygame # Inport pygame
from settings import * # Import everything from settings
from tile import Tile # Import the Tile class from tile
from player import Player # Import the Player class from player
from support import * # Import everything from support
from random import choice # Import choice from random
from random import randint
from weapon import Weapon # Import the Weapon class from weapon
from ui import UI # Import the UI class from ui
from enemy import Enemy # import the enemy class from enemy
from particles import AnimationPlayer
import os # Import os (Operating system)

# Get the absolute path for this directory
sourceFileDir = os.path.dirname(os.path.abspath(__file__))

# Level Class
class Level:
    # Initialize Function (This is called when the class "Level" is created)
    def __init__(self):
        self.display_surface = pygame.display.get_surface() # Geting the screen

        # Sprite Groups (Setting up sprite groups)
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        
        # Attack Sprites (For weanpon sprites)
        self.current_attack = None

        # Pygame group for the weanpon and enemys
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # Create the map / Run the create map Function
        self.create_map()

        # User interface (UI)
        self.ui = UI() # Set ui to the ui class

        self.animation_player = AnimationPlayer()

        self.running = False

    # Create Map Function (This makes the map)
    def create_map(self):
        # This is the layouts for the map these are csv files (Csv file are just python list of lists)
        layouts = {
            'boundary': import_csv_layout(os.path.join(sourceFileDir, '../graphics/map/map_FloorBlocks.csv')), # These also get pass through the "import_csv_layout" Function from support
            'grass': import_csv_layout(os.path.join(sourceFileDir, '../graphics/map/map_Grass.csv')),
            'object': import_csv_layout(os.path.join(sourceFileDir, '../graphics/map/map_Objects.csv')),
            'entities': import_csv_layout(os.path.join(sourceFileDir, '../graphics/map/Entities.csv'))
        }

        #This is the graphics fo the map
        graphics = {
            'grass': import_folder(os.path.join(sourceFileDir, '../graphics/grass')), # These also get pass through the "import_folder" Function from support
            'objects': import_folder(os.path.join(sourceFileDir, '../graphics/objects'))
        }

        for style, layouts in layouts.items(): # This runs through the layouts
            for row_index, row in enumerate(layouts): # This runs through the rows of the map
                for col_index, col in enumerate(row): # This runs through the columns of the map
                    if col != '-1':
                        # Place the tile
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        
                        if style == 'boundary': # if the style is boundary make the tile place it in the obstacle sprites and make invisible
                            Tile((x,y),[self.obstacle_sprites],'invisible')
                        if style == 'grass': # if the style is grass make the tile with a random grass image and place it in the obstacle sprites
                            random_grass_image = choice(graphics['grass'])
                            Tile((x,y),[self.visible_sprites,self.obstacle_sprites,self.attackable_sprites],'grass',random_grass_image)
                        if style == 'object': # if the style is object make the tile image and place it in the obstacle sprites
                            surf = graphics['objects'][int(col)]
                            Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'objects',surf)
                        if style == 'entities':
                            if col == '394':
                                # Makes the player, place them at (x, y)
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites, self.create_attack,
                                    self.destroy_attack)
                            else: # Else the entity is a enemy
                                #If the id number equal then set it to the monster
                                if col == '390': monster_name = 'bamboo'
                                elif col == '391': monster_name = 'spirit'
                                elif col == '392': monster_name = 'raccoon'
                                else: monster_name = 'squid'
                                
                                # Makes the enemy at (x, y)
                                Enemy(
                                    monster_name,
                                    (x,y),
                                    [self.visible_sprites, self.attackable_sprites],
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.trigger_death_particles)

    # Create Attack Function (This gets pass through to the Player class)
    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_sprites, self.attack_sprites]) # Set the current weapon to the weapon
    
    # Destroy Attack Function (This gets pass through to the Player class)
    def destroy_attack(self):
        # If we have a weapon destroy it and set current weapon to none
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    # Player attack logic Function (Attack logic so that enemy take damge)
    def player_attack_logic(self):
        if self.attack_sprites: # If there are attack sprites
            for attack_sprite in self.attack_sprites: # Go through all the attack sprite
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False) # All attack sprites that have collide
                if collision_sprites: # If there are collision sprites
                    for target_sprite in collision_sprites: # Go through all the collison sprites
                        if target_sprite.sprite_type == 'grass':
                            for leaf in range(randint(3, 6)):
                                self.animation_player.create_grass_particles(target_sprite.rect.center - pygame.math.Vector2(0, 30), [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

            # Spawn Particles
            self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])

    def trigger_death_particles(self, pos, particles_type):
        self.animation_player.create_particles(particles_type, pos, self.visible_sprites)

    # Run Function (This runs when the game runs)
    def run(self):
        # Draw all visible sprites and update them
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        
        # Draw all the enemys
        self.visible_sprites.enemy_update(self.player)

        # Run the player attacking logic
        self.player_attack_logic()

        # Run UI display Function
        self.ui.display(self.player)

        # Sound
        if not self.running:
            self.main_sound = pygame.mixer.Sound(os.path.join(sourceFileDir, '../audio/main.ogg'))
            self.main_sound.set_volume(0.2)
            self.main_sound.play(loops = -1)
        self.running = True

# Custom Camera Group (For all visible sprites)
class YSortCameraGroup(pygame.sprite.Group):
    # Initialize Function (This is called when the class "YSortCameraGroup" is created)
    def __init__(self):
        # This Initialize some key Variable
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # Floor (This make the floor for the game)
        self.floor_surf = pygame.image.load(os.path.join(sourceFileDir, '../graphics/tilemap/ground.png')).convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (-64 * 8, -64 * 8)) # Set the position for the floor

    # Custom Draw Function (The draw the player so they can stand in front and behind)
    def custom_draw(self, player):
        # Get and sets the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Drawing Floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos) # Draws the floor with the floor offset

        # Goes throgh all sprite and Draws them with there offset position
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    # Enemy Update (So we can pass the player only to enemy and not all visible sprites)    
    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy'] # Get all the enemy spites
        for enemy in enemy_sprites: # Go through all the enemy and update them
            enemy.enemy_update(player)