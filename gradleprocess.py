import sublime, sublime_plugin
import os
from subprocess import Popen

class GradleCommand(object):
	
	def __init__(self, command):
		self._command = command
		self._popen = Popen([command, '--gradle-daemon'])
		


class GradleProcess(object):
	def __init__(self, project, view):
		self._project = project
		self._view = view
		self._command = GradleCommand(self.gradleCommand())

	def gradleCommand(self):
		gradlew = self._project.path('gradlew')
		if gradlew is None:
			for path in os.get_exec_path():
				command = os.path.join(path, 'gradle')
				if os.access(command, os.X_OK):
					return command
		else:
			return gradlew
		