import math

class Util(object):

    @staticmethod
    def get_rotate_angle(sourceLocation, targetLocation):
        """ Get the angle to rotate an image at the source location to point towards
            the target location and whether or not the image should be flipped on the 
            y-axis.  It is assumed that the image is starting horizontal pointing 
            to the right.  The angle can be used for input into the 
            pygame.transform.rotate() function.
        """
        angle = 0
        flip = False

        if targetLocation[0] == sourceLocation[0]:
            if targetLocation[1] > sourceLocation[1]:
                # Cursor is directly below player
                angle = -90
            else:
                # Cursor is directly above or on the player
                angle = 0
        else:
            if targetLocation[0] < sourceLocation[0]:
                # Cursor is to the left of the player. Image needs to be flipped
                # on the y-axis.
                flip = True

            # Determine the angle to rotate the image
            dy = float((sourceLocation[1]-targetLocation[1]))
            dx = float(abs(targetLocation[0]-sourceLocation[0]))
            angle = math.degrees(math.atan(dy/dx))

        return (angle, flip)

