# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import io
import re
from git import Repo
import os

APEX_EXTENSION = 'cls'

def main(argv=None):
    # get the current repo
    repo = Repo(str(os.getcwd()))
    git_modified_files = repo.git.diff(None, name_only=True)
    # modified files and untracked files
    to_be_committed_files = git_modified_files.split('\n')
    to_be_committed_files.extend(repo.untracked_files)
    # filter non apex files
    for file_name in to_be_committed_files:
        if len(file_name) <= 4 or file_name[-3:] != APEX_EXTENSION:
            to_be_committed_files.remove(file_name)
    print(to_be_committed_files)
    return 0


if __name__ == "__main__":
    exit(main())
