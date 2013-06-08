import sys
import pygame
from pygame.locals import *
from menu.menu import MainMenu

FLAGS = pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF

class GameState(object):
    def __init__(self):
        pass
    
    def handle_events(self, events, gameengine):
        # Process all the events since last time we processed
        for event in events:
            self.handle_event(event, gameengine)
    
    def handle_event(self, event, gameengine):
        if event.type == KEYDOWN:
            if event.key == K_BACKQUOTE:
                gameengine.debugging = not gameengine.debugging
    
class PlayState(GameState):
    def __init__(self):
        super(PlayState, self).__init__()
        
    def handle_event(self, event, gameengine):
        if event.type == QUIT:
            # Quit event
            pygame.quit()
            sys.exit()
        elif event.type == VIDEORESIZE:
            # User resized the game window so reset the screen surface and camera
            gameengine.winWidth = event.w
            gameengine.winHeight = event.h 
            
            gameengine.camera.window = Rect(gameengine.camera.window.left, gameengine.camera.window.top, event.w, event.h)
            
            pygame.display.set_mode(event.size, FLAGS)
                            
        elif event.type == KEYDOWN:
            if event.key == K_a:
                gameengine.player.xdirection = -1;
            elif event.key == K_d:
                gameengine.player.xdirection = 1;
            elif event.key == K_SPACE:
                gameengine.player.jump()
            elif event.key == K_PLUS or event.key == K_KP_PLUS:
                gameengine.player.speed = min(10,gameengine.player.speed + 1)
            elif event.key == K_MINUS or event.key == K_KP_MINUS:
                gameengine.player.speed = max(1,gameengine.player.speed - 1)
            elif event.key >= K_0 and event.key <= K_9:
                # Switch equipped item
                selectedItem = gameengine.player.equipment.get(event.key-K_0)
                if selectedItem:
                    gameengine.player.currentItem = selectedItem
            elif event.key == K_ESCAPE:
                # Switch to menu state
                gameengine.currentState = gameengine.menuState
            elif event.key == K_TAB:
                # Switch to inventory state
                gameengine.currentState = gameengine.inventoryState
            else:
                super(PlayState, self).handle_event(event, gameengine)

        elif event.type == KEYUP:
            if event.key == K_a or event.key == K_d:
                gameengine.player.xdirection = 0;
            elif event.type == K_d:
                gameengine.player.xdirection = 0;
        elif event.type == MOUSEBUTTONDOWN:
            # Translate the mouse click location into the world map 
            # location
            worldPosition = gameengine.camera.window_to_map(event.pos)
            
            if event.button == 1:   # Left mouse click
                gameengine.player.currentItem.do_primary(worldPosition,gameengine)
            elif event.button == 3: # Right mouse click
                gameengine.player.currentItem.do_secondary(worldPosition,gameengine)

class InventoryState(PlayState):
    """ Game state where an inventory is displayed
    """
    
    def __init__(self, inventory):
        super(PlayState, self).__init__()
        
        self.inventory = inventory
    
    def handle_event(self, event, gameengine):
        if event.type == KEYDOWN:
            if event.key == K_TAB:
                # Switch to playing state
                gameengine.currentState = gameengine.playState
            else:
                # Didn't handle this event, let the super class
                # try and handle it
                super(InventoryState, self).handle_event(event, gameengine)
        elif event.type == MOUSEBUTTONDOWN:
            # Translate the mouse click location into the world map 
            # location
            if event.button == 1:   # Left mouse click
                collision = self.inventory.do_primary(event.pos, gameengine)
                
                if not collision:
                    # Didn't handle this event, let the super class
                    # try and handle it
                    super(InventoryState, self).handle_event(event, gameengine)
            else:
                super(InventoryState, self).handle_event(event, gameengine)
        else:
            # Didn't handle this event, let the super class
            # try and handle it
            super(InventoryState, self).handle_event(event, gameengine)
    
    def displayInventory(self, screen):
        self.inventory.display(screen)
    
class MenuState(GameState):
    """ Game state where the menu is displayed
    """
    
    def __init__(self):
        super(MenuState, self).__init__()
        self.menu = MainMenu()
         
    def handle_event(self, event, gameengine):
        if event.type == QUIT:
            # Quit event
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                # Close the menu and switch back to playing state
                gameengine.currentState = gameengine.playState
                
        elif event.type == MOUSEBUTTONDOWN:
            # Check if the mouse click position collides with any menu
            # item, meaning the user clicked a menu item
            for menuItem in self.menu.menuItems:
                if menuItem.rect.collidepoint(event.pos):
                    menuItem.action()
             
    def displayMenu(self, screen):
        self.menu.display(screen)
