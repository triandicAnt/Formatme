# -*- coding: utf-8 -*-
import re

LOOPS_AND_CONDITIONAL_SET = {'if (', 'for (', 'while ('}
NEW_LINE = '\n'
FREAKING_QUOTE = '\''
OPEN_PARENTHESIS = '('
CLOSE_PARENTHESIS = ')'
OPEN_CURLY_BRACKET = '{'
CLOSE_CURLY_BRACKET = '}'
EMPTY_STRING = ''
SEMICOLON = ';'

def run(text):
    """
    @brief      set up the line for formatting. If a line contains odd
                number of `{`/'}' or `(`/`)`, it will be split into two
                multiple lines.

    @param      line  The line

    @return     formatted line.
    """
    lines = text.strip(NEW_LINE).split(NEW_LINE)
    newtext = EMPTY_STRING
    for l in lines:
        l = setup_me(l.strip(), OPEN_PARENTHESIS, CLOSE_PARENTHESIS)
        l = setup_me(l.strip(), OPEN_CURLY_BRACKET, CLOSE_CURLY_BRACKET)
        newtext += l + NEW_LINE
    return newtext.strip(NEW_LINE)

def setup_me(line, open_bracket, close_bracket):
    if is_loops_and_conditionals(line):
        return line
    open_paren_count, close_paren_count, indices = (
        get_bracket_count_and_index_of_unmatched(
            line,
            open_bracket,
            close_bracket
        )
    )
    needs_format, bracket = (
        check_is_formatted(
            line.strip(),
            open_bracket,
            close_bracket,
            open_paren_count - close_paren_count
        )
    )
    if needs_format:
        if bracket in {OPEN_PARENTHESIS, OPEN_CURLY_BRACKET}:
            return setup_line(line, indices, 1)
        else:
            return setup_line(line, indices, 0)
    return line

def setup_line(line, indices, salt):
    """
    @brief      Set up line for indentation

    @param      line  The line
    @param      index The indices to split

    @return     formatted line.
    """
    if len(indices) <= 0:
        return line
    length_of_line = len(line)
    new_line = EMPTY_STRING
    start_index = 0
    for index in indices:
        new_line += line[start_index : index + salt] + NEW_LINE
        start_index = index + salt
    new_line += line[start_index:]
    return new_line.strip(NEW_LINE)

def check_is_formatted(line, open_bracket, close_bracket, diff_paren):
    """
    @brief      Check if the paren is formatted.

    @param      line  The line

    @return     True if the line is paren formatted, False otherwise.
    """
    if (
        (diff_paren == 1 and line[-1] != open_bracket)
        or diff_paren > 1
    ):
        return (True, open_bracket)
    elif diff_paren < 0:
        if line != OPEN_PARENTHESIS and line != close_bracket + SEMICOLON:
            return (True, close_bracket)
    return (False, EMPTY_STRING)

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

def get_bracket_count_and_index_of_unmatched(line, open_bracket, close_bracket):
    """
    @brief      Gets the parenthesis count and the indices of unmatched brackets.

    @param      line  The line

    @return     The parenthesis count.
    """
    open_count = 0
    close_count = 0
    temp_open_count = 0
    quote_flag = False
    index_stack = []

    for idx, char in enumerate(line):
        if char == FREAKING_QUOTE:
            quote_flag = not quote_flag
        if quote_flag:
            continue
        elif char == open_bracket:
            index_stack.append(idx)
            open_count += 1
            temp_open_count += 1
        elif char == close_bracket:
            close_count += 1
            if temp_open_count <= 0:
                index_stack.append(idx)
            else:
                index_stack.pop()
            temp_open_count -= 1
    return (open_count, close_count, index_stack)
