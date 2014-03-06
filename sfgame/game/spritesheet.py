# Pygame spritesheet example
# Licensed under LGPLv3

# This class handles sprite sheets
# This was taken from www.scriptefun.com/transcript-2-using
# sprite-sheets-and-drawing-the-background
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)

# File based in Source: http://www.pygame.org/wiki/Spritesheet?parent=CookBook
 
import pygame
from game.anim import BaseAnimation
from constants import PERSONA_SIZE
 
class SpriteSheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error, message:
            print 'Unable to load spritesheet image:', filename
            raise SystemExit, message
        
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None, resize=True):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()

        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        # fits sprite to square size    
        if resize:
            rect.fit((rect.x, rect.y), PERSONA_SIZE)
            return pygame.transform.smoothscale(image, PERSONA_SIZE)
        else:
            return image
    
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey) for rect in rects]
    
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

    
class SpriteStripAnim(BaseAnimation):
    """sprite strip animator"""
    
    def __init__(self, filename, rect, count, colorkey=None,
                 loop=False, frames=1):
        """construct a SpriteStripAnim
        
        filename, rect, count, and colorkey are the same arguments used
        by spritesheet.load_strip.
        """
        self.filename = filename
        ss = SpriteSheet(filename)
        self.images = ss.load_strip(rect, count, colorkey)     
        super(SpriteStripAnim, self).__init__(self.images, loop, frames)
        
    