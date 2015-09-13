#!/usr/bin/env python
# -*- coding: utf-8 -*-
def dup_filter(children):
  # childrenと同じ物だけを集めるフィルタ
  def filter(item):
    return set(item['children']) == set(children)
  return filter

def dup_map(item):
  # pathだけを集めるmapper
  return item['path']

def find_duplicates(needle, list):
  # listからneedle(フォルダ)の子供と同じ子供をもつフォルダを集める
  path = needle['path']
  filtered = filter(dup_filter(needle['children']), list)
  dup = map(dup_map, filtered)
  return {'path': path, 'dup': dup}
#   return [
#     {
#       'path': '/fol/hoge/fuga',
#       'dups': [
#         'https://google.com/',
#         'https://google.co.jp/',
#         'https://google.com/?q=some+keywords'
#       ]
#     }
#   ]

def collect_duplicates(list, all):
  # allからlistの先頭要素と重複する物を探し，それとlistの残りの重複を探した物をつなげて返す
  first = list.pop(0)
  found = [find_duplicates(first, all)]
  if list == []:
    return found
  collected = collect_duplicates(list, all)
  found.extend(collected)
  return found
