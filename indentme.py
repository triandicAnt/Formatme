# -*- coding: utf-8 -*-

def run(text):
    lines = text.split('\n')
    tabs = 0
    newtext = ''
    tab_space = ' ' * 4
    is_current_line_closes = False
    indent = ''
    diff = 0
    soql_flag = False
    soql_end_flag = False
    soql_start_indent = ''
    soql_end_indent = ''
    other_flag = False
    akane_no_mai_flag = False
    count = 0
    soql_rises_flag = False
    parenthesis_count = 0
    for line in lines:
        count += 1
        if is_line_comment(line.strip()):
            newtext += line + '\n'
            continue
        line = line.strip()
        if len(line) == 0:
            newtext += '\n'
            continue
        is_comment = is_line_comment(line)
        open_parenthesis,close_parenthesis = is_parenthesis(line)
        if soql_flag:
            indent = soql_start_indent
        elif soql_end_flag:
            indent = soql_end_indent
            soql_end_flag = False
            soql_end_indent = ''
            soql_start_indent = ''
        else:
            indent = tab_space*tabs

        if '}' in line and '{' in line and line[0] == '}':
            indent = tab_space*(tabs-1)
        elif '}' in line and '{' in line:
            indent = tab_space*tabs
        elif '{' in line:
            indent = tab_space*tabs
            tabs += line.count('{')
            print('line ' + str(count) + ' tabs ' + str(tabs) + ' -------1')
        elif not soql_flag and akane_no_mai(line):
            tabs -= line.count('}')
            indent = tab_space*tabs
            parenthesis_count = open_parenthesis - close_parenthesis
            tabs += parenthesis_count
            print('line ' + str(count) + ' tabs ' + str(tabs) + ' -------1.5')
        elif '}' in line:
            tabs -= line.count('}')
            print('line ' + str(count) +' tabs ' + str(tabs) + ' -------2')
            indent = tab_space*tabs
        elif 'return' in line and line[-1] != ';':
            other_flag = True
            tabs += 1
            print('line ' + str(count) + ' tabs ' + str(tabs) + ' -------3')
        elif other_flag and ';' in line:
            tabs -= 1
            print('line ' + str(count) + ' tabs ' + str(tabs) + ' -------4')
            other_flag = False
        elif not soql_flag and akane_no_mai(line):
            parenthesis_count = open_parenthesis - close_parenthesis
            tabs += parenthesis_count
            print('line ' + str(count) + ' tabs ' + str(tabs) + ' -------5')
            akane_no_mai_flag = True
        elif not soql_flag and line[-1] == ')' and akane_no_mai_flag and close_parenthesis > open_parenthesis:
            tabs -= parenthesis_count
            parenthesis_count = 0
            print('line ' + str(count) + ' tabs ' + str(tabs) + ' -------6')
            akane_no_mai_flag = False
        elif les_ecorchés(line) and akane_no_mai_flag:
            tabs -= parenthesis_count
            parenthesis_count = 0
            print('line ' + str(count) + ' tabs ' + str(tabs) + ' -------6.1')
            akane_no_mai_flag = False
        elif ');' == line:
            tabs -= 1
            print('line ' + str(count) + ' tabs ' + str(tabs) + ' -------7')
            indent = tab_space*tabs
        elif not soql_flag and virtù_e_fortuna(line):
            tabs -= 1
            print('line ' + str(count) + ' tabs ' + str(tabs) + ' -------8')
        elif not soql_flag:
            indent = tab_space*tabs

        # handle the fishy comma
        # if peaky_blinders_comma(line):
        #     line = red_right_hand(line)
        if line.strip() == '{':
            print('line ' + str(count) +  ' tabs ' + str(tabs))

        newline = indent + line.rstrip()
        newtext += newline  + '\n'
        if start_soql_query(newline):
            # find the position on that in line
            square_bracket_index = 0
            soql_flag = True
            if ': [' in newline:
                square_bracket_index = newline.index(': [') + 3
            elif '= [' in newline:
                square_bracket_index = newline.index('= [') + 3
            elif '([' in newline:
                square_bracket_index = newline.index('([') + 2
            # next lines indent would be indent + diff
            if not soql_start_indent:
                diff = square_bracket_index - len(soql_start_indent) - 1
            else:
                diff = square_bracket_index - len(indent)
            soql_start_indent += (' ' * diff) #+ tab_space
        if ('])' in newline or '];' in newline):
            soql_flag = False
            soql_end_flag = True
            new_len = len(indent)-diff
            soql_end_indent = ' ' * new_len
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
            final_statement += ','
        else:
            final_statement += ', '
        final_statement += elephant_stone_strip(word)
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

def akane_no_mai(line):
    open_parenthesis,close_parenthesis = is_parenthesis(line)
    if ('if (' in line or 'else if (' in line or 'for (' in line or line[-1] == '(') and open_parenthesis > close_parenthesis:
        return True
    return False

def virtù_e_fortuna(line):
    open_parenthesis,close_parenthesis = is_parenthesis(line)
    if line [-1] == ')' and close_parenthesis > open_parenthesis:
        return True
    return False

def les_ecorchés(line):
    if '])' in line or '];' in line:
        return True
    return False

