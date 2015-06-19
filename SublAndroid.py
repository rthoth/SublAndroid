import sublime
import sublime_plugin

from threading import Thread
from .gradle import Gradle
from .project import Project, has_project, search_project_folders


class SublAndroidCommand(sublime_plugin.WindowCommand):
    
    def __init__(self, *args):
        super(SublAndroidCommand, self).__init__(*args)
        self._gradle = None

    def run(self, action, tasks = []):
        if action == 'start':
            self.start()

    def is_enabled(self):
        return has_project(self.window)

    def start(self):
        if self.gradle():
            self._gradle.start()

    def gradle(self):
        if self._gradle is None:
            project = self._project()
            if project is not None:
                self._gradle = Gradle(project, self.window)

        return self._gradle

    def _project(self):
        folders = search_project_folders(self.window)
        return Project(folders[0]) if len(folders) == 1 else None