#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import bencode
from os.path import expanduser
# binary plist
import biplist

def getBookmarkFilePath():
  home = expanduser("~")
  return home + "/Library/Safari/Bookmarks.plist"

def loadBookmarks(dummy = False):
  if(dummy):
    import dummy
    return dummy.bookmarks
  bookmarkFile = getBookmarkFilePath()
  return biplist.readPlist(bookmarkFile)

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

def calcHash(list):
  # 配列からmd5ハッシュ値を求める
  # http://stackoverflow.com/a/5419072
  return hashlib.md5(bencode.bencode(list)).hexdigest()

def gatherUrlOrHash(folder):
  folders = filter(isFolder, getChildren(folder))
  folders_hash = map(generateHash, folders)
  bookmarks = filter(isBookmark, getChildren(folder))
  bookmarks_url = map(getUrl, bookmarks)
  bookmarks_url.extend(folders_hash)
  return bookmarks_url

def generateHash(folder):
  bookmarks_url = gatherUrlOrHash(folder)
  return calcHash(bookmarks_url)

def hash_or_url(item):
  # ブックマークならURLを返し，フォルダならハッシュ値を返す
  if isBookmark(item):
    return getUrl(item)
  if isFolder(item):
    return generateHash(item)
