# -*- coding: utf-8 -*-
import re

def run(text):
    lines = text.strip('\n').split('\n')

    tabs = 0
    diff = 0
    akane_no_mai_count = 0
    paren_ragnarok_count = 0
    parenthesis_diff_count = 0
    parenthesis_tabs_count = 0

    indent = ''
    newtext = ''
    tab_space = ' ' * 4
    soql_start_indent = ''
    soql_end_indent = ''

    soql_flag = False
    soql_end_flag = False
    return_flag = False
    akane_no_mai_flag = False
    soql_rises_flag = False
    paren_ragnarok_flag = False
    host_awake_flag = False
    block_comment_flag = False
    no_semicolon_flag = False
    return_paren_Flag = False
    open_curly_Flag = False

    total_num_of_lines = len(lines)
    for i in range(0, total_num_of_lines):
        orig_line = lines[i]
        line = orig_line.strip()
        if line.startswith('/*'):
            block_comment_flag = True
        elif line.endswith('*/'):
            block_comment_flag = False
        if is_line_comment(line, block_comment_flag):
            newtext += orig_line + '\n'
            continue
        if len(line) == 0:
            newtext += '\n'
            continue

        line_number = i + 1
        open_parenthesis, close_parenthesis = get_parenthesis_count(line)
        # soql
        if soql_flag:
            indent = soql_start_indent
        elif soql_end_flag:
            indent = soql_end_indent
            soql_end_flag = False
            soql_end_indent = ''
            soql_start_indent = ''
        else:
            indent = tab_space*tabs

        # } and if/else/for
        if (
            not is_character_in_quotes(line, '}')
            and '}' in line
            and not soql_flag
            and akane_no_mai(line)
        ):
            tabs -= line.count('}')
            indent = tab_space*tabs
            akane_no_mai_count = open_parenthesis - close_parenthesis
            tabs += akane_no_mai_count
            abra_ca_dabra(line_number, tabs, 1)
        # multiline return start
        elif 'return' in line and line[-1] != ';':
            return_flag = True
            tabs += 1
            abra_ca_dabra(line_number, tabs, 2)
        # multiline return end
        elif return_flag and ';' in line:
            print(return_paren_Flag)
            tabs -= 1
            if (
                line.strip() == '));'
                or line.strip() == ');'
                or line.strip() == '});'
            ):
                if return_paren_Flag and len(line.strip()) > 2:
                    tabs -= 1
                    return_paren_Flag = False
                indent = tab_space*tabs
            abra_ca_dabra(line_number, tabs, 3)
            return_flag = False
        # multiline if/else if/for start
        elif (
            not soql_flag
            and not return_flag
            and not is_character_in_quotes(line, '(')
            and akane_no_mai(line)
        ):
            diff = (open_parenthesis-close_parenthesis)
            parenthesis_diff_count += diff
            if akane_no_mai_flag:
                akane_no_mai_count += diff
            else:
                akane_no_mai_count = diff
            if akane_no_mai_count > 0:
                parenthesis_tabs_count += 1
                tabs += 1
            elif akane_no_mai_count < 0:
                tabs -= 1
                parenthesis_tabs_count -= 1
            if start_soql_query(line):
                parenthesis_diff_count = 0
                parenthesis_tabs_count = 0
            abra_ca_dabra(line_number, tabs, 4)
            akane_no_mai_flag = True
        elif (
            not soql_flag
            and ('));' == line
            or ');' == line
            or '});' == line
            or ')' == line)
        ):
            paren_ragnarok_flag = False
            akane_no_mai_count -= line.count(')')
            # parenthesis_diff_count -= 1
            # if line == '});':
            #     tabs -= 2
            #     parenthesis_diff_count = 0
            #     parenthesis_tabs_count = 0
            if ';' in line and parenthesis_tabs_count != 0:
                tabs -= parenthesis_tabs_count
                parenthesis_diff_count = 0
                parenthesis_tabs_count = 0
            elif ';' in line and parenthesis_tabs_count == 0:
                parenthesis_diff_count = 0
                parenthesis_tabs_count = 0
            else:
                tabs -= 1
                parenthesis_diff_count -= 1
                parenthesis_tabs_count -= 1
            akane_no_mai_flag = False
            indent = tab_space*tabs
            abra_ca_dabra(line_number, tabs, 10)
        # multiline if/else if/for start
        elif (
            not soql_flag
            and not return_flag
            #and line[-1] == ')'
            and akane_no_mai_flag
            and not return_of_parenthesis(line)
            and close_parenthesis > open_parenthesis
        ):
            open_count, close_count = get_parenthesis_count(line)
            diff_count = close_count-open_count
            parenthesis_diff_count += open_count - close_count
            if paren_ragnarok_flag:
                if (
                    diff_count > 0 and
                    diff_count < (akane_no_mai_count + paren_ragnarok_count)
                ):
                    tabs -= 1
                    parenthesis_tabs_count -= 1
                else:
                    tabs -= 2
                    parenthesis_tabs_count -= 2
                paren_ragnarok_count = 0
                paren_ragnarok_flag = False
            elif parenthesis_tabs_count > 0:
                tabs -= 1
                parenthesis_tabs_count -= 1
            akane_no_mai_count += open_count - close_count
            if akane_no_mai_count == 0:
                akane_no_mai_flag = False
            # if line == ')':
            if ';' in line:
                indent = tab_space*tabs
            if (
                parenthesis_diff_count == 0
                and parenthesis_tabs_count != 0
            ):
                tabs -= parenthesis_tabs_count
                parenthesis_tabs_count = 0
            abra_ca_dabra(line_number, tabs, 5)
        # )] and ]; with multiline if/else/for
        elif les_ecorchés(line) and akane_no_mai_flag:
            tabs -= 1
            akane_no_mai_count = 0
            abra_ca_dabra(line_number, tabs, 6)
            akane_no_mai_flag = False
        # multiline ) statement end
        elif (
            not soql_flag
            and not return_flag
            and virtù_e_fortuna(line)
        ):
            tabs -= 1
            abra_ca_dabra(line_number, tabs, 7)
        # multiline statement start
        elif (
            not return_flag
            and not soql_flag
            and not is_character_in_quotes(line, '(')
            and not is_character_in_quotes(line, ')')
            and not return_of_parenthesis(line)
            and parenthesis_ragnarok(line) > 0
        ):
            paren_count = parenthesis_ragnarok(line)
            if not paren_ragnarok_flag:
                paren_ragnarok_count = paren_count
            else:
                paren_ragnarok_count += paren_count
            paren_ragnarok_flag = True
            curly_diff = curly_contrapasso(line)
            if curly_diff != 0:
                tabs += curly_diff
            # tabs += paren_count
            if paren_count > 0:
                tabs += 1
            elif paren_count < 0:
                tabs -= 1
            abra_ca_dabra(line_number, tabs, 8)
        # multiline statement end
        elif (
            not return_flag
            and paren_ragnarok_flag
            and parenthesis_rises(line)
        ):
            paren_ragnarok_flag = False
            curly_diff = curly_contrapasso(line)
            # if curly_diff != 0:
            #     tabs += curly_diff
            # tabs -= paren_ragnarok_count
            total_diff = curly_diff + paren_ragnarok_count
            if total_diff > 0:
                tabs += 1
            elif total_diff < 0:
                tabs -= 1
            if line == '});':
                indent = tab_space*tabs
            paren_ragnarok_count = 0
            abra_ca_dabra(line_number, tabs, 9)
        elif '}' in line and '{' in line and line[0] == '}':
            indent = tab_space*(tabs-1)
            open_count = line.count('{')
            close_count = line.count('}')
            if open_count > close_count:
                tabs += open_count - close_count
            elif open_count < close_count:
                tabs -= close_count - open_count
            abra_ca_dabra(line_number, tabs, 11)
        elif '}' in line and '{' in line:
            indent = tab_space*tabs
            abra_ca_dabra(line_number, tabs, 12)
        elif '{' in line:
            indent = tab_space*tabs
            tabs += line.count('{')
            if return_flag:
                return_paren_Flag = True
            if is_line_data_structure(line):
                open_curly_Flag = True
            if akane_no_mai_flag:
                parenthesis_diff_count += line.count('{')
                parenthesis_tabs_count += line.count('{')
            abra_ca_dabra(line_number, tabs, 13)
        elif '}' in line:
            tabs -= line.count('}')
            if open_curly_Flag:
                open_curly_Flag = False
            if akane_no_mai_flag:
                open_count,close_count = get_parenthesis_count(line)
                parenthesis_diff_count += open_count - close_count
                parenthesis_tabs_count -= line.count('}')
            indent = tab_space*tabs
            abra_ca_dabra(line_number, tabs, 14)
        # soql in the same line
        elif start_soql_query(line) and end_soql_query(line):
            indent = tab_space*tabs
            soql_flag = False
            abra_ca_dabra(line_number, tabs, 16)
        elif (
            not return_flag
            and not soql_flag
            and not akane_no_mai_flag
            and not open_curly_Flag
            and not start_soql_query(line)
            and not is_character_in_quotes(line, ';')
            and not is_line_keywords(line)
        ):
            indent = tab_space*tabs
            if ';' not in line:
                if not no_semicolon_flag:
                    no_semicolon_flag = True
                    tabs += 1
            elif no_semicolon_flag:
                no_semicolon_flag = False
                tabs -= 1
            abra_ca_dabra(line_number, tabs, 15)
        else:
            print('🤷🤷‍♀️🤷‍♀️lines are awake🙄🙄🙄 {}'.format(str(line_number)))

        # handle the fishy comma
        # if peaky_blinders_comma(line):
        #     line = red_right_hand(line)

        newline = indent + line.rstrip()
        newtext += newline  + '\n'

        if start_soql_query(line) and end_soql_query(line):
            continue

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
        if (
            '])' in newline
            or '];' in newline
            or ')];' in newline
        ):
            soql_flag = False
            soql_end_flag = True
            new_len = len(indent)-diff
            soql_end_indent = ' ' * new_len

        # Find the line that's awake
        if (
            line_number != total_num_of_lines
            and not host_awake_flag
            and tabs == 0
        ):
            print('😱😱😱😱😱Only boring people get bored😱😱😱😱😱')
            abra_ca_dabra(line_number, tabs, -1)
            print('👽👽👽It doesn\'t look like anything to me👽👽👽')
            host_awake_flag = True

    # remove the last '\n'
    newtext = newtext[:-1]
    if tabs == 0:
        print('\n🙀🐾If I fits, I sits🐾🐈')
    else:
        print('\n🏇🔫🤖violent delights have violent ends🤖🔫🏇')
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
    # return '];' in line
     r = re.compile(r'](.+)*;$')
     return r.search(line) != None

def get_parenthesis_count(line):
    open_count = line.count('(')
    close_count = line.count(')')
    return (open_count,close_count)

def red_right_hand(line):
    """
    1.Split by comma
        If line contains
        (1) .split(
        (2) = ','
        (3) = ', '
        then skip it.
        Divide and rule
    """
    if (
        '.split(' in line
        or "= ','" in line
        or "= ', '" in line
    ):
        return line
    # split line by comma and join them together with spaces
    segments = line.split(',')
    if len(segments) == 0:
        return line
    """
    method1('param1','param2'   ,    'param3');
    [method1('param1','param2'   ,    'param3');]
    """
    final_statement = elephant_stone_strip(segments[0])
    prev_word = final_statement
    for word in segments[1:]:
        if fools_gold(word):
            final_statement += ','
        else:
            final_statement += ', '
        final_statement += elephant_stone_strip(word)
        prev_word = word
    return final_statement

def peaky_blinders_comma(line):
    return ',' in line

def fools_gold(word):
    # return true if `'` is odd else false
    return word.count("'")%2 == 1

def elephant_stone_strip(word):
    if fools_gold(word):
        return word
    return word.strip()

def akane_no_mai(line):
    open_parenthesis,close_parenthesis = get_parenthesis_count(line)
    if (
        (
            'if (' in line
            or 'for (' in line
            or line[-1] == '('
            or (
                parenthesis_ragnarok(line) > 0
                and not return_of_parenthesis(line)
            )
        )
        and open_parenthesis > close_parenthesis
    ):
        return True
    return False

def virtù_e_fortuna(line):
    open_parenthesis, close_parenthesis = get_parenthesis_count(line)
    if line [-1] == ')' and close_parenthesis > open_parenthesis:
        return True
    return False

def les_ecorchés(line):
    if (
        '])' in line
        or '];' in line
        or ')];' in line
    ):
        return True
    return False

def parenthesis_ragnarok(line):
    open_parenthesis,close_parenthesis = get_parenthesis_count(line)
    return open_parenthesis - close_parenthesis

def parenthesis_rises(line):
    open_parenthesis,close_parenthesis = get_parenthesis_count(line)
    if (
        len(line) > 2
        and (line [-1] == ')' or line[-2:] == ');')
        and close_parenthesis > open_parenthesis
    ):
        return True
    return False

def abra_ca_dabra(line, tabs, index):
    print(
        ('line {} tabs {}  -------> {}'
            .format(
                str(line),
                str(tabs),
                str(index),
            )
        )
    )

def return_of_parenthesis(line):
    return (
        "'(" in line
        # or "('" in line
        # or "')" in line
        or ")'" in line
    )

def curly_contrapasso(line):
    open_count = line.count('{')
    close_count = line.count('}')
    return open_count - close_count

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
