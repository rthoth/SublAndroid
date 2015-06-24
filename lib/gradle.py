from .view import View
from .daemon import Daemon

class Gradle:

    def __init__(self, project, window):
        self._project = project
        self._window = window
        self._view = View(window)
        self._daemon = None

    def daemon(self):
        if self._daemon is None:
            self._daemon = Daemon(self._project.path)

        return self._daemon

    def start(self):
        self.daemon().send({"command": "hello"}, self._onHello)

    def _onHello(self, hello):
        message