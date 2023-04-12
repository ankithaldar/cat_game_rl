#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Producer Policy'''


#imports
import numpy as np
import random as rnd
#   script imports
from .simple_policy import SimplePolicy
#imports


# classes
class ConsumerSimplePolicy(SimplePolicy):
  '''Producer Policy'''

  def __init__(self, observation_space, action_space, config):
    SimplePolicy.__init__(self, observation_space, action_space, config)

  def _action(self, facility_state, facility_state_info):
    def default_facility_control(source_id, product_id, order_qty = 4):  # (level 4 -> 8 units)
      control = [
        product_id,
        source_id,
        order_qty
      ]
      return control

    action = default_facility_control(0, 0, 0)
    if facility_state_info is not None and len(facility_state_info) > 0:
      if np.count_nonzero(facility_state_info['bom_inputs']) > 0:
        action = default_facility_control(*self._find_source(facility_state_info))
      else:
        action = default_facility_control(0, 0, 0)

    return action

  def _find_source(self, f_state_info):
    # stop placing orders when the facility ran out of money
    if f_state_info['is_positive_balance'] <= 0:
      return (0, 0, 0)

    inputs = f_state_info['bom_inputs']
    available_inventory = f_state_info['storage_levels']
    inflight_orders = np.sum(np.reshape(f_state_info['consumer_in_transit_orders'], (self.n_products, -1)), axis=0)
    booked_inventory = available_inventory + inflight_orders

    # stop placing orders when the facilty runs out of capacity
    if sum(booked_inventory) > f_state_info['storage_capacity']:
      return (0, 0, 0)

    most_neeed_product_id = None
    min_ratio = float('inf')
    for product_id, quantity in enumerate(inputs):
      if quantity > 0:
        fulfillment_ratio = booked_inventory[product_id] / quantity
        if fulfillment_ratio < min_ratio:
          min_ratio = fulfillment_ratio
          most_neeed_product_id = product_id

    exporting_sources = []
    if most_neeed_product_id is not None:
      for i in range(self.n_sources):
        if f_state_info['consumer_source_export_mask'][i*self.n_sources + most_neeed_product_id] == 1:
          exporting_sources.append(i)

    return (rnd.choice(exporting_sources), most_neeed_product_id)

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
