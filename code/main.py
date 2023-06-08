'''
This is the Main file, the file you run to play the game
This file contains the main Game class and the code to run it
'''

import pygame, sys # Import pygame and system
from settings import * # Import all from settings (Another python script)
from level import Level # level class from Level (Another python script)
from main_menu import Main_Menu
from how_to_play import How_To_Play
import os # Import os (Operating system)

# Get the absolute path for this directory
sourceFileDir = os.path.dirname(os.path.abspath(__file__))

# Main game class
class Game:
    # Initialize Function (This is called when the class "Game" is created)
    def __init__(self):
        pygame.init() # Run pygame init function
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH)) # Set the screen size
        pygame.display.set_caption('RPG') # Set the windows name to "RPG"
        self.clock = pygame.time.Clock() # Set the clock variable to pygame's clock

        self.level = Level() # Set the level to the level class
        self.main_menu = Main_Menu() # Set the main menu class
        self.how_to_play = How_To_Play() # Set the main menu class

        self.isRunning = 0 # Set the game to not running

        # Sound
        self.main_menu_sound = pygame.mixer.Sound(os.path.join(sourceFileDir, '../audio/main_menu.ogg'))
        self.main_menu_sound.set_volume(0.2)
        self.main_menu_sound.play(loops = -1)

        pygame.mouse.set_visible(False) # Set the mouse to invisible
    
    # Run Function (This is called when the game runs)
    def run(self):
        while True: # (This loop is forever until broken)
            for event in pygame.event.get(): # loops through all pygame's event
                if event.type == pygame.QUIT: # If the event type is set to quit then quit the game
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:  
                    if event.key == pygame.K_SPACE and self.isRunning != 2:
                        self.isRunning += 1

            self.screen.fill('black') # Fills the backgound to black
            
            if self.isRunning == 2:
                self.main_menu_sound.stop()
                self.level.run() # Runs the level class Run Function
            elif self.isRunning == 1:
                self.how_to_play.run()
            else:
                self.main_menu.run()

            pygame.display.update() # Updates the screen
            self.clock.tick(FPS) # Sets the clock tick rate to FPS (60)

# If the name of the file = main then run the game
if __name__ == '__main__':
    game = Game()
    game.run()