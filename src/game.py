#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Logics Of The Game
'''

# imports
from dataclasses import dataclass
from typing import Dict

from game_materials import GameMaterials

# imports

DEBUG = False

# ==============================================================================

@dataclass
class Items():
  name: str
  req_unit_raw: Dict[str, int]
  init_cost: int
  required_time: int

# ==============================================================================

class CatGame:
  '''
  Logics of the game
  '''

  def __init__(self):
    self.time = 0
    self.coins = GameMaterials()
    self.load_items()

  def load_items(self):
    pass

  def get_presents_coins(self):
    '''
    get 210 coins every 5 mins in the game
    '''
    self.coins.update_coins(gained_coins=210)

# ==============================================================================
