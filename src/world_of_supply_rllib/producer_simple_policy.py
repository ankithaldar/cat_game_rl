#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Producer Policy'''


#imports
import numpy as np
#   script imports
from .simple_policy import SimplePolicy
from world_of_supply_environment.steel_factory_cell import SteelFactoryCell
from world_of_supply_environment.lumber_factory_cell import LumberFactoryCell
from world_of_supply_environment.toy_factory_cell import ToyFactoryCell
from world_of_supply_environment.warehouse_cell import WarehouseCell
from world_of_supply_environment.retailer_cell import RetailerCell
#imports


# classes
class ProducerSimplePolicy(SimplePolicy):
  '''Producer Policy'''

  def __init__(self, observation_space, action_space, config):
    SimplePolicy.__init__(self, observation_space, action_space, config)

    facility_types = config['facility_types']
    self.unit_prices = [0] * len(facility_types)
    unit_price_map = {
      SteelFactoryCell.__name__: 0,  # $400
      LumberFactoryCell.__name__: 0, # $400
      ToyFactoryCell.__name__: 2,    # $1000
      WarehouseCell.__name__: 4,     # $1400
      RetailerCell.__name__: 6       # $1800
    }

    for f_class, f_id in facility_types.items():
      self.unit_prices[ f_id ] = unit_price_map[f_class]

  def _action(self, facility_state, facility_state_info):
    def default_facility_control(unit_price):
      control = [
        unit_price,    # unit_price
        2,             # production_rate (level 2 -> 4 units)
      ]
      return control

    action = default_facility_control(0)
    if facility_state_info is not None and len(facility_state_info) > 0:
      unit_price = self.unit_prices[ np.flatnonzero( facility_state_info['facility_type'] )[0] ]
      action = default_facility_control(unit_price)

    return action
# classes


# functions
def function_name():
  pass
# functions


# main
def main():
  pass


# if main script
if __name__ == '__main__':
  main()
