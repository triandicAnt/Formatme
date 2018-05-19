# -*- coding: utf-8 -*-

import unittest
from regexme import *
import re


def format_me(self, text):
    for key, value in regex_dict.items():
        text = re.sub(key, value, text, flags=re.MULTILINE)
    return text

class TestFormatMe(unittest.TestCase):

    def test_simple(self):
        self.assertNotEqual('java', 'apex')

    def test_single_line_if_else(self):
        """
        #1)  single line if/else should be enclosed with curly braces
        """
        input_string = '''
                        if (i am hungry)
                            Syso(i watch netflix);
                        '''
        expected_string = '''
                        if (i am hungry) {
                            Syso(i watch netflix);
                        }
                        '''
        self.assertNotEqual(format_me(self, input_string), expected_string)


if __name__ == '__main__':
    unittest.main()