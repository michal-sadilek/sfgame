# Filename: board.py
# 
# Add license here

# Author: Adalberto Medeiros (adalbas@gmail.com)
# Code references:

# Abstract class containing main methods and definitions
# for a board

import numpy as np

import pygame
from pygame import sprite

from constants import SCREEN_SIZE, SQUARE_SIZE
from square import BitSquare

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
        try:
            i, j = tuple((center - s_size/ 2)/ s_size)
        except IndexError:
            print "No square at %d, %d." % (i,j)
            # TODO: how to treat this exception?
            i, j = (0, 0)
        return (i, j)
    
    def get_square_from_position(self, pos, sqr_size=SQUARE_SIZE):
        # get the board square the persona is in
        i, j = self.get_index_from_position(pos, sqr_size)
        return self.get_square(i,j)
    
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
        return self.squares[i][j]
    
    def update(self):
        pass
    
    def draw(self, surface):
        """Implemented by child class"""
        pass
    

class BitBoard(Board):
    """ 0 and 1 board. To build mazes, for instance"""
    
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
        # TODO: Change matrix to numpy

        def set_bitsquare(i, j, sqr_size):
            new_sqr = BitSquare((i, j), sqr_size, self.matrix_board[i][j])
            return new_sqr
        
        N, M = self.get_size()
        sqr_size = self.get_square_size()
        
        self.squares = [ [set_bitsquare(i, j, sqr_size) \
                          for j in range(N) ] \
                        for i in range(M) ]
    
    def draw(self, surface):
        """ draw the squares from the board"""
        if self.squares is None:
            self.load_board()
        
        N, M = self.get_size()
        for i in range(N):
            for j in range(M):
                self.squares[i][j].draw(surface)
                
    def update(self):
        """ update only needed squares with effects, anim, sprites, etc..."""
        pass
        # highlight squares in diagonal
        N, M = self.get_size()
        for i in range(N):
            for j in range(M):
                if i == j:
                    self.squares[i][j].highlight([190, 50, 190, 255, 50],
                                                  on=False)
                    
    def set_size(self, pixel_size, square_size):
        # get number of squares per axis
        n_sqrs = np.array(pixel_size)/np.array(square_size)
        return tuple(n_sqrs)
    

class BoardEngine(object):
    def __init__(self, board):
        self.board = board
        self.players = sprite.Group([])
        self.enemies = sprite.Group([])
        self.objects = sprite.Group([])
        
    def set_move_area(self, player):
        i, j = self.board.get_index_from_position(player.rect.center,
                                                   self.board.sqr_size)
        move_area = self.board.get_neighbors(i, j)
        
        # convert area to array to use use .flatten method to get a list 
        # from it
        group = sprite.Group(list(move_area.flatten()))
        print group
        if sprite.spritecollideany(player, group) is None:
            player.speed = (0,0)
            
        return group
            
    def event(self, event, seconds):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_area = self.set_move_area(self.current)
                self.highlight_squares(move_area.sprites())
                
    def highlight_squares(self, squares):
        for square in squares:
            square.highlight([190, 50, 190, 255, 50])
        
    def set_current_player(self, player):
        self.current = player
        
    def add_player(self, *players):
        """Add player(s) to sprite Group players"""
        self.players.add(*players)
    
    def add_objects(self, group):
        pass
    
        