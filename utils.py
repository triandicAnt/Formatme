# -*- coding: utf-8 -*-
import Formatme.constant as CONST
import re


def is_multiline_loops_and_conditionals(line):
    """
    @brief      Determines if loops and conditionals.

    @param      line  The line

    @return     True if loops and conditionals, False otherwise.
    """
    for val in CONST.LOOPS_AND_CONDITIONAL_SET:
        if line.startswith(val) and line[-1] != CONST.OPEN_CURLY_BRACKET:
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
        if char == CONST.QUOTE:
            quote_flag = not quote_flag
        if quote_flag:
            continue
        elif char == open_bracket:
            open_count += 1
        elif char == close_bracket:
            close_count += 1
    return (open_count, close_count)

def is_line_comment(line, block_comment_flag):
    """
    @brief      Determines if line comment.

    @param      line                The line
    @param      block_comment_flag  The block comment flag

    @return     True if line comment, False otherwise.
    """
    return (
        line.startswith(CONST.COMMENT_START)
        or line.startswith(CONST.STAR)
        or line.endswith(CONST.COMMENT_END)
        or line.startswith(CONST.BLOCK_COMMENT)
        or block_comment_flag
    )

def is_line_conditional_or_try_catch(line):
    """
    @brief      Determines if line conditional or try catch.

    @param      line  The line

    @return     True if line conditional or try catch, False otherwise.
    """
    return (
        line.startswith('} else {')
        or line.startswith('} else if (')
        or line.startswith('} catch (')
    )


def is_line_keywords(line):
    """
    @brief      Determines if line keywords.

    @param      line  The line

    @return     True if line keywords, False otherwise.
    """
    line = line.strip().lower()
    return (
        line == 'override'
        or line == '@override'
        or line == '@istest'
        or line == '@testsetup'
        or line == '@testvisible'
        or line == '@future(callout=true)'
    )

def is_character_in_quotes(line, char):
    """
    @brief      Determines if character in quotes.

    @param      line  The line
    @param      char  The character

    @return     True if character in quotes, False otherwise.
    """
    stmt = re.search(r'\'(.+)\'', line)
    if not stmt:
        return False
    return char in stmt.group(0)

def is_line_data_structure(line):
    """
    @brief      Determines if line data structure.

    @param      line  The line

    @return     True if line data structure, False otherwise.
    """
    stmt = re.search(r'(.+)\{$', line)
    if not stmt:
        return False
    data_strucrtures = {
        'List',
        'Set',
        'Map',
        'enum'
    }
    for ds in data_strucrtures:
        if ds in stmt.group(0):
            return True
    return False
