# -*- coding: utf-8 -*-

import sublime
import sublime_plugin
import re
from collections import OrderedDict
from Formatme.regexme import regex_dict
import Formatme.indentme

# do you want to format the whole file or only a selection?
process_all = True

"""
Usage : Select the text you want to format and press: CRTL + B
        Or Right click and select `Formatme->Format me`

PS : Please expect a little misbehavior of the code as its not trained for few unseen circumstances.
"""

class FormatmeCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        # only execute on Apex classes ending with `.cls`
        file_name = self.view.window().active_view().file_name()
        if not file_name or not file_name.endswith('.cls'):
            return
        if process_all:
            process_whole_file(self, edit) # format the entire file
        else:
            process_selection(self, edit) # format only the selected text

def process_whole_file(self, edit):
    # select all text
    region = sublime.Region(0, self.view.size())
    text = self.view.substr(region)
    text = format_me(self, edit, region, text)
    text = indent_me_returns(self, edit, region, text)
    replace_text(self, edit, region, text)

def process_selection(self, edit):
    # get user selection
    for region in self.view.sel():
        # if selection not empty then
        if not region.empty():
            text = self.view.substr(region)
            text = format_me(self, edit, region, text)
            replace_text(self, edit, region, text)

def format_me(self, edit, region, text):
    for key, value in regex_dict.items():
        text = re.sub(key, value, text, flags=re.MULTILINE)
    # replace content in view while removing any trailing whitespaces.
    text = text.rstrip(' +');
    return text

def indent_me(self, edit, region, text):
    return indent_me_returns(self, edit, region, text)

def replace_text(self, edit, region, text):
    self.view.replace(edit, region, text)

"""
This class removes the dirty flag from the processed tab
"""
class RemoveDirty(sublime_plugin.EventListener):
    # "save" event hook to remove dirty window
    def on_post_save_async(self, view):
        view.run_command("revert")
