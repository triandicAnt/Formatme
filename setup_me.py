# -*- coding: utf-8 -*-
import re

QUOTE_REGEX = r'\'(.+)\''
LOOPS_AND_CONDITIONAL_SET = {'if (', 'for (', 'while ('}
NEW_LINE = '\n'
FREAKING_QUOTE = '\''
OPEN_PARENTHESIS = '('
CLOSE_PARENTHESIS = ')'
OPEN_CURLY_BRACKET = '{'
CLOSE_CURLY_BRACKET = '}'

def run(text):
    lines = text.strip('\n').split('\n')
    newtext = ''
    for l in lines:
        l = setup_me(l, '(', ')')
        print(l + '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        l = setup_me(l, '{', '}')
        print(l + '************************************')
        newtext += l + NEW_LINE
        print('^^^')
    return newtext.strip(NEW_LINE)

def setup_me(line, open, close):
    # print('********************************')
    # print(line)
    # print('********************************')
    if is_loops_and_conditionals(line):
        return line
    split_list = line.split(NEW_LINE)
    # print(split_list)
    for index, l in enumerate(split_list):
        if l.strip() == '':
            continue
        needs_format_paren, paren = check_is_formatted(l, open, close)
        if needs_format_paren:
            indices = find_index_of_unmatched_bracket(l, open, close)
            # print(indices)
            if indices:
                split_list[index] = get_formatted_line(l, indices[0])
                # print('----------------------------- in (((((   ')
                # print(''.join(split_list))
                # print('----------------------------- )))))))')
                split_list[index] = setup_me(''.join(split_list),open, close)
    return NEW_LINE.join(split_list).strip(NEW_LINE)


def setup_me2(line):
    # print('********************************')
    # print(line)
    # print('********************************')
    if is_loops_and_conditionals(line):
        return line
    split_list = line.split(NEW_LINE)
    # print(split_list)
    for index, l in enumerate(split_list):
        if l.strip() == '':
            continue
        needs_format_curly, curly = check_is_formatted_curly(l)
        if needs_format_curly:
            indices = find_index_of_unmatched_bracket(l, '{', '}')
            # print(indices)
            if indices:
                split_list[index] = get_formatted_line(l, indices[0])
                # print('-----------------------------  in {{{{{')
                # print(''.join(split_list))
                # print('----------------------------- }}}}}}}')
                split_list[index] = setup_me(''.join(split_list), '{', '}')
        else:
            continue
    return NEW_LINE.join(split_list).strip(NEW_LINE)

def get_formatted_line(line, index):
    """
    @brief      Get formatted line

    @param      line  The line
    @param      index The index to split

    @return     formatted line.
    """
    if index <= 0:
        return line
    return line[:index+1] + NEW_LINE + line[index+1:]


def check_is_formatted(line, open, close):
    """
    @brief      Check if the paren is formatted.

    @param      line  The line

    @return     True if the line is paren formatted, False otherwise.
    """
    # get parenthesis count
    open_paren, close_paren = get_bracket_count(line, open, close)
    # get diff
    diff_paren = open_paren - close_paren
    if diff_paren > 0 and line[-1] != open:
        return (True, open)
    elif diff_paren < 0:
        if line[-1] == ';' and len(line) > 2 and line[-2] != close:
            return (True, close)
        elif line[-1] != close:
            return (True, close)
    return (False, '')

def check_is_formatted_curly(line):
    """
    @brief      Check if the curly is formatted.

    @param      line  The line

    @return     True if the line is curly formatted, False otherwise.
    """
    # get curly count
    open_curly, close_curly = get_bracket_count(line, '{', '}')
    # get diff
    diff_curly = open_curly - close_curly
    if diff_curly > 0 and line[-1] != '{':
        return (True, '{')
    elif diff_curly < 0:
        if line[-1] == ';' and len(line) > 2 and line[-2] != '}':
            return (True, '}')
        elif line[-1] != '}':
            return (True, '}')
    return (False, '')


def is_loops_and_conditionals(line):
    """
    @brief      Determines if loops and conditionals.

    @param      line  The line

    @return     True if loops and conditionals, False otherwise.
    """
    for val in LOOPS_AND_CONDITIONAL_SET:
        if line.startswith(val):
            return True
    return False

def find_index_of_unmatched_bracket(line, open_char, close_char):
    """
    @brief      Find index of first unmatched parenthesis

    @param      line  The string

    @param      char  The character

    @return     find the indices
    """
    index_stack = []
    push_chars, pop_chars = open_char, close_char
    for i, c in enumerate(line):
        if c in push_chars :
          index_stack.append(i)
        elif c in pop_chars :
          if not len(index_stack):
            index_stack.append(i)
          else :
            index_stack.pop()
    return index_stack

def get_bracket_count(line, open, close):
    """
    @brief      Gets the parenthesis count.

    @param      line  The line

    @return     The parenthesis count.
    """
    open_count = 0
    close_count = 0
    quote_flag = False
    for c in line:
        if c == FREAKING_QUOTE:
            quote_flag = not quote_flag
        if quote_flag:
            continue
        elif c == open:
            open_count += 1
        elif c == close:
            close_count += 1
    return (open_count, close_count)

