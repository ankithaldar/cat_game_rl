#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Get hardware status information
'''

# imports
import multiprocessing as mp
import os

import ray
from tensorflow.python.client import device_lib

# imports


def print_hardware_status():
  print('Number of CPU cores:', mp.cpu_count())
  stream = os.popen('cat /proc/meminfo | grep Mem')
  print(f'Memory: {stream.read()}')

  stream = os.popen('lspci | grep -i nvidia ')
  print(f'GPU status: {stream.read()}')

  print(device_lib.list_local_devices())

  ray.shutdown()
  ray.init(num_gpus=1)
  print(f'ray.get_gpu_ids(): {ray.get_gpu_ids()}')
  print(f'CUDA_VISIBLE_DEVICES: {os.environ.get("CUDA_VISIBLE_DEVICES")}')
