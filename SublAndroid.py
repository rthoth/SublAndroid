import sublime_plugin

from os.path import join

from .lib.gradle import Gradle
from .lib.project import has_project, search_project_folders


class SublAndroid(sublime_plugin.WindowCommand):

    _instances = {}

    @classmethod
    def _instance(cls, window, instance=None):
        id = str(window.id())
        current_instance = cls._instances[id] if id in cls._instances else None
        if instance is not None:
            cls._instances[id] = instance

        return current_instance

    def __init__(self, *args):
        super(SublAndroid, self).__init__(*args)
        self._gradle = None

        old_instance = self._instance(self.window, self)
        if old_instance is not None:
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
            self._folder = folders[0] if len(folders) == 1 else None
            self._gradle = Gradle(self.resolve_path, self.window)

        return self._gradle

    def resolve_path(self, path=None):
        return join(self._folder, path) if path is not None else self._folder

    def on_save(self, view):
        pass


class Listener(sublime_plugin.EventListener):

    def on_post_save_async(self, view):
        pass
