#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Simulation Tracker
'''

import os

import matplotlib.pyplot as plt
import numpy as np

APPLICATION_PATH = os.path.abspath(
  os.path.abspath(os.path.dirname(__file__)) + '/../' + '/../'
)

class SimulationTracker:
  '''
  Simulation Tracker
  '''
  def __init__(self, eposod_len, n_episods, facility_names):
    self.episod_len = eposod_len
    self.global_balances = np.zeros((n_episods, eposod_len))
    self.facility_names = list(facility_names)
    self.step_balances = np.zeros((n_episods, eposod_len, len(facility_names)))

  def add_sample(self, episod, t, global_balance, rewards):
    self.global_balances[episod, t] = global_balance
    # ensure facility order is preserved
    assert self.facility_names == list(rewards.keys())
    self.step_balances[episod, t, :] = np.array(list(rewards.values()))

  def render(self):
    _, axs = plt.subplots(3, 1, figsize=(16, 12))
    x = np.linspace(0, self.episod_len, self.episod_len)

    axs[0].set_title('Global balance')
    axs[0].plot(x, self.global_balances.T)

    axs[1].set_title('Cumulative Sum of Rewards')
    axs[1].plot(x, np.cumsum(np.sum(self.step_balances, axis = 2), axis = 1).T )

    axs[2].set_title('Reward Breakdown by Agent (One Episod)')
    axs[2].plot(x, np.cumsum(self.step_balances[0, :, :], axis = 0))
    axs[2].legend(self.facility_names, loc='upper left')

    # plt.show()

    plt.savefig(
      os.path.join(
        APPLICATION_PATH,
        'charts',
        'simulationtracker.pdf'
      )
    )
