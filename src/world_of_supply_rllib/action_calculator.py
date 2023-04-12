#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Action Calculator for the system'''


#imports
from collections import defaultdict
import numpy as np
import random as rnd
#   script imports
from .utils import (
  utils_agentid_to_fid,
  utils_is_producer_agent,
  utils_is_consumer_agent
)
from world_of_supply_environment.world import World
from world_of_supply_environment.facility_cell import FacilityCell
from world_of_supply_environment.simple_control_policy import SimpleControlPolicy
#imports


# classes
class ActionCalculator:
  '''Action Calculator for the system'''

  def __init__(self, env):
    self.env = env

  def action_dictionary_to_control(self, action_dict, world):
    actions_by_facility = defaultdict(list)
    for agent_id, action in action_dict.items():
      f_id = utils_agentid_to_fid(agent_id)
      actions_by_facility[f_id].append((agent_id, action))

    controls = {}
    for f_id, actions in actions_by_facility.items():
      controls[f_id] = self._actions_to_control( world.facilities[ f_id ], actions )

    return World.Control(facility_controls = controls)


  def _actions_to_control(self, facility, actions):
    unit_price_mapping = {
      0: 400,
      1: 600,
      2: 1000,
      3: 1200,
      4: 1400,
      5: 1600,
      6: 1800,
      7: 2000
    }

    small_controls_mapping = {
      0: 0,
      1: 2,
      2: 4,
      3: 6,
      4: 8,
      5: 10
    }

    def get_or_zero(arr, i):
      if i < len(arr):
        return arr[i]
      else:
        return 0

    n_facility_sources = len(facility.consumer.sources) if facility.consumer is not None else 0

    control = FacilityCell.Control(
      unit_price = 0,
      production_rate = 0,
      consumer_product_id = 0,
      consumer_source_id = 0,
      consumer_quantity = 0
    )
    for agent_id, action in actions:
      action = np.array(action).flatten()

      if utils_is_producer_agent(agent_id):
        control.unit_price = unit_price_mapping[ get_or_zero(action, 0) ]
        control.production_rate = small_controls_mapping[ get_or_zero(action, 1) ]

      if utils_is_consumer_agent(agent_id):

        product_id = self.env.product_ids[ get_or_zero(action, 0) ]
        exporting_sources = SimpleControlPolicy.find_exporting_sources(facility, product_id)
        source_id_auto = 0 if len(exporting_sources)==0 else rnd.choice( exporting_sources )

        #source_id_policy = int( round(get_or_zero(action, 1) * (n_facility_sources-1) / self.env.max_sources_per_facility) )
        source_id_policy = min(get_or_zero(action, 1), n_facility_sources-1)

        control.consumer_product_id = product_id
        control.consumer_source_id =  source_id_policy   # source_id_auto
        control.consumer_quantity = small_controls_mapping[ get_or_zero(action, 2) ]

    return control

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
