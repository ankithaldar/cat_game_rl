#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Manufacturing Unit Logic
'''

# imports
from abc import ABC
from collections import Counter

# imports

DEBUG = False

class Agent(ABC):
  def act(self, control):
    pass


class ManufacturingUnit(Agent):
  '''
  Create Manucaturing Unit For The Game
  '''

  def __init__(self, item_detail, start_time, batch_size, economy,
  current_time):
    self.item_detail = item_detail
    self.start_time = start_time
    self.current_time = current_time
    self.batch_size = batch_size
    self.economy = economy
    self.idle = True

    if DEBUG:
      print(f'{self.item_detail.name}')

  # get total coins required to craft a batch
  def manufacturing_cost(self):
    return (
      (1 + 0.25*(self.batch_size - 1))
      * self.item_detail.init_cost
      * self.batch_size
    )

  # get total of each items required to craft a batch
  def batch_stash(self, item):
    return self.item_detail.req_unit_raw[item] * self.batch_size

  def check_materials_coins_if_available(self):
    is_available = []

    # check if previous materials are available
    for each in self.item_detail.req_unit_raw.keys():
      required_units = self.item_detail.req_unit_raw[each] * self.batch_size
      if self.economy.stash[each] >= required_units:
        is_available.append(True)
      else:
        if DEBUG:
          print(f'{each}: {required_units} is not available')
        is_available.append(False)

    # check if coinss are available
    if self.economy.coins >= self.manufacturing_cost():
      is_available.append(True)
    else:
      if DEBUG:
        print('coins are not available')
      is_available.append(False)

    return all(is_available)

  def update_coins(self):
    self.economy.update_coins(used_coins=self.manufacturing_cost())

  def update_used_stash(self):
    used_stash = dict()
    for each in self.item_detail.req_unit_raw.keys():
      used_stash[each] = -self.batch_stash(each)

    self.economy.update_stash(used_stash=used_stash)

  def start_crafting(self):
    if self.check_materials_coins_if_available() and self.idle:
      self.update_coins()
      self.update_used_stash()
      self.idle = False
      if DEBUG:
        print(f'{self.item_detail.name} is crafting')
    else:
      pass

  def stop_crafting(self):
    if ((not self.idle) and
    self.start_time + self.item_detail.required_time == self.current_time):
      self.idle = True
      self.economy.update_stash(
        gained_stash=Counter(
          {self.item_detail.name: self.batch_size}
        ))
      if DEBUG:
        print(f'{self.item_detail.name} is done')
