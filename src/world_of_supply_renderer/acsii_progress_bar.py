#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Acsii progress bar
'''

# imports
# imports


def utils_ascii_progress_bar(done, limit, bar_lenght_char=15):
  if limit == 0:
    done_chars = 0
  else:
    done_chars = round(min(done, limit)/limit*bar_lenght_char)
  bar = ['='] * (done_chars)
  return ''.join(
    bar + (['-'] * (bar_lenght_char - done_chars)) + [f' {done}/{limit}']
  )
