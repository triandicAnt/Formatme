# -*- coding: utf-8 -*-

import sublime
import sublime_plugin
import Formatme.regexme as rm
import Formatme.indentme as im
import Formatme.setup_me as sm

# do you want to format the whole file or only a selection?
process_all = True

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
    text_bkp = text
    text = format_me(text)
    # text = setup_me(text)
    # text = indent_me_retuns_back_from_future(text)
    # Replace the text only if it has been modified
    if text != text_bkp:
        replace_text(self, edit, region, text)

def process_selection(self, edit):
    # get user selection
    for region in self.view.sel():
        if not region.empty():
            text = self.view.substr(region)
            text = format_me(text)
            replace_text(self, edit, region, text)

def format_me(text):
    return rm.run(text)

def indent_me(text):
    return im.run(text)

def setup_me(text):
    return sm.run(text)

def replace_text(self, edit, region, text):
    self.view.replace(edit, region, text)

"""
This class removes the dirty flag from the processed tab
"""
class RemoveDirty(sublime_plugin.EventListener):
    # "save" event hook to remove dirty window
    def on_post_save_async(self, view):
        view.run_command("revert")
