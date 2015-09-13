#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Folder

def dup_filter(children):
  # childrenと同じ物だけを集めるフィルタ
  def filter(item):
    return set(item['children']) == set(children)
  return filter

def find_duplicates(needle, list):
  # listからneedle(フォルダ)の子供と同じ子供をもつフォルダを集める
  path = needle['path']
  # 子供と一致するかを判断するフィルタを作る
  child_filter = dup_filter(needle['children'])
  # 一覧から一致する物だけを集める
  filtered = filter(child_filter, list)
  # pathだけをdupに格納する
  dup = map(Folder.getPath, filtered)
  return {'path': path, 'dup': dup}

def collect_duplicates(list, all):
  def find_duplicate(item):
    return find_duplicates(item, all)
  found = map(find_duplicate, list)
  return found
