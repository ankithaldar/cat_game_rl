#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''utils for rllib module'''


#imports
#   script imports
#imports

# functions
def utils_agentid_producer(facility_id):
  return facility_id + 'p'

def utils_agentid_consumer(facility_id):
  return facility_id + 'c'

def utils_is_producer_agent(agent_id):
  return agent_id[-1] == 'p'

def utils_is_consumer_agent(agent_id):
  return agent_id[-1] == 'c'

def utils_agentid_to_fid(agent_id):
  return agent_id[:-1]
# functions
