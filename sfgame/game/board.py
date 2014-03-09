# Filename: board.py
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
import copy

import numpy as n
from numpy import ma
from scipy import ndimage

import pygame
from pygame import sprite

from constants import SCREEN_SIZE, SQUARE_SIZE, FPS
from game.square import BitSquare
from game.persona import Team, MoveAreaMask

LOG = logging.getLogger(__name__)

class Board(object):
    """This class contains the methods and definitions for a board, i.e.
    the map where the players will be set in"""
    
    def __init__(self):
        """ Load board for a given size (in pixels) and a board matrix"""
        pass
        
    def load(self):
        """ Load squares in board, with all their characteristics
        Implemented by child class"""
        pass    
    
    def draw(self, surface):
        """ draw the squares from the board"""
        if self.squares is None:
            self.load_board()
        
        N, M = self.get_size()
        for i in range(N):
            for j in range(M):
                self.squares[i][j].draw(surface)
         
    def update(self):
        pass
 
    def get_size(self):
        return self.matrix_board.shape
    
    def get_pixel_size(self):
        """ Return size of the board in pixels"""
        return n.array(self.size) * n.array(self.sqr_size)
    
    def get_square_size(self):
        return self.sqr_size
    
    def get_index_from_position(self, pos, sqr_size=SQUARE_SIZE):
        # get the board square the persona is in
        center = n.array(pos)
        s_size = n.array(sqr_size)
        i, j = n.around(n.array(center - s_size/ 2, dtype=float)/ s_size).astype(int)
        return (i, j)
    
    def get_square_from_position(self, pos, sqr_size=SQUARE_SIZE):
        # get the board square the persona is in
        i, j = self.get_index_from_position(pos, sqr_size)
        #LOG.debug('Return square for index %d, %d' % (i,j))
        try:
            return self.get_square(i,j)
        except IndexError:
            raise
    
    def get_neighbors(self, i, j, dist=1, mask=n.ones((3,3))):
        """ Use scipy binary dilation to get appropriate methods."""
        # Convert mask to full board size, based on defined
        # i, j position
        full_mask = n.zeros_like(self.matrix_board)
        full_mask[i, j] = 1
        
        # apply mask using distance as iterations
        n_mask = ndimage.binary_dilation(full_mask,
                                         structure=mask, iterations=dist)
        # get masked array and compress it to 1d array
        neighbors = ma.array(self.squares, mask=~n_mask).compressed()
        LOG.debug("Neighbors found for mask %s: %s" % (mask, neighbors))
        return neighbors.tolist()

    def get_square(self, i, j):
        """ Return square on matrix(i,j)"""
        try:
            if i < 0 or j < 0:
                raise IndexError
            return self.squares[i][j]
        except IndexError:
            raise
        
    def set_size(self, pixel_size, square_size):
        """Set number of squares per axis """
        # TODO: is this really needed?
        n_sqrs = n.array(pixel_size)/n.array(square_size)
        return tuple(n_sqrs)
    
    def set_board_engine(self, board_engine):
        self.board_engine = board_engine
        
    def get_board_engine(self):
        return self.board_engine
    
    
class BitBoard(Board):
    """ 0 and 1 board. To build mazes or chessboards."""
    
    def __init__(self, sqr_size=SQUARE_SIZE, matrix=None, filename=None):
        super(BitBoard, self).__init__()
        self.sqr_size = sqr_size
        if filename:
            self.size, self.matrix_board = \
                 self._load_from_file(filename)
        elif matrix:
            self.size = matrix.shape
            self.matrix_board = matrix
        else: # default
            self.size = self.set_size(SCREEN_SIZE, sqr_size)
            self.matrix_board = self._create_chessboard(self.size)  
            print self.matrix_board, self.matrix_board.shape
            
    def _create_chessboard(self, size):
        """ Chess board calculated by:
        matrix: Xij = | sin [(i+j) * pi/2] |
        """
        def f(i,j):
            return n.absolute(n.sin((i+j)*n.pi/2).astype(int))       
        return n.fromfunction(f, size, dtype=int)
    
    def load(self):
        """ load BitSquares """
        # TODO: Change matrix to numpy ??

        def set_bitsquare(i, j, sqr_size):
            new_sqr = BitSquare((i, j), sqr_size, self.matrix_board[i][j])
            return new_sqr
        
        N, M = self.get_size()
        sqr_size = self.get_square_size()
        
        self.squares = [ [set_bitsquare(i, j, sqr_size) \
                          for j in range(N) ] \
                        for i in range(M) ]
  

class BoardEngine(object):
    def __init__(self, board, current=None):
        self.board = board
        board.set_board_engine(self)
        self.current_player = current
        self.teams = []
        self.move_area = MoveArea(self.board)
        
    def load(self):
        """ Initialize board effects"""
        if self.current_player is None:
            LOG.warning("No current player set for board %s" % self.board)
        else:
            self.move_area.update_area(self.current_player)
            self.ma_filter_other_teams(self.current_player)
            self.highlight_squares(self.move_area.sprites())          
        
    def event(self, event, seconds):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                # turn off previous move_area
                self.highlight_squares(self.move_area.sprites(), on=False)
                # Update move area
                mask = ndimage.generate_binary_structure(2, 1).astype(int)
                ma_mask = MoveAreaMask(mask, 1)
                self.move_area.update_area(self.current_player, ma_mask)
                self.ma_filter_player(self.current_player)
                self.highlight_squares(self.move_area.sprites(), on=True)
                
            elif event.key == pygame.K_s:
                # turn off previous move_area
                self.highlight_squares(self.move_area.sprites(), on=False)
                # Change current player
                self.current_player = self.next_player(self.teams)
                # Set new move area
                self.move_area.update_area(self.current_player)
                self.ma_filter_other_teams(self.current_player)
                self.highlight_squares(self.move_area.sprites(), on=True)
                
    def ma_filter_other_teams(self, player):
        others = self.get_others_team(player)
        for other in others:
            self.move_area.filter_collision(other)
            
    def ma_filter_player(self, player):
        self.move_area.filter_single_collision(player)
            
    def ma_get_collided_others(self, player):
        others = self.get_others_team(player)
        collided = sprite.Group([])
        for other in others:
            collided.append(self.move_area.get_collided(other))
        LOG.debug("collided sprites %s: " % collided)
        return collided
                
    def highlight_squares(self, squares, on=True):
        for square in squares:
            square.highlight([190, 50, 190, 255, 50], FPS/4, on)
        
    def get_current_player(self):
        return self.current_player
    
    def get_team(self, player):
        for team in self.teams:
            if team.has(player):
                return team
        LOG.warning('No team defined for player %s' % player)
        return None
    
    def get_others_team(self, player):
        team = self.get_team(player)
        others = copy.copy(self.teams)
        others.remove(team)
        return others
    
    def next_player(self, teams, **kwargs):
        # get team current player
        current_team = self.get_team(self.current_player)
        for team in teams:
            if current_team != team:
                return team.next_player()
        return self.current_player
        
    def set_current_player(self, player):
        """ To set it current, a player should have been added to the 
        board engine"""
        for team in self.teams:
            if player in team:
                self.current_player = player
                return
        LOG.warning('Player %s not on board engine' % player.rect)
        self.current_player = None
        
    def create_team(self, name):
        team = Team(name)
        self.teams.append(team)
        return team
    

class MoveArea(sprite.Group):
    def __init__(self, board):
        super(MoveArea, self).__init__([])
        self.board = board

    def get_collided(self, group):
        return sprite.groupcollide(self, group, False, False)
    
    def filter_single_collision(self, single):
        sprite.spritecollide(single, self, True)
    
    def filter_collision(self, group):
        # Check collision and remove squares from this group
        # if collision is true
        # TODO: use a collide function and pass as parameter to check 
        # indices instead of checking rects
        sprite.groupcollide(self, group, True, False)
    
    def update_area(self, player, move_mask=None):
        # get move area from mask (list of squares)
        if move_mask is None:
            move_mask = player.get_move_mask()
        i, j = self.board.get_index_from_position(player.rect.center)
        move_area = self.board.get_neighbors(i, j, move_mask.distance,
                                             move_mask.get_mask())
        self.empty()
        self.add(move_area)
        LOG.debug("move area %s" % self)
        # Update move area for the player
        player.move_area = self
        return self
