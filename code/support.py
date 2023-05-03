'''
This is the Support script, this is where the "import_csv_layout" and "import_folder" are
They import csv files and images so that they are readable
'''

import pygame # Import pygame
from csv import reader # Import reader form csv
from os import walk # Import walk form os (Operating system)

# Import csv layout Function
def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map: # Open the level map
        layout = reader(level_map, delimiter = ',') # Get the layout
        for row in layout: # Go through all the rows
            terrain_map.append(list(row)) # Add the rows to the terrain map
        return terrain_map # Return the terrain map

# Import folder Function
def import_folder(path):
    surface_list = []

    for _,__,img_files in walk(path): # Go through image files in path
        for image in img_files: # Go through images in image files
            full_path = path + '/' + image # Get the path of the image
            image_surf = pygame.image.load(full_path).convert_alpha() # load the image
            surface_list.append(image_surf) # Add the image to the surface list

    return surface_list # Return the surface list