# -*- coding: utf-8 -*-

import sublime
import sublime_plugin
import re
from collections import OrderedDict

"""
Format apex code.

1.  `if(`    =>      `if (`
2.  `for(`   =>      `for (`
3.  `while(` =>      `while (`
4.  `){`     =>      ') {'
5.  '>{'     =>      '> {'
6.  ', +'    =>      ', ' # take care of lines ending with comma
7.  '='      =>      ' = '
8.  '+'      =>      ' + '
9.  '-'      =>      ' - '
10. '*'      =>      ' * '
11. '\'      =>      ' \ '
12. '+='     =>      ' += '
13. '-='     =>      ' -= '
14. '*='     =>      ' *= '
15. '\='     =>      ' \= '
16. '\n'     =>      2 or more \n to 2
17. '; *'    =>      Process semicolon
18. ' *!= *' =>      !=
19. ' +'     =>      Trailing whitespaces

Usage : Select the text you want to format and press: CRTL + B
        Or Right click and select `Formatme->Format me`

PS : Please expect a little misbehavior of the code as its not trained for few unseen circumstances.
"""

regex_dict = OrderedDict([
    (r'if *\(' , r'if ('),                    # if
    (r'\} *else *\{' , r'} else {'),          # else
    (r'\} *else *if *\(' , r'} else if ('),   # else if
    (r'for *\(' , r'for ('),                  # for
    (r'while *\(' , r'while ('),              # while
    (r'> *\{' , r'> {'),                      # >{
    (r'\) *\{' , r') {'),                     # ){
    # (r'\w{' , r' {'),                         # {
    # (r'} *' , r'}'),                          # }
    (r', *' , r', '),                         # ,
    (r', *\n' , r',\n'),                      # , \n
    #(r' += +' , r' = '),                     # =
    #(r' +\+ +' , r' + '),                     # +
    #(r' +\- +' , r' - '),                     # -
    (r' *\+\+ *' , r'++'),                    # ++
    (r' *\-\- *' , r'--'),                    # --
    # (r' +\* +' , r' * '),                   # * - this is conflicting with /**
    # (r'\/\/ *' , r'// '),                     # //
    (r' *\=\> *' , r' => '),                  # =>
    (r' *\=\= *' , r' == '),                    # ==
    (r' *\+\= *' , r' += '),                  # +=
    (r' *\-\= *' , r' -= '),                  # -=
    (r' *\*\= *' , r' *= '),                  # *=
    #(r' *\\= *' , r' \\= '),                  # \=
    (r'\n{2,}' , r'\n\n'),                    # 2 or more \n to 2
    (r' *; *' , r'; '),                       #;
    (r' *!= *' , r' != '),                    # !=
    (r' +$' , '')                             #remove trailing whitespaces
])

class FormatmeCommand(sublime_plugin.TextCommand):

     def run(self, edit):
        # get user selection
        all_text = self.view.substr(sublime.Region(0, self.view.size()))
        print(all_text)
        for key, value in regex_dict.items():
            all_text = re.sub(key, value, all_text, flags=re.MULTILINE)
        self.view.replace(edit, sublime.Region(0, self.view.size()), all_text.rstrip(' +'))
        # for region in self.view.sel():
        #     # if selection not empty then
        #     if not region.empty():
        #         selected_text = self.view.substr(region)
        #         for key, value in regex_dict.items():
        #             selected_text = re.sub(key, value, selected_text, flags=re.MULTILINE)
        #         # replace content in view while removing any trailing whitespaces.
        #         self.view.replace(edit, region, selected_text.rstrip(' +'))
