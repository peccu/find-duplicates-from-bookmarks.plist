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
  bookmarks = Bookmark.loadBookmarks()
  print 'collecting bookmarks'
  folders = Folder.collect(bookmarks)
  print 'find duplication'
  duplicates = findDuplicator.collect_duplicates(folders, list(folders))
  print
  selectDuplicates.select_duplicate(duplicates)

main()
