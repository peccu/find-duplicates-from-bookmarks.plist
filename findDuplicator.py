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
  # allからlistの先頭要素と重複する物を探し
  # それとlistの残りの重複を探した物をつなげて返す
  first = list.pop(0)
  # 先頭要素と重複する物を取得する
  found = [find_duplicates(first, all)]
  if list == []:
    # 重複なし
    return found
  # 残りの要素も重複を探す
  collected = collect_duplicates(list, all)
  found.extend(collected)
  return found
