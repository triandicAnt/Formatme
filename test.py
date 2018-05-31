# -*- coding: utf-8 -*-

import unittest
import regexme as rm

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
        formatted_text = rm.run(self.__original_code_block)
        unittest.assertEquals(formatted_text, self.__expected_code_block)

class TestFormatMe(unittest.TestCase):

    def test_simple(self):
        self.assertNotEqual('java', 'apex')
        self.assertEquals('sfdc', 'sfdc')

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
        cb = CodeBlockTest()
        # `flag == false` ==> `!flag`
        cb.build_original_code_block('if (flag == false) {')
        cb.build_expected_code_block('if (!flag) {')
        # `flag != true` ==> `!flag`
        cb.build_original_code_block('if (flag != true) {')
        cb.build_expected_code_block('if (!flag) {')
        # `list.isEmpty() == false` ==> `!list.isEmpty()`
        cb.build_original_code_block('if (list.isEmpty() == false {')
        cb.build_expected_code_block('if (!list.isEmpty() {')
        #  test multiple statements in 1 line
        cb.build_original_code_block('if (x == false && list.isEmpty() != true) {')
        cb.build_expected_code_block('if (!x && !list.isEmpty()) {')
        cb.evaluate(self)

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
        cb = CodeBlockTest()
        # test that if statements with no brackets get surrounded with curly brackets
        cb.build_original_code_block('if (i am hungry)')
        cb.build_original_code_block('    I will sleep;')
        cb.build_original_code_block('else')
        cb.build_original_code_block('    I will run;')
        cb.build_expected_code_block('if (i am hungry) {')
        cb.build_expected_code_block('    I will sleep;')
        cb.build_expected_code_block('} else {')
        cb.build_expected_code_block('    I will run;')
        cb.build_expected_code_block('}')
        # test that `else` gets moved to the line of the previous close curly bracket
        cb.build_original_code_block('if (sth) {')
        cb.build_original_code_block('    hello from the other side;')
        cb.build_original_code_block('}')
        cb.build_original_code_block('else {')
        cb.build_original_code_block('    earth says goodbye!;')
        cb.build_original_code_block('}')
        cb.build_expected_code_block('if (sth) {')
        cb.build_expected_code_block('    hello from the other side;')
        cb.build_expected_code_block('} else {')
        cb.build_expected_code_block('    earth says goodbye!;')
        cb.build_expected_code_block('}')
        # test that `else if` gets moved to the line of the previous close curly bracket
        cb.build_original_code_block('if (sth) {')
        cb.build_original_code_block('    hello from the other side;')
        cb.build_original_code_block('}')
        cb.build_original_code_block('else if (sth else) {')
        cb.build_original_code_block('    earth says goodbye!;')
        cb.build_original_code_block('}')
        cb.build_expected_code_block('if (sth) {')
        cb.build_expected_code_block('    hello from the other side;')
        cb.build_expected_code_block('} else if (sth else) {')
        cb.build_expected_code_block('    earth says goodbye!;')
        cb.build_expected_code_block('}')
        cb.evaluate(self)

    def test_if_else_same_line_01(self):
        cb = CodeBlockTest()
        #
        cb.build_original_code_block('if (sth) return;')
        cb.build_expected_code_block('if (sth) {')
        cb.build_expected_code_block('    return;')
        cb.build_expected_code_block('}')
        cb.evaluate(self)

    def test_process_double_and_41_42(self):
        cb = CodeBlockTest()
        # single space around `&&`
        cb.build_original_code_block('a    &&b;')
        cb.build_expected_code_block('a && b;')
        # single space around `||`
        cb.build_original_code_block('x    ||y;')
        cb.build_expected_code_block('x || y;')
        # single space around `&&` and `||` in a multiline statement
        cb.build_original_code_block('if (sth')
        cb.build_original_code_block('    &&  A')
        cb.build_original_code_block('    ||B)')
        cb.build_original_code_block('{')
        cb.build_expected_code_block('if (sth')
        cb.build_expected_code_block('    && A')
        cb.build_expected_code_block('    || B)')
        cb.build_expected_code_block('{')
        cb.evaluate(self)

if __name__ == '__main__':
    unittest.main()