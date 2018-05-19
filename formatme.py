# -*- coding: utf-8 -*-

import sublime
import sublime_plugin
import re
from collections import OrderedDict
import Formatme.indentme as indent # import with module name
from Formatme.regexme import regex_dict

# do you want to format the whole file or only a selection?
process_all = True

"""
Usage : Select the text you want to format and press: CRTL + B
        Or Right click and select `Formatme->Format me`

PS : Please expect a little misbehavior of the code as its not trained for few unseen circumstances.
"""


class FormatmeCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        indent.whattheheck() # call your awesome method
        # only execute on Apex classes ending with `.cls`
        file_name = self.view.window().active_view().file_name()
        if not file_name or not file_name.endswith('.cls'):
            return
        if process_all:
            process_whole_file(self, edit) # format the entire file
        else:
            process_selection(self, edit) # format only the selected text

def process_whole_file(self, edit):
    """
    This method process whole file
    """
    # select all text
    region = sublime.Region(0, self.view.size())
    text = self.view.substr(region)
    text = format_me(self, edit, region, text)
    # text = fix_indentation(self, edit, region, text)

def process_selection(self, edit):
    """
    This method processes the selection
    """
    # get user selection
    for region in self.view.sel():
        # if selection not empty then
        if not region.empty():
            text = self.view.substr(region)
            format_me(self, edit, region, text)

def format_me(self, edit, region, text):
    """
    this method is responsible to do the formatting
    """
    for key, value in regex_dict.items():
        text = re.sub(key, value, text, flags=re.MULTILINE)
    # replace content in view while removing any trailing whitespaces.
    text = text.rstrip(' +');
    self.view.replace(edit, region, text)
    return text

def fix_indentation(self, edit, region, text):
    lines = text.split('\n')
    tabs = 0
    newtext = ''
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            newtext += '\n'
            continue
        is_comment = is_line_comment(line)
        if (line.startswith('}') or line.startswith(')')) and not is_comment:
            tabs -= 1
        newline = ' ' * (tabs * 4)
        newline += line
        if (line.endswith('{') or line.endswith('(')) and not is_comment:
            tabs += 1
        newtext += newline + '\n'
    newtext = newtext[:-1] # remove the last '\n'
    self.view.replace(edit, region, newtext)

def is_line_comment(line):
    return line.startswith('//') or line.startswith('/*') or line.startswith('*') or line.endswith('*/')

"""
This class removes the dirty flag from the processed tab
"""
class RemoveDirty(sublime_plugin.EventListener):
    # "save" event hook to remove dirty window
    def on_post_save_async(self, view):
        view.run_command("revert")
