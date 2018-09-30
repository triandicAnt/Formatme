# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import io
import re
from git import Repo


def main(argv=None):
    repo = Repo(str('/Users/sudhansu/Library/Application Support/Sublime Text 3/Packages/Formatme'))
    git_modified_files = repo.git.diff('HEAD~1..HEAD', name_only=True)
    print(git_modified_files)


if __name__ == "__main__":
    exit(main())