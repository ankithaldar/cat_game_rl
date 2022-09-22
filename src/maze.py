#!/usr/bin/env python
# -*- coding: utf-8 -*-


#  Copyright (c) 2022, Ankit Haldar
#  All rights reserved.
#
#  This source code is licensed under the BSD-style license found in the
#  LICENSE file in the root directory of this source tree. An additional grant
#  of patent rights can be found in the PATENTS file in the same directory.


'''
Doc String for the module
'''

__author__ = "Ankit 'Helder' Haldar"
__version__ = '0.1'


import random
from dataclasses import dataclass

#imports
import numpy as np

#   script imports
#imports


# - States
#   > 0 means free
#   > -1 means not traversable
#   > 1 means goal


# https://youtu.be/psDlXfbe6ok?t=8700



# classes
@dataclass
class Agent:
  '''
  Maze Agent
  '''
  i:int=0
  j:int=0

  @property
  def loc(self):
    return (self.i, self.j)

  def v_move(self, direction):
    direction = 1 if direction > 0 else -1
    return Agent(self.i + direction, self.j)

  def h_move(self, direction):
    direction = 1 if direction > 0 else -1
    return Agent(self.i, self.j + direction)

  def __repr__(self) -> str:
    return str(self.loc)


@dataclass
class Maze:
  '''
  Maze Builder
  '''
  rows:int=4
  columns:int=4

  def generate_maze(self):
    a = np.zeros(shape=(self.rows, self.columns))
    a[-1, -1] =  1
    a[0, 1:3] = -1
    a[1, 2:]  = -1
    # a[2, 0]   = -1
    a[3, 0:2] = -1

    return a

class QLearning:
  def __init__(self, n_states, n_actions, lr=0.01, discount_factor=0.99):
    self.q = np.zeros(shape=(n_states, n_actions))
    self.lr = lr
    self.df = discount_factor

  def update(self, st, at, rt, st1):
    self.q[st, at] = (1 - self.lr) * self.q[st, at] + self.lr * (
      rt + self.df * np.max(self.q[st1])
    )


class MazeEnv:
  '''
  Environment for Maze RL
  '''

  def __init__(self, rows:int=4, columns:int=4):
    # super(MazeEnv, self).__init__()
    self.env = Maze(rows, columns).generate_maze()
    self.mousy = Agent(0, 0)

  def state_for_agent(self, a):
    _, nc = self.env.shape
    return a.i * nc + a.j

  def in_bounds(self, i, j):
    nr, nc = self.env.shape
    return 0 <= i < nr and 0 <= j < nc

  def agent_in_bounds(self, a):
    return self.in_bounds(a.i, a.j)

  def agent_dient(self, a):
    return not self.env[a.i, a.j] == -1

  def is_valid_new_agent(self, m):
    return self.agent_in_bounds(m) and self.agent_dient(m)

  @property
  def all_actions(self):
    a = self.mousy
    return [
        a.v_move(1),
        a.v_move(-1),
        a.h_move(1),
        a.h_move(-1)
    ]

  def compute_possible_moves(self):
    # a = self.mousy
    moves = self.all_actions
    return [
      (m, idx) for idx, m in enumerate(moves) if self.is_valid_new_agent(m)
    ]

  def do_a_move(self, a):
    assert self.is_valid_new_agent(a), "Mousy can't go there"
    self.mousy = a
    return 10 if self.has_won() else -0.1

  def has_won(self):
    a = self.mousy
    return self.env[a.i, a.j] == 1

  def visualize(self):
    assert self.agent_in_bounds(self.mousy), 'Mousy is out of bounds'
    e = self.env.copy()
    m = self.mousy
    e[m.i, m.j] = 6
    print(e)
    print('--------------------------------')

# classes


# functions
def function_name():
  pass
# functions


# main
def main():

  rows, columns = 5, 5

  # training
  q_lr = QLearning(rows*columns, 4)

  for i in range(5000):
    m = MazeEnv(rows, columns)
    final_score = 0
    while not m.has_won():
      moves = m.compute_possible_moves()
      random.shuffle(moves)
      move , move_idx = moves[0]

      # calculate q value
      at = move_idx
      st = m.state_for_agent(m.mousy)
      rt = m.do_a_move(move)
      final_score += rt

      st1 = m.state_for_agent(m.mousy)

      q_lr.update(st, at, rt, st1)

      # final_score += m.do_a_move(move)
      # print(f'took move idx {move_idx}')

      # m.mousy = moves[0]

      # m.visualize()

    # print(f'finished episode {i+1} with score {final_score}')

  # print(q_lr.q)
  # print(f'final score:{final_score}')
  # print('done')

  # training

  # exploitation
  m = MazeEnv(rows, columns)
  score = 0
  while not m.has_won():
    rt = m.do_a_move(
      m.all_actions[
        np.argmax(
          q_lr.q[m.state_for_agent(m.mousy)]
        )
      ]
    )
    m.visualize()
    score += rt
  print(f'final score: {score}')



# if main script
if __name__ == '__main__':
  main()
  print(f'\n\nCoded by {__author__}')

