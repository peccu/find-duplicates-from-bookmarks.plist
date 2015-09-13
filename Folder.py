#!/usr/bin/env python
# -*- coding: utf-8 -*-
import bookmark

def getPath(item):
  if 'path' in item:
    return item['path']
  return ''

