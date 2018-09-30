# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from git import Repo
import os

APEX_EXTENSION = 'cls'

def get_modified_and_untracked_files():
    """
    @brief      Gets the modified and untracked files.

    @return     A list of modified and untracked files.
    """
    # get the current repo
    repo = Repo(str(os.getcwd()))
    # get modified files
    git_modified_files = repo.git.diff(None, name_only=True)
    to_be_committed_files = git_modified_files.split('\n')
    # untracked (newly added files)
    to_be_committed_files.extend(repo.untracked_files)
    # filter non apex files
    files_to_modify = []
    for file_name in to_be_committed_files:
        if len(file_name) > 4 and file_name[-3:] == APEX_EXTENSION:
            files_to_modify.append(file_name)
    return files_to_modify