import sublime, sublime_plugin
import os
from subprocess import Popen

def find_java():
	# TODO: fix
	return '/usr/bin/java'

def jar():
	return os.path.join(os.path.dirname(__file__), 'sublandroid.jar')

def port():
	return 12345

class SublAndroidDaemon(object):
	def __init__(self, project, view):
		self._project = project
		self._view = view
		self._port = port()
		self._popen = Popen([find_java(), '-jar', jar(), project.path('.'), str(self._port)])
		sublime.set_async_timeout(self._try_connect, 1000)

	def _try_connect(self):
		if self._popen is None:
			self._connect()
		else:
			raise Error('SublAndroidDaemon is out!')