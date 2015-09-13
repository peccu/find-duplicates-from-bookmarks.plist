#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import codecs
sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

import Bookmark
import Folder
import findDuplicator
import selectDuplicates

def main():
  print 'loading bookmarks'
  sys.stdout.flush()
  bookmarks = Bookmark.loadBookmarks()
  print 'collecting bookmarks'
  sys.stdout.flush()
  folders = Folder.collect(bookmarks)
  print 'found folders: ' + str(len(folders))
  print 'find duplication'
  sys.stdout.flush()
  duplicates = findDuplicator.collect_duplicates(folders, list(folders))
  print
  sys.stdout.flush()
  selectDuplicates.select_duplicate(duplicates)

main()
