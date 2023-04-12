#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Reward calculator for the system'''


#imports
import statistics
#   script imports
from .utils import utils_agentid_producer, utils_agentid_consumer
#imports


# classes
class RewardCalculator:
  '''Reward calculator for the system'''

  def __init__(self, env_config):
    self.env_config = env_config

  def calculate_reward(self, world, step_outcome) -> dict:
    return self._retailer_profit(world, step_outcome)

  def _retailer_profit(self, env, step_outcome):
    retailer_revenue = {
      f_id: sheet.profit
      for f_id, sheet in step_outcome.facility_step_balance_sheets.items()
      if 'Retailer' in f_id
    }
    global_reward_retail_revenue = statistics.mean(retailer_revenue.values())

    global_profits = {
      f_id: sheet.total()
      for f_id, sheet in step_outcome.facility_step_balance_sheets.items()
    }
    global_reward_total_profit = statistics.mean( global_profits.values() )

    w_gl_profit = 0.0 + 0.8 * (env.current_iteration / env.n_iterations)

    global_reward_producer = (1 - w_gl_profit) * global_reward_retail_revenue + w_gl_profit * global_reward_total_profit
    global_reward_consumer = (1 - w_gl_profit) * global_reward_retail_revenue + w_gl_profit * global_reward_total_profit

    wp = self.env_config['global_reward_weight_producer']
    wc = self.env_config['global_reward_weight_consumer']
    producer_reward_by_facility = { f_id: wp * global_reward_producer + (1 - wp) * sheet.total() for f_id, sheet in step_outcome.facility_step_balance_sheets.items() }
    consumer_reward_by_facility = { f_id: wc * global_reward_consumer + (1 - wc) * sheet.total() for f_id, sheet in step_outcome.facility_step_balance_sheets.items() }

    rewards_by_agent = {}
    for f_id, reward in producer_reward_by_facility.items():
      rewards_by_agent[utils_agentid_producer(f_id)] = reward
    for f_id, reward in consumer_reward_by_facility.items():
      rewards_by_agent[utils_agentid_consumer(f_id)] = reward
    return rewards_by_agent
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
