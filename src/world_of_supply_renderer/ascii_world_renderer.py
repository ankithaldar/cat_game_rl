#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
ASCII World Rendering
'''

import math
import os

# import PIL
import yaml
from PIL import Image, ImageDraw, ImageFont

from world_of_supply_environment.facility_cell import FacilityCell
from world_of_supply_environment.lumber_factory_cell import LumberFactoryCell
# imports
from world_of_supply_environment.railroad_cell import RailroadCell
from world_of_supply_environment.retailer_cell import RetailerCell
from world_of_supply_environment.steel_factory_cell import SteelFactoryCell
from world_of_supply_environment.toy_factory_cell import ToyFactoryCell
from world_of_supply_environment.warehouse_cell import WarehouseCell
from world_of_supply_renderer.ascii_world_status_printer import \
    asciiworldstatusprinter_status

# imports

APPLICATION_PATH = os.path.abspath(
    os.path.abspath(os.path.dirname(__file__)) + '/../' + '/../'
)


class AsciiWorldRenderer:
  '''
  ASCII World Rendering
  '''
  def render(self, world):
    ascii_layers = []

    def new_layer():
      return [[' ' for x in range(world.size_x)] for y in range(world.size_y)]

    # print infrastructure (background)
    layer = new_layer()
    for y in range(world.size_y):
      for x in range(world.size_x):
        c = world.grid[x][y]
        if isinstance(c, RailroadCell):
          layer[y][x] = self.railroad_sprite(x, y, world.grid)
    ascii_layers.append(layer)

    # print vechicles
    layer = new_layer()
    for y in range(world.size_y):
      for x in range(world.size_x):
        c = world.grid[x][y]
        if isinstance(c, FacilityCell) and c.distribution is not None:
          for vechicle in c.distribution.fleet:
            if vechicle.is_enroute():
              location = vechicle.current_location()
              layer[location[1]][location[0]] = '*'
    ascii_layers.append(layer)

    # print facilities (foreground)
    layer = new_layer()
    for y in range(world.size_y):
      for x in range(world.size_x):
        c = world.grid[x][y]
        if isinstance(c, SteelFactoryCell):
          layer[y][x] = 'S'
        if isinstance(c, LumberFactoryCell):
          layer[y][x] = 'L'
        if isinstance(c, ToyFactoryCell):
          layer[y][x] = 'T'
        if isinstance(c, WarehouseCell):
          layer[y][x] = 'W'
        if isinstance(c, RetailerCell):
          layer[y][x] = 'R'
    ascii_layers.append(layer)

    # print ascii on canvas
    # print(APPLICATION_PATH)
    margin_side = 150
    margin_top = 20
    font = ImageFont.truetype(
      os.path.join(APPLICATION_PATH, 'assets', 'FiraMono-Bold.ttf'),
      24
    )

    test_text = '\n'.join(''.join(row) for row in ascii_layers[0])
    test_img = Image.new('RGB', (10, 10))
    test_canvas = ImageDraw.Draw(test_img)
    (map_w, map_h) = test_canvas.multiline_textsize(test_text, font=font)
    img_w = map_w + 2 * margin_side
    img_h = int(map_h * 4.0)

    img = Image.new('RGB', (img_w, img_h), color='#263238')
    canvas = ImageDraw.Draw(img)

    color_theme = ['#80A7FB',  # pale blue
                   '#FFCB6B',  # yellow
                   '#C3E88D',  # light green
                   '#FF5370']  # red
    for layer, color in zip(ascii_layers, color_theme):
      text = '\n'.join(''.join(row) for row in layer)
      canvas.multiline_text(
        (
          margin_side,
          margin_top
        ),
        text,
        font=font,
        fill=color
      )

    # print logo
    logo = Image.open(
      os.path.join(APPLICATION_PATH, 'assets', 'world-of-supply-logo.png'),
      'r'
    ).convert('RGBA')
    logo.thumbnail(
      (
        int(img_w/5),
        int(img_h/10)
      ),
      Image.ANTIALIAS
    )
    img.paste(logo, (int(img_w/2 - img_w/10), 0), mask=logo)

    # print status
    font = ImageFont.truetype(
      os.path.join(APPLICATION_PATH, 'assets', 'monaco.ttf'),
      11
    )
    status = asciiworldstatusprinter_status(world)
    n_columns = 3
    n_rows = math.ceil(len(status) / n_columns)
    col_wide = img_w/n_columns * 0.90
    for i in range(n_columns):
      column_left_x = img_w/2 - (n_columns * col_wide)/2 + col_wide*i
      canvas.multiline_text(
        (
          column_left_x,
          map_h * 1.1
        ),
        self.to_yaml(status[i*n_rows: (i+1)*n_rows]),
        font=font, fill='#BBBBBB'
      )

    return img

  def to_yaml(self, obj):
    return yaml.dump(obj).replace("'", '')

  def railroad_sprite(self, x, y, grid):
    top = False
    bottom = False
    left = False
    right = False

    if isinstance(grid[x-1][y], RailroadCell):
      left = True
    if isinstance(grid[x+1][y], RailroadCell):
      right = True
    if isinstance(grid[x][y-1], RailroadCell):
      top = True
    if isinstance(grid[x][y+1], RailroadCell):
      bottom = True

    # Sprites: ╔╗╚╝╠╣╦╩╬═║
    if (top or bottom) and not right and not left:
      return '║'
    if (right or left) and not top and not bottom:
      return '═'
    if top and not bottom and right and not left:
      return '╚'
    if top and not bottom and not right and left:
      return '╝'
    if bottom and not top and right and not left:
      return '╔'
    if bottom and not top and not right and left:
      return '╗'
    if top and bottom and not right and left:
      return '╣'
    if top and bottom and right and not left:
      return '╠'
    if top and not bottom and right and left:
      return '╩'
    if bottom and not top and right and left:
      return '╦'
    if top and bottom and right and left:
      return '╬'
