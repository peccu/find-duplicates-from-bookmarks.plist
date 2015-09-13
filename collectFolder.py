#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pretty print
import pprint
pp = pprint.PrettyPrinter(indent=2)
import bookmark
import Folder

def collect(root):
  # フォルダの一覧を得る
  # pp.pprint(root)
  
  # 子供のフォルダ一覧を取得
  folders = filter(bookmark.isFolder, bookmark.getChildren(root))
  print 'folder count: ' + str(len(folders))
  # foldersだと子供を集められるけど，親のパスが未設定でずっとパスが空になる？
  def printing(item):
    print 'has path: ' + Folder.getPath(item)
    print 'has title: ' + bookmark.getTitle(item)
  map(printing, folders)

  # 
  folder = map(Folder.gen_create_folder(root), folders)
  print 'path: ' + Folder.getPath(folder)
  pp.pprint(map(Folder.getPath, folder))
  list = folder
  rest = map(collect, folders)
  list.extend(rest)
#   return list
#   mapped = map(walk_folder(root), getChildren(root))
#   print 'hoge'
#   pp.pprint(mapped)
#   return mapped

  # pathと子供のurlを求める
  # フォルダがあれば同階層に引き上げる
  # フォルダ内のURLの集合をmd5で表現すれば比較の回数を減らせそう
  return [
    {
      'path': '/fol/hoge/fuga',
      'children': [
        'https://google.com/',
        'https://google.co.jp/',
        'https://google.com/?q=some+keywords'
      ]
    },
    {
      'path': '/fol/hoge/fuga/piyo',
      'children': [
        'https://google.com/',
        'https://google.co.jp/',
        'https://google.com/?q=some+keywords'
      ]
    }
  ]
