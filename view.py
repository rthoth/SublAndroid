import sublime
import sublime_plugin

class View(object):

    def __init__(self, window):
        self._view = window.create_output_panel('sublandroid')
        window.run_command('show_panel', {'panel': 'output.sublandroid'})

    def append(self, str):
        self._view.run_command('subl_android_view_append', {'str': str})

class SublAndroidViewAppend(sublime_plugin.TextCommand):

    def run(self, edit, str):
        self.view.insert(edit, 0, str)