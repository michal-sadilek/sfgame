# Filename: persona.py
# 
# Add license here

# Author: Adalberto Medeiros (adalbas@gmail.com)
# Code references:

import pygame

from spritesheet import SpriteStripAnim
from constants import FPS

class Persona(object):
    
    def __init__(self, pos, size, **kwargs):
        self.rect = pygame.Rect(pos,size)
        self.strip_index = 0
    
    def move(self, dx, dy):       
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)
    
    def move_single_axis(self, dx, dy):    
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy
    
    def draw(self, surface):
        if self.strips is None:
            self.sprite_anim()
            
        sprite = self.strips[self.strip_index].next()
        surface.blit(sprite, self.rect)
    
    def sprite_anim(self):
        frames = FPS / 2
        filename = '/home/acfleury/user/sf/sfgame/data/images/ShiningForce2_Bowie.png'
        # position to each stripanim (2 stripes each)
        stripesheet = [(0,0,23,27), (45,0,23,27), (90,0,22,27), (134,0,22,27)]
        count = 2
        colorkey = pygame.Color('white')
        
        self.strips = []       
        for i in range(len(stripesheet)):
            self.strips.append(SpriteStripAnim(filename,  stripesheet[i],
                                          count, colorkey, True, frames))
            
    def event(self):
        # Move the player if an arrow key is pressed
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.strip_index = 3
            self.move(-4, 0)
        if key[pygame.K_RIGHT]:
            self.strip_index = 2
            self.move(4, 0)
        if key[pygame.K_UP]:
            self.strip_index = 1
            self.move(0, -4)
        if key[pygame.K_DOWN]:
            self.strip_index = 0
            self.move(0, 4)
    
    def set_effect(self):
        pass
    