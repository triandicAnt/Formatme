# -*- coding: utf-8 -*-

import sublime
import sublime_plugin
import re
from collections import OrderedDict

# do you want to format the whole file or only a selection?
process_all = True

"""
Usage : Select the text you want to format and press: CRTL + B
        Or Right click and select `Formatme->Format me`

PS : Please expect a little misbehavior of the code as its not trained for few unseen circumstances.
"""

equal_dict = {
    r' *= *= *' : ' == ',
    r' *\+ *= *' : ' += ',
    r' *- *= *' : ' -= ',
    r' *\* *= *' : ' *= ',
    r' *\/ *= *' : ' /= ',
    r' *= *> *' : ' => ',
    r' *\! *= *' : ' != ',
    r' *> *= *' : ' >= ',
    r' *< *= *' : ' <= ',
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
    print('--------------' + stmt)
    for k, v in equal_dict.items():
        # stmt = stmt.replace(k, v)
        stmt = re.sub(k, v, stmt, flags=re.MULTILINE)
    return stmt

"""
process comma
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
    ###### RULE #######                                                             ###### DOCUMENTATION ######
    (r'^\s*(if|else)[^;{]+(;)', single_line_if_else),                               #1)  single line if/else should be encased with curly braces
    (r'if *\(', r'if ('),                                                           #2)  1 space between `if (`
    (r'\} *else *\{', r'} else {'),                                                 #3)  1 space between `} else {`
    (r'\} *else *if *\(', r'} else if ('),                                          #3)  1 space between `} else if (`
    (r'for *\(', r'for ('),                                                         #4)  1 space between `for (`
    (r'while *\(', r'while ('),                                                     #5)  1 space between `while (`
    (r'> *\{', r'> {'),                                                             #6)  1 space between `> {`
    (r'\) *\{', r') {'),                                                            #7)  1 space between `) {`
    # (r'\w{', r' {'),                                                              #8)  ?
    # (r'} *', r'}'),                                                               #9)  ?
    (r'(\, *[^\'\,\'|\w|\n])', process_comma),                                      #10) ?
    (r', *\n', r', \n'),                                                            #11) 1 newline after `, `
    (r' *= *', r' = '),                                                             #12) 1 space around ` = `
    (r'( *= *= *| *\+ *= *| *\- *= *| *\* *= *| *= *> *| *\/ *= *| *\! *= *| *> *= *| *< *= *)', process_equal_override),         #13)
    #(r' +\+ +', r' + '),                                                           #14) ?
    #(r' +\- +', r' - '),                                                           #15) ?
    (r' *\+\+ *', r'++'),                                                           #16) no space around `++`
    (r' *\-\- *', r'--'),                                                           #17) no space around `--`
    # (r' +\* +', r' * '),                                                          #18) ? -- this is conflicting with `/**`
    # (r'\/\/ *', r'// '),                                                          #19) ?
    (r' *\=\> *', r' => '),                                                         #20) 1 space around ` => `
    (r' *\=\= *', r' == '),                                                         #21) 1 space around ` == `
    (r' *\+\= *', r' += '),                                                         #22) 1 space around ` += `
    (r' *\-\= *', r' -= '),                                                         #23) 1 space around ` -= `
    (r' *\*\= *', r' *= '),                                                         #24) 1 space around ` *= `
    (r' */= *', r' /= '),                                                           #25) 1 space around ` /= `
    (r'\n{2, }', r'\n\n'),                                                          #26) at most 2 newlines
    (r' *; *', r';'),                                                               #27) no spaces around `;`
    (r' +$', ''),                                                                   #28) no trailing whitespaces
    (r'(.+) testMethod (.+)', remove_test_method),                                  #29) replace `testMethod` with `@isTest`
    (r'(.+) class (.+) *{', class_name),                                            #30) 1 space between `SampleClass {`
    (r'(.+)(\s*==\s*true|\s*!=\s*false)(.+)', process_if_true),                     #31) remove `== true` or `!= false`
    #(r'((\w|\.)+|(\((\w|,)*\)))+\s*==\s*false', process_if_false),                 #32) convert `x == false` to `!x`
    (r'\s*\=\=\s*true', process_true),                                              #33) remove `== true`
    (r'\s*\!\=\s*false', process_true),                                             #34) remove `!= false`
    (r'^ *(for|if|while)[^{]+{$', process_multiline_loop),                          #35) 1 newline between multiline forloop and `{`
    (r'(for|if|while) *\(.+\)\n+ *{', get_loop),                                    #36) no newline between `for (..) {`
    (r'(?i)\bSELECT\b *' , r'select '),                                             #37) lowercase soql keyword `select`
    (r'(?i)\bFROM\b *' , r'from '),                                                 #38) lowercase soql keyword `from`
    (r'(?i)\bWHERE\b *' , r'where '),                                               #39) lowercase soql keyword `where`
    (r'(?i)\bLIMIT\b *' , r'limit '),                                               #40) lowercase soql keyword `limit`
    (r'(?i)\bGROUP BY\b *' , r'group by'),                                          #41) lowercase soql keyword `group by`
    (r'(?i)\bORDER BY\b *' , r'order by'),                                          #42) lowercase soql keyword `order by`
    (r'(?i)\bHAVING\b *' , r'having'),                                              #43) lowercase soql keyword `having`
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
    region = sublime.Region(0, self.view.size())
    text = self.view.substr(region)
    formatMe(self, edit, region, text)

def process_selection(self, edit):
    # get user selection
    for region in self.view.sel():
        # if selection not empty then
        if not region.empty():
            text = self.view.substr(region)
            formatMe(self, edit, region, text)

def formatMe(self, edit, region, text):
    for key, value in regex_dict.items():
        text = re.sub(key, value, text, flags=re.MULTILINE)
    # replace content in view while removing any trailing whitespaces.
    self.view.replace(edit, region, text.rstrip(' +'))

class RemoveDirty(sublime_plugin.EventListener):
    # "save" event hook to remove dirty window
    def on_post_save_async(self, view):
        view.run_command("revert")
