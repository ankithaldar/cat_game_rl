#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
World Status Printer
'''

#imports
from collections import Counter

from multipledispatch import dispatch

#   script imports
from world_of_supply_environment.facility_cell import FacilityCell
from world_of_supply_environment.storage_unit import StorageUnit
from world_of_supply_environment.transport import Transport
from world_of_supply_environment.world import World

from .acsii_progress_bar import utils_ascii_progress_bar

#imports

# functions
def asciiworldstatusprinter_cell_status(cell):
  return [f'{cell.__class__.__name__} ({cell.x}, {cell.y})']

def asciiworldstatusprinter_counter(counter) -> str:
  # this removes zero counters
  return dict(counter + Counter())


@dispatch(World)
def asciiworldstatusprinter_status(world: World) -> list:
  status = [
    [
      'World:',
      [
        f'Time step: {world.time_step}',
        f'Global balance: {world.economy.global_balance()}'
      ]
    ]
  ]
  for f in world.facilities.values():
    status.append(asciiworldstatusprinter_status(f))

  return status


@dispatch(FacilityCell)
def asciiworldstatusprinter_status(facility: FacilityCell) -> list:
  status = [f'{facility.id} ({facility.x}, {facility.y})']

  substatuses = [f'Balance: {facility.economy.total_balance}']
  if facility.distribution is not None:
    u = facility.distribution
    transport_status = [
        f'{asciiworldstatusprinter_status(t)}' +
      f'{utils_ascii_progress_bar(t.location_pointer, t.path_len()-1, 5)}'
      for t in u.fleet
      ]
    substatuses.append( ['Fleet:', transport_status] )
    inbound_orders = [
      f'{order.product_id}:{order.quantity} at '+\
      f'${order.unit_price} -> {order.destination.id}' \
        for order in u.order_queue
    ]
    substatuses.append( [f'Inbound orders:', inbound_orders] )
    substatuses.append( [f'Current unit price: ${u.economy.unit_price}'] )
    substatuses.append( [f'Penalties: wrong orders {u.economy.total_wrong_order_penalties}, pending orders {u.economy.total_pending_order_penalties}'] )

  if facility.consumer is not None:
    in_transit_units_total = sum(sum(facility.consumer.open_orders.values(), Counter()).values())
    outbound_orders = [ f'{src} -> {asciiworldstatusprinter_counter(order)}' for src, order in facility.consumer.open_orders.items()]
    substatuses.append( [f'Outbound orders ({in_transit_units_total} units):', outbound_orders] )
    substatuses.append( [f'Total units purchased: {facility.consumer.economy.total_units_purchased}'] )
    substatuses.append( [f'Total units received: {facility.consumer.economy.total_units_received}'] )

  if facility.seller is not None:
    substatuses.append( [f'Current unit price: ${facility.seller.economy.unit_price}'] )
    substatuses.append( [f'Current demand: {facility.seller.economy.market_demand(facility.seller.economy.unit_price)}'] )
    substatuses.append( [f'Total units sold: {facility.seller.economy.total_units_sold}'] )


  substatuses.append([
    'Storage:', asciiworldstatusprinter_status(facility.storage)
  ])
  status.append(substatuses)
  return status


@dispatch(Transport)
def asciiworldstatusprinter_status(t: Transport) -> str:
  status = None
  if t.destination is None:
    status = 'IDLE'
  else:
    if t.location_pointer == 0 and t.payload == 0:
      status = f'LOAD {t.product_id}:{t.requested_quantity}' + \
       f'-> {t.destination.id}'
    if t.payload > 0 and t.step > 0:
      status = f'MOVE {t.product_id}:{t.payload} -> {t.destination.id}'
    if t.location_pointer == len(t.path) - 1 and t.payload > 0:
      status = f'UNLD {t.product_id}:{t.payload} -> {t.destination.id}'
    if t.step < 0 and t.payload == 0:
      status = f'BACK {t.destination.id} -> home'
  return status


@dispatch(StorageUnit)
def asciiworldstatusprinter_status(storage: StorageUnit) -> list:
  return [
    f'Usage: {utils_ascii_progress_bar(storage.used_capacity(), storage.max_capacity)}',
    f'Storage cost/unit: {storage.economy.unit_storage_cost}',
    f'Inventory: {asciiworldstatusprinter_counter(storage.stock_levels)}'
  ]

# functions
