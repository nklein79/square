import pygame

class TileEngine(object):
    """ Tile engine that works with the tile layer of the game
        http://en.wikipedia.org/wiki/Tile_engine
    """

    def __init__(self, worldSize=(0,0), tileSize=32):
        self.tileSize=tileSize
        self.tiles=[[None for _ in range(worldSize[0])] for _ in range(worldSize[1])]
        self.tileWorldSurface = None 
        
        
    @classmethod
    def fromfilename(cls, filename, tileSize=32):
        """ Create a new TileEngine using the provided file as the tile map. 
            The file is expected to be an image file where the pixel color maps 
            to the tile type at that location.
        """
        
        surface = pygame.image.load(filename)
        width, height = surface.get_size()
        
        engine = cls((width,height), tileSize)
        
        engine.tileWorldSurface = pygame.Surface((width*tileSize, height*tileSize), pygame.SRCALPHA, 32)
        engine.tileWorldSurface.convert_alpha()
        
        for x in range(0,width):
            for y in range(0,height):
                color = surface.get_at((x,y))
                value = color.r
                
                if value == 0:
                    tile = Tile("images/rock-texture.png")
                    engine.place_tile((x,y), tile)

        return engine
    
    def get_tile(self, location):
        """ Get the tile at the specified tile location
        """
        return self.tiles[location[0]][location[1]]
    
    def get_tile_pixel(self, location):
        """ Get the tile at the specified world pixel location
        """
        tileLocation = self.pixel_to_tile(location)
        return self.get_tile(tileLocation)
    
    def pixel_to_tile(self, location):
        """ Get the tile location, (x,y) tuple, given the world pixel location.
        """  
        return (location[0]/self.tileSize, location[1]/self.tileSize)   
    
    def tile_to_pixel(self, location):
        """ Get the world pixel location, (x,y) tuple, given the tile location.
        """  
        return (location[0]*self.tileSize, location[1]*self.tileSize)  
    
    def place_tile(self, location, tile):
        """ Place the given tile at the given tile location. Returns the tile 
            that was placed.
        """
        
        # Set the tile's internal location
        tile.rect.topleft = self.tile_to_pixel((location[0],location[1]))
        
        self.tiles[location[0]][location[1]] = tile
        
        # Update the world tile surface
        self.tileWorldSurface.blit(tile.image, (location[0]*self.tileSize,location[1]*self.tileSize))
        
        return tile
    
    def remove_tile(self, location, background):
        """ Remove the tile at the given tile location. Returns the removed 
            tile or None if no tile was found at that location.
        """
        tile = self.tiles[location[0]][location[1]]
        self.tiles[location[0]][location[1]] = None
        
        # Update the world tile surface by filling the removed tile space with
        # transparency  
        tileSubsurface = self.tileWorldSurface.subsurface(pygame.Rect(location[0]*self.tileSize,location[1]*self.tileSize, self.tileSize, self.tileSize))
        tileSubsurface.fill((0,0,0,0))
        
        return tile

    def get_tiles(self, window=(0,0,0,0)):
        """ Get all the tiles in the specified window.  The window is tile size. 
        """
        results = []
        
        # Loop through all the tiles in the window
        for x in range(window[0],window[0]+window[2]+1):
            for y in range(window[1],window[1]+window[3]+1):
                tile = self.tiles[x][y]
                
                if tile == None:
                    continue
                else:
                    results.append(tile)
                    
        return results
    
    def get_tiles_pixel(self, window=(0,0,0,0)):
        """ Get all the tiles in the specified window.  The window is pixel 
            size. 
        """
        window = tuple(x/self.tileSize for x in window)
        return self.get_tiles(window)
    
    def get_surface_tiles(self, window=(0,0,0,0)):
        """ Get all surface tiles in the specified window.  The window is tile 
            size. Surface tiles are tiles that have at least one empty adjacent
            tile. 
        """
        results = []
        
        # Loop through all the tiles in the window
        for x in range(window[0],window[0]+window[2]):
            for y in range(window[1],window[1]+window[3]):
                tile = self.tiles[x][y]
                
                if tile == None:
                    continue
                
                # Check the adjacent tiles to determine if this is a 
                # surface tile
                # Locations to check (up, down, left and right) constrained
                # to within the tile map
                checks = [(x,max(0,y-1)),
                          (x,min(len(self.tiles[x])-1,y+1)),
                          (max(0,x-1),y),
                          (min(len(self.tiles)-1,x+1),y)]
                
                for check in checks:
                    checkTile = self.get_tile((check[0],check[1]))
                    if(checkTile == None):
                        # Found adjacent empty tile, this is a surface tile
                        results.append(tile)
                        break
                    
        return results
    

class Tile(pygame.sprite.Sprite):
    def __init__(self, image=None, color=(128, 128, 128), initial_position=(0,0), size=(32,32)):
        # All sprite classes should extend pygame.sprite.Sprite. This
        # gives you several important internal methods that you probably
        # don't need or want to write yourself. Even if you do rewrite
        # the internal methods, you should extend Sprite, so things like
        # isinstance(obj, pygame.sprite.Sprite) return true on it.
        pygame.sprite.Sprite.__init__(self)
      
        if image:
            self.image = pygame.image.load(image)
            self.image.convert()
            self.image.set_alpha(255)
        else:
            self.image = pygame.Surface(size)
            self.image.fill(color)
            self.image.set_alpha(255)
        
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.topleft = initial_position

    def update(self, current_time):
        pass
