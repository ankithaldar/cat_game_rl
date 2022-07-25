#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
get the hardware status of the computer
'''

# imports
import multiprocessing as mp
import os

from tensorflow.python.client import device_lib

# imports


def get_hardware_status():
  '''
  get the hardware status of the computer
  '''
  # get the hardware status of the computer
  print('Number of CPU cores:', mp.cpu_count())
  stream = os.popen('cat /proc/meminfo | grep Mem')
  print(f'Memory: {stream.read()}')

  stream = os.popen('lspci | grep -i nvidia ')
  print(f'GPU status: {stream.read()}')

  print(device_lib.list_local_devices())
