#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Folder

def select_each(item):
  def select_print(path):
    print str(len(Folder.getPath(item))) + ': folder:' + Folder.getPath(item) + ' => ' + path
  map(select_print, item['dup'])

def select_duplicate(list):
  map(select_each, list)
