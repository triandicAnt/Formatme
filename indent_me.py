# -*- coding: utf-8 -*-
import Formatme.constant as CONST


def run(text):
    lines = text.strip(CONST.NEW_LINE).split(CONST.NEW_LINE)

    tabs = 0
    diff = 0

    indent = CONST.EMPTY_STRING
    newtext = CONST.EMPTY_STRING
    tab_space = CONST.NEW_STRING * 4
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

    total_num_of_lines = len(lines)
    for i in range(0, total_num_of_lines):
        orig_line = lines[i]
        line = orig_line.strip()

        # handle comments
        if line.startswith('/*'):
            block_comment_flag = True
        elif line.endswith('*/'):
            block_comment_flag = False
        if is_line_comment(line, block_comment_flag):
            newtext += indent + orig_line + CONST.NEW_LINE
            continue
        if len(line) == 0:
            newtext += CONST.NEW_LINE
            continue

        line_number = i + 1

        # soql in the same line
        if start_soql_query(line) and end_soql_query(line):
            indent = tab_space*tabs
            soql_flag = False
            preety_print_line(line_number, tabs, 1)

        # soql
        elif soql_flag:
            indent = soql_start_indent
        elif soql_end_flag:
            indent = soql_end_indent
            soql_end_flag = False
            soql_end_indent = CONST.EMPTY_STRING
            soql_start_indent = CONST.EMPTY_STRING
        else:
            indent = tab_space*tabs

        # multiline return start
        if 'return' in line and line[-1] != CONST.SEMICOLON:
            return_flag = True
            tabs += 1
            preety_print_line(line_number, tabs, 2)

        # multiline return end
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

        # opening bracket line
        elif (
            line[-1] == CONST.OPEN_PARENTHESIS
            or line[-1] == OPEN_CURLY_BRACKET
        ):
            if is_line_conditional(line):
                indent = tab_space*(tabs-1)
            else:
                indent = tab_space*tabs
            tabs += 1
            open_bracket_flag = True
            preety_print_line(line_number, tabs, 4)

        # closing bracket line
        elif (
            line == CONST.CLOSE_PARENTHESIS + CONST.SEMICOLON
            or line == CLOSE_CURLY_BRACKET + CONST.SEMICOLON
            or line == CONST.CLOSE_PARENTHESIS
            or line == CONST.CLOSE_CURLY_BRACKET
        ):
            tabs -= 1
            indent = tab_space*tabs
            if line != CONST.CLOSE_PARENTHESIS:
                open_bracket_flag = False
            preety_print_line(line_number, tabs, 5)

        # rest of the line
        elif (
            not return_flag
            and not soql_flag
            and not start_soql_query(line)
            and not is_character_in_quotes(line, CONST.SEMICOLON)
            and not is_line_keywords(line)
        ):
            indent = tab_space*tabs
            if SEMICOLON not in line:
                if not no_semicolon_flag and not open_bracket_flag:
                    no_semicolon_flag = True
                    tabs += 1
            elif no_semicolon_flag:
                no_semicolon_flag = False
                tabs -= 1
            preety_print_line(line_number, tabs, 6)
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
            soql_start_indent += (' ' * diff) #+ tab_space

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

def is_line_comment(line, block_comment_flag):
    return (
        line.startswith('/*')
        or line.startswith('*')
        or line.endswith('*/')
        or line.startswith('//')
        or block_comment_flag
    )

def start_soql_query(line):
    return ': [' in line or '= [' in line or '([' in line

def end_soql_query(line):
     r = re.compile(r'](.+)*;$')
     return r.search(line) != None

def is_soql_end(line):
    if (
        '])' in line
        or '];' in line
        or ')];' in line
    ):
        return True
    return False

def preety_print_line(line, tabs, index):
    print(
        ('line {} tabs {}  -------> {}'
            .format(
                str(line),
                str(tabs),
                str(index),
            )
        )
    )

def is_line_keywords(line):
    line = line.strip().lower()
    return (
        line == 'override'
        or line == '@override'
        or line == '@istest'
        or line == '@testsetup'
        or line == '@testvisible'
    )

def is_character_in_quotes(line, char):
    stmt = re.search(r'\'(.+)\'', line)
    if not stmt:
        return False
    return char in stmt.group(0)

def is_line_data_structure(line):
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

def is_line_conditional(line):
    return (
        line.startswith('} else {')
        or line.startswith('} else if (')
    )