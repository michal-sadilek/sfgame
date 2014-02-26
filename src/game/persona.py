# Filename: persona.py
# 
# Add license here

# Author: Adalberto Medeiros (adalbas@gmail.com)
# Code references:

import pygame
import numpy

from spritesheet import SpriteStripAnim
from constants import FPS, PERSONA_SIZE

SIZE = PERSONA_SIZE[0]   # size of the square side
MOVE_DELAY = 4          # time to move from one square to another
MOVE_SPEED = SIZE / MOVE_DELAY      # speed to move a square

class Persona(object):  
    def __init__(self, board, pos, size, **kwargs):
        self.rect = pygame.Rect(pos,size)
        self.x = pos[0]
        self.y = pos[1]
        self.current_sqr = board.get_square_from_position(self.rect.center)
        self.strip_index = 0
        self.speed = (0,0)
        self.board = board
        
    def stop(self):
        self.speed = (0,0)
                
    def move(self, speed, seconds=1):       
        # Move each axis separately. Note that this checks for collisions both times.
        dx, dy = speed
        if dx != 0:
            self.move_single_axis(dx, 0, seconds)
        if dy != 0:
            self.move_single_axis(0, dy, seconds)
    
    def move_single_axis(self, dx, dy, seconds=1):    
        # Move the rect
        # return lock
        self.x += dx * seconds
        self.y += dy * seconds
        
        board_size = self.board.get_pixel_size()
        
        # collision with board boundaries
        # TODO: change to persona size
        if self.x + self.rect.w > board_size[0] or self.x < 0:
            self.x -= dx * seconds
            self.stop()
        if self.y + self.rect.h > board_size[1] or self.y < 0:
            self.y -= dy * seconds
            self.stop()
            
        # Check if movement may stop and center it to square
        # TODO: buggy code
        #import pdb
        #pdb.set_trace()
        sqr = self.board.get_square_from_position(self.rect.center)
        print sqr.rect, self.current_sqr.rect
        if sqr.rect.center != self.current_sqr.rect.center:        
            print "Move to center", self.rect.center
            self.x = sqr.rect.x
            self.y = sqr.rect.y
            self.current_sqr = sqr
            self.stop()
                   
    def draw(self, surface):
        if self.strips is None:
            self.sprite_anim()
            
        # fix float values in rect
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)
            
        sprite = self.strips[self.strip_index].next()
        surface.blit(sprite, self.rect)
    
    def sprite_anim(self):
        
        # TODO(adalbas): change values below to the appropriate place (BD, file...)
        frames = FPS / 4
        filename = '/home/acfleury/user/sf/sfgame/data/images/ShiningForce2_Bowie.png'
        # position to each stripanim (2 stripes each)
        stripesheet = [(0,0,23,27), (45,0,23,27), (90,0,22,27), (134,0,22,27)]
        count = 2
        colorkey = pygame.Color('white')
        
        self.strips = []       
        for i in range(len(stripesheet)):
            self.strips.append(SpriteStripAnim(filename,  stripesheet[i],
                                          count, colorkey, True, frames))
            
    def event(self, event, seconds):
        # fix center from last move
        if event.type == pygame.KEYUP:
            pass
          
    def keypressed(self, keys, seconds):
        # Move the player if an arrow key is pressed
        if self.speed == (0,0):
            lock = False
        else:
            lock = True
        if not lock:
            if keys[pygame.K_LEFT]:
                self.strip_index = 2
                self.speed = (-MOVE_SPEED, 0)
            if keys[pygame.K_RIGHT]:
                self.strip_index = 3
                self.speed = (MOVE_SPEED, 0)
            if keys[pygame.K_UP]:
                self.strip_index = 1
                self.speed = (0, -MOVE_SPEED)
            if keys[pygame.K_DOWN]:
                self.strip_index = 0
                self.speed = (0, MOVE_SPEED)
        self.move(self.speed, seconds)       
        # lock movement for MOVE_DELAY time
        #self.cooldown -= seconds
                 
    def set_effect(self):
        pass
    
# not currently used   
class Move(object):        
    def __init__(self, persona, speed):
        translation = numpy.identity(3, dtype=numpy.int)
        translation[0][2] = speed[0]
        translation[1][2] = speed[1]
        self.translation = translation
        self.persona = persona
        self.move()         
        
    def get_current(self):
        cur_t = self.persona.rect.center
        return numpy.array([cur_t[0],cur_t[1],1]).T

    def move(self):
        # Find values for dx and dy to move
        current = self.get_current()
        m_vector = numpy.dot(self.translation, current).T
        self.persona.rect.centerx = m_vector[0]
        self.persona.rect.centery = m_vector[1]
        
    def square_move(self):
        pass
        #dist_to_center = numpy.array(sqr.rect.center) - numpy.array(self.rect.center)
        #move_array = numpy.array([dx * seconds, dy * seconds])
        #next_sqr_center = numpy.array(self.rect.center) + numpy.round(move_array)
        #print sqr.rect.center, "-", self.rect.center, move_array, dist_to_center
        #if numpy.any(numpy.array(sqr.rect.center) == next_sqr_center):
            
        #if numpy.any(move_array * dist_to_center > 0):      
            # this will check both the distance and the move
            # are on the same direction 
        #if numpy.any(numpy.absolute(dist_to_center) == 39): # < numpy.absolute(move_array)