# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import io
import re
from git import Repo
import os
import regexme as rm

APEX_EXTENSION = 'cls'

def format_files(file_name):
    """
    @brief      Formats the files

    @param      file_name  The file name

    @return     { description_of_the_return_value }
    """
    try:
        content = io.open(file_name).read()
        if not content:
            return 0
        new_content = rm.run(content)
        if new_content != content:
            with io.open(file_name, 'w') as changed_file:
                changed_file.write(new_content)
                print('\"{file_name}\" : is modified by Regex Expression.'.format(file_name=file_name))
            return 1
        else:
            return 0
    except Exception as e:
        print(e)
        return 1

def main(argv=None):
    # get the current repo
    repo = Repo(str(os.getcwd()))
    git_modified_files = repo.git.diff(None, name_only=True)
    # modified files and untracked files
    to_be_committed_files = git_modified_files.split('\n')
    to_be_committed_files.extend(repo.untracked_files)
    # filter non apex files
    files_to_modify = []
    for file_name in to_be_committed_files:
        if len(file_name) > 4 and file_name[-3:] == APEX_EXTENSION:
            files_to_modify.append(file_name)
    # apply regex to all files
    status = 0
    for file_name in files_to_modify:
        status |= format_files(file_name)
    return status


if __name__ == "__main__":
    exit(main())
