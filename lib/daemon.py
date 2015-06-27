import sublime
import os
import socket

from subprocess import Popen
from functools import partial
from threading import Thread
from .emitter import Emitter


daemon_command = os.path.join(os.path.dirname(__file__), '../daemon/bin/sublandroid')


def port():
    return 12345

_NL = ord('\n')

_ATTEMPT_DELAY = 250
_MAX_ATTEMPTS = 10


class Daemon(Emitter):
    def __init__(self, project_path):
        self._socket = None
        self._port = port()
        self._popen = Popen([daemon_command, project_path, str(self._port), 'debug'])
        self._attempt = 0
        self._off = False
        sublime.set_timeout_async(self._try_connect, _ATTEMPT_DELAY)

    def shutdown(self):
        self._off = True
        self._popen.terminate()

    def _connect(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect(('127.0.0.1', self._port))
        self.thread = Thread(target=self.wait)
        self.thread.start()

    def _try_connect(self):
        self._attempt += 1
        if self._popen.returncode is None:
            try:
                self._connect()
            except ConnectionRefusedError:
                if self._attempt <= _MAX_ATTEMPTS:
                    sublime.set_timeout_async(self._try_connect, _ATTEMPT_DELAY)
                else:
                    self.fire('start_failed')
        else:
            self._socket = False

    def send(self, message, callback):
        sublime.set_timeout_async(partial(self._send, message, callback))

    def _send(self, message, callback):
        if self._socket:
            data = (sublime.encode_value(message, False) + '\n').encode()
            limit = len(data)
            total_sent = 0
            while total_sent < limit:
                sent = self._socket.send(data[total_sent:])
                if sent == 0:
                    callback(RuntimeError('Comunication failed'), None)
                    return
                else:
                    total_sent += sent

            data = b''
            while True:
                chunk = self._socket.recv(1024)
                if chunk:
                    if chunk[-1] == _NL:
                        data += chunk[:-1]
                        break
                    else:
                        data += chunk
                else:
                    callback(RuntimeError('Comunication failed'), None)
                    return

            json = data.decode()
            sublime.message_dialog('Gradle Response: %s.' % json)
            status = json[0]

            try:
                message = sublime.decode_value(json[1:])
            except ValueError as value_error:
                message = value_error

            if status == 'S':
                callback(None, message)
            else:
                callback(message)

        elif self._socket is None:
            sublime.set_timeout_async(partial(self._send, message, callback), _ATTEMPT_DELAY)

    def wait(self):
        self._popen.wait()
        self.fire('end')
        if not self._off:
            self.fire('crash')
