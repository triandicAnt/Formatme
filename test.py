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
        input_string = '''if (i am hungry)
    Syso(i watch netflix);'''
        expected_string = '''if (i am hungry) {
    Syso(i watch netflix);
}'''
        self.assertEqual(format_me(self, input_string), expected_string)

    def test_if_false(self):
        #26) convert `x == false|z != true ` to `!x`
        test_data_dict = {
        '''if (flag == false) { // bad''' : '''if (!flag) { // bad''',
        '''if (flag != true) {  // bad''' : '''if (!flag) {  // bad''',
        '''if (list.isEmpty() == false) {
                 // sth
            }'''                          : '''if (!list.isEmpty()) {
                 // sth
            }''',
        '''if (x == false && list.isEmpty() != true) {''' : '''if (!x && !list.isEmpty()) {''',
        '''if (flag != true) {  // bad''' : '''if (!flag) {  // bad''',
        }
        for key, value in test_data_dict.items():
            self.assertEqual(format_me(self, key), value)


if __name__ == '__main__':
    unittest.main()