import pygame
from pygame.locals import *

class Menu(pygame.sprite.Sprite):
    """ Game menu
    """
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.menuItems = []

    def display(self, screen):
        for menuItem in self.menuItems:
            menuItem.display(screen)

class MainMenu(Menu):
    """ Main menu
    """
    
    def __init__(self):
        super(MainMenu, self).__init__()
        
        self.postion = (0,0)
        
        controlsAction = lambda: 1+1 
        controlsMenuItem = MenuItem("Controls", controlsAction)
        
        quitAction = lambda: pygame.event.post(pygame.event.Event(QUIT)) 
        quitMenuItem = MenuItem("Quit", quitAction)
        
        self.menuItems.append(controlsMenuItem)
        self.menuItems.append(quitMenuItem)

    def display(self, screen):
        index = 0
        for menuItem in self.menuItems:
            position = (screen.get_rect().center[0], screen.get_rect().center[1] + (index * 50))
            menuItem.display(screen, position)
            index += 1

class MenuItem(Menu):
    """ Game menu item
    """
    
    def __init__(self, text, action):
        super(MenuItem, self).__init__()
        
        self.width = 200
        self.height = 40
        
        self.menuFnt = pygame.font.SysFont('Arial', 32, True)
        self.action = action
        
        self.image = pygame.Surface((self.width,self.height), pygame.SRCALPHA)
        self.image.fill((0,0,0,0))

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)
        
        self.image.blit(self.menuFnt.render(text, True, (255,255,255)), (0,0))
        
    def select(self):
        self.action()

    def update(self, current_time, entities=None):
        pass
    
    def display(self, screen, position=(0,0)):
        self.rect.topleft = position
        screen.blit(self.image, self.rect.topleft)
