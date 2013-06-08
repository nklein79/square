import pygame
import inventory
from engine.camera import Camera

class Character(pygame.sprite.Sprite):
    def __init__(self, color, initial_position):

        # All sprite classes should extend pygame.sprite.Sprite. This
        # gives you several important internal methods that you probably
        # don't need or want to write yourself. Even if you do rewrite
        # the internal methods, you should extend Sprite, so things like
        # isinstance(obj, pygame.sprite.Sprite) return true on it.
        pygame.sprite.Sprite.__init__(self)
      
        self.updateDelay = 10
      
        # Create the image that will be displayed and fill it with the
        # right color.
        #self.image = pygame.Surface([15, 15])
        #self.image.fill(color)
        
        self.images = pygame.image.load('images/player-sprite.png')
        self.images.convert_alpha()
        
        self.image = self.images.subsurface(pygame.Rect(0,0,30,32))
        
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position

        self.nextUpdateTime = 0 # update() hasn't been called yet.
        self.walkingTime = 0
        self.nextAltWalkingImageTime = 0
        self.walkingImageAlt = False
        
        # Start in the air
        self.onGround = False
        self.jumpspeed = 6
        self.gravity = 0.2
        self.maxFallingSpeed = 30
        
        self.speed = 3
        self.xdirection = 0 # Start standing still
        self.ydirection = self.maxFallingSpeed # Start falling
        
        self.equipment = inventory.Inventory(10) # equipped items
        self.inventory = inventory.Inventory(50) # inventory
        self.currentItem = None

    def jump(self):
        # Only jump if currently on the ground
        if self.onGround:
            self.onGround = False
            self.ydirection = -self.jumpspeed

    def update(self, gameengine, current_time):
        # Move our position up or down by one pixel
        if self.xdirection > 0: self.rect.left += self.speed
        elif self.xdirection < 0: self.rect.left -= self.speed
        
        # Get the tiles around the character to check for collisions.  We 
        # limit the check to the local character camera to limit unnecessary
        # collision detection on tiles not near the character
        localCameraWidth = gameengine.tileengine.tileSize * 5
        localCameraHeight = gameengine.tileengine.tileSize * 5
        localCamera = Camera(localCameraWidth,localCameraHeight, gameengine.camera.worldMapWidth, gameengine.camera.worldMapWidth)
        localCamera.update(gameengine.base, self)
        tiles = gameengine.tileengine.get_tiles_pixel(localCamera.window)
        
        # Do collision detection after moving horizontally
        if self.collide(tiles, True):
            self.xdirection = 0
        
        #if self.ydirection != 0: self.rect.top += 1*self.jumpspeed
        #elif self.ydirection < 0: self.rect.top -= 1*self.speed
        
        if not self.onGround:
            # Slow jumping speed due to gravity
            self.ydirection = self.ydirection + self.gravity
            
            # Check for max falling speed
            if self.ydirection > self.maxFallingSpeed: self.ydirection = self.maxFallingSpeed
            
            self.rect.top += self.ydirection
        
        # Do collision detection after moving vertically
        if self.collide(tiles, False):
            self.ydirection = 0
        
        # Check if the character is actually on the ground as it may have
        # moved off a cliff.  Only necessary if the character moved 
        # horizontally.
        
        # Temporary move down 1
        self.rect.bottom += 1 
        
        self.onGround = self.collide(tiles, False)
        
        # Undo the temporary move down 1 if not on the ground
        if not self.onGround: 
            self.rect.bottom -= 1
        
        # Update the sprite image
        self.update_image(current_time)
        
        # Update the current item
        if self.currentItem:
            self.currentItem.update(gameengine, self)
        


    def collide(self, entities=None, horizontal=True):
        """ Check if this character collides with any of the provided 
            entities in the horizontal or vertical directions.  
        """
        
        # Get all the entities that collide with the character
        collidedEntities = pygame.sprite.spritecollide(self, entities, False, pygame.sprite.collide_rect)
        
        for entity in collidedEntities:
            if horizontal and self.xdirection > 0:
                self.rect.right = entity.rect.left
                return True
            elif horizontal and self.xdirection < 0:
                self.rect.left = entity.rect.right
                return -1
            elif not horizontal and self.ydirection > 0:
                self.rect.bottom = entity.rect.top
                self.onGround = True
                return 1
            elif not horizontal and self.ydirection < 0:
                self.rect.top = entity.rect.bottom
                return -1
                
        # No collision detected
        return 0

    def update_image(self, current_time):
        """ Update the image based on the state
        """
        
        # If walking, alternate the walking image periodically to give the 
        # visual effect of walking 
        if self.xdirection != 0:
            if self.nextAltWalkingImageTime < current_time:
                self.walkingImageAlt = not self.walkingImageAlt            
                self.nextAltWalkingImageTime = current_time + self.updateDelay*30
    
        offset = 0
        if self.walkingImageAlt:
            offset = 30
    
        if self.xdirection > 0:
            self.image = self.images.subsurface(pygame.Rect(30+offset,0,30,32))
        elif self.xdirection < 0:
            self.image = self.images.subsurface(pygame.Rect(30+offset,0,30,32))
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = self.images.subsurface(pygame.Rect(0,0,30,32))
                       

