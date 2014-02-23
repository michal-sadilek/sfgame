# Filename: square.py
# 
# Add license here

# Author: Adalberto Medeiros (adalbas@gmail.com)
# Code references:

import pygame

from anim import BaseAnimation
from constants import FPS

class Square():
    
    def __init__(self, pos, size, value):
        pass
    
    def get_type(self):
        pass
    
    def get_size(self):
        pass
    
    def get_value_criterias(self):
        """The map value should be associated to a 
        certain type of criterias, as stripesheet filename,
        colorkey, and other useful information for the 
        square"""
    
    def draw(self, surface):
        pass
    
    def get_tile(self):
        pass
    
    def set_tile(self):
        pass
    
    def hihglight(self):
        """ Highlight square and makes it blink.
        Frequency is added as input"""
    

class BitSquare(Square):
    """ Values can be 1 or 0"""
    
    def __init__(self, pos, size, value):
        self.size = size
        self.value = value
        self.rect = pygame.Rect(pos, size)
        
    def set_highlight(self, alpha_array):
        self.h_effect = BaseAnimation(alpha_array, True, FPS/2)
        self.h_effect.iter() 
              
    def get_color(self):
        pass 
        
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
            
    def get_rect(self):
        """ return Rect """
        return self.rect
        
    def get_value(self):
        """ Return 0 or 1"""
        return self.value
    
    def get_size(self):
        """ Return square size"""
        return self.size
    
    

