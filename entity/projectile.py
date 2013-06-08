import pygame
import math
from engine.camera import Camera

class Projectile(pygame.sprite.Sprite):
    """ Any projectile
    """ 
    def __init__(self, gameengine, angle, speed, initial_position):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.angle = angle
        self.speed = speed
        
        self.image = pygame.Surface((5,5))
        self.image.fill((255,255,255))
        self.image.set_alpha(255)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position
        
        gameengine.projectiles.add(self)
        
    def get_velocity(self, angle, speed):
        xVelocity = float(speed) * math.cos(math.radians(angle))
        yVelocity = float(speed) * math.sin(math.radians(angle))
        
        return (xVelocity, yVelocity)
    
    def update(self, gameengine, current_time):        
        xVelocity, yVelocity = self.get_velocity(self.angle, self.speed)
        
        self.rect.left += xVelocity
        self.rect.top -= yVelocity
        
        # Check if the projectile went outside the game map.  If so, remove
        # it.
        if not self.rect.colliderect(gameengine.base.get_rect()):
            gameengine.projectiles.remove(self)
        
        # Check if the projectile collided with any characters
        collided = self.collide(gameengine.characters, [gameengine.player])
        
        if collided:
            # Projectile collided with a player
            gameengine.projectiles.remove(self)
        
        else:
            # Check if the projectile collided with any tiles
            localCameraWidth = gameengine.tileengine.tileSize * 5
            localCameraHeight = gameengine.tileengine.tileSize * 5
            localCamera = Camera(localCameraWidth,localCameraHeight, gameengine.camera.worldMapWidth, gameengine.camera.worldMapWidth)
            localCamera.update(gameengine.base, self)
            tiles = gameengine.tileengine.get_tiles_pixel(localCamera.window)
            
            #tiles = gameengine.tileengine.get_tiles_pixel(gameengine.camera.window)
            collided = self.collide(tiles)
            
            if collided:
                gameengine.projectiles.remove(self)
            
    def collide(self, entities=None, ignoreList=None):
        """ Check if this projectile collides with any of the provided 
            entities in the horizontal or vertical directions.  
        """
        
        # Get all the entities that collide with the player
        collidedEntities = pygame.sprite.spritecollide(self, entities, False, pygame.sprite.collide_rect)
        
        for entity in collidedEntities:
            # Collision detected
            if ignoreList and entity in ignoreList:
                continue
            else:  
                return True
                
        # No collision detected
        return False