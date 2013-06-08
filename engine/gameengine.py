import pygame
from pygame.locals import *
from pygame import Surface

from engine.camera import Camera
from engine.tileengine import TileEngine
from entity.character import Character
from entity import item
import gamestate

# Size of the game tiles / grid
TILE_SIZE = 32

# World map size (number of tiles, not pixels)
WORLD_MAP_SIZE = (100, 100)
WORLD_MAP_PIXEL_SIZE = (WORLD_MAP_SIZE[0]*TILE_SIZE, WORLD_MAP_SIZE[1]*TILE_SIZE)

# Name of the world map file
WORLD_MAP_FILE = "images/worldmap1.png"

class GameEngine(object):
    
    def __init__(self, initialWidth, initialHeight):
        
        self.debugging = True
            
        self.winWidth = initialWidth
        self.winHeight = initialHeight
            
        self.clock = pygame.time.Clock()
        
        # Initialize the camera
        self.camera = Camera(self.winWidth, self.winHeight, WORLD_MAP_PIXEL_SIZE[0], WORLD_MAP_PIXEL_SIZE[1])
        
        # Load the base (world surface)
        self.base = self.load_base()
        
        # Load the background
        self.background = self.load_background()
        
        # Initialize the tile engine
        self.tileengine = TileEngine.fromfilename(WORLD_MAP_FILE, TILE_SIZE) 
                
        # Initialize the player sprites
        self.characters = pygame.sprite.Group()
        self.player = Character([255, 0, 0], (1600,1000))
        self.characters.add(self.player)
        
        self.player.equipment.add(item.TileTool(), 1)
        self.player.currentItem = self.player.equipment.get(1)
        self.player.equipment.add(item.Weapon(), 2)
        self.player.equipment.add(item.EnemyTool(), 3)
        
        # Initialize projectiles
        self.projectiles = pygame.sprite.Group()
        
        # Initialize different states of the game
        self.playState = gamestate.PlayState()
        self.menuState = gamestate.MenuState()
        self.inventoryState = gamestate.InventoryState(self.player.inventory)
        self.currentState = self.playState
    
    def load_background(self):
        """ Load the background for the world
        """
        background = pygame.image.load('images/background.png')
        background.convert()
            
        return background

    def load_base(self):
        """ Load the base (back surface) for the world
        """
        width,height = (WORLD_MAP_SIZE[0]*TILE_SIZE,WORLD_MAP_SIZE[1]*TILE_SIZE)
        
        image = Surface((TILE_SIZE, TILE_SIZE))
        image.convert()
        
        base = pygame.Surface((width,height))
        base.convert()
        
        # Fill in sky with blue
        base.fill(Color(0,0,255), Rect(0, 0, width, height/2))
        
        # Fill in ground with brown
        base.fill(Color("#573B0C"), Rect(0, height/2, width, height/2))
            
        return base
