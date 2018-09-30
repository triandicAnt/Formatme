# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import io
import regexme as rm
from git_utils import get_modified_and_untracked_files

def format_files(file_name):
    """
    @brief      Formats the files.

    @param      file_name  The file name.

    @return     status based on files modification.
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
    # apply regex to all files
    status = 0
    for file_name in get_modified_and_untracked_files():
        status |= format_files(file_name)
    return status


if __name__ == "__main__":
    exit(main())
