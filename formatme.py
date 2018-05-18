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
def process_singleline_loop(matchedobj):
    return matchedobj.group(0).split('\n')[0] + ' {'

"""
The multiline line for loop should have the curly bracket in next line.
"""
def process_multiline_loop(matchedobj):
    stmt = matchedobj.group(0).strip('\n+')
    return stmt[:-1].strip('\n+').rstrip(' +').rstrip('\n+')+'\n' + get_leading_spaces(stmt) + '{'

"""
Remove the `testMethod` keyword from the test class methods and adding the keyword `@isTest`.
Remove `private` from test method definition
"""
def remove_test_method(matchedobj):
    str = '\t@isTest\n'
    m1 = matchedobj.group(1)
    if 'private ' in m1:
        x = m1.split('private ')
        str += x[0] + x[1]
    else:
        str += m1
    str += ' ' + matchedobj.group(2)
    return str

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

"""
"""
def remove_trailing_newline(matchedobj):
    return '\n' + matchedobj.group(0).split('\n\n')[1]

"""
process single/double equals while ignoring comments.
The comments generally start with `\\` or `/*`. Ignore
those matches and process the rest.
"""
def process_equals(matchedobj):
    stmt = matchedobj.group(0)
    if stmt:
        if '//' in stmt or '/*' in stmt:
            return stmt
        elif stmt.count('=') == 1:
            return ' = '
        elif stmt.count('=') == 2:
            return ' == '

"""
process divide by & equals while ignoring comments.
"""
def process_divide_equals(matchedobj):
    stmt = matchedobj.group(0)
    if stmt:
        if '//' in stmt or '/*' in stmt:
            return stmt
        else:
            return ' /= '

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
    (r'(\, *[^\'\,\'|\w|\n|\(|<])', process_comma),                                 #10) 1 space after `, `
    (r', *\n', r', \n'),                                                            #11) no trailing space after `, `
    (r'\/\*[\s\S]*?\*\/|\/\/[\s\S].*|\s*=\s*', process_equals),                     #12) 1 space around ` = `
    (r'\/\*[\s\S]*?\*\/|\/\/[\s\S].*|\s*=\s*=\s*', process_equals),                 #13a) ` == `
    (r' *\+ *= *', r' += '),                                                        #13b) ` += `
    (r' *\- *= *', r' -= '),                                                        #13c) ` -= `
    (r' *\* *= *', r' *= '),                                                        #13d) ` *= `
    (r' *= *> *', r' => '),                                                         #13e) ` => `
    (r'\/\*[\s\S]*?\*\/|\/\/[\s\S].*| *\/ *= *', process_divide_equals),            #13f) ` /= `
    (r' *\! *= *', r' != '),                                                        #13g) ` != `
    (r' *> *= *', r' >= '),                                                         #13h) ` >= `
    (r' *< *= *', r' <= '),                                                         #13i) ` <= `
    (r' *& *= *', r' &= '),                                                         #13j) ` &= `
    (r' *\| *= *', ' |= '),                                                         #13k) ` |= `
    #(r' +\+ +', r' + '),                                                           #14) `+`
    #(r' +\- +', r' - '),                                                           #15) `-`
    (r' *\+\+ *', r'++'),                                                           #16) no space around `++`
    (r' *\-\- *', r'--'),                                                           #17) no space around `--`
    # (r'\/\/ *', r'// '),                                                          #19) 1 space after `// ` comments
    (r'\n{2,}', r'\n\n'),                                                           #20) at most 2 newlines
    (r' *; *\n', r';\n'),                                                           #21) no spaces around `;`
    (r' +$', ''),                                                                   #22) no trailing whitespaces
    (r'(.+) (?i)testMethod (.+)', remove_test_method),                              #23) replace `testMethod` with `@isTest`
    (r'(.+) class (.+) *{', class_name),                                            #24) 1 space between `SampleClass {`
    (r'(.+)(\s*==\s*true|\s*!=\s*false)(.+)', process_if_true),                     #25) remove `== true` or `!= false`
    #(r'((\w|\.)+|(\((\w|,)*\)))+\s*==\s*false', process_if_false),                 #26) convert `x == false` to `!x`
    (r'^ *(for|if|while)[^{|}]+{$', process_multiline_loop),                        #27) 1 newline between multiline forloop and `{`
    (r'(for|if|while) *\(.+\)\n+ *{', process_singleline_loop),                     #28) no newline between singline forloop and `{`
    (r'(?i)\bSELECT\b *' , r'select '),                                             #29) lowercase soql keyword `select`
    (r'(?i)\bFROM\b *' , r'from '),                                                 #30) lowercase soql keyword `from`
    (r'(?i)\bWHERE\b *' , r'where '),                                               #31) lowercase soql keyword `where`
    (r'(?i)\bLIMIT\b *' , r'limit '),                                               #32) lowercase soql keyword `limit`
    (r'(?i)\bGROUP BY\b *' , r'group by '),                                         #33) lowercase soql keyword `group by`
    (r'(?i)\bORDER BY\b *' , r'order by '),                                         #34) lowercase soql keyword `order by`
    (r'(?i)\bHAVING\b *' , r'having '),                                             #35) lowercase soql keyword `having`
    (r'\n{2}\s*}', remove_trailing_newline),                                        #36) remove trailing newline at end of functions
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
    text = formatMe(self, edit, region, text)
    text = fix_indentation(self, edit, region, text)

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
    text = text.rstrip(' +');
    self.view.replace(edit, region, text)
    return text

def fix_indentation(self, edit, region, text):
    lines = text.split('\n')
    tabs = 0
    newtext = ''
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            newtext += '\n'
            continue
        is_comment = is_line_comment(line)
        if (line.startswith('}') or line.startswith(')')) and not is_comment:
            tabs -= 1
        newline = ' ' * (tabs * 4)
        newline += line
        if (line.endswith('{') or line.endswith('(')) and not is_comment:
            tabs += 1
        newtext += newline + '\n'
    newtext = newtext[:-1] # remove the last '\n'
    self.view.replace(edit, region, newtext)

def is_line_comment(line):
    return line.startswith('//') or line.startswith('/*') or line.startswith('*') or line.endswith('*/')

class RemoveDirty(sublime_plugin.EventListener):
    # "save" event hook to remove dirty window
    def on_post_save_async(self, view):
        view.run_command("revert")
