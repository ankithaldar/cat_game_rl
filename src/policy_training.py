#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Policy Training'''


# imports
import numpy as np
from tqdm import tqdm
#   script imports
import wsr_training as wsrt
from world_of_supply_rllib.utils import utils_is_consumer_agent
from world_of_supply_rllib.utils import utils_is_producer_agent
from world_of_supply_rllib.consumer_simple_policy import ConsumerSimplePolicy
from world_of_supply_rllib.producer_simple_policy import ProducerSimplePolicy
from world_of_supply_rllib.simple_policy import SimplePolicy
from world_of_supply_rllib.world_of_supply_env import WorldOfSupplyEnv
from world_of_supply_tools.simulation_tracker import SimulationTracker
from world_of_supply_renderer.ascii_world_renderer import AsciiWorldRenderer
#imports


# functions
def policy_training():
  wsrt.print_model_summaries()
  # Policy training
  #trainer = wsrt.play_baseline(n_iterations = 1)
  trainer = wsrt.train_ppo(n_iterations = 600)

  return trainer


def load_policy(trainer, policy_mode, env, agent_id):
  if policy_mode == 'baseline':
    if utils_is_producer_agent(agent_id):
      return ProducerSimplePolicy(
        env.observation_space,
        env.action_space_producer,
        SimplePolicy.get_config_from_env(env)
      )
    elif utils_is_consumer_agent(agent_id):
      return ConsumerSimplePolicy(
        env.observation_space,
        env.action_space_consumer,
        SimplePolicy.get_config_from_env(env)
      )
    else:
      raise Exception(f'Unknown agent type {agent_id}')

  if policy_mode == 'trained':
    policy_map = wsrt.policy_mapping_global.copy()
    wsrt.update_policy_map(policy_map)
    return trainer.get_policy(wsrt.create_policy_mapping_fn(policy_map)(agent_id))

def policy_evaluation(trainer):
  # Parameters of the tracing simulation
  policy_mode = 'baseline'   # 'baseline' or 'trained'
  episod_duration = 500
  steps_to_render = None #(0, episod_duration)  # (0, episod_duration) or None

  renderer = AsciiWorldRenderer()
  frame_seq = []
  env_config_for_rendering = wsrt.env_config.copy()
  env_config_for_rendering.update({
    'downsampling_rate': 1
  })

  env = WorldOfSupplyEnv(env_config_for_rendering)
  env.set_iteration(1, 1)
  print(f'Environment: Producer action space {env.action_space_producer}, Consumer action space {env.action_space_consumer}, Observation space {env.observation_space}')
  states = env.reset()
  infos = None

  policies = {}
  rnn_states = {}
  for agent_id in states.keys():
    policies[agent_id] = load_policy(trainer, policy_mode, env, agent_id)
    rnn_states[agent_id] = policies[agent_id].get_initial_state()

  # Simulation loop
  tracker = SimulationTracker(episod_duration, 1, env.agent_ids())
  for epoch in tqdm(range(episod_duration)):

    action_dict = {}
    if epoch % wsrt.env_config['downsampling_rate'] == 0:
      for agent_id, state in states.items():
        policy = policies[agent_id]
        rnn_state = rnn_states[agent_id]
        if infos is not None and agent_id in infos:
          action_dict[agent_id], rnn_state, _ = policy.compute_single_action(
            state,
            info=infos[agent_id],
            state=rnn_state
          )
        else:
          action_dict[agent_id], rnn_state, _ = policy.compute_single_action(
            state,
            state=rnn_state
          )
    states, rewards, dones, infos = env.step(action_dict)

    tracker.add_sample(
      0,
      epoch,
      env.world.economy.global_balance().total(),
      rewards
    )

    if steps_to_render is not None and epoch >= steps_to_render[0] and epoch < steps_to_render[1]:
      frame = renderer.render(env.world)
      frame_seq.append(np.asarray(frame))

  tracker.render()

  if steps_to_render is not None:
    print('Rendering the animation...')
    AsciiWorldRenderer.plot_sequence_images(frame_seq)

# functions


# main
def main():
  trainer = policy_training()
  policy_evaluation(trainer)


# if main script
if __name__ == '__main__':
  main()
