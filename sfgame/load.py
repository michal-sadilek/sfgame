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
import ConfigParser
import random as r
from ast import literal_eval
import logging

from game.persona import Persona
from constants import PERSONA_SIZE, FPS

BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
DATADIR = os.path.join(BASEDIR, 'data')
PLAYER_CONFIG = os.path.join(DATADIR, 'players')

LOG = logging.getLogger('game.load')

def load_config(filename):
    config = ConfigParser.ConfigParser()
    config.read(filename)
    return config

def load_teams(config, board_engine):
    teams = config.get('DEFAULT','teams').split(',')
    # create teams
    return [ board_engine.create_team(team) for team in teams ]
    
def load_players(config, board_engine, team):
    players = config.get(team, 'players').split(',')
    return [ load_player(config, board_engine, player) for player in players]
    
def generate_pos(square_size, board_size):
    x_pos = r.randint(0, board_size[0]-1)
    y_pos = r.randint(0, board_size[1]-1)
    return (x_pos * square_size[0], y_pos * square_size[1])
    
def load_player(config, board_engine, p):
    try:
        f = config.get(p, 'filename')
        spritesheet = config.get(p, 'spritesheet')
        anim_time = config.getfloat(p, 'anim_time')
        count = config.getint(p, 'count')
        colorkey = config.get(p, 'colorkey')
    except:
        raise
    
    filename = os.path.join(DATADIR, f)
    spritesheet_pos = literal_eval(spritesheet)
    # get player attributes
    board = board_engine.board
    size = PERSONA_SIZE
    pos = generate_pos(board.get_square_size(), board.get_size())
    
    LOG.debug('size %s, pos %s' % (size,pos))
    
    player = Persona(board, pos, size)
    player.sprite_anim(filename, spritesheet_pos, count,
                       int(FPS * anim_time), colorkey)
    return player

    
                                        