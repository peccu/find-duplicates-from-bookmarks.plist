#!/usr/bin/env python
# -*- coding: utf-8 -*-
import bookmark

def getPath(item):
  if 'path' in item:
    return item['path']
  return ''

def walk_folder(parent):
  print 'path ' + getPath(parent)

  # 戻りがなんか変

  def walk_folder_sub(item):
    if bookmark.isFolder(item):
      return map(walk_folder(item), bookmark.getChildren(item))
    folder = {
      'path': getPath(parent) + '/' + bookmark.getTitle(item),
      'children': map(bookmark.hash_or_url, bookmark.getChildren(item))
    }
    return folder
  return walk_folder_sub

def gen_create_folder(parent):
  def create_folder(item):
    print 'parent path: ' + getPath(parent)
    print 'parent Title: ' + bookmark.getTitle(parent)
    path = getPath(parent) + '/' + bookmark.getTitle(parent) + '/' + bookmark.getTitle(item)
    print 'generating path: ' + path
    bookmarks = map(bookmark.hash_or_url, bookmark.getChildren(item))
    # print 'generated children: '
    # pp.pprint(bookmarks)
    folder = {
      'path': path,
      'children': bookmarks
    }
    return folder
  return create_folder


# ほしいのは，フォルダの一覧
# 深さ優先で全てたどる
# 子供がいれば子供を求める
# 子供がいなくなれば抜ける


# rootが今見ているノード
# listが集まっているフォルダの一覧
# 親のパスをどうやって引き継ぐか
def func(node, list):
  if not bookmark.hasChild(node):
    return None
  if bookmark.isBookmark(node):
    return None
  if bookmark.isFolder(node):
    return create_folder(node)
  for i in bookmark.getChildren(node):
    list.extend(func(i, list))
