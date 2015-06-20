import sublime
import sublime_plugin

from threading import Thread
from .gradle import Gradle
from .project import Project, has_project, search_project_folders

def withGradle(func):
    def funcInvoke(self, *args):
        if self._gradle is None:
            self._gradle = self.gradle();

        if self._gradle is not None:
            return func(self, *args)

    return funcInvoke


class SublAndroidCommand(sublime_plugin.WindowCommand):
    
    def __init__(self, *args):
        super(SublAndroidCommand, self).__init__(*args)
        self._gradle = None

    def run(self, action, tasks = []):
        if action == 'start':
            self.start()

    def is_enabled(self):
        return has_project(self.window)

    @withGradle
    def start(self):
        self._gradle.start()

    def gradle(self):
        project = self._project()
        return Gradle(project, self.window) if project else None

    def _project(self):
        folders = search_project_folders(self.window)
        return Project(folders[0]) if len(folders) == 1 else None