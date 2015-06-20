from .view import View
from .gradleprocess import GradleProcess

class Gradle:
    
    def __init__(self, project, window):
        self._project = project
        self._window = window
        self._view = View(window)
        self._process = GradleProcess(project, self._view)

    def start(self):
        pass
