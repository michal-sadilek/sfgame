# Filename: square.py
# 
# Add license here

# Author: Adalberto Medeiros (adalbas@gmail.com)
# Code references: pygame - wall.py example

import os
import pygame

import constants as K
from game.board import BitBoard

# Initialize pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Set up the display
pygame.display.set_caption(K.SCREEN_NAME)
clock = pygame.time.Clock()

# Create and load board (squares)
chessboard = BitBoard(None)
chessboard.load_board()

screen = pygame.display.set_mode(K.SCREEN_SIZE)

running = True
while running:
    
    clock.tick(K.FPS)
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
            
    # Start screen
    screen.fill(pygame.Color('white'))
    
    # draw methods
    chessboard.draw_board(screen)
    
    pygame.display.flip()
