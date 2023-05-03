'''
This is the Main file, the file you run to play the game
This file contains the main Game class and the code to run it
'''

import pygame, sys # Import pygame and system
from settings import * # Import all from settings (Another python script)
from level import Level # level class from Level (Another python script)

# Main game class
class Game:
    # Initialize Function (This is called when the class "Game" is created)
    def __init__(self):
        pygame.init() # Run pygame init function
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH)) # Set the screen size
        pygame.display.set_caption('RPG') # Set the windows name to "RPG"
        self.clock = pygame.time.Clock() # Set the clock variable to pygame's clock

        self.level = Level() # Set the level to the level class
    
    # Run Function (This is called when the game runs)
    def run(self):
        while True: # (This loop is forever until broken)
            for event in pygame.event.get(): # loops through all pygame's event
                if event.type == pygame.QUIT: # If the event type is set to quit then quit the game
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill('black') # Fills the backgound to black
            self.level.run() # Runs the level class Run Function
            pygame.display.update() # Updates the screen
            self.clock.tick(FPS) # Sets the clock tick rate to FPS (60)

# If the name of the file = main then run the game
if __name__ == '__main__':
    game = Game()
    game.run()