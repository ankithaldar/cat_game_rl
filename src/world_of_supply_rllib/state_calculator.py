#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''State calculator for the system'''


#imports
import numpy as np
#   script imports
from world_of_supply_environment.facility_cell import FacilityCell
from .utils import utils_agentid_producer, utils_agentid_consumer
#imports


# classes
class StateCalculator:
  '''State calculator for the system'''

  def __init__(self, env):
    self.env = env

  def world_to_state(self, world):
    state = {}
    for facility_id, facility in world.facilities.items():
      f_state = self._state(facility)
      self._add_global_features(f_state, world)
      state[utils_agentid_producer(facility_id)] = f_state
      state[utils_agentid_consumer(facility_id)] = f_state

    return self._serialize_state(state), state

  def _state(self, facility: FacilityCell):
    state = {}

    facility_type = [0] * len(self.env.facility_types)
    facility_type[self.env.facility_types[facility.__class__.__name__]] = 1
    state['facility_type'] = facility_type

    facility_id_one_hot = [0] * len(self.env.reference_world.facilities)
    facility_id_one_hot[facility.id_num - 1] = 1
    state['facility_id'] = facility_id_one_hot

    #state['balance_profit'] = self._balance_norm( facility.economy.total_balance.profit )
    #state['balance_loss'] = self._balance_norm( facility.economy.total_balance.loss )
    state['is_positive_balance'] = 1 if facility.economy.total_balance.total() > 0 else 0

    self._add_bom_features(state, facility)
    self._add_distributor_features(state, facility)
    self._add_consumer_features(state, facility)

    #state['sold_units'] = 0
    #if facility.seller is not None:
    #    state['sold_units'] = facility.seller.economy.total_units_sold

    state['storage_capacity'] = facility.storage.max_capacity
    state['storage_levels'] = [0] * self.env.n_products()
    for i, prod_id in enumerate(self.env.product_ids):
      if prod_id in facility.storage.stock_levels.keys():
        state['storage_levels'][i] = facility.storage.stock_levels[prod_id]
    state['storage_utilization'] = sum(state['storage_levels']) / state['storage_capacity']

    return state

  def _add_global_features(self, state, world):
    state['global_time'] = world.time_step / self.env.env_config['episod_duration']
    state['global_storage_utilization'] = [ f.storage.used_capacity() / f.storage.max_capacity for f in world.facilities.values() ]
    #state['balances'] = [ self._balance_norm(f.economy.total_balance.total()) for f in world.facilities.values() ]

  def _balance_norm(self, v):
    return v/1000

  def _add_bom_features(self, state, facility: FacilityCell):
    state['bom_inputs'] = [0] * self.env.n_products()
    state['bom_outputs'] = [0] * self.env.n_products()
    for i, prod_id in enumerate(self.env.product_ids):
      if prod_id in facility.bom.inputs.keys():
        state['bom_inputs'][i] = facility.bom.inputs[prod_id]
      if prod_id == facility.bom.output_product_id:
        state['bom_outputs'][i] = facility.bom.output_lot_size

  def _add_distributor_features(self, state, facility: FacilityCell):
    ##state['fleet_position'] = [0] * self.max_fleet_size
    ##state['fleet_payload'] = [0] * self.max_fleet_size
    state['distributor_in_transit_orders'] = 0
    state['distributor_in_transit_orders_qty'] = 0
    if facility.distribution is not None:
      ##for i, v in enumerate(facility.distribution.fleet):
      ##    state['fleet_position'][i] = WorldOfSupplyEnv._safe_div( v.location_pointer, v.path_len() )
      ##    state['fleet_payload'][i] = v.payload

      q = facility.distribution.order_queue
      ordered_quantity = sum([ order.quantity for order in q ])
      state['distributor_in_transit_orders'] = len(q)
      state['distributor_in_transit_orders_qty'] = ordered_quantity

  def _add_consumer_features(self, state, facility: FacilityCell):
    # which source exports which product
    state['consumer_source_export_mask'] = [0] * ( self.env.n_products() * self.env.max_sources_per_facility )
    # provide the agent with the statuses of tier-one suppliers' inventory and in-transit orders
    ##state['consumer_source_inventory'] = [0] * ( self.env.n_products() * self.max_sources_per_facility )
    state['consumer_in_transit_orders'] = [0] * ( self.env.n_products() * self.env.max_sources_per_facility )
    if facility.consumer is not None:
      for i_s, source in enumerate(facility.consumer.sources):
        for i_p, product_id in enumerate(self.env.product_ids):
          i = i_s * self.env.max_sources_per_facility + i_p
          #state['consumer_source_inventory'][i] = source.storage.stock_levels[product_id]
          if source.bom.output_product_id == product_id:
            state['consumer_source_export_mask'][i] = 1
          if source.id in facility.consumer.open_orders:
            state['consumer_in_transit_orders'][i] = facility.consumer.open_orders[source.id][product_id]

  @staticmethod
  def _safe_div(x, y):
    if y != 0:
      return x
    return 0

  def _serialize_state(self, state):
    result = {}
    for k, v in state.items():
      state_vec = np.hstack(list(v.values()))
      state_normal = ( state_vec - np.min(state_vec) )  /  ( np.max(state_vec) - np.min(state_vec) )
      result[k] = state_normal
    return result
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
