# -*- coding: utf-8 -*-

import sublime
import sublime_plugin
import re
from collections import OrderedDict

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

Usage : Select the text you want to format and press: CRTL + B
        Or Right click and select `Formatme->Format me`

PS : Please expect a little misbehavior of the code as its not trained for few unseen circumstances.
"""

"""
The one line for loop should have the curly bracket in the same line.
"""
def get_loop(matchedobj):
    return matchedobj.group(0).split('\n')[0] + ' {'


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


regex_dict = OrderedDict([
    (r'if *\(', r'if ('), #                                                         # if
    (r'\} *else *\{', r'} else {'), #                                               # else
    (r'\} *else *if *\(', r'} else if ('), #                                        # else if
    (r'for *\(', r'for ('), #                                                       # for
    (r'while *\(', r'while ('), #                                                   # while
    (r'> *\{', r'> {'), #                                                           # > {
    (r'\) *\{', r') {'), #                                                          # ) {
    # (r'\w{', r' {'), #                                                            # {
    # (r'} *', r'}'), #                                                             # }
    (r', *', r', '), #                                                              #,
    (r', *\n', r', \n'), #                                                          #, \n
    #(r' += +', r' = '), #                                                          # =
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
    #(r' *\\= *', r' \\= '), #                                                      # \=
    (r'\n{2, }', r'\n\n'), #                                                        # 2 or more \n to 2
    (r' *; *', r'; '), #                                                            #;
    (r' * != *', r' != '), #                                                        # !=
    (r' +$', ''), #                                                                 # remove trailing whitespaces
    (r'(for|if|while) \(.+\)\n+\s*{',get_loop),#                                    # single line loops should have { on same line
    (r'(.+) testMethod (.+)', remove_test_method), #                                # handle @isTest
    (r'(.+) class (.+) *{', class_name), #                                          # class name brackets should contain the space before.
])



class FormatmeCommand(sublime_plugin.TextCommand):

     def run(self, edit):
        if not file_name.endswith('.cls'): # only execute on Apex classes
            return
        # select all text
        all_text = self.view.substr(sublime.Region(0, self.view.size()))
        for key, value in regex_dict.items():
            all_text = re.sub(key, value, all_text, flags=re.MULTILINE)
        self.view.replace(edit, sublime.Region(0, self.view.size()), all_text.rstrip(' +'))
        # The below code is for selected text
        # get user selection
        # for region in self.view.sel():
        #     # if selection not empty then
        #     if not region.empty():
        #         selected_text = self.view.substr(region)
        #         for key, value in regex_dict.items():
        #             selected_text = re.sub(key, value, selected_text, flags=re.MULTILINE)
        #         # replace content in view while removing any trailing whitespaces.
        #         self.view.replace(edit, region, selected_text.rstrip(' +'))


class RemoveDirty(sublime_plugin.EventListener):

  # "save" event hook to remove dirty window
  def on_post_save_async(self, view):
    view.run_command("revert")
