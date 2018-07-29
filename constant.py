# -*- coding: utf-8 -*-

LOOPS_AND_CONDITIONAL_SET = {
    'if (',
    'for (',
    'while (',
    '} else if ('
}
NEW_LINE = '\n'
QUOTE = '\''
OPEN_PARENTHESIS = '('
CLOSE_PARENTHESIS = ')'
OPEN_CURLY_BRACKET = '{'
CLOSE_CURLY_BRACKET = '}'
EMPTY_STRING = ''
NEW_STRING = ' '
SEMICOLON = ';'
TAB = NEW_STRING * 4
COMMENT_START = '/*'
COMMENT_END = '*/'
RETURN = 'return'
ELSE_IF = '} else if ('

def is_multiline_loops_and_conditionals(line):
    """
    @brief      Determines if loops and conditionals.

    @param      line  The line

    @return     True if loops and conditionals, False otherwise.
    """
    for val in LOOPS_AND_CONDITIONAL_SET:
        if line.startswith(val) and line[-1] != OPEN_CURLY_BRACKET:
            return True
    return False

def get_bracket_count(line, open_bracket, close_bracket):
    """
    @brief      Gets the parenthesis count.

    @param      line  The line

    @return     The parenthesis count.
    """
    open_count = 0
    close_count = 0
    quote_flag = False
    index_stack = []

    for idx, char in enumerate(line):
        if char == QUOTE:
            quote_flag = not quote_flag
        if quote_flag:
            continue
        elif char == open_bracket:
            open_count += 1
        elif char == close_bracket:
            close_count += 1
    return (open_count, close_count)
