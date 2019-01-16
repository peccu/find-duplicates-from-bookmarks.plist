#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Folder

def select_each(item):
  def select_print(path):
    # print str(Folder.getDepth(item)) + ': folder:' + Folder.getPath(item) + ' => ' + path
    if item['path'] == path:
      return
    if (len(item['path']) < len(path)) or (len(item['path']) == len(path) and item['path'] < path):
      print str(Folder.getDepth(item)) + ': ' + str(len(item['path'])) + ': folder:' + item['path'] + ' => ' + path
    else:
      # print str(len(path)) + ': folder:' + path + ' => ' + item['path']
      return
  map(select_print, item['dup'])

def select_duplicate(list):
  map(select_each, list)
