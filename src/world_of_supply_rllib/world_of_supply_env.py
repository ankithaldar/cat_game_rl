#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Multi-Agent Environment'''


#imports
from ray.rllib.env.multi_agent_env import MultiAgentEnv
from gym.spaces import MultiDiscrete, Box
import numpy as np
#   script imports
from .state_calculator import StateCalculator
from .reward_calculator import RewardCalculator
from .action_calculator import ActionCalculator
from world_of_supply_environment.world_builder import WorldBuilder
from world_of_supply_environment.world import World
from .utils import utils_agentid_producer, utils_agentid_consumer
#imports


# classes
class WorldOfSupplyEnv(MultiAgentEnv):
  '''Multi-Agent Environment'''

  def __init__(self, env_config):
    self.env_config = env_config
    self.reference_world = WorldBuilder.create()
    self.current_iteration = 0
    self.n_iterations = 0

    self.product_ids = self._product_ids()
    self.max_sources_per_facility = 0
    self.max_fleet_size = 0
    self.facility_types = {}
    facility_class_id = 0
    for f in self.reference_world.facilities.values():
      if f.consumer is not None:
        sources_num = len(f.consumer.sources)
        if sources_num > self.max_sources_per_facility:
          self.max_sources_per_facility = sources_num

      if f.distribution is not None:
        if len(f.distribution.fleet) > self.max_fleet_size:
          self.max_fleet_size = len(f.distribution.fleet)

      facility_class = f.__class__.__name__
      if facility_class not in self.facility_types:
        self.facility_types[facility_class] = facility_class_id
        facility_class_id += 1

    self.state_calculator = StateCalculator(self)
    self.reward_calculator = RewardCalculator(env_config)
    self.action_calculator = ActionCalculator(self)

    self.action_space_producer = MultiDiscrete([
      8,                             # unit price
      6,                             # production rate level
    ])

    self.action_space_consumer = MultiDiscrete([
      self.n_products(),                           # consumer product id
      self.max_sources_per_facility,               # consumer source id
      6                                            # consumer_quantity
    ])

    example_state, _ = self.state_calculator.world_to_state(
      world=self.reference_world
    )
    state_dim = len(list(example_state.values())[0])
    self.observation_space = Box(
      low=0.00,
      high=1.00,
      shape=(state_dim, ),
      dtype=np.float64
    )

  def reset(self):
    self.world = WorldBuilder.create(80, 16)
    self.time_step = 0
    state, _ = self.state_calculator.world_to_state(self.world)
    return state

  def step(self, action_dict):
    control = self.action_calculator.action_dictionary_to_control(
      action_dict=action_dict,
      world=self.world
    )

    outcome = self.world.act(control)
    self.time_step += 1

    # churn through no-action cycles
    for _ in range(self.env_config['downsampling_rate'] - 1):
      nop_outcome = self.world.act(World.Control({}))
      self.time_step += 1

      balances = outcome.facility_step_balance_sheets
      for agent_id in balances.keys():
        balances[agent_id] = balances[agent_id] + nop_outcome.facility_step_balance_sheets[agent_id]

    rewards = self.reward_calculator.calculate_reward(self, outcome)

    seralized_states, info_states = self.state_calculator.world_to_state(self.world)

    is_done = self.time_step >= self.env_config['episod_duration']
    dones = { agent_id: is_done for agent_id in seralized_states.keys() }
    dones['__all__'] = is_done

    return seralized_states, rewards, dones, info_states

  def agent_ids(self):
    agents = []
    for f_id in self.world.facilities.keys():
      agents.append(utils_agentid_producer(f_id))
    for f_id in self.world.facilities.keys():
      agents.append(utils_agentid_consumer(f_id))
    return agents

  def set_iteration(self, iteration, n_iterations):
    self.current_iteration = iteration
    self.n_iterations = n_iterations

  def n_products(self):
    return len(self._product_ids())

  def _product_ids(self):
    product_ids = set()
    for f in self.reference_world.facilities.values():
      product_ids.add(f.bom.output_product_id)
      product_ids.update(f.bom.inputs.keys())
    return list(product_ids)
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
