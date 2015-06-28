import sublime_plugin
import sublime
from .lib import util

from os.path import join, realpath, relpath

from .lib.gradle import Gradle
from .lib.project import has_project, search_project_folders


def ifgradle(func):
    def method(self, *args, **kwargs):
        if self._gradle:
            return func(self, *args, **kwargs)
    return method


class SublAndroid(sublime_plugin.WindowCommand):

    instances = {}

    @classmethod
    def instance(cls, window, instance=None):
        id = str(window.id())
        current_instance = cls.instances[id] if id in cls.instances else None
        if instance is not None:
            cls.instances[id] = instance

        return current_instance

    def __init__(self, *args):
        super(SublAndroid, self).__init__(*args)
        self._gradle = None

        old_instance = self.instance(self.window, self)
        if old_instance:
            old_instance.shutdown()

        self.actions = {
            "start": self.start,
            "stop": self.shutdown
        }

    def shutdown(self):
        if self._gradle:
            self._gradle.off('end', self.on_gradle_end)
            self._gradle.shutdown()
            self._gradle = None

    def run(self, action, tasks=[]):
        if action in self.actions:
            self.actions[action]()

    def is_enabled(self):
        return has_project(self.window.folders())

    def start(self):
        self.gradle.start()

    @property
    def gradle(self):
        if self._gradle is None:
            folders = search_project_folders(self.window.folders())
            self.folder = realpath(folders[0]) if len(folders) == 1 else None
            self._gradle = Gradle(self.resolve_path, self.window)
            self._gradle.once('end', self.on_gradle_end)
            self._gradle.once('failed', self.on_gradle_failed)
            self._gradle.on('java_compile_error', self.on_java_compile_error)

        return self._gradle

    def resolve_path(self, path=None):
        return join(self.folder, path) if path is not None else self.folder

    def on_gradle_end(self):
        sublime.error_message('OMG! Gradle is dead!')
        self._gradle.off('failed', self.on_gradle_failed)
        self._gradle = None

    def on_gradle_failed(self):
        self._gradle.off('end', self.on_gradle_end)

    def on_java_compile_error(self, evt, failures):
        sublime.message_dialog(str(len(failures)))
        for failure in failures:
            util.show_java_failure(failure, self.window)

    @ifgradle
    def on_saved(self, view):
        file_name = realpath(view.file_name())
        if file_name:
            if file_name.startswith(self.folder):
                self._gradle.process(relpath(file_name, self.folder))


class Listener(sublime_plugin.EventListener):

    def on_post_save_async(self, view):
        subl_android = SublAndroid.instance(view.window())
        if subl_android:
            subl_android.on_saved(view)
