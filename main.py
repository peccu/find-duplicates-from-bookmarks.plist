#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import codecs
sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

import bookmark
import collectFolder
import findDuplicator
import selectDuplicates

def main():
  print 'loading bookmarks'
  bookmarks = bookmark.loadBookmarks(True)
  print 'collecting bookmarks'
  folders = collectFolder.collect(bookmarks)
#   pp.pprint(folders)
  print 'find duplication'
  duplicates = findDuplicator.collect_duplicates(folders, list(folders))
  print 'duplicated'
#   pp.pprint(duplicates)
  print 'found duplication'
  print
  selectDuplicates.select_duplicate(duplicates)

main()
