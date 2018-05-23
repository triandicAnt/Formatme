# -*- coding: utf-8 -*-

def indent_me(self, edit, region, text):
    lines = text.split('\n')
    tabs = 0
    newtext = ''
    is_prev_line_open = False
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            newtext += '\n'
            continue
        is_comment = is_line_comment(line)
        # print(line)
        # print('--- ' + str(is_line_close(line)) + '------' + str(is_line_open(line)))
        if is_line_close(line) and not is_comment:
            tabs -= 1
            is_prev_line_open = False
        indents = ' ' * (tabs * 4)
        if is_line_open(line) and not is_comment:
            if line == '{': # handle the single { in multiline forloops
                indents = ' ' * (tabs-1 * 4)
            tabs += 1
            is_prev_line_open = True
        newtext += indents
        newtext += line + '\n'
    newtext = newtext[:-1] # remove the last '\n'
    self.view.replace(edit, region, newtext)

def is_line_open(line):
    return count_brackets(line, '{}', True) # count_brackets(line, '()', True) or count_brackets(line, '[]', True)

def is_line_close(line):
    return count_brackets(line, '{}', False) # count_brackets(line, '()', False) or count_brackets(line, '[]', False)

def count_brackets(line, bracket, openflag):
    open_bracket = bracket[0]
    close_bracket = bracket[1]
    count = 0
    for c in line:
        if openflag:
            if c == open_bracket:
                count += 1
            elif c == close_bracket and count > 0:  ## `} else {`
                count -= 1
        else:
            if c == close_bracket:
                count += 1
            elif c == open_bracket:
                count -= 1
    return count > 0

def is_line_comment(line):
    return line.startswith('/*') or line.startswith('*') or line.endswith('*/')

def indent_me_returns(self, edit, region, text):
    lines = text.split('\n')
    tabs = 0
    newtext = ''
    tab_space = ' '*4
    is_current_line_closes = False
    indent = ''
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            newtext += '\n'
            continue
        is_comment = is_line_comment(line)
        if '}' in line and '{' in line and line[0] == '}' and not is_comment:
            indent = tab_space*(tabs-1)
        elif '}' in line and '{' in line and not is_comment:
            indent = tab_space*tabs
        elif '{' in line and not is_comment:
            indent = tab_space*tabs
            tabs += line.count('{')
            print('{' + str(tabs))
        elif '}' in line and not is_comment:
            tabs -= line.count('}')
            indent = tab_space*tabs
            print('}' + str(tabs))
        elif '}' not in line and '{' not in line and not is_comment:
            indent = tab_space*tabs
        open_parenthesis,close_parenthesis = is_parenthesis(line)
        if open_parenthesis > close_parenthesis:
            tabs += 1
        elif open_parenthesis < close_parenthesis:
            tabs -= 1
        newtext += indent
        newtext += line + '\n'
    newtext = newtext[:-1] # remove the last '\n'
    self.view.replace(edit, region, newtext)



def is_parenthesis(line):
    open_count = line.count('(')
    close_count = line.count(')')
    return (open_count,close_count)


