# Third-party
import pygame
from pygame.locals import *
from time import time
import engine.gamestate
from engine.gameengine import GameEngine

# Resolution of the window (what the user sees)
WIN_WIDTH = 1024
WIN_HEIGHT = 768

# Size of the game tiles / grid
TILE_SIZE = 32

# World map size (number of tiles, not pixels)
WORLD_MAP_SIZE = (100, 100)
WORLD_MAP_PIXEL_SIZE = (WORLD_MAP_SIZE[0]*TILE_SIZE, WORLD_MAP_SIZE[1]*TILE_SIZE)

# Refer to pygame documentation for various display mode flags


# Color depth (0 means automatically determine this)
DEPTH = 0

# Frames Per Second limiter
FPS_LIMIT = 50
SKIP_TICKS = 1000 / FPS_LIMIT
MAX_FRAMESKIP = 10

def main():
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT), engine.gamestate.FLAGS, DEPTH)
    pygame.display.set_caption("Square!")
    
    # Initialize the game engine
    gameengine = GameEngine(WIN_WIDTH, WIN_HEIGHT)
    
    # Initialize the camera
    camera = gameengine.camera
    
    # Misc initialization
    arialFnt = pygame.font.SysFont('Arial', 16)
    
    charUpdateTime = 0
    tileTime = 0
    characterTime = 0
    
    nextGameTick = pygame.time.get_ticks()
    
    # Loop until the user exits the game
    while True: 
        gameengine.currentState.handle_events(pygame.event.get(), gameengine)
        
        inMenu = gameengine.currentState == gameengine.menuState
        inInventory = gameengine.currentState == gameengine.inventoryState
        
        # Display only the camera view of the world map
        winSurface = camera.update(gameengine.base, gameengine.player)                
        
        if not inMenu:
            # Control how fast the game updates, which is different from how
            # fast the display updates.  Refer to the following link for a
            # good article on the game loop.
            # http://www.koonsolo.com/news/dewitters-gameloop/
            
            loops = 0
            while pygame.time.get_ticks() > nextGameTick and loops < MAX_FRAMESKIP:
                # Update the characters on the world map
                start = time()        
                gameengine.characters.update(gameengine, pygame.time.get_ticks())
                end = time()
                charUpdateTime = end - start
                
                # Update the projectiles
                gameengine.projectiles.update(gameengine, pygame.time.get_ticks())
                
                nextGameTick += SKIP_TICKS
                loops += 1
        
        # The actual visual display consists of the following layers from background to foreground
        # 1. Background
        # 2. Tiles (from tile engine)
        # 3. Entities (player player, mobs, npc's, etc...)
        # 4. Menu
        
        # Blit the background (only the camera view  
        screen.blit(winSurface, (0,0))
        screen.blit(gameengine.background, (0,0))
        
        # Blit the tiles
        start = time()
        #for tile in tiles:
        #    screen.blit(tile.image, camera.apply(tile))
        tileWindowSurface = gameengine.tileengine.tileWorldSurface.subsurface(gameengine.camera.window)
        screen.blit(tileWindowSurface, (0,0))
        end = time()
        tileTime = end-start
        
        # Now blit the characters on the screen adjusting for camera location
        # Also blit the player's item, if equipped
        start = time()
        for character in gameengine.characters:
            screen.blit(character.image, camera.apply(character))
            
            if character.currentItem and character.currentItem.image:
                screen.blit(character.currentItem.image, camera.apply(character.currentItem))
        end = time()
        characterTime = end-start
        
        # Blit all the projectiles
        for projectile in gameengine.projectiles:
            screen.blit(projectile.image, camera.apply(projectile))
        
        # Display the inventory
        if inInventory:
            gameengine.inventoryState.displayInventory(screen)
        
        # Display the menu
        if inMenu:
            gameengine.menuState.displayMenu(screen)
            
        # Debugging info
        if gameengine.debugging:
            screen.blit(arialFnt.render('left: ' +  str(gameengine.player.rect.left) + ', top: ' + str(gameengine.player.rect.top), True, (255,255,255)), (5,5))
            screen.blit(arialFnt.render('FPS: ' +  str(gameengine.clock.get_fps()), True, (255,255,255)), (5,25))
            screen.blit(arialFnt.render('Character Update Time: %.4f' % charUpdateTime, True, (255,255,255)), (5,45))
            screen.blit(arialFnt.render('Character Time: %.4f' % characterTime, True, (255,255,255)), (5,65))
            screen.blit(arialFnt.render('Tile Time: %.4f' % tileTime, True, (255,255,255)), (5,85))
            screen.blit(arialFnt.render('Characters: %.0f, Projectiles: %.0f' % (len(gameengine.characters), len(gameengine.projectiles)), True, (255,255,255)), (5,105))
            
        # Actually update the visible screen
        pygame.display.update()
        
        if not inMenu:
            # Tick the game clock limiting to 30 frames per second
            gameengine.clock.tick(FPS_LIMIT)

if __name__ == "__main__":
    main()
