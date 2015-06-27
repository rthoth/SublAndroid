from .gradle_view import GradleView
from .daemon import Daemon
from .emitter import Emitter


def onlysuccess(method):
    def _method(self, error, message):
        if not error:
            return method(self, message)

    return _method


class Gradle(Emitter):

    def __init__(self, resolve_path, window):
        self.gradleView = GradleView(window)
        self._daemon = None
        self.resolve_path = resolve_path

    @property
    def daemon(self):
        if self._daemon is None:
            self._daemon = Daemon(self.resolve_path())
            self._daemon.on('end', self.on_daemon_end)
            self._daemon.on('start_failed', self.on_daemon_failed)

        return self._daemon

    def shutdown(self):
        if self.gradleView:
            self.gradleView.info('Bye bye!')

        if self._daemon:
            self._daemon.off('end', self.on_daemon_end)
            self._daemon.shutdown()

    def start(self):
        self.daemon.send({"command": "hello"}, self.on_hello)

    def process(self, path):
        self.gradleView.info('User saved %s' % path)

    def on_daemon_end(self):
        self._daemon.off('end', self.on_daemon_end)
        self._daemon = None
        self.fire('end')

    def on_daemon_failed(self):
        self._daemon.off('end', self.on_daemon_end)
        self._daemon.off('start_failed', self.on_daemon_failed)
        self._daemon = None
        self.fire('failed')

    @onlysuccess
    def on_show_tasks(self, tasks):
        header = 'Gradle %s \n' % self.gradleVersion
        itens = ['%s: %s' % (task['name'], task['description']
                 if 'description' in task else '') for task in tasks]

        self.gradleView.info('%s\n%s' % (header, '\n'.join(itens)))

    @onlysuccess
    def on_hello(self, message):
        self.gradleVersion = message['gradleVersion']
        self.gradleMessage = message['message']
        self.gradleView.info('Gradle %s started and says %s' % (self.gradleVersion, self.gradleMessage))
        self._daemon.send({'command': 'showTasks'}, self.on_show_tasks)
