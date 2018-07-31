# -*- coding: utf-8 -*-


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
PLUS = '+'
STAR = '*'
BLOCK_COMMENT = '//'

LOOPS_AND_CONDITIONAL_SET = {
    'if (',
    'for (',
    'while (',
    '} else if (',
}

SINGLE_LINES = {
    OPEN_PARENTHESIS,
    '&& (',
    '|| (',
}
