# Filename: square.py
# 
# Add license here

# Author: Adalberto Medeiros (adalbas@gmail.com)
# Code references: pygame - wall.py example

import os
import pygame

import constants as K
from game.board import BitBoard
from game.persona import Persona

# Initialize pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
#os.environ["SDL_SRCALPHA"] = "1"
pygame.init()

# Set up the display
pygame.display.set_caption(K.SCREEN_NAME)
screen = pygame.display.set_mode(K.SCREEN_SIZE)
clock = pygame.time.Clock()

# Create and load board (squares)
chessboard = BitBoard(None)
chessboard.load_board()
chessboard.update_board()

# Create player and add it to the board
player = Persona((0,0), (24,24))
player.sprite_anim()

running = True
while running:
    
    clock.tick(K.FPS)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
            pygame.quit()
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
    
    # treat players, npc, and others.        
    player.event() 
           
    # Start screen
    screen.fill(pygame.Color(K.SCREEN_COLOR))
    
    # draw methods
    chessboard.draw_board(screen)
    player.draw(screen)
    
    pygame.display.flip()
