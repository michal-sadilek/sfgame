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
# class Camera source from Dominic Kexel

import os
import pygame
import logging
import logging.config

import constants as K
from game.board import BitBoard, BoardEngine
import load

LOG = logging.getLogger(__name__)

def config():
    pass

class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def complex_camera(camera, target_rect):
    WIN_WIDTH, WIN_HEIGHT = K.SCREEN_SIZE
    HALF_WIDTH = int(WIN_WIDTH / 2)
    HALF_HEIGHT = int(WIN_HEIGHT / 2)
    
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
    t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return pygame.Rect(l, t, w, h)

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
    board_engine = BoardEngine(chessboard)
    
    # Load teams and players from config players file
    config = load.load_config(load.PLAYER_CONFIG)
    teams = load.load_teams(config, board_engine)
    for team in teams:
        players = load.load_players(config, board_engine, team.name)
        for player in players:
            team.add_player(player)
    
    # Set current player and load engine -> needed to set up move area
    LOG.debug('Teams: %s' % teams)
    board_engine.set_current_player(teams[0].next_player())
    board_engine.load()
    
    board_width, board_height = chessboard.get_pixel_size()
    camera = Camera(complex_camera, board_width, board_height)
  
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
               
        # Start screen (background)
        screen.fill(pygame.Color(K.SCREEN_COLOR))
        
        camera.update(cur_player)
        
        # draw methods
        #chessboard.draw(screen)
        chessboard.draw(screen, camera)
        for team in teams:
            for player in team:
                player.draw(screen, camera)
                #player.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    basedir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                    '../'))  
    logging.config.fileConfig(basedir + '/logging.conf')
    # short instructions
    print "Instructions:"
    print "Use arrows to move"
    print "s	to switch player"
    print "a	to ???"
    game()

