# -*- coding: utf-8 -*-

import unittest
import regexme as rm

class TestFormatMe(unittest.TestCase):
    def test_simple(self):
        self.assertNotEqual('java', 'apex')
        self.assertEquals('sfdc', 'sfdc')

    # def test_if_else_same_line_01(self):
    #     cb = CodeBlockTest()
    #     # if/else statement should be on separate line of condition with curly braces
    #     cb.build_original_code_block('if (sth) return;', True)
    #     cb.build_original_code_block('else doSomething();')
    #     cb.build_expected_code_block('if (sth) {', True)
    #     cb.build_expected_code_block('    return;')
    #     cb.build_expected_code_block('} else {')
    #     cb.build_expected_code_block('    doSomething();')
    #     cb.build_expected_code_block('}')
    #     cb.evaluate(self)

    def test_single_line_if_else_02(self):
        cb = CodeBlockTest()
        # if/else should be enclosed by curly braces
        cb.build_original_code_block('if (i am hungry)', True)
        cb.build_original_code_block('    foo(i watch netflix);')
        cb.build_original_code_block('else')
        cb.build_original_code_block('    return;')
        cb.build_expected_code_block('if (i am hungry) {', True)
        cb.build_expected_code_block('    foo(i watch netflix);')
        cb.build_expected_code_block('} else {')
        cb.build_expected_code_block('    return;')
        cb.build_expected_code_block('}')
        cb.evaluate(self)

    def test_one_space_before_open_parenthesis_03(self):
        cb = CodeBlockTest()
        # test 'if ('
        cb.build_original_code_block('if(a) {', True)
        cb.build_expected_code_block('if (a) {', True)
        # test 'for ('
        cb.build_original_code_block('for(stuff) {', True)
        cb.build_expected_code_block('for (stuff) {', True)
        # test 'while ('
        cb.build_original_code_block('while  (true) {', True)
        cb.build_expected_code_block('while (true) {', True)
        # test catch ('
        cb.build_original_code_block('}catch  (Exception e) {', True)
        cb.build_expected_code_block('} catch (Exception e) {', True)
        cb.evaluate(self)

    def test_one_space_after_close_curly_04(self):
        cb = CodeBlockTest()
        # test '} else'
        cb.build_original_code_block('}else{', True)
        cb.build_expected_code_block('} else {', True)
        # test '} catch'
        cb.build_original_code_block('}  catch(', True)
        cb.build_expected_code_block('} catch (', True)
        cb.evaluate(self)

    def test_one_space_before_open_curly_05(self):
        cb = CodeBlockTest()
        # test 'else {'
        cb.build_original_code_block('}else{', True)
        cb.build_expected_code_block('} else {', True)
        # test 'try {'
        cb.build_original_code_block('try  {', True)
        cb.build_expected_code_block('try {', True)
        # test '> {'
        cb.build_original_code_block('Map<X,X>{', True)
        cb.build_expected_code_block('Map<X,X> {', True)
        # test ') {'
        cb.build_original_code_block('for(stuff){', True)
        cb.build_expected_code_block('for (stuff) {', True)
        cb.evaluate(self)

    # # def test_one_space_between_else_if_06(self):
    # ''' TODO
    # def test_rule2(self):
    # def test_rule3(self):
    # def test_rule4(self):
    # def test_rule5(self):
    # def test_rule6(self):
    # def test_rule7(self):
    # def test_rule8(self):
    # def test_rule9(self):
    # def test_rule10(self):
    # def test_rule11(self):
    # def test_rule12(self):
    # def test_rule13(self):
    # def test_rule14(self):
    # def test_rule15(self):
    # def test_rule16(self):
    # def test_rule17(self):
    # def test_rule18(self):
    # def test_rule19(self):
    # def test_rule20(self):
    # def test_rule21(self):
    # def test_rule22(self):
    # def test_rule23(self):
    # def test_rule24(self):
    # def test_rule25(self):
    # '''

    def test_if_false_26(self):
        cb = CodeBlockTest()
        # `flag == false` ==> `!flag`
        cb.build_original_code_block('if (flag == false) {', True)
        cb.build_expected_code_block('if (!flag) {', True)
        # `flag != true` ==> `!flag`
        cb.build_original_code_block('if (flag != true) {', True)
        cb.build_expected_code_block('if (!flag) {', True)
        # `list.isEmpty() == false` ==> `!list.isEmpty()`
        cb.build_original_code_block('if (list.isEmpty() == false {', True)
        cb.build_expected_code_block('if (!list.isEmpty() {', True)
        #  test multiple statements in 1 line
        cb.build_original_code_block('if (x == false && list.isEmpty() != true) {', True)
        cb.build_expected_code_block('if (!x && !list.isEmpty()) {', True)
        cb.evaluate(self)

    # '''
    # def test_rule27(self):
    # def test_rule28(self):
    # def test_rule29(self):
    # def test_rule30(self):
    # def test_rule31(self):
    # def test_rule32(self):
    # def test_rule33(self):
    # def test_rule34(self):
    # def test_rule35(self):
    # def test_rule36(self):
    # def test_rule37(self):
    # '''

    def test_if_else_same_line_38(self):
        cb = CodeBlockTest()
        # test that if statements with no brackets get surrounded with curly brackets
        cb.build_original_code_block('if (i am hungry)', True)
        cb.build_original_code_block('    I will sleep;')
        cb.build_original_code_block('else')
        cb.build_original_code_block('    I will run;')
        cb.build_expected_code_block('if (i am hungry) {', True)
        cb.build_expected_code_block('    I will sleep;')
        cb.build_expected_code_block('} else {')
        cb.build_expected_code_block('    I will run;')
        cb.build_expected_code_block('}')
        # test that `else` gets moved to the line of the previous close curly bracket
        cb.build_original_code_block('if (sth) {', True)
        cb.build_original_code_block('    hello from the other side;')
        cb.build_original_code_block('}')
        cb.build_original_code_block('else {')
        cb.build_original_code_block('    earth says goodbye!;')
        cb.build_original_code_block('}')
        cb.build_expected_code_block('if (sth) {', True)
        cb.build_expected_code_block('    hello from the other side;')
        cb.build_expected_code_block('} else {')
        cb.build_expected_code_block('    earth says goodbye!;')
        cb.build_expected_code_block('}')
        # test that `else if` gets moved to the line of the previous close curly bracket
        cb.build_original_code_block('if (sth) {', True)
        cb.build_original_code_block('    hello from the other side;')
        cb.build_original_code_block('}')
        cb.build_original_code_block('else if (sth else) {')
        cb.build_original_code_block('    earth says goodbye!;')
        cb.build_original_code_block('}')
        cb.build_expected_code_block('if (sth) {', True)
        cb.build_expected_code_block('    hello from the other side;')
        cb.build_expected_code_block('} else if (sth else) {')
        cb.build_expected_code_block('    earth says goodbye!;')
        cb.build_expected_code_block('}')
        cb.evaluate(self)

    def test_process_double_and_41_42(self):
        cb = CodeBlockTest()
        # single space around `&&`
        cb.build_original_code_block('a    &&b;', True)
        cb.build_expected_code_block('a && b;', True)
        # single space around `||`
        cb.build_original_code_block('x    ||y;', True)
        cb.build_expected_code_block('x || y;', True)
        # single space around `&&` and `||` in a multiline statement
        cb.build_original_code_block('if (sth', True)
        cb.build_original_code_block('    &&  A')
        cb.build_original_code_block('    ||B)')
        cb.build_original_code_block('{')
        cb.build_expected_code_block('if (sth', True)
        cb.build_expected_code_block('    && A')
        cb.build_expected_code_block('    || B)')
        cb.build_expected_code_block('{')
        cb.evaluate(self)

class CodeBlockTest:
    def __init__(self):
        self.__original_list = []
        self.__expected_list = []
        self.__original_code_block = ""
        self.__expected_code_block = ""

    def build_original_code_block(self, str, start_new_block_flag = False):
        if start_new_block_flag:
            self.__original_list.append(self.__original_code_block)
            self.__original_code_block = ""
        if self.__original_code_block != "":
            str = "\n" + str
        self.__original_code_block += str

    def build_expected_code_block(self, str, start_new_block_flag = False):
        if start_new_block_flag:
            self.__expected_list.append(self.__expected_code_block)
            self.__expected_code_block = ""
        if self.__expected_code_block != "":
            str = "\n" + str
        self.__expected_code_block += str

    def evaluate(self, unittest):
        if len(self.__original_list) != len(self.__expected_list):
            print("Different sized code blocks")
            print(self.__original_list)
            print(self.__expected_list)
            return
        if self.__original_code_block != "":
            self.__original_list.append(self.__original_code_block)
            self.__original_code_block = ""
        if self.__expected_code_block != "":
            self.__expected_list.append(self.__expected_code_block)
            self.__expected_code_block = ""
        for i in range(len(self.__original_list)):
            o = rm.run(self.__original_list[i])
            e = self.__expected_list[i]
            result = unittest.assertEquals(o, e)

if __name__ == '__main__':
    unittest.main()