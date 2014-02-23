# Filename: board.py
# 
# Add license here

# Author: Adalberto Medeiros (adalbas@gmail.com)
# Code references:

# Abstract class containing main methods and definitions
# for a board

import numpy as np

from constants import SCREEN_SIZE, SQUARE_SIZE
from square import BitSquare

class Board(object):
    """This class contains the methods and definitions for a board, i.e.
    the map where the players will be set in"""
    
    def __init__(self, file_board=None):
        """ Load board for a given size (in pixels) and a board matrix"""
        self.size, self.matrix_board = self._load_board_from_file(file_board)
        
    def _load_board_from_file(self, filename):
        """ Load board info from file and return a matrix of Squares.
        This class should be override by the child board classes.
        This will just create a bit board chess given the self.size"""
        """ Implemented by child class"""
        pass
        
    def load_board(self):
        """ Load squares in board, with all their characteristics
        Implemented by child class"""
        pass
        
    def get_matrix_size(self):
        return self.matrix_board.shape
    
    def get_size(self):
        """ Return size of the board in pixels"""
        return self.size
    
    def get_square_size(self):
        sqr_size = np.array(self.size)/np.array(self.matrix_board.shape)
        return tuple(sqr_size)
    
    def draw_board(self):
        """Implemented by child class"""
        pass
    

class BitBoard(Board):
    """ 0 and 1 board. To build mazes, for instance"""
    
    def __init__(self, file_board=None):
        if file_board is None:
            self.size = SCREEN_SIZE 
            self.matrix_board = self._create_chessboard()  
            print self.matrix_board
        else:
            self.size, self.matrix_board = \
                 self._load_board_from_file(file_board)
            
    def _create_chessboard(self):
        """ Chess board calculated by:
        matrix: Xij = | sin [(i+j) * pi/2] |
        """
        self.matrix_size = tuple(np.array(self.size)/np.array(SQUARE_SIZE))
        def f(i,j):
            return np.absolute(np.sin((i+j)*np.pi/2).astype(int))
        
        return np.fromfunction(f, self.matrix_size, dtype=int)
    
    def load_board(self):
        """ load BitSquares """
        # TODO: Change matrix to numpy

        def set_bitsquare(i, j, sqr_size):
            new_sqr = BitSquare((i*sqr_size[0], j*sqr_size[1]),
                                sqr_size, self.matrix_board[i][j])
            return new_sqr
        
        N, M = self.get_matrix_size()
        sqr_size = self.get_square_size()
        
        self.squares = [ [set_bitsquare(i, j, sqr_size) \
                          for i in range(N) ] \
                        for j in range(M) ]
    
    def draw_board(self, surface):
        """ draw the squres from the board"""
        if self.squares is None:
            self.load_board()
        
        N, M = self.get_matrix_size()
        for i in range(N):
            for j in range(M):
                self.squares[i][j].draw(surface)
                
    def update_board(self):
        """ update only needed squares with effects, anim, sprites, etc..."""
        # highlight squares in diagonal
        N, M = self.get_matrix_size()
        for i in range(N):
            for j in range(M):
                if i == j:
                    self.squares[i][j].set_highlight([190, 50, 190, 255, 50])
        