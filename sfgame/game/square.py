# Filename: square.py
# Copyright 2014, SFGame Project
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Author: Adalberto Medeiros (adalbas@outlook.com)

import logging

import pygame
from pygame import sprite

from game.spritesheet import BaseAnimation

LOG = logging.getLogger(__name__)

class Square(sprite.Sprite):
    
    def __init__(self, index, size, value):
        super(Square, self).__init__()
        self.index = index
        self.h_effect = None
        self.rect = pygame.Rect((index[0]*size[0], index[1]*size[1]), size)
        self.value = value
          
    def get_value(self):
        """ Return the string/number value of the square"""
        return self.value
    
    def get_size(self):
        """ Return square size"""
        return self.size

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
            # Error is reached if self.h_effect is None, i. e., highlight is off
            pass
        finally:
            # Choose color based on value
            if self.value == 1:
                color = pygame.Color('white')
            elif self.value == 0:
                color = pygame.Color('red')
            sqr_surface.fill(color)
            
            surface.blit(sqr_surface, self.rect)
