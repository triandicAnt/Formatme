# -*- coding: utf-8 -*-

def run(text):
    lines = text.split('\n')
    tabs = 0
    newtext = ''
    tab_space = ' ' * 4
    is_current_line_closes = False
    indent = ''
    diff = 0
    for line in lines:
        if is_line_comment(line.strip()):
            newtext += line + '\n'
            continue
        line = line.strip()
        if len(line) == 0:
            newtext += '\n'
            continue
        is_comment = is_line_comment(line)
        if '}' in line and '{' in line and line[0] == '}':
            indent = tab_space*(tabs-1)
        elif '}' in line and '{' in line:
            indent = tab_space*tabs
        elif '{' in line:
            indent = tab_space*tabs
            tabs += line.count('{')
        elif '}' in line:
            tabs -= line.count('}')
            indent = tab_space*tabs
        elif diff == 0:
            indent = tab_space*tabs
        open_parenthesis,close_parenthesis = is_parenthesis(line)
        # check for the open and close parenthesis
        if open_parenthesis > close_parenthesis:
            tabs += 1
        elif open_parenthesis < close_parenthesis:
            tabs -= 1
        # handle the fishy comma
        if peaky_blinders_comma(line):
            line = red_right_hand(line)
        newline = indent + line
        newtext += newline  + '\n'
        if start_soql_query(newline):
            # find the position on that in line
            square_bracket_index = 0
            if ': [' in newline:
                square_bracket_index = newline.index(': [') + 3
            elif '= [' in newline:
                square_bracket_index = newline.index('= [') + 3
            elif '([' in newline:
                square_bracket_index = newline.index('([') + 2
            # next lines indent would be indent + diff
            diff = square_bracket_index - len(indent)
            indent += (' ' * diff) #+ tab_space
        if ('])' in newline or '];' in newline):
            new_len = len(indent)-diff
            indent = ' ' * new_len
            diff = 0
    newtext = newtext[:-1] # remove the last '\n'
    return newtext

def is_line_comment(line):
    return line.startswith('/*') or line.startswith('*') or line.endswith('*/') or line.startswith('//')

def start_soql_query(line):
    return ': [' in line or '= [' in line or '([' in line

def is_parenthesis(line):
    open_count = line.count('(')
    close_count = line.count(')')
    return (open_count,close_count)

def red_right_hand(line):
    """
    1.Split by comma
        If line contains split / = ',' / = ', ' skip it.
        Divide and rule
    """
    if 'split' in line or "= ','" in line or "= ', '" in line or is_line_comment(line):
        return line
    # split line by comma and join them together with spaces
    segments = line.split(',')
    if len(segments) == 0:
        return line
    """
    method1('param1','param2'   ,    'param3');
    [method1('param1','param2'   ,    'param3');]
    """
    final_statement = elephant_stone_strip(segments[0])
    prev_word = final_statement
    for word in segments[1:]:
        if fools_gold(word):
            final_statement += ',' + elephant_stone_strip(word)
        else:
            final_statement += ', ' + elephant_stone_strip(word)
        prev_word = word
    return final_statement

def peaky_blinders_comma(line):
    return ',' in line

def fools_gold(word):
    # return true if `'` is odd else false
    return word.count("'")%2 == 1

def elephant_stone_strip(word):
    if fools_gold(word):
        return word
    return word.strip()