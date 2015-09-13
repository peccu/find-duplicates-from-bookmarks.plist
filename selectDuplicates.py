#!/usr/bin/env python
# -*- coding: utf-8 -*-
def select_each(item):
  def select_print(path):
    print str(len(item['path'])) + ': folder:' + item['path'] + ' => ' + path
  map(select_print, item['dup'])

def select_duplicate(list):
  map(select_each, list)
