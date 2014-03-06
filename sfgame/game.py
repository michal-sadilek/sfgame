# Filename: square.py
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

import os
import pygame
import logging.config

import constants as K
from game.board import BitBoard, BoardEngine
from game.persona import Persona

def config():
    pass

def game():
    # Initialize pygame
    os.environ["SDL_VIDEO_CENTERED"] = "1"
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
    
    # Create players and add them to the board
    player1 = Persona(chessboard,(0,0), K.PERSONA_SIZE)
    player1.sprite_anim()
    player2 = Persona(chessboard,(320,320), K.PERSONA_SIZE)
    player2.sprite_anim()
    player3 = Persona(chessboard, (120, 120), K.PERSONA_SIZE)
    player3.sprite_anim()
    
    # Create board engine and associate players
    board_engine = BoardEngine(chessboard)
    teamA = board_engine.create_team("Team A")
    teamB = board_engine.create_team("Team B")
    teamA.add_player(player1)
    teamB.add_player([player2, player3])
    board_engine.set_current_player(player1)
    board_engine.load()
    
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
            board_engine.event(e, seconds)       
            cur_player = board_engine.get_current_player()
            cur_player.event(e, seconds)
        
        # move player
        key = pygame.key.get_pressed()
        cur_player.keypressed(key, seconds)
               
        # Start screen
        screen.fill(pygame.Color(K.SCREEN_COLOR))
        
        # draw methods
        chessboard.draw(screen)
        for player in teamA:
            player.draw(screen)
        for player in teamB:
            player.draw(screen)
        
        pygame.display.flip()
    
if __name__ == "__main__":
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                    '../'))  
    logging.config.fileConfig(basedir + '/logging.conf')
    game()
