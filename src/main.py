#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Main runner for World of Supply
'''


#imports
import numpy as np
from tqdm import tqdm as tqdm

from world_of_supply_environment.simple_control_policy import \
    SimpleControlPolicy
from world_of_supply_environment.world_builder import WorldBuilder
from world_of_supply_renderer.ascii_world_renderer import AsciiWorldRenderer
from world_of_supply_renderer.plot_sequence_images import \
    worldrenderer_plot_sequence_images
from world_of_supply_tools.hardware_status import print_hardware_status
from world_of_supply_tools.simulation_tracker import SimulationTracker

#   script imports
#imports

print_hardware_status()


def simulation_logic_and_rendering():
  '''
  This is the main logic of the simulation.
  '''
  episode_len = 1000
  n_episodes = 10
  world = WorldBuilder.create()

  tracker = SimulationTracker(episode_len, n_episodes, world.facilities.keys())
  with tqdm(total=episode_len * n_episodes) as pbar:
    for i in range(n_episodes):
      world = WorldBuilder.create()
      policy = SimpleControlPolicy()
      for t in range(episode_len):
        outcome = world.act(policy.compute_control(world))
        tracker.add_sample(
          episod=i,
          t=t,
          global_balance=world.economy.global_balance().total(),
          rewards={
            k: v.total() for k, v in \
               outcome.facility_step_balance_sheets.items()
          }
        )
        pbar.update(1)

  tracker.render()

  # Test rendering
  renderer = AsciiWorldRenderer()
  frame_seq = []
  world = WorldBuilder.create()
  policy = SimpleControlPolicy()
  for _ in tqdm(range(300)):
    frame = renderer.render(world)
    frame_seq.append(np.asarray(frame))
    world.act(policy.compute_control(world))

  print('Rendering the animation...')
  worldrenderer_plot_sequence_images(frame_seq)



# main
def main():
  simulation_logic_and_rendering()

# if main script
if __name__ == '__main__':
  main()
