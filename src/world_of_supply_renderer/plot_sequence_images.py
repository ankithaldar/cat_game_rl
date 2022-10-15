#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
plot images in sequence
'''

import os

# imports
import matplotlib.pyplot as plt
from IPython.display import HTML, display
from matplotlib import animation

# imports

APPLICATION_PATH = os.path.abspath(
  os.path.abspath(os.path.dirname(__file__)) + '/../' + '/../'
)


def worldrenderer_plot_sequence_images(image_array):
  '''
  Display images sequence as an animation in jupyter notebook
  Args:
  image_array(numpy.ndarray):
    image_array.shape equal to (num_images, height, width, num_channels)
  '''
  dpi = 72.0
  xpixels, ypixels = image_array[0].shape[:2]
  fig = plt.figure(figsize=(ypixels/dpi, xpixels/dpi), dpi=dpi)
  im = plt.figimage(image_array[0])

  def animate(i):
    im.set_array(image_array[i])
    return (im,)

  anim = animation.FuncAnimation(
    fig,
    animate,
    frames=len(image_array),
    interval=200,
    repeat_delay=1,
    repeat=True
  )
  display(HTML(anim.to_html5_video()))

  anim.save(
    os.path.join(
      APPLICATION_PATH,
      'charts',
      'worldrender.mp4',
    ),
    writer=animation.FFMpegWriter(fps=5)
  )
