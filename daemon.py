import sublime, sublime_plugin
import os
import socket

from subprocess import Popen
from functools import partial


daemon_command = os.path.join(os.path.dirname(__file__), 'daemon/bin/sublandroid')


def port():
    return 12345

NL = ord('\n')

class Daemon(object):
    def __init__(self, real_path):
        self._socket = None
        self._port = port()
        sublime.message_dialog(str([daemon_command, real_path('.')]))
        self._popen = Popen([daemon_command, real_path('.'), str(self._port)])
        sublime.set_timeout_async(self._try_connect, 1000)

    def _connect(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect(('127.0.0.1', self._port))
        self._socket_file = self._socket.makefile('r', newline='\n')


    def _try_connect(self):
        if self._popen.returncode is None:
            self._connect()
        else:
            self._socket = False
            raise ChildProcessError()

    def send(self, message, callback):
        sublime.set_timeout_async(partial(self._send, message, callback))

    def _send(self, message, callback):
        if self._socket is None:
            sublime.set_timeout_async(partial(self._send, message, callback), 100)
        elif self._socket:
            json = sublime.encode_value(message, False)
            self._socket.send(json.encode())
            json = self._socket_file.readline()
            sublime.message_dialog(json);