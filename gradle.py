import sublime, sublime_plugin
import subprocess

from .view import View

class Gradle:
    
    def __init__(self, project, window):
        self._process = None
        self._project = project
        self._view = None
        self._window = window

    def start(self):
        if self._process is None:
            self._process = GradleProcess(self.view())

    def view(self):
        if self._view is None:
            self._view = View(self._window)
        
        return self._view

class GradleProcess(object):

    def __init__(self, view):
        view.append('SubAndroid')