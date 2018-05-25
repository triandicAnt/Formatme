# -*- coding: utf-8 -*-

import unittest
from regexme import *
import re

def format_me(text):
    for key, value in regex_dict.items():
        text = re.sub(key, value, text, flags=re.MULTILINE)
    return text

class CodeBlockTest:
    def __init__(self):
        self.__original_code_block = ""
        self.__expected_code_block = ""

    def build_original_code_block(self, str):
        if self.__original_code_block != "":
            str = "\n" + str
        self.__original_code_block += str

    def build_expected_code_block(self, str):
        if self.__expected_code_block != "":
            str = "\n" + str
        self.__expected_code_block += str

    def evaluate(self, unittest):
        unittest.assertEquals(format_me(self.__original_code_block), self.__expected_code_block)

    def reset(self):
        self.__original_code_block = ""
        self.__expected_code_block = ""

class TestFormatMe(unittest.TestCase):

    def test_simple(self):
        self.assertNotEqual('java', 'apex')

    def test_single_line_if_else_1(self):
        cb = CodeBlockTest()
        # build original text
        cb.build_original_code_block('if (i am hungry)')
        cb.build_original_code_block('    Syso(i watch netflix);')
        #build expected text
        cb.build_expected_code_block('if (i am hungry) {')
        cb.build_expected_code_block('    Syso(i watch netflix);')
        cb.build_expected_code_block('}')
        cb.evaluate(self)

    ''' TODO
    def test_rule2(self):
    def test_rule3(self):
    def test_rule4(self):
    def test_rule5(self):
    def test_rule6(self):
    def test_rule7(self):
    def test_rule8(self):
    def test_rule9(self):
    def test_rule10(self):
    def test_rule11(self):
    def test_rule12(self):
    def test_rule13(self):
    def test_rule14(self):
    def test_rule15(self):
    def test_rule16(self):
    def test_rule17(self):
    def test_rule18(self):
    def test_rule19(self):
    def test_rule20(self):
    def test_rule21(self):
    def test_rule22(self):
    def test_rule23(self):
    def test_rule24(self):
    def test_rule25(self):
    '''

    def test_if_false_26(self):
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
            self.assertEqual(format_me(key), value)

    '''
    def test_rule27(self):
    def test_rule28(self):
    def test_rule29(self):
    def test_rule30(self):
    def test_rule31(self):
    def test_rule32(self):
    def test_rule33(self):
    def test_rule34(self):
    def test_rule35(self):
    def test_rule36(self):
    def test_rule37(self):
    '''

    def test_if_else_same_line_38(self):
        test_data_dict = {
                    '''if (i am hungry)
    I will sleep;
else if
    I will run;''' : '''if (i am hungry) {
    I will sleep;
} else if {
    I will run;
}''',

'''                    if (sth) {
                        hello from the other side;
                    }
                    else {
                        earth says goodbye!;
                    }''' : '''                    if (sth) {
                        hello from the other side;
                    } else {
                        earth says goodbye!;
                    }''',

'''if (sth) {
    hello from the other side;
}
else if {
    earth says goodbye!;
}''' : '''if (sth) {
    hello from the other side;
} else if {
    earth says goodbye!;
}''',
        }
        for key, value in test_data_dict.items():
            self.assertEqual(format_me(key), value)

    def test_if_else_same_line_01(self):
        test_data_dict = {
        'if (sth) return;' : '''if (sth) {
    return;
}'''
        }
        for key, value in test_data_dict.items():
            self.assertEqual(format_me(key), value)

    def test_process_double_and_41_42(self):
        test_data_dict = {
        '''if( monkey     && monkey)
    fight;
else if (monkey
        && gorilla||  ape) {
    discuss politics;
}''': '''if ( monkey && monkey) {
    fight;
} else if (monkey
        && gorilla || ape) {
    discuss politics;
}'''
        }
        for key, value in test_data_dict.items():
            self.assertEqual(format_me(key), value)

if __name__ == '__main__':
    unittest.main()