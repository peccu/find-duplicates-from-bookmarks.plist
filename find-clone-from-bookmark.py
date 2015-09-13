#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import sys
import codecs
sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

from os.path import expanduser

# binary plist
import biplist
# pretty print
import pprint
pp = pprint.PrettyPrinter(indent=2)

def getTitle(item):
  if 'Title' in item:
    return item['Title']
  return ''

def getUrl(item):
  if 'URLString' in item:
    return item['URLString']
  return ''

def isFolder(item):
  if item == None:
    return false
  if item == []:
    return false
  return (not 'URLString' in item) and ('Children' in item)

def isBookmark(item):
  if item == None:
    return false
  if item == []:
    return false
  return 'URLString' in item

def isFolderOrBookmark(item):
  return isFolder(item) or isBookmark(item)

def getChildren(item):
  if 'Children' in item:
    return filter(isFolderOrBookmark, item['Children'])
  return []

import hashlib
import bencode

def calcHash(list):
  # 配列からmd5ハッシュ値を求める
  # http://stackoverflow.com/a/5419072
  return hashlib.md5(bencode.bencode(list)).hexdigest()

def generateHash(folder):
  folders = filter(isFolder, getChildren(folder))
  folders_hash = map(generateHash, folders)
  bookmarks = filter(isBookmark, getChildren(folder))
  bookmarks_url = map(getUrl, bookmarks)
  bookmarks_url.extend(folders_hash)
  return calcHash(bookmarks_url)

def hash_or_url(item):
  # ブックマークならURLを返し，フォルダならハッシュ値を返す
  if isBookmark(item):
    return getUrl(item)
  if isFolder(item):
    return generateHash(item)

def getPath(item):
  if 'path' in item:
    return item['path']
  return ''

def walk_folder(parent):
  print 'path ' + getPath(parent)

  # 戻りがなんか変

  def walk_folder_sub(item):
    if isFolder(item):
      return map(walk_folder(item), getChildren(item))
    folder = {
      'path': getPath(parent) + '/' + getTitle(item),
      'children': map(hash_or_url, getChildren(item))
    }
    return folder
  return walk_folder_sub

def gen_create_folder(parent):
  def create_folder(item):
    print 'parent path: ' + getPath(parent)
    print 'parent Title: ' + getTitle(parent)
    path = getPath(parent) + '/' + getTitle(parent) + '/' + getTitle(item)
    print 'generating path: ' + path
    bookmarks = map(hash_or_url, getChildren(item))
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
  if not hasChild(node):
    return None
  if isBookmark(node):
    return None
  if isFolder(node):
    return create_folder(node)
  for i in getChildren(node):
    list.extend(func(i, list))


def collect(root):
  # フォルダの一覧を得る
  # pp.pprint(root)
  
  # 子供のフォルダ一覧を取得
  folders = filter(isFolder, getChildren(root))
  print 'folder count: ' + str(len(folders))
  # foldersだと子供を集められるけど，親のパスが未設定でずっとパスが空になる？
  def printing(item):
    print 'has path: ' + getPath(item)
    print 'has title: ' + getTitle(item)
  map(printing, folders)

  # 
  folder = map(gen_create_folder(root), folders)
  print 'path: ' + getPath(folder)
  pp.pprint(map(getPath, folder))
  list = folder
  rest = map(collect, folders)
  list.extend(rest)
  return list
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
#   print "path: " + path
#   pp.pprint(needle)
  filtered = filter(dup_filter(needle['children']), list)
#   print "filtered"
#   pp.pprint(filtered)
  dup = map(dup_map, filtered)
#   print "mapped"
#   pp.pprint(dup)
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
#   print 'first'
#   pp.pprint(first)
  found = [find_duplicates(first, all)]
#   print 'found'
#   pp.pprint(found)
  if list == []:
#     print 'list is null'
    return found
#   print 'list is not null'
  collected = collect_duplicates(list, all)
#   print 'collected'
#   pp.pprint(collected)
  found.extend(collected)
#   print 'collect and extended'
#   pp.pprint(found)
  return found

def select_each(item):
  def select_print(path):
    print str(len(item['path'])) + ': folder:' + item['path'] + ' => ' + path
  map(select_print, item['dup'])

def select_duplicate(list):
  map(select_each, list)

#   print str(len('/patho/to/folder')) + ' /path/to/folder : /path/to/duplicates'

def main():
  print 'loading bookmarks'
  home = expanduser("~")
  bookmarks = biplist.readPlist(home + "/Library/Safari/Bookmarks.plist")
  print 'collecting bookmarks'
  folders = collect(bookmarks)
#   pp.pprint(folders)
  print 'find duplication'
  duplicates = collect_duplicates(folders, list(folders))
  print 'duplicated'
#   pp.pprint(duplicates)
  print 'found duplication'
  print
  select_duplicate(duplicates)

main()
sys.exit()
