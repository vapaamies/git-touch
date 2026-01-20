#!/usr/bin/env python

"""
    Copyright © 2026 Владислав Джавадов (Vladislav Javadov)
    Distributed under terms of BSD license: http://touch.cantorsys.com/license
"""

from fnmatch import fnmatchcase
import git

def get(path='', pattern='release/*') -> str:
  version = '0.0'
  build = ''

  with git.Repo(path, search_parent_directories=True) as repo:
    for tag in repo.tags:
      if fnmatchcase(tag.name, pattern):
        version = tag.name.split('/')[-1]
        break

    for commit in repo.iter_commits(paths=path):
      build = commit.committed_datetime.strftime('%y%j') + '-' + commit.hexsha[:len(repo.git.rev_parse(commit, short=True))]
      break

  return (version + '.' + build) if build else version

if __name__ == '__main__': # patcher
  PATTERN = b'$(' + b'VERSION' + b')' # don't trigger on self
  USAGE = 'Usage: {} file-mask [tag-mask]'

  from sys import argv
  from glob import glob

  me = argv.pop(0)
  if argv:
    files = argv.pop(0)
    tags = argv.pop(0) if argv else ''

    for name in glob(files, recursive=True):
      with open(name, 'rb') as file:
        body = file.read()
      if body.find(PATTERN) >= 0:
        version = get(name, tags) if tags else get(name)
        with open(name, 'wb') as file:
          file.write(body.replace(PATTERN, version.encode()))
        print(name, '→', version)
  else:
    print(USAGE.format(me))