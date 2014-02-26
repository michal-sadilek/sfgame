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

# clock setup
clock = pygame.time.Clock()
elapsed = 0

# Create and load board (squares)
chessboard = BitBoard()
chessboard.load()
chessboard.update()

# Create player and add it to the board
player = Persona(chessboard,(0,0), K.PERSONA_SIZE)
player.sprite_anim()

running = True
while running:
    
    elapsed = clock.tick(K.FPS)
    seconds = elapsed/1000.0

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
            pygame.quit()
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
        # treat players, npc, and others.        
        player.event(e, seconds)
    
    # move player
    key = pygame.key.get_pressed()
    player.keypressed(key, seconds)
           
    # Start screen
    screen.fill(pygame.Color(K.SCREEN_COLOR))
    
    # draw methods
    chessboard.draw(screen)
    player.draw(screen)
    
    pygame.display.flip()
