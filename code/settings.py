'''
This is the settings script, this is where all the settings are
That all other file use to access the settings
'''

import os # Import os (Operating system)

# Get the absolute path for this directory
sourceFileDir = os.path.dirname(os.path.abspath(__file__))

# Screen Settings (Heigth and Width)
WIDTH = 1280
HEIGTH = 720
FPS = 60 # This is how many Frames per second is displayed on the screen

# Tile Settings (This is the size of every tile)
TILESIZE = 64

HITBOX_OFFSET = {
    'player': -26,
    'objects': -40,
    'grass': -10,
    'invisible': 0
}

# UI (User interface)
BAR_HEIGHT = 20 # Height of the bars
HEALTH_BAR_WIDTH = 200 # Health bar width
ENERGY_BAR_WIDTH = 140 # Energy bar width
ITEM_BOX_SIZE = 80 # Item box size
FONT = os.path.join(sourceFileDir, '../graphics/font/joystix.ttf')

# General Colors
UI_BG_COLOR = '#222222' # BG color
UI_BORDER_COLOR = '#111111' # Border color

# UI Colors
HEALTH_COLOR = 'red' # Health color
ENERGY_COLOR = 'blue' # Energy color
UI_BORDER_COLOR_ACTIVE = 'gold' # Border color active

# Weapons Settings (This contains all the weapon data in a list of lists like cooldown, famage and the graphic for the weapons)
weapon_data = {
	'sword': {'cooldown': 100, 'damage': 15,'graphic': os.path.join(sourceFileDir, '../graphics/weapons/sword/full.png')},
	'lance': {'cooldown': 400, 'damage': 30,'graphic': os.path.join(sourceFileDir, '../graphics/weapons/lance/full.png')},
	'axe': {'cooldown': 300, 'damage': 20, 'graphic': os.path.join(sourceFileDir, '../graphics/weapons/axe/full.png')},
	'rapier':{'cooldown': 50, 'damage': 8, 'graphic': os.path.join(sourceFileDir, '../graphics/weapons/rapier/full.png')},
	'sai':{'cooldown': 80, 'damage': 10, 'graphic': os.path.join(sourceFileDir, '../graphics/weapons/sai/full.png')}}

# Enemy (This contains all the enemy data in a list of lists)
monster_data = {
	'squid': {'health': 100,'damage':20,'attack_type': 'slash', 'attack_sound': os.path.join(sourceFileDir, '../audio/attack/slash.wav'), 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360},
	'raccoon': {'health': 300,'damage':40,'attack_type': 'claw',  'attack_sound': os.path.join(sourceFileDir, '../audio/attack/claw.wav'),'speed': 2, 'resistance': 3, 'attack_radius': 120, 'notice_radius': 400},
	'spirit': {'health': 100,'damage':8,'attack_type': 'thunder', 'attack_sound': os.path.join(sourceFileDir, '../audio/attack/fireball.wav'), 'speed': 4, 'resistance': 3, 'attack_radius': 60, 'notice_radius': 350},
	'bamboo': {'health': 70,'damage':6,'attack_type': 'leaf_attack', 'attack_sound': os.path.join(sourceFileDir, '../audio/attack/slash.wav'), 'speed': 3, 'resistance': 3, 'attack_radius': 50, 'notice_radius': 300}}