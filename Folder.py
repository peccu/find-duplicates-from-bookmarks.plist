#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pretty print
import pprint
pp = pprint.PrettyPrinter(indent=2)
import Bookmark

def getDepth(item):
  if 'depth' in item:
    return item['depth']
  return ''

def getPath(item):
  if 'path' in item:
    return item['path']
  return ''

def getChildren(item):
  if 'children' in item:
    return item['children']
  return ''

def collect_list(parent, current):
  # このフォルダのパスと子供一覧をリストに追加
  children = Bookmark.gatherUrlOrHash(current)
  folder = {
    'path': parentPath,
    'children': children
  }
  outlist = [folder]
  # 子フォルダから再帰的にパスと子供一覧を集める
  child_list = filter(Bookmark.isFolder, Bookmark.getChildren(current))
  def collect_child(child):
    newPath = parentPath + '/' + Bookmark.getTitle(child)
    children = collect_list(newPath, child)
    outlist.extend(children)
  map(collect_child, child_list)
  return outlist

def collect(root):
  # フォルダの一覧を得る
  list = collect_list('', root)
  return list
