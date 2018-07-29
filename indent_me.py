# -*- coding: utf-8 -*-
import Formatme.constant as CONST
import Formatme.utils as UTILS
import re

"""
Different type of lines:
1. Soql line - soql statement in the same line.
2. Soql start line.
3. Soql continue line.
4. Soql end line.
5. Multiline return start line.
6. Multiline return end line.
7. Open bracket line.
8. Close bracket line.
9. Multiline conditional start line.
10. Multiline conditional end line.
11. Rest of lines.
"""

def run(text):
    """
    @brief      Indents the line based on the line type.

    @param      text  The text

    @return     indented text
    """
    lines = text.strip(CONST.NEW_LINE).split(CONST.NEW_LINE)

    tabs = 0
    diff = 0
    # for multiline conditional
    total_paren_count = 0
    total_tabs_added = 0

    indent = CONST.EMPTY_STRING
    newtext = CONST.EMPTY_STRING
    tab_space = CONST.TAB
    soql_start_indent = CONST.EMPTY_STRING
    soql_end_indent = CONST.EMPTY_STRING

    soql_flag = False
    soql_end_flag = False
    return_flag = False
    block_comment_flag = False
    no_semicolon_flag = False
    return_paren_flag = False
    open_bracket_flag = False
    last_line_flag = False
    conditonal_flag = False

    total_num_of_lines = len(lines)
    for i in range(0, total_num_of_lines):
        orig_line = lines[i]
        line = orig_line.strip()

        # handle comments
        if line.startswith(CONST.COMMENT_START):
            block_comment_flag = True
        elif line.endswith(CONST.COMMENT_END):
            block_comment_flag = False
        if CONST.is_line_comment(line, block_comment_flag):
            indent = tab_space*tabs
            if line.startswith('*'):
                indent = tab_space*tabs + CONST.NEW_STRING
            newtext += indent + orig_line + CONST.NEW_LINE
            continue
        if len(line) == 0:
            newtext += CONST.NEW_LINE
            continue

        line_number = i + 1

        # soql in the same line #1
        if start_soql_query(line) and end_soql_query(line):
            indent = tab_space*tabs
            soql_flag = False
            preety_print_line(line_number, tabs, 1)

        # soql start #2
        elif soql_flag:
            indent = soql_start_indent

        # soql end #4
        elif soql_end_flag:
            indent = soql_end_indent
            soql_end_flag = False
            soql_end_indent = CONST.EMPTY_STRING
            soql_start_indent = CONST.EMPTY_STRING

        # default indent #3
        else:
            indent = tab_space*tabs

        # multiline return start #5
        if CONST.RETURN in line and line[-1] != CONST.SEMICOLON:
            return_flag = True
            tabs += 1
            preety_print_line(line_number, tabs, 2)

        # multiline return end #6
        elif return_flag and CONST.SEMICOLON in line:
            tabs -= 1
            if (
                line.strip() == '));'
                or line.strip() == ');'
                or line.strip() == '});'
            ):
                if return_paren_flag and len(line.strip()) > 2:
                    tabs -= 1
                    return_paren_flag = False
                indent = tab_space*tabs
            preety_print_line(line_number, tabs, 3)
            return_flag = False

        # opening bracket line #7
        elif (
            line[-1] == CONST.OPEN_PARENTHESIS
            or line[-1] == CONST.OPEN_CURLY_BRACKET
        ):
            if (
                UTILS.is_line_conditional_or_try_catch(line)
                # or line == CONST.OPEN_CURLY_BRACKET
            ):
                tabs -= 1
                indent = tab_space*tabs
            else:
                indent = tab_space*tabs
            tabs += 1
            open_bracket_flag = True
            preety_print_line(line_number, tabs, 4)

        # closing bracket line #8
        elif (
            line == CONST.CLOSE_PARENTHESIS + CONST.SEMICOLON
            or line == CONST.CLOSE_CURLY_BRACKET + CONST.SEMICOLON
            or line == CONST.CLOSE_PARENTHESIS
            or line == CONST.CLOSE_CURLY_BRACKET
        ):
            tabs -= 1
            indent = tab_space*tabs
            if line != CONST.CLOSE_PARENTHESIS:
                open_bracket_flag = False
            preety_print_line(line_number, tabs, 5)

        # multiline conditional start #9
        elif UTILS.is_multiline_loops_and_conditionals(line):
            open_paren, close_paren = (
                UTILS.get_bracket_count(
                    line,
                    CONST.OPEN_PARENTHESIS,
                    CONST.CLOSE_PARENTHESIS
                )
            )
            conditonal_flag = True
            total_paren_count += (open_paren - close_paren)
            if line.startswith(CONST.ELSE_IF):
                tabs -= 1
                indent = tab_space*tabs
            tabs += 1
            total_tabs_added += 1
            preety_print_line(line_number, tabs, 6)

        # multiline conditional end #10
        elif conditonal_flag:
            open_paren, close_paren = (
                UTILS.get_bracket_count(
                    line,
                    CONST.OPEN_PARENTHESIS,
                    CONST.CLOSE_PARENTHESIS
                )
            )
            total_paren_count += (open_paren - close_paren)
            diff = (open_paren - close_paren)
            if diff > 0:
                tabs += 1
                total_tabs_added += 1
            elif diff < 0:
                if total_paren_count == 0:
                    conditonal_flag = False
                    tabs -= total_tabs_added
                    total_tabs_added = 0
            preety_print_line(line_number, tabs, 7)

        # rest of the line #11
        elif (
            not return_flag
            and not soql_flag
            and not start_soql_query(line)
            and not UTILS.is_character_in_quotes(line, CONST.SEMICOLON)
            and not UTILS.is_line_keywords(line)
        ):
            indent = tab_space*tabs
            if (
                CONST.SEMICOLON not in line
                and not no_semicolon_flag
                and (
                    line[-1] == CONST.QUOTE
                    or line[-1] == CONST.PLUS
                )
            ):
                no_semicolon_flag = True
                tabs += 1
            elif no_semicolon_flag:
                no_semicolon_flag = False
                tabs -= 1
            preety_print_line(line_number, tabs, 8)
        else:
            print('🤷🤷‍♀️🤷‍🙄🙄🙄 {}'.format(str(line_number)))

        newline = indent + line.rstrip()
        newtext += newline  + CONST.NEW_LINE

        # if the soql ends in same line then don't set the flags
        if start_soql_query(line) and end_soql_query(line):
            continue

        # handle multiline soql line
        if start_soql_query(newline):
            # find the position in line
            square_bracket_index = 0
            soql_flag = True
            if ': [' in newline:
                square_bracket_index = newline.index(': [') + 4
            elif '= [' in newline:
                square_bracket_index = newline.index('= [') + 4
            elif '([' in newline:
                square_bracket_index = newline.index('([') + 3
            # next lines indent would be indent + diff
            if not soql_start_indent:
                diff = square_bracket_index - len(soql_start_indent) - 1
            else:
                diff = square_bracket_index - len(indent)
            soql_start_indent += (CONST.NEW_STRING * diff) #+ tab_space

        # handle soql end line
        if (
            '])' in newline
            or '];' in newline
            or ')];' in newline
        ):
            soql_flag = False
            soql_end_flag = True
            new_len = len(indent)-diff
            soql_end_indent = ' ' * new_len

        # Handle unindented lines
        if (
            line_number != total_num_of_lines
            and not last_line_flag
            and tabs == 0
        ):
            print('😱😱😱😱😱😱😱😱😱😱')
            preety_print_line(line_number, tabs, -1)
            print('👽👽👽👽👽👽👽👽👽👽')
            last_line_flag = True

    # remove the last '\n'
    newtext = newtext[:-1]
    if tabs == 0:
        print('\n🙀🐾If I fits, I sits🐾🐈')
    else:
        print('\n🏇🔫🤖Indentation not done properly.🤖🔫🏇')
    return newtext

def start_soql_query(line):
    """
    @brief      Starts a soql query.

    @param      line  The line

    @return     { description_of_the_return_value }
    """
    return ': [' in line or '= [' in line or '([' in line

def end_soql_query(line):
    """
    @brief      Ends a soql query.

    @param      line  The line

    @return     { description_of_the_return_value }
    """
    r = re.compile(r'](.+)*;$')
    return r.search(line) != None

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
