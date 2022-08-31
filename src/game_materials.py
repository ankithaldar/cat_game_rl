#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Global game economy
'''

# imports
from collections import Counter

# imports


class GameEconomy:
  '''
  Total Game Economy
  '''

  def __init__(self):
    self.coins = 0
    self.items_in_hand = Counter()

  def init_stash(self):
    pass

  def update_coins(self, used_coins=0, gained_coins=0):
    self.coins += gained_coins - used_coins

  def update_stash(self, used_stash=None, gained_stash=None):
    if used_stash is not None:
      self.items_in_hand.subtract(used_stash)

    if gained_stash is not None:
      self.items_in_hand.update(gained_stash)
