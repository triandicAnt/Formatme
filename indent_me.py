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
11. Rest of lines including multiline string statements.
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
    total_conditional_tabs_added = 0
    total_return_tabs_added = 0

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
            newtext += orig_line + CONST.NEW_LINE
            #indent = tab_space*tabs
            # if line.startswith('*'):
            #     indent = tab_space*tabs + CONST.NEW_STRING
            # newtext += indent + orig_line + CONST.NEW_LINE
            continue
        if len(line) == 0:
            newtext += CONST.NEW_LINE
            continue

        line_number = i + 1

        # soql in the same line #1
        if UTILS.start_soql_query(line) and UTILS.end_soql_query(line):
            indent = tab_space*tabs
            soql_flag = False
            UTILS.preety_print_line(line_number, tabs, 1)

        # soql start #2
        elif soql_flag:
            indent = soql_start_indent

        # soql end #4
        elif soql_end_flag:
            soql_end_flag = False
            soql_end_indent = CONST.EMPTY_STRING
            soql_start_indent = CONST.EMPTY_STRING
            indent = tab_space*tabs

        # default indent #3
        else:
            indent = tab_space*tabs

        # multiline return start #5
        if CONST.RETURN in line and line[-1] != CONST.SEMICOLON:
            return_flag = True
            tabs += 1
            total_return_tabs_added += 1
            UTILS.preety_print_line(line_number, tabs, 2)

        # multiline return end #6
        elif return_flag and CONST.SEMICOLON in line:
            tabs -= total_return_tabs_added
            if (
                line.strip() == '));'
                or line.strip() == ');'
                or line.strip() == '});'
            ):
                indent = tab_space*tabs
            return_flag = False
            total_return_tabs_added = 0
            UTILS.preety_print_line(line_number, tabs, 3)

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
            total_conditional_tabs_added += 1
            UTILS.preety_print_line(line_number, tabs, 4)

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
                total_conditional_tabs_added += 1
            elif diff < 0:
                if total_paren_count == 0:
                    conditonal_flag = False
                    tabs -= total_conditional_tabs_added
                    total_conditional_tabs_added = 0
            UTILS.preety_print_line(line_number, tabs, 5)

        # opening bracket line #7
        elif UTILS.is_line_has_open_bracket(line):
            if (
                UTILS.is_line_conditional_or_try_catch(line)
                # or line == CONST.OPEN_CURLY_BRACKET
            ):
                tabs -= 1
                indent = tab_space*tabs
            else:
                indent = tab_space*tabs
            tabs += 1
            if return_flag:
                total_return_tabs_added += 1
            if line[-1] == CONST.OPEN_PARENTHESIS:
                open_bracket_flag = True
            UTILS.preety_print_line(line_number, tabs, 6)

        # closing bracket line #8
        elif (
            line == CONST.CLOSE_PARENTHESIS + CONST.SEMICOLON
            or line == CONST.CLOSE_CURLY_BRACKET + CONST.SEMICOLON
            or line.startswith(CONST.CLOSE_PARENTHESIS)
            or line.startswith(CONST.CLOSE_CURLY_BRACKET)
        ):
            tabs -= 1
            # if string line ends then decrease a tab
            # as it was set earlier
            if no_semicolon_flag:
                tabs -= 1
                no_semicolon_flag = False
            if return_flag:
                total_return_tabs_added -= 1
            indent = tab_space*tabs
            # if line != CONST.CLOSE_PARENTHESIS:
            open_bracket_flag = False
            UTILS.preety_print_line(line_number, tabs, 7)

        # rest of the line #11
        elif (
            not return_flag
            and not soql_flag
            and not UTILS.start_soql_query(line)
            and not UTILS.is_character_in_quotes(line, CONST.SEMICOLON)
            and not UTILS.is_line_keywords(line)
        ):
            indent = tab_space*tabs
            if (
                line[-1] != CONST.SEMICOLON
                and not no_semicolon_flag
                and (
                    line[-1] == CONST.PLUS # String
                    or line[0] == CONST.PLUS # String
                )
            ):
                no_semicolon_flag = True
                tabs += 1
                if line[0] == CONST.PLUS:
                    indent = tab_space*tabs
            elif no_semicolon_flag and line[-1] == CONST.SEMICOLON:
                no_semicolon_flag = False
                tabs -= 1
            elif line[0] == CONST.PLUS and line[-1] == CONST.SEMICOLON:
                indent = tab_space*(tabs+1)
            elif open_bracket_flag and line[-1] == CONST.SEMICOLON:
                tabs -= 1
                open_bracket_flag = False
            UTILS.preety_print_line(line_number, tabs, 8)
        else:
            #indent = tab_space*tabs
            print('🤷🤷‍♀️🤷‍🙄🙄🙄 {}'.format(str(line_number)))

        newline = indent + line.rstrip()
        newtext += newline  + CONST.NEW_LINE

        # if the soql ends in same line then don't set the flags
        if UTILS.start_soql_query(line) and UTILS.end_soql_query(line):
            continue

        # handle multiline soql line
        if UTILS.start_soql_query(newline):
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
            soql_end_indent = CONST.NEW_STRING * new_len

        # Handle unindented lines
        if (
            line_number != total_num_of_lines
            and not last_line_flag
            and tabs == 0
        ):
            print('😱😱😱😱😱😱😱😱😱😱')
            UTILS.preety_print_line(line_number, tabs, -1)
            print('👽👽👽👽👽👽👽👽👽👽')
            last_line_flag = True

    # remove the last '\n'
    newtext = newtext[:-1]
    if tabs == 0:
        print('\n🙀🐾If I fits, I sits🐾🐈')
    else:
        print('\n🏇🔫🤖Indentation not done properly.🤖🔫🏇')
    return newtext
