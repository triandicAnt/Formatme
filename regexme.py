# -*- coding: utf-8 -*-

import re
from collections import OrderedDict

comment_pattern = r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)'
quote_pattern = r'([^\']+?)(\'.*?\'|$)'
loc_list = [0]
comment_dict = {}

def run(text):
    comment_p = re.compile(comment_pattern)
    for m in comment_p.finditer(text):
        comment_dict[m.end()] = m.end() - m.start()
    comment_ordered_dict = OrderedDict(sorted(comment_dict.items()))
    code_parts = re.split(comment_pattern, text)
    # filter out none comments and do the regex formatting
    code_parts = [x for x in code_parts if x is not None]
    code_parts = [x for x in code_parts if x.strip() not in ('*', '\n', ' ')]
    total = 0
    for i, code in enumerate(code_parts):
        # total += len(code)
        if not is_line_a_comment(code):
            changed_code = code
            # check for quotes
            l = re.split(quote_pattern, changed_code)
            l = [a for a in l if a != '']
            for j, unquoted in enumerate(l):
                new_code = unquoted
                if not is_in_quotes(new_code):
                    for (key, value, message) in regex_quote_sensitive_list:
                        # regex_pos = 0
                        new_code_temp = re.sub(key, value, new_code, flags=re.MULTILINE)
                        if new_code_temp != new_code:
                            if loc_list[0] != 0:
                                print(text[loc_list[0] : loc_list[0] + 10])
                                comment = get_comment_position(comment_ordered_dict, loc_list[0])
                                final_loc = loc_list[0]
                                if comment != 0:
                                    final_loc = comment + loc_list[0]
                                start_loc = text.count('\n', 0, final_loc) + 1
                                print('Line Number ~ ' + str(start_loc) + ' >>> ' + message)
                            else:
                                print(message)
                        loc_list[0] = 0
                        new_code = new_code_temp
                        # if loc_list:
                        #     del loc_list[-1]
                if new_code != unquoted:
                    l[j] = new_code
            changed_code = ''.join([x for x in l if x not in (' ', '\n')])
            if changed_code != code:
                code_parts[i] = changed_code
    text = ''.join([x for x in code_parts if x not in (' ', '\n')])
    for (key, value, message) in case_insensitive_list:
        new_text = re.sub(key, value, text, flags=re.MULTILINE)
        if text != new_text:
            text = new_text
            print(text[loc_list[0] : loc_list[0] + 10])
            if loc_list[0] != 0:
                start_loc = text.count('\n', 0, loc_list[0]) + 1
                print('Line Number ~ ' + str(start_loc) + ' >>> ' + message)
        loc_list[0] = 0
        # if loc_list:
        #     del loc_list[-1]
    # replace content in view while removing any trailing whitespaces.
    text = text.rstrip(' +');
    return text

############ HELPER METHODS ############

def get_comment_position(ordered_dict, pos):
    keys = list(ordered_dict.keys())
    if not keys or pos < keys[0]:
        return 0
    nearest = max(x for x in keys if x <= pos)
    return nearest
    # total_comment = 0
    # for key, value in ordered_dict.items():
    #     total_comment += value
    #     if key == nearest:
    #         break
    # return total_comment


def get_leading_spaces(statement):
    """Get the number of leading spaces in a line"""
    leading_space_count = len(statement) - len(statement.lstrip(' '))
    leading_space = ''
    while leading_space_count > 0:
        leading_space += ' '
        leading_space_count -= 1
    return leading_space

def is_line_a_comment(line):
    """Check if a line is a comment"""
    line = line.strip()
    if line.startswith('/*') or line.startswith('//'):
        return True
    return False

def is_in_quotes(code_part):
    return code_part.strip().startswith("\'")

############ REGEX FORMATTING METHODS ############
def process_singleline_loop(matchedobj):
    """Single line loops should have `{` on the same line"""
    loc_list[0] = matchedobj.start()
    return matchedobj.group(0).split('\n')[0] + ' {'

def pre_process_multiline_loop(matchedobj):
    """Multi line loops should end with `)` and have `{` on a new line"""
    x = matchedobj.group(0).split('\n')
    leading_spaces = get_leading_spaces(x[1])
    loc_list[0] = matchedobj.start()
    return x[0] + ')\n' + leading_spaces + '{'

def process_multiline_loop(matchedobj):
    """Multi line loops should have `{` on a separate new line"""
    loc_list[0] = matchedobj.start()
    stmt = matchedobj.group(0).strip('\n+')
    return stmt[:-1].strip('\n+').rstrip(' +').rstrip('\n+')+'\n' + get_leading_spaces(stmt) + '{'

def remove_test_method(matchedobj):
    """Replace `private testMethod` keyword with `@isTest` annotation"""
    loc_list[0] = matchedobj.start()
    str = '\t@isTest\n'
    m1 = matchedobj.group(1)
    if 'private ' in m1:
        x = m1.split('private ')
        str += x[0] + x[1]
    else:
        str += m1
    str += ' ' + matchedobj.group(2)
    return str

def class_name(matchedobj):
    """1 space between class declaration and `{`"""
    loc_list[0] = matchedobj.start()
    return matchedobj.group(1) + ' class ' + matchedobj.group(2).rstrip(' +') + ' {'

"""
process == true {
"""
def process_if_true(matchedobj):
    loc_list[0] = matchedobj.start()
    return matchedobj.group(1).rstrip(' +') + matchedobj.group(3)

"""
process == false
"""
def process_if_false(matchedobj):
    loc_list[0] = matchedobj.start()
    if 'if (' not in matchedobj.group(0) and 'else if (' not in matchedobj.group(0):
        return matchedobj.group(0)
    return re.sub(r'(\S)+\s*==\s*false|(\S)+\s*!=\s*true', \
        process_if_false_is_back, matchedobj.group(0), flags=re.MULTILINE)

def process_if_false_is_back(matchedobj):
    stmt = re.compile(r'\s*==\s*|\s*\!=\s*').split(matchedobj.group(0))[0].strip()
    if not stmt:
        return matchedobj.group(0)
    if stmt[0] == '(':
        return '(!{0}'.format(stmt[1:])
    return '!{0}'.format(stmt)


"""
[Before]
    }
    else {
        //
    }
[After]
    } else {
        //
    }
"""
def format_if_else_same_line(matchedobj):
    loc_list[0] = matchedobj.start()
    stmts = re.compile(r'\n*').split(matchedobj.group(0))
    if not stmts:
        return matchedobj.group(0)
    return '{0} {1}'.format(stmts[0],stmts[1].strip())

"""
process comma
"""
def process_comma(matchedobj):
    loc_list[0] = matchedobj.start()
    return matchedobj.group(1).rstrip(' +') + ' '

"""
process single line if else
[Before]
    if (true) // A
        doSomething
    else // B
        doSomethingElse
[After]
    if (true) { // A
        doSomething
    }
    else { // B
        doSomethingElse
    }
"""
def add_brackets_to_multiline_if_else(matchedobj):
    """
    SKIP|FAIL
    skip if ; is in quotes
    """
    if ";'" in matchedobj.group(0):
        return matchedobj.group(0)
    loc_list[0] = matchedobj.start()
    stmt = matchedobj.group(0).lstrip()
    if '\n' in stmt and '{' not in stmt:
        stmts = matchedobj.group(0).split('\n')
        if not stmts[0]:
            del stmts[0]
        conditional_statement = stmts[0] + ' {'
        # handle the comment if there's a comment at the end of the same line
        if '//' in stmts[0]:
            comment_splits = stmts[0].split('//')
            conditional_statement = comment_splits[0].strip() + ' { //' + comment_splits[1]
        rest = '\n'.join(stmts[1:])
        return (
            conditional_statement
            + '\n' + rest
            + '\n'
            + get_leading_spaces(stmts[0]) + '}'
        )
    return matchedobj.group(0)

"""
"""
def remove_trailing_newline(matchedobj):
    loc_list[0] = matchedobj.start()
    return '\n' + matchedobj.group(0).split('\n\n')[1]

"""
process single/double equals while ignoring comments.
The comments generally start with `\\` or `/*` or '= . Ignore
those matches and process the rest.
"""
def process_equals(matchedobj):
    stmt = matchedobj.group(0)
    # is_character_in_quotes(stmt, 'else') or "'" in stmt
    if "'" in stmt:
        return stmt
    loc_list[0] = matchedobj.start()
    if stmt:
        if '//' in stmt or '/*' in stmt:
            return stmt
        elif stmt.count('=') == 1:
            return ' = '
        elif stmt.count('=') == 2:
            return ' == '

"""
process divide by & equals while ignoring comments.
"""
def process_divide_equals(matchedobj):
    stmt = matchedobj.group(0)
    loc_list[0] = matchedobj.start()
    if stmt:
        if '//' in stmt or '/*' in stmt:
            return stmt
        else:
            return ' /= '

"""
process Single line if/else statements.
[Before]
    if (sth() && nothing()) return;
    else print(1);
[After]
    if (sth() && nothing()) {
        return;
    }
    else {
        print(1)
    }
"""
def add_brackets_to_singleline_if_else(matchedobj):
    stmt = matchedobj.group(0)
    # find the closing bracket for the if/else.
    # First find the occurence of '('
    if not stmt:
        return
    if is_character_in_quotes(stmt, 'else') or "else'" in stmt:
        return stmt
    leading_spaces = ' ' * (len(stmt) - len(stmt.lstrip('\n*').lstrip(' ')))
    stmt = stmt.strip()
    loc_list[0] = matchedobj.start()
    if 'if' in stmt or 'else if' in stmt:
        parenthesis_index = stmt.strip().index('(')
        # from parenthesis_index onwards we want to find the closing parenthesis
        count = 1
        index_count = 0
        for char in stmt.strip()[parenthesis_index + 1 : ]:
            index_count = index_count + 1
            if char == '(':
                count = count + 1
            if char == ')':
                count = count - 1
                if count == 0:
                    break
        return '{0}{1}{2}\n{3}{4}\n{5}'.format(
            leading_spaces,
            stmt[:parenthesis_index + index_count + 1],
            '{',
            leading_spaces + ' ' * 4,
            stmt[parenthesis_index + index_count +1:].strip(),
            leading_spaces + '}'
        )
    elif 'else' in stmt:
        # handle the else case
        stmts = stmt.split(' ')
        return_stmt = " ".join(stmts[1:])
        return '{0}{1}{2}\n{3}{4}\n{5}'.format(
            leading_spaces,
            stmts[0],
            ' {',
            leading_spaces + ' ' * 4,
            return_stmt.strip(),
            leading_spaces + '}'
        )
    else:
        return stmt

"""
process &&
"""
def process_double_and(matchedobj):
    loc_list[0] = matchedobj.start()
    stmt = matchedobj.group(0)
    # skip the records if it has a \n otherwise process it
    if '\n' in stmt:
        return stmt.split('&&')[0] + '&& '
    else:
        return ' && '

"""
process ||
"""
def process_double_or(matchedobj):
    loc_list[0] = matchedobj.start()
    stmt = matchedobj.group(0)
    # skip the records if it has a \n otherwise process it
    if '\n' in stmt:
        return stmt.split('||')[0] + '|| '
    else:
        return ' || '

def is_character_in_quotes(line, char):
    stmt = re.search(r'\'(.+?)\'', line)
    if not stmt:
        return False
    return char in stmt.group(0)

"""
Process assertEquals(true, val);
assert(val);
Process assertEquals(false, val);
assert(!val);
"""
def process_assert_equals(matchedobj):
    loc_list[0] = matchedobj.start()
    stmt = matchedobj.group(0)
    if not stmt:
        return
    val = matchedobj.group(1)
    if val:
        if 'true' in stmt:
            return 'System.assert({};'.format(val)
        elif 'false' in stmt:
            return 'System.assert(!{};'.format(val)
    return stmt


def at_most_2_new_lines(matchedobj):
    loc_list[0] = matchedobj.start()
    return '\n\n'

def no_space_around_semicolon(matchedobj):
    loc_list[0] = matchedobj.start()
    return r';\n'

def lowercase_select(matchedobj):
    loc_list[0] = matchedobj.start()
    return r'select '

def lowercase_from(matchedobj):
    loc_list[0] = matchedobj.start()
    return r'from '

def lowercase_where(matchedobj):
    loc_list[0] = matchedobj.start()
    return r'where '

def lowercase_limit(matchedobj):
    loc_list[0] = matchedobj.start()
    return r'limit '

def lowercase_group_by(matchedobj):
    loc_list[0] = matchedobj.start()
    return r'group by '

def lowercase_order_by(matchedobj):
    loc_list[0] = matchedobj.start()
    return r'order by '

def lowercase_having(matchedobj):
    loc_list[0] = matchedobj.start()
    return r'having '

def get_set_property(matchedobj):
    loc_list[0] = matchedobj.start()
    return '{get; set;}'

def try_condition(matchedobj):
    loc_list[0] = matchedobj.start()
    return r'try {'

def catch_condition(matchedobj):
    loc_list[0] = matchedobj.start()
    return r'} catch ('

def custom_field_rule(matchedobj):
    loc_list[0] = matchedobj.start()
    return '__c'

def custom_relation_rule(matchedobj):
    loc_list[0] = matchedobj.start()
    return '__r'

# these are no quote sensitive
case_insensitive_list = [
    ###### RULE #######                                                                     ###### DOCUMENTATION ######
    (r' *(if\s*\(|else\s*if|else)(.+);$', add_brackets_to_singleline_if_else, 'single line if/else statements should be multi-lined & enclosed with curly brackets'),              # single line if/else statements should be multi-lined & enclosed with curly brackets
    (r'^ *(if\s*\(|else|for\s*\()[^;{]+(;\')|^ *(if\s*\(|else|for\s*\()[^;{]+(;),',
        add_brackets_to_multiline_if_else, 'single line if/else/for should be enclosed with curly braces'
    ),                                                                                      # single line if/else/for should be enclosed with curly braces
    (r'\n{2,}', r'\n\n', 'at most 2 newlines'),                                                                   # at most 2 newlines
    (r' *; *\n', r';\n', 'no spaces around `;`'),                                                                   # no spaces around `;`
    # (r' +$', '', 'no trailing whitespaces'),                                                                         # no trailing whitespaces
    (r'(.+) class (.+) *{', class_name, '1 space between `SampleClass {`'),                                                    # 1 space between `SampleClass {`
    (r'(.+)(\s*==\s*true|\s*!=\s*false)(.+)', process_if_true, 'remove `== true` or `!= false`'),                             # remove `== true` or `!= false`
    (r'(.+)==\s*false\s*(.+)|(.+)!=\s*true\s*(.+)', process_if_false, 'convert `x == false|z != true ` to `!x`'),                      # convert `x == false|z != true ` to `!x`
    (r'(.+)\n *\) *\{$', pre_process_multiline_loop, 'Fix multiline loops that end with ){ on new line'),                                       # Fix multiline loops that end with '){' on new line
    (r'^ *(for\s*\(|if\s*\(|while\s*\(|} else if\s*\()[^{}]+{$', process_multiline_loop, '1 newline between multiline for loop and `{`'),   # 1 newline between multiline forloop and `{`
    (r'(for|if|while) *\(.+\)\n+ *{', process_singleline_loop, 'no newline between singline forloop and `{`'),                             # no newline between singline forloop and `{`
    (r'(?i)\bSELECT\b *' , lowercase_select, 'lowercase soql keyword `select`'),                                                     # lowercase soql keyword `select`
    (r'(?i)\bFROM\b *' , lowercase_from, 'lowercase soql keyword `from`'),                                                         # lowercase soql keyword `from`
    (r'(?i)\bWHERE\b *' , lowercase_where, 'lowercase soql keyword `where`'),                                                       # lowercase soql keyword `where`
    (r'(?i)\bLIMIT\b *' , lowercase_limit, 'lowercase soql keyword `limit`'),                                                       # lowercase soql keyword `limit`
    (r'(?i)\bGROUP BY\b *' , lowercase_group_by,'lowercase soql keyword `group by`'),                                                 # lowercase soql keyword `group by`
    (r'(?i)\bORDER BY\b *' , lowercase_order_by, 'lowercase soql keyword `order by`'),                                                 # lowercase soql keyword `order by`
    (r'(?i)\bHAVING\b *' , lowercase_having, 'lowercase soql keyword `having`'),                                                     # lowercase soql keyword `having`
    (r'\n{2}\s*}', remove_trailing_newline, 'remove trailing newline at end of functions'),                                                # remove trailing newline at end of functions
    (r'({\s*get;\s*set;\s*})',get_set_property, 'get/set for class variables'),                                               # get/set for class variables
    (r'}\n+\s*else', format_if_else_same_line, 'else/else if should start with closing } of if'),                                             # else/else if should start with closing } of if
    (r'try *\{', try_condition, '1 space between `try {`'),                                                                 # 1 space between `try {`
    (r'\} *catch *\(', catch_condition, ' 1 space between `} catch (`'),                                                       # 1 space between `} catch (`
    (r'__C\b', custom_field_rule, 'change `__C` to `__c`'),                                                                      # case sensitive `__c`
    (r'__R\b', custom_relation_rule, 'Change `__R` to `__r`'),                                                                      # case sensitive `__r`
    (r'^\s*System\.assertEquals\(true\s*,\s*(.+);$', process_assert_equals, 'assert equals true'),                # assert equals true
    (r'^\s*System\.assertEquals\(false\s*,\s*(.+);$', process_assert_equals, 'assert equals false'),               # assert equals false
]

def if_condition_single_space(matchedobj):
    loc_list[0] = matchedobj.start()
    return r'if ('

def else_condition_single_space(matchedobj):
    loc_list[0] = matchedobj.start()
    return r'} else {'

def else_if_condition_single_space(matchedobj):
    loc_list[0] = matchedobj.start()
    return r'} else if ('

def for_condition_single_space(matchedobj):
    loc_list[0] = matchedobj.start()
    return r'for ('

def while_condition_single_space(matchedobj):
    loc_list[0] = matchedobj.start()
    return r'while ('

def angle_and_curly_condition_single_space(matchedobj):
    loc_list[0] = matchedobj.start()
    return r'> {'

def parenthesis_and_curly_condition_single_space(matchedobj):
    loc_list[0] = matchedobj.start()
    return r') {'

def single_space_after_comma(matchedobj):
    loc_list[0] = matchedobj.start()
    return ', '

def no_space_before_comma(matchedobj):
    loc_list[0] = matchedobj.start()
    return r', \n'

def single_space_plus(matchedobj):
    loc_list[0] = matchedobj.start()
    return r' + '

def single_space_minus(matchedobj):
    loc_list[0] = matchedobj.start()
    return r' - '

def single_space_plus_equals(matchedobj):
    loc_list[0] = matchedobj.start()
    return r' += '

def single_space_minus_equals(matchedobj):
    loc_list[0] = matchedobj.start()
    return r' -= '

def single_space_star_equals(matchedobj):
    loc_list[0] = matchedobj.start()
    return r' *= '

def single_space_equals_greater(matchedobj):
    loc_list[0] = matchedobj.start()
    return r' => '

def single_space_not_equals(matchedobj):
    loc_list[0] = matchedobj.start()
    return r' != '

def single_space_greater_than_equals(matchedobj):
    loc_list[0] = matchedobj.start()
    return r' >= '

def single_space_less_than_equals(matchedobj):
    loc_list[0] = matchedobj.start()
    return r' <= '

def single_space_and_equals(matchedobj):
    loc_list[0] = matchedobj.start()
    return r' &= '

def single_space_or_equals(matchedobj):
    loc_list[0] = matchedobj.start()
    return r' |= '

def no_space_plus_plus(matchedobj):
    loc_list[0] = matchedobj.start()
    return r'++'

def no_space_minus_minus(matchedobj):
    loc_list[0] = matchedobj.start()
    return r'--'

# these are case sensitive
regex_quote_sensitive_list = [
    (r'if *\(', if_condition_single_space, '1 space between `if (`'),                                                                   # 1 space between `if (`
    (r'\} *else *\{', else_condition_single_space, '1 space between `} else {`'),                                                         # 1 space between `} else {`
    (r'\} *else *if *\(', else_if_condition_single_space, '1 space between `} else if (`'),                                                  # 1 space between `} else if (`
    (r'for *\(', for_condition_single_space, '1 space between `for (`'),                                                                 # 1 space between `for (`
    (r'while *\(', while_condition_single_space, '1 space between `while (`'),                                                             # 1 space between `while (`
    (r'> *\{', angle_and_curly_condition_single_space, '1 space between `> {`'),                                                                     # 1 space between `> {`
    (r'\) *\{', parenthesis_and_curly_condition_single_space, '1 space between `) {`'),                                                                    # 1 space between `) {`
    #(r'(\, *[^\'\,\'|\/|\w|\n|\(|<])', process_comma, '1 space after `, `'),                                     # 1 space after `, `
    # (r'( *\, *)', single_space_after_comma, '1 space after `, `'),                                                           # 1 space after `, `
    # (r', *\n', r', \n', 'no trailing space after `, `'),                                                                    # no trailing space after `, `
    (r'(.+) (?i)testMethod (.+)', remove_test_method, 'replace `testMethod` with `@isTest`'),                                      # replace `testMethod` with `@isTest`
    # (r'\'(.+?)\'|\'=\s*|\/\*[\s\S]*?\*\/|\/\/[\s\S].*|\s*=\s*', process_equals, '1 space around ` = `'),            # 1 space around ` = `
    # (r'\/\*[\s\S]*?\*\/|\/\/[\s\S].*|\s*=\s*=\s*', process_equals, '1 space before and after ` == `'),                         # ` == `
    # (r' *\+ *', single_space_plus, '1 space before and after `+`'),                                                                  # `+`    # broken example: '10+'
    (r' *\- *', single_space_minus, '1 space before and after `-`'),                                                                  # `-`    # broken example: 'Pre-Sale'
    (r' *\+ *= *', single_space_plus_equals, '1 space before and after `+=`'),                                                                # ` += `
    (r' *\- *= *', single_space_minus_equals, '1 space before and after `-=`'),                                                                # ` -= `
    (r' *\* *= *', single_space_star_equals, '1 space before and after `*=`'),                                                                # ` *= `
    (r' *= *> *', single_space_equals_greater, '1 space before and after `=>`'),                                                                 # ` => `
    (r'\/\*[\s\S]*?\*\/|\/\/[\s\S].*| *\/ *= *', process_divide_equals, '1 space before and after `/=`'),                    # ` /= `
    (r' *\! *= *', single_space_not_equals, '1 space before and after `!=`'),                                                                # ` != `
    (r' *> *= *', single_space_greater_than_equals, '1 space before and after `>=`'),                                                                 # ` >= `
    (r' *< *= *', single_space_less_than_equals, '1 space before and after `<=`'),                                                                 # ` <= `
    (r' *& *= *', single_space_and_equals, '1 space before and after `&=`'),                                                                 # ` &= `
    (r' *\| *= *', single_space_or_equals, '1 space before and after `|=`'),                                                                 # ` |= `
    (r' *\+\+ *| *\+  \+ *', no_space_plus_plus, '1 space before and after `++`'),                                                        # no space around `++`
    (r' *\-\- *', no_space_minus_minus, '1 space before and after `--`'),                                                                   # no space around `--`
    (r'\s*&& *', process_double_and, '1 space before and after `&&`'),                                                       # && should have 1 space before and after.
    (r'\s*\|\| *', process_double_or, '1 space before and after `||`'),                                                      # || should have 1 space before and after.
]
