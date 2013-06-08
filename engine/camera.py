from pygame.locals import Rect
        
class Camera(object):
    def __init__(self, width, height, worldMapWidth, worldMapHeight):
        self.window = Rect(0, 0, width, height)
        self.worldMapWidth = worldMapWidth
        self.worldMapHeight = worldMapHeight

    def window_to_map(self, location):
        """ Translate the window pixel location in the world map pixel location 
        """
        return (location[0] + self.window.left, location[1] + self.window.top)

    def apply(self, target):
        """ Project the target on the world map onto the location on the 
            camera window.  In other words, get a Rect for where the target
            is relative to the window.
        """
        return target.rect.move(-self.window.left, -self.window.top)

    def update(self, surface, target):
        """ Center the camera around the target
        """
        
        left, top, _, _ = target.rect
        _, _, width, height = self.window
        
        # Center the target within the camera window to start
        left, top, _, _ = left-(width/2), top-(height/2), width, height
    
        # Ensure camera window does not go outside the world map
        left = max(0, left)                         # stop scrolling at the left edge
        left = min(self.worldMapWidth-width-1, left)  # stop scrolling at the right edge
        top = min(self.worldMapHeight-height-1, top)  # stop scrolling at the bottom
        top = max(0, top)                           # stop scrolling at the top
    
        self.window = Rect(left, top, width, height)
        winSurface = surface.subsurface(self.window)
        
        return winSurface
