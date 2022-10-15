#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Create distribution unit with given configuration.
'''

# imports
from .distribution_unit import DistributionUnit
from .transport import Transport

# imports


def create_distribution_unit(facility, config):
  return DistributionUnit(
    facility,
    config.fleet_size,
    DistributionUnit.Economy(
      wrong_order_penatly = config.wrong_order_penatly,
      pending_order_penalty = config.pending_order_penalty
    ),
    Transport.Economy(config.unit_transport_cost)
  )
