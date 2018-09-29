# -*- coding: utf-8 -*-
import Formatme.constant as CONST
import Formatme.utils as UTILS


def run(text):
    """
    @brief      set up the line for formatting. If a line contains odd
                number of `{}' or `()`, it will be split into two
                multiple lines.

    @param      line  The line

    @return     formatted line.
    """
    lines = text.strip(CONST.NEW_LINE).split(CONST.NEW_LINE)
    newtext = CONST.EMPTY_STRING
    conditional_start = False
    soql_flag = False
    line_number = 1
    for l in lines:
        orig_line = l
        l = orig_line.strip()
        # skip the commented lines and retuen statements
        if UTILS.is_line_comment(l) or l.startswith(CONST.RETURN):
           newtext += orig_line + CONST.NEW_LINE
           continue
        # skip the soql lines
        if UTILS.soql_in_same_line(l):
            soql_flag = False
        elif UTILS.start_soql_query(l):
            soql_flag = True
        elif UTILS.end_soql_query(l):
            soql_flag = False
            newtext += orig_line + CONST.NEW_LINE
            continue
        elif soql_flag:
            newtext += orig_line + CONST.NEW_LINE
            continue
        l = l.strip()

        # skip for multiline conditional and loops
        if UTILS.is_multiline_loops_and_conditionals(l):
            conditional_start = True
        elif conditional_start and l == CONST.OPEN_CURLY_BRACKET:
            conditional_start = False

        # else setup me
        elif not conditional_start:
            l = setup_me(l, CONST.OPEN_PARENTHESIS, CONST.CLOSE_PARENTHESIS)
            l = setup_me(l, CONST.OPEN_CURLY_BRACKET, CONST.CLOSE_CURLY_BRACKET)
        newtext += l + CONST.NEW_LINE
        line_number += 1
    # handle single line parenthesis
    newtext = cleanup_lines(newtext)
    return newtext.strip(CONST.NEW_LINE)

def cleanup_lines(lines):
    split_lines = lines.split(CONST.NEW_LINE)
    for i, sub_line in enumerate(split_lines):
        if i > 0 and sub_line.strip() in CONST.SINGLE_LINES:
            split_lines[i-1] += CONST.NEW_STRING + sub_line
            del(split_lines[i])
    return CONST.NEW_LINE.join(split_lines)


def setup_me(line, open_bracket, close_bracket):
    open_paren_count, close_paren_count, indices = (
        UTILS.get_bracket_count_and_index_of_unmatched(
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
        if bracket in {CONST.OPEN_PARENTHESIS, CONST.OPEN_CURLY_BRACKET}:
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
    new_line = CONST.EMPTY_STRING
    start_index = 0
    for index in indices:
        new_line += line[start_index : index + salt] + CONST.NEW_LINE
        start_index = index + salt
    new_line += line[start_index:]
    return new_line.strip(CONST.NEW_LINE)

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
        if line != CONST.OPEN_PARENTHESIS and line != close_bracket + CONST.SEMICOLON:
            return (True, close_bracket)
    return (False, CONST.EMPTY_STRING)
