# -*- coding: utf-8 -*-
import Formatme.constant as CONST
import Formatme.regexme as regexme
import re

soql_flag = False
comment_flag = False

def is_multiline_loops_and_conditionals(line):
    """
    @brief      Determines if loops and conditionals.

    @param      line  The line

    @return     True if loops and conditionals, False otherwise.
    """
    for val in CONST.LOOPS_AND_CONDITIONAL_SET:
        conditional_line = line
        if CONST.BLOCK_COMMENT in line:
            conditional_line = line.split(CONST.BLOCK_COMMENT)[0].strip()
        if conditional_line.startswith(val) and conditional_line[-1] != CONST.OPEN_CURLY_BRACKET:
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

def is_line_comment(line):
    """
    @brief      Determines if line comment.

    @param      line                The line

    @return     True if line comment, False otherwise.
    """
    global comment_flag
    return (
        comment_start(line)
        or comment_end(line)
        or star_comment(line)
        or line.startswith(CONST.BLOCK_COMMENT)
        or comment_flag
    )

def comment_start(line):
    global comment_flag
    if line.startswith(CONST.COMMENT_START) and line.endswith(CONST.COMMENT_END):
        comment_flag = False
        return True
    if line.startswith(CONST.COMMENT_START):
        comment_flag = True
        return True
    return False

def comment_end(line):
    global comment_flag
    if line.endswith(CONST.COMMENT_END) and comment_flag:
        comment_flag = False
        return True
    return False

def star_comment(line):
    global comment_flag
    if line.startswith(CONST.STAR) and comment_flag:
        return True
    return False


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
        or line.startswith('} finally {')
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

def is_line_has_open_bracket(line):
    """
    @brief      Determines if line has an open bracket.

    @param      line  The line

    @return     True if line has an open bracket, False otherwise.
    """
    conditional_line = line
    if CONST.BLOCK_COMMENT in line:
        conditional_line = line.split(CONST.BLOCK_COMMENT)[0].strip()
    return (
        conditional_line[-1] == CONST.OPEN_PARENTHESIS
        or conditional_line[-1] == CONST.OPEN_CURLY_BRACKET
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

def start_soql_query(line):
    """
    @brief      Starts a soql query.

    @param      line  The line

    @return     { description_of_the_return_value }
    """
    global soql_flag
    soql_flag = True
    if (
        regexme.is_character_in_quotes(line, ': [')
        or regexme.is_character_in_quotes(line, '= [')
        or regexme.is_character_in_quotes(line, '([')
    ):
        return False
    return ': [' in line or '= [' in line or '([' in line

def soql_in_same_line(line):
    global soql_flag
    if start_soql_query(line):
        open_paren_count, close_paren_count, indices = (
            get_bracket_count_and_index_of_unmatched(
                line,
                '[',
                ']'
            )
        )
        if open_paren_count-close_paren_count == 0:
            soql_flag = False
            return True
    return False

def end_soql_query(line):
    """
    @brief      Ends a soql query.

    @param      line  The line

    @return     { description_of_the_return_value }
    """
    global soql_flag
    end_flag = (
        soql_flag and (
            '])' in line
            or '];' in line
            or ')];' in line
            or '].' in line
        )
    )
    if end_flag:
        soql_flag = False
    return end_flag

def is_operator_start(line):
    if (
        line.startswith('+')
        or line.startswith('-')
        or line.startswith('/')
        or line.startswith('*')
    ):
        return True
    return False

def is_operator_end(line):
    if (
        line.endswith('+')
        or line.endswith('-')
        or line.endswith('/')
        or line.endswith('*')
    ):
        return True
    return False

def preety_print_line(line, tabs, index):
    """
    @brief      Preety prints line

    @param      line   The line
    @param      tabs   The tabs
    @param      index  The index

    """
    print(
        ('line {} tabs {}  -------> {}'
            .format(
                str(line),
                str(tabs),
                str(index),
            )
        )
    )

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
        if char == CONST.QUOTE:
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
