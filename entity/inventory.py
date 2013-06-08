import pygame

class Inventory(object):
    """ Inventory of items
    """
    
    def __init__(self, size=50):
        self.size = size
        self.items=[InventoryItem(x, None) for x in range(size)]
        
    def add(self, item, slot):
        if self.items[slot].item != None:
            raise Exception("Already an item in this slot")
        
        self.items[slot].item = item
        
        return item
    
    def remove(self, slot):
        item = self.items[slot].item
        self.items[slot].item = None
        return item
    
    def get(self, slot):
        return self.items[slot].item
    
    def display(self, screen):
        for item in self.items:
            item.display(screen)
    
    def do_primary(self, position, gameengine):
        return self.collide(position)
    
    def collide(self, position):
        """ Check if this position collides with any inventory item.
            Basically if the user clicked on an inventory item  
        """
        
        # Get all the entities that collide with the character
        for item in self.items:
            if item.rect.collidepoint(position):
                item.image.fill((0,200,0))
                return True
        
        # Did not collide
        return False
        
class InventoryItem(pygame.sprite.Sprite):
    """ Item in an inventory.  Somewhat confusing as this is not an Item
        but contains an Item.  This also handles the imaging when displaying
        the inventory and displaying this inventory item
    """
    
    def __init__(self, index, item):
        pygame.sprite.Sprite.__init__(self)
        
        self.index = index
        self.item = item
        self.size = (50,50)
        self.padding = 10
        self.horizontalCount = 10
        
        # Initialize slot image
        self.image = pygame.Surface(self.size)
        self.image.fill((0,0,200))
        self.image.set_alpha(160)
        self.rect = self.image.get_rect()
        
        left = index / self.horizontalCount * (self.size[0] + self.padding) + self.padding
        top = index % self.horizontalCount * (self.size[1] + self.padding) + self.padding
        self.rect.topleft = (top, left) 
        
    def display(self, screen):
        screen.blit(self.image, self.rect.topleft)
        
        if self.item:
            pass
    