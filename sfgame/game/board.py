# Filename: board.py
# 
# Add license here

# Author: Adalberto Medeiros (adalbas@gmail.com)
# Code references:

# Abstract class containing main methods and definitions
# for a board

import logging
import numpy as np
from numpy import ma

import pygame
from pygame import sprite

from constants import SCREEN_SIZE, SQUARE_SIZE, FPS
from square import BitSquare
from persona import Team

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
        return np.array(self.size) * np.array(self.sqr_size)
    
    def get_square_size(self):
        return self.sqr_size
    
    def get_index_from_position(self, pos, sqr_size):
        # get the board square the persona is in
        center = np.array(pos)
        s_size = np.array(sqr_size)
        i, j = np.around(np.array(center - s_size/ 2, dtype=float)/ s_size).astype(int)
        return (i, j)
    
    def get_square_from_position(self, pos, sqr_size=SQUARE_SIZE):
        # get the board square the persona is in
        i, j = self.get_index_from_position(pos, sqr_size)
        #LOG.debug('Return square for index %d, %d' % (i,j))
        try:
            return self.get_square(i,j)
        except IndexError:
            raise
    
    def get_neighbors(self, i, j, dist=1):
        """ This method returs a 3x3 matrix where the center element
            is the i,j element. You can easily find the top square
            by get the neighbor[0][1] for instance."""
        # treat negative values
        ibound, jbound = (i - dist, j - dist)
        if ibound < 0 : ibound = 0
        if jbound < 0 : jbound = 0
        return np.array(self.squares)[ibound:i+2,jbound:j+2]

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
        n_sqrs = np.array(pixel_size)/np.array(square_size)
        return tuple(n_sqrs)
    
    def set_board_engine(self, board_engine):
        self.board_engine = board_engine
    
    
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
            return np.absolute(np.sin((i+j)*np.pi/2).astype(int))       
        return np.fromfunction(f, size, dtype=int)
    
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
        
    def load(self):
        """ Initialize board effects"""
        move_area = self.update_move_area(self.current_player)
        self.current_player.move_area = move_area
        self.highlight_squares(self.current_player.move_area.sprites())
        
    def event(self, event, seconds):
        # TODO: Each child (different types of board engine)
        # should implement the board events.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                # Turn off previous highlight
                move_area = self.current_player.move_area
                if move_area is not None:
                    self.highlight_squares(move_area.sprites(),
                                           on=False)
                turn_criteria = {'team_alternate' : 'true'}
                # Change current player
                self.current_player = self.next_player(self.teams)
                # Set new move area
                move_area = self.update_move_area(self.current_player)
                self.current_player.move_area = move_area
                self.highlight_squares(self.current_player.move_area.sprites())
                
    def update_move_area(self, player):
        i, j = self.board.get_index_from_position(player.rect.center,
                                                   self.board.sqr_size)
        move_area = self.board.get_neighbors(i, j)
        # convert area to array to use use .flatten method to get a list 
        group = sprite.Group(list(move_area.flatten()))
        return group
                
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


# not in use yet
class MoveArea(sprite.Group):
    def __init__(self, player, board, move_mask):
        self.player = player
        self.board = board
        self.move_mask = move_mask
        
    def get(self, distance=1):
        # get move area from mask (list of squares)
        i, j = self.move_mask.p_pos
        squares = self.board.get_neighbors(i, j, distance)
        move_area = ma.array(squares, self.move_mask)
        return move_area.compressed()
        
    def update(self, move_mask):
        self.move_mask = move_mask
        
# not in use yet
class MoveAreaMask(object):
    def __init__(self, matrix=None, distance=1):
        """ Define the mask that will be used to get the right squares for 
            a player's move area. This mask has a distance to the player
            (which will used in the get neighbors method.
            The mask is a set of 1 and 0, and a P value to sign up where
            the player is (mostly common in the middle.
            This can be loaded from configure file or calculated from
            player's attributes (further in the development).
            Ex: [ [1  0  1]
                  [0  P  0]
                  [0  0  0] ]"""
        if matrix is None:
            matrix = np.zeros((2+distance, 2+distance), dtype=int)
        self.p_pos = (matrix.shape[0] / 2, matrix.shape[1] / 2) # player position
        self.distance = 1
        