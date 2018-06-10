# -*- coding: utf-8 -*-

import re
from collections import OrderedDict

def run(text):
    for key, value in regex_dict.items():
        text = re.sub(key, value, text, flags=re.MULTILINE)
    # replace content in view while removing any trailing whitespaces.
    text = text.rstrip(' +');
    return text

############ HELPER METHODS ############
def get_leading_spaces(statement):
    """Get the number of leading spaces in a line"""
    leading_space_count = len(statement) - len(statement.lstrip(' '))
    leading_space = ''
    while leading_space_count > 0:
        leading_space += ' '
        leading_space_count -= 1
    return leading_space

def is_line_a_comment(line):
    """Check if a line is a comment"""
    l = line.strip()
    return l.startswith('//') or l.startswith('/*') or l.endswith('*/') or l.startswith('*')


############ REGEX FORMATTING METHODS ############
def process_singleline_loop(matchedobj):
    """Single line loops should have `{` on the same line"""
    return matchedobj.group(0).split('\n')[0] + ' {'

def pre_process_multiline_loop(matchedobj):
    """Multi line loops should end with `)` and have `{` on a new line"""
    x = matchedobj.group(0).split('\n')
    leading_spaces = get_leading_spaces(x[1])
    return x[0] + ')\n' + leading_spaces + '{'

def process_multiline_loop(matchedobj):
    """Multi line loops should have `{` on a separate new line"""
    stmt = matchedobj.group(0).strip('\n+')
    return stmt[:-1].strip('\n+').rstrip(' +').rstrip('\n+')+'\n' + get_leading_spaces(stmt) + '{'

def remove_test_method(matchedobj):
    """Replace `private testMethod` keyword with `@isTest` annotation"""
    str = '\t@isTest\n'
    m1 = matchedobj.group(1)
    if 'private ' in m1:
        x = m1.split('private ')
        str += x[0] + x[1]
    else:
        str += m1
    str += ' ' + matchedobj.group(2)
    return str

def class_name(matchedobj):
    """1 space between class declaration and `{`"""
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
    stmt = re.compile(r'\s*==\s*|\s*\!=\s*').split(matchedobj.group(0))[0].strip()
    if not stmt:
        return matchedobj.group(0)
    if stmt[0] == '(':
        return '(!{0}'.format(stmt[1:])
    return '!{0}'.format(stmt)

"""
if () {

}
else{

}
"""
def format_if_else_same_line(matchedobj):
    stmts = re.compile(r'\n*').split(matchedobj.group(0))
    if not stmts:
        return matchedobj.group(0)
    return '{0} {1}'.format(stmts[0],stmts[1].strip())

"""
process comma
"""
def process_comma(matchedobj):
    return matchedobj.group(1).rstrip(' +') + ' '

"""
process single line if else
"""
def single_line_if_else(matchedobj):
    """
    SKIP|FAIL
    skip if ; in in quotes
    """
    if ";'" in matchedobj.group(0):
        return matchedobj.group(0)
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

"""
process Single line if/else statements.
if (sth() && nothing()) return;

if (sth() && nothing())
    return;
"""
def if_else_same_line(matchedobj):
    stmt = matchedobj.group(0)
    # find the closing bracket for the if/else.
    # First find the occurence of '('
    if not stmt:
        return
    leading_spaces = ' '*(len(stmt) - len(stmt.lstrip('\n*').lstrip(' ')))
    stmt = stmt.strip()
    if 'if' in stmt or 'else if' in stmt:
        parenthesis_index = stmt.strip().index('(')
        # from parenthesis_index onwards we want to find the closing parenthesis
        count = 1
        index_count = 0
        for char in stmt.strip()[parenthesis_index + 1 : ]:
            index_count = index_count + 1
            if char == '(':
                count = count + 1
            if char == ')':
                count = count - 1
                if count == 0:
                    break
        return '\n{0}{1}\n{2}{3}'.format(leading_spaces, stmt[:parenthesis_index + index_count + 1],\
            '{0}{1}'.format(leading_spaces, ' ' * 4),stmt[parenthesis_index + index_count +1:].strip())
    elif 'else' in stmt:
        # handle the else case
        stmts = stmt.split(' ')
        return '\n{0}{1}\n{2}{3}'.format(leading_spaces, stmts[0],\
            '{0}{1}'.format(leading_spaces, ' ' * 4),stmts[1].strip())
    else:
        return stmt

"""
process &&
SKIP|FAIL
"""
def process_double_and(matchedobj):
    stmt = matchedobj.group(0)
    # skip the records if it has a \n otherwise process it
    if '\n' in stmt:
        return stmt.split('&&')[0] + '&& '
    else:
        return ' && '

"""
process ||
SKIP|FAIL
"""
def process_double_or(matchedobj):
    stmt = matchedobj.group(0)
    # skip the records if it has a \n otherwise process it
    if '\n' in stmt:
        return stmt.split('||')[0] + '|| '
    else:
        return ' || '

regex_dict = OrderedDict([
    ###### RULE #######                                                             ###### DOCUMENTATION ######
    (r'\s*(if\s*\(|else\s*if|else)(.+);$', if_else_same_line),                      #0)  single line if else statement should be in the next line.
    (r'^\s*(if|else)[^;{]+(;\')|^\s*(if|else)[^;{]+(;)', single_line_if_else),      #1)  single line if/else should be enclosed with curly braces
    (r'if *\(', r'if ('),                                                           #2)  1 space between `if (`
    (r'\} *else *\{', r'} else {'),                                                 #3)  1 space between `} else {`
    (r'\} *else *if *\(', r'} else if ('),                                          #3)  1 space between `} else if (`
    (r'for *\(', r'for ('),                                                         #4)  1 space between `for (`
    (r'while *\(', r'while ('),                                                     #5)  1 space between `while (`
    (r'> *\{', r'> {'),                                                             #6)  1 space between `> {`
    (r'\) *\{', r') {'),                                                            #7)  1 space between `) {`
    #(r'(\, *[^\'\,\'|\/|\w|\n|\(|<])', process_comma),                              #10) 1 space after `, `
    (r', *\n', r', \n'),                                                            #11) no trailing space after `, `
    (r'\/\*[\s\S]*?\*\/|\/\/[\s\S].*|\s*=\s*', process_equals),                     #12) 1 space around ` = `
    (r'\/\*[\s\S]*?\*\/|\/\/[\s\S].*|\s*=\s*=\s*', process_equals),                 #13a) ` == `
    # (r' *\+ *', r' + '),                                                          #14) `+`    # broken example: '10+'
    # (r' *\- *', r' - '),                                                          #15) `-`    # broken example: 'Pre-Sale'
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
    (r' *\+\+ *', r'++'),                                                           #16) no space around `++`
    (r' *\-\- *', r'--'),                                                           #17) no space around `--`
    (r'\n{2,}', r'\n\n'),                                                           #20) at most 2 newlines
    (r' *; *\n', r';\n'),                                                           #21) no spaces around `;`
    (r' +$', ''),                                                                   #22) no trailing whitespaces
    (r'(.+) (?i)testMethod (.+)', remove_test_method),                              #23) replace `testMethod` with `@isTest`
    (r'(.+) class (.+) *{', class_name),                                            #24) 1 space between `SampleClass {`
    (r'(.+)(\s*==\s*true|\s*!=\s*false)(.+)', process_if_true),                     #25) remove `== true` or `!= false`
    (r'(\S)+\s*==\s*false|(\S)+\s*!=\s*true', process_if_false),                    #26) convert `x == false|z != true ` to `!x`
    (r'(.+)\n *\) *\{$', pre_process_multiline_loop),                               #27a)Fix multiline loops that end with '){' on new line
    (r'^ *(for|if|while)[^{|}]+{$', process_multiline_loop),                        #27b)1 newline between multiline forloop and `{`
    (r'(for|if|while) *\(.+\)\n+ *{', process_singleline_loop),                     #28) no newline between singline forloop and `{`
    (r'(?i)\bSELECT\b *' , r'select '),                                             #29) lowercase soql keyword `select`
    (r'(?i)\bFROM\b *' , r'from '),                                                 #30) lowercase soql keyword `from`
    (r'(?i)\bWHERE\b *' , r'where '),                                               #31) lowercase soql keyword `where`
    (r'(?i)\bLIMIT\b *' , r'limit '),                                               #32) lowercase soql keyword `limit`
    (r'(?i)\bGROUP BY\b *' , r'group by '),                                         #33) lowercase soql keyword `group by`
    (r'(?i)\bORDER BY\b *' , r'order by '),                                         #34) lowercase soql keyword `order by`
    (r'(?i)\bHAVING\b *' , r'having '),                                             #35) lowercase soql keyword `having`
    (r'\n{2}\s*}', remove_trailing_newline),                                        #36) remove trailing newline at end of functions
    (r'({\s*get;\s*set;\s*})','{get; set;}'),                                       #37) get/set for class variables
    (r'}\n+\s*else', format_if_else_same_line),                                     #38) else/else if should start with closing } of if
    (r'try *\{', r'try {'),                                                         #39) 1 space between `try {`
    (r'\} *catch *\(', r'} catch ('),                                               #40) 1 space between `} catch (`
    (r'(\n *&& *| *&& *)', process_double_and),                                     #41) && should have 1 space before and after.
    (r'\n *\|\| *| *\|\| *', process_double_or),                                    #42) || should have 1 space before and after.
])