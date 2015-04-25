# Filename: persona.py
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
import itertools
import pygame
from pygame import sprite
import numpy as n
from pprint import pprint

from game.spritesheet import SpriteStripAnim
from constants import FPS, PERSONA_SIZE

LOG = logging.getLogger(__name__)

# TODO: move this to functions or constants module
SIZE = PERSONA_SIZE[0]   # size of the square side
MOVE_DELAY = 0.5         # time to move from one square to another
MOVE_SPEED = SIZE / MOVE_DELAY      # speed to move a square

class Persona(sprite.Sprite):
    def __init__(self, board, pos, size, **kwargs):
        super(Persona, self).__init__()
        self.image = pygame.Surface(size).convert()
        self.image.fill(pygame.Color('white'))
        #self.rect = self.image.get_rect()
        #self.rect.x = pos[0]
        #self.rect.y = pos[1]
        self.rect = pygame.Rect(pos, size)
        self.x = pos[0]
        self.y = pos[1]
        self.strip_index = 0
        self.speed = (0,0)
        self.board = board
        self.move_mask = self.get_move_mask()
        self.move_area = sprite.Group(board.squares)
        self.square_walk = n.zeros(2, dtype=int)     
     
    def current_sqr(self):
        sqr = self.board.get_square_from_position(self.rect.center)
        return sqr   
        
    def stop(self):
        self.speed = (0, 0)
        
    def is_stopped(self):
        if self.speed == (0, 0):
            return True
        else:
            return False
        
    def get_direction(self):
        if self.is_stopped():
            return (0, 1)
        return (n.array(self.speed) / n.linalg.norm(n.array(self.speed))).astype(int)
                
    def move(self, speed, seconds=1):
        # Dont need to perform movement if speed is 0
        if self.is_stopped():
            return
          
        # start square movement
        if n.all(self.square_walk == n.array([0,0])):
            try:
                index = self.current_sqr().index
            except IndexError:
                LOG.warning('Could not retrieve current position for rect %s' % self.rect)
                self.stop()
                return
            
            # Check for collisions (next square exists)
            direction = self.get_direction()
            n_i, n_j = n.array(index) + direction
            try:
                # try block to get uninvalid indexes (outside board)
                n_square = self.board.get_square(n_i, n_j)
                LOG.debug('Move to next square. Current: %s Next:%s' %
                          (self.rect, n_square.rect))
                
                if n_square not in self.move_area:
                    LOG.debug("Try to move outside move area: %s" % n_square.rect)
                    self.stop() 
                    return
            except IndexError:
                self.stop()
                return  
        
        # If all collision check passed, then move
        delta = n.array([speed[0] * seconds, speed[1] * seconds])
        self.x += delta[0]
        self.y += delta[1]        
        try:
            self.walk_iter(delta).next()
        except StopIteration:
            # Fix square position
            sqr = self.current_sqr()
            self.x = sqr.rect.x
            self.y = sqr.rect.y 
            self.square_walk = n.zeros(2)
            self.stop()
            return
    
    def walk_iter(self, delta): 
        # generator to move one square at a time
        sqr_size = n.array(self.board.get_square_size())
        while n.all(n.absolute(self.square_walk) < sqr_size):
            self.square_walk = self.square_walk + delta
            yield 
                   
    def draw(self, surface, camera):
        if self.strips is None:
            self.sprite_anim()
            
        # fix float values in rect
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)
            
        sprite = self.strips[self.strip_index].next()
        self.image.fill(pygame.Color('white'))
        self.image.set_colorkey(pygame.Color('white'), pygame.RLEACCEL)
        self.image.blit(sprite, (0,0))
        surface.blit(self.image, camera.apply(self))
    
    def sprite_anim(self, filename, spritesheet,
                    count, frames, colorkey):
        
        self.strips = []       
        for i in range(len(spritesheet)):
            self.strips.append(SpriteStripAnim(filename,  spritesheet[i],
                                               count, pygame.Color(colorkey),
                                               True, frames))
            
    def event(self, event, seconds):
        # fix center from last move
        if event.type == pygame.KEYUP:
            return
          
    def keypressed(self, keys, seconds):
        # Move the player if an arrow key is pressed
        lock = not self.is_stopped()
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
        #self.draw(self.image) 
        
    def get_move_mask(self):
        matrix = n.ones((3,3))
        matrix[0,0] = 0
        matrix[0,2] = 0
        return self.set_mask(matrix, distance=2)
    
    def set_mask(self, matrix, distance=1):
        self.move_mask = MoveAreaMask(matrix, distance)
        return self.move_mask


class MoveAreaMask(object):
    def __init__(self, matrix=None, distance=1):
        """ Define the mask that will be used to get the right squares for 
            a player's move area. This mask has a distance to the player
            (which will used in the get neighbors method.
            The mask is a set of 1 and 0, and a P value to sign up where
            the player is (mostly common in the middle.
            This can be loaded from configure file or calculated from
            player's attributes (further in the development).
            Ex: [ [0  1  1]
                  [1  P  1]
                  [1  1  1] ]"""
        if matrix is None:
            matrix = n.ones((2+distance, 2+distance), dtype=int)
        self.p_pos = (matrix.shape[0] / 2, matrix.shape[1] / 2) # player position
        self.distance = distance
        self.matrix = matrix
        
    def get_mask(self):
        return self.matrix


class Team(sprite.Group):
    def __init__(self, name):
        super(Team, self).__init__()
        self.name = name
        self.players_pos = []
        self.team_iter = itertools.cycle(self.sprites())
        
    def add_player(self, *players):
        """Add player(s) to sprite Group players"""
        self.add(*players)
        self.team_iter = itertools.cycle(self.sprites())
        
    def next_player(self, *kwargs):
        LOG.debug("Team %s sprites: %s" % (self.name, self.sprites()))
        return self.team_iter.next()
    
    def get_all_positions(self):
        # get index positions for all players in this team
        if self.players_pos is not None:
            return self.players_pos
        
        for player in self.sprites():
            p_pos = player.board.get_index_from_position(player.rect.center)
            self.players_pos.append(p_pos)
        return self.players_pos   
            
            
# not currently used   
class Move(object):        
    def __init__(self, persona, speed):
        translation = n.identity(3, dtype=n.int)
        translation[0][2] = speed[0]
        translation[1][2] = speed[1]
        self.translation = translation
        self.persona = persona
        self.move()         
        
    def get_current(self):
        cur_t = self.persona.rect.center
        return n.array([cur_t[0],cur_t[1],1]).T

    def move(self):
        # Find values for dx and dy to move
        current = self.get_current()
        m_vector = n.dot(self.translation, current).T
        self.persona.rect.centerx = m_vector[0]
        self.persona.rect.centery = m_vector[1]     
