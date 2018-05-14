# -*- coding: utf-8 -*-

import sublime
import sublime_plugin
import re
from collections import OrderedDict

# do you want to format the whole file or only a selection?
process_all = True

"""
Format apex code.

1.  `if (`                          < => `if (`
2.  `for (`                         < => `for (`
3.  `while (`                       < => `while (`
4.  `) {`                           < => ') {'
5.  '> {'                           < => '> {'
6.  ', +'                           < => ', ' # take care of lines ending with comma
7.  '='                             < => ' = '
8.  '+'                             < => ' + '
9.  '-'                             < => ' - '
10. '*'                             < => ' * '
11. '\'                             < => ' \ '
12. ' += '                          < => ' += '
13. ' -= '                          < => ' -= '
14. ' *= '                          < => ' *= '
15. '\='                            < => ' \= '
16. '\n'                            < => 2 or more \n to 2
17. '; *'                           < => Process semicolon
18. ' * != *'                       < => !=
19. ' +'                            < => Trailing whitespaces
20. 'for (..) {'                    < => single line loops should have { on same line
21. Handle @isTest                  < => testMethod is deprecated, replace it with @isTest.
22. Handle class name brackets      < => Add space before bracket.
23. Process if true                 < => if (true_flag) {}
24. Process if false                < => if (!false_flag) {}

Usage : Select the text you want to format and press: CRTL + B
        Or Right click and select `Formatme->Format me`

PS : Please expect a little misbehavior of the code as its not trained for few unseen circumstances.
"""

equal_dict = {
    '=  =' : ' == ',
    '+ =' : ' += ',
    '- =' : ' -= ',
    '* =' : ' *= ',
    '/ =' : ' /= ',
    '= >' : ' => ',
    '! =' : ' != ',
    '> =' : ' >= ',
    '< =' : ' <= ',
}

"""
Get leading spaces before statement

"""
def get_leading_spaces(statement):
    leading_space_count = len(statement) - len(statement.lstrip(' '))
    leading_space = ''
    while(leading_space_count > 0):
        leading_space += ' '
        leading_space_count -= 1
    return leading_space

"""
The one line for loop should have the curly bracket in the same line.
"""
def get_loop(matchedobj):
    return matchedobj.group(0).split('\n')[0] + ' {'

"""
The multiline line for loop should have the curly bracket in next line.
"""
def process_multiline_loop(matchedobj):
    stmt = matchedobj.group(0).strip('\n+')
    return stmt[:-1].strip('\n+').rstrip(' +').rstrip('\n+')+'\n' + get_leading_spaces(stmt) + '{'


"""
Remove the `testMethod` keyword from the test class methods and adding the keyword `@isTest`.
"""
def remove_test_method(matchedobj):
    prefix = '\t@isTest\n'
    return prefix + matchedobj.group(1) + ' ' + matchedobj.group(2)

"""
Handle class name brackets.
"""
def class_name(matchedobj):
    return matchedobj.group(1) + ' class ' + matchedobj.group(2).rstrip(' +') + ' {'


"""
process == true {
"""
def process_if_true(matchedobj):
    return matchedobj.group(1).rstrip(' +') + matchedobj.group(3)


"""
process == false
"""
def process_if_false(matchedobj):
     return '!' + re.compile(r'\s*==\s*').split(matchedobj.group(0))[0]

"""
process == true OR != false
"""
def process_true(matchedobj):
     return ''

"""
process equal override
"""
def process_equal_override(matchedobj):
    stmt = matchedobj.group(0)
    for k, v in equal_dict.items():
        stmt = stmt.replace(k, v)
    return stmt

"""
process equal override
"""
def process_comma(matchedobj):
    return matchedobj.group(1).rstrip(' +') + ' '

"""
process single line if else
"""
def single_line_if_else(matchedobj):
    stmt = matchedobj.group(0).lstrip()
    if '\n' in stmt and '{' not in stmt:
        stmts = matchedobj.group(0).split('\n')
        if not stmts[0]:
            del stmts[0]
        return (stmts[0] + ' {'
            + '\n' + stmts[1]
            + '\n'
            + get_leading_spaces(stmts[0]) + '}')
    return matchedobj.group(0)


regex_dict = OrderedDict([
    (r'^\s*(if|else)[^;{]+(;)', single_line_if_else),#                                  # single line if else
    (r'if *\(', r'if ('), #                                                         # if
    (r'\} *else *\{', r'} else {'), #                                               # else
    (r'\} *else *if *\(', r'} else if ('), #                                        # else if
    (r'for *\(', r'for ('), #                                                       # for
    (r'while *\(', r'while ('), #                                                   # while
    (r'> *\{', r'> {'), #                                                           # > {
    (r'\) *\{', r') {'), #                                                          # ) {
    # (r'\w{', r' {'), #                                                            # {
    # (r'} *', r'}'), #                                                             # }
    (r'(\, *[^\'\,\'|\w|\n])', process_comma), #                                       #,
    (r', *\n', r', \n'), #                                                          #, \n
    (r' *= *', r' = '), #                                                           # =
    (r'(=  =|\+ =|\- =|\* =|= >|/ =|! =|> =|< =)', process_equal_override), #       # process equal overide
    #(r' +\+ +', r' + '), #                                                         # +
    #(r' +\- +', r' - '), #                                                         # -
    (r' *\+\+ *', r'++'), #                                                         #++
    (r' *\-\- *', r'--'), #                                                         #--
    # (r' +\* +', r' * '), #                                                        # * - this is conflicting with /**
    # (r'\/\/ *', r'// '), #                                                        # //
    (r' *\=\> *', r' => '), #                                                       # =>
    (r' *\=\= *', r' == '), #                                                       # ==
    (r' *\+\= *', r' += '), #                                                       # +=
    (r' *\-\= *', r' -= '), #                                                       # -=
    (r' *\*\= *', r' *= '), #                                                       # *=
    (r' */= *', r' /= '), #                                                         # /=
    (r'\n{2, }', r'\n\n'), #                                                        # 2 or more \n to 2
    (r' *; *', r';'), #                                                            #;
    (r' *!= *', r' != '), #                                                         # !=
    (r' +$', ''), #                                                                 # remove trailing whitespaces
    (r'(.+) testMethod (.+)', remove_test_method), #                                # handle @isTest
    (r'(.+) class (.+) *{', class_name), #                                          # class name brackets should contain the space before.
    (r'(.+)(\s*==\s*true|\s*!=\s*false)(.+)', process_if_true), #                   # process if(true_flag) {}
    #(r'((\w|\.)+|(\((\w|,)*\)))+\s*==\s*false', process_if_false), #               # process == false
    (r'\s*\=\=\s*true', process_true), #                                            # process == true
    (r'\s*\!\=\s*false', process_true), #                                           # process != false
    (r'^ *(for|if|while)[^{]+{$', process_multiline_loop), #                        # process multiline loop
    (r'(for|if|while) *\(.+\)\n+ *{', get_loop),#                                   # single line loops should have { on same line
])

regex_soql = OrderedDict([
    (r'(?i)\bSELECT\b *' , r'select '),
    (r'(?i)\bFROM\b *' , r'from '),
    (r'(?i)\bWHERE\b *' , r'where '),
    (r'(?i)\bLIMIT\b *' , r'limit '),
    (r'(?i)\bGROUP\b *' , r'group '),
    (r'(?i)\bORDER by\b *' , r'order '),
    (r'(?i)\bHAVING\b *' , r'having'),
    # (r'[select (\s|\w|,|(|))+ FROM ' : select_from),
    # (r'[select (\s|\w|,|(|))+ from (\s|\w)+ WHERE ', select_where),
    # (r'[select (\s|\w|,|(|))+ from (\s|\w|\W)+ LIMIT ', select_limit),
    # (r'[select (\s|\w|,|(|))+ from (\s|\w|\W)+ ORDER BY ', select_order),
    # (r'[select (\s|\w|,|(|))+ from (\s|\w|\W)+ GROUP BY ', select_group_by),
])

class FormatmeCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        # only execute on Apex classes ending with `.cls`
        file_name = self.view.window().active_view().file_name()
        if not file_name or not file_name.endswith('.cls'):
            return
        if process_all:
            process_whole_file(self, edit) # format the entire file
        else:
            process_selection(self, edit) # format only the selected text

def process_whole_file(self, edit):
    # select all text
    all_text = self.view.substr(sublime.Region(0, self.view.size()))
    for key, value in regex_dict.items():
        all_text = re.sub(key, value, all_text, flags=re.MULTILINE)
    # for key, value in regex_soql.items():
    #     all_text = re.sub(key, value, all_text, flags=re.MULTILINE)
    self.view.replace(edit, sublime.Region(0, self.view.size()), all_text.rstrip(' +'))

def process_selection(self, edit):
    # get user selection
    for region in self.view.sel():
        # if selection not empty then
        if not region.empty():
            selected_text = self.view.substr(region)
            for key, value in regex_dict.items():
                selected_text = re.sub(key, value, selected_text, flags=re.MULTILINE)
            # replace content in view while removing any trailing whitespaces.
            self.view.replace(edit, region, selected_text.rstrip(' +'))

class RemoveDirty(sublime_plugin.EventListener):
    # "save" event hook to remove dirty window
    def on_post_save_async(self, view):
        view.run_command("revert")
