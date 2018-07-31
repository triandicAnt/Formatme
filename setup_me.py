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
    block_comment_flag = False

    for l in lines:
        orig_line = l
        l = orig_line.strip()
        # skip the commented lines
        if l.startswith(CONST.COMMENT_START):
            block_comment_flag = True
        elif l.endswith(CONST.COMMENT_END):
            block_comment_flag = False
        if (
            UTILS.is_line_comment(l, block_comment_flag)
            or l.startswith(CONST.RETURN)
        ):
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
