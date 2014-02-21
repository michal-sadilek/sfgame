# Filename: square.py
# 
# Add license here

# Author: Adalberto Medeiros (adalbas@gmail.com)
# Code references:

import pygame

class Square():
    
    def __init__(self, pos, size, value):
        pass
    
    def get_type(self):
        pass
    
    def get_size(self):
        pass
    
    def draw(self, surface):
        pass
    
    def get_tile(self):
        pass
    
    def set_tile(self):
        pass
    

class BitSquare(Square):
    """ Values can be 1 or 0"""
    
    def __init__(self, pos, size, value):
        self.size = size
        self.value = value
        self.rect = pygame.Rect(pos, size)
        
    def get_color(self):
        pass 
        
    def draw(self, surface):
        if self.value == 1:
            surface.fill(pygame.Color('white'), self.rect)
        elif self.value == 0:
            surface.fill(pygame.Color('black'), self.rect)
            
    def get_rect(self):
        """ return Rect """
        return self.rect
        
    def get_value(self):
        """ Return 0 or 1"""
        return self.value
    
    def get_size(self):
        """ Return square size"""
        return self.size

