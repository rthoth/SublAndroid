import sublime, sublime_plugin

from threading import Thread
from .gradle import Gradle
from .project import Project, has_project


class SublAndroidCommand(sublime_plugin.WindowCommand):
	
	def __init__(self, *args):
		super(SublAndroidCommand, self).__init__(*args)
		

	def run(self, tasks):
		self._gradle.tasks(tasks)

	def is_enabled(self):
		return has_project(self.window)