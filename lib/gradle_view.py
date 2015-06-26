import sublime_plugin


def show(method):
    def _method(self, *args, **kwargs):
        self._window.run_command('show_panel', {'panel': 'output.%s' % self.output_name})
        return method(self, *args, **kwargs)

    return _method


class GradleView(object):

    output_name = 'sublandroid'

    def __init__(self, window):
        self._window = window
        self._view = window.create_output_panel(self.output_name)

    @show
    def info(self, str):
        self._view.run_command('subl_android_view_append', {'str': str})


class SublAndroidViewAppend(sublime_plugin.TextCommand):

    def run(self, edit, str):
        self.view.insert(edit, self.view.size(), str)
        self.view.insert(edit, self.view.size(), '\n')
