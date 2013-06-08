import pygame
import math
from engine.tileengine import Tile
from utilities.util import Util
from entity.projectile import Projectile
from character import Character

class Item(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
    
    def do_primary(self, worldLocation, gameengine):
        pass
    
    def do_secondary(self, worldLocation, gameengine):
        pass
    
    def update(self, gameengine, character):
        pass
    
class TileTool(Item):
    """ Tool item whose primary action is placing tiles and secondary action
        is removing tiles
    """ 
    
    def __init__(self):
        super(TileTool, self).__init__()
    
    def do_primary(self, worldLocation, gameengine):
        """ Place a tile at the provided location
        """
        
        # Get the tile at the clicked position if one exists
        clickedTile = gameengine.tileengine.get_tile_pixel(worldLocation)
        
        # Place a tile at this location if one is not already there   
        if clickedTile == None:
            gameengine.tileengine.place_tile(gameengine.tileengine.pixel_to_tile(worldLocation), Tile(None,(0,0,0)))
    
    def do_secondary(self, worldLocation, gameengine):
        """ Remove a tile at the provided location
        """
        
        # Get the tile at the clicked position if one exists
        clickedTile = gameengine.tileengine.get_tile_pixel(worldLocation)
        
        # Remove tile at this location if one is located there
        if clickedTile != None:
            gameengine.tileengine.remove_tile(gameengine.tileengine.pixel_to_tile(worldLocation), gameengine.background)

class EnemyTool(Item):
    """ Tool item whose primary action is placing new enemies.  This is for 
        testing purposes.
    """ 
    
    def __init__(self):
        super(EnemyTool, self).__init__()
    
    def do_primary(self, worldLocation, gameengine):
        """ Place an enemy at the location
        """
        
        # Create a new character
        character = Character((0,0,0), worldLocation)
        gameengine.characters.add(character)
        
class Weapon(Item):
    
    def __init__(self):
        super(Weapon, self).__init__()
        
        loadedImage = pygame.image.load('images/weapon-sprite.png')
        loadedImage.convert_alpha()
        
        width, height = loadedImage.get_size()
        
        # Adjust the original image so that we can easily rotate the time 
        # around the entity holding this weapon
        adjustedImage = pygame.Surface((width*2, height), pygame.SRCALPHA, 32)
        adjustedImage.convert_alpha()
        adjustedImage.fill((0,0,0,0))
        adjustedImage.blit(loadedImage, (width, 0))
        
        self.originalImage = adjustedImage
        
        self.image = self.originalImage;
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)
        
    def do_primary(self, worldLocation, gameengine):
        angle,flip = self.get_cursor_angle(gameengine, gameengine.player)
        
        if flip:
            angle = -(angle + 180)
        
        projectile = Projectile(gameengine, angle, 10, gameengine.player.rect.center)
        
        gameengine.projectiles.add(projectile)
    
    def do_secondary(self, worldLocation, gameengine):
        pass    

    def get_cursor_angle(self, gameengine, character):
        playerLocation = gameengine.camera.apply(character).center
        mousePosition = pygame.mouse.get_pos();
        
        angle,flip = Util.get_rotate_angle(playerLocation, mousePosition)
        
        return (angle, flip)

    def update(self, gameengine, character):
        # Rotate the image to follow the mouse cursor and move to attach to the 
        # player
        angle,flip = self.get_cursor_angle(gameengine, character)
        
        # Always start using the original image as transforming an already
        # transformed image will distort the image
        self.image = self.originalImage
        self.image = pygame.transform.rotate(self.image, angle)
        
        if flip:
            self.image = pygame.transform.flip(self.image, True, False)
        
        # Rotate resizes the image so we have to center it at the original
        # location
        self.rect = self.image.get_rect(center=character.rect.center)
