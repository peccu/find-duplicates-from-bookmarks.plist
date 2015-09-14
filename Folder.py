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
    'depth': getDepth(parent),
    'path': getPath(parent),
    'children': children
  }
  outlist = [folder]
  # 子フォルダから再帰的にパスと子供一覧を集める
  child_list = filter(Bookmark.isFolder, Bookmark.getChildren(current))
  def collect_child(child):
    newPath = getPath(parent) + '/' + Bookmark.getTitle(child)
    child_folder = {
      'depth': getDepth(parent) + 1,
      'path': newPath
    }
    children = collect_list(child_folder, child)
    outlist.extend(children)
  map(collect_child, child_list)
  return outlist

def collect(root):
  # フォルダの一覧を得る
  folder = {
    'depth': 0,
    'path': ''
  }
  list = collect_list(folder, root)
  return list
