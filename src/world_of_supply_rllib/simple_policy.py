#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Simple policy'''


#imports
from ray.rllib.policy.policy import Policy
#   script imports
#imports


# classes
class SimplePolicy(Policy):
  '''Simple policy'''

  def __init__(self, observation_space, action_space, config):
    Policy.__init__(self, observation_space, action_space, config)
    self.action_space_shape = action_space.shape
    self.n_products = config['number_of_products']
    self.n_sources = config['number_of_sources']

  def compute_actions(
    self,
    obs_batch,
    state_batches=None,
    prev_action_batch=None,
    prev_reward_batch=None,
    info_batch=None,
    episodes=None,
    **kwargs
  ):

    if info_batch is None:
      action_dict = [ self._action(f_state, None) for f_state in obs_batch ], [], {}
    else:
      action_dict = [self._action(f_state, f_state_info) for f_state, f_state_info in zip(obs_batch, info_batch)], [], {}

    return action_dict

  def learn_on_batch(self, samples):
    '''No learning.'''
    return {}

  def get_weights(self):
    pass

  def set_weights(self, weights):
    pass

  @staticmethod
  def get_config_from_env(env):
    return {
      'facility_types': env.facility_types,
      'number_of_products': env.n_products(),
      'number_of_sources': env.max_sources_per_facility
    }
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
