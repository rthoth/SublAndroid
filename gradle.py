from .view import View
from .sublandroid_daemon import SublAndroidDaemon

class Gradle:
    
    def __init__(self, project, window):
        self._project = project
        self._window = window
        self._view = View(window)
        self._process = SublAndroidDaemon(project, self._view)

    def start(self):
        pass
