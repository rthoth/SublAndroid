import sublime
import sublime_plugin

from threading import Thread
from .gradle import Gradle
from .project import Project, has_project, search_project_folders

def withGradle(func):
    def funcInvoke(self, *args):
        if self.gradle is None:
            self.gradle = self._gradle();

        if self.gradle is not None:
            return func(self, *args)

    return funcInvoke


class SublAndroidCommand(sublime_plugin.WindowCommand):
    
    def __init__(self, *args):
        super(SublAndroidCommand, self).__init__(*args)
        SublAndroidListener
        self.gradle = None

        SublAndroidListener.instance(self.window, self)
    def run(self, action, tasks = []):
        if action == 'start':
            self.start()

    def is_enabled(self):
        return has_project(self.window)

    @withGradle
    def start(self):
        self.gradle.start()

    def _gradle(self):
        project = self._project()
        return Gradle(project, self.window) if project else None

    def _project(self):
        folders = search_project_folders(self.window)
        return Project(folders[0]) if len(folders) == 1 else None

    def on_save(self, view):
        pass


class SublAndroidListener(sublime_plugin.EventListener):

    @classmethod
    def _get_instances(cls):
        try:
            return cls.instances
        except AttributeError:
            cls.instances = {};
            return cls.instances


    @classmethod
    def instance(cls, window, subl_android = None):
        id = str(window.id())
        instances = cls._get_instances();
        if subl_android is None:
            return instances[id] if id in instances else None
        else:
            instances[id] = subl_android
            return instances[id]
            



    def on_post_save_async(self, view):
        subl_android = self.instance(view.window())
        if subl_android:
            subl_android.on_save(view)
