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

LF = ord('\n')

ATTEMPT_DELAY = 500
MAX_ATTEMPTS = 20


def onlysuccess(method):
    def _method(self, error, message):
        if not error:
            return method(self, message)

    return _method


class Daemon(Emitter):
    def __init__(self, project_path):
        self.socket = None
        self.port = port()
        self.popen = Popen([daemon_command, project_path, str(self.port), 'debug'])
        self.attempts = 0
        self._off = False
        sublime.set_timeout_async(self.try_connect, ATTEMPT_DELAY)

    def shutdown(self):
        self._off = True
        self.popen.terminate()

    def _connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('127.0.0.1', self.port))
        self.thread = Thread(target=self.wait)
        self.thread.start()

    def try_connect(self):
        self.attempts += 1
        if self.popen.returncode is None:
            try:
                self._connect()
            except ConnectionRefusedError:
                if self.attempts <= MAX_ATTEMPTS:
                    sublime.set_timeout_async(self.try_connect, ATTEMPT_DELAY)
                else:
                    self.fire('start_failed')
        else:
            self.socket = False

    def send(self, message, callback):
        sublime.set_timeout_async(partial(self._send, message, callback))

    def _send(self, message, callback):
        if self.socket:
            data = (sublime.encode_value(message, False) + '\n').encode()
            limit = len(data)
            total_sent = 0
            while total_sent < limit:
                sent = self.socket.send(data[total_sent:])
                if sent == 0:
                    callback(RuntimeError('Comunication failed'), None)
                    return
                else:
                    total_sent += sent

            data = b''
            while True:
                chunk = self.socket.recv(4096)
                if chunk:
                    if chunk[-1] == LF:
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

        elif self.socket is None:
            sublime.set_timeout_async(partial(self._send, message, callback), ATTEMPT_DELAY)

    def wait(self):
        self.popen.wait()
        self.fire('end')
        if not self._off:
            self.fire('crash')
