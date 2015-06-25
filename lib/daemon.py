import sublime
import os
import socket

from subprocess import Popen
from functools import partial

daemon_command = os.path.join(os.path.dirname(__file__), '../daemon/bin/sublandroid')


def port():
    return 12345

_NL = ord('\n')


class Daemon(object):
    def __init__(self, project_path):
        self._socket = None
        self._port = port()
        self._popen = Popen([daemon_command, project_path, str(self._port), 'debug'])
        sublime.set_timeout_async(self._try_connect, 1000)

    def shutdown(self):
        pass

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
            data = sublime.encode_value(message, False).encode()
            limit = len(data)
            total_sent = 0
            sublime.message_dialog(data.decode())
            while total_sent < limit:
                sent = self._socket.send(data[total_sent:])
                if sent == 0:
                    callback(RuntimeError('Comunication failed'))
                    return
                else:
                    total_sent += sent
            data = b''
            while True:
                chunk = self._socket.recv(1)
                sublime.message_dialog(str(chunk))
                if len(chunk) == 0:
                    callback(RuntimeError('Comunication failed'))

                if chunk[0] != _NL:
                    continue
                else:
                    data += chunk
            json = data.decode()
            json = sublime.decode_value(json)
            callback(None, json)
