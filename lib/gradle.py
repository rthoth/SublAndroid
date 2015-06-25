from .gradle_view import GradleView
from .daemon import Daemon


class Gradle(object):

    def __init__(self, resolve_path, window):
        self._view = GradleView(window)
        self._daemon = None
        self._resolve_path = resolve_path

    @property
    def daemon(self):
        if self._daemon is None:
            self._daemon = Daemon(self._resolve_path())

        return self._daemon

    def shutdown(self):
        if not self._daemon:
            self._daemon.shutdown()

    def start(self):
        self.daemon.send({"command": "hello"}, self._on_hello)

    def _on_hello(self, hello):
        pass
