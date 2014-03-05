# Filename: square.py
# 
# Add license here

# Author: Adalberto Medeiros (adalbas@gmail.com)
# Code references:

import pygame
from pygame import sprite

from game.anim import BaseAnimation

class Square(sprite.Sprite):
    
    def __init__(self, index, size, value):
        super(Square, self).__init__()
        self.index = index
        self.rect = pygame.Rect((index[0]*size[0], index[1]*size[1]), size)
        self.value = value
          
    def get_value(self):
        """ Return the string/number value of the square"""
        return self.value
    
    def get_size(self):
        """ Return square size"""
        return self.size
    
    def draw(self, surface):
        """ Implemented by child"""
        pass
    
    def highlight(self, alpha_array, duration, on=True):
        """The alpha array to make it blink, the duration for each blink,
        in frames per second and if it should be on or off"""
        if not on:
            self.h_effect = None
            return
        self.h_effect = BaseAnimation(alpha_array, True, duration)
        self.h_effect.iter() 

class BitSquare(Square):
    """ Values can be 1 or 0"""
    
    def __init__(self, index, size, value):
        super(BitSquare, self).__init__(index, size, value)
        
    def draw(self, surface):
        # create a temporary surface before draw in the final one
        # this is useful to apply animations and set other attributes
        sqr_surface = pygame.Surface((self.rect.w, self.rect.h)).convert()                         
                            
        # apply highlight
        try:
            alpha = self.h_effect.next()
            sqr_surface.set_alpha(alpha)
        except AttributeError:
            pass
                                               
        # Choose color based on value
        if self.value == 1:
            color = pygame.Color('white')
        elif self.value == 0:
            color = pygame.Color('red')
        sqr_surface.fill(color)
        
        surface.blit(sqr_surface, self.rect)

    
    

