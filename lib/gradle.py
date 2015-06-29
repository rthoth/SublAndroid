from .gradle_view import GradleView
from .daemon import Daemon, onlysuccess
from .emitter import Emitter
from .java import Java
from os import path

SRC_PATH = 'src' + path.sep
SRC_MAIN_PATH = path.join(SRC_PATH, 'main') + path.sep
JAVA_EXTENSION = '.java'


class Gradle(Emitter):

    def __init__(self, resolve_path, window):
        self.gradle_view = GradleView(window)
        self._daemon = None
        self.resolve_path = resolve_path

    @property
    def daemon(self):
        if self._daemon is None:
            self._daemon = Daemon(self.resolve_path())
            self.java = Java(self, self._daemon)
            self._daemon.once('end', self.on_daemon_end)
            self._daemon.once('start_failed', self.on_daemon_failed)

        return self._daemon

    def shutdown(self):
        if self.gradle_view:
            self.gradle_view.info('Bye bye!')

        if self._daemon:
            self._daemon.off('end', self.on_daemon_end)
            self._daemon.shutdown()

    def start(self):
        self.daemon.send({"command": "hello"}, self.on_hello)

    def process(self, path):
        self.gradle_view.info('User saved %s' % path)

        if path.startswith(SRC_PATH):
            if path.endswith(JAVA_EXTENSION):
                self.java.saved(path)

    def on_daemon_end(self, evt):
        self._daemon.off('end', self.on_daemon_end)
        self._daemon = None
        self.fire('end')

    def on_daemon_failed(self, evt):
        self._daemon.off('end', self.on_daemon_end)
        self._daemon.off('start_failed', self.on_daemon_failed)
        self._daemon = None
        self.fire('failed')

    @onlysuccess
    def on_show_tasks(self, tasks):
        header = 'Gradle %s \n' % self.gradleVersion
        itens = ['%s: %s' % (task['name'], task['description']
                 if 'description' in task else '') for task in tasks]

        self.gradle_view.info('%s\n%s' % (header, '\n'.join(itens)))

    @onlysuccess
    def on_hello(self, message):
        self.gradleVersion = message['gradleVersion']
        self.gradleMessage = message['message']
        self.gradle_view.info('Gradle %s started and says %s' % (self.gradleVersion, self.gradleMessage))
        # self._daemon.send({'command': 'showTasks'}, self.on_show_tasks)
