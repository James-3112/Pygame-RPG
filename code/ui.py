'''
This is the UI script, this is where everything to do with the UI is done
Such as Health bar, Energy bar, and weapon selection box
'''

import pygame
from settings import *

class UI:
    # Initialize Function (This is called when the class "UI" is created)
    def __init__(self):
        # General
        self.display_surface = pygame.display.get_surface() # Get the screen

        # Bar Setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT) # Make the health bar
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT) #make the energy bar

        # Convert weapon dictionary (Get the weapon dictionary and makes it into a list)
        self.weapon_graphics = []
        for weapon in weapon_data.values(): # Goes through all the weapon data
            path = weapon['graphic'] # Get the graphics
            weapon = pygame.image.load(path).convert_alpha() # Load the weapon with pygame
            self.weapon_graphics.append(weapon) # Add the weapon to the weapons graphics list
    
    # Show Bar Function (Darws the bars on the screen)
    def show_bar(self, current, max_amount, bg_rect, color):
        # Darw backgound of bar
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # Converting stat to pixels
        ratio = current / max_amount # Get the ratio of current to max health
        current_width = bg_rect.width * ratio # To get tje width you times it by the ratio
        current_rect = bg_rect.copy() # Copy the backgound rect (Rectangle)
        current_rect.width = current_width # Set the width

        # Darwing the bar
        pygame.draw.rect(self.display_surface, color, current_rect) # Darwing the bar
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3) # Darwing the border
    
    # Selection Box Function (Creates the selection box backgound for the weapons)
    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE) # Makes the rect (Rectangle)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect) # Draws it

        # Selection Box Border
        if has_switched: # If has switched make the border a different color
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else: # Else keep it the same
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        return bg_rect # Return the Backgound Rectangle

    # Weapon Overlay (Creates the weapons image for the selection box)
    def weapon_overlay(self, weapon_index, has_switched):
        bg_rect = self.selection_box(10, 630, has_switched) # Draw Backgound for weapon selection box

        weapon_surf = self.weapon_graphics[weapon_index] # Get the weapon image
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center) # Make the rect (Rectangle) for the image 

        self.display_surface.blit(weapon_surf, weapon_rect) # Draw the weapon image

    # Display (This get run by the level class)
    def display(self, player):
        # Display the health and energy bar
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)

        # Display the weapon overlay
        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)