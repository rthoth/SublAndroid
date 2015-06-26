import sublime_plugin
import sublime

from os.path import join, realpath, relpath

from .lib.gradle import Gradle
from .lib.project import has_project, search_project_folders


def ifgradle(func):
    def method(self, *args, **kwargs):
        if self._gradle:
            return func(self, *args, **kwargs)
    return method


class SublAndroid(sublime_plugin.WindowCommand):

    _instances = {}

    @classmethod
    def instance(cls, window, instance=None):
        id = str(window.id())
        current_instance = cls._instances[id] if id in cls._instances else None
        if instance is not None:
            cls._instances[id] = instance

        return current_instance

    def __init__(self, *args):
        super(SublAndroid, self).__init__(*args)
        self._gradle = None

        old_instance = self.instance(self.window, self)
        if old_instance:
            old_instance.shutdown()

    def shutdown(self):
        if self._gradle is not None:
            self._gradle.shutdown()

    def run(self, action, tasks=[]):
        if action == 'start':
            self.start()

    def is_enabled(self):
        return has_project(self.window.folders())

    def start(self):
        self.gradle.start()

    @property
    def gradle(self):
        if self._gradle is None:
            folders = search_project_folders(self.window.folders())
            self._folder = realpath(folders[0]) if len(folders) == 1 else None
            self._gradle = Gradle(self.resolve_path, self.window)
            self._gradle.on('end', self.on_gradle_end)

        return self._gradle

    def resolve_path(self, path=None):
        return join(self._folder, path) if path is not None else self._folder

    def on_gradle_end(self):
        sublime.error_message('OMG! Gradle is dead!')
        self._gradle.off('end', self.on_gradle_end)
        self._gradle = None

    @ifgradle
    def on_saved(self, view):
        file_name = realpath(view.file_name())
        if file_name:
            if file_name.startswith(self._folder):
                self._gradle.process(relpath(file_name, self._folder))


class Listener(sublime_plugin.EventListener):

    def on_post_save_async(self, view):
        instance = SublAndroid.instance(view.window())
        if instance:
            instance.on_saved(view)
